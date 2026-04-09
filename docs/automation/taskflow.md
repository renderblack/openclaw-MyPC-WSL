# Task Flow

Task Flow is a directed graph executor for orchestrating complex, multi-step agentic workflows. It lets you define a graph of tasks with dependencies, then execute them in topological order — running independent branches in parallel and pausing at decision points.

## Concepts

### Nodes and edges

* **Nodes** — individual units of work (tool calls, agent runs, or sub-workflows)
* **Edges** — directional dependencies (`A → B` means B waits for A)
* **Parallel branches** — tasks with no mutual dependency run concurrently

### Task states

| State       | Meaning                                           |
| ----------- | ------------------------------------------------- |
| `pending`   | Waiting for dependencies                          |
| `running`   | Currently executing                               |
| `waiting`   | Paused at a decision (awaiting external input)    |
| `completed` | Finished successfully                             |
| `failed`    | Errored; downstream tasks are cancelled           |
| `cancelled` | Manually stopped; downstream tasks are cancelled  |

### Routing modes

Tasks support three routing behaviors:

* **linear** — process edges in definition order
* **dynamic** — routing determined at runtime based on context
* **conditional** — branch based on previous task output

## Defining a flow

Task Flow graphs are defined as JSON and submitted via the `openclaw tasks` CLI or the SDK.

```json
{
  "name": "build-and-deploy",
  "nodes": {
    "checkout": {
      "type": "tool",
      "tool": "exec",
      "params": { "command": "git checkout main" }
    },
    "test": {
      "type": "tool",
      "tool": "exec",
      "params": { "command": "npm test" },
      "depends": ["checkout"]
    },
    "build": {
      "type": "tool",
      "tool": "exec",
      "params": { "command": "npm run build" },
      "depends": ["checkout"]
    },
    "deploy": {
      "type": "tool",
      "tool": "exec",
      "params": { "command": "npm run deploy" },
      "depends": ["test", "build"]
    }
  }
}
```

## Execution

### Startup

Submit a flow:

```bash
openclaw tasks submit build-and-deploy.json
```

The Gateway creates a task record and begins execution. Independent tasks (`checkout` runs first; `test` and `build` run in parallel after `checkout`; `deploy` runs after both complete).

### Progress and inspection

```bash
# Check task status
openclaw tasks list

# Tail live output
openclaw tasks logs --id <task-id>

# Cancel a running task
openclaw tasks cancel --id <task-id>
```

### Wait and resume

For tasks paused at a decision node, use:

```bash
openclaw tasks resume --id <task-id> --choice <option>
```

## Decision nodes

Tasks can include interactive decision points. When a decision node is reached, execution pauses and the task enters `waiting` state. You can then:

* Resume with a specific choice via CLI
* Configure automatic decisions based on rules
* Set a timeout to auto-cancel or skip

```json
{
  "review": {
    "type": "decision",
    "prompt": "Should this PR be merged?",
    "options": ["approve", "request-changes", "comment"],
    "timeout": "24h"
  }
}
```

## Error handling

When a task fails, by default all downstream tasks are cancelled. You can override this per dependency:

```json
{
  "cleanup": {
    "type": "tool",
    "tool": "exec",
    "params": { "command": "docker system prune -f" },
    "depends": ["deploy"],
    "required": false
  }
}
```

## Webhook integration

Task completion can trigger webhooks:

```json
{
  "onComplete": "https://your-server.com/webhook/task-complete",
  "onFailure": "https://your-server.com/webhook/task-failed"
}
```

## Session binding

When a Task Flow run starts, it can be bound to a specific session:

```bash
openclaw tasks submit flow.json --session main
```

This lets the flow access workspace context, memory, and prior conversation state.

## CLI reference

| Command                       | Description                          |
| ----------------------------- | ------------------------------------ |
| `openclaw tasks submit <file>` | Submit a new task flow               |
| `openclaw tasks list`         | List all tasks (running/complete/etc) |
| `openclaw tasks logs --id X`  | Stream logs for a task               |
| `openclaw tasks cancel --id X` | Cancel a running task                |
| `openclaw tasks resume --id X` | Resume a waiting task                |
| `openclaw tasks inspect --id X`| Show full task graph and state       |
