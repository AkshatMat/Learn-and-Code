from pydantic import BaseModel
from typing import Optional

class HeadlinesRangeRequest(BaseModel):
    start_date: str
    end_date: str
    category: Optional[str] = None
