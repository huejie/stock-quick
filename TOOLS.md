# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Claude Code编程助手

**安装位置：**
- Claude Code: `/root/.nvm/versions/node/v22.22.0/bin/claude` (版本: 2.1.29)
- Wingman脚本: `~/code/claude-code-wingman/`
- tmux: `/usr/bin/tux`

**使用方法：**
```bash
# 启动Claude Code会话
~/code/claude-code-wingman/claude-wingman.sh \
  --session <session-name> \
  --workdir <project-directory> \
  --prompt "<task description>"

# 监控会话
tmux capture-pane -t <session-name> -p -S -100

# 查看所有会话
tmux ls | grep claude-auto

# 杀死会话
tmux kill-session -t <session-name>
```

**注意：**
- 首次在某个目录运行时，需要手动attach并信任文件夹
- Wingman会自动处理权限提示
- 适合大型代码生成、重构等任务

---

Add whatever helps you do your job. This is your cheat sheet.
