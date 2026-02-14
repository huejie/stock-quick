# 飞书操作快速参考

> 重要！每次飞书操作失败时，先检查以下规则

---

## 🚫 常见错误及解决

### 错误1: 操作失败 / 无权限
**检查清单：**
- [ ] 是否写入到知识库中？（不是机器人名下）
- [ ] 是否使用分段追加方式？
- [ ] 每段是否超过200字符？
- [ ] 是否有Markdown表格？（改为列表）

### 错误2: API 次数消耗过快
**原因**: 飞书插件每分钟检查机器人状态
**解决**: 添加24小时缓存（见下方代码）

### 错误3: 文档找不到
**原因**: 文档创建在机器人名下，不在知识库中
**解决**: 必须创建在知识库中

---

## ✅ 正确操作流程

### 1. 创建/写入文档
```
使用 feishu_doc 工具
操作模式: append（分段追加）
每段长度: < 200字符
格式: 纯文本或简单列表，无表格
```

### 2. 创建定时任务
```
Session: Isolated
Wake Mode: Next heartbeat
Payload: Agent turn
Deliver: true
Channel: Feishu
Enable: true
```

### 3. 权限检查
必须开通的权限：
- `docx:document.block:convert` ✅
- `wiki:wiki` ✅
- `docx:document:create` ✅

---

## 💬 提示词模板

### 写入飞书文档
```
请将以下内容写入飞书知识库：
【内容】

注意：
- 写入到【知识库名称】知识库
- 使用分段追加方式
- 每段不超过200字符
- 不使用Markdown表格
```

### 创建定时任务
```
帮我创建一个新的定时任务提醒
提醒内容：【提醒内容】
执行频率：【执行频率】

按照以下标准创建任务：
- Session: Isolated
- Wake Mode: Next heartbeat
- Payload: Agent turn
- Deliver: true
- Channel: Feishu
- Enable: true
```

---

## 🔧 技术优化

### API 缓存优化代码
添加到飞书插件代码中：

```javascript
// 24小时缓存
const PROBE_CACHE_TTL_MS = 24 * 60 * 60 * 1000;
const probeCache = new Map();

function getCacheKey(cfg) {
  if (!cfg?.appId) return "no-creds";
  return `${cfg.appId}:${cfg.domain ?? "feishu"}`;
}

export async function probeFeishu(cfg) {
  // 先检查缓存
  const cacheKey = getCacheKey(cfg);
  const cached = probeCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < PROBE_CACHE_TTL_MS) {
    return cached.result;
  }

  // 调用API
  // ...

  // 保存到缓存
  probeCache.set(cacheKey, { result, timestamp: Date.now() });
  return result;
}
```

---

## 📝 配置文件位置

### 主配置
`~/.openclaw/openclaw.json`
- 飞书 appId/appSecret
- 渲染模式: `renderMode: "card"`

### 飞书插件代码
`/root/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/extensions/feishu/`
- 需要修改的位置: `probeFeishu` 函数

---

## 🎯 快速检查清单

每次飞书操作前：
- [ ] 知识库 space_id 已配置
- [ ] 使用 append 方式写入
- [ ] 内容分段且每段 < 200字符
- [ ] 无 Markdown 表格
- [ ] 权限已开通
- [ ] 机器人已加入群聊
- [ ] 知识库已创建并添加管理员

---

*更新时间: 2026-02-09*
