---
name: pltutil
description: >-
  Drive pltutil, the Blue Clover Devices PLTcloud command line tool. Install it, validate an API token and project access, upload a release, deploy to a deployment group or a single PLT, wait for a test report, and clear a PLT's direct target. Use when the user wants to run a test plan on a PLT from a terminal or coding agent, or asks about pltutil or its options. For the PLTcloud web console or CI setup use plt-cloud; to write a plan use plt-test-plan-builder.
metadata:
  version: "20261030.0.4"
---

# pltutil

`pltutil` uploads files as a PLTcloud project release, and can deploy that
release to PLTs and wait for the test report. It was named `pltcloud` before
v0.7.4.

## Before running it

1. Check that it is installed with `command -v pltutil`. Downloads are listed
   in `references/usage.md`.
2. Check that `PLTCLOUD_API_TOKEN` is set, without printing its value. Never
   print, log, or commit the token, and avoid `-t`, which exposes it in the
   process list. If it is missing, ask the user to set it.
3. Get the project UUID from the user, and the deployment group UUID or PLT
   serial number and model if deploying. Do not guess them.
4. Validate the token and project access. This uploads nothing:

   ```console
   pltutil -p "${PROJECT_UUID}" -vvv
   ```

## Actions that affect hardware

Confirm the target with the user before running these. Do not retry them
automatically.

- `-a` starts test plan execution on physical PLTs, and any fixture and DUT
  attached to them. With a deployment group, that means every PLT in the group.
- `-clear-plt` makes a PLT fall back to its deployment group release, which can
  downgrade it. The command does not ask for confirmation.

## Common tasks

Upload a release without starting it:

```console
pltutil -p "${PROJECT_UUID}" -v "1.2.3" -f "dist/*"
```

Deploy to a deployment group, run the test plan, and wait for the report:

```console
pltutil -p "${PROJECT_UUID}" -d "${DPG_UUID}" -utcDateVersion -a -wait-report -jsonp -report-save-dir . -f "dist/*"
```

Do the same on one PLT:

```console
pltutil -p "${PROJECT_UUID}" -pltserial 00006 -pltmodel plt-106 -utcDateVersion -a -wait-report -jsonp -report-save-dir . -f basic.yaml
```

Clear a PLT's direct target:

```console
pltutil -clear-plt -pltserial 00006 -pltmodel plt-106
```

## Reading the result

**Exit code 0 does not mean the test passed.** `-wait-report` exits 0 whenever
it receives a report, including a failing one. Always read `pass_fail`.

| Outcome | Exit code |
|---|---|
| Report received, PASS or FAIL | 0 |
| No report before `-wait-timeout` (default 10m), or any other error | 1 |
| Interrupted | 130 |

With `-jsonp`, log lines are JSON objects, mostly on stderr. When a report
arrives, the last line on stdout is the report summary, so parse that line:

```json
{"report_uuid": "...", "timestamp": "...", "model": "plt-106", "serial_number": "...", "plt_serial_number": "00006", "test_plan_title": "...", "pass_fail": "PASS"}
```

`-report-save-dir` writes the full report to `report-<uuid>.json`. When a test
fails, read that file and use the `plt-debugging` skill.

A timeout does not mean the test failed. The PLT may be offline, busy, or still
running. Tell the user, and do not redeploy without asking.

## Option rules

- `-f` requires a version: `-v` or `-utcDateVersion`.
- `-a` requires `-d`, or both `-pltserial` and `-pltmodel`.
- `-pltserial` and `-pltmodel` go together, need `-f` and `-a`, and cannot be
  combined with `-d`. Serial numbers are zero-padded to 5 digits.
- `-wait-report` requires `-f` and `-a`. `-report-save-dir` requires `-wait-report`.
- `-clear-plt` needs `-pltserial` and `-pltmodel`, and cannot be combined with
  upload options.
- Quote file patterns, such as `-f "dist/*"`, so the tool expands them instead
  of the shell.

## Where to look

| Need | Read |
|---|---|
| Downloads, worked examples with output, every option, `pltcloud` migration | `references/usage.md` |
| Changes per version, or an option an installed version rejects | `references/release-notes.md` |
| Setting up a CI pipeline, Hardware CI | the `plt-cloud` skill's `references/ci.md` |
| Finding project UUIDs | the `plt-cloud` skill's `references/projects.md` |
| Finding deployment group UUIDs | the `plt-cloud` skill's `references/web-console.md` |
| Creating API tokens | the `plt-cloud` skill's `references/ci.md` |
| Writing the test plan to upload | the `plt-test-plan-builder` skill |
| Diagnosing a failing report | the `plt-debugging` skill |

Page paths in this skill and its references are relative to https://docs.pltcloud.com/ — a page's URL is that base plus its path.
