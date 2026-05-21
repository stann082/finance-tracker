from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TransactionType(str, Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"


class TransactionResponse(BaseModel):
    id: str  # MongoDB ObjectId as string
    amount: float
    balance: float
    category: Optional[str] = None
    date: datetime
    description: Optional[str] = None
    is_deposit: bool
    is_recurring: Optional[bool] = False
    transaction_id: Optional[str] = None
    type: TransactionType

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    amount: float
    balance: float
    date: datetime
    description: Optional[str] = None
    category: Optional[str] = None
    is_recurring: bool = False
    transaction_id: Optional[str] = None


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    balance: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_recurring: Optional[bool] = None
    transaction_id: Optional[str] = None
