# Agent Reach 配置指南

## 📊 当前状态

**可用渠道**: 5/9 (56%)

### ✅ 已配置（5个）

1. ✅ **全网语义搜索** - Exa 搜索已配置
   - 支持全网搜索
   - 支持 Reddit 搜索
   - 支持 Twitter 搜索

2. ✅ **Twitter/X 推文读取**
   - 可读取公开推文
   - 需要 Cookie 才能搜索和发推

3. ✅ **YouTube 视频字幕**
   - yt-dlp 已安装
   - 可提取视频字幕

4. ✅ **RSS/Atom 订阅**
   - feedparser 已安装
   - 可读取 RSS 源

5. ✅ **网页读取**
   - Jina Reader API
   - 可读取任意 URL

### ⚠️ 需配置（4个）

#### P1 - GitHub（需手动安装）
- **状态**: ⚠️ gh CLI 未安装
- **优先级**: P1
- **安装方法**:
```bash
# 方法1：使用脚本
/root/.openclaw/scripts/install-gh-cli.sh

# 方法2：手动安装
cd /tmp
wget https://github.com/cli/cli/releases/download/v2.87.3/gh_2.87.3_linux_amd64.rpm
yum localinstall -y gh_2.87.3_linux_amd64.rpm
```

#### P2 - Twitter 完整功能（需 Cookie）
- **状态**: ⚠️ 只能读取推文
- **优先级**: P2
- **配置方法**:
1. 安装 Cookie-Editor Chrome 扩展
   - https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
2. 访问 x.com 或 twitter.com
3. 点击扩展 → Export → Header String
4. 配置：
```bash
agent-reach configure twitter-cookies "你的Cookie字符串"
```

#### P2 - Reddit & Bilibili（需代理）
- **状态**: ⬜ 服务器 IP 被封
- **优先级**: P2
- **原因**: Reddit 和 Bilibili 封锁服务器 IP
- **解决方案**: 配置 residential proxy
- **推荐**: https://webshare.io ($1/月)
- **配置方法**:
```bash
agent-reach configure proxy http://user:pass@ip:port
```

#### P3 - 小红书（需 MCP）
- **状态**: ⬜ 未配置
- **优先级**: P3
- **配置方法**:
```bash
mcporter config add xiaohongshu http://localhost:18060/mcp
```
- **注意**: 需要先启动小红书 MCP 服务

---

## 🎯 使用示例

### 全网搜索
```bash
# 基本搜索
agent-reach search "AI 最新进展"

# 搜索 Reddit
agent-reach search-reddit "programming tips"

# 搜索 Twitter
agent-reach search-twitter "OpenAI"
```

### 读取网页
```bash
# 读取任意网页
agent-reach read https://example.com

# 读取 GitHub README
agent-reach read https://github.com/user/repo
```

### YouTube
```bash
# 获取视频字幕
agent-reach read https://www.youtube.com/watch?v=VIDEO_ID
```

### RSS 订阅
```bash
# 读取 RSS 源
agent-reach read https://feeds.example.com/rss
```

---

## 📋 快速命令参考

| 命令 | 功能 |
|------|------|
| `agent-reach doctor` | 查看状态 |
| `agent-reach search "query"` | 全网搜索 |
| `agent-reach search-reddit "query"` | Reddit 搜索 |
| `agent-reach search-twitter "query"` | Twitter 搜索 |
| `agent-reach search-github "query"` | GitHub 搜索 |
| `agent-reach search-youtube "query"` | YouTube 搜索 |
| `agent-reach read <url>` | 读取 URL |
| `agent-reach configure twitter-cookies "..."` | 配置 Twitter |
| `agent-reach configure proxy URL` | 配置代理 |

---

## 🔧 配置文件位置

- **mcporter 配置**: `/root/.openclaw/workspace/config/mcporter.json`
- **agent-reach 配置**: `~/.config/agent-reach/`

---

## 📊 功能对比

| 功能 | 状态 | 优先级 | 需要操作 |
|------|------|--------|----------|
| 全网搜索 | ✅ | - | 已配置 |
| Twitter 读取 | ✅ | - | 已配置 |
| YouTube 字幕 | ✅ | - | 已配置 |
| RSS 订阅 | ✅ | - | 已配置 |
| 网页读取 | ✅ | - | 已配置 |
| GitHub 仓库 | ⚠️ | P1 | 安装 gh CLI |
| Twitter 搜索 | ⚠️ | P2 | 配置 Cookie |
| Reddit 读取 | ⬜ | P2 | 配置代理 |
| Bilibili | ⬜ | P2 | 配置代理 |
| 小红书 | ⬜ | P3 | 配置 MCP |

---

## 🚀 下一步建议

### 立即可做
1. ✅ **使用搜索功能** - 已配置，可直接使用
2. ✅ **读取网页** - 已配置，可直接使用
3. ✅ **读取 RSS** - 已配置，可直接使用

### 推荐配置（P1）
4. **安装 gh CLI** - 解锁 GitHub 功能
   ```bash
   /root/.openclaw/scripts/install-gh-cli.sh
   ```

### 可选配置（P2-P3）
5. **配置 Twitter Cookie** - 解锁搜索和发推
6. **配置代理** - 解锁 Reddit 和 Bilibili
7. **配置小红书** - 解锁小红书笔记

---

## 💡 常见问题

### Q: 搜索功能怎么用？
A: 直接使用 `agent-reach search "查询内容"`

### Q: 如何读取 GitHub README？
A: 使用 `agent-reach read https://github.com/user/repo`

### Q: Twitter Cookie 怎么获取？
A: 安装 Cookie-Editor 扩展，访问 x.com，导出 Header String

### Q: 为什么 Reddit 和 Bilibili 不能用？
A: 服务器 IP 被封，需要配置 residential proxy

---

*配置指南 - Agent Reach v1.0.0*
*最后更新: 2026-02-25*
