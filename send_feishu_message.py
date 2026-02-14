#!/usr/bin/env python3
"""
飞书消息发送脚本
用于定时任务发送消息到飞书
"""

import os
import sys
import json
import requests
from datetime import datetime

def get_feishu_token():
    """获取飞书访问令牌"""
    # 从OpenClaw配置中获取app_id和app_secret
    config_path = "/root/.openclaw/openclaw.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        app_id = config.get("channels", {}).get("feishu", {}).get("appId", "")
        app_secret = config.get("channels", {}).get("feishu", {}).get("appSecret", "")
        
        if not app_id or not app_secret:
            print("错误: 未找到飞书配置")
            return None
        
        # 获取访问令牌
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                return result.get("tenant_access_token")
            else:
                print(f"获取token失败: {result}")
        else:
            print(f"HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"获取token异常: {e}")
    
    return None

def send_feishu_message(message, chat_id=None):
    """发送飞书消息"""
    token = get_feishu_token()
    if not token:
        print("无法获取飞书访问令牌")
        return False
    
    # 如果没有指定chat_id，尝试发送到默认会话
    # 这里需要根据实际情况调整
    if not chat_id:
        # 尝试获取当前会话的chat_id
        # 这里简化处理，实际需要从OpenClaw会话信息中获取
        print("警告: 未指定chat_id，使用默认处理")
        # 这里可以添加逻辑来获取当前会话的chat_id
        return False
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    data = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": message})
    }
    
    try:
        response = requests.post(
            f"{url}?receive_id_type=chat_id",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print(f"消息发送成功: {result.get('data', {}).get('message_id')}")
                return True
            else:
                print(f"消息发送失败: {result}")
        else:
            print(f"HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"发送消息异常: {e}")
    
    return False

def send_simple_message():
    """发送简单的测试消息"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"""🐱 测试消息 - 定时任务系统

时间: {current_time}
来源: Python脚本测试
状态: 定时任务系统工作正常

这是一条通过Python脚本发送的测试消息。
如果收到这条消息，说明定时任务的消息发送机制可以正常工作。"""
    
    print(f"准备发送消息: {message[:50]}...")
    
    # 这里简化处理，实际需要正确的chat_id
    # 暂时只打印消息，不实际发送
    print("消息内容:")
    print(message)
    print("\n注意: 需要配置正确的chat_id才能实际发送到飞书")
    
    # 在实际环境中，这里应该调用 send_feishu_message(message, chat_id)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果有参数，使用参数作为消息
        message = " ".join(sys.argv[1:])
        send_simple_message_custom(message)
    else:
        # 发送默认测试消息
        send_simple_message()