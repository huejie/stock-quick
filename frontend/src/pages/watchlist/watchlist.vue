<!-- pages/watchlist/watchlist.vue -->
<template>
  <view class="watchlist-page">
    <!-- 市场标签 -->
    <view class="market-tabs">
      <view class="tab-item" :class="{ active: currentTab === 'A' }" @tap="switchTab('A')">
        A股 ({{ aShareCount }})
      </view>
      <view class="tab-item" :class="{ active: currentTab === 'HK' }" @tap="switchTab('HK')">
        港股 ({{ hkStockCount }})
      </view>
    </view>

    <!-- 股票列表 -->
    <view class="stock-list" v-if="!loading && filterStocks.length > 0">
      <view
        class="stock-card"
        v-for="stock in filterStocks"
        :key="stock.code"
      >
        <view class="stock-header">
          <text class="stock-name">{{ stock.name }}</text>
          <text class="stock-code">{{ stock.code }}</text>
        </view>
        <view class="stock-price">
          <text class="price" v-if="stock.current_price">
            ¥{{ stock.current_price?.toFixed(2) }}
          </text>
          <text class="change" :class="getChangeClass(stock.change)" v-if="stock.change !== undefined">
            {{ stock.change > 0 ? '+' : '' }}{{ stock.change }}%
          </text>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-if="!loading && filterStocks.length === 0">
      <text class="empty-text">暂无自选股</text>
      <text class="empty-hint">点击右上角 + 添加股票</text>
    </view>

    <!-- 加载状态 -->
    <view class="loading-state" v-if="loading">
      <text>加载中...</text>
    </view>

    <!-- 添加按钮 -->
    <view class="add-btn" @tap="showAddModal = true">
      <text class="add-icon">+</text>
    </view>

    <!-- 添加弹窗 -->
    <view class="modal-mask" v-if="showAddModal" @tap="showAddModal = false">
      <view class="modal-content" @tap.stop>
        <view class="modal-header">
          <text>添加自选股</text>
          <text class="close-btn" @tap="showAddModal = false">×</text>
        </view>
        <view class="modal-body">
          <input
            class="search-input"
            v-model="searchKeyword"
            placeholder="输入股票代码或名称"
            @input="onSearchInput"
          />
          <view class="search-results" v-if="searchResults.length > 0">
            <view
              class="result-item"
              v-for="stock in searchResults"
              :key="stock.code"
              @tap="selectStock(stock)"
            >
              <text class="result-name">{{ stock.name }}</text>
              <text class="result-code">{{ stock.code }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { onPullDownRefresh } from '@dcloudio/uni-app'
import { useWatchlistStore } from '@/store/watchlist'
import type { StockItem } from '@/types/watchlist'
import { MarketType } from '@/types/watchlist'

const watchlistStore = useWatchlistStore()
const currentTab = ref<'A' | 'HK'>('A')
const showAddModal = ref(false)
const searchKeyword = ref('')
const searchResults = ref<StockItem[]>([])

const refreshData = async () => {
  await watchlistStore.fetchWatchlist()
}

onMounted(() => {
  refreshData()
})

// 下拉刷新
onPullDownRefresh(() => {
  refreshData().then(() => {
    uni.stopPullDownRefresh()
  })
})

const aShareCount = computed(() => watchlistStore.watchlistData?.A_shares_count || 0)
const hkStockCount = computed(() => watchlistStore.watchlistData?.HK_stocks_count || 0)

const filterStocks = computed(() => {
  if (!watchlistStore.watchlistData) return []
  const market = currentTab.value === 'A' ? MarketType.A_SHARE : MarketType.HK_STOCK
  return watchlistStore.watchlistData.stocks.filter(s => s.market === market)
})

const switchTab = (tab: 'A' | 'HK') => {
  currentTab.value = tab
}

const getChangeClass = (change?: number) => {
  if (!change) return ''
  return change > 0 ? 'text-success' : 'text-danger'
}

const onSearchInput = async () => {
  if (!searchKeyword.value) {
    searchResults.value = []
    return
  }
  try {
    // 调用搜索 API
    const res = await watchlistStore.searchStocks(searchKeyword.value)
    searchResults.value = res.data || []
  } catch (error) {
    console.error('搜索失败:', error)
    searchResults.value = []
  }
}

const selectStock = async (stock: StockItem) => {
  try {
    await watchlistStore.addStock('default_user', stock.code)
    showAddModal.value = false
    searchKeyword.value = ''
    searchResults.value = []
  } catch (error) {
    // 错误已在 store 中处理
  }
}
</script>

<style lang="scss" scoped>
.watchlist-page {
  min-height: 100vh;
  padding-bottom: 80px;
}

.market-tabs {
  display: flex;
  background: #fff;
  padding: 16px;
  margin-bottom: 8px;

  .tab-item {
    flex: 1;
    text-align: center;
    padding: 8px;
    border-radius: 4px;
    font-size: 14px;

    &.active {
      background: #1976d2;
      color: #fff;
    }
  }
}

.stock-list {
  padding: 8px;
}

.stock-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 8px;

  .stock-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;

    .stock-name {
      font-size: 16px;
      font-weight: bold;
    }

    .stock-code {
      font-size: 12px;
      color: #757575;
    }
  }

  .stock-price {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .price {
      font-size: 20px;
      font-weight: bold;
    }

    .change {
      font-size: 14px;
      padding: 4px 8px;
      border-radius: 4px;
    }
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;

  .empty-text {
    font-size: 16px;
    color: #757575;
    margin-bottom: 8px;
  }

  .empty-hint {
    font-size: 14px;
    color: #bdbdbd;
  }
}

.loading-state {
  display: flex;
  justify-content: center;
  padding: 40px;
  color: #757575;
}

.add-btn {
  position: fixed;
  right: 20px;
  bottom: 80px;
  width: 56px;
  height: 56px;
  background: #1976d2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);

  .add-icon {
    font-size: 32px;
    color: #fff;
    line-height: 1;
  }
}

.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 80%;
  max-width: 400px;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;

  .close-btn {
    font-size: 24px;
    color: #757575;
  }
}

.modal-body {
  padding: 16px;
}

.search-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-results {
  margin-top: 16px;
  max-height: 200px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }

  .result-name {
    font-size: 14px;
  }

  .result-code {
    font-size: 12px;
    color: #757575;
  }
}
</style>
