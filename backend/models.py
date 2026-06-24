from typing import Literal, Optional
from pydantic import BaseModel, Field


class MatchAnalysis(BaseModel):
    uyum_puani: int = Field(..., ge=0, le=100)
    eslesen_beceriler: list[str] = []
    eksik_beceriler: list[str] = []
    genel_degerlendirme: str = ""


class AnalysisResponse(BaseModel):
    id: str
    baslik: str
    tarih: str
    match: MatchAnalysis
    gelisim_onerileri: str


class HistoryItem(BaseModel):
    id: str
    baslik: str
    tarih: str
    uyum_puani: Optional[int] = None


class HistoryList(BaseModel):
    items: list[HistoryItem]


FeedbackCategory = Literal["bug", "idea", "other"]


class FeedbackCreate(BaseModel):
    category: FeedbackCategory
    message: str = Field(..., min_length=3, max_length=4000)
    page_url: Optional[str] = Field(default=None, max_length=2048)


class FeedbackResponse(BaseModel):
    id: str
    created_at: str
