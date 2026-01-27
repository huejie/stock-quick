# api/watchlist.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import (
    ApiResponse,
    WatchlistResponse,
    AddWatchlistRequest,
    RemoveWatchlistRequest,
    StockItem,
    MarketType,
)
from app.services.watchlist_service import watchlist_service

router = APIRouter(prefix="/watchlist", tags=["自选股"])


@router.get("", response_model=ApiResponse[WatchlistResponse])
async def get_watchlist(user_id: str = "default_user"):
    """获取自选股列表"""
    items = watchlist_service.get_user_watchlist(user_id)

    # 转换为响应格式
    stocks = [
        StockItem(
            code=item.stock_code,
            name=item.stock_name,
            market=item.market,
        )
        for item in items
    ]

    # 统计数量
    a_count = sum(1 for s in stocks if s.market == MarketType.A_SHARE)
    hk_count = sum(1 for s in stocks if s.market == MarketType.HK_STOCK)

    return ApiResponse(data=WatchlistResponse(
        user_id=user_id,
        stocks=stocks,
        A_shares_count=a_count,
        HK_stocks_count=hk_count,
    ))


@router.post("", response_model=ApiResponse[dict])
async def add_to_watchlist(request: AddWatchlistRequest):
    """添加自选股"""
    # 简单判断市场类型
    if request.stock_code.endswith(".HK") or request.stock_code.startswith("00"):
        market = MarketType.HK_STOCK
    else:
        market = MarketType.A_SHARE

    # 获取股票名称 - MVP 简化处理
    stock_name = f"股票{request.stock_code}"

    success = watchlist_service.add_stock(
        user_id=request.user_id,
        stock_code=request.stock_code,
        stock_name=stock_name,
        market=market
    )

    if not success:
        raise HTTPException(status_code=400, detail="股票已在自选中")

    return ApiResponse(data={"message": "添加成功"})


@router.delete("", response_model=ApiResponse[dict])
async def remove_from_watchlist(request: RemoveWatchlistRequest):
    """删除自选股"""
    success = watchlist_service.remove_stock(
        user_id=request.user_id,
        stock_code=request.stock_code
    )

    if not success:
        raise HTTPException(status_code=404, detail="股票不在自选中")

    return ApiResponse(data={"message": "删除成功"})


@router.get("/search", response_model=ApiResponse[list[StockItem]])
async def search_stocks(keyword: str = ""):
    """搜索股票"""
    stocks = watchlist_service.search_stock(keyword)
    return ApiResponse(data=stocks)
