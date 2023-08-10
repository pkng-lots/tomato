import datetime
from decimal import Decimal

from pydantic import BaseModel


class PaymentBase(BaseModel):
    pass


class PaymentCreate(PaymentBase):
    txn_id: str
    txn_date: datetime.datetime
    prv_txn: int
    order_id: str
    account_id: str
    command: str
    sum: Decimal
    result: int
    comment: str
    pass


class PaymentCheck(PaymentBase):
    txn_id: str
    result: int
    comment: str
    pass

class PaymentPay(PaymentCheck):
    prv_txn_id: str
    sum: Decimal
    pass


class Payment(PaymentBase):
    id: int
    txn_id: str
    txn_date: datetime.datetime
    prv_txn: int
    order_id: str
    account_id: str
    command: str
    sum: Decimal
    result: int
    comment: str
    insert_datetime: datetime.datetime
    update_datetime: datetime.datetime
    delete_datetime: datetime.datetime
    is_deleted: bool

    owner_id: int

    class Config:
        orm_mode = True


class DummyBase(BaseModel):
    title: str


class DummyCreate(DummyBase):
    pass


class Dummy(DummyBase):
    id: int
    title: str
    class Config:
        orm_mode = True