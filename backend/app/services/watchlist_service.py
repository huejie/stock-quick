# services/watchlist_service.py
from typing import List, Optional
from app.schemas.watchlist import StockItem, MarketType
from app.models.watchlist import WatchlistItem
from datetime import datetime
import json
import time
import threading


class WatchlistService:
    """自选股服务 - MVP 版本使用内存存储"""

    def __init__(self):
        # MVP: 使用内存存储，生产环境替换为数据库
        self._storage: dict[str, List[WatchlistItem]] = {}
        # 股票数据缓存 - 初始化时先用 fallback 数据
        self._a_stocks_cache: List[StockItem] = self._get_default_a_stocks()
        self._hk_stocks_cache: List[StockItem] = self._get_default_hk_stocks()
        self._cache_time: float = 0
        self._cache_duration = 3600  # 缓存1小时
        self._is_loading = False

        # 启动时后台加载真实数据
        self._start_background_load()

    def _get_default_a_stocks(self) -> List[StockItem]:
        """默认 A 股数据"""
        return [
            StockItem(code="600519", name="贵州茅台", market=MarketType.A_SHARE),
            StockItem(code="000001", name="平安银行", market=MarketType.A_SHARE),
            StockItem(code="000002", name="万科A", market=MarketType.A_SHARE),
            StockItem(code="600036", name="招商银行", market=MarketType.A_SHARE),
            StockItem(code="601318", name="中国平安", market=MarketType.A_SHARE),
            StockItem(code="000858", name="五粮液", market=MarketType.A_SHARE),
            StockItem(code="002594", name="比亚迪", market=MarketType.A_SHARE),
            StockItem(code="300750", name="宁德时代", market=MarketType.A_SHARE),
            StockItem(code="601398", name="工商银行", market=MarketType.A_SHARE),
            StockItem(code="601288", name="农业银行", market=MarketType.A_SHARE),
            StockItem(code="600030", name="中信证券", market=MarketType.A_SHARE),
            StockItem(code="601166", name="兴业银行", market=MarketType.A_SHARE),
            StockItem(code="600000", name="浦发银行", market=MarketType.A_SHARE),
            StockItem(code="000333", name="美的集团", market=MarketType.A_SHARE),
            StockItem(code="600276", name="恒瑞医药", market=MarketType.A_SHARE),
            StockItem(code="000651", name="格力电器", market=MarketType.A_SHARE),
            StockItem(code="601888", name="中国中免", market=MarketType.A_SHARE),
            StockItem(code="600887", name="伊利股份", market=MarketType.A_SHARE),
            StockItem(code="002415", name="海康威视", market=MarketType.A_SHARE),
            StockItem(code="300059", name="东方财富", market=MarketType.A_SHARE),
        ]

    def _get_default_hk_stocks(self) -> List[StockItem]:
        """默认港股数据"""
        return [
            StockItem(code="00700", name="腾讯控股", market=MarketType.HK_STOCK),
            StockItem(code="09988", name="阿里巴巴", market=MarketType.HK_STOCK),
            StockItem(code="03690", name="美团", market=MarketType.HK_STOCK),
            StockItem(code="09999", name="网易", market=MarketType.HK_STOCK),
            StockItem(code="01810", name="小米集团", market=MarketType.HK_STOCK),
            StockItem(code="09618", name="京东集团", market=MarketType.HK_STOCK),
            StockItem(code="02318", name="中国平安", market=MarketType.HK_STOCK),
            StockItem(code="00005", name="汇丰控股", market=MarketType.HK_STOCK),
            StockItem(code="00941", name="中国移动", market=MarketType.HK_STOCK),
            StockItem(code="03988", name="中国银行", market=MarketType.HK_STOCK),
        ]

    def _start_background_load(self):
        """后台加载真实数据"""
        thread = threading.Thread(target=self._load_real_data)
        thread.daemon = True
        thread.start()

    def _load_real_data(self):
        """后台加载真实股票数据"""
        if self._is_loading:
            return

        self._is_loading = True
        print("后台加载股票数据...")

        try:
            import akshare as ak

            # 获取 A 股数据
            try:
                print("正在获取 A 股数据...")
                df_a = ak.stock_zh_a_spot_em()
                if df_a is not None and not df_a.empty:
                    df_a_limited = df_a.head(2000)
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

            # 获取港股数据
            try:
                print("正在获取港股数据...")
                df_hk = ak.stock_hk_spot_em()
                if df_hk is not None and not df_hk.empty:
                    df_hk_limited = df_hk.head(1000)
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

            self._cache_time = time.time()

        except Exception as e:
            print(f"加载股票数据失败: {e}")

        finally:
            self._is_loading = False

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
        """搜索股票 - 直接从缓存搜索，不等待"""
        if not keyword or not keyword.strip():
            return []

        keyword_lower = keyword.lower().strip()
        results = []

        # 直接从缓存搜索（缓存已有默认数据）
        for stock in self._a_stocks_cache:
            if keyword_lower in stock.code.lower() or keyword_lower in stock.name.lower():
                results.append(stock)
                if len(results) >= 20:
                    break

        if len(results) < 20:
            for stock in self._hk_stocks_cache:
                if keyword_lower in stock.code.lower() or keyword_lower in stock.name.lower():
                    results.append(stock)
                    if len(results) >= 20:
                        break

        return results


# 全局单例
watchlist_service = WatchlistService()
