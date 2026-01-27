# schemas/__init__.py
from .common import ApiResponse, PaginationParams, PaginatedResponse
from .watchlist import (
    StockItem,
    MarketType,
    AddWatchlistRequest,
    RemoveWatchlistRequest,
    WatchlistResponse,
)

__all__ = [
    "ApiResponse",
    "PaginationParams",
    "PaginatedResponse",
    "StockItem",
    "MarketType",
    "AddWatchlistRequest",
    "RemoveWatchlistRequest",
    "WatchlistResponse",
]
