#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
磁盘分析工具 - 简单实现
分析 C 盘空间使用情况
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def analyze_directory(path, max_depth=2):
    """分析目录大小"""
    path = Path(path)
    if not path.exists():
        return None
    
    total_size = 0
    file_count = 0
    dir_count = 0
    
    try:
        for item in path.iterdir():
            try:
                if item.is_file():
                    total_size += item.stat().st_size
                    file_count += 1
                elif item.is_dir() and max_depth > 0:
                    dir_size, f_count, d_count = analyze_directory(item, max_depth - 1)
                    total_size += dir_size
                    file_count += f_count
                    dir_count += d_count
            except (PermissionError, OSError):
                continue
    except (PermissionError, OSError):
        pass
    
    return total_size, file_count, dir_count

def get_drive_info(drive_letter='C'):
    """获取驱动器信息"""
    drive = Path(f"{drive_letter}:\\")
    
    # 使用 os 模块获取磁盘空间
    total, used, free = shutil.disk_usage(drive)
    
    return {
        'drive': f"{drive_letter}:",
        'total': format_size(total),
        'used': format_size(used),
        'free': format_size(free),
        'usage_percent': (used / total) * 100
    }

def main():
    """主函数"""
    print("=" * 60)
    print("[DISK ANALYSIS REPORT]")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 分析 C 盘
    print("\n[C Drive Overview]")
    try:
        total, used, free = shutil.disk_usage('C:\\')
        print(f"  总容量: {format_size(total)}")
        print(f"  已使用: {format_size(used)} ({(used/total)*100:.1f}%)")
        print(f"  可用空间: {format_size(free)}")
    except Exception as e:
        print(f"  错误: {e}")
    
    # 分析 C 盘根目录主要文件夹
    print("\n[C Drive Root Directories]")
    c_root = Path('C:\\')
    top_dirs = []
    
    try:
        for item in c_root.iterdir():
            if item.is_dir():
                try:
                    size, f_count, d_count = analyze_directory(item, max_depth=1)
                    if size:
                        top_dirs.append((item.name, size, f_count, d_count))
                except (PermissionError, OSError):
                    continue
    except (PermissionError, OSError):
        pass
    
    # 按大小排序
    top_dirs.sort(key=lambda x: x[1], reverse=True)
    
    for name, size, f_count, d_count in top_dirs[:10]:
        print(f"  {name:30s} {format_size(size):>12}  (文件:{f_count}, 目录:{d_count})")
    
    print("\n" + "=" * 60)
    print("Analysis complete")

if __name__ == "__main__":
    import shutil
    main()
