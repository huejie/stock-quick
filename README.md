# 智投助手

> 股票信息追踪应用 (Web H5 + 微信小程序)

## 项目简介

个人自用的股票信息追踪小程序，快速查看市场热点和自选股动态。

- **快**: 打开即看，3秒掌握市场热点
- **简**: 无广告、无干扰，只显示核心信息
- **全**: A股+港股统一管理

## 技术栈

### 前端
- uni-app (Vue 3 + TypeScript)
- Pinia 状态管理
- uCharts 图表

### 后端
- FastAPI (Python)
- akshare (A股数据)
- yfinance (港股数据)

### 部署
- 云开发/Serverless

## 项目结构

```
stock-quick/
├── frontend/          # uni-app 前端
│   ├── src/
│   │   ├── pages/    # 页面
│   │   ├── components/
│   │   ├── store/    # Pinia
│   │   ├── api/      # API 封装
│   │   └── types/    # TypeScript 类型
│   └── package.json
│
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── api/      # 路由
│   │   ├── services/ # 业务逻辑
│   │   ├── schemas/  # Pydantic 模型
│   │   └── core/     # 配置
│   └── requirements.txt
│
└── agents/           # Subagent 定义
```

## 快速开始

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload
```

后端将运行在 `http://localhost:8000`

API 文档: `http://localhost:8000/docs`

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# H5 开发
npm run dev:h5

# 微信小程序开发
npm run dev:mp-weixin
```

## 功能进度

### MVP (P0) - 当前版本

| 功能 | 状态 |
|------|------|
| 自选股管理 | ✅ 基础完成 |
| 市场热点 | 🚧 开发中 |

### 计划功能

| 功能 | 优先级 |
|------|--------|
| 股票详情 | P1 |
| K线图表 | P1 |
| 价格提醒 | P2 |
| 持仓盈亏 | P2 |

## 开发规范

- 前端代码: `frontend/src/`
- 后端代码: `backend/app/`
- API 规范: RESTful
- 统一响应格式: `{ code, message, data }`

## License

MIT
