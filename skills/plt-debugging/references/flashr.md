# Flashr and Test Agent Programming Failures

Both commands report their result as an exit status, and a non-zero status
fails the `agentExec` step. Start from the status and the command's console
output.

## flashr-flash

`flashr-flash <target> <firmwareFile> [<offset>]` wraps OpenOCD: CMSIS-DAP
adapter, SWD transport, 4000 kHz, then
`program <firmwareFile> [<offset>] verify reset exit`.

| Symptom | Cause | Remedy |
|---|---|---|
| The step times out after about a second | `agentExec` defaults to a 1000 ms timeout, shorter than a program-and-verify cycle. | Set `timeout:` on the step (the documented examples use `2m`). |
| Exit status `1`, and the output lists the available targets | `<target>` is not the name of a `target/<target>.cfg` file in the OpenOCD script directory. It is an OpenOCD name (`nrf52`, `stm32f4x`), not a PLT `program` target. | Pick the name from the printed list. For a target OpenOCD does not ship, send a configuration with `agentCfg` and set `OPENOCD_SCRIPTS` to its directory. |
| Exit status `1`, target name is valid | The firmware file does not exist at the given path. | List the image under `with:` in the `agentCfg` step and reference it as `/run/pltagent/mnt/<file>`. |
| Exit status `2` | Usage error: wrong number of arguments. A `.bin` image was given without an offset, or an offset was given for a `.hex` or `.elf`. | Add the flash address for `.bin` (for example `0x08000000`); remove it for `.hex` and `.elf`. |
| Any other non-zero status | OpenOCD's own status: the probe or the target cannot be reached, or programming or verification failed. | Run the connection check below to separate a probe or wiring problem from an image problem. |
| `flashr-flash` is not found | The command was added in agentOS v1.6.2. | Update agentOS. |

When OpenOCD cannot reach the probe or the target, check the documented
limits first:

- **One Flashr per Test Agent.** There is no option to select a probe.
- **SWD only.** JTAG targets are not supported.
- **Fixed 4000 kHz adapter speed.** A target that needs a different speed
  must be programmed by running `openocd` directly.
- **Target support.** OpenOCD 0.12 does not ship a configuration for some
  targets, the RP2350 among them.

Target power and SWD wiring are not covered on these pages; check them as
for any SWD programmer.

### Connection check

Run OpenOCD directly on the Test Agent with `init` and `exit` only. A
successful connect reads the target's `DPIDR` and examines its cores,
which rules out the probe, the wiring and the target name before the
image is involved. Substitute the target name:

```yaml
- command: agentExec AGENT "openocd -f interface/cmsis-dap.cfg -c 'transport select swd' -c 'adapter speed 4000' -f target/nrf52.cfg -c init -c exit"
  timeout: 30s
```

Lower the `adapter speed` value here to test whether the fixed 4000 kHz is
the problem. This is the Flashr equivalent of the `identify` diagnostic
used with the PLT's built-in programming interfaces.

## flashr-update

`flashr-update` takes no arguments and wraps `mcumgr`. It uploads the first
file matching `/var/lib/pltagent/per401-fw-*`, then
`/run/pltagent/mnt/per401-fw-*`.

| Symptom | Cause | Remedy |
|---|---|---|
| Exit status `1` | No firmware image was found. | Send the signed image, named `per401-fw-v<version>-slot0.signed.bin`, with `agentCfg`. |
| The wrong image was uploaded | Any file whose name starts with `per401-fw-` matches and only the first match is used; `/var/lib/pltagent` is searched before the RAMDISK. | Send exactly one such file, and check for one already in `/var/lib/pltagent`. |
| Status `0`, but the Flashr still runs the old firmware | The upload only writes the alternate firmware slot. | Mark the image for use and restart the Flashr: `mcumgr ... image list`, `image test <hash>`, `reset` (commands in the `plt` skill's `references/flashr.md`). |
| The Flashr reverts after a restart | The new firmware did not confirm itself, so the bootloader went back to the previous image. | Check that the image is the signed application image for the PER-401. |
| Any other non-zero status | `mcumgr`'s own status: the Flashr cannot be reached or the upload failed. | Check that a single Flashr is attached and that its serial link `/dev/flashr-<serial>-serial` exists. |
| `flashr-update` is not found | The command was added in agentOS v2.0.2. | Update agentOS. |

## On the Test Agent

- Commands run as the `pltagent` user; `sudo` works without a password.
- The root file system is read-only. Write to `/tmp` or to the RAMDISK at
  `/run/pltagent/mnt`.
- The agentOS version is reported to the PLT with the test results
  (`DISTRO_VERSION`) and, from agentOS v2.0.2, in the USB product string.
  Compare it with `references/version-gating.md`.

## References

The full pages for the commands below are bundled in the
`plt` skill's `references/flashr.md`, and the Test Agent pages in the `plt`
skill's `references/test-agent.md`.
