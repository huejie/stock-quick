#!/usr/bin/env python3
"""
直接推送服务（不后台）
在会话中每分钟推送当前时间
"""
import time
from datetime import datetime

def main():
    """主函数：直接推送"""
    count = 0
    
    print("\n" + "=" * 60)
    print("📱 主人，现在开始每分钟推送当前时间消息")
    print("=" * 60)
    print("⚙️  推送间隔：60秒（1分钟）")
    print("⚙️  退出方式：Ctrl+C")
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
            
            # 直接推送（在会话中显示）
            print("=" * 60)
            print(f"📱 [推送 #{count}] {timestamp}")
            print("=" * 60)
            print(f"主人，现在是：{date_str} {time_str}")
            print(f"（{weekday}）")
            print("=" * 60)
            print(f"这是第{count}条推送")
            print("=" * 60)
            print()
            
            # 等待60秒（1分钟）
            print(f"⏰ 等待60秒后推送下一条消息...", end="", flush=True)
            for i in range(60):
                time.sleep(1)
                if (i+1) % 10 == 0:
                    print(f" ({i+1}/60)", end="", flush=True)
            print()  # 换行
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 收到停止信号，推送服务已停止")
        print("=" * 60)
        print(f"📊 总共推送了{count}条消息")
        print("=" * 60)

if __name__ == '__main__':
    main()
