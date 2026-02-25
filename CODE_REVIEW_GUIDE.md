# 代码审查系统配置指南

## 📚 目录

1. [系统概述](#系统概述)
2. [文件结构](#文件结构)
3. [审查规则配置](#审查规则配置)
4. [如何添加新规则](#如何添加新规则)
5. [如何修改现有规则](#如何修改现有规则)
6. [如何禁用规则](#如何禁用规则)
7. [测试规则](#测试规则)
8. [常见问题](#常见问题)

---

## 系统概述

### 工作原理

```
GitLab MR提交 → Webhook接收 → 获取代码diff → 运行审查规则 → 发送报告
```

### 核心组件

- **Webhook服务**：`gitlab-webhook-server.py` - 接收GitLab事件
- **审查引擎**：`js-code-reviewer-v3.py` - 执行代码审查
- **规则库**：内置在审查引擎中，可自定义

---

## 文件结构

```
/root/.openclaw/workspace/
├── gitlab-webhook-server.py      # Webhook服务主程序
├── js-code-reviewer-v3.py        # 代码审查引擎（主要修改这个文件）
├── CODE_REVIEW_GUIDE.md          # 本文档
├── CODE_REVIEW_V3_UPGRADE.md     # v3.0升级说明
└── webhook-logs.jsonl            # Webhook日志
```

### 服务管理

```bash
# 查看服务状态
systemctl status gitlab-webhook

# 重启服务
systemctl restart gitlab-webhook

# 查看日志
journalctl -u gitlab-webhook -f

# 查看webhook记录
tail -f /root/.openclaw/workspace/webhook-logs.jsonl
```

---

## 审查规则配置

### 规则结构

每条规则包含以下字段：

```python
{
    'id': 'SEC001',                    # 规则ID（唯一）
    'name': 'XSS风险 - innerHTML',     # 规则名称
    'pattern': r'\.innerHTML\s*=',     # 正则表达式（匹配问题代码）
    'type': '安全性',                  # 问题类型
    'level': 'blocking',               # 问题级别（blocking/optimization）
    'risk': '可能导致XSS攻击',         # 风险说明
    'suggestion': '使用textContent',   # 修改建议
    'frameworks': ['all']              # 适用框架（all/vue/react/angular）
}
```

### 字段说明

#### 1. **id** - 规则ID
- 格式：类型缩写 + 3位数字
- 类型缩写：
  - `SEC` - 安全性（Security）
  - `FUNC` - 功能性（Functional）
  - `QUAL` - 代码质量（Quality）
  - `MAINT` - 可维护性（Maintainability）
  - `PERF` - 性能（Performance）
- 示例：`SEC001`, `QUAL003`, `FUNC002`

#### 2. **name** - 规则名称
- 简洁明了，说明问题类型
- 示例：`XSS风险 - innerHTML`, `使用var声明`

#### 3. **pattern** - 正则表达式
- **重要**：这是匹配问题代码的核心
- 使用Python正则表达式语法
- 常用模式：
  ```python
  r'console\.log\s*\('          # 匹配 console.log()
  r'\bvar\s+\w+'                # 匹配 var 变量声明
  r'\.innerHTML\s*='            # 匹配 .innerHTML =
  r'(password|token)\s*='       # 匹配 password= 或 token=
  ```

#### 4. **type** - 问题类型
- 可选值：
  - `安全性` - 安全漏洞
  - `功能性` - 功能问题
  - `代码质量` - 代码规范
  - `可维护性` - 代码维护
  - `性能` - 性能问题

#### 5. **level** - 问题级别
- `blocking` - 阻断级（必须修复）
- `optimization` - 优化建议（建议改进）

#### 6. **risk** - 风险说明
- 简短说明问题的危害
- 示例：`可能导致XSS攻击`, `生产环境性能影响`

#### 7. **suggestion** - 修改建议
- 提供具体的修改方案
- 示例：`使用textContent替代innerHTML`, `使用let或const`

#### 8. **frameworks** - 适用框架
- `['all']` - 适用于所有框架
- `['vue']` - 仅Vue项目
- `['react']` - 仅React项目
- `['angular']` - 仅Angular项目
- `['vue', 'react']` - Vue和React项目

---

## 如何添加新规则

### 步骤1：确定规则内容

假设你要添加一个规则：**检测alert()使用**

- **问题**：生产代码中不应该使用alert()
- **正则**：`\balert\s*\(`
- **类型**：代码质量
- **级别**：blocking
- **ID**：QUAL006（假设已有QUAL001-QUAL005）

### 步骤2：编辑审查引擎

```bash
vim /root/.openclaw/workspace/js-code-reviewer-v3.py
```

### 步骤3：找到规则列表

在文件中找到 `self.rules = [` 部分（约第22行）

### 步骤4：添加新规则

在规则列表中添加：

```python
{
    'id': 'QUAL006',
    'name': '使用alert()',
    'pattern': r'\balert\s*\(',
    'type': '代码质量',
    'level': 'blocking',
    'risk': '生产环境不应使用alert弹窗',
    'suggestion': '使用自定义弹窗组件或console.log调试',
    'frameworks': ['all']
},
```

### 步骤5：保存并重启服务

```bash
# 保存文件后
systemctl restart gitlab-webhook
```

### 步骤6：测试新规则

```bash
# 创建测试文件
cat > /tmp/test-alert.txt << 'EOF'
diff --git a/test.js b/test.js
--- a/test.js
+++ b/test.js
@@ -0,0 +1,3 @@
+alert('hello');
+console.log('test');
+alert('world');
EOF

# 运行测试
python3 /root/.openclaw/workspace/js-code-reviewer-v3.py "$(cat /tmp/test-alert.txt)"
```

**预期输出：**
```
### 1. [QUAL006] 使用alert()
- **类型**: 代码质量
- **风险**: 生产环境不应使用alert弹窗
- **建议**: 使用自定义弹窗组件或console.log调试
- **出现位置** (2处):
  1. `test.js` 第1行
     ```alert('hello');```
  2. `test.js` 第3行
     ```alert('world');```
```

---

## 如何修改现有规则

### 示例1：修改规则级别

**需求**：将console.log从blocking改为optimization

1. 找到规则：
```python
{
    'id': 'QUAL003',
    'name': 'console.log未移除',
    'pattern': r'console\.log\s*\(',
    'type': '代码质量',
    'level': 'blocking',  # 修改这里
    'risk': '生产环境性能影响',
    'suggestion': '移除或使用条件编译',
    'frameworks': ['all']
}
```

2. 修改：
```python
'level': 'optimization',  # 改为optimization
```

3. 重启服务：
```bash
systemctl restart gitlab-webhook
```

### 示例2：修改正则表达式

**需求**：让console.log规则也匹配console.warn和console.error

1. 找到规则：
```python
'pattern': r'console\.log\s*\(',
```

2. 修改：
```python
'pattern': r'console\.(log|warn|error)\s*\(',
```

3. 测试：
```bash
cat > /tmp/test-console.txt << 'EOF'
diff --git a/test.js b/test.js
--- a/test.js
+++ b/test.js
@@ -0,0 +1,3 @@
+console.log('test');
+console.warn('warning');
+console.error('error');
EOF

python3 /root/.openclaw/workspace/js-code-reviewer-v3.py "$(cat /tmp/test-console.txt)"
```

---

## 如何禁用规则

### 方法1：注释掉规则

```python
# {
#     'id': 'QUAL003',
#     'name': 'console.log未移除',
#     ...
# },
```

### 方法2：删除规则

直接删除整个规则字典

### 方法3：修改框架限制

```python
# 只在Vue项目中启用
'frameworks': ['vue']  # 原来是 ['all']
```

---

## 测试规则

### 快速测试脚本

创建测试脚本 `test-rule.sh`：

```bash
#!/bin/bash

# 测试规则
cat > /tmp/test-diff.txt << 'EOF'
diff --git a/test.js b/test.js
--- a/test.js
+++ b/test.js
@@ -0,0 +1,5 @@
+var x = 1;
+console.log(x);
+alert('test');
+eval('code');
+document.innerHTML = '<p>test</p>';
EOF

echo "运行审查..."
python3 /root/.openclaw/workspace/js-code-reviewer-v3.py "$(cat /tmp/test-diff.txt)"
```

### 测试单个正则表达式

```python
import re

# 测试正则
pattern = r'\balert\s*\('
test_cases = [
    "alert('hello')",    # 应该匹配
    "alert('world')",    # 应该匹配
    "console.log('x')",  # 不应匹配
    "myAlert()",         # 不应匹配
]

for case in test_cases:
    if re.search(pattern, case):
        print(f"✅ 匹配: {case}")
    else:
        print(f"❌ 不匹配: {case}")
```

---

## 常见问题

### Q1: 修改规则后不生效？

**A:** 确保重启了webhook服务：
```bash
systemctl restart gitlab-webhook
```

### Q2: 正则表达式不匹配？

**A:** 使用Python测试正则：
```python
import re
pattern = r'你的正则'
text = "测试代码"
print(re.search(pattern, text))
```

### Q3: 如何查看当前所有规则？

**A:** 查看审查引擎文件：
```bash
grep -A 8 "'id':" /root/.openclaw/workspace/js-code-reviewer-v3.py
```

### Q4: 如何查看审查日志？

**A:** 查看webhook日志：
```bash
tail -f /root/.openclaw/workspace/webhook-logs.jsonl
```

### Q5: 规则太严格，误报太多？

**A:** 调整正则表达式，使其更精确：
- 使用 `\b` 单词边界
- 使用更具体的模式
- 降低规则级别（blocking → optimization）

### Q6: 如何添加Vue/React特定规则？

**A:** 设置 `frameworks` 字段：
```python
{
    'id': 'FUNC001',
    'name': 'Vue - v-for缺少key',
    'pattern': r'v-for=.*(?<!:key=)',
    'frameworks': ['vue'],  # 只在Vue项目中生效
    ...
}
```

---

## 正则表达式快速参考

### 常用模式

| 模式 | 说明 | 示例 |
|------|------|------|
| `\b` | 单词边界 | `\bvar\b` 匹配var但不匹配variable |
| `\s*` | 任意空白字符 | `console\s*\(` 匹配console() |
| `\w+` | 一个或多个字母数字 | `var\s+\w+` 匹配变量声明 |
| `\.` | 点号（转义） | `console\.log` |
| `[^"]*` | 非引号字符 | `"[^"]*"` 匹配字符串 |
| `(?<!x)` | 负向后瞻 | `(?<!:key=)` 前面不是:key= |
| `(a|b)` | 或 | `(log|warn|error)` |

### 示例正则

```python
# 匹配console.log/warn/error
r'console\.(log|warn|error)\s*\('

# 匹配var声明（但不匹配variable）
r'\bvar\s+\w+'

# 匹配==但不匹配===
r'[^=!]==[^=]'

# 匹配innerHTML赋值
r'\.innerHTML\s*='

# 匹配密码硬编码
r'(password|secret|token)\s*[=:]\s*["\'][^"\']+["\']'

# 匹配TODO/FIXME
r'(TODO|FIXME|XXX|HACK):'

# 匹配alert/confirm/prompt
r'\b(alert|confirm|prompt)\s*\('
```

---

## 规则优先级

规则按列表顺序检查，**第一次匹配后停止**（每个代码行只报告一个问题）。

### 建议顺序

1. **安全性问题**（最高优先级）
2. **功能性问题**
3. **代码质量问题**
4. **可维护性问题**
5. **性能问题**（最低优先级）

---

## 完整示例：添加Vue组件name检查规则

### 需求
Vue组件应该有name属性，便于调试

### 实现

```python
{
    'id': 'FUNC005',
    'name': 'Vue - 组件缺少name属性',
    'pattern': r'export\s+default\s+\{[^}]*\}',
    'type': '功能性',
    'level': 'optimization',
    'risk': '组件没有name属性，调试困难',
    'suggestion': '添加name属性：export default { name: "ComponentName", ... }',
    'frameworks': ['vue']
}
```

### 注意事项

这个规则比较复杂，需要检查export default后面是否有name属性。可能需要更复杂的逻辑，建议使用多行匹配或代码解析。

---

## 进阶：自定义审查逻辑

如果正则表达式不够用，可以修改 `check_line` 方法：

```python
def check_line(self, code_line: str, frameworks: List[str]) -> Optional[Dict]:
    """检查单行代码"""
    
    # 自定义逻辑：检查Vue组件name
    if 'vue' in frameworks:
        if 'export default' in code_line:
            # 检查后续几行是否有name
            # ... 复杂逻辑
    
    # 原有的规则检查
    for rule in self.rules:
        # ...
```

---

## 联系与支持

如有问题，可以：
1. 查看日志：`journalctl -u gitlab-webhook -f`
2. 查看文档：本文件
3. 测试规则：使用测试脚本
4. 查看代码：`js-code-reviewer-v3.py`

---

*最后更新：2026-02-25*
*版本：v3.0*
*作者：小K* 🐱
