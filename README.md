# quantdev

This repo currently contains **OpenQuant** (in `openquant/`): a Next.js frontend + FastAPI backend.

## Run (local dev)

Frontend (http://localhost:3000):

```bash
cd openquant
npm install
npm run dev
```

Backend API (optional, http://localhost:8000):

```bash
cd openquant/apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tests (API)

```bash
cd openquant/apps/api
pip install -r requirements-dev.txt
pytest
```

If `npm`/Next.js has issues on very new Node versions, use Node 20.x.

## Run (Docker Compose)

Prereq: Docker Desktop installed.

```bash
cd openquant
cp .env.example .env
# set at least NEXTAUTH_SECRET (and optionally OPENAI_API_KEY)
docker compose up --build
```

Stop:

```bash
cd openquant
docker compose down
```
