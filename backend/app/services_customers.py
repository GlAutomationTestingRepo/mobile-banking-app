"""Customer-related database operations."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Customer, CustomerAuth, CustomerGender, CustomerStatus


def _hash_password(raw_password: str) -> str:
    """Very simple password hashing placeholder."""
    import hashlib

    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def create_customer(
    db: Session,
    *,
    name: str,
    lastname: str,
    email: str,
    phone: str,
    gender: CustomerGender,
    birth_date: datetime,
    status: CustomerStatus = CustomerStatus.Active,
    country: str,
    nationality: str,
    login: str,
    password: str,
) -> Customer:
    """Create a new customer and auth record in a single transaction."""
    customer = Customer(
        Customer_Name=name,
        Customer_Lastname=lastname,
        Customer_Email=email,
        Customer_Phone=phone,
        Customer_Gender=gender,
        Customer_BirthDate=birth_date,
        Customer_Status=status,
        Customer_Country=country,
        Customer_Nationality=nationality,
    )
    db.add(customer)
    db.flush()  # populate Customer_ID

    auth = CustomerAuth(
        CustomerID=customer.Customer_ID,
        Customer_Login=login,
        Customer_Password_Hash=_hash_password(password),
    )
    db.add(auth)

    db.commit()
    db.refresh(customer)
    return customer


def get_customer_by_id(db: Session, customer_id: int) -> Optional[Customer]:
    """Return customer with basic info by Customer_ID."""
    return db.get(Customer, customer_id)


def update_customer(
    db: Session,
    customer_id: int,
    *,
    name: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    gender: Optional[CustomerGender] = None,
    birth_date: Optional[datetime] = None,
    status: Optional[CustomerStatus] = None,
    country: Optional[str] = None,
    nationality: Optional[str] = None,
) -> Optional[Customer]:
    """Update customer fields that are provided; returns updated customer or None."""
    customer = db.get(Customer, customer_id)
    if not customer:
        return None

    if name is not None:
        customer.Customer_Name = name
    if lastname is not None:
        customer.Customer_Lastname = lastname
    if email is not None:
        customer.Customer_Email = email
    if phone is not None:
        customer.Customer_Phone = phone
    if gender is not None:
        customer.Customer_Gender = gender
    if birth_date is not None:
        customer.Customer_BirthDate = birth_date
    if status is not None:
        customer.Customer_Status = status
    if country is not None:
        customer.Customer_Country = country
    if nationality is not None:
        customer.Customer_Nationality = nationality

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

