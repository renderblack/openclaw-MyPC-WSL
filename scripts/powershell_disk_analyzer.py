import json
import os
from pathlib import Path

def get_disk_usage(path, max_depth=2, current_depth=0):
    """递归获取目录大小"""
    if current_depth > max_depth:
        return {"path": str(path), "size": 0, "type": "truncated"}
    
    try:
        total_size = 0
        items = []
        
        for item in Path(path).iterdir():
            try:
                if item.is_dir():
                    # 递归计算子目录
                    subdir_size = get_disk_usage(item, max_depth, current_depth + 1)
                    items.append(subdir_size)
                    total_size += subdir_size.get("size", 0)
                else:
                    # 文件
                    size = item.stat().st_size
                    total_size += size
                    items.append({
                        "path": str(item),
                        "size": size,
                        "type": "file"
                    })
            except (PermissionError, OSError):
                continue
        
        return {
            "path": str(path),
            "size": total_size,
            "type": "directory",
            "items": sorted(items, key=lambda x: x.get("size", 0), reverse=True)[:20]  # 只保留前 20 个
        }
    except (PermissionError, OSError) as e:
        return {"path": str(path), "size": 0, "type": "error", "error": str(e)}

# 分析 C:\Users 目录（排除系统目录）
print("正在分析 C:\\Users 目录...")
result = get_disk_usage("C:\\Users", max_depth=3)

# 保存为 JSON 文件
output_path = "C:\\Users\\Administrator\\Desktop\\disk_analysis.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"分析完成！结果已保存到: {output_path}")
print(f"总大小: {result['size'] / (1024**3):.2f} GB")
