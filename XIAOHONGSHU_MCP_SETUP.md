# 小红书 MCP 配置说明

## 📊 当前状态

**配置状态**: ✅ 已配置
**服务状态**: ❌ 未启动
**可用性**: 0%（需要启动服务）

---

## ✅ 已完成的配置

1. **MCP 配置已添加**
   - 文件：`/root/.openclaw/workspace/config/mcporter.json`
   - 地址：`http://localhost:18060/mcp`
   - 状态：✅ 配置成功

2. **验证配置**
```bash
mcporter config list
```

**输出：**
```
xiaohongshu
  Source: local (/root/.openclaw/workspace/config/mcporter.json)
  Transport: http (http://localhost:18060/mcp)
```

---

## ❌ 需要完成的配置

### 启动小红书 MCP 服务

小红书 MCP 是一个独立的服务，需要单独启动。

#### 方法1: 使用官方 xiaohongshu-mcp

**安装：**
```bash
npm install -g xiaohongshu-mcp
```

**启动：**
```bash
xiaohongshu-mcp --port 18060
```

**验证：**
```bash
curl http://localhost:18060/mcp
```

#### 方法2: 使用 Docker

**拉取镜像：**
```bash
docker pull xiaohongshu-mcp:latest
```

**启动容器：**
```bash
docker run -d \
  --name xiaohongshu-mcp \
  -p 18060:18060 \
  xiaohongshu-mcp:latest
```

#### 方法3: 从源码构建

**克隆仓库：**
```bash
git clone https://github.com/xxx/xiaohongshu-mcp.git
cd xiaohongshu-mcp
```

**安装依赖：**
```bash
npm install
```

**启动服务：**
```bash
npm start -- --port 18060
```

---

## 🎯 使用示例

### 启动服务后

**搜索小红书：**
```bash
agent-reach search-xhs "美妆教程"
```

**读取笔记：**
```bash
agent-reach read https://www.xiaohongshu.com/explore/xxxxx
```

---

## ⚠️ 注意事项

### 1. 服务依赖
- 需要 Node.js 环境
- 可能需要小红书 Cookie（用于登录）

### 2. 端口占用
- 默认端口：18060
- 确保端口未被占用

### 3. 反爬虫
- 小红书有反爬虫机制
- 可能需要配置 Cookie
- 建议设置请求间隔

---

## 🔧 配置 Cookie（可选）

如果需要登录才能访问某些内容：

**获取 Cookie：**
1. 安装 Cookie-Editor Chrome 扩展
2. 访问 xiaohongshu.com
3. 导出 Cookie（Header String 格式）

**配置到服务：**
```bash
export XHS_COOKIE="你的Cookie字符串"
xiaohongshu-mcp --port 18060
```

---

## 📊 优先级

**当前优先级**: P3（最低）

**原因**：
- 需要 additional setup（启动独立服务）
- 小红书内容可以通过网页读取获取
- 不是核心功能

**建议**：
- 如果经常需要小红书内容，建议启动服务
- 如果偶尔使用，可以直接用网页读取

---

## 🚀 快速测试

### 测试服务是否启动

```bash
curl http://localhost:18060/mcp
```

**期望响应：**
```json
{
  "status": "ok",
  "service": "xiaohongshu-mcp"
}
```

### 测试搜索功能

```bash
agent-reach search-xhs "测试"
```

---

## 💡 替代方案

如果不想启动小红书 MCP，可以使用：

### 方案1: 直接网页读取
```bash
agent-reach read https://www.xiaohongshu.com/explore/xxxxx
```

### 方案2: 使用 Exa 搜索
```bash
agent-reach search "小红书 关键词"
```

---

## 📝 总结

**已配置**:
- ✅ MCP 配置已添加到 mcporter.json

**待完成**:
- ❌ 启动 xiaohongshu-mcp 服务（端口 18060）

**建议**:
- 如果需要小红书功能，按照上述方法启动服务
- 如果不急，可以先使用其他已配置的功能

---

*小红书 MCP 配置说明*
*最后更新: 2026-02-25*
