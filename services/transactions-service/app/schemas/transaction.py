from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# -----------------------------
# Transaction Schemas
# -----------------------------
class TransactionBase(BaseModel):
    description: str
    amount: float
    category: Optional[str] = None
    date: Optional[datetime] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction"""
    pass


class TransactionResponse(TransactionBase):
    """Schema for returning transaction details"""
    id: int
    user_id: int

    class Config:
        from_attributes = True  # ✅ Pydantic v2


class TransactionPublic(TransactionBase):
    """Public-facing transaction schema (without user_id)"""
    id: int

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    """Schema for returning a list of transactions"""
    transactions: List[TransactionResponse]


# -----------------------------
# Category Schemas
# -----------------------------
class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    """Schema for creating a new spending category"""
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryPublic(CategoryBase):
    """Public-facing category schema"""
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# Pagination Schema
# -----------------------------
class PaginatedTransactions(BaseModel):
    """Schema for paginated transaction list responses"""
    total: int
    page: int
    size: int
    transactions: List[TransactionResponse]


# -----------------------------
# CSV Parsing Schema ✅
# -----------------------------
class CSVParsedRow(BaseModel):
    """Schema representing a single parsed row from a CSV upload"""
    description: str
    amount: float
    date: Optional[datetime] = None
    category: Optional[str] = None
