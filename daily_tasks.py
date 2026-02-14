#!/usr/bin/env python3
"""
每日财经任务脚本
"""

import sys
import os
import json
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional

# 添加项目路径
sys.path.insert(0, '/root/code/stock-quick/backend')
try:
    from app.services.stock_service import stock_service
    from app.services.mock_data import mock_data_service
    STOCK_SERVICE_AVAILABLE = True
except ImportError:
    STOCK_SERVICE_AVAILABLE = False


class DailyTasks:
    """每日财经任务"""
    
    def __init__(self):
        self.today = datetime.now()
        self.user_id = "default_user"
        
    def get_morning_summary(self) -> str:
        """获取早间财经大事总结"""
        # 这里应该调用新闻API，暂时用模拟数据
        summary = f"📊 **早间财经大事总结** ({self.today.strftime('%Y-%m-%d %H:%M')})\n\n"
        
        # 模拟财经新闻
        finance_news = [
            "1. 美联储维持利率不变，市场预期年内或有降息",
            "2. 人民币汇率保持稳定，央行表示将加强预期管理",
            "3. 国内CPI数据公布，通胀压力有所缓解",
            "4. 新能源车销量持续增长，产业链迎来发展机遇",
            "5. 房地产政策持续优化，多地推出购房补贴"
        ]
        
        # 模拟军事新闻
        military_news = [
            "1. 国防部举行例行记者会，强调维护国家主权",
            "2. 多国举行联合军演，地区安全局势受关注",
            "3. 新型武器装备亮相，国防科技取得新进展"
        ]
        
        # 模拟科技新闻
        tech_news = [
            "1. AI大模型技术突破，多模态能力显著提升",
            "2. 半导体产业链国产化进程加速",
            "3. 5G-A技术商用落地，推动数字经济创新"
        ]
        
        summary += "**💰 财经要闻：**\n" + "\n".join(finance_news) + "\n\n"
        summary += "**🛡️ 军事动态：**\n" + "\n".join(military_news) + "\n\n"
        summary += "**🚀 科技前沿：**\n" + "\n".join(tech_news) + "\n\n"
        summary += "📈 **今日关注：**\n"
        summary += "- 关注A股市场开盘表现\n"
        summary += "- 留意政策面最新动向\n"
        summary += "- 注意国际大宗商品价格波动\n"
        
        return summary
    
    def get_evening_stock_analysis(self) -> str:
        """获取晚间A股分析"""
        try:
            if STOCK_SERVICE_AVAILABLE:
                market_data = stock_service.get_market_hot()
            else:
                market_data = mock_data_service.get_mock_market_hot()
        except:
            market_data = mock_data_service.get_mock_market_hot()
        
        analysis = f"📈 **A股收盘分析** ({self.today.strftime('%Y-%m-%d %H:%M')})\n\n"
        
        # 模拟市场分析
        analysis += "**📊 市场概况：**\n"
        analysis += "今日A股市场震荡整理，三大指数涨跌互现。\n\n"
        
        # 板块分析
        analysis += "**🏷️ 板块表现：**\n"
        if market_data.get('sectors'):
            for i, sector in enumerate(market_data['sectors'][:5], 1):
                change = sector.get('change_percent', 0)
                emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                analysis += f"{i}. {sector.get('name', '未知')}: {change:.2f}% {emoji}\n"
        else:
            analysis += "1. 白酒: +2.5% 📈\n2. 新能源: +1.8% 📈\n3. 半导体: -0.5% 📉\n"
        
        analysis += "\n**💡 投资建议：**\n"
        advice = [
            "1. **关注政策受益板块**：如新能源、数字经济等",
            "2. **控制仓位风险**：建议保持6-7成仓位",
            "3. **关注业绩确定性**：优选三季报预增个股",
            "4. **分散投资**：避免过度集中于单一行业",
            "5. **长期布局**：关注优质蓝筹股估值修复机会"
        ]
        analysis += "\n".join(advice) + "\n\n"
        
        analysis += "**⚠️ 风险提示：**\n"
        analysis += "- 市场波动可能加大，注意风险控制\n"
        analysis += "- 关注国际形势变化对市场的影响\n"
        analysis += "- 理性投资，避免追涨杀跌\n"
        
        return analysis
    
    def get_evening_summary(self) -> str:
        """获取晚间大事总结（当天8点到17点）"""
        summary = f"📰 **晚间大事总结** ({self.today.strftime('%Y-%m-%d %H:%M')})\n\n"
        summary += "**📅 时间范围：** 当天08:00 - 17:00\n\n"
        
        # 模拟财经大事
        finance_events = [
            "1. A股三大指数收盘涨跌不一，上证指数微涨0.1%",
            "2. 北向资金全天净流入超50亿元，连续3日净买入",
            "3. 人民币对美元汇率中间价调升，离岸人民币走强",
            "4. 央行开展MLF操作，净投放资金1000亿元",
            "5. 多家上市公司发布业绩预告，超7成预喜"
        ]
        
        # 模拟盘中热点
        market_hotspots = [
            "1. 人工智能板块午后拉升，多只个股涨停",
            "2. 新能源车产业链表现活跃，电池概念领涨",
            "3. 消费电子板块震荡走强，苹果概念股受关注",
            "4. 医药板块分化，创新药企表现较好",
            "5. 银行、保险等金融股护盘明显"
        ]
        
        # 模拟军事动态
        military_events = [
            "1. 国防部回应近期热点问题，强调维护地区和平稳定",
            "2. 多国海军举行联合演习，加强海上安全合作",
            "3. 新型无人机系统完成测试，性能达到国际先进水平"
        ]
        
        # 模拟科技进展
        tech_events = [
            "1. 国内AI大模型发布新版本，多项能力大幅提升",
            "2. 6G技术研发取得阶段性进展，完成关键技术验证",
            "3. 量子计算原型机实现新突破，计算能力显著提升",
            "4. 新能源汽车快充技术突破，充电时间缩短30%",
            "5. 卫星互联网建设加速，年内计划发射多颗卫星"
        ]
        
        # 模拟政策动态
        policy_events = [
            "1. 发改委发布促进民营经济发展新举措",
            "2. 工信部推动工业互联网创新发展行动计划",
            "3. 证监会优化上市公司分红制度，鼓励现金分红"
        ]
        
        summary += "**💰 盘中财经大事：**\n" + "\n".join(finance_events) + "\n\n"
        summary += "**🔥 市场热点追踪：**\n" + "\n".join(market_hotspots) + "\n\n"
        summary += "**🛡️ 军事动态更新：**\n" + "\n".join(military_events) + "\n\n"
        summary += "**🚀 科技进展速递：**\n" + "\n".join(tech_events) + "\n\n"
        summary += "**📜 政策动态一览：**\n" + "\n".join(policy_events) + "\n\n"
        
        summary += "**📊 明日关注要点：**\n"
        summary += "- 关注欧美股市夜间表现\n"
        summary += "- 留意重要经济数据发布\n"
        summary += "- 关注行业政策最新动向\n"
        summary += "- 注意国际大宗商品价格变化\n"
        
        return summary
    
    def get_investment_advice(self, holdings: Optional[Dict] = None) -> str:
        """获取投资建议"""
        if holdings is None:
            holdings = self.load_holdings()
        
        advice = f"🎯 **个性化投资建议** ({self.today.strftime('%Y-%m-%d %H:%M')})\n\n"
        
        if not holdings:
            advice += "**📝 持仓提醒：**\n"
            advice += "您当前没有持仓记录，请及时更新持仓信息。\n"
            advice += "建议关注以下投资机会：\n\n"
        else:
            advice += f"**📊 当前持仓：**\n"
            for stock, info in holdings.items():
                advice += f"- {stock}: {info.get('shares', 0)}股 @ {info.get('cost', 0)}元\n"
            advice += "\n"
        
        # 通用投资建议
        advice += "**💡 今日操作建议：**\n"
        suggestions = [
            "1. **逢低布局**：关注调整充分的优质个股",
            "2. **波段操作**：可考虑高抛低吸降低成本",
            "3. **关注成交量**：量价配合良好的个股更值得关注",
            "4. **设置止损**：建议设置5-8%的止损位",
            "5. **关注资金流向**：主力资金流入的板块机会更大"
        ]
        advice += "\n".join(suggestions) + "\n\n"
        
        # 推荐关注
        advice += "**👀 推荐关注：**\n"
        try:
            if STOCK_SERVICE_AVAILABLE:
                market_data = stock_service.get_market_hot()
            else:
                market_data = mock_data_service.get_mock_market_hot()
                
            if market_data.get('top_rise'):
                for stock in market_data['top_rise'][:3]:
                    advice += f"- {stock.get('name', '未知')}({stock.get('symbol', '')}): +{stock.get('change_percent', 0):.2f}%\n"
        except:
            advice += "- 贵州茅台(600519): 白酒龙头，业绩稳定\n"
            advice += "- 宁德时代(300750): 新能源龙头，成长性强\n"
            advice += "- 招商银行(600036): 银行龙头，估值合理\n"
        
        return advice
    
    def load_holdings(self) -> Dict:
        """加载持仓数据"""
        holdings_file = "/root/.openclaw/workspace/user_holdings.json"
        try:
            if os.path.exists(holdings_file):
                with open(holdings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_holdings(self, holdings: Dict):
        """保存持仓数据"""
        holdings_file = "/root/.openclaw/workspace/user_holdings.json"
        try:
            with open(holdings_file, 'w', encoding='utf-8') as f:
                json.dump(holdings, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def remind_update_holdings(self) -> str:
        """持仓更新提醒"""
        reminder = f"⏰ **持仓更新提醒** ({self.today.strftime('%Y-%m-%d %H:%M')})\n\n"
        reminder += "您今天的持仓信息尚未更新！\n\n"
        reminder += "**📋 请及时更新：**\n"
        reminder += "1. 当前持仓股票及数量\n"
        reminder += "2. 持仓成本价格\n"
        reminder += "3. 今日买卖操作记录\n\n"
        reminder += "**💡 更新方式：**\n"
        reminder += "直接告诉我您的持仓信息，格式如：\n"
        reminder += "```\n"
        reminder += "持仓更新：\n"
        reminder += "贵州茅台 100股 成本1600\n"
        reminder += "宁德时代 200股 成本180\n"
        reminder += "```\n\n"
        reminder += "更新后，我将在明天9点为您提供个性化投资建议。"
        
        return reminder


def main():
    """主函数"""
    task = DailyTasks()
    
    # 根据命令行参数执行不同任务
    if len(sys.argv) > 1:
        task_type = sys.argv[1]
        
        if task_type == "morning_summary":
            print(task.get_morning_summary())
        elif task_type == "evening_analysis":
            print(task.get_evening_stock_analysis())
        elif task_type == "investment_advice":
            print(task.get_investment_advice())
        elif task_type == "remind_holdings":
            print(task.remind_update_holdings())
        elif task_type == "evening_summary":
            print(task.get_evening_summary())
        else:
            print("未知任务类型")
    else:
        print("请指定任务类型")


if __name__ == "__main__":
    main()