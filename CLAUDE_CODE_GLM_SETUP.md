# Claude Code GLM 配置指南

## API Key
`ZjM4NGMyNDYtNDE3MS00Y2JlLTk2MDctYzI2NjM5MmJmOTE3`

## 配置方法

### 方法1: 使用环境变量（推荐）

```bash
export ANTHROPIC_API_KEY="ZjM4NGMyNDYtNDE3MS00Y2JlLTk2MDctYzI2NjM5MmJmOTE3"
export OPENAI_API_KEY="ZjM4NGMyNDYtNDE3MS00Y2JlLTk2MDctYzI2NjM5MmJmOTE3"
export OPENAI_API_BASE="https://open.bigmodel.cn/api/paas/v4"

claude --model glm-4.7 --help
```

### 方法2: 使用settings.json配置文件

位置: `~/.claude/settings.json`

```json
{
  "model": "glm-4.7",
  "apiUrl": "https://openbigmodel.cn/api/paas/v4/chat/completions",
  "apiKey": "ZjM4NGMyNDYtNDE3MS00Y2JlLTk2MDctYzI2NjM5MmJmOTE3",
  "provider": "openai-compatible"
}
```

### 方法3: 直接在命令行中指定

```bash
OPENAI_API_KEY="ZjM4NGMyNDYtNDE3MS00Y2JlLTk2MDctYzI2NjM5MmJmOTE3" \
OPENAI_API_BASE="https://open.bigmodel.cn/api/paas/v4" \
claude --model glm-4.7 --print "Hello, can you see me?"
```

## GLM 模型列表

- glm-4
- glm-4-flash
- glm-4-plus
- glm-4-0520

## 测试配置

```bash
# 测试GLM连接
claude --print "测试：你是谁？"

# 使用特定模型
claude --model glm-4.7 --print "Say hello in Chinese"
```

## 注意事项

1. GLM API是OpenAI兼容的
2. API endpoint: `https://open.bigmodel.cn/api/paas/v4/chat/completions`
3. 需要有效的API key
4. 首次使用可能需要验证
