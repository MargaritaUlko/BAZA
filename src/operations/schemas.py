from datetime import datetime
from pydantic import BaseModel

from pydantic import BaseModel
from datetime import datetime

class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    type: str
    date: datetime

    class Config:
        from_attributes = True