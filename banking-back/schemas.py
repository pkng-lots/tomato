import datetime
import decimal

from pydantic import BaseModel


class PaymentBase(BaseModel):
    title: str
    decsription: str | None = None


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    txn_id: str
    txn_date: datetime.datetime
    prv_txn: int
    order_id: str
    account_id: str
    # "check" or "pay"
    command: str
    sum: decimal
    result: int
    comment: str
    insert_datetime: datetime.datetime
    update_datetime: datetime.datetime
    delete_datetime: datetime.datetime
    is_deleted: bool

    owner_id: int

    class Config:
        orm_mode = True
