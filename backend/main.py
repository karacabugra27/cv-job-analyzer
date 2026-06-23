import os
import sys
import tempfile
import uuid
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import run_pipeline
from backend.auth import CurrentUser, get_current_user
from backend.cache import (
    analysis_cache_key,
    get_cached_analysis,
    set_cached_analysis,
)
from backend.db import get_session
from backend.models import AnalysisResponse, HistoryItem, HistoryList
from backend.models_db import Analysis
from backend.rate_limit import enforce_rate_limit
from backend.redis_client import get_redis

app = FastAPI(title="Liyakat API", version="0.3.0")

_default_origins = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,https://liyakat.vercel.app"
cors_origins = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", _default_origins).split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _to_response(row: Analysis) -> AnalysisResponse:
    return AnalysisResponse(
        id=str(row.id),
        baslik=row.baslik,
        tarih=row.tarih.isoformat(),
        match=row.match,
        gelisim_onerileri=row.gelisim_onerileri,
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/me")
def me(user: CurrentUser = Depends(get_current_user)):
    return {"id": str(user.id), "email": user.email}


@app.delete("/api/me")
async def delete_me(
    user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await session.execute(delete(Analysis).where(Analysis.user_id == user.id))
    await session.commit()

    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
    if not service_key or not supabase_url:
        raise HTTPException(
            status_code=500,
            detail="Sunucu yapılandırması eksik (SUPABASE_SERVICE_ROLE_KEY).",
        )

    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.delete(
            f"{supabase_url}/auth/v1/admin/users/{user.id}",
            headers={
                "apikey": service_key,
                "Authorization": f"Bearer {service_key}",
            },
        )
        if res.status_code not in (200, 204):
            raise HTTPException(
                status_code=502,
                detail=f"Supabase hesabı silinemedi: {res.text}",
            )

    return {"deleted": str(user.id)}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(
    cv_file: UploadFile = File(...),
    job_text: str = Form(...),
    baslik: str = Form(...),
    user: CurrentUser = Depends(enforce_rate_limit),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    if cv_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Sadece PDF dosyası kabul edilir.")

    contents = await cv_file.read()
    cache_key = analysis_cache_key(contents, job_text)

    cached = await get_cached_analysis(redis, cache_key)
    if cached is not None:
        result = cached
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        try:
            result = run_pipeline(tmp_path, job_text)
        finally:
            os.unlink(tmp_path)
        await set_cached_analysis(redis, cache_key, result)

    row = Analysis(
        id=uuid.uuid4(),
        user_id=user.id,
        baslik=baslik,
        match=result["match"],
        gelisim_onerileri=result["gelisim_onerileri"],
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return _to_response(row)


@app.get("/api/history", response_model=HistoryList)
async def get_history(
    user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Analysis)
        .where(Analysis.user_id == user.id)
        .order_by(Analysis.tarih.desc())
    )
    rows = result.scalars().all()
    items = [
        HistoryItem(
            id=str(r.id),
            baslik=r.baslik,
            tarih=r.tarih.isoformat(),
            uyum_puani=r.match.get("uyum_puani") if isinstance(r.match, dict) else None,
        )
        for r in rows
    ]
    return HistoryList(items=items)


@app.get("/api/history/{record_id}", response_model=AnalysisResponse)
async def get_history_detail(
    record_id: uuid.UUID,
    user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    row = await session.get(Analysis, record_id)
    if row is None or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")
    return _to_response(row)


@app.delete("/api/history/{record_id}")
async def delete_history(
    record_id: uuid.UUID,
    user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    row = await session.get(Analysis, record_id)
    if row is None or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")
    await session.execute(delete(Analysis).where(Analysis.id == record_id))
    await session.commit()
    return {"deleted": str(record_id)}
