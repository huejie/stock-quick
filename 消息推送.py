#!/usr/bin/env python3
"""
简单的消息推送服务（带缓冲禁用）
每分钟推送当前时间
"""
import sys
import time
from datetime import datetime

# 禁用Python的输出缓冲
sys.stdout.reconfigure(line_buffering=True)

print("🚀 消息推送服务启动中...")
print("=" * 60)

try:
    messages_sent = 0
    
    while True:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_str = datetime.now().strftime('%Y年%m月%d日')
        time_str = datetime.now().strftime('%H时%M分%S秒')
        weekday = datetime.now().strftime('%A')
        
        # 格式化时间消息
        message = f"主人，现在是：{date_str} {time_str} ({weekday})"
        
        # 立即输出（禁用缓冲）
        print("=" * 60, flush=True)
        print(f"📱 [{current_time}] 推送给主人的消息", flush=True)
        print("=" * 60, flush=True)
        print(f"{message}", flush=True)
        print("=" * 60, flush=True)
        print(f"已发送消息数：{messages_sent}", flush=True)
        print("=" * 60, flush=True)
        
        messages_sent += 1
        
        # 等待60秒（1分钟）
        for i in range(60):
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\n" + "=" * 60, flush=True)
    print("⏹️ 消息推送服务已停止", flush=True)
    print("=" * 60, flush=True)
