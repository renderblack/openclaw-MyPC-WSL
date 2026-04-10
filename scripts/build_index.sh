#!/bin/bash
# OpenClaw Docs - 索引构建脚本
# 用法: ./scripts/build_index.sh

set -e

DOCS_DIR="$(cd "$(dirname "$0")/.." && pwd)/latest"
OUTPUT="$DOCS_DIR/INDEX.md"

echo "构建文档索引..."

# 统计
TOTAL_FILES=$(find "$DOCS_DIR/docs" -name "*.md" | wc -l)
TOTAL_SIZE=$(du -sh "$DOCS_DIR" | cut -f1)

# 生成索引
cat > "$OUTPUT" << 'HEADER'
# OpenClaw 官方文档 · 知识库索引

> 版本：2026.4.11 | 维护者：卡拉米 | 抓取来源：openclawx.cloud

---

## 📂 文档树
HEADER

# 动态生成文档树
echo '```' >> "$OUTPUT"
find "$DOCS_DIR/docs" -type f -name "*.md" | sort | sed "s|$DOCS_DIR/docs/||" | sed 's|/| / |g' >> "$OUTPUT"
echo '```' >> "$OUTPUT"

# 添加统计信息
cat >> "$OUTPUT" << STATS

---

## 📊 统计信息

| 指标 | 值 |
|------|---|
| 文档总数 | $TOTAL_FILES |
| 总大小 | $TOTAL_SIZE |
| 覆盖类别 | Architecture, Automation, Best Practices, Channels, CLI, Concepts, Configuration, Deployment, Guides, Reference, Skills, Troubleshooting |

---

*最后更新：$(date '+%Y-%m-%d %H:%M %Z')*
STATS

echo "索引构建完成：$OUTPUT"
echo "文档数：$TOTAL_FILES"
