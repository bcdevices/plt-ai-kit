# Flow control

## resume

Control resume behavior

Control whether to allow an operator to resume test plan execution after a test item failure.

Resuming is allowed by default (as if resume on had run at the start of the plan). When resuming is allowed and a test item fails, the PLT screen presents the operator with a Resume/Abort choice; choosing Resume continues the plan with the next test item. When resuming is not allowed, a test item failure aborts the plan immediately, with no operator prompt.

This setting is scoped to the running test plan: whichever state is in effect (on or off) at the moment a step fails is what applies to that failure. A resume step earlier in the plan changes behavior for every step after it.

```yaml
- command: resume on|off
```

| Argument | Description |
|---|---|
| `on` | Allow operator to resume test plan execution (default) |
| `off` | Do not allow operator to resume test plan execution; abort the plan immediately on failure |

## sleepms

Delay [Deprecated]

Temporarily suspend test suite execution for a fixed duration, displaying an optional message on the PLT screen for the duration of the delay.

```yaml
- command: sleepms <duration> [<message>]
```

| Argument | Description |
|---|---|
| `<duration>` | Delay duration, in milliseconds (integer). If a timeout: step field is also set, the shorter of the two is used. If neither is set, the step fails. |
| `<message>` | Optional: Message to display on screen during delay. |

The operator can abort the delay early from the PLT screen; doing so aborts the running test plan.

> **NOTE:** If duration cannot be parsed as an integer, it is instead treated as message (i.e. sleepms <message> with no explicit duration), and a timeout: step field must supply the delay.

See also: `wait`
## wait

Delay

Temporarily suspend test suite execution for a fixed duration, displaying an optional message on the PLT screen for the duration of the delay.

```yaml
- command: wait [<message>]
  timeout: <duration>
```

| Argument | Description |
|---|---|
| `timeout` | Step-level field that provides the delay duration. Either a plain number, interpreted as milliseconds (e.g. 500), or a Go duration string such as 500ms, 5s, or 1m30s. Required; the step fails to parse if timeout: is omitted. |
| `<message>` | Optional: Message to display on screen during delay. |

The operator can abort the delay early from the PLT screen; doing so aborts the running test plan.

See also: `sleepms`
