import json

with open("C:\\temp\\gdu_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"数据长度：{len(data)}")
print(f"索引 0: {data[0]}")
print(f"索引 1: {data[1]}")
print(f"索引 2: {data[2]}")
print(f"索引 3 类型：{type(data[3])}")

if isinstance(data[3], list):
    print(f"索引 3 长度：{len(data[3])}")
    if len(data[3]) > 0:
        print(f"第一个元素：{data[3][0]}")
        if len(data[3]) > 1:
            print(f"第二个元素：{data[3][1]}")
