import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 90-93 with expanded subtasks
# Line 90 (index 89): "6. **OpenClaw Cron QQ推送配置** (待执行?)"
# Lines 90-93 contain the QQ cron task

new_section = """6. **OpenClaw Cron QQ推送配置** (待执行)
   - **目标**: 定时推送内容到 QQ
   - **配置命令**: `openclaw cron add --announce --channel qqbot --to "qqbot:c2c:OPENID"`
   - **待确认事项**:
     1. 推送内容：每天早上的天气预报？下午的上下文消耗提醒？还是固定内容？
     2. 推送时间：早上 8-9 点？下午 14-15 点？
     3. 推送频率：每小时一次？每天几次？
   - **执行步骤**:
     1. 确认推送内容和时间
     2. 使用 `openclaw cron add` 创建 cron job
     3. 测试推送是否正常
   - **状态**: 待用户确认推送内容后执行
"""

new_lines = lines[:89] + [new_section + '\n'] + lines[93:]

with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated OpenClaw Cron QQ section with subtasks')
