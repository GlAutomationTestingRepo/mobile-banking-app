# Mobile Banking App

FastAPI backend for mobile banking.

## Install (first time)

From `backend`:

1. Create venv (optional but recommended):
   - `python -m venv .venv`
2. Activate venv (PowerShell):
   - `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`

In PyCharm: **File → Open** → `Mobile Banking App`, then set **Python Interpreter** to `backend\.venv`.

## Run locally in PyCharm (SQLite, no Docker)

From `backend` (activate venv first if you use one):

1. Activate venv (PowerShell):
   - `.\.venv\Scripts\Activate.ps1`
2. Use SQLite (default) — do **not** set `DATABASE_URL` in `.env`:
   - if `.env` has `DATABASE_URL=postgresql+...`, remove that line or delete `.env`
   - database file: `banking.db`
3. Create tables:
   - `python init_db.py`
4. Start API:
   - `python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`
5. Open API docs in browser:
   - `http://127.0.0.1:8000/docs`
6. Open root endpoint:
   - `http://127.0.0.1:8000/`

Expected root response:
- `{"message":"Mobile Banking API is running"}`

PyCharm: terminal working directory `backend`, interpreter `backend\.venv`. Or **Run → Edit Configurations → Python**: module `uvicorn`, parameters `main:app --reload --host 127.0.0.1 --port 8000`, working directory `backend`.

## Run tests

From `backend`:

1. Install pytest (once):
   - `pip install pytest`
2. Run tests:
   - `pytest tests/ -q`

## API helper scripts

With the API running, see [backend/scripts/api_methods/README.md](backend/scripts/api_methods/README.md).

## Optional: PostgreSQL with Docker

From project root (`Mobile Banking App`):

1. Start only DB:
   - `docker compose up -d db`
2. Check status:
   - `docker compose ps`
3. Stop DB when done:
   - `docker compose down`

From `backend`:

1. Create `backend/.env` with:
   - `DATABASE_URL=postgresql+psycopg2://banking:banking_dev@localhost:5432/banking`
2. Create tables:
   - `python init_db.py`
3. Start API:
   - `python -m uvicorn main:app --reload`

Or run API + DB in Docker from project root:
- `docker compose up -d --build`
- `docker compose down`

## Business rules (IDs)

After a **Customer_ID** or **Account_ID** is deleted, that ID is retired and cannot be reused. Deleting a customer also retires all of that customer's account IDs.

If you already had a database, run `python init_db.py` again to add `retired_customer_ids` and `retired_account_ids` tables.
