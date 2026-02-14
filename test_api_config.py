#!/usr/bin/env python3
"""
API配置测试脚本
测试智谱和Moonshot的编程套餐API调用
"""

import requests
import json

def test_zhipu_api():
    """测试智谱API"""
    print("🔍 测试智谱API...")
    
    api_key = "426d95f7cb9446198df27b638645f30a.IanAwc1u9eck5rzk"
    
    # 测试端点1: 标准端点
    url1 = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers1 = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data1 = {
        "model": "glm-4.7",
        "messages": [
            {"role": "user", "content": "你好，请简单介绍一下自己"}
        ],
        "max_tokens": 100
    }
    
    try:
        response1 = requests.post(url1, headers=headers1, json=data1, timeout=10)
        print(f"标准端点测试: {response1.status_code}")
        if response1.status_code == 200:
            result = response1.json()
            print(f"✅ 标准端点可用")
            print(f"响应: {result['choices'][0]['message']['content'][:50]}...")
        else:
            print(f"❌ 标准端点失败: {response1.text[:200]}")
    except Exception as e:
        print(f"❌ 标准端点异常: {e}")
    
    # 测试端点2: 编程套餐可能使用的端点
    url2 = "https://open.bigmodel.cn/api/paas/v4/completions"
    data2 = {
        "model": "glm-4.7",
        "prompt": "你好，请简单介绍一下自己",
        "max_tokens": 100
    }
    
    try:
        response2 = requests.post(url2, headers=headers1, json=data2, timeout=10)
        print(f"completions端点测试: {response2.status_code}")
        if response2.status_code == 200:
            result = response2.json()
            print(f"✅ completions端点可用")
        else:
            print(f"❌ completions端点失败: {response2.text[:200]}")
    except Exception as e:
        print(f"❌ completions端点异常: {e}")

def test_moonshot_api():
    """测试Moonshot API"""
    print("\n🔍 测试Moonshot API...")
    
    api_key = "sk-Z60hjUnpYyRiWUOd9TGBgv5YbwAJS6p1DlQJTKOiuTuKz93Q"
    
    # 测试端点
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 测试不同的模型
    models_to_test = [
        "moonshot-v1-auto",      # 自动模型
        "moonshot-v1-8k",       # 8k上下文
        "kimi-k2-thinking",      # 当前配置的模型
    ]
    
    for model in models_to_test:
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "你好，请简单介绍一下自己"}
            ],
            "max_tokens": 100
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            print(f"模型 {model}: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {model} 可用")
                break
            else:
                print(f"❌ {model} 失败: {response.text[:100]}")
        except Exception as e:
            print(f"❌ {model} 异常: {e}")

def get_available_models():
    """获取可用的模型列表"""
    print("\n🔍 尝试获取可用模型列表...")
    
    # 智谱模型列表API
    zhipu_url = "https://open.bigmodel.cn/api/paas/v4/models"
    zhipu_api_key = "426d95f7cb9446198df27b638645f30a.IanAwc1u9eck5rzk"
    
    try:
        headers = {"Authorization": f"Bearer {zhipu_api_key}"}
        response = requests.get(zhipu_url, headers=headers, timeout=10)
        if response.status_code == 200:
            models = response.json()
            print("✅ 智谱可用模型:")
            for model in models.get('data', []):
                print(f"   - {model.get('id')}")
        else:
            print(f"❌ 获取模型列表失败: {response.text[:200]}")
    except Exception as e:
        print(f"❌ 获取模型列表异常: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 OpenClaw API配置测试")
    print("=" * 50)
    
    test_zhipu_api()
    test_moonshot_api()
    get_available_models()
    
    print("\n" + "=" * 50)
    print("📝 测试完成")
    print("=" * 50)
