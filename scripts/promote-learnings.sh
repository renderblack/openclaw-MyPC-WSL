#!/bin/bash
# promote-learnings.sh - 自动将 .learnings/ 中的重要内容晋升到 MEMORY.md, AGENTS.md, TOOLS.md
# 使用方式：bash scripts/promote-learnings.sh

WORKSPACE="$HOME/.openclaw/workspace"
LEARNINGS_DIR="$WORKSPACE/.learnings"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
AGENTS_FILE="$WORKSPACE/AGENTS.md"
TOOLS_FILE="$WORKSPACE/TOOLS.md"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧠 开始学习晋升检查...${NC}"

# 检查目录是否存在
if [ ! -d "$LEARNINGS_DIR" ]; then
    echo -e "${RED}❌ .learnings/ 目录不存在${NC}"
    exit 1
fi

# 初始化计数器
error_count=0
learning_count=0
feature_count=0
promoted_count=0

# 1. 检查 ERRORS.md
if [ -f "$LEARNINGS_DIR/ERRORS.md" ]; then
    echo -e "${YELLOW}📋 检查 ERRORS.md...${NC}"
    # 查找最近 7 天的错误（简单 grep，可根据需要调整）
    recent_errors=$(grep -A 5 "\*\*[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\*\*" "$LEARNINGS_DIR/ERRORS.md" | grep -c "Fix:" || true)
    if [ "$recent_errors" -gt 0 ]; then
        echo -e "  发现 $recent_errors 个近期错误记录"
        error_count=$recent_errors
    fi
fi

# 2. 检查 LEARNINGS.md
if [ -f "$LEARNINGS_DIR/LEARNINGS.md" ]; then
    echo -e "${YELLOW}📋 检查 LEARNINGS.md...${NC}"
    # 查找 best_practice 和 insight
    best_practices=$(grep -c "best_practice" "$LEARNINGS_DIR/LEARNINGS.md" || true)
    insights=$(grep -c "insight" "$LEARNINGS_DIR/LEARNINGS.md" || true)
    if [ "$best_practices" -gt 0 ]; then
        echo -e "  发现 $best_practices 条 best_practice"
    fi
    if [ "$insights" -gt 0 ]; then
        echo -e "  发现 $insights 条 insight"
    fi
    learning_count=$((best_practices + insights))
fi

# 3. 检查 FEATURE_REQUESTS.md
if [ -f "$LEARNINGS_DIR/FEATURE_REQUESTS.md" ]; then
    echo -e "${YELLOW}📋 检查 FEATURE_REQUESTS.md...${NC}"
    pending_features=$(grep -c "Status: Pending" "$LEARNINGS_DIR/FEATURE_REQUESTS.md" || true)
    if [ "$pending_features" -gt 0 ]; then
        echo -e "  发现 $pending_features 个待处理需求"
    fi
    feature_count=$pending_features
fi

# 4. 晋升逻辑（简化版：手动确认）
echo ""
echo -e "${GREEN}📊 总结:${NC}"
echo "  - 近期错误：$error_count"
echo "  - 学习记录：$learning_count"
echo "  - 待办需求：$feature_count"
echo ""

if [ $((error_count + learning_count + feature_count)) -eq 0 ]; then
    echo -e "${GREEN}✅ 没有需要晋升的内容${NC}"
    exit 0
fi

echo -e "${YELLOW}⚠️  发现待晋升内容，请手动检查以下文件:${NC}"
echo "  - $LEARNINGS_DIR/ERRORS.md"
echo "  - $LEARNINGS_DIR/LEARNINGS.md"
echo "  - $LEARNINGS_DIR/FEATURE_REQUESTS.md"
echo ""
echo -e "${GREEN}💡 建议:${NC}"
echo "  1. 打开上述文件，确认哪些内容需要晋升"
echo "  2. 将通用性强的内容复制到 $MEMORY_FILE"
echo "  3. 将工作流优化复制到 $AGENTS_FILE"
echo "  4. 将工具技巧复制到 $TOOLS_FILE"
echo ""
echo -e "${GREEN}🎉 检查完成${NC}"
