import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, DECIMAL, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Payment(Base):
    """Simple class for KSP payment data."""
    __tablename__ = "payments"
    id = Column("id", BigInteger, primary_key=True, index=True)
    """Unique identifier of row in table."""

    txn_id = Column("txn_id", String, unique=True, index=True)
    """ID of request from System to provider. """

    txn_date = Column("txn_dttm", DateTime, index=True)
    """Date of request from System to provider, has YYYYMMDDHHMMSS format."""

    prv_txn = Column("prv_txn_id", BigInteger, index=True)
    """Unique provider payment identifier."""

    order_id = Column("order_id", String, unique=True, index=True)
    """"""

    account_id = Column("account_id", String, index=True)
    """Identifier of customer in providet database."""

    command = Column("command", String, index=True)
    """
    This field comes from System to Provider, and may contain 2 possible value - \"check\" and \"pay\".
    Sending payment info (System->Provider) works in 2 stages - \"check\" (provider approves existence
    of sent account(account_id) in own database) and then, if OK, provider accepts \"pay\" command from
    System). CHECK and PAY requests from System has DIFFERENT txn_id.
    """

    sum = Column("sum", DECIMAL, index=True)
    """Sum of payment, decimal number."""

    insert_datetime = Column("ins_dttm", DateTime, index=True)
    update_datetime = Column("upd_dttm", DateTime, index=True)
    delete_datetime = Column("del_dttm", DateTime, index=True)
    is_deleted = Column("is_del", Boolean, default=False)


class Dummy(Base):
    __tablename__ = "dummy"

    id = Column("id", BigInteger, primary_key=True, index=True)
    title = Column("txn_id", String, unique=False, index=True)
