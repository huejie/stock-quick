#!/bin/bash
# 为OpenClaw gateway添加消息去重中间件

SERVICE_FILE="$HOME/.config/systemd/user/openclaw-gateway.service"
BACKUP_FILE="$SERVICE_FILE.backup"

echo "🔧 开始为OpenClaw gateway添加去重中间件..."

# 备份原始文件
if [ ! -f "$BACKUP_FILE" ]; then
  echo "📦 备份原始服务文件..."
  cp "$SERVICE_FILE" "$BACKUP_FILE"
else
  echo "✅ 备份文件已存在"
fi

# 检查是否已经打过补丁
if grep -q "feishu-dedup-middleware" "$SERVICE_FILE"; then
  echo "⚠️  已经打过补丁了"
  echo "如需重新应用，请先恢复备份: cp $BACKUP_FILE $SERVICE_FILE"
  exit 0
fi

# 添加NODE_OPTIONS环境变量，加载去重中间件
echo "📝 修改服务文件..."

# 找到Environment=HOME=/root那一行，在它之后添加NODE_OPTIONS
sed -i '/Environment=HOME=\/root/a Environment=NODE_OPTIONS=--require=/root/.openclaw/workspace/feishu-dedup-middleware.js' "$SERVICE_FILE"

echo "✅ 补丁已应用！"

# 重载systemd配置
echo "🔄 重新加载systemd配置..."
systemctl --user daemon-reload

echo ""
echo "📋 操作完成！"
echo ""
echo "下一步："
echo "  1. 重启OpenClaw gateway:"
echo "     systemctl --user restart openclaw-gateway"
echo "  2. 查看日志确认中间件已加载:"
echo "     journalctl --user -u openclaw-gateway -f | grep Dedup"
echo "  3. 发送测试消息验证去重功能"
echo ""
echo "如需恢复原配置："
echo "  cp $BACKUP_FILE $SERVICE_FILE"
echo "  systemctl --user daemon-reload"
echo "  systemctl --user restart openclaw-gateway"
