#!/usr/bin/env python3
import time
import sys
from datetime import datetime

# 禁用输出缓冲
sys.stdout.reconfigure(line_buffering=False)
sys.stderr.reconfigure(line_buffering=False)

def main():
    print("\n主人，时间推送服务启动中...", flush=True)
    print("=" * 60, flush=True)
    print("每分钟推送当前时间消息", flush=True)
    print("=" * 60, flush=True)
    print()
    
    messages_sent = 0
    
    try:
        while True:
            messages_sent += 1
            
            # 获取当前时间
            now = datetime.now()
            date_str = now.strftime('%Y年%m月%d日')
            time_str = now.strftime('%H时%M分%S秒')
            weekday = now.strftime('%A')
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            
            # 推送消息（立即刷新）
            print("\n" * 2, flush=True)
            print("=" * 60, flush=True)
            print(f"📱 第{messages_sent}条推送 [{timestamp}]", flush=True)
            print("=" * 60, flush=True)
            print(f"主人，现在是：{date_str} {time_str}", flush=True)
            print(f"({weekday})", flush=True)
            print("=" * 60, flush=True)
            print(f"已推送：{messages_sent}条消息", flush=True)
            print("=" * 60, flush=True)
            print("\n" * 2, flush=True)
            
            # 等待60秒（1分钟）
            print(f"⏰ 等待60秒后推送下一条...", flush=True)
            for i in range(60):
                time.sleep(1)
                if (i + 1) % 10 == 0:
                    print(f"  {60 - i}秒后推送...", flush=True)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60, flush=True)
        print("收到停止信号", flush=True)
        print("=" * 60, flush=True)
        print(f"总共推送了{messages_sent}条消息", flush=True)
        print("=" * 60, flush=True)

if __name__ == '__main__':
    main()
