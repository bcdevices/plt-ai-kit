# pltutil Release Notes

Changes per version. Use these when an installed pltutil rejects an option or behaves differently than documented.

## pltutil v0.7

Source: `releases/pltutil/0.7/`

**pltutil v0.7.5**

Released 2026-10-30.

Added:

- -pltserial and -pltmodel with -a deploy the release to one PLT instead of a deployment group. Both options must be given together, and need -f and -a.
- -clear-plt clears the direct release target of the PLT given by -pltserial and -pltmodel, so it falls back to its deployment group release. This can downgrade the PLT to an older group release. It uploads nothing.

Changed:

- -pltserial is zero-padded to 5 digits, so -pltserial 6 targets the PLT with serial number 00006.
- -pltserial and -pltmodel no longer require -wait-report. They still limit the reports that -wait-report waits for.
- -a is rejected before any network call unless it is given with -d, or with -pltserial and -pltmodel.
- -wait-report is now a flag that turns the wait on, and no longer takes a duration. The deadline moved to -wait-timeout (default 10 minutes).
- -wait-report long-polls the reports API instead of polling every 30 seconds, and starts before the deploy call, so a report that arrives right after deploy is caught.

Removed:

- -report-poll, which is no longer needed now that the wait is a long poll.

**pltutil v0.7.4**

Released 2026-10-28.

Added:

- -jsonp prints log lines and the -wait-report summary as JSON objects, for integration with coding agents and other tools.

Changed:

- Renamed the CLI tool to pltutil (was pltcloud). Update scripts and CI pipelines to call pltutil and install the pltutil package. See Renamed from pltcloud.
- Renamed the -model option to -pltmodel and the -serial option to -pltserial.

**pltutil v0.7.3**

Released 2026-10-26.

Added:

- -wait-report waits for the first new test report on the release, then prints it and exits.
- -report-save-dir saves the report as JSON.

**pltutil v0.7.2**

Released 2026-10-23.

Added:

- Release binaries for Linux, Windows, and macOS.
- Read the API token from PLTCLOUD_API_TOKEN when -t is not provided.

Changed:

- Upgrade the Go toolchain from 1.23 to 1.26.
- Upgrade golang.org/x/oauth2 from v0.24.0 to v0.37.0.

**pltutil v0.7.1**

Released 2025-06-05.

Added:

- -report-policy specifies report controls in a JSON or YAML file, and includes the policy file in uploads.

**pltutil v0.7.0**

Released 2025-04-04.

Added:

- -repeat deploys a release to a deployment group and automatically repeats test execution until failure.
