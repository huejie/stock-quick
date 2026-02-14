#!/usr/bin/env python3
"""
简单的消息推送服务
每分钟推送当前时间
"""
import time
from datetime import datetime

print("🚀 消息推送服务启动中...")
print("=" * 60)

try:
    while True:
        current_time = datetime.now()
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        date_str = current_time.strftime('%Y年%m月%d日')
        hour = current_time.strftime('%H')
        minute = current_time.strftime('%M')
        weekday = current_time.strftime('%A')
        
        message = f"主人，现在是：{date_str} {hour}时{minute}分"
        
        print("=" * 60)
        print(f"📱 [{time_str}] 推送给主人的消息")
        print("=" * 60)
        print(f"{message}")
        print("=" * 60)
        print(f"({weekday})")
        print("=" * 60)
        
        # 等待60秒（1分钟）
        for i in range(60):
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print("⏹️ 消息推送服务已停止")
    print("=" * 60)
