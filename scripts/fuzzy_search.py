# -*- coding: utf-8 -*-
"""
本地文件模糊搜索工具
使用自然语言描述搜索文件，支持中文
"""

import os
import sys
from pathlib import Path

def search_files(keyword, search_path="G:\\", extensions=None):
    """模糊搜索文件"""
    if extensions is None:
        extensions = ['.pdf', '.docx', '.doc', '.txt', '.md', '.xlsx', '.xls', '.pptx', '.ppt']
    
    results = []
    keywords = [keyword]
    
    # 简繁转换
    simple_to_trad = {
        '项目': '項目', '动画': '動畫', '铁路': '鐵路',
        '桥梁': '橋樑', '建设': '建設', '工程': '工程'
    }
    for k, v in simple_to_trad.items():
        if k in keyword:
            keywords.append(keyword.replace(k, v))
    
    # 提取关键字符
    key_chars = set()
    for kw in keywords:
        for c in kw:
            if not c.isalnum() and c not in key_chars:
                key_chars.add(c)
    
    print(f"搜索关键词: {keyword}")
    print(f"搜索变体: {keywords}")
    print(f"关键字符: {''.join(key_chars)}")
    print(f"搜索路径: {search_path}")
    print()
    
    for root, dirs, files in os.walk(search_path):
        for filename in files:
            if Path(filename).suffix.lower() not in extensions:
                continue
            
            filepath = os.path.join(root, filename)
            score = 0
            matched = []
            
            for kw in keywords:
                if kw.lower() in filename.lower():
                    score += 100
                    matched.append(f"关键词'{kw}'")
                if kw.lower() in filepath.lower():
                    score += 50
            
            # 关键字符匹配
            for c in key_chars:
                if c in filename:
                    score += 5
            
            # 特殊关键词加分
            special_keywords = ['中铁', '二十四局', '沪昆', '铁路', '合同', '动画', '演示', '施工']
            for sk in special_keywords:
                if sk in filename:
                    score += 30
                    matched.append(sk)
            
            if score > 0:
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                results.append({
                    'score': score,
                    'name': filename,
                    'path': filepath,
                    'size': f"{size_mb:.2f} MB",
                    'matched': ', '.join(matched)
                })
    
    # 排序
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "中铁二十四局沪昆铁路合同"
    search_path = sys.argv[2] if len(sys.argv) > 2 else "G:\\"
    
    print("=" * 50)
    print("本地文件模糊搜索工具")
    print("=" * 50)
    print()
    
    results = search_files(keyword, search_path)
    
    if results:
        print(f"找到 {len(results)} 个结果:")
        print()
        for r in results[:30]:
            print(f"[分数: {r['score']}] {r['name']}")
            print(f"   路径: {r['path']}")
            print(f"   大小: {r['size']}")
            print(f"   匹配: {r['matched']}")
            print()
    else:
        print("未找到匹配的文件")