// types/watchlist.ts
export enum MarketType {
  A_SHARE = 'A',
  HK_STOCK = 'HK'
}

export interface StockItem {
  code: string
  name: string
  market: MarketType
  current_price?: number
  change?: number
}

export interface WatchlistResponse {
  user_id: string
  stocks: StockItem[]
  A_shares_count: number
  HK_stocks_count: number
}
