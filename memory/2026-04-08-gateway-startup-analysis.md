# Session: 2026-04-08 06:37:54 UTC

- **Session Key**: agent:main:main
- **Session ID**: 190f2878-3fa6-43bd-a902-604ef7727071
- **Source**: webchat

## Conversation Summary

assistant: 开始排查 `node.list` 慢的问题，预计 3 步。

**第 1 步：检查节点配置**

assistant: **第 2 步：分析 56 秒延迟前后的日志上下文**

assistant: **第 3 步：实时测试 node.list 性能**

assistant: **排查结果：**

`node.list` 大多数时候很快（50-200ms），但有两次异常：

| 时间 | 耗时 | 关联事件 |
|------|------|---------|
| 07:43:58 | **58.7秒** | Control UI 启动批量查询 |
| 07:53:57 | **56.8秒** | WeChat 插件重连 + Control UI 批量查询重叠 |

**根本原因：**

不是 `node.list` 本身慢，而是它被阻塞在 WebSocket RPC 队列里。等 `models.list`（12秒）和 `chat.history`（12秒）这些耗时操作完成后，才轮到它。

**优化方向：**

1. **Control UI 启动时批量调用** → 建议给 Control UI 加请求间隔或合并批量查询
2. **WeChat 插件重连机制** → 每次重连都会触发 `setWeixinRuntime`，可能影响 RPC 响应
3. **当前正常** → 最新几次 `node.list` 都是 2-8 秒，正常范围

要不要我给 OpenClaw 提个 issue，反映 Control UI 启动时批量查询阻塞的问题？
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Wed 2026-04-08 08:06 GMT+8] 你能根据现有的启动情况进一步分析启动时间太长的问题吗？如果信息还不够，是不是需要针对启动进行专门的监控，然后再分析监控的情况？
assistant: 好问题，让我先抓取今天启动那段完整日志来分析。

assistant: 现在我有了完整的启动日志，可以清晰地看到问题了。

---

## 🔍 启动时间分析

从日志提取的完整时间线（第一次启动）：

| 时间 | 耗时 | 事件 |
|------|------|------|
| 07:06:43 | 0s | Gateway 开始启动 |
| 07:06:45 | +2s | 加载配置完成 |
| 07:06:46 | +3s | 开始认证 |
| 07:07:06 | +20s | **Gateway Ready（8插件，20.3秒）** |
| 07:07:06 | +20s | 开始启动 channels/sidecars |
| 07:07:07 | +21s | **检测到 stale gateway (PID 27540)** |
| 07:07:07 | +21s | 停止 stale 进程，重试 |
| 07:07:29 | +43s | 第二次启动开始 |
| 07:07:53 | +67s | 第二次 ready (20.4s) |
| 07:07:54 | +68s | **60s 健康检查超时** |
| 07:07:54 | +68s | 端口 18789 已被占用（PID 31920）|

---

## 🐌 慢的根本原因：不是启动慢，是重复启动

**Gateway 本身启动只需 ~20 秒**，但触发了两次启动：

1. **第一次启动**：07:06:43 → 07:07:06（20秒），但 07:07:07 检测到 stale gateway（PID 27540），认为没启动成功
2. **第二次启动**：07:07:29 → 07:07:53（20秒），又等了 60s 健康检查，但健康检查本身有问题（device-required）

**核心问题：**
1. **`device-required` 错误** - 健康检查探测失败了
2. **`pricing bootstrap failed`** - 模型价格服务启动超时
3. **Bonjour 广告卡住** - 服务卡在 probing 状态超过 11 秒

---

**结论：现有的日志够分析，不需要额外监控。**

最大的问题是 **Scheduled Task 重启时没有正确等待 gateway 健康**，导致重复启动。Gateway 本身 20 秒就 ready 了，但健康检查的 60 秒超时和实际的 device-required 错误叠加，让整个过程显得很慢。

要我针对这三个具体问题逐一修复吗？
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Wed 2026-04-08 08:14 GMT+8] 1、device-required 错误 -健康检查探测为什么每次都会失败（导致每次启动都会启动两次）
2、pricing bootstrap failed - 模型价格服务启动超时，也是从来都没有正常过，这个是不是必须的，能否修复或者无法修复就取消。
3、Bonjour 广告卡住 - 服务卡在 probing 状态超过 11 秒，这个也是能否修复或者无法修复就取消。
你的修复方案是什么
assistant: 好问题，逐个分析。预计 3 步，先查配置和日志找到根因，再给出方案。

**第 1 步：查看当前配置中与这三个问题相关的部分**

assistant: **第 2 步：查 OpenClaw 文档中这三个子系统的配置方式**

assistant: **第 3 步：在源码中定位这三个子系统的具体配置项**

assistant: **第 3 步：确认修复方案**

基于源码分析，以下是三个问题的根因和修复方案：

---

## 🔍 分析结果

### 问题 1：device-required（健康检查探测失败）

**根因**：Gateway 内部有健康检查机制（`refreshGatewayHealthSnapshot`），它会定期通过 WebSocket 连接到自己的控制界面来检查状态。当 Gateway 由 Scheduled Task 启动时，这个自检连接会因为"未配对设备"而被拒绝。

**这会导致**：
- 健康检查失败 → 认为 gateway 不健康 → 触发 channel restart 循环
- 但实际上 gateway 本身是健康的

**修复方案**：这是 OpenClaw 的已知行为，没有配置文件可以直接修改。可以通过给 Scheduled Task 增加 `startupGrace` 时间来缓解——让 gateway 先完全启动，再进行健康检查。

---

### 问题 2：pricing bootstrap failed

**根因**：Gateway 启动时会从 OpenRouter API 拉取模型价格目录（`https://openrouter.ai/models`），但国内网络不通，2秒超时后失败。

**关键代码**：
```javascript
fetchImpl(OPENROUTER_MODELS_URL, {
    signal: AbortSignal.timeout(FETCH_TIMEOUT_MS)  // 超时即放弃
});
```

**影响**：只是 warning，不影响启动，但每次启动都会记日志。

**修复方案**：**无配置文件可关**。只能通过环境变量或等待官方修复。我建议向 OpenClaw 提 issue，请求增加 `OPENCLAW_DISABLE_PRICING_REFRESH=1` 选项。

---

### 问题 3：Bonjour 广告卡住

**根因**：mDNS 广播卡在 `probing` 状态超过 11 秒，触发 automatic restart。这是非 Windows Native 环境的常见问题。

**修复方案**：**有解！** 可以通过环境变量禁用：
```
OPENCLAW_DISABLE_BONJOUR=1
```

---

## ✅ 推荐修复操作

| 修复项 | 操作 | 效果 |
|--------|------|------|
| **禁用 Bonjour** | 设置 `OPENCLAW_DISABLE_BONJOUR=1` | 消除 mDNS 卡住问题 |
| **增加 startup grace** | Scheduled Task 增加延迟 | 给 gateway 更多时间完成自检 |
| **pricing** | 向官方提 issue | 等待修复 |

需要我现在执行前两个修复吗？
user: Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
When reading HEARTBEAT.md, use workspace file C:/Users/Administrator/.openclaw/workspace/HEARTBEAT.md (exact case). Do not read docs/heartbeat.md.
Current time: Wednesday, April 8th, 2026 - 08:54 (Asia/Shanghai) / 2026-04-08 00:54 UTC
assistant: 早晨检查时间到！距离上次 morning check 已过去 2 天，执行例行检查。

assistant: Morning check complete. C盘 76.3GB (34.2%) · RAM 15.1GB free · Gateway running. Memory updated.

HEARTBEAT_OK
