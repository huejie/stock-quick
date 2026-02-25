// store/watchlist.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { StockItem, WatchlistResponse } from '@/types/watchlist'
import { watchlistApi } from '@/api/watchlist'

export const useWatchlistStore = defineStore('watchlist', () => {
  const watchlistData = ref<WatchlistResponse | null>(null)
  const loading = ref(false)

  // 获取自选股列表
  const fetchWatchlist = async (userId: string = 'default_user') => {
    loading.value = true
    try {
      const res = await watchlistApi.getList(userId)
      watchlistData.value = res.data
    } catch (error) {
      console.error('获取自选股失败:', error)
      uni.showToast({
        title: '获取失败',
        icon: 'none'
      })
    } finally {
      loading.value = false
    }
  }

  // 添加自选股
  const addStock = async (userId: string, stockCode: string) => {
    try {
      await watchlistApi.add(userId, stockCode)
      uni.showToast({
        title: '添加成功',
        icon: 'success'
      })
      await fetchWatchlist(userId)
    } catch (error) {
      console.error('添加失败:', error)
      uni.showToast({
        title: '添加失败',
        icon: 'none'
      })
      throw error
    }
  }

  // 删除自选股
  const removeStock = async (userId: string, stockCode: string) => {
    try {
      await watchlistApi.remove(userId, stockCode)
      uni.showToast({
        title: '删除成功',
        icon: 'success'
      })
      await fetchWatchlist(userId)
    } catch (error) {
      console.error('删除失败:', error)
      uni.showToast({
        title: '删除失败',
        icon: 'none'
      })
      throw error
    }
  }

  // 搜索股票
  const searchStocks = async (keyword: string) => {
    try {
      return await watchlistApi.search(keyword)
    } catch (error) {
      console.error('搜索失败:', error)
      throw error
    }
  }

  return {
    watchlistData,
    loading,
    fetchWatchlist,
    addStock,
    removeStock,
    searchStocks,
  }
})
