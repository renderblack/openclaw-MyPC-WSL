import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 89-92 are the 腾讯系迁移 task (0-indexed: 88-91)
# We need to remove lines 89-92 and also fix line 92 which has "### ?? �����ȼ�"
# The task says:
# Line 89: - **��Ѷϵ�ļ�Ǩ�Ƶ� D: ??** (��ִ??
# Line 90: - **Ŀ��**: �ͷ� C �̿��?
# Line 91: - **�漰**: ��ҵ΢�š�΢�ŵ���Ѷϔ��̼?
# Line 92: - **״??*: ��ִ??### ?? �����ȼ�

# Remove lines 89-91 (index 88-90), keep line 92 if it's the section header
# Actually line 92 starts with "### ?? �����ȼ�" which is the next section marker
# So we should remove lines 89-91 and keep line 92

new_lines = lines[:88] + lines[92:]

with open(r'C:/Users/Administrator/.openclaw/workspace/MEMORY.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Removed 腾讯系文件迁移 task')
