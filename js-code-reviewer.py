#!/usr/bin/env python3
"""
JavaScript代码审查脚本（去重版本）
"""

import re
import sys

def review_js_code(diff: str) -> dict:
    """
    审查JavaScript代码（每个代码行只报告最严重的问题）
    """
    issues = {'blocking': [], 'optimization': []}
    lines = diff.split('\n')
    
    current_file = None
    current_line = 0
    
    for i, line in enumerate(lines):
        # 解析diff文件头
        if line.startswith('+++ b/'):
            current_file = line[6:].strip()
            current_line = 0
            continue
        
        # 解析diff位置信息
        if line.startswith('@@'):
            match = re.search(r'\+(\d+)', line)
            if match:
                current_line = int(match.group(1))
            continue
        
        # 跳过其他diff头部
        if line.startswith('diff --git') or line.startswith('index ') or line.startswith('---'):
            continue
        
        # 只检查新增的行（以+开头），忽略删除的行（以-开头）
        if not line.startswith('+'):
            if current_line > 0:
                current_line += 1
            continue
        
        # 提取实际代码
        code_line = line[1:].strip() if len(line) > 1 else ""
        
        # 如果是空行或注释，跳过
        if not code_line or code_line.startswith('//'):
            current_line += 1
            continue
        
        # 定义检查规则（按优先级排序）
        checks = [
            # 安全性问题（最高优先级）
            {
                'condition': lambda c: 'innerHTML' in c,
                'type': '安全性',
                'issue': 'XSS跨站脚本攻击风险',
                'risk': '直接渲染用户输入的HTML可能导致恶意脚本执行',
                'suggestion': '使用textContent替代innerHTML，或使用DOMPurify等库进行HTML过滤',
                'level': 'blocking'
            },
            # 功能性问题
            {
                'condition': lambda c: 'v-for' in c and ':key' not in c and 'key=' not in c,
                'type': '功能性',
                'issue': 'v-for缺少:key属性',
                'risk': '可能导致Vue渲染错误和性能问题',
                'suggestion': '添加唯一key：v-for="item in list" :key="item.id"',
                'level': 'blocking'
            },
            {
                'condition': lambda c: '.map(' in c and 'key=' not in c,
                'type': '功能性',
                'issue': 'React列表渲染缺少key属性',
                'risk': '可能导致React渲染错误和性能问题',
                'suggestion': '添加唯一key：items.map(item => <div key={item.id}>...</div>)',
                'level': 'blocking'
            },
            {
                'condition': lambda c: 'class=' in c and current_file and current_file.endswith('.jsx'),
                'type': '功能性',
                'issue': 'JSX中使用了class而非className',
                'risk': 'class是JavaScript保留字，会导致语法错误',
                'suggestion': '使用className：<div className="container">',
                'level': 'blocking'
            },
            # 代码质量问题
            {
                'condition': lambda c: c.startswith('var '),
                'type': '代码质量',
                'issue': '使用了var声明变量',
                'risk': 'var有作用域提升问题，let/const更安全',
                'suggestion': '使用let（可变）或const（不可变）替代var',
                'level': 'blocking'
            },
            {
                'condition': lambda c: ' == ' in c or ' != ' in c,
                'type': '代码质量',
                'issue': '使用了弱相等(==)',
                'risk': '可能发生类型转换，导致意外结果',
                'suggestion': '使用强相等(===)或(!==)避免类型转换',
                'level': 'blocking'
            },
            {
                'condition': lambda c: 'console.log' in c,
                'type': '代码质量',
                'issue': '包含console.log调试语句',
                'risk': '生产环境不应包含调试日志',
                'suggestion': '移除或使用条件编译',
                'level': 'blocking'
            },
            # 可维护性问题
            {
                'condition': lambda c: 'TODO' in c or 'FIXME' in c,
                'type': '可维护性',
                'issue': '代码中包含TODO/FIXME标记',
                'risk': '可能遗漏未完成的工作',
                'suggestion': '创建Issue跟踪，或及时处理',
                'level': 'optimization'
            },
            {
                'condition': lambda c: '!important' in c,
                'type': '可维护性',
                'issue': '使用了!important',
                'risk': '降低样式可维护性，难以覆盖',
                'suggestion': '提高选择器优先级或使用CSS Modules替代',
                'level': 'optimization'
            },
            {
                'condition': lambda c: 'http://' in c or 'https://' in c,
                'type': '可维护性',
                'issue': '包含URL硬编码',
                'risk': '环境切换时需要修改代码',
                'suggestion': '移到配置文件或环境变量',
                'level': 'optimization'
            }
        ]
        
        # 检查代码，找到第一个匹配的规则
        for check in checks:
            if check['condition'](code_line):
                issue = {
                    'type': check['type'],
                    'issue': check['issue'],
                    'file': current_file,
                    'line': current_line,
                    'code': code_line[:80],
                    'risk': check['risk'],
                    'suggestion': check['suggestion']
                }
                
                if check['level'] == 'blocking':
                    issues['blocking'].append(issue)
                else:
                    issues['optimization'].append(issue)
                
                # 找到第一个匹配后，跳出循环（每个代码行只报告一个问题）
                break
        
        # 更新行号
        current_line += 1
    
    return issues

def format_review_result(issues: dict, mr_title: str, user: str, project: str) -> str:
    """格式化审查结果"""
    parts = []
    
    # 总体评价
    total = len(issues['blocking']) + len(issues['optimization'])
    if total == 0:
        parts.append("## 总体评价\n代码质量良好，未发现明显问题。✅")
    else:
        parts.append(f"## 总体评价\n发现**{len(issues['blocking'])}个阻断级问题**需要修复，**{len(issues['optimization'])}个优化建议**供参考。")
    
    # 阻断级问题
    if issues['blocking']:
        parts.append("\n## 🔴 阻断级问题（必须修复）")
        for i, issue in enumerate(issues['blocking'], 1):
            if issue['file']:
                parts.append(f"\n### {i}. {issue['type']}：{issue['issue']}")
                parts.append(f"**位置**: `{issue['file']}` 第{issue['line']}行")
                parts.append(f"**代码**: `{issue['code']}`")
                parts.append(f"- **风险**: {issue['risk']}")
                parts.append(f"- **修改建议**: {issue['suggestion']}")
            else:
                parts.append(f"\n### {i}. {issue['type']}：{issue['issue']}")
                parts.append(f"- **风险**: {issue['risk']}")
                parts.append(f"- **修改建议**: {issue['suggestion']}")
    
    # 优化建议
    if issues['optimization']:
        parts.append("\n## 💡 优化建议（建议改进）")
        for i, issue in enumerate(issues['optimization'], 1):
            if issue['file']:
                parts.append(f"\n### {i}. {issue['type']}：{issue['issue']}")
                parts.append(f"**位置**: `{issue['file']}` 第{issue['line']}行")
                parts.append(f"**代码**: `{issue['code']}`")
                parts.append(f"- **说明**: {issue['risk']}")
                parts.append(f"- **修改建议**: {issue['suggestion']}")
            else:
                parts.append(f"\n### {i}. {issue['type']}：{issue['issue']}")
                parts.append(f"- **说明**: {issue['risk']}")
                parts.append(f"- **修改建议**: {issue['suggestion']}")
    
    return "\n".join(parts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 js-code-reviewer.py '<diff_content>'")
        sys.exit(1)
    
    diff_content = sys.argv[1]
    issues = review_js_code(diff_content)
    result = format_review_result(issues, "MR", "user", "project")
    print(result)
