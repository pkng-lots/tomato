from pydantic import BaseModel


class PaymentBase(BaseModel):
    title: str
    decsription: str | None = None


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
