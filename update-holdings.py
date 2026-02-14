#!/usr/bin/env python3
"""
更新持仓数据并计算盈亏
"""

import json
import subprocess
from datetime import datetime

# 读取持仓数据
with open('/root/.openclaw/workspace/user_holdings.json', 'r', encoding='utf-8') as f:
    holdings = json.load(f)

# 计算总成本
total_cost = sum(h['shares'] * h['cost'] for h in holdings.values())

print(f"📊 持仓数据更新成功！")
print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"\n当前持仓（{len(holdings)}只）：")

for name, data in holdings.items():
    cost = data['shares'] * data['cost']
    print(f"- {name} ({data['symbol']}) - {data['shares']}股 - 成本{data['cost']}元 (持仓{cost:.2f}元)")

print(f"\n💰 总持仓成本：{total_cost:.2f}元")

print(f"\n⚠️ 注意：当前无法获取实时价格，盈亏计算需要手动提供当前价。")
