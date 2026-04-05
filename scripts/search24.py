# -*- coding: utf-8 -*-
import os
import sys

keyword = sys.argv[1] if len(sys.argv) > 1 else "24"
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
        if keyword in filepath:
            score += 50
        if "24" in filename or "二十四" in filename:
            score += 30
        if "沪昆" in filename:
            score += 30
        if "铁路" in filename:
            score += 20
        if "合同" in filename:
            score += 20
        
        if score > 0:
            results.append((score, filename, filepath))

results.sort(reverse=True)

output = []
output.append("找到 %d 个结果:\n" % len(results))
for score, name, path in results[:30]:
    output.append("[%d] %s" % (score, name))
    output.append("   %s\n" % path)

with open(r"C:\Users\Administrator\.openclaw\workspace\search_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))