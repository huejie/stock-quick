#!/usr/bin/env python3
"""
主人时间推送服务（超简单版）
每分钟推送一次时间消息到会话中
"""
import time
from datetime import datetime
import sys

# 禁用所有输出缓冲
sys.stdout.reconfigure(line_buffering=False)
sys.stderr.reconfigure(line_buffering=False)

print("主人，时间推送服务启动中...")
print("=" * 60)
print("每分钟会推送一条时间消息到会话中")
print("=" * 60)
print()

messages_sent = 0

try:
    while True:
        # 获取当前时间
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        date_str = now.strftime('%Y年%m月%d日')
        time_str = now.strftime('%H时%M分%S秒')
        weekday = now.strftime('%A')
        
        messages_sent += 1
        
        # 推送消息（强制刷新到会话中）
        print(f"\n主人，现在是：{date_str} {time_str} ({weekday})")
        print("=" * 60)
        print(f"这是第{messages_sent}条推送消息")
        print("=" * 60)
        
        # 强制刷新输出
        sys.stdout.flush()
        
        # 等待60秒（1分钟）
        for i in range(60):
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print("时间推送服务已停止")
    print("=" * 60)
