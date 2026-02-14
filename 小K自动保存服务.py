#!/usr/bin/env python3
"""
小K自动保存服务 - 防止卡住和数据丢失
"""

import time
import json
import signal
import sys
from datetime import datetime
from pathlib import Path
from threading import Thread, Event

class KKAutoSaveService:
    """小K自动保存服务"""
    
    def __init__(self, interval_minutes=30):
        self.workspace = Path("/root/.openclaw/workspace")
        self.interval = interval_minutes * 60  # 转换为秒
        self.stop_event = Event()
        self.state_manager = self.create_state_manager()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def create_state_manager(self):
        """创建状态管理器（避免循环导入）"""
        class SimpleStateManager:
            def __init__(self, workspace):
                self.workspace = workspace
                self.backup_dir = workspace / "backups"
                self.backup_dir.mkdir(exist_ok=True)
                
            def save_snapshot(self, data):
                """保存快照"""
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_file = self.backup_dir / f"auto_snapshot_{timestamp}.json"
                
                try:
                    with open(backup_file, 'w', encoding='utf-8') as f:
                        json.dump({
                            'timestamp': datetime.now().isoformat(),
                            'data': data
                        }, f, ensure_ascii=False, indent=2)
                    return True
                except Exception as e:
                    print(f"❌ 快照保存失败: {e}")
                    return False
        
        return SimpleStateManager(self.workspace)
    
    def collect_system_state(self):
        """收集系统状态"""
        try:
            # 收集关键文件状态
            state = {
                'timestamp': datetime.now().isoformat(),
                'critical_files': {},
                'processes': self.get_running_processes(),
                'disk_space': self.get_disk_space(),
                'memory_usage': self.get_memory_usage(),
                'last_heartbeat': time.time()
            }
            
            # 关键文件检查
            critical_files = [
                'user_holdings.json',
                'position_management.json',
                'HEARTBEAT.md',
                'SOUL.md',
                'IDENTITY.md',
                'kk_state.json'
            ]
            
            for file_name in critical_files:
                file_path = self.workspace / file_name
                if file_path.exists():
                    state['critical_files'][file_name] = {
                        'exists': True,
                        'size': file_path.stat().st_size,
                        'mtime': file_path.stat().st_mtime
                    }
                else:
                    state['critical_files'][file_name] = {'exists': False}
            
            return state
            
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def get_running_processes(self):
        """获取运行进程（简化版）"""
        try:
            import subprocess
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            # 只统计相关进程
            relevant = []
            for line in lines[:20]:  # 只取前20行
                if any(keyword in line for keyword in ['python', 'node', 'nginx', 'uvicorn']):
                    relevant.append(line[:100])  # 只取前100字符
            
            return {
                'total_lines': len(lines),
                'relevant_count': len(relevant),
                'sample': relevant[:5]  # 只返回5个样本
            }
        except:
            return {'error': '无法获取进程信息'}
    
    def get_disk_space(self):
        """获取磁盘空间"""
        try:
            import shutil
            usage = shutil.disk_usage(self.workspace)
            return {
                'total_gb': round(usage.total / (1024**3), 2),
                'used_gb': round(usage.used / (1024**3), 2),
                'free_gb': round(usage.free / (1024**3), 2),
                'percent_used': round((usage.used / usage.total) * 100, 1)
            }
        except:
            return {'error': '无法获取磁盘信息'}
    
    def get_memory_usage(self):
        """获取内存使用"""
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            
            mem_info = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    mem_info[key.strip()] = value.strip()
            
            return {
                'total_mb': int(mem_info.get('MemTotal', '0 kB').replace('kB', '').strip()) // 1024,
                'free_mb': int(mem_info.get('MemFree', '0 kB').replace('kB', '').strip()) // 1024,
                'available_mb': int(mem_info.get('MemAvailable', '0 kB').replace('kB', '').strip()) // 1024
            }
        except:
            return {'error': '无法获取内存信息'}
    
    def save_state_snapshot(self):
        """保存状态快照"""
        state = self.collect_system_state()
        success = self.state_manager.save_snapshot(state)
        
        if success:
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] 自动保存完成")
            # 清理旧快照（保留最近24小时）
            self.cleanup_old_snapshots(24)
        else:
            print(f"⚠️  [{datetime.now().strftime('%H:%M:%S')}] 自动保存失败")
        
        return success
    
    def cleanup_old_snapshots(self, keep_hours=24):
        """清理旧快照"""
        cutoff_time = time.time() - (keep_hours * 3600)
        deleted = 0
        
        for file in (self.workspace / "backups").glob("auto_snapshot_*.json"):
            if file.stat().st_mtime < cutoff_time:
                try:
                    file.unlink()
                    deleted += 1
                except:
                    pass
        
        if deleted > 0:
            print(f"🗑️  清理了 {deleted} 个旧快照")
    
    def signal_handler(self, signum, frame):
        """信号处理"""
        print(f"\n📶 收到信号 {signum}，正在停止服务...")
        self.stop_event.set()
    
    def run(self):
        """运行自动保存服务"""
        print("🐱 小K自动保存服务启动")
        print(f"📅 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏰ 保存间隔: {self.interval//60} 分钟")
        print("=" * 50)
        
        save_count = 0
        last_save_time = time.time()
        
        try:
            while not self.stop_event.is_set():
                current_time = time.time()
                
                # 检查是否需要保存
                if current_time - last_save_time >= self.interval:
                    print(f"\n💾 开始第 {save_count + 1} 次自动保存...")
                    
                    if self.save_state_snapshot():
                        save_count += 1
                        last_save_time = current_time
                    
                    # 显示状态摘要
                    state = self.collect_system_state()
                    disk = state.get('disk_space', {})
                    if isinstance(disk, dict) and 'free_gb' in disk:
                        print(f"💾 磁盘: {disk['free_gb']}GB 可用 | 🧠 内存: {state.get('memory_usage', {}).get('available_mb', 0)}MB 可用")
                
                # 等待1分钟再检查
                self.stop_event.wait(60)
                
                # 心跳显示
                if not self.stop_event.is_set():
                    elapsed = int(time.time() - last_save_time)
                    next_save = max(0, self.interval - elapsed)
                    print(f"⏳ 下次保存: {next_save//60}分{next_save%60}秒后", end='\r')
        
        except KeyboardInterrupt:
            print("\n\n🛑 用户中断")
        except Exception as e:
            print(f"\n❌ 服务异常: {e}")
        finally:
            # 最终保存
            print("\n💾 执行最终保存...")
            self.save_state_snapshot()
            
            print(f"\n📊 服务统计:")
            print(f"   总保存次数: {save_count}")
            print(f"   运行时间: {int(time.time() - last_save_time + self.interval)} 秒")
            print(f"   结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\n🐱 小K自动保存服务已停止")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        interval = int(sys.argv[1])
    else:
        interval = 30  # 默认30分钟
    
    service = KKAutoSaveService(interval_minutes=interval)
    service.run()

if __name__ == "__main__":
    main()