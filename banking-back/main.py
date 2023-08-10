import decimal
from decimal import Decimal
from typing import Union, Optional

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import decimal
from decimal import Decimal

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name} !!!"}


@app.post("/dummy/create", response_model=schemas.Dummy)
def create_dummy(db: Session = Depends(get_db)):
    return crud.create_payment(db=db)


@app.get("/payment/create", response_model=Union[schemas.PaymentCheck, schemas.PaymentPay])
def create_payment(command: str, txn_id: int, account: str, sum: str, txn_date: Optional[str] = None,
                    db: Session = Depends(get_db)):
    if command == "check":
        return schemas.PaymentCheck(txn_id=str(txn_id), result=0, comment="")
    elif command == "pay":
        return schemas.PaymentPay(txn_id=str(txn_id), prv_txn_id="100", result=0, sum=500, comment="")
    return {}
