---
name: plt-cloud
description: >-
  Reference for PLTcloud, the Blue Clover Devices cloud backend - web console administration, projects, releases and deployment groups, PLT connectivity, serial number and webhook APIs, webhook signature validation, CI upload, the Hardware CI GitHub App, the Report Connector and the Slack app. Use when the user asks about PLTcloud, deploying firmware or test plans to PLTs, test reports, or implementing a webhook endpoint. For commands and hardware info use plt; to write a plan use plt-test-plan-builder.
metadata:
  version: "20260415.0.1-32-gce6971592"
---

# PLTcloud

PLTcloud is the cloud backend for Blue Clover Devices PLTs. Each PLT holds a
secured connection to PLTcloud, which it uses to:

- receive firmware and test plans (a project *release*, deployed to PLTs
  through deployment groups)
- execute webhooks during a test run
- upload test reports

Humans manage organizations, users, PLTs, projects and releases through the
web console at https://pltcloud.com/. Releases can also be uploaded from a CI
pipeline with the PLTcloud command line client.

## Test plan commands that reach PLTcloud

These steps fail when the PLT has no PLTcloud connection. Full syntax is in
the `plt` skill's `references/commands/cloud.md`.

- `serial` — Request or set serial number
- `webhook` — Invoke webhook

Serial number allocation (monotonic counter or webhook) and the webhook
endpoint itself are configured in the project's Project Settings on PLTcloud,
not in the test plan.

## Where to look

PLTcloud documentation pages are bundled below, grouped by task. Each
page is a `## <title>` section with its source path.

| Need | Read |
|---|---|
| Serial number allocation, webhook payloads, validating `X-Hub-Signature-256` | `references/webhooks.md` |
| Uploading releases from CI, the PLT Hardware CI GitHub App / Action | `references/ci.md` |
| Exporting reports (Report Connector, S3), the Slack app | `references/reports.md` |
| Network requirements for a PLT (DHCP, DNS, firewall, NTP), service status | `references/connectivity.md` |
| Accounts, organizations, users, adding PLTs, deployment groups | `references/web-console.md` |
| Projects, files, releases, project settings, debug keys, viewing reports | `references/projects.md` |
| Syntax of `serial` / `webhook` steps | the `plt` skill's `references/commands/cloud.md` |

Page paths in this skill and its references are relative to https://docs.pltcloud.com/ — a page's URL is that base plus its path.

Product policies (end-of-life, update patches) are at
`policies/`.
