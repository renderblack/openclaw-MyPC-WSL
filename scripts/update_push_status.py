import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'r', encoding='utf-8') as f:
    content = f.read()

old = '6. **定时推送功能配置** (待执行)'

new = '''6. **定时推送功能配置** (开发中)
   - **目标**: 每4小时推送消息到 Telegram
   - **脚本**: `combined_status.py`
   - **内容**: 系统状态、天气(嘉兴)、工程安全新闻
   - **发送**: Telegram (1022202630)
   - **问题**: 新闻抓取失败、Cron配置受限
   - **状态**: 手动触发成功，待配置定时任务'''

if old in content:
    content = content.replace(old, new, 1)
    with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated')
else:
    print('Section not found')
