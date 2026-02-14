#!/usr/bin/env python3
import time
import sys
from datetime import datetime

print("主人，现在开始每分钟推送当前时间！")
print("=" * 60)

while True:
    try:
        now = datetime.now()
        msg = f"主人，现在是：{now.strftime('%Y年%m月%d日 %H时%M分%S秒')}"
        print(f"\n[{now.strftime('%H:%M')}] {msg}")
        print("=" * 60)
        
        for i in range(60):
            time.sleep(1)
            if i % 10 == 0:
                print(f"  ⏳ {60-i}秒后推送下一条...", flush=True)
                
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️ 消息推送服务已停止")
        print("=" * 60)
        sys.exit(0)
