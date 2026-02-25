#!/usr/bin/env python3
"""
JavaScript代码审查脚本 v3.0
优化：
- 问题归类：相同问题合并显示
- 精确定位：显示文件名和行号
- 代码片段：显示问题代码
"""

import re
import sys
from typing import List, Dict, Optional
from collections import defaultdict

class CodeReviewer:
    """代码审查器"""
    
    def __init__(self):
        self.current_file = None
        self.current_line = 0
        
        # 定义检查规则（按优先级排序）
        self.rules = [
            # === 安全性问题（最高优先级）===
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
            {
                'id': 'SEC002',
                'name': '敏感信息硬编码',
                'pattern': r'(password|secret|token|api[_-]?key)\s*[=:]\s*[\'"][^\'"]+[\'"]',
                'type': '安全性',
                'level': 'blocking',
                'risk': '敏感信息泄露风险',
                'suggestion': '使用环境变量或配置文件',
                'frameworks': ['all']
            },
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
            
            # === 功能性问题 ===
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
            
            # === 代码质量问题 ===
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
            
            # === 可维护性问题 ===
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
            
            # === 性能问题 ===
            {
                'id': 'PERF001',
                'name': '循环内定义函数',
                'pattern': r'for\s*\([^)]*\)\s*\{[^}]*(function|\(.*\)\s*=>)[^}]*\}',
                'type': '性能',
                'level': 'optimization',
                'risk': '每次迭代创建新函数，内存浪费',
                'suggestion': '将函数定义移到循环外',
                'frameworks': ['all']
            }
        ]
    
    def detect_framework(self, code: str) -> List[str]:
        """检测代码使用的框架"""
        frameworks = ['all']
        
        if 'vue' in self.current_file.lower() or 'v-for' in code or 'v-if' in code:
            frameworks.append('vue')
        
        if '.jsx' in self.current_file.lower() or 'React' in code or 'className' in code:
            frameworks.append('react')
        
        if '@Component' in code or 'angular' in code.lower():
            frameworks.append('angular')
        
        return frameworks
    
    def check_line(self, code_line: str, frameworks: List[str]) -> Optional[Dict]:
        """检查单行代码"""
        # 跳过空行和注释
        if not code_line.strip() or code_line.strip().startswith(('//', '/*', '*')):
            return None
        
        for rule in self.rules:
            # 检查框架匹配
            if not any(fw in rule['frameworks'] for fw in frameworks):
                continue
            
            # 检查规则匹配
            if re.search(rule['pattern'], code_line, re.IGNORECASE):
                return {
                    'id': rule['id'],
                    'name': rule['name'],
                    'type': rule['type'],
                    'level': rule['level'],
                    'risk': rule['risk'],
                    'suggestion': rule['suggestion'],
                    'file': self.current_file,
                    'line': self.current_line,
                    'code': code_line.strip()[:80]
                }
        
        return None
    
    def review_code(self, diff: str) -> Dict:
        """审查代码并归类问题"""
        lines = diff.split('\n')
        frameworks = ['all']
        
        # 存储所有问题（按问题ID分组）
        issues_grouped = defaultdict(lambda: {
            'info': None,
            'occurrences': []
        })
        
        for i, line in enumerate(lines):
            # 解析文件名
            if line.startswith('+++ b/'):
                self.current_file = line[6:].strip()
                frameworks = self.detect_framework(diff)
                continue
            
            # 解析行号
            if line.startswith('@@'):
                match = re.search(r'\+(\d+)', line)
                if match:
                    self.current_line = int(match.group(1))
                continue
            
            # 跳过diff头部
            if line.startswith(('diff --git', 'index ', '---')):
                continue
            
            # 只检查新增的行
            if not line.startswith('+'):
                if self.current_line > 0:
                    self.current_line += 1
                continue
            
            # 提取代码
            code_line = line[1:].strip() if len(line) > 1 else ""
            
            # 检查代码
            issue = self.check_line(code_line, frameworks)
            if issue:
                issue_id = issue['id']
                
                # 第一次遇到这个问题，保存问题信息
                if issues_grouped[issue_id]['info'] is None:
                    issues_grouped[issue_id]['info'] = {
                        'id': issue['id'],
                        'name': issue['name'],
                        'type': issue['type'],
                        'level': issue['level'],
                        'risk': issue['risk'],
                        'suggestion': issue['suggestion']
                    }
                
                # 添加出现位置
                issues_grouped[issue_id]['occurrences'].append({
                    'file': issue['file'],
                    'line': issue['line'],
                    'code': issue['code']
                })
            
            # 更新行号
            self.current_line += 1
        
        # 分离blocking和optimization问题
        result = {'blocking': [], 'optimization': []}
        
        for issue_id, data in issues_grouped.items():
            if data['info']:
                issue_entry = {
                    'info': data['info'],
                    'occurrences': data['occurrences']
                }
                
                if data['info']['level'] == 'blocking':
                    result['blocking'].append(issue_entry)
                else:
                    result['optimization'].append(issue_entry)
        
        return result

def format_review_result(issues: Dict) -> str:
    """格式化审查结果（问题归类版）"""
    parts = []
    
    # 统计问题数量
    total_blocking = len(issues['blocking'])
    total_optimization = len(issues['optimization'])
    total_occurrences_blocking = sum(len(i['occurrences']) for i in issues['blocking'])
    total_occurrences_optimization = sum(len(i['occurrences']) for i in issues['optimization'])
    
    # 总体评价
    if total_blocking == 0 and total_optimization == 0:
        return "## 总体评价\n\n代码质量良好，未发现明显问题。✅\n\n继续保持！"
    
    parts.append("## 总体评价\n\n")
    if total_blocking > 0:
        parts.append(f"发现 **{total_blocking}类阻断级问题**（共{total_occurrences_blocking}处）需要修复")
    if total_optimization > 0:
        if total_blocking > 0:
            parts.append(f"，**{total_optimization}类优化建议**（共{total_occurrences_optimization}处）供参考")
        else:
            parts.append(f"发现 **{total_optimization}类优化建议**（共{total_occurrences_optimization}处）供参考")
    parts.append("。\n")
    
    # 阻断级问题
    if issues['blocking']:
        parts.append("\n## 🔴 阻断级问题（必须修复）\n")
        for i, issue_entry in enumerate(issues['blocking'], 1):
            info = issue_entry['info']
            occurrences = issue_entry['occurrences']
            
            parts.append(f"\n### {i}. [{info['id']}] {info['name']}\n")
            parts.append(f"- **类型**: {info['type']}\n")
            parts.append(f"- **风险**: {info['risk']}\n")
            parts.append(f"- **建议**: {info['suggestion']}\n")
            parts.append(f"- **出现位置** ({len(occurrences)}处):\n")
            
            for j, occ in enumerate(occurrences, 1):
                parts.append(f"  {j}. `{occ['file']}` 第{occ['line']}行\n")
                parts.append(f"     ```{occ['code']}```\n")
    
    # 优化建议
    if issues['optimization']:
        parts.append("\n## 💡 优化建议（建议改进）\n")
        for i, issue_entry in enumerate(issues['optimization'], 1):
            info = issue_entry['info']
            occurrences = issue_entry['occurrences']
            
            parts.append(f"\n### {i}. [{info['id']}] {info['name']}\n")
            parts.append(f"- **类型**: {info['type']}\n")
            parts.append(f"- **说明**: {info['risk']}\n")
            parts.append(f"- **建议**: {info['suggestion']}\n")
            parts.append(f"- **出现位置** ({len(occurrences)}处):\n")
            
            for j, occ in enumerate(occurrences, 1):
                parts.append(f"  {j}. `{occ['file']}` 第{occ['line']}行\n")
                parts.append(f"     ```{occ['code']}```\n")
    
    # 总结
    parts.append("\n---\n\n")
    parts.append("*本报告由小K代码审查系统v3.0自动生成*")
    
    return "".join(parts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 js-code-reviewer-v3.py '<diff_content>'")
        sys.exit(1)
    
    diff_content = sys.argv[1]
    reviewer = CodeReviewer()
    issues = reviewer.review_code(diff_content)
    result = format_review_result(issues)
    print(result)
