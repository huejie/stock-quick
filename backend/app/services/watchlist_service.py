# services/watchlist_service.py
from typing import List, Optional
from app.schemas.watchlist import StockItem, MarketType
from app.models.watchlist import WatchlistItem
from datetime import datetime
import json
import akshare as ak


class WatchlistService:
    """自选股服务 - MVP 版本使用内存存储"""

    def __init__(self):
        # MVP: 使用内存存储，生产环境替换为数据库
        self._storage: dict[str, List[WatchlistItem]] = {}
        # 股票数据缓存
        self._a_stocks_cache: List[StockItem] = []
        self._hk_stocks_cache: List[StockItem] = []
        self._cache_time: float = 0
        self._cache_duration = 3600  # 缓存1小时，减少刷新频率
        self._is_loading = False  # 防止并发加载

    def get_user_watchlist(self, user_id: str) -> List[WatchlistItem]:
        """获取用户自选股列表"""
        return self._storage.get(user_id, [])

    def add_stock(
        self,
        user_id: str,
        stock_code: str,
        stock_name: str,
        market: MarketType
    ) -> bool:
        """添加自选股"""
        if user_id not in self._storage:
            self._storage[user_id] = []

        # 检查是否已存在
        for item in self._storage[user_id]:
            if item.stock_code == stock_code:
                return False  # 已存在

        # 添加新股票
        new_item = WatchlistItem(
            user_id=user_id,
            stock_code=stock_code,
            stock_name=stock_name,
            market=market,
            created_at=datetime.now()
        )
        self._storage[user_id].append(new_item)
        return True

    def remove_stock(self, user_id: str, stock_code: str) -> bool:
        """删除自选股"""
        if user_id not in self._storage:
            return False

        original_length = len(self._storage[user_id])
        self._storage[user_id] = [
            item for item in self._storage[user_id]
            if item.stock_code != stock_code
        ]

        return len(self._storage[user_id]) < original_length

    def search_stock(self, keyword: str) -> List[StockItem]:
        """搜索股票 - 使用 akshare 获取真实数据（带缓存）"""
        if not keyword or not keyword.strip():
            return []

        keyword_lower = keyword.lower().strip()
        results = []

        import time
        current_time = time.time()

        try:
            # 如果缓存为空，同步加载（首次加载）
            if not self._a_stocks_cache and not self._is_loading:
                print("首次加载股票数据...")
                self._update_stock_cache()
            # 如果缓存过期但有旧数据，异步刷新（不阻塞搜索）
            elif current_time - self._cache_time > self._cache_duration and not self._is_loading:
                print("缓存过期，后台更新中...")
                import threading
                thread = threading.Thread(target=self._update_stock_cache)
                thread.daemon = True
                thread.start()

            # 搜索 A股（从缓存）
            for stock in self._a_stocks_cache:
                if keyword_lower in stock.code.lower() or keyword_lower in stock.name.lower():
                    results.append(stock)
                    if len(results) >= 20:  # 限制结果数量
                        break

            # 如果结果不足20条，继续搜索港股
            if len(results) < 20:
                for stock in self._hk_stocks_cache:
                    if keyword_lower in stock.code.lower() or keyword_lower in stock.name.lower():
                        results.append(stock)
                        if len(results) >= 20:
                            break

        except Exception as e:
            print(f"搜索失败: {e}")
            # 如果失败，返回一些热门股票作为fallback
            return self._get_fallback_stocks(keyword)

        # 如果缓存为空（akshare失败），使用fallback
        if not self._a_stocks_cache and not self._hk_stocks_cache:
            print("缓存为空，使用fallback数据")
            return self._get_fallback_stocks(keyword)

        return results

    def _update_stock_cache(self):
        """更新股票数据缓存（线程安全）"""
        # 防止并发加载
        if self._is_loading:
            return

        import time
        start_time = time.time()
        self._is_loading = True

        try:
            # 获取A股数据（批量处理，提高效率）
            print("正在获取A股数据...")
            df_a = ak.stock_zh_a_spot_em()
            if df_a is not None and not df_a.empty:
                # 批量处理，提高效率
                df_a_limited = df_a.head(2000)  # 增加到2000只
                self._a_stocks_cache = [
                    StockItem(
                        code=str(row.get('代码', '')),
                        name=str(row.get('名称', '')),
                        market=MarketType.A_SHARE
                    )
                    for _, row in df_a_limited.iterrows()
                ]
            print(f"A股数据获取完成，共 {len(self._a_stocks_cache)} 只")
        except Exception as e:
            print(f"获取A股数据失败: {e}")
            if not self._a_stocks_cache:  # 只在没有缓存时才清空
                self._a_stocks_cache = []

        try:
            # 获取港股数据
            print("正在获取港股数据...")
            df_hk = ak.stock_hk_spot_em()
            if df_hk is not None and not df_hk.empty:
                # 批量处理
                df_hk_limited = df_hk.head(1000)  # 增加到1000只
                self._hk_stocks_cache = [
                    StockItem(
                        code=str(row.get('代码', '')),
                        name=str(row.get('名称', '')),
                        market=MarketType.HK_STOCK
                    )
                    for _, row in df_hk_limited.iterrows()
                ]
            print(f"港股数据获取完成，共 {len(self._hk_stocks_cache)} 只")
        except Exception as e:
            print(f"获取港股数据失败: {e}")
            if not self._hk_stocks_cache:  # 只在没有缓存时才清空
                self._hk_stocks_cache = []

        import time
        self._cache_time = time.time()
        self._is_loading = False
        elapsed = time.time() - start_time
        print(f"缓存更新完成，耗时 {elapsed:.1f} 秒")

    def _get_fallback_stocks(self, keyword: str) -> List[StockItem]:
        """akshare失败时的fallback数据"""
        fallback_stocks = [
            StockItem(code="600519", name="贵州茅台", market=MarketType.A_SHARE),
            StockItem(code="000001", name="平安银行", market=MarketType.A_SHARE),
            StockItem(code="000002", name="万科A", market=MarketType.A_SHARE),
            StockItem(code="600036", name="招商银行", market=MarketType.A_SHARE),
            StockItem(code="601318", name="中国平安", market=MarketType.A_SHARE),
            StockItem(code="000858", name="五粮液", market=MarketType.A_SHARE),
            StockItem(code="002594", name="比亚迪", market=MarketType.A_SHARE),
            StockItem(code="300750", name="宁德时代", market=MarketType.A_SHARE),
            StockItem(code="00700", name="腾讯控股", market=MarketType.HK_STOCK),
            StockItem(code="09988", name="阿里巴巴", market=MarketType.HK_STOCK),
        ]

        keyword_lower = keyword.lower()
        return [
            stock for stock in fallback_stocks
            if keyword_lower in stock.code.lower() or keyword_lower in stock.name.lower()
        ]


# 全局单例
watchlist_service = WatchlistService()
