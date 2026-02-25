# schemas/watchlist.py
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class MarketType(str, Enum):
    """市场类型"""
    A_SHARE = "A"
    HK_STOCK = "HK"


class StockItem(BaseModel):
    """股票项"""
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    market: MarketType = Field(..., description="市场类型")
    current_price: Optional[float] = Field(None, description="当前价格")
    change: Optional[float] = Field(None, description="涨跌幅(%)")


class AddWatchlistRequest(BaseModel):
    """添加自选股请求"""
    user_id: str = Field(..., description="用户ID")
    stock_code: str = Field(..., min_length=6, max_length=10, description="股票代码")


class RemoveWatchlistRequest(BaseModel):
    """删除自选股请求"""
    user_id: str = Field(..., description="用户ID")
    stock_code: str = Field(..., description="股票代码")


class WatchlistResponse(BaseModel):
    """自选股列表响应"""
    user_id: str
    stocks: list[StockItem]
    A_shares_count: int = Field(0, description="A股数量")
    HK_stocks_count: int = Field(0, description="港股数量")
