# OpenClaw 技能开发规范

## 技能设计原则

1. **单一职责**：一个技能只做一件事
2. **可组合**：与其他技能协同工作
3. **幂等性**：重复执行结果一致
4. **可测试**：有明确的输入输出

## 目录结构

```
my-skill/
├── SKILL.md              # 必须：技能定义
├── _meta.json            # 必须：元数据
├── references/          # 可选：参考文档
│   ├── api.md
│   └── guide.md
├── scripts/             # 可选：脚本
│   ├── main.py
│   └── utils.py
├── assets/              # 可选：静态资源
├── tests/               # 可选：测试
│   └── test_main.py
└── package.json         # 可选：Node依赖
```

## SKILL.md 编写规范

```markdown
# SKILL.md - skill-name

## 触发条件
当用户请求...时使用此技能。

## 功能说明
详细描述技能功能。

## 工作流程
1. 步骤1
2. 步骤2
3. 步骤3

## 工具依赖
- exec: 执行Python脚本
- browser: 抓取网页

## 输入参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|

## 输出格式
\`\`\`json
{
  "success": true,
  "result": {}
}
\`\`\`

## 错误处理
| 错误 | 处理方式 |
|------|---------|
| 网络错误 | 重试3次 |
| 超时 | 返回缓存 |

## 使用示例
### 示例1：基础用法
用户：xxx
助手：xxx

### 示例2：高级用法
用户：xxx
助手：xxx

## 注意事项
- 注意1
- 注意2
```

## _meta.json 编写规范

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "技能描述（不超过100字）",
  "author": "作者名",
  "homepage": "https://github.com/xxx",
  "keywords": ["keyword1", "keyword2"],
  "license": "MIT",
  "openclaw": {
    "version": "2026.4.x",
    "tools": ["exec", "browser"],
    "channels": ["*"]
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/xxx"
  }
}
```

## 脚本开发规范

### Python

```python
#!/usr/bin/env python3
"""技能名称

功能描述
"""

import sys
import json
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='技能名称')
    parser.add_argument('--input', required=True, help='输入数据')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    args = parser.parse_args()
    
    # 读取输入
    input_data = json.loads(sys.stdin.read()) if not args.input else json.loads(args.input)
    
    # 处理
    result = process(input_data)
    
    # 输出
    print(json.dumps(result, ensure_ascii=False))

def process(data):
    """核心处理函数"""
    try:
        # 处理逻辑
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    main()
```

### JavaScript

```javascript
#!/usr/bin/env node

const main = async () => {
  // 解析参数
  const args = process.argv.slice(2);
  const input = args.includes('--input') 
    ? JSON.parse(args[args.indexOf('--input') + 1])
    : JSON.parse(await readStdin());
  
  // 处理
  const result = await process(input);
  
  // 输出
  console.log(JSON.stringify(result));
};

const process = async (data) => {
  try {
    // 处理逻辑
    return { success: true, data };
  } catch (error) {
    console.error(error);
    return { success: false, error: error.message };
  }
};

const readStdin = () => new Promise((resolve) => {
  let data = '';
  process.stdin.on('data', chunk => data += chunk);
  process.stdin.on('end', () => resolve(data));
});

main();
```

## 测试规范

```python
# tests/test_main.py
import unittest
from scripts.main import process

class TestSkill(unittest.TestCase):
    def test_basic(self):
        result = process({"input": "test"})
        self.assertTrue(result["success"])
    
    def test_error(self):
        result = process({"invalid": True})
        self.assertFalse(result["success"])

if __name__ == "__main__":
    unittest.main()
```

## 发布流程

```bash
# 1. 本地测试
npm install -g @openclaw/skill-cli
openclaw skills test ./my-skill

# 2. 提交到clawhub
clawhub login
clawhub publish

# 3. GitHub发布（可选）
git tag v1.0.0
git push origin v1.0.0
```

## 质量检查清单

- [ ] SKILL.md完整且格式正确
- [ ] _meta.json格式正确
- [ ] 脚本可执行权限正确
- [ ] 有错误处理
- [ ] 有单元测试
- [ ] 文档示例可运行

---

*来源：openclawx.cloud/en/tools/creating-skills + 实战经验*
