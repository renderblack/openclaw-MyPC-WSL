import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Administrator\.openclaw\workspace\MEMORY.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 100-114 contain the Quark section (index 99-113)
# Replace with updated content

new_section = """6. **夸克网盘上传功能** (2026-04-07 暂缓)
   - **目标**: 将 G:\\动画组共享\\... 视频上传到夸克网盘
   - **文件**: 中铁24局沪昆铁路抬升改建项目介绍(带水印)20231201.mp4 (0.71 GB)
   - **状态**: 暂缓 (2026-04-07 14:42)
   - **已测试方案**:
     - quarkpan Python 库: OSS bucket ul-zb 返回 502 Bad Gateway
     - 夸克PC客户端本地API: 端口9128有响应但API路径全返回404
     - Selenium + Chrome (新profile): Chrome启动成功但无法定位上传按钮
   - **卡住原因**: 夸克网盘网页版上传按钮选择器未知，Selenium无法定位
   - **下次尝试**: JavaScript注入方式触发文件选择，或手动确认上传按钮位置
   - **依赖**: 需要用户在Chrome中登录夸克网盘
"""

# Replace lines 100-114 (index 99-113)
new_lines = lines[:99] + [new_section + '\n'] + lines[114:]

with open(r'C:\Users\Administrator\.openclaw\workspace\MEMORY.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated successfully')
