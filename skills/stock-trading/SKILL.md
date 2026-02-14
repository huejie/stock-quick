---
name: stock-trading
description: 股票交易应用开发技能 - 包含股票数据获取、K线图表、交易逻辑、风险管理等
metadata:
  category: finance
  version: 1.0.0
  requires: []
---

# 股票交易应用开发技能

专业的股票交易应用开发技能包，适用于A股、港股等股票市场应用开发。

## 核心能力

### 1. 股票数据获取
- 实时行情数据
- 历史K线数据
- 财务数据
- 新闻资讯
- 资金流向数据

### 2. 技术分析
- K线图表绘制
- 技术指标计算
- 趋势分析
- 支撑阻力位
- 成交量分析

### 3. 交易逻辑
- 自选股管理
- 价格提醒
- 模拟交易
- 持仓管理
- 盈亏计算

### 4. 风险管理
- 风险提示
- 仓位管理
- 止损止盈
- 风险评估
- 合规检查

## 数据源

### A股数据源
1. **akshare** - Python库，免费A股数据
   - 实时行情
   - 历史K线
   - 财务数据
   - 资金流向

2. **tushare** - Python库，需要token
   - 更全面的A股数据
   - 更稳定的接口

3. **新浪财经API** - 免费接口
   - 实时行情
   - 分时数据

### 港股数据源
1. **yfinance** - Python库
   - 港股实时行情
   - 历史数据
   - 财务数据

2. **腾讯财经API** - 免费接口
   - 港股行情

### 数据缓存策略
```python
# 数据缓存示例
CACHE_CONFIG = {
    '实时行情': {'ttl': 60},      # 60秒缓存
    'K线数据': {'ttl': 300},     # 5分钟缓存
    '财务数据': {'ttl': 3600},   # 1小时缓存
    '新闻资讯': {'ttl': 1800},   # 30分钟缓存
}
```

## 技术实现

### 后端API设计
```python
# FastAPI股票API示例
from fastapi import APIRouter, Query
from typing import Optional
from datetime import date

router = APIRouter()

@router.get("/stocks/{symbol}/quote")
async def get_stock_quote(
    symbol: str,
    market: str = Query("A", description="市场: A- A股, H-港股")
):
    """获取股票实时行情"""
    pass

@router.get("/stocks/{symbol}/kline")
async def get_stock_kline(
    symbol: str,
    period: str = Query("1d", description="周期: 1d-日线, 1w-周线, 1m-月线"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """获取K线数据"""
    pass

@router.get("/market/hot")
async def get_market_hot():
    """获取市场热点"""
    pass

@router.get("/market/capital")
async def get_capital_flow():
    """获取资金流向"""
    pass
```

### 前端数据展示
```typescript
// TypeScript股票数据接口
interface StockQuote {
  symbol: string;      // 股票代码
  name: string;        // 股票名称
  current: number;     // 当前价
  change: number;      // 涨跌额
  changePercent: number; // 涨跌幅
  volume: number;      // 成交量
  amount: number;      // 成交额
  high: number;        // 最高价
  low: number;         // 最低价
  open: number;        // 开盘价
  prevClose: number;   // 昨收价
  timestamp: string;   // 更新时间
}

interface KLineData {
  time: string;        // 时间
  open: number;        // 开盘价
  high: number;        // 最高价
  low: number;         // 最低价
  close: number;       // 收盘价
  volume: number;      // 成交量
}
```

## 图表实现

### K线图表配置
```javascript
// uCharts K线图配置
const klineChartConfig = {
  type: 'candle',
  categories: [],      // 时间轴
  series: [{
    data: [],         // K线数据
    color: '#4CAF50', // 上涨颜色
    colorNegative: '#F44336' // 下跌颜色
  }],
  xAxis: {
    disableGrid: true,
    itemCount: 50,    // 显示数量
    scrollShow: true  // 支持滚动
  },
  yAxis: {
    gridType: 'dash', // 虚线网格
    data: [{ min: 0 }]
  },
  extra: {
    candle: {
      color: {
        upLine: '#4CAF50',
        upFill: '#E8F5E9',
        downLine: '#F44336',
        downFill: '#FFEBEE'
      }
    }
  }
};
```

### 分时图配置
```javascript
// 分时图配置
const timeShareConfig = {
  type: 'line',
  categories: [],      // 时间点
  series: [{
    name: '价格',
    data: [],         // 价格数据
    color: '#2196F3'
  }],
  xAxis: {
    disableGrid: true,
    boundaryGap: false // 不留白
  },
  yAxis: {
    gridType: 'solid',
    splitNumber: 5     // 分割线数量
  }
};
```

## 业务逻辑

### 自选股管理
```python
# 自选股业务逻辑
class WatchlistService:
    def __init__(self):
        self.watchlist = []
    
    def add_stock(self, symbol: str, market: str) -> bool:
        """添加自选股"""
        # 检查股票是否存在
        # 检查是否已添加
        # 添加到自选股列表
        pass
    
    def remove_stock(self, symbol: str) -> bool:
        """删除自选股"""
        pass
    
    def get_watchlist(self) -> list:
        """获取自选股列表"""
        pass
    
    def update_prices(self):
        """更新自选股价格"""
        # 批量获取股票价格
        # 更新缓存
        pass
```

### 价格提醒
```python
# 价格提醒逻辑
class PriceAlertService:
    def __init__(self):
        self.alerts = {}
    
    def set_alert(self, symbol: str, target_price: float, condition: str):
        """设置价格提醒"""
        # condition: 'above' 高于, 'below' 低于
        pass
    
    def check_alerts(self, current_price: float):
        """检查价格提醒"""
        pass
    
    def send_notification(self, alert):
        """发送通知"""
        pass
```

## 性能优化

### 数据更新策略
1. **WebSocket实时推送** - 重要数据实时更新
2. **轮询更新** - 次要数据定时更新
3. **增量更新** - 只更新变化的数据
4. **批量请求** - 减少请求次数

### 缓存策略
```python
# Redis缓存示例
import redis
import json
from datetime import datetime, timedelta

class StockCache:
    def __init__(self):
        self.redis = redis.Redis()
    
    def get_quote(self, symbol: str):
        """获取缓存行情"""
        key = f"quote:{symbol}"
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None
    
    def set_quote(self, symbol: str, data: dict, ttl: int = 60):
        """设置缓存行情"""
        key = f"quote:{symbol}"
        self.redis.setex(key, ttl, json.dumps(data))
```

## 合规和安全

### 合规要求
1. **风险提示** - 必须显示风险提示
2. **数据准确性** - 确保数据准确
3. **用户隐私** - 保护用户数据
4. **交易合规** - 符合监管要求

### 安全措施
1. **API限流** - 防止滥用
2. **数据验证** - 验证输入数据
3. **错误处理** - 友好的错误提示
4. **日志记录** - 记录重要操作

## 部署架构

### 微服务架构
```
┌─────────────────┐
│   前端应用      │
│  (H5/小程序)    │
└────────┬────────┘
         │ HTTP/WebSocket
┌────────▼────────┐
│   API网关       │
└────────┬────────┘
         │
┌────────▼────────┐
│  股票数据服务   │
│  (FastAPI)     │
└────────┬────────┘
         │
┌────────▼────────┐
│  缓存层(Redis)  │
└────────┬────────┘
         │
┌────────▼────────┐
│  数据源         │
│  (akshare等)    │
└─────────────────┘
```

### Serverless架构
```yaml
# serverless.yml示例
service: stock-quick

provider:
  name: aliyun
  runtime: python3.9

functions:
  getQuote:
    handler: handler.get_quote
    events:
      - http:
          path: /stocks/{symbol}/quote
          method: get
  
  getKline:
    handler: handler.get_kline
    events:
      - http:
          path: /stocks/{symbol}/kline
          method: get
```

## 测试策略

### 单元测试
```python
# 股票服务测试
def test_stock_service():
    service = StockService()
    
    # 测试获取行情
    quote = service.get_quote("000001")
    assert quote is not None
    assert "symbol" in quote
    assert "current" in quote
    
    # 测试K线数据
    kline = service.get_kline("000001", "1d")
    assert len(kline) > 0
```

### 集成测试
```python
# API集成测试
def test_stock_api():
    # 测试行情API
    response = client.get("/stocks/000001/quote")
    assert response.status_code == 200
    
    # 测试K线API
    response = client.get("/stocks/000001/kline?period=1d")
    assert response.status_code == 200
```

## 监控和告警

### 监控指标
1. **API响应时间** - 确保快速响应
2. **数据更新延迟** - 确保数据实时性
3. **错误率** - 监控系统稳定性
4. **用户活跃度** - 监控用户行为

### 告警规则
```yaml
# 告警规则示例
alerts:
  - name: "API响应时间过高"
    condition: "api_response_time > 1000"
    duration: "5m"
    
  - name: "数据更新失败"
    condition: "data_update_error_rate > 0.1"
    duration: "10m"
    
  - name: "用户请求激增"
    condition: "request_rate increase() > 200%"
    duration: "2m"
```

## 相关技能链接

- **前端开发技能** - 图表展示和交互
- **后端开发技能** - API设计和数据服务
- **UI/UX设计技能** - 数据可视化设计
- **DevOps技能** - 部署和监控
- **测试技能** - 质量保证

---

**使用提示**: 当需要进行股票应用开发、数据获取、图表实现或交易逻辑设计时，使用此技能。
