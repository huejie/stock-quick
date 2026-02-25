# 代码审查规则快速参考

## 🚀 快速添加规则（3步）

### 1. 编辑文件
```bash
vim /root/.openclaw/workspace/js-code-reviewer-v3.py
```

### 2. 添加规则（约第22行）
```python
{
    'id': 'QUAL006',              # 规则ID
    'name': '使用alert()',         # 规则名称
    'pattern': r'\balert\s*\(',   # 正则表达式
    'type': '代码质量',            # 问题类型
    'level': 'blocking',          # 问题级别
    'risk': '生产环境不应使用alert',  # 风险说明
    'suggestion': '使用自定义弹窗',   # 修改建议
    'frameworks': ['all']         # 适用框架
},
```

### 3. 重启服务
```bash
systemctl restart gitlab-webhook
```

---

## 📋 字段说明

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| id | ✅ | 规则ID | SEC001, QUAL003 |
| name | ✅ | 规则名称 | XSS风险 - innerHTML |
| pattern | ✅ | 正则表达式 | r'\.innerHTML\s*=' |
| type | ✅ | 问题类型 | 安全性/功能性/代码质量/可维护性/性能 |
| level | ✅ | 问题级别 | blocking/optimization |
| risk | ✅ | 风险说明 | 可能导致XSS攻击 |
| suggestion | ✅ | 修改建议 | 使用textContent |
| frameworks | ✅ | 适用框架 | ['all']/['vue']/['react'] |

---

## 🎯 规则ID命名规范

| 前缀 | 类型 | 示例 |
|------|------|------|
| SEC | 安全性 | SEC001, SEC002 |
| FUNC | 功能性 | FUNC001, FUNC002 |
| QUAL | 代码质量 | QUAL001, QUAL002 |
| MAINT | 可维护性 | MAINT001, MAINT002 |
| PERF | 性能 | PERF001, PERF002 |

---

## 📝 常用正则表达式

```python
# console.log/warn/error
r'console\.(log|warn|error)\s*\('

# var声明
r'\bvar\s+\w+'

# 弱相等
r'[^=!]==[^=]'

# innerHTML
r'\.innerHTML\s*='

# eval()
r'\beval\s*\('

# 敏感信息
r'(password|secret|token)\s*[=:]\s*["\'][^"\']+["\']'

# TODO/FIXME
r'(TODO|FIXME|XXX|HACK):'

# alert/confirm/prompt
r'\b(alert|confirm|prompt)\s*\('

# debugger
r'\bdebugger\b'

# !important
r'!important'

# URL硬编码
r'(https?://|/api/)[^\s\'"<>]+'
```

---

## 🧪 测试规则

```bash
# 创建测试文件
cat > /tmp/test-rule.txt << 'EOF'
diff --git a/test.js b/test.js
--- a/test.js
+++ b/test.js
@@ -0,0 +1,3 @@
+alert('test');
+console.log('hello');
+var x = 1;
EOF

# 运行测试
python3 /root/.openclaw/workspace/js-code-reviewer-v3.py "$(cat /tmp/test-rule.txt)"
```

---

## 🔧 常用命令

```bash
# 查看服务状态
systemctl status gitlab-webhook

# 重启服务
systemctl restart gitlab-webhook

# 查看日志
journalctl -u gitlab-webhook -f

# 查看webhook记录
tail -f /root/.openclaw/workspace/webhook-logs.jsonl

# 查看所有规则
grep -A 8 "'id':" /root/.openclaw/workspace/js-code-reviewer-v3.py
```

---

## 🎨 框架限制

```python
# 所有框架
'frameworks': ['all']

# 仅Vue
'frameworks': ['vue']

# 仅React
'frameworks': ['react']

# Vue和React
'frameworks': ['vue', 'react']
```

---

## ⚠️ 注意事项

1. **修改规则后必须重启服务**
2. **每个代码行只报告第一个匹配的问题**
3. **规则按列表顺序检查**
4. **正则表达式使用Python语法**
5. **建议先测试再部署**

---

## 📚 完整文档

详细文档请查看：`CODE_REVIEW_GUIDE.md`

---

*快速参考卡片 - 小K代码审查系统 v3.0*
