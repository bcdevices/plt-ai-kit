# PLTcloud Web Console — Projects, Releases and Reports

Creating and configuring projects in the PLTcloud web console: files, releases, project settings (serial number allocation, webhooks, debug keys) and browsing test reports.

## Manage Projects

Source: `pltcloud/webconsole/project/`

The list of projects allows you to switch between them and to select the project you want to work on in PLTcloud.

## Create Project

Source: `pltcloud/webconsole/project/create/`

You can create a project or go through the list of projects already created by clicking on the 3 dots in the top app bar:

- Click Add Project
- Enter the name and description of the project in their respective fields.
- Click the Create button.

## Change Active Project

Source: `pltcloud/webconsole/project/select/`

On the Project List Page, the active project is marked with a Checkmark icon in the Active column

Click on the Select Project (compass) icon for the project you want to activate.

## Project Details

Source: `pltcloud/webconsole/project/detail/`

The Project Detail view is accessible from the Project menu item on the project drop-down in the top banner.

In addition to basic information about your project, more details are shown here:

- Project UUID
- pltOS version constraints

Click on the Settings button to change these settings.

## Files

Source: `pltcloud/webconsole/project/files/`

Releases are made up of Files. Each Release must include a Test Plan definition (.yaml), in addition to any firmware images (.hex, .elf, .bin) or other files needed during execution of the test plan.

For example, to test and program an STM IoT demo board, we need to upload the firmware and the test plan. The firmware can be uploaded as an ELF file, for example, STM32L4_IOT_HR.elf. The test plan is supplied as a YAML file, for example, suite-stm32l4DK-IOT-BLE.yaml:

*``suite-stm32l4DK-IOT-BLE.yaml`` YAML test plan*

```yaml
title: "Erase, Program, Identify, Test"
suite:
- ident: ICT-T1
  title: Erase stm32l4_DevKit with USB ST-Link
  steps:
  - command: erase stm32l4_STLink
- ident: ICT-T2
  title: Program STM32L4-IOT-BLE stm32l4_DevKit with USB ST-Link
  steps:
  - command: program stm32l4_STLink none,STM32L4_IOT_HR.elf,none
- ident: ICT-T3
  title: Identify DUT
  steps:
  - command: identify stm32l4_IoT_STLink
- ident: ICT-T4
  title: BLE discovery
  steps:
  - command: bledis %BLEMAC% 30  # Wait up to 30 seconds for BLE discovery to complete
```

**Add Files**

- Select Files from the left-hand menu.
- Click Add File.
- Click the upload icon and navigate to the file you want to add.
- Click the Open button of the file dialog.
- Optionally, add a description of the file.
- Click the Submit button.

Repeat this until you have added all the files required for the test suite.

> **NOTE:** If you upload a file with the same name and description as an existing active file, the active file will be automatically archived and the new file will become active.

**View Files**

Active Files:

- Click the PLT on the left-hand menu, and the active Files list will appear.

Archived Files:

- On the File List page, click on the down carrot next to the Show Active
- Click the drop-down menu that appears and select Archived
- Click the Update button

All Files:

- On the File List page, click on the down carrot next to the “All”
- Click the drop-down menu that appears and select Archived
- Click the Update button

**File Detail**

The File Detail page can be accessed by clicking the Details (stack boxes) icon on the File List page.

The File Detail page shows the following fields:

- Meta-information section - Shows information on about the file, including name, size, and encoding,
- Preview section - shows a preview of the file contents. Binary will be displayed as hex

**Archiving Files**

- On the Files List page, click the Archive icon (down arrow box) for the file you want to remove.

> **NOTE:** Files cannot be deleted, only archived.

**Restoring a File**

- View all archived files (see above)
- Click the Restore icon (Trashcan) of the file you want to unarchive. That file will appear now in the active file list.

**Download a File**

Option 1:

- On the Files List page, click the Download icon (down arrow cloud) for the file you want to download.

Option 2:

- On the File Detail page, click the Download icon (down arrow cloud) for the file you want to download.

## Releases

Source: `pltcloud/webconsole/project/releases/`

The Releases page shows the releases that have been created in a Project.

Files may be uploaded and managed directly from the release creation or editing page. Previously added files are also available for inclusion.

You can create multiple releases per project.

For example, to create a new release, you would fill the version and description of cases of your release, and select the files (firmware images and YAML files) you want to be part of your release.

**View Active Releases**

- Click on the Release button on the left-hand menu. The Release List page will appear

**View Archived Releases**

- On the :doc`File List <files>` page, click on the down carrot next to the “Show Active”
- Click the drop-down menu that appears and select Archived
- Click the Update button

**Create a Release**

- Select Releases from the left-hand menu and then click Add Release.
- Enter the version.
- Optionally, add a description.
- Check the boxes of the Files you want to add to this Release.
- If needed, click Add Files to add a new File directly to the Release.
- Click the Add button to save the Release.

**Release Details Page**

- Click on the Details (single block) icon. The Release Details will open.

The Release Details page has the following information:

- Version - The name of the version
- Description - An optional description of the release
- Active - The status of the release. The options are Active or Archived. Only Active Releases are deployable. Archived Release must be restored before they can be deployed
- Files - The files included the release
- Deployment Groups - All the deployment groups that the release has deployed to.

**Deploy a Release**

Option 1: Deploying the current release:

- On the Deployment Groups (`pltcloud/webconsole/plt/dpg/`) page, click the Deploy button
- Click the Deploy button
- Click the Dismiss button

Option 2: Deploying a new release

- On the Release List page, click the Deploy button
- From the listboxes, select the Release and the Deployment Group
- Click the Select button
- Click the Deploy button to confirm the deployment
- Click the Dismiss button. The Deployment Group Details (`pltcloud/webconsole/plt/dpg/`) page will appear

Option 3: Deploy a specific new release

- Click the Release icon (Down arrow)
- From the listboxes select the Deployment Group, Click the Select button
- Click the Deploy button to confirm the deployment
- Click the Dismiss button. The Deployment Groups (`pltcloud/webconsole/plt/dpg/`) page will appear.

The Release is now staged for download.

- On the PLT, press the #4 (Main Menu) button and then scroll to Check for Updates.
- Press the #3 (Enter) button
- The PLT will recognize the staged Release and display “Update Available”.
- Click the #2 (Update) button. The new deployment will download, and the PLT will restart.

> **NOTE:** If the PLT does not find the new Release, it will display “No Update Available”. If that happens, review the deployment process to confirm it was correct.

**Archive a Release**

Option 1:

- Click the Archive (box down arrow) icon on the Release List page
- Click the Archive button to confirm
- Click the Dismiss button. The Release Details page will reappear, but now the Active field will show “Archived”

Option 2:

- On the Release Detail page, click the Archive icon (box down arrow)
- Click the Archive button to confirm
- Click the Dismiss button. The Release Details page will reappear, but now the Active field will show “Archived”

**Restore an Archived Release**

View the archived releases:

- Click the Restore (trashcan) icon on the Release List page or the Restore button on the Release Detail page
- Click the Restore button
- Click the Dismiss button. The Release Details page will appear, but now the Active field will show “Active”

## Project Settings

Source: `pltcloud/webconsole/project/settings/`

## Edit Settings

Source: `pltcloud/webconsole/project/settings/basic/`

**Basic Setttings**

The Project Settings page can be accessed by clicking the Settings button on the Project Details (`pltcloud/webconsole/project/detail/`) view.

It can be used to modify basic project settings:

- Project Name and Description
- pltOS version constraints
- Webhook configuration

**pltOS Version**

The default version is “Latest”. When "Latest" is set, the PLT application will update its OS during the next deployment from PLTcloud.

To maintain the same version, click the pltOS dropdown menu and select the version you want to keep.

**Store-and-Forward**

If the PLT cannot submit the test report to PLTcloud at the end of the test, it can store the report locally for later re-submission.

Enable the checkbox to allow offline storage of test reports for future submission.

**Monotonic Serial Numbers**

The Monotonic Serial Number section has the following fields:

- Start Value - First serial number
- End Value - Last serial number
- Next Value - Increment between serial numbers
- Length - Number of digits

**Serial Number Webhook API**

To perform number allocation through an external Serial Number Webhook API (`pltcloud/webhook-api/`) endpoint, select the Webhook Serial Number Allocation scheme.

Specify the API endpoint:

- WebHook URL: URL of the API endpoint accepting HTTP POST requests from PLTcloud.
- Authentication Token: Hex-encoded token, used to sign the JSON payload sent to the provided URL

**Test Webhook**

- In the Webhook Serial Number Details section, Adjust the Sample Webhook Payload as needed
- Click the Test button.

PLTcloud will send the sample payload to the URL you specify.

## Debug Keys

Source: `pltcloud/webconsole/project/settings/debugkeys/`

The Debug Keys page allows users with the Administrator role to manager public SSH keys to control local access to PLTs while in Debug Mode.

The SSH keys for which public keys are attached for a project can be used to upload test plan YAML files and other artifacts using SFTP.

Once a debug SSH (.pub) key is set on a project that is deployed to a PLT, the Debug Mode can be activated by an Administrator from the Reset section of the Manage PLTs (`pltcloud/webconsole/plt/`) view in PLTcloud:

- Reset PLT in Debug Mode
- Wait for PLT to restart in Debug Mode

While the PLT is in Debug Mode, an SFTP client (such as sftp or WinSCP) can be used to upload release files.

*Example :program:`sftp` session with PLT in *Debug Mode**

```console
$ sftp debug@<PLT IP>
debug@<PLT_IP>$ put myTestPlan.yaml
debug@<PLT_IP>$ put firmware.hex
debug@<PLT_IP>$ quit
```

> **NOTE:** After adding or modifying test plan YAML files, use the on-screen menu to select "Restart" to ensure the new plans are available.

## Manage Reports

Source: `pltcloud/webconsole/report/`

When a test is executed on a PLT, the report will be automatically generated and be available under the Reports section.

Reports are listed in chronological order, and they will be bold-ed if they were generated less than 5 minutes ago.

> **IMPORTANT:** While test reports can be accessed from the web administration console, PLTcloud itself is not meant to be used as a Data Warehouse.We recommend setting up a Report Connector (`pltcloud/report-connector/`) to have PLTcloud act as a data source for a data pipeline (or ETL tool) or storage bucket of your choice.
