# API method scripts

These scripts call your FastAPI endpoints from terminal.

## Install (first time)

From `backend`:

1. Create venv (optional but recommended):
   - `python -m venv .venv`
2. Activate venv (PowerShell):
   - `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`

## Run with Docker Compose (API + PostgreSQL)

From project root (`Mobile Banking App`):

1. Build and start all services:
   - `docker compose up -d --build`
2. Check status:
   - `docker compose ps`
3. Open API docs in browser:
   - `http://127.0.0.1:8000/docs`
4. Open root endpoint:
   - `http://127.0.0.1:8000/`
5. Stop services when done:
   - `docker compose down`

Expected root response:
- `{"message":"Mobile Banking API is running"}`

## Run DB only + backend locally (alternative)

From project root (`Mobile Banking App`):

1. Start only DB:
   - `docker compose up -d db`
2. Check status:
   - `docker compose ps`
3. Stop DB when done:
   - `docker compose down`

## Configure local backend to use Docker PostgreSQL

From `backend` (PowerShell), if you run API locally via `uvicorn`:

1. Set database URL for current terminal:
   - `$env:DATABASE_URL="postgresql+psycopg2://banking:banking_dev@localhost:5432/banking"`
2. Create tables:
   - `python init_db.py`
3. Start API:
   - `uvicorn main:app --reload`

## Script API URL (optional)

If scripts should call a different API URL, set:
- `$env:API_BASE_URL="http://127.0.0.1:8000"`

## New methods you should see in `/docs`

- `POST /accounts/{account_id}/balances` (add new balance row, max 3 per account)
- `GET /accounts/{account_id}/balances` (list all balances of account)
- `POST /cards` now enforces max 2 cards per account
- `POST /transactions/{transaction_id}/cancel` (works for transactions and payments)

## POST scripts

- `python scripts/api_methods/post_customers.py` (creates a customer with unique email/login)
- `python scripts/api_methods/post_accounts.py`
- `python scripts/api_methods/post_cards.py` (generates unique card number)
- `python scripts/api_methods/post_cards_two_for_account.py` (create 1-2 cards for one account, max 2 total)
- `python scripts/api_methods/post_transactions.py`
- `python scripts/api_methods/post_transactions_transfer.py`
- `python scripts/api_methods/post_transactions_cancel.py`
- `python scripts/api_methods/post_payments_cancel.py` (same as cancel transaction; payments are transactions)
- `python scripts/api_methods/post_account_balances_multi.py` (create 2-3 balances for one account, max 3 total)

## GET scripts (interactive in terminal)

- `python scripts/api_methods/get_customers_by_id.py`
- `python scripts/api_methods/get_accounts_by_id.py`
- `python scripts/api_methods/get_accounts_balance.py`
- `python scripts/api_methods/get_cards_by_id.py`
- `python scripts/api_methods/get_transactions_history.py`

Each GET script asks you what ID/filter to use and then prints response status + JSON body.

