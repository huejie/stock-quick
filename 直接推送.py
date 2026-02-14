#!/usr/bin/env python3
"""
主人消息推送服务（直接输出版）
每分钟推送当前时间
"""
import time
import sys
from datetime import datetime

print("\n" + "=" * 60)
print("📱 主人，现在开始每分钟推送当前时间消息")
print("=" * 60)
print("\n✅ 服务已启动！")
print("✅ 每分钟你会收到一条时间消息")
print("✅ 内容包括：日期、时间、星期")
print("\n" + "=" * 60)

messages_sent = 0

try:
    while True:
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        date_str = current_time.strftime('%Y年%m月%d日')
        time_str = current_time.strftime('%H时%M分%S秒')
        weekday = current_time.strftime('%A')
        
        # 立即输出（确保被看到）
        sys.stdout.flush()
        print(f"\n📱 [{timestamp}] 第{messages_sent+1}条推送")
        print("=" * 60)
        print(f"主人，现在是：")
        print(f"  日期：{date_str}")
        print(f"  时间：{time_str}")
        print(f"  星期：{weekday}")
        print("=" * 60)
        sys.stdout.flush()
        
        messages_sent += 1
        
        # 等待60秒（1分钟）
        print(f"⏰ 下次推送时间：60秒后...", flush=True)
        for i in range(60):
            time.sleep(1)
            # 每隔10秒显示一次进度
            if (i+1) % 10 == 0:
                print(f"  ⏳ {60-i}秒后推送...", flush=True)
        
except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print("⏹️  收到停止信号")
    print(f"📊 总共推送了{messages_sent}条消息")
    print("=" * 60)
    print("✅ 消息推送服务已停止")
    print("=" * 60)
    sys.stdout.flush()
