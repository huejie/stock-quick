<!-- pages/market/market.vue -->
<template>
  <view class="market-page">
    <view class="section">
      <view class="section-header">
        <text class="section-title">🔥 市场热点</text>
        <text class="update-time">更新于 {{ updateTime }}</text>
      </view>

      <view class="section-body">
        <view class="placeholder-card">
          <text class="placeholder-text">板块轮动</text>
          <text class="placeholder-hint">功能开发中...</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onPullDownRefresh } from '@dcloudio/uni-app'

const updateTime = ref('')

onMounted(() => {
  updateTime.value = new Date().toLocaleTimeString()
})

onPullDownRefresh(() => {
  updateTime.value = new Date().toLocaleTimeString()
  setTimeout(() => {
    uni.stopPullDownRefresh()
  }, 500)
})
</script>

<style lang="scss" scoped>
.market-page {
  min-height: 100vh;
  padding: 8px;
}

.section {
  margin-bottom: 16px;
}

.section-header {
  background: #fff;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px 8px 0 0;
  border-bottom: 1px solid #f5f5f5;

  .section-title {
    font-size: 16px;
    font-weight: bold;
  }

  .update-time {
    font-size: 12px;
    color: #757575;
  }
}

.section-body {
  background: #fff;
  padding: 16px;
  border-radius: 0 0 8px 8px;
}

.placeholder-card {
  text-align: center;
  padding: 40px 20px;

  .placeholder-text {
    display: block;
    font-size: 16px;
    color: #212121;
    margin-bottom: 8px;
  }

  .placeholder-hint {
    display: block;
    font-size: 14px;
    color: #757575;
  }
}
</style>
