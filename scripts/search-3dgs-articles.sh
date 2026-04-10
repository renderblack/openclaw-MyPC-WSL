#!/bin/bash
# search-3dgs-articles.sh - 搜索3DGS最新文章
# 每两天运行一次，通过微信发送结果给用户

DATE=$(date '+%Y-%m-%d')
TRACKER="/home/xiong/.openclaw/workspace/learn/3d-reconstruction/articles-tracker.md"
LOG="/tmp/3dgs-search-$(date '+%Y%m%d').log"

echo "[$(date)] 开始搜索3DGS最新文章..." > $LOG

# 搜索关键词
KEYWORDS="3D gaussian splatting OR 3DGS OR 高斯泼溅 OR NeRF"

# 这里只是记录搜索日志
# 实际推送由heartbeat时主动告知用户
echo "搜索关键词: $KEYWORDS" >> $LOG
echo "检查时间: $(date)" >> $LOG
echo "结果将主动推送到微信" >> $LOG

# 如果有结果，记录到tracker
if [ -f /tmp/3dgs-results.txt ]; then
    echo "" >> $TRACKER
    echo "## 自动搜索 $(date '+%Y-%m-%d')" >> $TRACKER
    cat /tmp/3dgs-results.txt >> $TRACKER
    rm /tmp/3dgs-results.txt
fi

echo "完成" >> $LOG
