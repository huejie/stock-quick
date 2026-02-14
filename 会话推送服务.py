#!/usr/bin/env python3
"""
主人消息推送服务（会话中实时推送）
每分钟主动推送当前时间消息到会话中
"""
import time
import threading
from datetime import datetime

# 全局变量：最新推送消息
latest_message = {
    'timestamp': None,
    'content': None,
    'sent_count': 0
}
message_lock = threading.Lock()

def push_message_task():
    """推送任务：每分钟更新推送消息"""
    global latest_message
    
    while True:
        try:
            # 获取当前时间
            now = datetime.now()
            date_str = now.strftime('%Y年%m月%d日')
            time_str = now.strftime('%H时%M分%S秒')
            weekday = now.strftime('%A')
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            
            # 格式化推送消息
            message = f"主人，现在是：{date_str} {time_str} ({weekday})"
            
            # 更新全局推送消息
            with message_lock:
                latest_message = {
                    'timestamp': timestamp,
                    'content': message,
                    'sent_count': latest_message['sent_count'] + 1
                }
            
            # 输出推送消息到会话中
            print("=" * 60)
            print(f"📱 [推送 #{latest_message['sent_count']}] {timestamp}")
            print("=" * 60)
            print(f"{message}")
            print("=" * 60)
            print(f"💬 主人，这是第{latest_message['sent_count']}条推送消息")
            print("=" * 60)
            
            # 等待60秒（1分钟）
            for i in range(60):
                time.sleep(1)
                # 每10秒显示一次进度
                if (i+1) % 10 == 0:
                    print(f"⏰ 等待下一条推送... {60-i-1}秒后", flush=True)
                
        except Exception as e:
            print(f"❌ 推送错误: {e}")
            time.sleep(10)  # 出错后等待10秒再试

def get_latest_message():
    """获取最新推送消息"""
    global latest_message
    return latest_message.copy()

def start_push_service():
    """启动推送服务（在后台线程）"""
    push_thread = threading.Thread(target=push_message_task, daemon=True)
    push_thread.start()
    print("🚀 推送服务已启动！每分钟推送当前时间消息到会话中")
    return push_thread

if __name__ == '__main__':
    print("📱 主人消息推送服务")
    print("=" * 60)
    print("📱 功能：每分钟推送当前时间消息到会话中")
    print("📱 读取方式：直接在会话中看到推送消息")
    print("=" * 60)
    
    # 启动推送服务
    start_push_service()
    
    print("📱 推送服务运行中...")
    print("📱 每分钟会推送一条时间消息")
    print("📱 直接在会话中就能看到")
    print("=" * 60)
    
    try:
        # 主线程等待
        while True:
            time.sleep(60)
            # 每分钟显示一次最新推送消息
            with message_lock:
                if latest_message['content']:
                    print(f"\n📱 [最新推送] {latest_message['content']}")
                    print("=" * 60)
                    print(f"⏰ 已推送：{latest_message['sent_count']}条消息")
                    print("=" * 60)
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 收到停止信号，推送服务已停止")
        print("=" * 60)
