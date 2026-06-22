FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch \
    && pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY langchain_pipeline/ ./langchain_pipeline/
COPY rag/ ./rag/
COPY monitoring/ ./monitoring/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY pipeline.py ./

ENV HF_HOME=/app/.cache/huggingface \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
