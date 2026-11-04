# PLTcloud Web Console Steps

Detailed console steps for creating an account, enrolling a PLT, creating a project and deployment group, and creating and deploying a release.

## Create a PLTcloud Account

Source: `pltcloud/webconsole/create/`

- Navigate to https://pltcloud.com
- Authenticate with either Email/Password, Github, Gmail, or Microsoft Account.

If you are joining an organization be sure to use the same Email address that your PLTcloud administrator used. If you use a Github or Microsoft account PLTcloud will use the Email address associated with those accounts. If you do not know which email to use, contact your administrator.

If you are not joining an organization, you will be asked to create one after logging in.

**Sign-Up (Email/Password)**

To create a new Email/Password account for PLTcloud, click on the Sign up link in the Login dialog, enter your Email and Password, and click on the Continue button.

**Email Confirmation**

You'll need to confirm your Email address by clicking on the link that is sent in the Email address provided during sign up.

**Create your Organization**

- Enter Name, Owner Email, and URL host prefix
- Click the Create button
- The PLTcloud Dashboard will open.

From the Dashboard, you can use all the PLTcloud capabilities

## Adding a PLT

Source: `pltcloud/webconsole/plt/add/`

On the PLT UI panel, press the Menu button to enter the PLT Menu, and select Enroll.

The PLT will show an enrollment code on the OLED display.

You can enroll your PLT under the PLTs section of the PLTcloud website. On the PLTcloud website, use this code as the Activation code in the Enroll PLT form.

You can then set the PLT to a specific deployment group by clicking on on SET DEPLOYMENT GROUP.

## Create Project

Source: `pltcloud/webconsole/project/create/`

You can create a project or go through the list of projects already created by clicking on the 3 dots in the top app bar:

- Click Add Project
- Enter the name and description of the project in their respective fields.
- Click the Create button.

## Deployment Groups

Source: `pltcloud/webconsole/plt/dpg/`

PLTs are organized into Deployment Groups.

These are groups of PLTs that are meant to run the same set of tests. For example, you can have a group of PLTs that you will want to use for In-Circuit (ICT) testing and another group of PLTs that you will want to use for Final Assembly, Test & Pack-out (FATP) testing.

New Deployment Groups can be created in the PLTs view.

You can then fill out the name and the description of the group.

**Adding a Deployment Group**

- Select PLTs from the left-hand menu and then click the Add Deployment Group button.
- On the New Deployment Group page, fill out the Name and Description in their respective fields.
- Click the Create button.
- Select PLTs from the left-hand menu
- In the top menu, click List.
- Click the "eye" icon of the PLT you want to add to the Deployment Group.
- On the PLT Details (`pltcloud/webconsole/plt/detail/`) page, click the Set Deployment Group button.
- In the Set Deployment page, select the Deployment Group.
- Click the Set Deployment Group button to save.

**Deployment Group Details**

The Deployment Group Details page has the following fields:

- Name - Name of the Deployment Group
- Description (Optional) - The description of the Deployment Group
- Project - The project the group is associated with
- Release - The release that is currently deployed to the group
- PLTs - The lists of all the PLT currently in the group

Not bundled; see Update Deployment Settings (`pltcloud/webconsole/plt/dpg/#update-deployment-settings`), Delete Deployment Group (`pltcloud/webconsole/plt/dpg/#delete-deployment-group`).

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

Not bundled; see Archive a Release (`pltcloud/webconsole/project/releases/#archive-a-release`), Restore an Archived Release (`pltcloud/webconsole/project/releases/#restore-an-archived-release`).
