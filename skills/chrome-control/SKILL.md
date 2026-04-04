# Chrome Control Skill

使用 Python + pychrome 库通过 Chrome DevTools Protocol (CDP) 控制 Chrome 浏览器。

## 功能

- 导航到指定 URL
- 截取页面截图
- 获取页面标题和 HTML 内容
- 元素交互（点击、输入文本）
- 表单填写
- JavaScript 执行

## 前提条件

1. **Chrome 已安装**
   - 路径：`C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`

2. **Python 依赖**
   ```bash
   pip install pychrome requests
   ```

3. **Chrome 以调试模式启动**
   ```bash
   chrome.exe --remote-debugging-port=9222
   ```

## 使用方法

### 启动 Chrome 调试模式

```powershell
# 关闭所有 Chrome 窗口后，以调试模式启动
chrome.exe --remote-debugging-port=9222 --no-first-run --no-default-browser-check
```

### 运行控制脚本

```bash
python C:\Users\Administrator\.openclaw\workspace\scripts\chrome_control.py
```

## 脚本功能

| 功能 | 函数 | 说明 |
|------|------|------|
| 获取标签页 | `get_tabs()` | 列出所有打开的标签页 |
| 导航 | `navigate_to(url, tab)` | 导航到指定 URL |
| 截图 | `take_screenshot(tab, path)` | 截取当前页面 |
| 页面标题 | `get_page_title(tab)` | 获取页面标题 |
| 页面内容 | `get_page_content(tab)` | 获取 HTML 内容 |
| 点击元素 | `click_element(tab, selector)` | 点击 CSS 选择器匹配的元素 |
| 输入文本 | `type_text(tab, selector, text)` | 向输入框填入文本 |

## 示例

```python
import pychrome
import base64
import time

CHROME_DEBUG_URL = "http://localhost:9222"

# 获取标签页
tabs = get_tabs()

# 创建浏览器和标签页
browser = pychrome.Browser(url=CHROME_DEBUG_URL)
tab = browser.new_tab()
tab.start()

# 导航
tab.call_method("Page.navigate", url="https://www.bing.com")
time.sleep(3)

# 截图
result = tab.call_method("Page.captureScreenshot", format="png")
screenshot_data = base64.b64decode(result['data'])
with open("screenshot.png", 'wb') as f:
    f.write(screenshot_data)

# 获取页面标题
result = tab.call_method("Runtime.evaluate", expression="document.title")
print(result['result']['value'])

tab.stop()
```

## 常见问题

**Q: Chrome 调试接口无法连接？**
A: 确保使用 `--remote-debugging-port=9222` 启动 Chrome，并且没有其他进程占用该端口。

**Q: 截图是空白或黑屏？**
A: 某些特殊页面（如 chrome:// 页面）可能无法截图，尝试访问普通 HTTPS 页面。

**Q: 如何关闭 Chrome 调试实例？**
A: 关闭所有 Chrome 窗口，或在任务管理器中结束 chrome.exe 进程。
