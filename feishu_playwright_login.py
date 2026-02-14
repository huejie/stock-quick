#!/usr/bin/env python3
"""
使用Playwright登录飞书并上传文档
"""
import json
import sys
from playwright.sync_api import sync_playwright

def login_and_upload_doc():
    """登录飞书并上传文档"""
    
    # 读取OpenClaw手册内容
    print("📖 读取OpenClaw常用指令手册...")
    try:
        with open('/root/.openclaw/workspace/OpenClaw常用指令手册.md', 'r', encoding='utf-8') as f:
            doc_content = f.read()
        print(f"✅ 文档读取成功（{len(doc_content)} 字符）")
    except Exception as e:
        print(f"❌ 读取文档失败: {e}")
        return
    
    # 启动Playwright
    print("\n🚀 启动Playwright...")
    
    with sync_playwright() as p:
        # 启动浏览器（headless=False，这样你能看到）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        try:
            # 步骤1：访问飞书登录页
            print("\n📍 步骤1：访问飞书登录页...")
            page.goto('https://passport.feishu.cn/login')
            page.wait_for_load_state('domcontentloaded')
            print("✅ 页面加载成功")
            
            # 步骤2：输入手机号
            print("\n📍 步骤2：输入手机号...")
            page.fill('input[placeholder="手机号"]', '17863970031')
            page.wait_for_timeout(1000)
            print("✅ 手机号输入成功")
            
            # 步骤3：点击登录
            print("\n📍 步骤3：点击登录按钮...")
            page.click('button:has-text("登录")')
            page.wait_for_timeout(2000)
            print("✅ 登录按钮点击成功")
            
            # 步骤4：等待用户输入验证码
            print("\n📍 步骤4：等待验证码输入...")
            print("🔍 请在浏览器中输入手机 17863970031 收到的验证码")
            print("⏸️  脚本将等待验证码输入完成...")
            
            try:
                # 等待跳转到飞书文档（最多等待120秒）
                page.wait_for_url('https://www.feishu.cn/**', timeout=120000)
                print("\n✅ 登录成功！已跳转到飞书")
            except Exception as e:
                print(f"\n⏸️  等待超时: {e}")
                print("💡 如果已经登录成功，按回车继续...")
                input("按回车继续...")
            
            # 步骤5：打开云文档
            print("\n📍 步骤5：打开云文档...")
            page.goto('https://www.feishu.cn/doc/')
            page.wait_for_load_state('domcontentloaded')
            print("✅ 云文档页面打开成功")
            
            # 步骤6：创建新文档
            print("\n📍 步骤6：创建新文档...")
            page.wait_for_timeout(2000)
            
            try:
                page.click('button[aria-label="新建文档"]')
                page.wait_for_timeout(1000)
                print("✅ 新建文档按钮点击成功")
            except:
                print("⚠️  未找到新建文档按钮，尝试手动操作...")
                print("💡 请手动点击'新建'按钮创建文档")
                input("按回车继续...")
            
            # 步骤7：输入文档标题
            print("\n📍 步骤7：输入文档标题...")
            page.wait_for_timeout(1000)
            
            try:
                title_input = page.query_selector('div[contenteditable="true"][role="heading"]')
                if title_input:
                    title_input.fill('OpenClaw常用指令手册')
                    page.wait_for_timeout(1000)
                    print("✅ 文档标题输入成功")
            except Exception as e:
                print(f"⚠️  自动输入标题失败: {e}")
                print("💡 请手动输入标题：OpenClaw常用指令手册")
                input("按回车继续...")
            
            # 步骤8：粘贴文档内容
            print("\n📍 步骤8：粘贴文档内容...")
            page.wait_for_timeout(1000)
            
            try:
                body_input = page.query_selector('div[contenteditable="true"]:not([role="heading"])')
                if body_input:
                    body_input.fill('')
                    body_input.type(doc_content)
                    page.wait_for_timeout(1000)
                    print(f"✅ 文档内容粘贴成功（{len(doc_content)} 字符）")
            except Exception as e:
                print(f"⚠️  自动粘贴失败: {e}")
                print("💡 请手动粘贴文档内容（已经准备好）")
                input("按回车继续...")
            
            # 步骤9：完成
            print("\n" + "=" * 50)
            print("🎉 文档上传完成！")
            print("=" * 50)
            print("\n💡 提示：")
            print("1. 请检查文档内容是否完整")
            print("2. 可以重命名文档或移动到其他文件夹")
            print("3. 按 Ctrl+C 退出浏览器")
            
            # 保持浏览器打开
            print("\n⏸️  浏览器将保持打开，你可以继续操作...")
            print("💡 输入 'exit' 或按 Ctrl+C 退出脚本")
            
            # 等待用户退出
            while True:
                command = input("输入 'exit' 退出: ").strip().lower()
                if command in ['exit', 'quit', 'q']:
                    break
                page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            print("💡 请截图或记录错误信息")
            input("按回车退出...")
        finally:
            browser.close()
            print("👋 浏览器已关闭")

if __name__ == "__main__":
    print("=" * 50)
    print("🐱 小K的Playwright飞书登录脚本")
    print("=" * 50)
    
    try:
        login_and_upload_doc()
    except KeyboardInterrupt:
        print("\n👋 脚本已中断")
    except Exception as e:
        print(f"\n❌ 脚本执行失败: {e}")
