import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the 定时推送配置 section and expand it
old_section = """6. **OpenClaw Cron QQ推送配置** (待执行)
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
   - **状态**: 待用户确认推送内容后执行"""

new_section = """6. **定时推送功能配置** (待执行)
   - **目标**: 每4小时推送4条消息到 QQ
   - **推送内容**（每种类型1条消息）:
     1. OpenClaw 状态（磁盘、内存、网关）
     2. 天气（当前城市天气）
     3. 系统健康检查（proactive_check.ps1）
     4. 行业新闻资讯（工程安全相关）
   - **配置命令**: `openclaw cron add --announce --channel qqbot --to "qqbot:c2c:OPENID"`
   - **搜索关键词**:
     - 必搜：桥梁事故、施工坍塌、工程安全死亡、大桥垮塌
     - 扩展：脚手架倒塌、塔吊事故、挂篮断裂、船撞桥
   - **执行步骤**:
     1. 创建 news_search.ps1 脚本（搜索引擎抓取）
     2. 测试新闻抓取是否正常
     3. 配置 OpenClaw Cron 每4小时执行
     4. 测试推送是否正常
   - **状态**: 第1步（创建新闻搜索脚本）

7. **TG群消息获取** (后面再弄)
   - **目标**: 将 Telegram 群作为信息获取渠道
   - **需要**: 教用户如何配置 TG Bot 监控群消息
   - **前提**: 用户需先加入相关工程/安全 TG 群
   - **状态**: 待用户确认后执行"""

content = content.replace(old_section, new_section)

with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated with news monitoring and TG task')
