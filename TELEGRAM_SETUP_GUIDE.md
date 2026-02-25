# Telegram Bot 配置指南

## 📝 前置准备

1. **创建 Telegram Bot**
   - 打开 Telegram
   - 搜索 `@BotFather`
   - 发送 `/newbot`
   - 按提示设置名称和用户名
   - 获取 Bot Token（格式：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`）

2. **获取你的 Telegram ID**
   - 搜索 `@userinfobot`
   - 发送任意消息
   - 获取你的 User ID

---

## 🔧 配置步骤

### 步骤1: 编辑配置文件

```bash
vim ~/.openclaw/openclaw.json
```

### 步骤2: 添加 Telegram 配置

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "你的Bot Token",
      "allowedUsers": ["你的User ID"]
    }
  }
}
```

### 步骤3: 重启 OpenClaw

```bash
openclaw restart
```

### 步骤4: 测试

在 Telegram 中找到你的 Bot，发送消息测试。

---

## 🎯 配置示例

### 完整配置

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx"
    },
    "telegram": {
      "enabled": true,
      "botToken": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
      "allowedUsers": ["123456789"]
    }
  }
}
```

---

## ⚙️ 高级配置

### 限制访问用户

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "你的Token",
      "allowedUsers": ["用户ID1", "用户ID2"]
    }
  }
}
```

### 群组支持

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "你的Token",
      "allowedGroups": ["群组ID1", "群组ID2"]
    }
  }
}
```

---

## 🔒 安全建议

1. **限制访问用户**
   - 只允许你的 User ID 访问
   - 防止他人使用你的 Bot

2. **保护 Bot Token**
   - 不要公开分享 Token
   - 定期重新生成 Token

3. **使用 Webhook**（可选）
   - 更安全
   - 响应更快

---

## 📊 功能对比

| 功能 | 飞书 | Telegram |
|------|------|----------|
| 富文本 | ✅ | ✅ |
| 文件传输 | ✅ | ✅ |
| 语音消息 | ✅ | ✅ |
| 群组支持 | ✅ | ✅ |
| 国际化 | ⚠️ | ✅ |
| 轻量级 | ⚠️ | ✅ |
| 响应速度 | 快 | 极快 |

---

## 💡 使用技巧

### 1. 快速命令

在 Telegram 中可以设置命令：

```
/start - 开始对话
/help - 查看帮助
/status - 查看状态
/clear - 清除上下文
```

### 2. Markdown 支持

Telegram 支持 Markdown 格式：

```
*粗体*
_斜体_
`代码`
```

### 3. 多设备同步

Telegram 支持多设备同时登录，可以在手机、电脑、平板上同时使用。

---

## 🐛 常见问题

### Q: Bot 不响应？

**A:** 检查以下几点：
1. Bot Token 是否正确
2. OpenClaw 是否重启
3. 是否在 allowedUsers 列表中

### Q: 如何获取 User ID？

**A:** 向 `@userinfobot` 发送消息即可获取

### Q: 可以同时使用飞书和 Telegram 吗？

**A:** 可以！配置文件中同时启用即可

---

## 🚀 快速开始

1. 创建 Bot: `@BotFather`
2. 获取 Token
3. 配置 OpenClaw
4. 重启服务
5. 开始对话！

---

*Telegram Bot 配置指南*
*最后更新: 2026-02-25*
