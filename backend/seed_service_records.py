"""Seed real DB with sample records created through service methods."""

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.database import SessionLocal
from app.models import (
    AccountTypeName,
    CardStatus,
    CardType,
    CustomerGender,
    CustomerStatus,
    TransactionTypeName,
)
from app.services_accounts import create_account
from app.services_cards import create_card
from app.services_customers import create_customer
from app.services_transactions import create_transaction, transfer_money


def main() -> None:
    suffix = uuid4().hex[:8]
    db = SessionLocal()
    try:
        # 1) create_customer x2
        customer_1 = create_customer(
            db,
            name="SeedAlice",
            lastname="Seed",
            email=f"seed.alice.{suffix}@example.com",
            phone="+111111111",
            gender=CustomerGender.F,
            birth_date=datetime(1995, 1, 15),
            status=CustomerStatus.Active,
            country="USA",
            nationality="American",
            login=f"seed_alice_{suffix}",
            password="seed_password_1",
        )
        customer_2 = create_customer(
            db,
            name="SeedBob",
            lastname="Seed",
            email=f"seed.bob.{suffix}@example.com",
            phone="+222222222",
            gender=CustomerGender.M,
            birth_date=datetime(1990, 6, 3),
            status=CustomerStatus.Pending,
            country="Canada",
            nationality="Canadian",
            login=f"seed_bob_{suffix}",
            password="seed_password_2",
        )

        # 2) create_account x2
        account_1 = create_account(
            db,
            customer_id=customer_1.Customer_ID,
            account_name=f"Seed Alice Main {suffix}",
            account_type=AccountTypeName.Current_Main,
            initial_balance=Decimal("1200.50"),
            currency="USD",
            limit_type="daily",
            limit_max_amount=Decimal("5000.00"),
        )
        account_2 = create_account(
            db,
            customer_id=customer_2.Customer_ID,
            account_name=f"Seed Bob Savings {suffix}",
            account_type=AccountTypeName.Savings,
            initial_balance=Decimal("300.00"),
            currency="USD",
        )

        # 3) create_card x2
        create_card(
            db,
            account_id=account_1.Account_ID,
            card_number=f"41111111{suffix}",
            card_type=CardType.Debit_Card,
            expiration_date=datetime(2030, 1, 1),
            status=CardStatus.Active,
            is_active=True,
        )
        create_card(
            db,
            account_id=account_2.Account_ID,
            card_number=f"42222222{suffix}",
            card_type=CardType.Credit_Card,
            expiration_date=datetime(2031, 6, 1),
            status=CardStatus.Inactive,
            is_active=False,
        )

        # 4) create_transaction x2
        create_transaction(
            db,
            account_id=account_1.Account_ID,
            amount=Decimal("150"),
            type_name=TransactionTypeName.Deposit,
            details=f"Seed deposit {suffix}",
            recipient_account_id=account_1.Account_ID,
            recipient_customer_id=customer_1.Customer_ID,
        )
        create_transaction(
            db,
            account_id=account_2.Account_ID,
            amount=Decimal("75"),
            type_name=TransactionTypeName.Payment,
            details=f"Seed payment {suffix}",
            recipient_account_id=account_1.Account_ID,
            recipient_customer_id=customer_1.Customer_ID,
        )

        # 5) transfer_money x2
        transfer_money(
            db,
            from_account_id=account_1.Account_ID,
            to_account_id=account_2.Account_ID,
            amount=Decimal("100"),
            details=f"Seed transfer one {suffix}",
        )
        transfer_money(
            db,
            from_account_id=account_1.Account_ID,
            to_account_id=account_2.Account_ID,
            amount=Decimal("50"),
            details=f"Seed transfer two {suffix}",
        )

        print("Seed data created with suffix:", suffix)
        print("Customer IDs:", customer_1.Customer_ID, customer_2.Customer_ID)
        print("Account IDs:", account_1.Account_ID, account_2.Account_ID)
    finally:
        db.close()


if __name__ == "__main__":
    main()
