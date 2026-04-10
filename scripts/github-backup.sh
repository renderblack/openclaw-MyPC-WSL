#!/bin/bash
# GitHub 自动备份脚本
# 用途：定时将 memory 文件夹同步到 GitHub

WORKSPACE="/home/xiong/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

# 配置 Git 代理（WSL2 环境通过 Windows Clash 访问 GitHub）
git config --global http.proxy http://172.18.176.1:7890

# 检查是否有变更
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

# 添加所有变更
git add -A

# 获取当前日期
DATE=$(date "+%Y-%m-%d %H:%M")

# 自动提交
git commit -m "自动备份 $DATE" || exit 0

# 推送到 GitHub
git push 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 备份成功 $DATE"
else
    echo "❌ 备份失败"
fi
