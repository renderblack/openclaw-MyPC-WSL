#!/bin/bash
# OpenClaw Docs 自动备份脚本
# 定时推送到 GitHub

set -e

DOCS_DIR="/home/xiong/openclaw-docs"
BRANCH="main"

# 从环境变量获取Token（更安全）
GIT_TOKEN="${GITHUB_TOKEN:-}"

if [ -z "$GIT_TOKEN" ]; then
    echo "[$(date)] 错误：未设置 GITHUB_TOKEN 环境变量"
    exit 1
fi

GIT_REPO="https://github.com/renderblack/openclaw-MyPC-WSL.git"

cd "$DOCS_DIR"

# 检查是否有变更
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
    echo "[$(date)] 没有变更，跳过推送"
    exit 0
fi

# 添加所有文件
git add -A

# 提交
git commit -m "docs: 自动备份 $(date '+%Y-%m-%d %H:%M')"

# 推送
git push "https://${GIT_TOKEN}@github.com/renderblack/openclaw-MyPC-WSL.git" master:main --quiet

echo "[$(date)] 备份完成"
