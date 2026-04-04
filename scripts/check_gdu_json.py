import json

with open("C:\\temp\\gdu_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"JSON 类型：{type(data)}")
print(f"JSON 长度：{len(data)}")
print()

for i, item in enumerate(data[:5]):
    print(f"索引 {i}: {type(item)} = {item}")
    print()
