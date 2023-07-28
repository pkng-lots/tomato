from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, String
from sqlalchemy.orm import relationship

from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True, index=True)
