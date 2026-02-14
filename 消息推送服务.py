#!/usr/bin/env python3
"""
消息推送服务（带状态文件）
"""
import time
import os
import json
from datetime import datetime

# 状态文件
STATE_FILE = '/tmp/push-service-state.json'
# 输出文件
OUTPUT_FILE = '/tmp/push-messages.txt'

# 初始化状态
if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'running': False,
            'last_message_time': None,
            'messages_count': 0
        }, f)

# 清空输出文件
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    pass

def write_message(message):
    """写入消息到输出文件"""
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")

def load_state():
    """加载状态"""
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_state(state):
    """保存状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False)

def main():
    """主函数"""
    print("🚀 消息推送服务启动中...")
    print("=" * 60)
    print("📱 输出文件：", OUTPUT_FILE)
    print("=" * 60)
    
    # 启动服务
    state = {
        'running': True,
        'start_time': datetime.now().isoformat(),
        'messages_count': 0
    }
    save_state(state)
    
    # 立即推送第一条消息
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    time_str = now.strftime('%H时%M分%S秒')
    weekday = now.strftime('%A')
    
    message = f"主人，推送服务已启动！现在是：{date_str} {time_str} ({weekday})"
    write_message(message)
    
    state['messages_count'] = 1
    state['last_message_time'] = now.isoformat()
    save_state(state)
    
    print("✅ 首条消息已推送")
    print("📱 每分钟会推送一条时间消息")
    print("=" * 60)
    
    try:
        while True:
            time.sleep(60)  # 等待60秒（1分钟）
            
            # 推送新消息
            now = datetime.now()
            date_str = now.strftime('%Y年%m月%d日')
            time_str = now.strftime('%H时%M分%S秒')
            weekday = now.strftime('%A')
            
            message = f"主人，现在是：{date_str} {time_str} ({weekday})"
            write_message(message)
            
            state['messages_count'] += 1
            state['last_message_time'] = now.isoformat()
            save_state(state)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 收到停止信号")
        state = load_state()
        state['running'] = False
        state['stopped_time'] = datetime.now().isoformat()
        save_state(state)
        print("✅ 状态已保存")
        print("✅ 推送服务已停止")
        print("=" * 60)

if __name__ == '__main__':
    main()
