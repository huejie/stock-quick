#!/bin/bash
# 运行每日任务脚本

TASK_TYPE=$1
WORKSPACE_DIR="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE_DIR/daily_tasks.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 执行任务: $TASK_TYPE" >> "$LOG_FILE"

cd "$WORKSPACE_DIR"

# 执行Python脚本
OUTPUT=$(python3 daily_tasks.py "$TASK_TYPE" 2>&1)

# 记录输出
echo "$OUTPUT" >> "$LOG_FILE"

# 发送到飞书（通过OpenClaw消息）
# 这里需要调用OpenClaw的API来发送消息
# 暂时先输出到日志

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 任务完成" >> "$LOG_FILE"

# 输出结果（会被cron捕获）
echo "$OUTPUT"