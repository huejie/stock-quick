#!/bin/bash

# Stock-Quick 一键启动脚本
# 同时启动后端 (FastAPI:8000) 和前端 (uni-app:7777)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Stock-Quick 智投助手 一键启动${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查 Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR] Python 未安装${NC}"
    exit 1
fi

# 检查 Node.js
if ! command -v npm &> /dev/null; then
    echo -e "${RED}[ERROR] Node.js/npm 未安装${NC}"
    exit 1
fi

# 启动后端
echo -e "${YELLOW}[1/2] 启动后端服务 (端口 8000)...${NC}"
cd "$BACKEND_DIR"

# 检查虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

# 检查依赖
if [ ! -d ".venv" ] && [ ! -d "venv" ]; then
    echo "安装后端依赖..."
    pip install -r requirements.txt -q
fi

# 启动后端 (后台运行)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo -e "${GREEN}后端服务已启动 (PID: $BACKEND_PID)${NC}"
echo "后端 API 文档: http://localhost:8000/docs"

# 等待后端启动
sleep 2

# 启动前端
echo -e "${YELLOW}[2/2] 启动前端服务 (端口 7777)...${NC}"
cd "$FRONTEND_DIR"

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 启动前端
npm run dev:h5 &
FRONTEND_PID=$!
echo -e "${GREEN}前端服务已启动 (PID: $FRONTEND_PID)${NC}"

# 返回项目目录
cd "$SCRIPT_DIR"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   所有服务启动完成!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "  前端地址: http://localhost:7777"
echo "  后端地址: http://localhost:8000"
echo "  API文档:  http://localhost:8000/docs"
echo "  健康检查: http://localhost:8000/health"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
echo ""

# 保存 PID 到文件
echo $BACKEND_PID > "$SCRIPT_DIR/.backend.pid"
echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"

# 等待任意子进程结束
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f $SCRIPT_DIR/.backend.pid $SCRIPT_DIR/.frontend.pid; exit 0" SIGINT SIGTERM

wait
