import json

# 读取 gdu 输出的 JSON 文件
with open("C:\\temp\\gdu_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"

# gdu JSON 结构：[1, 2, metadata, [root_info, subitem1, subitem2, ...]]
metadata = data[2]
items_list = data[3]

# 第一个元素是根目录信息，后面是子项
root_info = items_list[0]
sub_items = items_list[1:]

print("=" * 60)
print("C:\\Users 磁盘分析报告 (gdu)")
print("=" * 60)
print(f"分析工具：{metadata.get('progname', 'N/A')} {metadata.get('progver', 'N/A')}")
print(f"扫描目录：{root_info.get('name', 'N/A')}")
print()

# 递归函数来找出最大的目录
def find_largest_items(items, max_items=10, current_path=""):
    """找出最大的项目"""
    result = []
    for item in items:
        if isinstance(item, dict):
            name = item.get("name", "Unknown")
            size = item.get("dsize", item.get("asize", 0))
            path = f"{current_path}\\{name}" if current_path else name
            result.append({
                "path": path,
                "size": size,
                "items": item.get("items", [])
            })
    
    # 递归处理子目录
    for item in result:
        if item["items"]:
            sub_items = find_largest_items(item["items"], 1, item["path"])
            if sub_items:
                item["top_subitem"] = sub_items[0]
    
    return sorted(result, key=lambda x: x["size"], reverse=True)[:max_items]

# 获取子项
largest = find_largest_items(sub_items, 10)

print("【Top 10 最大占用目录】")
for i, item in enumerate(largest, 1):
    size_str = format_size(item["size"])
    print(f"{i}. {item['path']} ({size_str})")
    if "top_subitem" in item:
        sub = item["top_subitem"]
        sub_size = format_size(sub["size"])
        sub_name = sub["path"].split("\\")[-1]
        print(f"   └─ 最大子项：{sub_name} ({sub_size})")
    print()

print("=" * 60)
print("完整 JSON 数据保存在：C:\\temp\\gdu_output.json")
print("文件大小：48.7 MB")
print("=" * 60)
