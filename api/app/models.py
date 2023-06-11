from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Questions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    answer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)