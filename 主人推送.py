#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主人消息推送服务（超简单版）
每分钟推送当前时间
"""
import time
from datetime import datetime
import sys

def main():
    """主函数：直接推送消息"""
    count = 0
    
    print("\n" + "=" * 60)
    print("📱 主人，消息推送服务已启动！")
    print("=" * 60)
    print("⏰ 每分钟推送一次当前时间")
    print("⏹️  Ctrl+C 停止")
    print("=" * 60)
    print()
    
    try:
        while True:
            count += 1
            
            # 获取当前时间
            now = datetime.now()
            date_str = now.strftime('%Y年%m月%d日')
            time_str = now.strftime('%H时%M分%S秒')
            weekday = now.strftime('%A')
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            
            # 推送消息
            print("\n" + "=" * 60)
            print(f"📱 [推送 #{count}] {timestamp}")
            print("=" * 60)
            print(f"主人，现在是：{date_str} {time_str}")
            print(f"({weekday})")
            print("=" * 60)
            print(f"这是第{count}条推送")
            print("=" * 60)
            print()
            
            # 等待60秒（1分钟）
            print(f"⏳ 等待60秒后推送下一条消息...", flush=True)
            for i in range(60):
                if (i+1) % 10 == 0:
                    print(f"  剩余{60-i-1}秒...", flush=True)
                else:
                    print(".", end="", flush=True)
                time.sleep(1)
            print()  # 换行
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 收到停止信号")
        print(f"📊 总共推送了{count}条消息")
        print("=" * 60)
        print("✅ 消息推送服务已停止")
        print("=" * 60)
        sys.exit(0)

if __name__ == '__main__':
    main()
