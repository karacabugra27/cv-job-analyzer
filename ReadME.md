# Liyakat — CV ve İş İlanı Uyum Analizi

CV'nizi ve başvurmak istediğiniz iş ilanını yükleyin, yapay zekâ destekli bir pipeline pozisyona ne kadar uyduğunuzu hesaplasın, eksik becerilerinizi çıkartsın ve sizi o pozisyona yaklaştıracak somut gelişim önerileri üretsin.

Üretim ortamında: **[liyakat.vercel.app](https://liyakat.vercel.app)**

---

## Ne yapar?

1. CV PDF'inizi okur, anlam ve anahtar kelime bazlı **hibrit arama** (BM25 + vektör + cross-encoder rerank) ile en alâkalı bölümleri çıkartır.
2. CV ve iş ilanını dört aşamalı bir **LangGraph** pipeline'ından geçirir:
   - CV analiz → İş ilanı analiz → Uyum analizi → Gelişim önerileri
3. 0–100 arası uyum puanı, eşleşen / eksik beceri listesi ve kişiselleştirilmiş gelişim planı döner.
4. Tüm analizler kullanıcıya özel olarak saklanır, geçmişten tekrar açılabilir veya silinebilir.

## Mimari

```
Browser
   │  (Supabase JWT)
   ▼
Frontend (Vite + React + TS + Tailwind v4 + shadcn/ui, Vercel)
   │  /api/* (Bearer token)
   ▼
FastAPI Backend (Railway, Docker)
   ├─ Auth         → Supabase JWT (HS256 / ES256)
   ├─ Rate limit   → Upstash Redis  (3/gün, 1/dk per user)
   ├─ Cache        → Upstash Redis  (24h, cv+jd hash key)
   ├─ Pipeline     → LangGraph + Pinecone + OpenAI
   ├─ Tracing      → LangSmith
   ├─ Error mon.   → Sentry
   └─ DB           → Supabase Postgres (RLS açık, alembic migration)
```

### Kullanılan teknolojiler

| Katman | Teknoloji |
|---|---|
| LLM orkestrasyon | LangChain + **LangGraph** (koşullu node grafı) |
| Vektör DB | **Pinecone** (serverless), namespace başına bir CV |
| Retrieval | BM25 (lokal) + Pinecone + cross-encoder rerank, citation enforcement |
| Embedding | OpenAI `text-embedding-3-small` |
| Tracing | **LangSmith** (otomatik chain tracing) |
| Hata izleme | **Sentry** (backend + frontend) |
| Backend | FastAPI (async), SQLAlchemy 2.x + asyncpg, Alembic |
| Auth | **Supabase Auth** (JWT, JWKS rotasyonu destekli) |
| DB | Supabase Postgres + Row Level Security |
| Cache / rate limit | Upstash Redis |
| Frontend | React 19, Vite, TypeScript, Tailwind v4, shadcn/ui, React Query, Zustand, sonner |
| Deploy | Railway (backend), Vercel (frontend), Docker |

## Repo yapısı

```
.
├── backend/                FastAPI uygulaması (auth, cache, rate limit, endpoint'ler)
├── langchain_pipeline/     LangGraph state + node'lar + 4 chain
│   ├── chains/             CV analyst, job analyst, match analyst, gelişim önerileri
│   ├── state.py            GraphState TypedDict
│   ├── nodes.py            Node fonksiyonları
│   └── graph.py            StateGraph kurulumu
├── rag/                    Retrieval katmanı
│   ├── document_loader.py  pypdf ile PDF → chunk
│   ├── vector_store.py     Pinecone index yönetimi
│   ├── bm25_retriever.py   Lokal BM25
│   ├── hybrid_retriever.py BM25 + Pinecone birleştirme
│   ├── reranker.py         Cross-encoder rerank
│   └── citation_enforcer.py Chunk ID'leri ile prompt
├── monitoring/             LangSmith ve Sentry kurulumları
├── alembic/                DB migration'ları (analyses tablosu + RLS)
├── frontend/               React + Vite uygulaması
├── legacy/                 Eski CrewAI + ChromaDB + Streamlit kodu (referans)
├── pipeline.py             RAG → LangGraph entegrasyon noktası
├── docker-compose.yml
└── requirements.txt
```

## Lokal kurulum

### Gereksinimler

- Python 3.11
- Node 20+
- (Opsiyonel) Docker, eğer container ile çalıştırmak isterseniz
- Aşağıdaki servislerde ücretsiz hesaplar:
  - OpenAI API key
  - Pinecone (serverless index)
  - Supabase (Postgres + Auth)
  - Upstash Redis
  - LangSmith (opsiyonel, tracing için)
  - Sentry (opsiyonel, hata izleme için)

### 1) Repo'yu klonla ve env hazırla

```bash
git clone <repo-url> cv-job-analyzer
cd cv-job-analyzer
cp .env.example .env
# .env'i kendi anahtarlarınla doldur (aşağıdaki tabloya bak)
```

### 2) Backend

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# DB tablolarını oluştur (analyses + RLS politikaları)
alembic upgrade head

# API'yi çalıştır
uvicorn backend.main:app --reload --port 8000
```

Sağlık kontrolü: <http://localhost:8000/healthz>

### 3) Frontend

```bash
cd frontend
cp .env.example .env.local   # yoksa aşağıdaki anahtarları kendin oluştur
npm install
npm run dev
```

Uygulama <http://localhost:5173> adresinde çalışır. Vite proxy lokal dev'de backend'i `:8000`'den otomatik proxler — `VITE_API_BASE_URL`'i boş bırakmak yeterli.

### 4) Docker ile (opsiyonel)

```bash
docker compose up --build
```

## Ortam değişkenleri

### Backend (`.env`)

| Anahtar | Açıklama |
|---|---|
| `OPENAI_API_KEY` | OpenAI key (LLM + embedding) |
| `PINECONE_API_KEY` | Pinecone serverless key |
| `PINECONE_INDEX_NAME` | Index adı, yoksa otomatik oluşur |
| `DATABASE_URL` | `postgresql+asyncpg://...` (Supabase Postgres) |
| `SUPABASE_URL` | `https://<proj>.supabase.co` |
| `SUPABASE_JWT_SECRET` | Supabase Settings → API → JWT secret |
| `SUPABASE_SERVICE_ROLE_KEY` | Hesap silme endpoint'i için, **gizli tut** |
| `REDIS_URL` | Upstash Redis URL'i |
| `CORS_ORIGINS` | Virgülle ayrılmış frontend origin'leri |
| `LANGCHAIN_TRACING_V2` | `true` ise LangSmith aktif |
| `LANGCHAIN_API_KEY` | LangSmith key (boşsa tracing pasif) |
| `LANGCHAIN_PROJECT` | LangSmith proje adı |
| `SENTRY_DSN` | Backend Sentry DSN (boşsa Sentry pasif) |
| `SENTRY_ENVIRONMENT` | `development` / `production` |
| `SENTRY_TRACES_SAMPLE_RATE` | Performance sampling, `0.0`–`1.0` (varsayılan `0.1`) |

### Frontend (`frontend/.env.local`)

| Anahtar | Açıklama |
|---|---|
| `VITE_SUPABASE_URL` | Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase anon key |
| `VITE_API_BASE_URL` | Production backend URL'i. Lokal dev'de boş bırak (Vite proxy). |
| `VITE_SENTRY_DSN` | Frontend Sentry DSN (boşsa Sentry pasif) |
| `VITE_SENTRY_ENVIRONMENT` | `development` / `production` |

## Pipeline akışı

```
PDF → chunk → BM25 + Pinecone hybrid search → cross-encoder rerank
    → citation prompt
    → LangGraph:  CV Analiz → İş İlanı Analiz → Uyum Analizi → Gelişim Önerileri
    → JSON sonuç (uyum puanı, eşleşen/eksik beceri, gelişim metni)
```

Her CV içeriği MD5 ile namespace'lenir, böylece farklı kullanıcıların CV chunk'ları birbirine karışmaz.

## Gözlemlenebilirlik

- **LangSmith** — Tüm LLM çağrıları, prompt'lar, token sayıları ve latency otomatik kaydedilir. <https://smith.langchain.com> → `cv-job-analyzer` projesi → **Traces** sekmesi.
- **Sentry** — Backend (FastAPI integration) ve frontend (React + BrowserTracing) production hatalarını DSN'le yakalar. Lokal dev'de DSN boş bırakılırsa devre dışı kalır.

## Geri bildirim

Uygulamada sağ alttaki **Geri bildirim** butonundan hata raporu veya öneri gönderilebilir. Mesajlar `feedback` tablosuna düşer; oturum açmış kullanıcının `user_id`'si de yazılır.

## Üretim deploy

- **Backend** → Railway, repo kökündeki `backend/Dockerfile` ile build. Env değişkenleri Railway dashboard'ından set edilir.
- **Frontend** → Vercel, root = `frontend/`. `vercel.json` SPA rewrite'larını içerir.
- **Vector DB** → Pinecone cloud (serverless), free tier yeterli.
- **DB & Auth** → Supabase managed.
- **Redis** → Upstash serverless.

## Lisans ve katkı

Hobi/portföy projesidir. Issue veya PR açmadan önce kısa bir konu başlığıyla sorabilirsiniz.
