# OpenClaw 技能开发规范

## 技能结构

```
skill-name/
├── SKILL.md              # 必需：技能定义
├── _meta.json           # 必需：元数据
├── references/          # 可选：参考文档
├── scripts/             # 可选：脚本
│   ├── main.py
│   ├── utils.py
│   └── ...
├── assets/             # 可选：静态资源
└── package.json        # 可选：Node依赖
```

## SKILL.md 格式

```markdown
# SKILL.md - 技能名称

## 触发条件
描述何时使用此技能。

## 功能说明
详细说明技能功能。

## 工具列表
使用此技能需要的工具：
- tool_name: 工具说明

## 使用示例
### 示例1
\`\`\`
用户输入...
\`\`\`

### 示例2
\`\`\`
用户输入...
\`\`\`

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|

## 注意事项
- 注意点1
- 注意点2

## 最佳实践
- 实践1
- 实践2
```

## _meta.json 格式

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "技能描述",
  "author": "作者",
  "homepage": "https://github.com/...",
  "keywords": ["tag1", "tag2"],
  "license": "MIT",
  "openclaw": {
    "version": "2026.4.x"
  }
}
```

## 脚本示例

### Python脚本

```python
#!/usr/bin/env python3
"""技能主脚本"""

import sys
import json

def main():
    # 读取输入
    input_data = json.loads(sys.stdin.read())
    
    # 处理逻辑
    result = process(input_data)
    
    # 输出结果
    print(json.dumps(result))

def process(data):
    """处理函数"""
    return {
        "success": True,
        "result": data
    }

if __name__ == "__main__":
    main()
```

### JavaScript脚本

```javascript
#!/usr/bin/env node

const main = async () => {
  // 读取输入
  const input = JSON.parse(await readStdin());
  
  // 处理逻辑
  const result = await process(input);
  
  // 输出结果
  console.log(JSON.stringify(result));
};

const process = async (data) => {
  return {
    success: true,
    result: data
  };
};

main().catch(console.error);
```

## 工具调用规范

### exec工具

```yaml
tools:
  exec:
    command: "python3 /path/to/script.py"
    args:
      - "--input"
      - "{input}"
    timeout: 60
```

### 请求格式

```json
{
  "action": "execute",
  "skill": "skill-name",
  "input": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

## 发布技能

```bash
# 通过clawhub发布
clawhub publish

# 通过npm发布
npm publish
```

---

*来源：openclawx.cloud/en/tools/creating-skills*
