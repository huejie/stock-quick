#!/usr/bin/env python3
"""
小K状态管理器 - 解决保存问题
"""

import os
import json
import time
import sys
from datetime import datetime
from pathlib import Path

class KKStateManager:
    """小K状态管理器"""
    
    def __init__(self):
        self.workspace = Path("/root/.openclaw/workspace")
        self.backup_dir = self.workspace / "backups"
        self.state_file = self.workspace / "kk_state.json"
        
        # 确保目录存在
        self.backup_dir.mkdir(exist_ok=True)
        
    def save_state(self, state_data: dict) -> bool:
        """保存状态到文件"""
        try:
            # 1. 先保存到临时文件
            temp_file = self.state_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'data': state_data
                }, f, ensure_ascii=False, indent=2)
            
            # 2. 原子性替换
            temp_file.replace(self.state_file)
            
            # 3. 创建备份
            backup_file = self.backup_dir / f"kk_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 状态保存成功: {self.state_file}")
            print(f"📁 备份创建: {backup_file}")
            return True
            
        except Exception as e:
            print(f"❌ 状态保存失败: {e}")
            return False
    
    def load_state(self) -> dict:
        """从文件加载状态"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ 状态加载成功")
                return data.get('data', {})
            else:
                print("⚠️  状态文件不存在，返回空状态")
                return {}
        except Exception as e:
            print(f"❌ 状态加载失败: {e}")
            return {}
    
    def get_backup_list(self) -> list:
        """获取备份列表"""
        backups = []
        for file in self.backup_dir.glob("kk_state_*.json"):
            backups.append({
                'file': file.name,
                'size': file.stat().st_size,
                'mtime': datetime.fromtimestamp(file.stat().st_mtime)
            })
        
        # 按时间排序
        backups.sort(key=lambda x: x['mtime'], reverse=True)
        return backups
    
    def restore_backup(self, backup_name: str) -> bool:
        """从备份恢复"""
        backup_file = self.backup_dir / backup_name
        if not backup_file.exists():
            print(f"❌ 备份文件不存在: {backup_name}")
            return False
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # 保存为当前状态
            return self.save_state(backup_data)
            
        except Exception as e:
            print(f"❌ 备份恢复失败: {e}")
            return False
    
    def cleanup_old_backups(self, keep_days: int = 7):
        """清理旧备份"""
        cutoff_time = time.time() - (keep_days * 24 * 3600)
        deleted = 0
        
        for file in self.backup_dir.glob("kk_state_*.json"):
            if file.stat().st_mtime < cutoff_time:
                try:
                    file.unlink()
                    deleted += 1
                except:
                    pass
        
        if deleted > 0:
            print(f"🗑️  清理了 {deleted} 个旧备份")
    
    def get_system_status(self) -> dict:
        """获取系统状态"""
        return {
            'workspace': str(self.workspace),
            'state_file': str(self.state_file),
            'state_exists': self.state_file.exists(),
            'state_size': self.state_file.stat().st_size if self.state_file.exists() else 0,
            'backup_count': len(list(self.backup_dir.glob("kk_state_*.json"))),
            'disk_free': self.get_disk_free(),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_disk_free(self) -> dict:
        """获取磁盘空间"""
        import shutil
        
        try:
            usage = shutil.disk_usage(self.workspace)
            return {
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'free_gb': usage.free / (1024**3),
                'percent_used': (usage.used / usage.total) * 100
            }
        except:
            return {'error': '无法获取磁盘信息'}

def main():
    """主函数"""
    manager = KKStateManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            status = manager.get_system_status()
            print("📊 小K系统状态:")
            print(json.dumps(status, indent=2, ensure_ascii=False))
            
        elif command == "save":
            # 保存当前状态
            current_state = {
                'holdings': manager.load_holdings(),
                'position': manager.load_position(),
                'cron_jobs': manager.load_cron_jobs(),
                'skills': manager.load_skills(),
                'last_updated': datetime.now().isoformat()
            }
            manager.save_state(current_state)
            
        elif command == "load":
            state = manager.load_state()
            print("📂 加载的状态:")
            print(json.dumps(state, indent=2, ensure_ascii=False))
            
        elif command == "backups":
            backups = manager.get_backup_list()
            print("📁 可用备份:")
            for i, backup in enumerate(backups[:10], 1):
                print(f"{i}. {backup['file']} ({backup['size']} bytes, {backup['mtime']})")
                
        elif command == "cleanup":
            manager.cleanup_old_backups()
            
        elif command == "restore" and len(sys.argv) > 2:
            manager.restore_backup(sys.argv[2])
            
        else:
            print("可用命令: status, save, load, backups, cleanup, restore <备份名>")
    else:
        # 交互模式
        print("🐱 小K状态管理器")
        print("=" * 40)
        
        status = manager.get_system_status()
        print(f"工作空间: {status['workspace']}")
        print(f"状态文件: {status['state_file']} ({'存在' if status['state_exists'] else '不存在'})")
        print(f"备份数量: {status['backup_count']}")
        
        disk = status['disk_free']
        if isinstance(disk, dict) and 'free_gb' in disk:
            print(f"磁盘空间: {disk['free_gb']:.1f}GB 可用 ({disk['percent_used']:.1f}% 已用)")
        
        print("\n💡 使用: python 小K状态管理器.py [status|save|load|backups|cleanup|restore]")

# 辅助方法
def load_holdings(self):
    """加载持仓数据"""
    holdings_file = self.workspace / "user_holdings.json"
    try:
        with open(holdings_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def load_position(self):
    """加载仓位管理数据"""
    position_file = self.workspace / "position_management.json"
    try:
        with open(position_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def load_cron_jobs(self):
    """加载cron任务（模拟）"""
    return {
        'count': 8,
        'next_run': '2026-02-04 08:00',
        'jobs': ['早间财经', '投资建议', '晚间分析等']
    }

def load_skills(self):
    """加载技能列表"""
    skills_dir = self.workspace / "skills"
    skills = []
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir():
                skills.append(item.name)
    return skills[:10]  # 只返回前10个

# 添加到类中
KKStateManager.load_holdings = load_holdings
KKStateManager.load_position = load_position
KKStateManager.load_cron_jobs = load_cron_jobs
KKStateManager.load_skills = load_skills

if __name__ == "__main__":
    main()