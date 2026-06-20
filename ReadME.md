# CV-İş Eşleştirme ve Gelişim Analizi

## Amaç
Kişinin özgeçmişinin başvuracağı işe olan uyumu hesaplanır. Bu analiz üzerinden eşleşen/eksik beceriler çıkarılır ve adayın profilini iş ilanına yaklaştıracak somut gelişim önerileri üretilir.

## Teknolojiler
- Python 3.11
- LangChain + LangGraph
- Pinecone (vector DB, serverless)
- BM25 + Cross-Encoder reranking (hybrid retrieval)
- LangSmith (tracing & monitoring)
- FastAPI backend + React (Vite + TS + Tailwind v4 + shadcn/ui) frontend

## Kurulum

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`.env` dosyasını oluştur:
```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk-...
PINECONE_INDEX_NAME=cv-job-analyzer
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_PROJECT=cv-job-analyzer
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

Çalıştır:
```bash
# Backend
uvicorn backend.main:app --reload

# Frontend (ayrı terminal)
cd frontend && npm install && npm run dev
```

## LangSmith Dashboard

Her analiz çalıştığında tüm LLM çağrıları, prompt'lar, token sayıları ve latency otomatik olarak LangSmith'e gönderilir.

1. https://smith.langchain.com adresine git
2. `cv-job-analyzer` projesini aç
3. **Traces** sekmesinde her bir pipeline run'ını görebilirsin:
   - Her node'un (CV analizi, iş analizi, uyum, gelişim önerileri) süresi
   - Token kullanımı ve maliyet
   - Tam prompt ve LLM cevabı
   - Hata varsa stack trace

LangSmith açmak için **kod değişikliği gerekmiyor** — sadece `.env`'deki `LANGCHAIN_API_KEY`'i doldurman yeterli. Boş bırakırsan tracing otomatik kapanır, uygulama normal çalışır.
