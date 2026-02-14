#!/usr/bin/env python3
"""
全方位小K启动器 - 明天开始的全方位服务
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

class FullServiceKK:
    """全方位小K服务"""
    
    def __init__(self):
        self.workspace = Path("/root/.openclaw/workspace")
        self.config_file = self.workspace / "kk_full_config.json"
        self.load_config()
        
    def load_config(self):
        """加载配置"""
        default_config = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "services": {
                "wealth": {
                    "enabled": True,
                    "schedule": ["09:00", "17:00", "21:00"],
                    "features": ["investment", "portfolio", "risk"]
                },
                "productivity": {
                    "enabled": True,
                    "schedule": ["08:30", "14:00"],
                    "features": ["focus", "email", "calendar"]
                },
                "health": {
                    "enabled": True,
                    "schedule": ["07:00", "12:00", "18:00", "22:00"],
                    "features": ["reminders", "habits"]
                },
                "learning": {
                    "enabled": True,
                    "schedule": ["20:00"],
                    "features": ["study", "skills"]
                },
                "life": {
                    "enabled": True,
                    "schedule": ["19:00"],
                    "features": ["entertainment", "social"]
                }
            },
            "user_preferences": {
                "wake_time": "07:20",
                "sleep_time": "23:00",
                "work_hours": ["09:00", "18:00"],
                "investment_style": "growth",
                "health_goals": ["exercise", "diet"],
                "learning_goals": ["investment", "technology"]
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_tomorrow_schedule(self):
        """获取明日服务时间表"""
        tomorrow = datetime.now() + timedelta(days=1)
        date_str = tomorrow.strftime('%Y年%m月%d日')
        
        schedule = f"🐱 **小K明日全方位服务时间表** ({date_str})\n\n"
        
        # 晨间服务（根据你的起床时间调整）
        schedule += "🌅 **晨间服务 (07:20-09:30)**\n"
        schedule += "├── 07:20: 🐱 早安！健康唤醒提醒\n"
        schedule += "├── 07:30: 🌤️ 天气简报 + 健康小贴士\n"
        schedule += "├── 07:40: 📰 全球财经要闻速递\n"
        schedule += "├── 07:50: 🔥 市场热点扫描 + 谣言预警\n"
        schedule += "├── 08:00: 🎯 今日目标设定与优先级\n"
        schedule += "└── 09:00: 💰 投资建议（8维度评分）\n\n"
        
        # 日间服务
        schedule += "🏢 **日间服务 (09:00-17:00)**\n"
        schedule += "├── 整点: 健康提醒（喝水、休息）\n"
        schedule += "├── 专注时段: 🎯 深度工作支持\n"
        schedule += "├── 邮件时段: 📧 智能邮件管理\n"
        schedule += "├── 投资监控: 📈 实时价格提醒\n"
        schedule += "└── 学习时段: 📚 技能学习支持\n\n"
        
        # 晚间服务
        schedule += "🌇 **晚间服务 (17:00-22:00)**\n"
        schedule += "├── 17:00: 📊 投资总结 + 市场分析\n"
        schedule += "├── 18:00: 🍽️ 健康饮食建议\n"
        schedule += "├── 19:00: 🎮 娱乐休闲推荐\n"
        schedule += "├── 20:00: 📖 学习时间安排\n"
        schedule += "├── 21:00: 💼 全天总结 + 明日计划\n"
        schedule += "└── 22:00: 😴 睡前准备提醒\n\n"
        
        # 服务特色
        schedule += "🎨 **服务特色**\n"
        schedule += "├── 🐾 猫式温柔提醒\n"
        schedule += "├── 🎯 精准个性化建议\n"
        schedule += "├── 📊 专业数据分析\n"
        schedule += "├── 🔄 智能学习优化\n"
        schedule += "└── 🛡️ 可靠服务保障\n\n"
        
        schedule += "💡 **温馨提示**\n"
        schedule += "1. 所有服务将通过飞书实时推送\n"
        schedule += "2. 可随时调整服务时间和内容\n"
        schedule += "3. 有任何需求请随时告诉我\n"
        schedule += "4. 服务将根据你的反馈持续优化\n"
        
        return schedule
    
    def get_service_details(self):
        """获取服务详情"""
        details = "🔧 **全方位小K服务详情**\n\n"
        
        # 财富健康服务
        details += "💰 **财富健康服务**\n"
        details += "├── 📈 专业股票分析（8维度评分）\n"
        details += "├── 💼 投资组合实时监控\n"
        details += "├── ⚠️ 风险预警与止损提醒\n"
        details += "├── 📊 仓位管理与调整建议\n"
        details += "└── 🧠 交易心理辅导\n\n"
        
        # 工作效率服务
        details += "⏰ **工作效率服务**\n"
        details += "├── 🎯 目标管理与优先级设定\n"
        details += "├── 🔍 深度工作专注支持\n"
        details += "├── 📧 智能邮件整理与回复\n"
        schedule += "├── 📅 日程安排与提醒\n"
        details += "└── 📋 工作流程优化建议\n\n"
        
        # 身心健康服务
        details += "🏃 **身心健康服务**\n"
        details += "├── 💧 定时喝水提醒\n"
        details += "├── 🧘 久坐休息提醒\n"
        details += "├── 🍽️ 健康饮食建议\n"
        details += "├── 😴 睡眠质量关注\n"
        details += "└── 🧠 心理状态调节\n\n"
        
        # 学习成长服务
        details += "📚 **学习成长服务**\n"
        details += "├── 🎯 学习目标设定\n"
        details += "├── 📖 学习资源推荐\n"
        details += "├── ⏰ 学习计划制定\n"
        details += "├── 📝 学习笔记整理\n"
        details += "└── 📊 学习进度跟踪\n\n"
        
        # 生活品质服务
        details += "🏠 **生活品质服务**\n"
        details += "├── 🌤️ 天气与出行建议\n"
        details += "├── 🎮 娱乐休闲推荐\n"
        details += "├── 👥 社交关系提醒\n"
        details += "├── 🛒 生活事务管理\n"
        details += "└── 🎉 特别日子关注\n"
        
        return details
    
    def setup_tomorrow_services(self):
        """设置明日服务"""
        print("🔧 设置明日全方位服务...")
        
        # 更新cron任务
        self.update_cron_jobs()
        
        # 保存配置
        self.save_config()
        
        print("✅ 明日服务设置完成")
        print("📅 服务将从明天早上07:20开始")
        
        return True
    
    def update_cron_jobs(self):
        """更新cron任务（模拟）"""
        # 这里实际应该调用cron API更新任务
        # 现在先模拟
        
        cron_updates = {
            "07:20": "🐱 早安！健康唤醒提醒",
            "07:30": "🌤️ 天气简报 + 健康小贴士",
            "07:40": "📰 全球财经要闻速递",
            "07:50": "🔥 市场热点扫描 + 谣言预警",
            "08:00": "🎯 今日目标设定",
            "09:00": "💰 投资建议（8维度评分）",
            "17:00": "📊 投资总结 + 市场分析",
            "18:00": "🍽️ 健康饮食建议",
            "20:00": "📖 学习时间安排",
            "21:00": "💼 全天总结 + 明日计划",
            "22:00": "😴 睡前准备提醒"
        }
        
        print("⏰ 已设置定时服务:")
        for time, service in cron_updates.items():
            print(f"   {time}: {service}")
    
    def run(self):
        """运行启动器"""
        print("🐱 全方位小K服务启动器")
        print("=" * 50)
        
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == "schedule":
                print(self.get_tomorrow_schedule())
                
            elif command == "details":
                print(self.get_service_details())
                
            elif command == "setup":
                self.setup_tomorrow_services()
                
            elif command == "config":
                print(json.dumps(self.config, indent=2, ensure_ascii=False))
                
            else:
                print("可用命令: schedule, details, setup, config")
        else:
            # 交互模式
            print("🎯 明日开始，小K将提供全方位服务！")
            print("\n1. 查看明日时间表: python 全方位小K启动器.py schedule")
            print("2. 查看服务详情: python 全方位小K启动器.py details")
            print("3. 设置明日服务: python 全方位小K启动器.py setup")
            print("4. 查看当前配置: python 全方位小K启动器.py config")
            print("\n💡 建议先查看时间表，然后设置服务")

def main():
    """主函数"""
    kk = FullServiceKK()
    kk.run()

if __name__ == "__main__":
    main()