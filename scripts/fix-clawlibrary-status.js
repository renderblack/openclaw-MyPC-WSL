const fs = require('fs');
const path = 'C:/Users/Administrator/.openclaw/workspace/MEMORY.md';
const buf = fs.readFileSync(path);

// Find "WizTree"
const wizTreeBytes = Buffer.from('WizTree', 'utf8');
let wizIdx = -1;
for (let i = 0; i < buf.length - wizTreeBytes.length; i++) {
    let match = true;
    for (let j = 0; j < wizTreeBytes.length; j++) {
        if (buf[i + j] !== wizTreeBytes[j]) { match = false; break; }
    }
    if (match) { wizIdx = i; break; }
}

console.log('WizTree at', wizIdx);

// Find the beginning of the line containing WizTree
// Walk backwards from wizIdx to find newline (0x0a)
let lineStart = wizIdx;
while (lineStart > 0 && buf[lineStart - 1] !== 0x0a) lineStart--;

// Find the previous line (which should contain the corrupted status)
let prevLineStart = lineStart - 1;
while (prevLineStart > 0 && buf[prevLineStart - 1] !== 0x0a) prevLineStart--;

// Find the end of the WizTree line
let lineEnd = wizIdx;
while (lineEnd < buf.length && buf[lineEnd] !== 0x0a) lineEnd++;

console.log('Previous line starts at', prevLineStart, 'ends before', lineStart);
console.log('WizTree line starts at', lineStart, 'ends at', lineEnd);

// Get the corrupted line content
const corruptedLine = buf.slice(prevLineStart, lineStart - 1).toString('utf8');
console.log('Corrupted line:', JSON.stringify(corruptedLine));

// The corrupted line ends with "待排" + U+FFFD + "4. **WizTree"
// We need to replace this entire line with the proper status

// Create the replacement text
const newLine = '   - **状态**: ✅ 已修复 (2026-04-06 22:20 重启服务后恢复)\n';
const newVerification = '   - **验证**: HTTP 200 OK，端口 5173 监听中 (PID 27924)\n';

console.log('Creating replacement...');

// Replace from prevLineStart to lineEnd (inclusive of newline at lineEnd)
const before = buf.slice(0, prevLineStart);
const after = buf.slice(lineEnd + 1); // +1 to skip the newline at end of WizTree line

const newBuf = Buffer.concat([before, Buffer.from(newLine + newVerification, 'utf8'), after]);

fs.writeFileSync(path, newBuf);
console.log('Done!');
