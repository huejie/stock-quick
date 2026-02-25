<!-- App.vue -->
<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('App Launch')
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style lang="scss">
/* 全局样式 */
page {
  background-color: #f5f5f5;
  font-size: 14px;
  line-height: 1.5;
  color: #212121;
}

/* 通用类 */
.text-primary {
  color: #1976d2;
}

.text-success {
  color: #e53935; /* A股红涨 */
}

.text-danger {
  color: #43a047; /* A股绿跌 */
}

.text-warning {
  color: #fb8c00;
}

.text-secondary {
  color: #757575;
}

/* 布局 */
.flex {
  display: flex;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 间距 */
-mt-1 { margin-top: 8px; }
-mt-2 { margin-top: 16px; }
-mb-1 { margin-bottom: 8px; }
-mb-2 { margin-bottom: 16px; }
.p-1 { padding: 8px; }
.p-2 { padding: 16px; }

/* 卡片 */
.card {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}
</style>
