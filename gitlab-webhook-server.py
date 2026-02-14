#!/usr/bin/env python3
"""
GitLab Webhook接收服务
用于接收GitLab的push、merge request等事件，并进行代码审查
- 接收MR事件
- 获取代码diff
- 通过Claude Code进行代码审查
- 将审查结果发送到飞书
- 自动回复到GitLab MR评论区
"""

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import hmac
import hashlib
import json
import os
import requests
from datetime import datetime
import logging
from pathlib import Path
import subprocess
import time
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(title="GitLab Webhook Receiver", version="2.0.0")

# Webhook Secret (建议从环境变量读取）
WEBHOOK_SECRET = None
LOG_FILE = Path("/root/.openclaw/workspace/webhook-logs.jsonl")

# 飞书通知目标
FEISHU_TARGET_USER = "ou_032db2f8e45df3e207b2ea3a0563df9c"

# GitLab配置
GITLAB_URL = "https://git.iec.io"
GITLAB_TOKEN = "glpat-PXwUZPoBJCzCTLPehb6HXm86MQp1OjJtbgk.01.0z0wr6brq"

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """验证GitLab webhook签名"""
    if not secret:
        return True

    hash_obj = hmac.new(secret.encode('utf-8'), payload, hashlib.sha1)
    expected_signature = f"sha1={hash_obj.hexdigest()}"
    return hmac.compare_digest(signature, expected_signature)

def log_webhook(event_type: str, data: dict):
    """记录webhook事件到日志文件"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "data": data
    }
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "status": "running",
        "service": "GitLab Webhook Receiver with Auto Code Review",
        "version": "2.0.0",
        "features": [
            "接收GitLab webhook事件",
            "自动获取MR diff",
            "AI代码审查",
            "飞书通知",
            "自动回复到GitLab MR评论区"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/webhook/gitlab")
async def handle_gitlab_webhook(
    request: Request,
    x_gitlab_token: str = Header(None),
    x_gitlab_event: str = Header(None)
):
    """处理GitLab webhook请求"""
    try:
        payload = await request.body()
        data = await request.json()

        # 验证签名（如果配置了secret）
        if WEBHOOK_SECRET and x_gitlab_token:
            if not verify_signature(payload, x_gitlab_token, WEBHOOK_SECRET):
                logger.warning("Invalid webhook signature")
                raise HTTPException(status_code=403, detail="Invalid signature")

        # 获取事件类型
        event_type = x_gitlab_event or data.get('object_kind', 'Unknown')

        logger.info(f"Received webhook: {event_type}")

        # 记录webhook事件
        log_webhook(event_type, data)

        # 根据事件类型处理
        if event_type == "Push Hook":
            await handle_push_event(data)
        elif event_type == "Merge Request Hook":
            await handle_merge_request_event(data)
        elif event_type == "Tag Push Hook":
            await handle_tag_push_event(data)
        elif event_type == "Pipeline Hook":
            await handle_pipeline_event(data)

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": f"Webhook received: {event_type}"}
        )

    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

def get_gitlab_diff(project_id: int, mr_iid: int) -> str:
    """获取GitLab MR的代码diff"""
    try:
        url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/diffs"
        headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            diffs = response.json()
            # 提取所有diff内容
            diff_text = ""
            for diff in diffs:
                diff_text += diff.get('diff', '') + "\n\n"

            # 限制diff长度
            if len(diff_text) > 6000:
                diff_text = diff_text[:6000] + "\n\n... (diff已截断，超过6000字符)"

            return diff_text
        else:
            logger.error(f"Failed to get diff: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Error getting diff: {e}")
        return None

def post_gitlab_mr_comment(project_id: int, mr_iid: int, comment: str) -> bool:
    """
    在GitLab MR评论区添加评论

    参数:
        project_id: 项目ID
        mr_iid: MR的IID（不是ID）
        comment: 评论内容

    返回:
        是否成功
    """
    try:
        url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
        headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

        data = {
            "body": comment
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 201:
            logger.info(f"Comment posted to MR {mr_iid} successfully")
            return True
        else:
            logger.error(f"Failed to post comment: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        logger.error(f"Error posting MR comment: {e}")
        return False

def run_claude_code_review(prompt: str) -> str:
    """
    使用Claude Code运行代码审查

    参数:
        prompt: 审查提示词

    返回:
        审查结果（或None如果失败）
    """
    session_name = f"code-review-{int(time.time())}"
    wingman_cmd = [
        '/root/code/claude-code-wingman/claude-wingman.sh',
        '--session', session_name,
        '--workdir', '/tmp',
        '--prompt', prompt
    ]

    try:
        logger.info(f"Claude Code review started: {session_name}")
        logger.info(f"Full command: {' '.join(wingman_cmd)}")

        # 直接运行Claude Code，等待完成（90秒超时）
        process = subprocess.run(
            wingman_cmd,
            capture_output=True,
            text=True,
            timeout=90
        )

        logger.info(f"Process returncode: {process.returncode}")
        logger.info(f"Process timeout: {'yes' if process.returncode is None else 'no'}")

        if process.returncode == 0:
            output = process.stdout
            stderr = process.stderr

            # 添加调试日志
            logger.info(f"Raw stdout length: {len(output) if output else 0} chars")
            logger.info(f"Raw stderr length: {len(stderr) if stderr else 0} chars")
            logger.info(f"Raw stdout preview: {output[:300] if output else 'None'}")

            # 如果stdout为空，尝试使用stderr
            if not output or len(output.strip()) < 10:
                if stderr and len(stderr.strip()) > 10:
                    logger.warning(f"Using stderr as output (stdout empty)")
                    output = stderr
                else:
                    logger.warning(f"Both stdout and stderr are empty or too short")
                    return "Claude Code无输出，可能prompt太短或模型响应为空。"

            # 过滤掉Claude Code的UI输出，只保留实际内容
            review_lines = []
            skip_patterns = [
                r'Claude Code',
                r'Welcome',
                r'Recent activity',
                r'GLM',
                r'Tips for',
                r'─+', r'│', r'╭', r'╯', r'▐', r'▝', r'▘', r'●',
                r'❯', r'esc', r'model to try', r'\[plugins\]',
                r'System Prompt', r'You can', r'Started server',
                r'Waiting for', r'Application startup',
                r'Uvicorn running', r'Press CTRL',
                r'\[Wingman\]', r'Attaching', r'Monitor',
                r'Commands:', r'Attach:', r'Monitor:', r'Kill:',
                r'Session started'
            ]

            for line in output.split('\n'):
                # 跳过UI输出
                if any(re.search(pattern, line) for pattern in skip_patterns):
                    continue
                # 跳过空行和纯符号行
                if not line.strip() or len(line.strip()) < 5:
                    continue
                review_lines.append(line)

            logger.info(f"After filtering: {len(review_lines)} lines, {len(output.split(chr(10)))} total")

            # 提取最后30行有意义的内容
            review_text = '\n'.join(review_lines[-30:])
            logger.info(f"Final review text length: {len(review_text)} chars, preview: {review_text[:200]}")

            if review_text.strip():
                return review_text
            else:
                return "审查完成，但未能提取详细内容。"
        else:
            logger.error(f"Claude Code failed: {process.stderr}")
            return f"Claude Code执行失败: {process.stderr}"

    except subprocess.TimeoutExpired:
        logger.error("Claude Code review timeout")
        return "审查超时，代码变更较大。"
    except Exception as e:
        logger.error(f"Claude Code review error: {e}")
        return f"审查失败: {str(e)}"

async def code_review(diff: str, mr_title: str, user: str, project: str) -> tuple[str, str]:
    """
    使用Claude Code进行代码审查

    参数:
        diff: 代码diff
        mr_title: MR标题
        user: 用户名
        project: 项目名

    返回:
        (飞书消息格式, GitLab评论格式)
    """
    if not diff:
        feishu_msg = f"⚠️ **代码审查失败**\n\n无法获取代码diff，跳过审查。"
        gitlab_comment = "⚠️ 代码审查失败\n\n无法获取代码diff，跳过审查。"
        return feishu_msg, gitlab_comment

    try:
        # 构造审查提示词
        review_prompt = f"""请对以下代码进行质量审查，重点关注：

**审查维度：**
1. 代码质量（命名、结构、可读性）
2. 潜在bug和逻辑问题
3. 性能优化建议
4. 安全问题
5. 最佳实践

**MR信息：**
- 项目：{project}
- 用户：{user}
- 标题：{mr_title}

**代码diff：**
```diff
{diff}
```

请以结构化的方式输出审查结果，包括：
- 总体评价（1句话）
- 发现的问题（列表形式，每个问题说明原因和改进建议）
- 优点（可选）

保持简洁专业，不超过300字。"""

        # 使用Claude Code进行代码审查
        review_result = run_claude_code_review(review_prompt)

        # 简化审查流程
        if review_result and "Claude Code" not in review_result and "超时" not in review_result and "失败" not in review_result:
            feishu_msg = f"🔍 **代码审查报告**\n\n📦 项目：{project}\n👤 提交者：{user}\n📋 MR：{mr_title}\n\n---\n\n{review_result}\n\n💡 *本评论由AI代码审查助手自动生成*"
            gitlab_comment = f"## 🔍 AI代码审查\n\n**项目**: {project}  \n**提交者**: {user}  \n**MR**: {mr_title}\n\n---\n\n{review_result}\n\n---\n\n*本评论由AI代码审查助手自动生成，如有问题请联系管理员*"
        else:
            # 审查失败的情况
            feishu_msg = f"📋 **代码审查通知**\n\n📦 项目：{project}\n👤 提交者：{user}\n📋 MR：{mr_title}\n\n💡 AI审查暂时不可用，请手动进行代码审查。"
            gitlab_comment = f"## 📋 代码审查通知\n\nAI审查服务暂时不可用，请手动进行代码审查。"

        return feishu_msg, gitlab_comment

    except Exception as e:
        logger.error(f"Code review error: {e}")
        feishu_msg = f"⚠️ **代码审查失败**\n\n审查过程中出现错误：{str(e)}"
        gitlab_comment = f"## ⚠️ 代码审查失败\n\n审查过程中出现错误：{str(e)}"
        return feishu_msg, gitlab_comment

async def handle_push_event(data: dict):
    """处理Push事件"""
    project = data.get('project', {}).get('name', 'Unknown')
    ref = data.get('ref', '')
    user = data.get('user_name', 'Unknown')
    commits = data.get('total_commits_count', 0)

    logger.info(f"Push event: {user} pushed {commits} commits to {ref} in {project}")

async def handle_merge_request_event(data: dict):
    """处理Merge Request事件"""
    mr = data.get('object_attributes', {})
    action = mr.get('action', 'Unknown')
    title = mr.get('title', 'Unknown')
    user = data.get('user', {}).get('name', 'Unknown')
    project = data.get('project', {})
    project_id = project.get('id')
    project_name = project.get('name', 'Unknown')
    mr_iid = mr.get('iid')

    logger.info(f"MR event: {user} {action} MR: {title}")

    # 只对新的MR（open action）进行代码审查
    if action == 'open' and mr_iid:
        logger.info(f"Starting code review for MR {mr_iid}")
        try:
            # 获取代码diff
            diff = get_gitlab_diff(project_id, mr_iid)

            if diff:
                # 进行代码审查
                feishu_msg, gitlab_comment = await code_review(diff, title, user, project_name)

                # 发送审查结果到飞书
                send_raw_feishu_message(feishu_msg)
                logger.info(f"Code review sent to Feishu for MR {mr_iid}")

                # 自动回复到GitLab MR评论区
                success = post_gitlab_mr_comment(project_id, mr_iid, gitlab_comment)
                if success:
                    logger.info(f"Code review posted to GitLab MR {mr_iid}")
                else:
                    logger.error(f"Failed to post review to GitLab MR {mr_iid}")
            else:
                logger.warning(f"Failed to get diff for MR {mr_iid}")

        except Exception as e:
            logger.error(f"Error during code review: {e}")

async def handle_tag_push_event(data: dict):
    """处理Tag Push事件"""
    project = data.get('project', {}).get('name', 'Unknown')
    ref = data.get('ref', '')
    user = data.get('user_name', 'Unknown')

    logger.info(f"Tag push event: {user} pushed tag {ref} in {project}")

async def handle_pipeline_event(data: dict):
    """处理Pipeline事件"""
    pipeline = data.get('object_attributes', {})
    status = pipeline.get('status', 'Unknown')
    source = pipeline.get('source', 'Unknown')

    logger.info(f"Pipeline event: Pipeline {status} from {source}")

def send_raw_feishu_message(message: str):
    """直接发送飞书消息（用于代码审查结果）"""
    try:
        # 设置完整的环境变量
        env = os.environ.copy()
        env['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:' + env.get('PATH', '')
        env['NVM_DIR'] = '/root/.nvm'

        # 使用绝对路径调用OpenClaw
        openclaw_path = '/root/.nvm/versions/node/v22.22.0/bin/openclaw'
        result = subprocess.run(
            [openclaw_path, 'message', 'send',
             '--channel', 'feishu',
             '--target', f'user:{FEISHU_TARGET_USER}',
             '--message', message],
            capture_output=True,
            text=True,
            timeout=15,
            env=env
        )
        if result.returncode == 0:
            logger.info(f"Raw Feishu message sent successfully")
        else:
            logger.error(f"Raw Feishu message failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        logger.error("Raw Feishu message timeout")
    except Exception as e:
        logger.error(f"Failed to send raw Feishu message: {str(e)}")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("GitLab Webhook Server v2.0.0 starting...")
    logger.info("Features:")
    logger.info("  - 接收GitLab webhook事件")
    logger.info("  - 自动获取MR diff")
    logger.info("  - AI代码审查")
    logger.info("  - 飞书通知")
    logger.info("  - 自动回复到GitLab MR评论区")
    logger.info("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_level="info"
    )
