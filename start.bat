@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM Stock-Quick 一键启动脚本 (Windows)
REM 同时启动后端 (FastAPI:8000) 和前端 (uni-app:7777)

echo ========================================
echo    Stock-Quick 智投助手 一键启动
echo ========================================
echo.

cd /d "%~dp0"
set "PROJECT_DIR=%~dp0"
set "BACKEND_DIR=%PROJECT_DIR%backend"
set "FRONTEND_DIR=%PROJECT_DIR%frontend"

REM 设置 Python 路径
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" (
    REM 尝试系统 PATH 中的 python
    where python >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Python 未安装，请先安装 Python
        pause
        exit /b 1
    )
    set "PYTHON_EXE=python"
)

REM 检查 Node.js
where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js/npm 未安装，请先安装 Node.js
    pause
    exit /b 1
)

REM 启动后端
echo [1/2] 启动后端服务 (端口 8000)...
cd /d "%BACKEND_DIR%"

REM 在新窗口启动后端
start "Stock-Quick Backend" cmd /c "cd /d "%BACKEND_DIR%" && "%PYTHON_EXE%" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo 后端服务已启动
echo 后端 API 文档: http://localhost:8000/docs

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端
echo [2/2] 启动前端服务 (端口 7777)...
cd /d "%FRONTEND_DIR%"

REM 检查并安装依赖
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)

REM 在新窗口启动前端
start "Stock-Quick Frontend" cmd /c "cd /d "%FRONTEND_DIR%" && npm run dev:h5"
echo 前端服务已启动

cd /d "%PROJECT_DIR%"

echo.
echo ========================================
echo    所有服务启动完成!
echo ========================================
echo.
echo   前端地址: http://localhost:7777
echo   后端地址: http://localhost:8000
echo   API文档:  http://localhost:8000/docs
echo   健康检查: http://localhost:8000/health
echo.
echo 关闭此窗口不会停止服务
echo 如需停止服务，请关闭对应的命令行窗口
echo.

pause
