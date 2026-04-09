const fs = require('fs');
const path = 'C:/Users/Administrator/.openclaw/workspace/MEMORY.md';
let content = fs.readFileSync(path, 'utf8');

// Find the ClawLibrary section and replace
const oldPattern = /ClawLibrary 修复\*\* \(2026-04-05 更新\)\n   - \*\*问题\*\*: 502 Bad Gateway \(Vite 开发服务器异常\)\n   - \*\*访问地址\*\*: `http:\/\/localhost:5173\/`\n   - \*\*状态\*\*: 待排查\n4\. \*\*WizTree 添加到安全软件白名单\*\*/;

const newContent = `ClawLibrary 修复** (2026-04-05 更新，2026-04-06 已修复)
   - **问题**: 502 Bad Gateway (Vite 开发服务器异常)
   - **访问地址**: \`http://localhost:5173/\`
   - **状态**: ✅ 已修复 (2026-04-06 22:20 重启服务后恢复)
   - **验证**: HTTP 200 OK，端口 5173 监听中 (PID 27924)
4. **WizTree 添加到安全软件白名单**`;

if (oldPattern.test(content)) {
    content = content.replace(oldPattern, newContent);
    fs.writeFileSync(path, content, 'utf8');
    console.log('Successfully updated MEMORY.md');
} else {
    console.log('Pattern not found, trying to find ClawLibrary section...');
    const idx = content.indexOf('ClawLibrary 修复');
    if (idx >= 0) {
        console.log('Found at index', idx);
        console.log('Content around it:', JSON.stringify(content.substring(idx, idx + 500)));
    }
}
