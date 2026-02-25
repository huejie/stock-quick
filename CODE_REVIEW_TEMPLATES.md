# 代码审查规则模板

## 📋 规则模板（复制后修改）

```python
{
    'id': 'XXXX',                    # 规则ID（SEC/FUNC/QUAL/MAINT/PERF + 3位数字）
    'name': '规则名称',              # 简洁明了
    'pattern': r'正则表达式',        # Python正则
    'type': '代码质量',              # 安全性/功能性/代码质量/可维护性/性能
    'level': 'blocking',             # blocking/optimization
    'risk': '风险说明',              # 简短说明危害
    'suggestion': '修改建议',        # 具体的修改方案
    'frameworks': ['all']            # all/vue/react/angular
},
```

---

## 🎯 常用规则模板

### 安全性规则

```python
# XSS风险
{
    'id': 'SEC001',
    'name': 'XSS风险 - innerHTML',
    'pattern': r'\.innerHTML\s*=',
    'type': '安全性',
    'level': 'blocking',
    'risk': '可能导致XSS跨站脚本攻击',
    'suggestion': '使用textContent或DOMPurify.sanitize()',
    'frameworks': ['all']
},

# 敏感信息硬编码
{
    'id': 'SEC002',
    'name': '敏感信息硬编码',
    'pattern': r'(password|secret|token|api_key)\s*[=:]\s*[\'"][^\'"]+[\'"]',
    'type': '安全性',
    'level': 'blocking',
    'risk': '敏感信息泄露风险',
    'suggestion': '使用环境变量或配置文件',
    'frameworks': ['all']
},

# eval()使用
{
    'id': 'SEC003',
    'name': 'eval()使用',
    'pattern': r'\beval\s*\(',
    'type': '安全性',
    'level': 'blocking',
    'risk': '代码注入风险',
    'suggestion': '使用JSON.parse()或new Function()',
    'frameworks': ['all']
},

# document.write
{
    'id': 'SEC004',
    'name': 'document.write使用',
    'pattern': r'\bdocument\.write\s*\(',
    'type': '安全性',
    'level': 'blocking',
    'risk': '可能导致XSS攻击',
    'suggestion': '使用DOM操作方法替代',
    'frameworks': ['all']
},
```

### 功能性规则

```python
# Vue - v-for缺少key
{
    'id': 'FUNC001',
    'name': 'Vue - v-for缺少key',
    'pattern': r'v-for=.*(?<!:key=)(?<!key=)',
    'type': '功能性',
    'level': 'blocking',
    'risk': 'Vue渲染错误和性能问题',
    'suggestion': '添加:key="item.id"',
    'frameworks': ['vue']
},

# React - 列表缺少key
{
    'id': 'FUNC002',
    'name': 'React - 列表缺少key',
    'pattern': r'\.map\s*\([^)]*\)\s*=>[^<]*<[A-Z][^>]*(?<!key=)(?<!:key=)',
    'type': '功能性',
    'level': 'blocking',
    'risk': 'React渲染错误和性能问题',
    'suggestion': '添加key={item.id}',
    'frameworks': ['react']
},

# JSX - class而非className
{
    'id': 'FUNC003',
    'name': 'JSX - class而非className',
    'pattern': r'class="[^"]*"',
    'type': '功能性',
    'level': 'blocking',
    'risk': 'JSX语法错误',
    'suggestion': '使用className="..."',
    'frameworks': ['react']
},

# 使用alert/confirm/prompt
{
    'id': 'FUNC004',
    'name': '使用alert/confirm/prompt',
    'pattern': r'\b(alert|confirm|prompt)\s*\(',
    'type': '功能性',
    'level': 'blocking',
    'risk': '生产环境不应使用原生弹窗',
    'suggestion': '使用自定义弹窗组件',
    'frameworks': ['all']
},
```

### 代码质量规则

```python
# 使用var声明
{
    'id': 'QUAL001',
    'name': '使用var声明',
    'pattern': r'\bvar\s+\w+',
    'type': '代码质量',
    'level': 'blocking',
    'risk': '变量提升导致的作用域问题',
    'suggestion': '使用let或const',
    'frameworks': ['all']
},

# 弱相等
{
    'id': 'QUAL002',
    'name': '弱相等(==)',
    'pattern': r'[^=!]==[^=]',
    'type': '代码质量',
    'level': 'blocking',
    'risk': '类型转换导致意外结果',
    'suggestion': '使用强相等(===)或(!==)',
    'frameworks': ['all']
},

# console.log未移除
{
    'id': 'QUAL003',
    'name': 'console.log未移除',
    'pattern': r'console\.log\s*\(',
    'type': '代码质量',
    'level': 'blocking',
    'risk': '生产环境性能影响',
    'suggestion': '移除或使用条件编译',
    'frameworks': ['all']
},

# debugger未移除
{
    'id': 'QUAL004',
    'name': 'debugger未移除',
    'pattern': r'\bdebugger\b',
    'type': '代码质量',
    'level': 'blocking',
    'risk': '生产环境会暂停执行',
    'suggestion': '移除debugger语句',
    'frameworks': ['all']
},

# 未使用的变量（简化版）
{
    'id': 'QUAL005',
    'name': '可能未使用的变量',
    'pattern': r'(const|let|var)\s+(\w+)\s*=[^;]*;(?![\s\S]*\2)',
    'type': '代码质量',
    'level': 'optimization',
    'risk': '代码冗余',
    'suggestion': '移除未使用的变量',
    'frameworks': ['all']
},
```

### 可维护性规则

```python
# TODO/FIXME未处理
{
    'id': 'MAINT001',
    'name': 'TODO/FIXME未处理',
    'pattern': r'(TODO|FIXME|XXX|HACK):',
    'type': '可维护性',
    'level': 'optimization',
    'risk': '可能遗漏未完成工作',
    'suggestion': '创建Issue跟踪或及时处理',
    'frameworks': ['all']
},

# CSS !important滥用
{
    'id': 'MAINT002',
    'name': 'CSS !important滥用',
    'pattern': r'!important',
    'type': '可维护性',
    'level': 'optimization',
    'risk': '样式难以覆盖和维护',
    'suggestion': '提高选择器优先级或使用CSS Modules',
    'frameworks': ['all']
},

# URL硬编码
{
    'id': 'MAINT003',
    'name': 'URL硬编码',
    'pattern': r'(https?://|/api/)[^\s\'"<>]+',
    'type': '可维护性',
    'level': 'optimization',
    'risk': '环境切换需要修改代码',
    'suggestion': '使用环境变量或配置文件',
    'frameworks': ['all']
},

# 魔法数字
{
    'id': 'MAINT004',
    'name': '魔法数字',
    'pattern': r'(?<!["\d])(\d{3,})(?!["\d])',
    'type': '可维护性',
    'level': 'optimization',
    'risk': '数字含义不明确',
    'suggestion': '使用常量并添加注释',
    'frameworks': ['all']
},
```

### 性能规则

```python
# 循环内定义函数
{
    'id': 'PERF001',
    'name': '循环内定义函数',
    'pattern': r'for\s*\([^)]*\)\s*\{[^}]*(function|\(.*\)\s*=>)[^}]*\}',
    'type': '性能',
    'level': 'optimization',
    'risk': '每次迭代创建新函数，内存浪费',
    'suggestion': '将函数定义移到循环外',
    'frameworks': ['all']
},

# 过长的函数（简化版）
{
    'id': 'PERF002',
    'name': '过长的函数',
    'pattern': r'function\s+\w+\s*\([^)]*\)\s*\{[\s\S]{500,}\}',
    'type': '性能',
    'level': 'optimization',
    'risk': '函数职责不单一，难以维护',
    'suggestion': '拆分为多个小函数',
    'frameworks': ['all']
},
```

---

## 🔧 自定义规则示例

### 检测setTimeout没有清除

```python
{
    'id': 'PERF003',
    'name': 'setTimeout未清除',
    'pattern': r'setTimeout\s*\(',
    'type': '性能',
    'level': 'optimization',
    'risk': '可能导致内存泄漏',
    'suggestion': '保存timer引用并在组件卸载时清除',
    'frameworks': ['vue', 'react']
},
```

### 检测直接修改props（Vue）

```python
{
    'id': 'FUNC005',
    'name': 'Vue - 直接修改props',
    'pattern': r'this\.\w+\s*=(?!.*computed)',
    'type': '功能性',
    'level': 'blocking',
    'risk': '违反单向数据流，可能导致bug',
    'suggestion': '使用emit或computed属性',
    'frameworks': ['vue']
},
```

### 检测使用了弃用的生命周期

```python
{
    'id': 'FUNC006',
    'name': 'React - 使用弃用生命周期',
    'pattern': r'(componentWillMount|componentWillReceiveProps|componentWillUpdate)',
    'type': '功能性',
    'level': 'blocking',
    'risk': 'React 17+已弃用',
    'suggestion': '使用componentDidMount或getDerivedStateFromProps',
    'frameworks': ['react']
},
```

---

## 📝 如何使用模板

1. **复制模板**
2. **修改字段**（特别是id、name、pattern）
3. **粘贴到规则列表**（`js-code-reviewer-v3.py` 约22行）
4. **重启服务**
5. **测试验证**

---

## ⚠️ 注意事项

1. **ID唯一性**：确保ID不重复
2. **正则测试**：先测试正则表达式
3. **框架匹配**：选择正确的frameworks
4. **级别选择**：blocking vs optimization
5. **规则顺序**：按优先级排序

---

*规则模板 - 小K代码审查系统 v3.0*
