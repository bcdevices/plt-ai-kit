# pltutil Usage

Downloads, authentication, worked examples with their output, migration from pltcloud, and all command-line options.

## pltutil CLI

Source: `pltutil/`

pltutil is the PLTcloud command line tool. It uploads files as a project release and can trigger deployment and test plan execution on the PLTs in a deployment group, or on a single PLT. Run it from a terminal, a CI pipeline (`pltcloud/continuous-integration/`), or a coding agent.

See the release notes (`releases/pltutil/`) for all changes between versions.

**Renamed from pltcloud**

This tool was named pltcloud before v0.7.4. PLTcloud itself, the PLTCLOUD_API_TOKEN environment variable, and the PLTcloud GitHub Action (https://github.com/bcdevices/pltcloud-action) keep their names.

To migrate an existing script or CI pipeline to the current version:

- Replace the pltcloud command with pltutil.
- Install the pltutil package. Packages are now named pltutil_<VERSION>_<ARCH>.deb.
- Replace -model with -pltmodel and -serial with -pltserial.
- Replace -wait-report <DURATION> with -wait-report -wait-timeout <DURATION>, and remove -report-poll.

**Download**

The current version is v0.7.5.

| Package | Platform |
|---|---|
| pltutil_0.7.5_amd64.deb (https://download.pltcloud.com/cli/pltutil_0.7.5_amd64.deb) | Debian-based Linux, x86-64 |
| pltutil_0.7.5_arm64.deb (https://download.pltcloud.com/cli/pltutil_0.7.5_arm64.deb) | Debian-based Linux, ARM64 |

Packages connect to the production PLTcloud environment. To install one:

```console
$ sudo apt install ./pltutil_0.7.5_amd64.deb
```

macOS and Windows builds are not currently published for download.

**Authentication**

Select API Tokens from the drop-down menu under the user menu in PLTcloud, then select Add Release Token and copy the token.

pltutil reads the token from the PLTCLOUD_API_TOKEN environment variable. The -t option also accepts a token, but the environment variable keeps it out of your shell history and process list.

To check that the token is valid and grants access to a project, without uploading anything:

```console
$ export PLTCLOUD_API_TOKEN=...
$ pltutil -p "${PROJECT_UUID}" -vvv
INFO[0000] PLTcloud upload tool
INFO[0000] Validating release..
INFO[0001] Project access validated
INFO[0001] "bfe34e54-b2f3-11e9-8f4c-06f2ca2a1f06" is a valid project UUID
```

The tool exits with a non-zero code if the token is invalid or does not grant access to the project, so this command also works as a CI pipeline check.

**Usage**

**Upload a release**

```console
$ pltutil -p "${PROJECT_UUID}" -v "123" -f "fwdist/*"
```

Files can be specified with patterns such as **/prefix*, grandparent/**/child?, **/parent/*, or ** (all files and directories, recursively).

**Deploy to a deployment group**

Add -d to deploy the release to a deployment group.

```console
$ export PLTCLOUD_API_TOKEN=...
$ pltutil -p "${PROJECT_UUID}" -d "${DPG_UUID}" -v "123" -f "fwdist/*"
INFO[0001] Uploading "fwdist/bento2-blue.hex"
INFO[0002] Uploading "fwdist/bento2-green.hex"
INFO[0002] Uploading "fwdist/bento_flash_blinky_test_blue_2026-07-15_01.yaml"
INFO[0003] Upload Details:
       Release UUID: b1a86272-30c7-4812-a6ac-c42b7dde6031
       Project UUID: bfe34e54-b2f3-11e9-8f4c-06f2ca2a1f06
Deployment Group ID: 956226f0-19d8-4a54-88e8-5cb88f4db9f9
            Version: "123"
        Auto Deploy: false
             Repeat: false
             Resume: false
Files:
  - "bento2-blue.hex" (87 KiB)
  - "bento2-green.hex" (87 KiB)
  - "bento_flash_blinky_test_blue_2026-07-15_01.yaml" (2 KiB)
INFO[0003] Deployed release. Check for update on PLT
```

**Auto-deploy with a timestamp-derived version**

The -a option enables auto-deploy and triggers test plan execution on the PLTs in the deployment group. The -utcDateVersion option generates a version based on the current UTC date and time.

```console
$ export PLTCLOUD_API_TOKEN=...
$ pltutil -p "${PROJECT_UUID}" -d "${DPG_UUID}" -utcDateVersion -a -f "fwdist/*"
INFO[0001] Uploading "fwdist/bento2-blue.hex"
INFO[0002] Uploading "fwdist/bento2-green.hex"
INFO[0003] Uploading "fwdist/bento_flash_blinky_test_blue_2026-07-15_01.yaml"
INFO[0003] Upload Details:
       Release UUID: 636159d0-7291-4764-ad2c-4a0742941813
       Project UUID: bfe34e54-b2f3-11e9-8f4c-06f2ca2a1f06
Deployment Group ID: 956226f0-19d8-4a54-88e8-5cb88f4db9f9
            Version: "2026-10-23T08:30:42Z"
        Auto Deploy: true
             Repeat: false
             Resume: false
Files:
  - "bento2-blue.hex" (87 KiB)
  - "bento2-green.hex" (87 KiB)
  - "bento_flash_blinky_test_blue_2026-07-15_01.yaml" (2 KiB)
INFO[0003] Deployed release. Check for test report on PLTcloud or report connector
```

**Deploy to one PLT**

Use -pltserial and -pltmodel with -a to deploy to a single PLT instead of a deployment group. Both options are required, and they cannot be combined with -d. Serial numbers are zero-padded to 5 digits, so -pltserial 6 targets serial number 00006.

```console
$ pltutil -p "${PROJECT_UUID}" -pltserial 00006 -pltmodel plt-106 -v "123" -a -f basic.yaml
```

To clear the direct target, so the PLT falls back to its deployment group release:

```console
$ pltutil -clear-plt -pltserial 00006 -pltmodel plt-106
INFO[0001] Cleared the direct release target of PLT 00006 (plt-106). It now falls back to its deployment group release.
```

> **WARNING:** Clearing a direct target can downgrade the PLT to an older deployment group release. The command does not ask for confirmation.

Clearing needs a valid API token, but no project UUID. If no PLT matches, or your account is not an Administrator or Manager in the PLT's organization, the command reports the same error for both cases.

**Wait for a test report**

Use -wait-report with -a to wait for the first new test report on the deployed release, print it, and exit. The wait gives up after -wait-timeout (default 10 minutes). The -report-save-dir option also saves the report as JSON.

```console
$ pltutil -p "${PROJECT_UUID}" -d "${DPG_UUID}" -utcDateVersion -a -wait-report -report-save-dir . -f basic.yaml
INFO[0001] Uploading "basic.yaml"
INFO[0002] Upload Details:
       Release UUID: 825eee1a-42ca-4a42-8727-62f4d4b32bf7
       Project UUID: bfe34e54-b2f3-11e9-8f4c-06f2ca2a1f06
Deployment Group ID: 956226f0-19d8-4a54-88e8-5cb88f4db9f9
            Version: "2026-10-26T11:59:41Z"
        Auto Deploy: true
             Repeat: false
             Resume: false
Files:
  - "basic.yaml" (162 bytes)
INFO[0063] Saved test report to report-8f196758-07f1-43eb-9ce7-d257987efc0e.json
Test report 8f196758-07f1-43eb-9ce7-d257987efc0e: model=plt-106 serial=00006 pass_fail=PASS test_plan="Basic test plan"
```

With a deployment group, the first report from any PLT counts. With -pltserial and -pltmodel, only reports from that PLT count. Add -vvv to see progress messages during the wait.

> **IMPORTANT:** -wait-report exits with code 0 whenever it receives a report, including a failing one. To act on the test result in a script, read pass_fail from the output. A timeout exits with code 1, and an interrupt exits with code 130.

> **NOTE:** Waiting for reports and single-PLT deployment require matching PLTcloud server support, which may not yet be enabled in the production environment.

**Use with coding agents**

The -jsonp option prints log lines and the -wait-report summary as JSON objects, for use by coding agents and other tools. See also PLT AI Kit (`ai-kit/`).

**Command-line options**

| Option | Description |
|---|---|
| -a | Auto deploy. Requires -d, or -pltserial and -pltmodel. |
| -clear-plt | Clear the direct release target of the PLT given by -pltserial and -pltmodel. Uploads nothing, and cannot be combined with upload options. |
| -d <UUID> | Deployment group UUID. |
| -ds <TEXT> | Release description. |
| -env <KEY=VALUE> | Add an arbitrary key to the test suite. Can be repeated. |
| -f <GLOB> | Files to upload. |
| -jsonp | Output log lines and the -wait-report summary as JSON objects. |
| -p <UUID> | Project UUID. |
| -pltmodel <MODEL> | Target PLT model. Used with -pltserial. |
| -pltserial <SERIAL> | Target PLT serial number. Used with -pltmodel. |
| -repeat | Repeat runs on deployment. |
| -report-policy <FILE> | Report policy file (JSON or YAML). |
| -report-save-dir <DIR> | Save the test report as JSON in this directory. Requires -wait-report. |
| -t <TOKEN> | API token. Prefer PLTCLOUD_API_TOKEN. |
| -trampoline | Catch runtime panics (default true). |
| -u <MINUTES> | Upload timeout in minutes (default 20). |
| -utcDateVersion | Use the UTC date and time as the release version. |
| -v <VERSION> | Release version. |
| -vvv | Verbose output. |
| -wait-report | Wait for the first new test report on the deployed release, then print it. Requires -a. |
| -wait-timeout <DURATION> | How long -wait-report waits before giving up (default 10m). |
