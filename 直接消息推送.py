#!/usr/bin/env python3
"""
主人消息推送服务（直接推送）
每分钟推送当前时间
"""
import sys
import time
from datetime import datetime

def main():
    """主函数：直接推送消息"""
    messages_sent = 0
    
    print("🚀 消息推送服务启动中...")
    print("=" * 60)
    print("📱 每分钟推送当前时间消息")
    print("=" * 60)
    
    try:
        while True:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            date_str = datetime.now().strftime('%Y年%m月%d日')
            hour = datetime.now().strftime('%H')
            minute = datetime.now().strftime('%M')
            weekday = datetime.now().strftime('%A')
            
            # 格式化时间消息
            message = f"主人，现在是：{date_str} {hour}时{minute}分 ({weekday})"
            
            # 立即输出，不等待
            sys.stdout.flush()
            print(message)
            sys.stdout.flush()
            print("=" * 60)
            print(f"已发送消息数：{messages_sent}")
            print("=" * 60)
            sys.stdout.flush()
            
            messages_sent += 1
            
            # 等待60秒（1分钟）
            for i in range(60):
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 收到停止信号，消息推送服务已停止")
        print("=" * 60)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
