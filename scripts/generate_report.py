import json

# 读取分析结果
with open("C:\\Users\\Administrator\\Desktop\\disk_analysis.json", "r", encoding="utf-8") as f:
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

def find_largest_items(items, max_items=10):
    """找出最大的项目"""
    sorted_items = sorted(items, key=lambda x: x.get("size", 0), reverse=True)
    return sorted_items[:max_items]

print("=" * 60)
print("C 盘磁盘分析报告")
print("=" * 60)
print(f"总占用：{format_size(data['size'])}")
print()

# 找出最大的子目录
print("【Top 10 最大占用目录】")
largest = find_largest_items(data.get("items", []))
for i, item in enumerate(largest, 1):
    size_str = format_size(item["size"])
    print(f"{i}. {item['path']} ({size_str})")
    if "items" in item and item["items"]:
        # 显示子目录中的最大项
        sub_largest = find_largest_items(item["items"], 3)
        for sub in sub_largest:
            sub_name = sub['path'].split('\\')[-1]
            print(f"   └─ {sub_name} ({format_size(sub['size'])})")
    print()

# 生成清理建议
print("=" * 60)
print("【清理建议】")
print("=" * 60)

# 检查常见可清理目录
cleanup_suggestions = []

# 检查 Package Cache
package_cache = next((item for item in data.get("items", []) if "Package Cache" in item["path"]), None)
if package_cache:
    cleanup_suggestions.append(f"- Package Cache: {format_size(package_cache['size'])} (可考虑清理旧版本)")

# 检查 Temp
temp_dir = next((item for item in data.get("items", []) if "Temp" in item["path"]), None)
if temp_dir:
    cleanup_suggestions.append(f"- Temp 目录：{format_size(temp_dir['size'])} (可安全清理)")

# 检查 Downloads
downloads_dir = next((item for item in data.get("items", []) if "Downloads" in item["path"]), None)
if downloads_dir:
    cleanup_suggestions.append(f"- Downloads: {format_size(downloads_dir['size'])} (检查旧下载文件)")

if cleanup_suggestions:
    for suggestion in cleanup_suggestions:
        print(suggestion)
else:
    print("未发现明显的可清理目录。")

print()
print("报告已保存到：C:\\Users\\Administrator\\Desktop\\disk_analysis.json")
print("你可以用文本编辑器打开查看完整数据。")
