# Scheduled Tasks (Cron)

Cron is the Gateway's built-in scheduler. It persists jobs, wakes the agent at the right time, and can deliver output back to a chat channel or webhook endpoint.

## Quick start

```bash
# Add a one-shot reminder
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

# Check your jobs
openclaw cron list

# See run history
openclaw cron runs --id <job-id>
```

## How cron works

* Cron runs **inside the Gateway** process (not inside the model).
* Jobs persist at `~/.openclaw/cron/jobs.json` so restarts do not lose schedules.
* All cron executions create [background task](/automation/tasks) records.
* One-shot jobs (`--at`) auto-delete after success by default.
* Isolated cron runs best-effort close tracked browser tabs/processes for their `cron:<jobId>` session when the run completes, so detached browser automation does not leave orphaned processes behind.
* Isolated cron runs also guard against stale acknowledgement replies. If the first result is just an interim status update (`on it`, `pulling everything together`, and similar hints) and no descendant subagent run is still responsible for the final answer, OpenClaw re-prompts once for the actual result before delivery.

Task reconciliation for cron is runtime-owned: an active cron task stays live while the cron runtime still tracks that job as running, even if an old child session row still exists. Once the runtime stops owning the job and the 5-minute grace window expires, maintenance can mark the task `lost`.

## Schedule types

| Kind    | CLI flag  | Description                                             |
| ------- | --------- | ------------------------------------------------------- |
| `at`    | `--at`    | One-shot timestamp (ISO 8601 or relative like `20m`)    |
| `every` | `--every` | Fixed interval                                          |
| `cron`  | `--cron`  | 5-field or 6-field cron expression with optional `--tz` |

Timestamps without a timezone are treated as UTC. Add `--tz America/New_York` for local wall-clock scheduling.

Recurring top-of-hour expressions are automatically staggered by up to 5 minutes to reduce load spikes. Use `--exact` to force precise timing or `--stagger 30s` for an explicit window.

## Execution styles

| Style           | `--session` value   | Runs in                  | Best for                        |
| --------------- | ------------------- | ------------------------ | ------------------------------- |
| Main session    | `main`              | Next heartbeat turn      | Reminders, system events        |
| Isolated        | `isolated`          | Dedicated `cron:<jobId>` | Reports, background chores      |
| Current session | `current`           | Bound at creation time   | Context-aware recurring work    |
| Custom session  | `session:custom-id` | Persistent named session | Workflows that build on history |

**Main session** jobs enqueue a system event and optionally wake the heartbeat (`--wake now` or `--wake next-heartbeat`). **Isolated** jobs run a dedicated agent turn with a fresh session. **Custom sessions** (`session:xxx`) persist context across runs, enabling workflows like daily standups that build on previous summaries.

For isolated jobs, runtime teardown now includes best-effort browser cleanup for that cron session. Cleanup failures are ignored so the actual cron result still wins.

When isolated cron runs orchestrate subagents, delivery also prefers the final descendant output over stale parent interim text. If descendants are still running, OpenClaw suppresses that partial parent update instead of announcing it.

### Payload options for isolated jobs

* `--message`: prompt text (required for isolated)
* `--model` / `--thinking`: model and thinking level overrides
* `--light-context`: skip workspace bootstrap file injection
* `--tools exec,read`: restrict which tools the job can use

`--model` uses the selected allowed model for that job. If the requested model is not allowed, cron logs a warning and falls back to the job's agent/default model selection instead. Configured fallback chains still apply, but a plain model override with no explicit per-job fallback list no longer appends the agent primary as a hidden extra retry target.

Model-selection precedence for isolated jobs is:
1. Gmail hook model override (when the run came from Gmail and that override is allowed)
2. Per-job payload `model`
3. Stored cron session model override
4. Agent/default model selection

Fast mode follows the resolved live selection too. If the selected model config has `params.fastMode`, isolated cron uses that by default. A stored session `fastMode` override still wins over config in either direction.

If an isolated run hits a live model-switch handoff, cron retries with the switched provider/model and persists that live selection before retrying. When the switch also carries a new auth profile, cron persists that auth profile override too. Retries are bounded: after the initial attempt plus 2 switch retries, cron aborts instead of looping forever.

## Delivery and output

| Mode       | What happens                                             |
| ---------- | -------------------------------------------------------- |
| `announce` | Deliver summary to target channel (default for isolated) |
| `webhook`  | POST finished event payload to a URL                     |
| `none`     | Internal only, no delivery                               |

Use `--announce --channel telegram --to "-1001234567890"` for channel delivery. For Telegram forum topics, use `-1001234567890:topic:123`. Slack/Discord/Mattermost targets should use explicit prefixes (`channel:<id>`, `user:<id>`).

For cron-owned isolated jobs, the runner owns the final delivery path. The agent is prompted to return a plain-text summary, and that summary is then sent through `announce`, `webhook`, or kept internal for `none`. `--no-deliver` does not hand delivery back to the agent; it keeps the run internal.

If the original task explicitly says to message some external recipient, the agent should note who/where that message should go in its output instead of trying to send it directly.

Failure notifications follow a separate destination path:
* `cron.failureDestination` sets a global default for failure notifications.
* `job.delivery.failureDestination` overrides that per job.
* If neither is set and the job already delivers via `announce`, failure notifications now fall back to that primary announce target.
* `delivery.failureDestination` is only supported on `sessionTarget="isolated"` jobs unless the primary delivery mode is `webhook`.

## CLI examples

One-shot reminder (main session):

```bash
openclaw cron add \
  --name "Calendar check" \
  --at "20m" \
  --session main \
  --system-event "Reminder: check the calendar" \
  --wake now
```

Periodic status report (isolated, daily):

```bash
openclaw cron add \
  --name "Daily standup" \
  --cron "0 9 * * 1-5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Summarize your tasks for today and blockers" \
  --announce --channel qqbot --to "qqbot:c2c:<user_id>"
```

Health check every 30 minutes:

```bash
openclaw cron add \
  --name "Health check" \
  --every 30m \
  --session isolated \
  --message "Run health diagnostics and report any issues" \
  --tools exec \
  --announce --channel telegram --to "<chat_id>"
```

## Troubleshooting

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| Job not running | Gateway restarted | Jobs persist; will run on next schedule |
| No output delivered | Wrong channel/chat ID | Verify with `openclaw cron list` |
| Model timeout | Slow model or network | Add `--timeout` or reduce job scope |
| Stale output | Interim text delivered instead of final | Use isolated session with `--message` |
| Orphaned browser | Automation not cleaned up | Isolated sessions now auto-clean |
