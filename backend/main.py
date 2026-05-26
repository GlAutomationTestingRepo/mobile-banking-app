"""FastAPI application entrypoint exposing basic banking operations.

Run from the `backend` folder:
    python -m uvicorn main:app --reload
"""

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    AccountCreate,
    AccountOut,
    AccountUpdate,
    BalanceCreate,
    BalanceOut,
    CardCreate,
    CardOut,
    CardUpdate,
    CustomerCreate,
    CustomerOut,
    CustomerUpdate,
    TransactionCreate,
    TransactionOut,
    TransferRequest,
)
from app.services_accounts import (
    create_account,
    create_account_balance,
    delete_account,
    get_account_balance,
    get_account_by_id,
    list_account_balances,
    update_account_name,
)
from app.services_cards import create_card, get_card_by_id, update_card_status
from app.services_customers import (
    create_customer,
    delete_customer,
    get_customer_by_id,
    update_customer,
)
from app.services_transactions import (
    cancel_transaction,
    create_transaction,
    get_transaction_history,
    transfer_money,
)

app = FastAPI(title="Mobile Banking API")


@app.get("/")
def root() -> dict:
    return {"message": "Mobile Banking API is running"}


# --------------------
# Customers
# --------------------


@app.post("/customers", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def api_create_customer(payload: CustomerCreate, db: Session = Depends(get_db)) -> CustomerOut:
    try:
        customer = create_customer(
            db,
            customer_id=payload.customer_id,
            name=payload.name,
            lastname=payload.lastname,
            email=payload.email,
            phone=payload.phone,
            gender=payload.gender,
            birth_date=payload.birth_date,
            status=payload.status,
            country=payload.country,
            nationality=payload.nationality,
            login=payload.login,
            password=payload.password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return customer


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    if not delete_customer(db, customer_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")


@app.get("/customers/{customer_id}", response_model=CustomerOut)
def api_get_customer(customer_id: int, db: Session = Depends(get_db)) -> CustomerOut:
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@app.patch("/customers/{customer_id}", response_model=CustomerOut)
def api_update_customer(
    customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)
) -> CustomerOut:
    customer = update_customer(
        db,
        customer_id,
        name=payload.name,
        lastname=payload.lastname,
        email=payload.email,
        phone=payload.phone,
        gender=payload.gender,
        birth_date=payload.birth_date,
        status=payload.status,
        country=payload.country,
        nationality=payload.nationality,
    )
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


# --------------------
# Accounts
# --------------------


@app.post("/accounts", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def api_create_account(payload: AccountCreate, db: Session = Depends(get_db)) -> AccountOut:
    try:
        account = create_account(
            db,
            account_id=payload.account_id,
            customer_id=payload.customer_id,
            account_name=payload.account_name,
            account_type=payload.account_type,
            initial_balance=payload.initial_balance,
            currency=payload.currency,
            limit_type=payload.limit_type,
            limit_max_amount=payload.limit_max_amount,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return account


@app.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_account(account_id: int, db: Session = Depends(get_db)) -> None:
    if not delete_account(db, account_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


@app.get("/accounts/{account_id}", response_model=AccountOut)
def api_get_account(account_id: int, db: Session = Depends(get_db)) -> AccountOut:
    account = get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@app.patch("/accounts/{account_id}", response_model=AccountOut)
def api_update_account(
    account_id: int, payload: AccountUpdate, db: Session = Depends(get_db)
) -> AccountOut:
    account = update_account_name(
        db,
        account_id,
        account_name=payload.account_name,
        account_type=payload.account_type,
    )
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@app.get("/accounts/{account_id}/balance", response_model=BalanceOut)
def api_get_balance(account_id: int, db: Session = Depends(get_db)) -> BalanceOut:
    balance = get_account_balance(db, account_id)
    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found")
    return balance


@app.get("/accounts/{account_id}/balances", response_model=List[BalanceOut])
def api_list_balances(account_id: int, db: Session = Depends(get_db)) -> List[BalanceOut]:
    return list_account_balances(db, account_id)


@app.post(
    "/accounts/{account_id}/balances",
    response_model=BalanceOut,
    status_code=status.HTTP_201_CREATED,
)
def api_create_balance(
    account_id: int,
    payload: BalanceCreate,
    db: Session = Depends(get_db),
) -> BalanceOut:
    try:
        return create_account_balance(
            db,
            account_id=account_id,
            balance=payload.balance,
            currency=payload.currency,
            is_limited=payload.is_limited,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


# --------------------
# Cards
# --------------------


@app.post("/cards", response_model=CardOut, status_code=status.HTTP_201_CREATED)
def api_create_card(payload: CardCreate, db: Session = Depends(get_db)) -> CardOut:
    try:
        card = create_card(
            db,
            account_id=payload.account_id,
            card_number=payload.card_number,
            card_type=payload.card_type,
            expiration_date=payload.expiration_date,
            status=payload.status,
            is_active=payload.is_active,
        )
        return card
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@app.get("/cards/{card_id}", response_model=CardOut)
def api_get_card(card_id: int, db: Session = Depends(get_db)) -> CardOut:
    card = get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card


@app.patch("/cards/{card_id}", response_model=CardOut)
def api_update_card(
    card_id: int, payload: CardUpdate, db: Session = Depends(get_db)
) -> CardOut:
    card = update_card_status(
        db,
        card_id,
        status=payload.status,
        is_active=payload.is_active,
    )
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card


# --------------------
# Transactions
# --------------------


@app.post("/transactions", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def api_create_transaction(
    payload: TransactionCreate, db: Session = Depends(get_db)
) -> TransactionOut:
    tx = create_transaction(
        db,
        account_id=payload.account_id,
        amount=payload.amount,
        type_name=payload.type_name,
        status=payload.status,
        details=payload.details,
        recipient_account_id=payload.recipient_account_id,
        recipient_customer_id=payload.recipient_customer_id,
    )
    return tx


@app.post(
    "/transactions/transfer",
    response_model=TransactionOut,
    status_code=status.HTTP_201_CREATED,
)
def api_transfer_money(payload: TransferRequest, db: Session = Depends(get_db)) -> TransactionOut:
    try:
        tx = transfer_money(
            db,
            from_account_id=payload.from_account_id,
            to_account_id=payload.to_account_id,
            amount=payload.amount,
            details=payload.details,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return tx


@app.get("/transactions/history", response_model=List[TransactionOut])
def api_get_transaction_history(
    account_id: int | None = None,
    customer_id: int | None = None,
    db: Session = Depends(get_db),
) -> List[TransactionOut]:
    txs = get_transaction_history(db, account_id=account_id, customer_id=customer_id)
    return txs


@app.post("/transactions/{transaction_id}/cancel", response_model=TransactionOut)
def api_cancel_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
) -> TransactionOut:
    tx = cancel_transaction(db, transaction_id=transaction_id)
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return tx

