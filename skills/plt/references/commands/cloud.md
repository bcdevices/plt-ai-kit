# PLTcloud

## serial

Request or set serial number

Set serial number, from test plan or through PLTcloud.

Under Project Settings in PLTcloud, serial number allocation can be configured to use either monotonic counters, or through a webhook.

```yaml
- command: serial request [<KEY>:<jsonKey>]...

- command: serial set <value>
```

| Argument | Description |
|---|---|
| `request` | Request serial number through PLTcloud backend |
| `<KEY>` | Test plan user key to extract from webhook response |
| `<jsonKey>` | Webhook response "extra" map key |
| `set` | Set serial number from test plan |
| `<value>` | Serial number to set |

serial request requires an active PLTcloud connection and fails the step if none is available. Any number of <KEY>:<jsonKey> mappings may be given; each copies the value of jsonKey from the webhook response's extra map into the test plan user key KEY. A jsonKey absent from the response is silently skipped.

serial set assigns the serial number directly from the test plan, with no PLTcloud round-trip.

Examples: Cloud Interaction (`TestPlanReference/cloud/`)
See also: `webhook`, PLTcloud Reference (`pltcloud/`), Serial Number Webhook API (`pltcloud/webhook-api/`)
## webhook

Invoke webhook

Invoke a webhook through PLTcloud. The webhook HTTPS endpoint, URL, and HTTP method are configured in Project Settings on PLTcloud — the test plan step only triggers the call and maps the response back into test plan keys.

The webhook call is sent with the current DUT's identifying information (serial number, release, project). PLTcloud's webhook response can include an "extra" map of key/value pairs; each <KEY>:<jsonKey> mapping copies the value at jsonKey in that map into the test plan user key KEY, where it can be used like any other defined key. Mappings for keys absent from the response are silently skipped. The step fails if PLTcloud is unreachable or the webhook call itself fails; it does not validate the webhook's own HTTP response status.

```yaml
- command: webhook request [<KEY>:<jsonKey>]...
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `request` | Invoke webhook through PLTcloud backend |
| `<KEY>` | Test plan user key to store the extracted value under |
| `<jsonKey>` | Key to read from the webhook response's "extra" map |
| `<retryCount>` | Number of times to retry the test step (optional) |

Examples: Cloud Interaction (`TestPlanReference/cloud/`)
See also: `serial`, PLTcloud Reference (`pltcloud/`), Serial Number Webhook API (`pltcloud/webhook-api/`)
