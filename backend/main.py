import os
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import run_pipeline
from backend import storage
from backend.models import (
    AnalysisResponse,
    HistoryItem,
    HistoryList,
    MatchAnalysis,
)

app = FastAPI(title="Liyakat AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(
    cv_file: UploadFile = File(...),
    job_text: str = Form(...),
    baslik: str = Form(...),
):
    if cv_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Sadece PDF dosyası kabul edilir.")

    contents = await cv_file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = run_pipeline(tmp_path, job_text)
    finally:
        os.unlink(tmp_path)

    record = {
        "id": str(uuid.uuid4()),
        "baslik": baslik,
        "tarih": datetime.now().isoformat(),
        "match": result["match"],
        "gelisim_onerileri": result["gelisim_onerileri"],
    }
    storage.save_record(record)
    return AnalysisResponse(**record)


@app.get("/api/history", response_model=HistoryList)
def get_history():
    records = storage.list_records()
    items = [
        HistoryItem(
            id=r["id"],
            baslik=r["baslik"],
            tarih=r["tarih"],
            uyum_puani=r.get("match", {}).get("uyum_puani"),
        )
        for r in records
    ]
    return HistoryList(items=items)


@app.get("/api/history/{record_id}", response_model=AnalysisResponse)
def get_history_detail(record_id: str):
    record = storage.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")
    return AnalysisResponse(**record)


@app.delete("/api/history/{record_id}")
def delete_history(record_id: str):
    deleted = storage.delete_record(record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")
    return {"deleted": record_id}
