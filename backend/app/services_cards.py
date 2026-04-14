"""Card operations."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Card, CardStatus, CardType


def create_card(
    db: Session,
    *,
    account_id: int,
    card_number: str,
    card_type: CardType,
    expiration_date: datetime,
    status: CardStatus = CardStatus.Active,
    is_active: bool = True,
    max_cards_per_account: int = 2,
) -> Card:
    """Create a new card tied to an account."""
    existing_count = db.query(Card).filter(Card.Account_ID == account_id).count()
    if existing_count >= max_cards_per_account:
        raise ValueError(f"Maximum {max_cards_per_account} cards per account")

    card = Card(
        Account_ID=account_id,
        Card_Number=card_number,
        Card_Type=card_type,
        Card_Expiration_Date=expiration_date,
        Card_Status=status,
        Is_Active=is_active,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def get_card_by_id(db: Session, card_id: int) -> Optional[Card]:
    """Return card information by ID."""
    return db.get(Card, card_id)


def update_card_status(
    db: Session,
    card_id: int,
    *,
    status: Optional[CardStatus] = None,
    is_active: Optional[bool] = None,
) -> Optional[Card]:
    """Update card status and/or active flag."""
    card = db.get(Card, card_id)
    if not card:
        return None

    if status is not None:
        card.Card_Status = status
    if is_active is not None:
        card.Is_Active = is_active

    db.add(card)
    db.commit()
    db.refresh(card)
    return card

