#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
深度磁盘分析工具 - 按文件类型分类
分析 C:/Users 和 C:/Windows 等大目录
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def get_file_extension(path):
    """获取文件扩展名"""
    return path.suffix.lower() if path.suffix else "(无扩展名)"

def analyze_by_extension(path, max_depth=3, max_files=1000):
    """按文件扩展名分析目录"""
    ext_sizes = defaultdict(int)
    ext_counts = defaultdict(int)
    total_size = 0
    total_files = 0
    
    def scan(current_path, depth):
        nonlocal total_size, total_files
        if depth > max_depth or total_files >= max_files:
            return
        
        try:
            for item in current_path.iterdir():
                try:
                    if item.is_file():
                        try:
                            size = item.stat().st_size
                            ext = get_file_extension(item)
                            ext_sizes[ext] += size
                            ext_counts[ext] += 1
                            total_size += size
                            total_files += 1
                        except (PermissionError, OSError):
                            continue
                    elif item.is_dir() and depth < max_depth:
                        # 跳过系统目录
                        skip_dirs = {'Windows', 'Program Files', 'Program Files (x86)', 'Recovery', 'EFI', '$Recycle.Bin', 'System Volume Information'}
                        if item.name not in skip_dirs:
                            scan(item, depth + 1)
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            pass
    
    try:
        scan(path, 0)
    except (PermissionError, OSError) as e:
        print(f"  错误: {e}")
        return None
    
    return ext_sizes, ext_counts, total_size, total_files

def main():
    """主函数"""
    print("=" * 70)
    print("[DEEP DISK ANALYSIS REPORT]")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 分析 Users 目录
    users_path = Path('C:\\Users')
    print(f"\n[Analyzing: {users_path}]")
    result = analyze_by_extension(users_path, max_depth=4)
    
    if result:
        ext_sizes, ext_counts, total_size, total_files = result
        print(f"  Total Size: {format_size(total_size)}")
        print(f"  Total Files: {total_files}")
        print(f"\n  Top 15 File Types by Size:")
        print(f"  {'Extension':<20} {'Size':>15} {'Count':>10}")
        print(f"  {'-'*20} {'-'*15} {'-'*10}")
        
        sorted_exts = sorted(ext_sizes.items(), key=lambda x: x[1], reverse=True)[:15]
        for ext, size in sorted_exts:
            count = ext_counts[ext]
            print(f"  {ext:<20} {format_size(size):>15} {count:>10}")
    
    # 分析 Windows 目录（按子目录）
    print(f"\n[Analyzing: C:/Windows (Top Subdirectories)]")
    windows_path = Path('C:/Windows')
    dir_sizes = []
    
    try:
        for item in windows_path.iterdir():
            if item.is_dir():
                try:
                    # 简单统计一级子目录大小
                    total = 0
                    count = 0
                    for sub in item.iterdir():
                        try:
                            if sub.is_file():
                                total += sub.stat().st_size
                                count += 1
                            elif sub.is_dir():
                                for sub2 in sub.iterdir():
                                    try:
                                        if sub2.is_file():
                                            total += sub2.stat().st_size
                                            count += 1
                                    except:
                                        pass
                        except:
                            pass
                    if total > 0:
                        dir_sizes.append((item.name, total, count))
                except:
                    continue
    except:
        pass
    
    dir_sizes.sort(key=lambda x: x[1], reverse=True)
    print(f"  {'Directory':<25} {'Size':>15} {'Files':>10}")
    print(f"  {'-'*25} {'-'*15} {'-'*10}")
    for name, size, count in dir_sizes[:10]:
        print(f"  {name:<25} {format_size(size):>15} {count:>10}")
    
    # 特殊目录分析：WinSxS（系统组件存储）
    winsxs_path = Path('C:/Windows/WinSxS')
    if winsxs_path.exists():
        try:
            winsxs_size = sum(f.stat().st_size for f in winsxs_path.rglob('*') if f.is_file())
            print(f"\n[Special: C:/Windows/WinSxS]")
            print(f"  Size: {format_size(winsxs_size)}")
            print(f"  Note: This is the component store. Do NOT delete manually.")
        except:
            print(f"\n[Special: C:/Windows/WinSxS]")
            print(f"  Unable to calculate size (permission denied)")
    
    print("\n" + "=" * 70)
    print("Analysis complete")

if __name__ == "__main__":
    main()
