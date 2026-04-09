#!/bin/bash
# monitor-3dgs.sh - 监控3DGS最新文章
# 定期检查关键词，检测新文章并记录

SEARCH_KEYWORDS="3D gaussian splatting OR 3DGS OR 高斯泼溅"
STATE_FILE="/home/xiong/.openclaw/workspace/learn/3d-reconstruction/.last_check"
OUTPUT_FILE="/home/xiong/.openclaw/workspace/learn/3d-reconstruction/articles-tracker.md"

echo "🔍 检查 3DGS 最新文章..."
echo "上次检查时间: $(cat $STATE_FILE 2>/dev/null || echo '首次运行')"
date > $STATE_FILE

# 记录本次检查
echo "" >> $OUTPUT_FILE
echo "## 检查记录 $(date '+%Y-%m-%d %H:%M')" >> $OUTPUT_FILE
echo "---" >> $OUTPUT_FILE
