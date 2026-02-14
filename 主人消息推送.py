#!/usr/bin/env python3
"""
给主人推送消息的服务
每分钟推送当前时间
"""
import time
from datetime import datetime
import threading

# 心跳状态
heartbeat_running = False
messages_sent = 0

def heartbeat_task():
    """心跳任务：每分钟推送当前时间消息给主人"""
    global heartbeat_running, messages_sent
    
    while heartbeat_running:
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            date_str = datetime.now().strftime('%Y年%m月%d日')
            time_str = datetime.now().strftime('%H时%M分%S秒')
            weekday = datetime.now().strftime('%A')
            
            # 格式化时间消息
            message = f"主人，现在是：{date_str} {time_str} ({weekday})"
            
            # 发送消息到控制台
            print("=" * 60)
            print(f"📱 [{current_time}] 推送给主人的消息")
            print("=" * 60)
            print(f"{message}")
            print("=" * 60)
            print(f"已发送消息数：{messages_sent}")
            print("=" * 60)
            
            messages_sent += 1
            
            # 等待60秒（1分钟）
            for i in range(60):
                if not heartbeat_running:
                    break
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ 心跳任务错误: {e}")

def start_heartbeat():
    """启动心跳任务"""
    global heartbeat_running
    if not heartbeat_running:
        heartbeat_running = True
        heartbeat_thread = threading.Thread(target=heartbeat_task, daemon=True)
        heartbeat_thread.start()
        print("🚀 心跳任务已启动！每分钟推送当前时间消息")

def stop_heartbeat():
    """停止心跳任务"""
    global heartbeat_running
    if heartbeat_running:
        heartbeat_running = False
        print("⏹️ 心跳任务已停止")

if __name__ == '__main__':
    # 直接启动心跳任务
    start_heartbeat()
    
    # 等待用户中断
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 收到停止信号，正在关闭心跳任务...")
        print("=" * 60)
        stop_heartbeat()
        print("✅ 心跳任务已停止")
