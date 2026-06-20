# CV-İş Eşleştirme, Cover-Letter ve Analizi

## Amaç
Kişinin özgeçmişinin başvuracağı işe olan uyumu hesaplanır. Bu uyum analizine göre motivasyon mektubu (cover letter) oluşturulur. İş ilanına göre de teknik ve davranışsal mülakat soruları, bu sorulara göre de stratejik cevaplar üretilir.

## Teknolojiler
- Python 3.11
- LangChain + LangGraph (conditional branching)
- Pinecone (vector DB, serverless)
- BM25 + Cross-Encoder reranking (hybrid retrieval)
- LangSmith (tracing & monitoring)
- Streamlit (geçici UI — Görev 5'te React'e geçilecek)

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
streamlit run app.py
```

## LangSmith Dashboard

Her analiz çalıştığında tüm LLM çağrıları, prompt'lar, token sayıları ve latency otomatik olarak LangSmith'e gönderilir.

1. https://smith.langchain.com adresine git
2. `cv-job-analyzer` projesini aç
3. **Traces** sekmesinde her bir pipeline run'ını görebilirsin:
   - Her node'un (CV analizi, iş analizi, uyum, cover letter, mülakat) süresi
   - Token kullanımı ve maliyet
   - Tam prompt ve LLM cevabı
   - Hata varsa stack trace

LangSmith açmak için **kod değişikliği gerekmiyor** — sadece `.env`'deki `LANGCHAIN_API_KEY`'i doldurman yeterli. Boş bırakırsan tracing otomatik kapanır, uygulama normal çalışır.
