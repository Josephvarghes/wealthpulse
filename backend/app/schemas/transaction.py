from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class RawTransaction(BaseModel):
    timestamp: Optional[str] = None
    date: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None


class NormalizedTransaction(BaseModel):
    id: int
    timestamp: datetime
    date: str  # YYYY-MM-DD format
    category: str
    description: str
    amount: float
    type: str  # 'Income' | 'Expense'


class FileValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    total_rows: int = 0

