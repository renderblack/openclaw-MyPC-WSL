#!/bin/bash
# 本地配置备份脚本
# 备份到 D:\openclaw-backup\，即使 OpenClaw 卸载也不会丢失

BACKUP_DIR="/mnt/d/openclaw-backup"
SOURCE_CONFIG="$HOME/.openclaw/openclaw.json"

mkdir -p "$BACKUP_DIR"

DATE=$(date +%Y%m%d)
cp "$SOURCE_CONFIG" "$BACKUP_DIR/openclaw.json.$DATE"

# 只保留最近5个备份
cd "$BACKUP_DIR" && ls -t openclaw.json.* | tail -n +6 | xargs -r rm

echo "✅ 配置已备份到 $BACKUP_DIR"
