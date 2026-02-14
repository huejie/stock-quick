#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主人消息推送服务（超简单版）
"""
import time
import sys
from datetime import datetime

# 禁用输出缓冲
def flush_print(text):
    print(text, flush=True)

flush_print("\n" + "=" * 60)
flush_print("📱 主人，消息推送服务已启动！")
flush_print("=" * 60)
flush_print("📱 每分钟你会收到一条时间消息")
flush_print("=" * 60)

count = 0

while True:
    try:
        count += 1
        
        # 获取当前时间
        now = datetime.now()
        date_str = now.strftime('%Y年%m月%d日')
        time_str = now.strftime('%H时%M分%S秒')
        weekday = now.strftime('%A')
        
        # 推送消息
        flush_print(f"\n📱 [消息 #{count}]")
        flush_print("=" * 60)
        flush_print(f"主人，现在是：{date_str} {time_str}")
        flush_print(f"({weekday})")
        flush_print("=" * 60)
        flush_print(f"这是第{count}条推送")
        flush_print("=" * 60)
        
        # 等待60秒
        flush_print(f"⏰ 等待60秒后推送下一条消息...")
        for i in range(60):
            if i % 10 == 0:
                flush_print(f"   {60-i}秒后推送...", end='\r')
            time.sleep(1)
        flush_print()  # 换行
            
    except KeyboardInterrupt:
        flush_print("\n" + "=" * 60)
        flush_print("⏹️ 消息推送服务已停止")
        flush_print(f"📊 总共推送了{count}条消息")
        flush_print("=" * 60)
        sys.exit(0)
