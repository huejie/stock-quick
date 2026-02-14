# 📖 OpenClaw 常用指令手册

> 为小K的AI伙伴准备的OpenClaw操作指南
> 
> **版本**: OpenClaw 2026.1.29
> **更新时间**: 2026-02-04

---

## 📋 目录

1. [快速开始](#快速开始)
2. [常用命令速查](#常用命令速查)
3. [配置管理](#配置管理)
4. [定时任务管理](#定时任务管理)
5. [网关控制](#网关控制)
6. [消息发送](#消息发送)
7. [会话管理](#会话管理)
8. [智能体管理](#智能体管理)
9. [设备管理](#设备管理)
10. [节点控制](#节点控制)
11. [插件管理](#插件管理)
12. [故障排查](#故障排查)
13. [高级功能](#高级功能)

---

## 🚀 快速开始

### 查看版本和帮助
```bash
# 查看版本
openclaw --version

# 查看帮助
openclaw --help

# 查看特定命令帮助
openclaw cron --help
openclaw gateway --help
```

### 初始化和向导
```bash
# 首次初始化
openclaw setup

# 交互式向导（推荐新手）
openclaw onboard

# 配置向导
openclaw configure
```

### 健康检查
```bash
# 完整健康检查
openclaw doctor

# 查看网关状态
openclaw gateway status
```

---

## ⚡ 常用命令速查

### 🎯 最常用命令（Top 10）

| 命令 | 说明 | 示例 |
|------|------|------|
| `openclaw config` | 配置管理 | `openclaw config get` |
| `openclaw cron` | 定时任务 | `openclaw cron list` |
| `openclaw gateway` | 网关控制 | `openclaw gateway restart` |
| `openclaw message` | 发送消息 | `openclaw message send` |
| `openclaw agents` | 智能体管理 | `openclaw agents list` |
| `openclaw doctor` | 健康检查 | `openclaw doctor` |
| `openclaw models` | 模型配置 | `openclaw models list` |
| `openclaw sessions` | 会话管理 | `openclaw sessions list` |
| `openclaw logs` | 查看日志 | `openclaw logs -f` |
| `openclaw tui` | 终端界面 | `openclaw tui` |

---

## ⚙️ 配置管理

### 查看配置
```bash
# 获取完整配置
openclaw config get

# 获取配置路径
openclaw config path

# 查看配置schema
openclaw config schema
```

### 修改配置
```bash
# 交互式配置
openclaw config set

# 直接设置配置值
openclaw config set <key> <value>

# 示例：设置默认模型
openclaw config set agents.defaults.model.primary "zai/glm-4.7"

# 示例：设置工作空间
openclaw config set agents.defaults.workspace "/path/to/workspace"
```

### 补丁更新配置
```bash
# 使用JSON补丁更新（安全推荐）
openclaw config.patch '{"models": {"providers": {"zhipu": {"apiKey": "new-key"}}}'

# 示例：更新智谱API key
openclaw config.patch '{"models": {"providers": {"zhipu": {"apiKey": "your-api-key"}}}}'
```

### 应用完整配置
```bash
# 应用完整配置（覆盖）
openclaw config.apply '{"version": "2026.1.29", "meta": {...}}'

# 注意：config.apply会验证+写入+重启
# 推荐使用config.patch进行部分更新
```

### 删除配置
```bash
# 删除配置项
openclaw config unset <key>

# 示例：删除某个配置
openclaw config unset agents.defaults.model.primary
```

---

## ⏰ 定时任务管理

### 查看任务
```bash
# 列出所有任务
openclaw cron list

# 列出包含禁用的任务
openclaw cron list --include-disabled

# 查看任务执行历史
openclaw cron runs <job-id>
```

### 添加任务
```bash
# 添加cron任务（每日9点）
openclaw cron add --name "每日提醒" \
  --schedule '0 9 * * *' \
  --tz 'Asia/Shanghai' \
  --text "早上好！这是定时任务提醒"

# 添加间隔任务（每24小时）
openclaw cron add --name "日报" \
  --schedule 'every' \
  --interval '86400000' \
  --text "日报提醒"

# 添加一次性任务
openclaw cron add --name "提醒" \
  --schedule 'at' \
  --at '2026-02-05T09:00:00' \
  --text "明天9点的提醒"
```

### 编辑任务
```bash
# 编辑任务文本
openclaw cron edit <job-id> --text "更新后的消息内容"

# 编辑任务时间
openclaw cron edit <job-id> --schedule '0 10 * * *'

# 修改投递设置
openclaw cron edit <job-id> --deliver --channel telegram --to "123456789"

# 禁用投递
openclaw cron edit <job-id> --no-deliver

# 禁用任务
openclaw cron edit <job-id> --disable

# 启用任务
openclaw cron edit <job-id> --enable
```

### 运行任务
```bash
# 立即运行任务
openclaw cron run <job-id>

# 强制运行（忽略时间）
openclaw cron run <job-id> --force
```

### 删除任务
```bash
# 删除任务
openclaw cron remove <job-id>

# 批量删除（使用jq或其他工具）
openclaw cron list | jq -r '.[].id' | xargs -I {} openclaw cron remove {}
```

### Wake功能
```bash
# 发送wake事件（立即触发）
openclaw cron wake "这是wake消息"

# 延迟触发（下一个心跳）
openclaw cron wake --mode next-heartbeat "延迟消息"
```

### 系统状态
```bash
# 查看cron状态
openclaw cron status

# 查看下次唤醒时间
openclaw cron status --next
```

---

## 🌐 网关控制

### 启动和停止
```bash
# 启动网关
openclaw gateway start

# 停止网关
openclaw gateway stop

# 重启网关
openclaw gateway restart

# 检查状态
openclaw gateway status
```

### 配置操作
```bash
# 应用配置（重启）
openclaw gateway restart --reason "更新配置"

# 配置补丁（自动重启）
openclaw gateway config.patch '{"key": "value"}'

# 应用配置（验证+写入+重启）
openclaw gateway config.apply '{"..."}'
```

### 日志管理
```bash
# 查看网关日志
openclaw logs

# 实时跟踪日志
openclaw logs -f

# 查看最近100行
openclaw logs --tail 100

# 查看错误日志
openclaw logs --error
```

### 查看进程
```bash
# 查看网关进程
openclaw gateway ps

# 查看网关详细信息
openclaw gateway ps --details
```

---

## 💬 消息发送

### 发送消息
```bash
# 发送文本消息
openclaw message send --to <target> --message "你好！"

# 发送到指定频道
openclaw message send --channel telegram --to "123456789" --message "测试消息"

# 发送到当前会话
openclaw message send --to <session-key> --message "会话消息"
```

### 批量发送
```bash
# 批量发送到多个目标
openclaw message broadcast --channel telegram \
  --targets "target1,target2,target3" \
  --message "群发消息"
```

### 添加媒体
```bash
# 发送图片
openclaw message send --to <target> \
  --media /path/to/image.jpg \
  --message "附带图片的消息"

# 发送文件
openclaw message send --to <target> \
  --path /path/to/file.pdf \
  --message "附带文件的消息"
```

### 消息选项
```bash
# 静默发送
openclaw message send --to <target> \
  --silent \
  --message "静默消息"

# 添加表情
openclaw message send --to <target> \
  --emoji "😊" \
  --message "带表情的消息"

# 回复指定消息
openclaw message send --to <target> \
  --reply-to <message-id> \
  --message "回复消息"
```

---

## 🎭 会话管理

### 查看会话
```bash
# 列出所有会话
openclaw sessions list

# 列出活跃会话
openclaw sessions list --active

# 列出特定类型的会话
openclaw sessions list --kinds main,isolated

# 查看会话历史
openclaw sessions history <session-key>

# 带工具调用的历史
openclaw sessions history <session-key> --include-tools

# 限制返回条数
openclaw sessions history <session-key> --limit 20
```

### 发送消息到会话
```bash
# 发送到指定会话
openclaw sessions send --session-key <key> --message "消息内容"

# 发送到指定标签的会话
openclaw sessions send --label <label> --message "消息内容"

# 发送到特定智能体的会话
openclaw sessions send --agent-id <agent-id> --message "消息内容"
```

### 会话管理
```bash
# 创建新会话
openclaw sessions create --agent-id <agent-id>

# 终止会话
openclaw sessions terminate <session-key>

# 清理过期会话
openclaw sessions cleanup --older-than 7d
```

---

## 🤖 智能体管理

### 列出智能体
```bash
# 列出所有智能体
openclaw agents list

# 列出活跃的智能体
openclaw agents list --active

# 查看智能体详情
openclaw agents show <agent-id>
```

### 管理智能体
```bash
# 添加智能体
openclaw agents add --agent-id <id> --config <config-file>

# 更新智能体配置
openclaw agents update <agent-id> --config <config-file>

# 删除智能体
openclaw agents remove <agent-id>
```

### 认证管理
```bash
# 列出认证配置
openclaw agents auth list

# 添加认证配置
openclaw agents auth add --provider <provider> --key <api-key>

# 删除认证配置
openclaw agents auth remove <provider>
```

---

## 📱 设备管理

### 配对设备
```bash
# 查看待配对设备
openclaw nodes status

# 列出设备
openclaw nodes list

# 查看设备详情
openclaw nodes describe <node-id>
```

### 设备操作
```bash
# 相机拍照
openclaw nodes camera-snap --node <node-id>

# 查看设备列表
openclaw nodes camera-list

# 屏幕录制
openclaw nodes screen-record --node <node-id> --duration 30

# 获取位置
openclaw nodes location-get --node <node-id>

# 发送通知
openclaw nodes notify --node <node-id> --title "提醒" --body "内容"
```

### 管理配对
```bash
# 查看待处理配对
openclaw nodes pending

# 批准配对
openclaw nodes approve <node-id>

# 拒绝配对
openclaw nodes reject <node-id>
```

---

## 🔌 插件管理

### 查看插件
```bash
# 列出已安装插件
openclaw plugins list

# 查看插件状态
openclaw plugins status
```

### 管理插件
```bash
# 安装插件
openclaw plugins install <plugin-name>

# 卸载插件
openclaw plugins uninstall <plugin-name>

# 更新插件
openclaw plugins update <plugin-name>

# 重新加载插件
openclaw plugins reload
```

---

## 🧠 内存管理

### 搜索内存
```bash
# 搜索内存
openclaw memory search "股票项目进展"

# 限制返回结果数
openclaw memory search "股票" --max-results 5

# 设置最低分数
openclaw memory search "股票" --min-score 0.8
```

### 读取内存
```bash
# 读取指定文件
openclaw memory get /root/.openclaw/workspace/MEMORY.md

# 读取指定行
openclaw memory get /path/to/file --from 10 --lines 20
```

---

## 🔧 故障排查

### 健康检查
```bash
# 完整诊断
openclaw doctor

# 诊断特定问题
openclaw doctor --non-interactive

# 修复问题
openclaw doctor --fix
```

### 日志调试
```bash
# 查看详细日志
openclaw logs --verbose

# 查看错误日志
openclaw logs --error

# 导出日志到文件
openclaw logs > /tmp/openclaw.log
```

### 重置配置
```bash
# 重置配置
openclaw reset

# 保留CLI，只重置网关和本地数据
openclaw reset --keep-cli

# 完全卸载
openclaw uninstall
```

---

## 🚀 高级功能

### 系统事件
```bash
# 发送系统事件
openclaw system event --text "系统事件内容"

# 发送心跳
openclaw system heartbeat

# 更新存在状态
openclaw system presence --status online
```

### 审批流程
```bash
# 列出审批
openclaw approvals list

# 批准审批
openclaw approvals approve <approval-id>

# 拒绝审批
openclaw approvals reject <approval-id>
```

### Dashboard
```bash
# 打开控制面板
openclaw dashboard

# 在浏览器中打开
openclaw dashboard --open
```

### TUI界面
```bash
# 启动终端界面
openclaw tui

# 使用特定profile
openclaw tui --profile custom
```

---

## 📊 性能和监控

### 查看状态
```bash
# 查看当前状态
openclaw status

# 查看网关统计
openclaw gateway status --stats

# 查看内存使用
openclaw gateway status --memory
```

### 模型配置
```bash
# 列出可用模型
openclaw models list

# 切换默认模型
openclaw models set-default <model-id>

# 测试模型
openclaw models test <model-id>
```

---

## 🔐 安全和权限

### 权限管理
```bash
# 查看权限
openclaw auth list

# 添加权限
openclaw auth add <permission>

# 删除权限
openclaw auth remove <permission>
```

### Token管理
```bash
# 生成新token
openclaw tokens create

# 列出token
openclaw tokens list

# 删除token
openclaw tokens remove <token-id>
```

---

## 📝 实用技巧

### 1. 创建快捷别名
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
alias oc='openclaw'
alias oc-status='openclaw status'
alias oc-logs='openclaw logs -f'
alias oc-cron='openclaw cron list'
alias oc-config='openclaw config get'
```

### 2. 定时任务常用模板
```bash
# 每日提醒（9点）
openclaw cron add --name "晨间提醒" \
  --schedule '0 9 * * *' \
  --tz 'Asia/Shanghai' \
  --text "早上好！新的一天开始了"

# 工作日提醒（周一到周五9点）
openclaw cron add --name "工作提醒" \
  --schedule '0 9 * * 1-5' \
  --tz 'Asia/Shanghai' \
  --text "该开始工作了！"

# 每小时检查
openclaw cron add --name "每小时检查" \
  --schedule '0 * * * *' \
  --text "每小时检查提醒"
```

### 3. 配置备份和恢复
```bash
# 备份配置
openclaw config get > /tmp/openclaw-backup.json

# 恢复配置
openclaw config.apply < /tmp/openclaw-backup.json

# 验证配置
openclaw config.validate
```

### 4. 批量操作
```bash
# 批量删除所有disabled的任务
openclaw cron list --include-disabled | \
  jq -r '.[] | select(.enabled == false) | .id' | \
  xargs -I {} openclaw cron remove {}

# 批量发送消息到多个会话
openclaw sessions list | \
  jq -r '.[].key' | \
  xargs -I {} openclaw sessions send --session-key {} --message "广播消息"
```

---

## 🎯 小K的推荐配置

### 1. 日常使用必备
```bash
# 每日检查状态
openclaw status

# 查看定时任务
openclaw cron list

# 实时查看日志
openclaw logs -f
```

### 2. OPC一人公司推荐
```bash
# 创建定时任务提醒
openclaw cron add --name "每日复盘" \
  --schedule '0 21 * * *' \
  --text "今天工作总结和明天计划"

# 创建市场开盘提醒
openclaw cron add --name "开盘提醒" \
  --schedule '0 9 * * 1-5' \
  --text "A股开盘了！注意盯盘"
```

### 3. 开发调试常用
```bash
# 重启网关应用配置
openclaw gateway restart

# 查看详细日志
openclaw logs --verbose --tail 50

# 测试配置
openclaw doctor
```

---

## 📚 文档和资源

### 官方文档
```bash
# 查看命令文档
openclaw docs <command>

# 示例：查看cron文档
openclaw docs cron

# 示例：查看config文档
openclaw docs config
```

### 在线资源
- 官方文档: https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
- Discord社区: https://discord.com/invite/clawd
- ClawdHub: https://clawdhub.com

---

## 🐱 小K的提示

### 1. 常见问题
**Q: 定时任务没有执行？**
- 检查时区设置
- 查看任务执行历史
- 确认网关状态

**Q: 配置修改不生效？**
- 使用 `openclaw gateway restart` 重启
- 检查配置JSON格式是否正确
- 查看日志确认配置加载

**Q: 消息发送失败？**
- 检查通道配置
- 确认target格式正确
- 查看错误日志

### 2. 最佳实践
- ✅ 定期备份配置
- ✅ 使用配置补丁而非完全替换
- ✅ 查看日志调试问题
- ✅ 使用doctor进行健康检查
- ✅ 定期清理过期会话

### 3. 性能优化
- 使用 `--limit` 和 `--max-results` 控制返回数据量
- 避免频繁的配置读取
- 合理设置定时任务间隔
- 及时清理过期数据和日志

---

**最后更新**: 2026-02-04  
**文档版本**: v1.0  
**维护者**: 小K 🐱💻

**喵~ 希望这份文档对你有帮助！** 🐾
