import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, DECIMAL, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column("id", BigInteger, primary_key=True, index=True)
    txn_id = Column("txn_id", String, unique=True, index=True)
    txn_date = Column("txn_dttm", DateTime, index=True)
    prv_txn = Column("prv_txn_id", BigInteger, index=True)
    order_id = Column("order_id", String, unique=True, index=True)
    account_id = Column("account_id", String, index=True)
    command = Column("command", String, index=True)
    sum = Column("sum", DECIMAL, index=True)
    insert_datetime = Column("ins_dttm", DateTime, index=True)
    update_datetime = Column("upd_dttm", DateTime, index=True)
    delete_datetime = Column("del_dttm", DateTime, index=True)
    is_deleted = Column("is_del", Boolean, default=False)
