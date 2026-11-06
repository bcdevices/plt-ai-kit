---
name: plt-setup
description: >-
  Walk a new Blue Clover Devices user step by step from an unboxed PLT to a first test run: hardware and wiring, PLTcloud account, PLT enrollment, project and deployment group, first release, and running the plan. Use when the user wants to get started with a PLT or PLTcloud, or asks what to do first. For reference on an existing setup use plt or plt-cloud; to write a plan use plt-test-plan-builder; for a failing step use plt-debugging.
metadata:
  version: "3.0.1"
---

# PLT Setup

Guide the user from a new PLT to a first test run, following the stages below.
`references/getting-started.md` holds the published guide. Use it for wording
and links.

## How to guide the user

- Give one stage at a time, and wait for the user to confirm its "Done when"
  check before moving on.
- The user does the physical and web console work. You cannot see the PLT or
  their browser, so ask what they see instead of assuming a step worked.
- Keep each message short: what to do, how to tell it worked, and a link.
- Do not invent details. If not covered by the skills or the docs, point to the
  [PLT Support Center](https://plt.bcdevices.com/hc/en-us).

## Find the starting point

Ask these together, then skip the stages that are already done:

1. Which PLT model do you have?
2. Do you already have a PLTcloud account, or are you joining an organization?
3. Is the PLT already enrolled? Do you already have a project and deployment
   group?
4. Are you using the Bento Board example with a Test Agent and Flashr, or your
   own target and programmer?

The guide is written for the PLT-106. For a PLT-300A, use `plt-300a/operation`
for its setup, menus, and running a plan. The PLTcloud stages are the same.

## Stages

### 1. Hardware

1. Assemble the PLT. Connect its USB-C power input to a power supply.
2. Connect Ethernet to a router or switch with DHCP and outbound Internet
   access. Static IP configuration on the PLT is not supported.
3. Wire the station from the Common Wiring table in
   `references/getting-started.md`.
4. Power on the PLT.

Check these two wiring rules with the user:

- Power the Test Agent externally, not from the PLT's USB port.
- Attach only one Flashr to a Test Agent.

**Done when:** the PLT has started and the user can open its menu.

For a restricted network, use the `plt-cloud` skill's `references/connectivity.md`.

### 2. PLTcloud account

Have the user sign up at https://pltcloud.com, confirm their email if they used
email and password, and create an organization. Someone joining an existing
organization signs in with the email their administrator invited and does not
create a new one.

**Done when:** they can see the PLTcloud dashboard.

### 3. Enroll the PLT

1. On the PLT, select **Menu → Enroll**. It shows an enrollment code.
2. In the **PLTs** section of PLTcloud, enter that code as the Activation code
   in the **Enroll PLT** form.

**Done when:** the PLT appears in the **PLTs** list. If enrollment fails, check
the network first.

### 4. Project and deployment group

Have the user create a project, create a deployment group, and assign the PLT
to the group. Steps are in `references/web-console-steps.md`. If an option is
missing, their role may not allow it, so suggest asking their administrator.

**Done when:** the deployment group lists the PLT.

### 5. First release

A release is a test plan plus the files it needs.

**Bento Board example.** With a shell, download the files for the user. Use
these URLs, because a GitHub `blob` page URL returns HTML instead of the file:

```console
curl -fLO https://github.com/bcdevices/bento-zephyr-fw/releases/download/v1.0.1/bento_blinky.hex
curl -fLO https://raw.githubusercontent.com/bcdevices/test-plans/main/bento/bento-flashr-blinky.yaml
```

Without a shell, give the user the links in `references/getting-started.md`.

**Own target or programmer.** Find the target in the `plt` skill's `references/targets.md`,
then write the plan with the `plt-test-plan-builder` skill.

Have the user add a release in the web console with a version that the project
has not used, and include both files.

**Done when:** the release is in the project's release list with both files.

The web console is the default path. Use the `pltutil` skill only if the user
prefers the command line.

### 6. Run the test plan

Confirm before this stage: deploying sends the release to every PLT in the
group, and running it programs the attached board.

1. Deploy the release to the deployment group.
2. On the PLT, select **Menu → Check for Updates → Update**. The PLT downloads
   the release and restarts.
3. Have the user start the test plan on the PLT.
4. Have the user open the test report in PLTcloud.

**Done when:** the report shows PASS. With the Bento example, the board is also
blinking.

| Symptom | Check |
|---|---|
| "No Update Available" | The PLT is in the group, and the release was deployed to that group |
| `usb detect` times out on `6666:8001` | Test Agent USB cable and external power |
| `flashr-flash` step fails | Flashr on the Test Agent, the Tag-Connect cable, and DUT USB power |
| Any other failure, or these checks do not help | The `plt-debugging` skill |

### 7. Next steps

Offer these and let the user choose:

| Goal | Use |
|---|---|
| Write a plan for their own board | the `plt-test-plan-builder` skill |
| Upload and deploy from a terminal | the `pltutil` skill |
| Upload from CI, or run Hardware CI | the `plt-cloud` skill's `references/ci.md` |
| Test report notifications in Slack | the `plt-cloud` skill's `references/reports.md` |

## Where to look

| Need | Read |
|---|---|
| Published guide, PLT-106 setup, Common Wiring table | `references/getting-started.md` |
| Console steps for accounts, enrollment, projects, groups, releases | `references/web-console-steps.md` |
| Bento firmware, shell, wiring, and plans | `references/bento.md` |
| Network and firewall requirements | the `plt-cloud` skill's `references/connectivity.md` |

Page paths in this skill and its references are relative to https://docs.pltcloud.com/ — a page's URL is that base plus its path.
