// api/watchlist.ts
import { http } from './request'
import type { StockItem, WatchlistResponse } from '@/types/watchlist'

export const watchlistApi = {
  // 获取自选股列表
  getList: (userId: string = 'default_user') =>
    http.get<WatchlistResponse>('/watchlist', { user_id: userId }),

  // 添加自选股
  add: (userId: string, stockCode: string) =>
    http.post('/watchlist', { user_id: userId, stock_code: stockCode }),

  // 删除自选股
  remove: (userId: string, stockCode: string) =>
    http.delete('/watchlist', { user_id: userId, stock_code: stockCode }),

  // 搜索股票
  search: (keyword: string) =>
    http.get<StockItem[]>('/watchlist/search', { keyword }),
}
