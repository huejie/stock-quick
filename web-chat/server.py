#!/usr/bin/env python3
"""
小K Web 聊天后端服务器
提供 API 接口与 OpenClaw 集成
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import subprocess
import json
from pathlib import Path

app = FastAPI(title="小K Web Chat", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """返回聊天界面"""
    html_file = Path(__file__).parent / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(), status_code=200)
    return HTMLResponse(content="<h1>聊天界面未找到</h1>", status_code=404)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """处理聊天消息"""
    try:
        # 调用 OpenClaw CLI
        result = subprocess.run(
            ['openclaw', 'send', '--message', message.message],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            reply = result.stdout.strip()
            return ChatResponse(reply=reply)
        else:
            raise HTTPException(status_code=500, detail="OpenClaw 处理失败")

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="请求超时")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "service": "小K Web Chat"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
