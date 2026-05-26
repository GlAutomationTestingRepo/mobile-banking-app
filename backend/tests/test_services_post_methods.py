from datetime import datetime
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import (
    Account,
    AccountLimit,
    AccountTypeName,
    AccountsBalance,
    Base,
    Card,
    CardStatus,
    CardType,
    Customer,
    CustomerGender,
    CustomerStatus,
    Transaction,
    TransactionHistory,
    TransactionStatus,
    TransactionTypeName,
)
from app.models import RetiredAccountId, RetiredCustomerId
from app.services_accounts import create_account, delete_account
from app.services_cards import create_card
from app.services_customers import create_customer, delete_customer
from app.services_transactions import create_transaction, transfer_money
from app.services_accounts import create_account_balance


def _build_test_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return test_session()


def _create_two_customers(db):
    customer_1 = create_customer(
        db,
        name="Alice",
        lastname="Stone",
        email="alice@example.com",
        phone="+111111111",
        gender=CustomerGender.F,
        birth_date=datetime(1995, 1, 15),
        status=CustomerStatus.Active,
        country="USA",
        nationality="American",
        login="alice_login",
        password="alice_password",
    )
    customer_2 = create_customer(
        db,
        name="Bob",
        lastname="Ray",
        email="bob@example.com",
        phone="+222222222",
        gender=CustomerGender.M,
        birth_date=datetime(1990, 6, 3),
        status=CustomerStatus.Pending,
        country="Canada",
        nationality="Canadian",
        login="bob_login",
        password="bob_password",
    )
    return customer_1, customer_2


def _create_two_accounts(db, customer_1_id, customer_2_id):
    account_1 = create_account(
        db,
        customer_id=customer_1_id,
        account_name="Alice Main",
        account_type=AccountTypeName.Current_Main,
        initial_balance=Decimal("1200.50"),
        currency="USD",
        limit_type="daily",
        limit_max_amount=Decimal("5000.00"),
    )
    account_2 = create_account(
        db,
        customer_id=customer_2_id,
        account_name="Bob Savings",
        account_type=AccountTypeName.Savings,
        initial_balance=Decimal("300.00"),
        currency="USD",
    )
    return account_1, account_2


def test_create_customer_two_queries_and_validate_data():
    db = _build_test_session()
    try:
        customer_1, customer_2 = _create_two_customers(db)

        all_customers = db.query(Customer).order_by(Customer.Customer_ID.asc()).all()
        assert len(all_customers) == 2
        assert customer_1.Customer_Email == "alice@example.com"
        assert customer_2.Customer_Email == "bob@example.com"
        assert all_customers[0].Customer_Name == "Alice"
        assert all_customers[1].Customer_Status == CustomerStatus.Pending
    finally:
        db.close()


def test_create_account_two_queries_and_validate_data():
    db = _build_test_session()
    try:
        customer_1, customer_2 = _create_two_customers(db)
        account_1, account_2 = _create_two_accounts(db, customer_1.Customer_ID, customer_2.Customer_ID)

        accounts = db.query(Account).order_by(Account.Account_ID.asc()).all()
        balances = db.query(AccountsBalance).order_by(AccountsBalance.Balance_ID.asc()).all()
        limits = db.query(AccountLimit).order_by(AccountLimit.Limits_ID.asc()).all()

        assert len(accounts) == 2
        assert len(balances) == 2
        assert len(limits) == 1
        assert account_1.Account_Name == "Alice Main"
        assert account_2.Account_Type == AccountTypeName.Savings
        assert Decimal(balances[0].Balance) == Decimal("1200.50")
        assert Decimal(balances[1].Balance) == Decimal("300.00")
    finally:
        db.close()


def test_create_card_two_queries_and_validate_data():
    db = _build_test_session()
    try:
        customer_1, customer_2 = _create_two_customers(db)
        account_1, account_2 = _create_two_accounts(db, customer_1.Customer_ID, customer_2.Customer_ID)

        card_1 = create_card(
            db,
            account_id=account_1.Account_ID,
            card_number="1234123412341234",
            card_type=CardType.Debit_Card,
            expiration_date=datetime(2030, 1, 1),
            status=CardStatus.Active,
            is_active=True,
        )
        card_2 = create_card(
            db,
            account_id=account_2.Account_ID,
            card_number="4321432143214321",
            card_type=CardType.Credit_Card,
            expiration_date=datetime(2031, 6, 1),
            status=CardStatus.Inactive,
            is_active=False,
        )

        cards = db.query(Card).order_by(Card.Card_ID.asc()).all()
        assert len(cards) == 2
        assert card_1.Card_Number == "1234123412341234"
        assert card_2.Card_Number == "4321432143214321"
        assert cards[0].Card_Status == CardStatus.Active
        assert cards[1].Is_Active is False
    finally:
        db.close()


def test_create_two_cards_per_account_limit_is_enforced():
    db = _build_test_session()
    try:
        customer_1, _ = _create_two_customers(db)
        account_1, _ = _create_two_accounts(db, customer_1.Customer_ID, customer_1.Customer_ID)

        create_card(
            db,
            account_id=account_1.Account_ID,
            card_number="1111111111111111",
            card_type=CardType.Debit_Card,
            expiration_date=datetime(2030, 1, 1),
            status=CardStatus.Active,
            is_active=True,
        )
        create_card(
            db,
            account_id=account_1.Account_ID,
            card_number="2222222222222222",
            card_type=CardType.Credit_Card,
            expiration_date=datetime(2031, 1, 1),
            status=CardStatus.Active,
            is_active=True,
        )

        did_raise = False
        try:
            create_card(
                db,
                account_id=account_1.Account_ID,
                card_number="3333333333333333",
                card_type=CardType.Debit_Card,
                expiration_date=datetime(2032, 1, 1),
                status=CardStatus.Active,
                is_active=True,
            )
        except ValueError:
            did_raise = True

        assert did_raise is True
    finally:
        db.close()


def test_create_three_balances_per_account_limit_is_enforced():
    db = _build_test_session()
    try:
        customer_1, _ = _create_two_customers(db)
        account_1, _ = _create_two_accounts(db, customer_1.Customer_ID, customer_1.Customer_ID)

        # One balance is created with the account already. Add two more (total 3).
        create_account_balance(db, account_id=account_1.Account_ID, balance=Decimal("10.00"), currency="EUR")
        create_account_balance(db, account_id=account_1.Account_ID, balance=Decimal("20.00"), currency="GBP")

        did_raise = False
        try:
            create_account_balance(db, account_id=account_1.Account_ID, balance=Decimal("30.00"), currency="JPY")
        except ValueError:
            did_raise = True

        assert did_raise is True
    finally:
        db.close()


def test_create_transaction_two_queries_and_validate_data():
    db = _build_test_session()
    try:
        customer_1, customer_2 = _create_two_customers(db)
        account_1, account_2 = _create_two_accounts(db, customer_1.Customer_ID, customer_2.Customer_ID)

        tx_1 = create_transaction(
            db,
            account_id=account_1.Account_ID,
            amount=Decimal("150"),
            type_name=TransactionTypeName.Deposit,
            status=TransactionStatus.Created,
            details="First deposit",
            recipient_account_id=account_1.Account_ID,
            recipient_customer_id=customer_1.Customer_ID,
        )
        tx_2 = create_transaction(
            db,
            account_id=account_2.Account_ID,
            amount=Decimal("75"),
            type_name=TransactionTypeName.Payment,
            status=TransactionStatus.Pending,
            details="Card payment",
            recipient_account_id=account_1.Account_ID,
            recipient_customer_id=customer_1.Customer_ID,
        )

        transactions = db.query(Transaction).order_by(Transaction.Transaction_ID.asc()).all()
        assert len(transactions) == 2
        assert tx_1.Amount_Of_Transaction == 150
        assert tx_2.Transaction_Status == TransactionStatus.Pending
        assert transactions[0].Transaction_Details == "First deposit"
        assert transactions[1].Type_ID is not None
    finally:
        db.close()


def test_deleted_customer_id_cannot_be_reused():
    db = _build_test_session()
    try:
        customer, _ = _create_two_customers(db)
        customer_id = customer.Customer_ID
        assert delete_customer(db, customer_id) is True

        did_raise = False
        try:
            create_customer(
                db,
                customer_id=customer_id,
                name="Reuse",
                lastname="Test",
                email="reuse@example.com",
                phone="+999999999",
                gender=CustomerGender.M,
                birth_date=datetime(1990, 1, 1),
                country="USA",
                nationality="American",
                login="reuse_login",
                password="reuse_password",
            )
        except ValueError:
            did_raise = True

        assert did_raise is True
        assert db.get(RetiredCustomerId, customer_id) is not None
    finally:
        db.close()


def test_deleted_account_id_cannot_be_reused():
    db = _build_test_session()
    try:
        customer_1, customer_2 = _create_two_customers(db)
        account_1, _ = _create_two_accounts(db, customer_1.Customer_ID, customer_2.Customer_ID)
        account_id = account_1.Account_ID
        assert delete_account(db, account_id) is True

        did_raise = False
        try:
            create_account(
                db,
                account_id=account_id,
                customer_id=customer_2.Customer_ID,
                account_name="Reused ID Account",
                account_type=AccountTypeName.Savings,
            )
        except ValueError:
            did_raise = True

        assert did_raise is True
        assert db.get(RetiredAccountId, account_id) is not None
    finally:
        db.close()


def test_transfer_money_two_queries_and_validate_data():
    db = _build_test_session()
    try:
        customer_1, customer_2 = _create_two_customers(db)
        account_1, account_2 = _create_two_accounts(db, customer_1.Customer_ID, customer_2.Customer_ID)

        transfer_1 = transfer_money(
            db,
            from_account_id=account_1.Account_ID,
            to_account_id=account_2.Account_ID,
            amount=Decimal("100"),
            details="Transfer one",
        )
        transfer_2 = transfer_money(
            db,
            from_account_id=account_1.Account_ID,
            to_account_id=account_2.Account_ID,
            amount=Decimal("50"),
            details="Transfer two",
        )

        balances = (
            db.query(AccountsBalance)
            .filter(AccountsBalance.Account_ID.in_([account_1.Account_ID, account_2.Account_ID]))
            .order_by(AccountsBalance.Account_ID.asc())
            .all()
        )
        history_rows = db.query(TransactionHistory).order_by(TransactionHistory.History_ID.asc()).all()
        transfer_rows = (
            db.query(Transaction)
            .filter(Transaction.Transaction_ID.in_([transfer_1.Transaction_ID, transfer_2.Transaction_ID]))
            .order_by(Transaction.Transaction_ID.asc())
            .all()
        )

        assert len(transfer_rows) == 2
        assert all(row.Transaction_Status == TransactionStatus.Completed for row in transfer_rows)
        assert Decimal(balances[0].Balance) == Decimal("1050.50")
        assert Decimal(balances[1].Balance) == Decimal("450.00")
        assert len(history_rows) == 4
    finally:
        db.close()
