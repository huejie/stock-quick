#!/usr/bin/env python3
"""
飞书消息推送服务
每分钟推送当前时间到飞书
"""
import time
import sys
from datetime import datetime
import requests
import json

# 飞书API配置
FEISHU_WEBHOOK_URL = None  # 需要主人提供
FEISHU_APP_ID = None      # 需要主人提供
FEISHU_APP_SECRET = None  # 需要主人提供

# 时间推送服务
def time_push_service():
    """时间推送服务：每分钟推送当前时间"""
    messages_sent = 0
    
    print("\n" + "=" * 60)
    print("📱 飞书消息推送服务")
    print("=" * 60)
    print("⚠️  配置要求：")
    print("   1. 飞书Webhook URL")
    print("   2. 飞书App ID")
    print("   3. 飞书App Secret")
    print("=" * 60)
    print()
    
    # 检查配置
    if not FEISHU_WEBHOOK_URL:
        print("❌ 飞书Webhook URL未配置")
        print("📝 请设置FEISHU_WEBHOOK_URL变量")
        print("📝 格式：https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        print("=" * 60)
        return
    
    try:
        while True:
            # 获取当前时间
            current_time = datetime.now()
            date_str = current_time.strftime('%Y年%m月%d日')
            time_str = current_time.strftime('%H时%M分%S秒')
            weekday = current_time.strftime('%A')
            timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # 创建飞书消息
            message_content = f"主人，现在是：{date_str} {time_str} ({weekday})"
            
            # 发送到飞书
            try:
                response = send_feishu_message(message_content)
                if response:
                    print(f"✅ [{timestamp}] 消息已推送到飞书")
                    print(f"   内容：{message_content}")
                    print("=" * 60)
                    messages_sent += 1
                else:
                    print(f"❌ [{timestamp}] 推送失败")
                    print("=" * 60)
            except Exception as e:
                print(f"❌ [{timestamp}] 推送错误：{e}")
                print("=" * 60)
            
            # 等待60秒（1分钟）
            for i in range(60):
                if (i+1) % 10 == 0:
                    print(f"⏳ {60-i}秒后推送下一条...", flush=True)
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 收到停止信号")
        print("=" * 60)
        print(f"📊 总共推送了{messages_sent}条消息")
        print("=" * 60)

def send_feishu_message(message):
    """发送消息到飞书"""
    if not FEISHU_WEBHOOK_URL:
        return None
    
    try:
        # 飞书消息格式
        message_data = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        
        # 发送POST请求到飞书Webhook
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            json=message_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                return True
            else:
                return False
        else:
            return False
            
    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False

if __name__ == '__main__':
    print("🚀 飞书消息推送服务启动中...")
    print("=" * 60)
    
    # 启动时间推送服务
    time_push_service()
