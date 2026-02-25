# 小K Web 聊天界面

## 🚀 快速启动

### 方法1: Python 服务器（推荐）

```bash
# 进入目录
cd /root/.openclaw/workspace/web-chat

# 安装依赖
pip install fastapi uvicorn

# 启动服务器
python3 server.py

# 访问
http://你的服务器IP:9999
```

### 方法2: 简单 HTTP 服务器

```bash
# 进入目录
cd /root/.openclaw/workspace/web-chat

# 启动服务器
python3 -m http.server 9999

# 访问
http://你的服务器IP:9999
```

---

## 📁 文件结构

```
/root/.openclaw/workspace/web-chat/
├── index.html       # 聊天界面
├── server.py        # Python 后端服务器
├── config.json      # 配置文件（可选）
└── README.md        # 说明文档
```

---

## ⚙️ 配置说明

### 创建配置文件（可选）

```bash
vim /root/.openclaw/workspace/web-chat/config.json
```

**内容：**
```json
{
  "apiUrl": "http://localhost:9999/api/chat",
  "apiKey": ""
}
```

---

## 🎨 功能特性

- ✅ **美观界面**: 现代化设计，渐变色主题
- ✅ **实时聊天**: 即时响应
- ✅ **打字指示器**: 显示"正在思考"状态
- ✅ **响应式设计**: 支持手机和电脑
- ✅ **消息历史**: 保存聊天记录
- ✅ **Markdown 支持**: 格式化消息

---

## 📊 界面预览

```
┌─────────────────────────────────┐
│  🐱 小K - AI 助手                │
│  在线 · GLM-5 驱动              │
├─────────────────────────────────┤
│                                 │
│  🐱 你好！我是小K...            │
│                                 │
│  👤 帮我查询天气                 │
│                                 │
│  🐱 好的，正在查询...           │
│                                 │
├─────────────────────────────────┤
│  [输入消息...          ] [➤]   │
└─────────────────────────────────┘
```

---

## 🔧 高级配置

### 修改端口

**编辑 server.py:**
```python
uvicorn.run(app, host="0.0.0.0", port=你的端口)
```

### 添加认证

**编辑 server.py:**
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/chat")
async def chat(message: ChatMessage, token: str = Depends(security)):
    # 验证 token
    if token.credentials != "your-secret-token":
        raise HTTPException(status_code=401)
    # 处理消息...
```

### 集成到 Nginx

**Nginx 配置:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:9999;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 🌐 公网访问

### 使用 Nginx 反向代理

1. **安装 Nginx**
```bash
yum install nginx -y
```

2. **配置反向代理**
```bash
vim /etc/nginx/conf.d/webchat.conf
```

3. **添加配置**
```nginx
server {
    listen 80;
    server_name 你的域名或IP;

    location / {
        proxy_pass http://localhost:9999;
    }
}
```

4. **重启 Nginx**
```bash
systemctl restart nginx
```

### 使用 HTTPS

```bash
# 安装 certbot
yum install certbot -y

# 获取证书
certbot certonly --standalone -d 你的域名

# Nginx 配置 SSL
server {
    listen 443 ssl;
    server_name 你的域名;

    ssl_certificate /etc/letsencrypt/live/你的域名/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/你的域名/privkey.pem;

    location / {
        proxy_pass http://localhost:9999;
    }
}
```

---

## 🚀 生产环境部署

### Systemd 服务

**创建服务文件:**
```bash
vim /etc/systemd/system/webchat.service
```

**内容:**
```ini
[Unit]
Description=小K Web Chat Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/web-chat
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/web-chat/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**启动服务:**
```bash
systemctl daemon-reload
systemctl start webchat
systemctl enable webchat
```

---

## 💡 使用建议

1. **安全**: 添加认证机制
2. **性能**: 使用 Nginx 反向代理
3. **监控**: 添加日志记录
4. **备份**: 定期备份配置文件

---

## 🐛 常见问题

### Q: 无法访问？

**A:** 检查防火墙：
```bash
firewall-cmd --add-port=9999/tcp --permanent
firewall-cmd --reload
```

### Q: 连接超时？

**A:** 检查 OpenClaw 是否运行：
```bash
systemctl status openclaw
```

### Q: 如何修改界面？

**A:** 编辑 `index.html` 文件

---

## 📝 更新日志

- **2026-02-25**: 初始版本发布
  - 基础聊天功能
  - 美观界面设计
  - Python 后端支持

---

*小K Web 聊天界面 - 让对话更简单*
