#!/usr/bin/env python3
"""
飞书登录辅助脚本
"""
import requests
import json
import time

def send_verify_code():
    """发送验证码"""
    print("📱 发送飞书验证码...")
    
    url = "https://passport.feishu.cn/passport/v1/send_code"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    data = {
        "mobile": "17863970031",
        "zone": "+86",
        "action": "login"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 验证码发送成功")
            if result.get("code") == 0:
                print(f"消息: {result.get('msg', 'success')}")
                print(f"data: {result.get('data')}")
                return True
            else:
                print(f"❌ 发送失败: {result}")
        else:
            print(f"❌ HTTP错误: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    return False

def login_with_code(code):
    """使用验证码登录"""
    print(f"\n🔐 使用验证码 {code} 登录...")
    
    url = "https://passport.feishu.cn/passport/v1/login_with_code"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    data = {
        "mobile": "17863970031",
        "zone": "+86",
        "code": code,
        "action": "login"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("登录结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            if result.get("code") == 0:
                token = result.get("data", {}).get("token")
                if token:
                    print(f"\n✅ 登录成功！")
                    print(f"Token: {token[:50]}...")
                    return token
            else:
                print(f"❌ 登录失败: {result.get('msg')}")
        else:
            print(f"❌ HTTP错误: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    return None

if __name__ == "__main__":
    print("=" * 50)
    print("🔐 飞书登录辅助脚本")
    print("=" * 50)
    
    # 步骤1：发送验证码
    if send_verify_code():
        print("\n" + "=" * 50)
        print("📱 请检查手机 17863970031 的短信")
        print("=" * 50)
        
        # 步骤2：获取验证码
        code = input("\n请输入收到的6位验证码: ").strip()
        
        # 步骤3：使用验证码登录
        if code and len(code) == 6:
            token = login_with_code(code)
            
            if token:
                print("\n✅ 登录成功！可以继续使用API了。")
                print(f"Token: {token}")
        else:
            print("❌ 验证码格式不对，应该是6位数字")
    else:
        print("❌ 发送验证码失败，请重试")
