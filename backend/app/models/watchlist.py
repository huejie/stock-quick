# models/watchlist.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.watchlist import MarketType


class WatchlistItem(BaseModel):
    """自选股数据模型"""
    id: Optional[str] = None
    user_id: str
    stock_code: str
    stock_name: str
    market: MarketType
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
