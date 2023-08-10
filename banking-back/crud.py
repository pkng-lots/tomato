import decimal
from decimal import Decimal

from sqlalchemy.orm import Session

import models
import schemas


def get_payments(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def create_dummy(db: Session):
    db_dummy = models.Dummy(title="123")
    db.add(db_dummy)
    db.commit()
    db.refresh(db_dummy)
    return db_dummy


def create_payment(db: Session, command:str, txn_id: int, account:str, sun: decimal):
    db_payment = models.Payment()
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
