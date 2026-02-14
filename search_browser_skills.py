#!/usr/bin/env python3
"""
下载并搜索GitHub上的OpenClaw浏览器相关skills
"""
import requests
import re

def get_github_readme():
    """下载GitHub README"""
    print("📥 下载 awesome-moltbot-skills README...")
    
    url = "https://raw.githubusercontent.com/VoltAgent/awesome-moltbot-skills/main/README.md"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            print("✅ README下载成功")
            return response.text
        else:
            print(f"❌ 下载失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 下载异常: {e}")
        return None

def search_browser_skills(content):
    """搜索浏览器相关的skills"""
    if not content:
        print("❌ 内容为空")
        return []
    
    print("\n🔍 搜索浏览器相关的skills...")
    
    # 浏览器相关关键词
    keywords = ['browser', 'automation', 'puppet', 'playwright', 'selenium', 
                 'chromium', 'chrome', 'headless', 'web', 'scraping']
    
    found_skills = []
    lines = content.split('\n')
    
    # 搜索包含浏览器关键词的行
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        if any(keyword in line_lower for keyword in keywords):
            # 提取skill名称（通常在markdown链接中）
            # 格式：- [skill-name](url)
            if '](' in line and '](' in line:
                # 提取名称
                name_match = re.search(r'\[([^\]]+)\]', line)
                if name_match:
                    skill_name = name_match.group(1)
                    # 提取URL
                    url_match = re.search(r'\]\((https://[^)]+)\)', line)
                    url = url_match.group(1) if url_match else ""
                    
                    found_skills.append({
                        'name': skill_name,
                        'url': url,
                        'line': line.strip()
                    })
    
    return found_skills

def analyze_browser_skills(skills):
    """分析找到的浏览器skills"""
    print(f"\n📊 找到 {len(skills)} 个浏览器相关的skills")
    
    # 分类统计
    categories = {
        'playwright': [],
        'puppet': [],
        'selenium': [],
        'chrome/chromium': [],
        'automation': []
    }
    
    for skill in skills:
        name_lower = skill['name'].lower()
        line_lower = skill['line'].lower()
        
        if 'playwright' in name_lower or 'playwright' in line_lower:
            categories['playwright'].append(skill['name'])
        if 'puppet' in name_lower or 'puppet' in line_lower:
            categories['puppet'].append(skill['name'])
        if 'selenium' in name_lower or 'selenium' in line_lower:
            categories['selenium'].append(skill['name'])
        if 'chrome' in name_lower or 'chromium' in name_lower:
            categories['chrome/chromium'].append(skill['name'])
        if 'automation' in name_lower or 'headless' in name_lower:
            categories['automation'].append(skill['name'])
    
    return categories

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 OpenClaw浏览器Skills搜索器")
    print("=" * 50)
    
    # 步骤1：下载README
    content = get_github_readme()
    
    if not content:
        print("❌ 无法继续，README下载失败")
        exit(1)
    
    # 步骤2：搜索浏览器skills
    skills = search_browser_skills(content)
    
    # 步骤3：显示结果
    print("\n" + "=" * 50)
    print("📊 搜索结果")
    print("=" * 50)
    
    if skills:
        for i, skill in enumerate(skills[:20], 1):
            print(f"{i}. {skill['name']}")
            print(f"   URL: {skill['url']}")
            print()
    else:
        print("⚠️  未找到浏览器相关的skills")
    
    # 步骤4：分类统计
    print("=" * 50)
    print("📊 按技术分类")
    print("=" * 50)
    
    categories = analyze_browser_skills(skills)
    
    for category, skill_list in categories.items():
        if skill_list:
            print(f"\n{category}:")
            for skill in skill_list:
                print(f"  - {skill}")
    
    # 步骤5：推荐
    print("\n" + "=" * 50)
    print("💡 推荐安装")
    print("=" * 50)
    
    if any('playwright' in s['name'].lower() for s in skills):
        print("🎯 推荐：Playwright（你已经安装过，配置正确）")
    
    if any('automation' in s['line'].lower() for s in skills):
        print("🎯 推荐：Automation相关技能（适合你的OPC项目）")
    
    print("\n💡 安装方式：")
    print("   npx clawhub install <skill-slug>")
    print("   或者: 直接访问skill的GitHub仓库")
