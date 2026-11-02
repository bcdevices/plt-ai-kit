---
name: plt-mcp
description: >-
  Use the PLT MCP server's tools to work with PLTcloud as the signed-in user: list organizations, projects, PLTs, deployment groups and releases, upload a test plan and firmware as a release, deploy it to an allowed test deployment group, and read the test results and history. Use when the pltcloud___ or pltdata___ tools are available and the user wants to run a test plan on a PLT, send firmware or a plan to PLTcloud, or look up PLTs, releases or test results. To run the command line tool instead use pltutil; to write a plan use plt-test-plan-builder; to diagnose a failing step use plt-debugging.
---

# PLT MCP server

The `plt-mcp` server gives the agent PLTcloud tools that act as the signed-in
user. It is a proof of concept against PLTcloud **staging**. Its data and
releases are not production's.

Tools are named here as the gateway names them, such as
`pltcloud___deploy_release`. The client adds its own prefix to that name.

## Before using it

1. If no `pltcloud___` or `pltdata___` tools are available, ask the user to run
   `/mcp`, pick `plt-mcp` and sign in. Sign-in uses local port 8765 and fails
   while something else is listening on it. Chat clients without a shell cannot
   upload files; see [Run a release](#run-a-release).
2. If a tool answers `AUTH_FAILED` or an authorization error, the token has
   probably expired. It lasts about a day and is not refreshed. Ask the user to
   sign in again.
3. Get IDs from the tools. Do not guess a UUID, a model or a serial number.

## Find things

| Need | Tool |
|---|---|
| The user's organizations and roles | `pltdata___list_my_organizations` |
| The user's projects | `pltcloud___list_my_projects` |
| An organization's PLTs | `pltdata___list_devices` |
| One PLT, with recent errors | `pltdata___get_device`, then `pltdata___get_device_errors` |
| Deployment groups, their release and PLTs | `pltdata___list_deployment_groups` |
| A project's releases | `pltdata___list_releases` |
| One release, its files and plan validation | `pltdata___get_release` |
| Results of one release | `pltcloud___get_run_results` |
| A PLT's test reports, with failing step | `pltdata___get_test_history` |
| Pass, fail and incomplete counts per day | `pltdata___get_pass_fail_history` |
| Daily report counts | `pltdata___get_usage` |

Organization tools take `org_uuid`. Project and release tools take
`project_uuid`. Deployment groups belong to the organization, not the project.
The release, deployment group and results tools need the Administrator or
Manager role. A `null` answer from a `pltdata___` tool can mean the item does
not exist or that the user lacks that role.

## Run a release

Files never pass through the MCP server. The tools return presigned S3 URLs and
the agent uploads to them directly, so this needs a shell with `curl` and access
to the files.

A release is a flat set of files: one test plan `.yaml` plus whatever it uses.
Each file must be under 100 MB, with at most 20 files. Plans refer to files by
bare name, so `program STM32F4_STLink app.hex` needs a file named `app.hex`.

### 1. Check the files

Stop and report any problem here. Nothing has reached PLTcloud yet.

- **Lint the plan** with the linter in the `plt-test-plan-builder` skill:

  ```console
  python3 <skill-dir>/../plt-test-plan-builder/scripts/plt_lint.py --strict plan.yaml
  ```

  Exit `0` is clean and `1` means errors were reported. Exit `3` means PyYAML is
  missing, so the plan was not linted: install it with
  `python3 -m pip install pyyaml` and run the linter again.
- **Check every file the plan names is in the set.** The linter does not check
  this, and PLTcloud does not either. Go through each `program` step's images
  (`[offset:]<img>[,[offset:]<img>...]`, where `none` is not a file), any
  `pack:` file, and each `extflash_write` file.
- **Get each file's size and SHA-256:**

  ```console
  wc -c < "app.hex"
  shasum -a 256 "app.hex"
  ```

### 2. Choose the target and confirm

- Use a version the project has not used, such as the current UTC time:
  `2026-11-02T17:30:00Z`. Check with `pltdata___list_releases` and its `version`
  argument. Creating a release archives a published release with the same
  version, and a deployment group serving that release then serves nothing.
- `pltcloud___deploy_release`'s description lists the only targets the gateway
  allows. If the tool is not offered, this gateway allows no deploys.
- Read the group with `pltdata___list_deployment_groups`. A deploy reaches
  **every** PLT in the group; this server cannot target a single PLT, though
  `pltutil` can.
- **Deploying runs the plan on physical PLTs and any attached fixture and DUT.**
  Tell the user the group, its PLTs and the files, and get their confirmation
  before step 5. Do not retry a deploy without asking.

### 3. Get upload URLs

Call `pltcloud___prepare_file_uploads` with `project_uuid`, `version`, an
optional `description`, and `files` (`name` with no path, and `content_length`
in bytes). It returns a `release_id`, and an `id` and `upload_url` per file. The
URLs last 30 minutes and anyone holding one can write to it, so do not save them
to files or commits.

### 4. Upload each file

Send no extra headers, and quote the URL:

```console
curl -sS -f -T "app.hex" -D - -o /dev/null "$UPLOAD_URL" | tr -d '\r' | awk 'tolower($1) == "etag:" { print $2 }'
```

This prints the file's ETag. Keep it exactly, quotes included. If a PUT fails,
retry it to the same URL. If it cannot succeed, stop and start again from step 3.

### 5. Create the release

Call one of these only after every PUT has succeeded. PLTcloud does not check
that the files arrived. Pass the same `project_uuid`, `version` and
`description`, the `release_id`, and each file's `id`, `name`, `content_length`
and `etag`.

- `pltcloud___complete_file_uploads` creates the release and deploys nothing.
  This cannot be followed by a deploy: PLTcloud only deploys a release in the
  call that creates it, so running it later means uploading it again.
- `pltcloud___deploy_release` takes `deployment_group_uuid` as well. It creates
  the release, assigns it to the group, and sends it to every PLT in the group,
  which runs the plan.

### 6. Check it landed

Call `pltdata___get_release` and compare each file's `sha256` with your own. It
is empty until PLTcloud has processed the file, so check again if it is empty.
For `test_plan_validation`, only `invalid` is a failure. `pending` is normal
just after an upload, and can last indefinitely if PLTcloud never checks the
plan.

### 7. Read the result

Call `pltcloud___get_run_results` with `project_uuid`, the `release_id` as
`release_uuid`, and `wait_seconds: 20`, and repeat until there is a report.

- Each PLT in the group produces its own report, so compare them with the
  group's PLTs. Read `pass_fail`; a report arriving does not mean the test passed.
- No report yet is not a failure. On `pltdata___list_deployment_groups`,
  `on_group_release` turning true shows the PLT received the release. After about
  10 minutes with no report, tell the user, who may need to check the bench. Do
  not redeploy without asking.
- **Do not judge whether a PLT is up from `connected` or `last_seen`.** On
  staging they can be weeks out of date while the PLT runs tests. A recent test
  report is the reliable sign.
- For a `FAIL`, get the failing step from `pltdata___get_test_history` for that
  PLT and use the `plt-debugging` skill. `INCOMPLETE` there means the run never
  finished, which is different from a step failing its check. Failure detail is
  clipped at 300 characters; the full report is in the PLTcloud web console.

## Errors

| Error | Meaning | Do |
|---|---|---|
| `AUTH_FAILED` | Token expired or not accepted, or no PLTcloud staging account | Ask the user to sign in again |
| `PERMISSION_DENIED` | Not Administrator or Manager on the project, or the target is not allowed | Tell the user; do not try another target |
| `INVALID_INPUT` | A bad argument, or a `release_id` that already exists | Fix the argument. For an existing `release_id`, restart from step 3 |
| `OUTCOME_UNKNOWN` | PLTcloud may have created the release, assigned it, and reached some PLTs | **Do not retry.** Check `pltdata___list_releases` and `pltdata___list_deployment_groups`, then tell the user |
| `TIMEOUT`, `UPSTREAM_UNAVAILABLE` | PLTcloud was slow, unreachable, or answered unexpectedly | Retry once. After a creating call, check `pltdata___list_releases` first |

## Where to look

| Need | Read |
|---|---|
| Writing or linting the plan | the `plt-test-plan-builder` skill |
| What a command or target does | the `plt` skill |
| Diagnosing a failing step | the `plt-debugging` skill |
| Projects, releases and deployment groups | the `plt-cloud` skill's `references/projects.md` |
| Deploying from a terminal or to a single PLT, with an API token | the `pltutil` skill |
