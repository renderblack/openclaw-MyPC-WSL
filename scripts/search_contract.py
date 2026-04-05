# -*- coding: utf-8 -*-
import os
import sys

keyword = sys.argv[1] if len(sys.argv) > 1 else "合同"
search_path = sys.argv[2] if len(sys.argv) > 2 else "G:\\"
extensions = ['.pdf', '.docx', '.doc', '.txt', '.md', '.xlsx', '.xls', '.pptx', '.ppt']

results = []
for root, dirs, files in os.walk(search_path):
    for filename in files:
        if os.path.splitext(filename)[1].lower() not in extensions:
            continue
        
        filepath = os.path.join(root, filename)
        score = 0
        
        if keyword.lower() in filename.lower():
            score += 100
        if "动画" in filename:
            score += 50
        if "演示" in filename:
            score += 30
        if "沪昆" in filename:
            score += 60
        if "铁路" in filename:
            score += 40
        if "中铁" in filename:
            score += 40
        if "二十四局" in filename:
            score += 60
        
        if score > 0:
            results.append((score, filename, filepath))

results.sort(reverse=True)

with open(r"C:\Users\Administrator\.openclaw\workspace\search_results2.txt", "w", encoding="utf-8") as f:
    f.write("找到 %d 个结果:\n\n" % len(results))
    for score, name, path in results[:50]:
        f.write("[%d] %s\n" % (score, name))
        f.write("   %s\n\n" % path)