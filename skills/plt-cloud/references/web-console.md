# PLTcloud Web Console — Organizations, Users and PLTs

Administering PLTcloud at https://pltcloud.com/: accounts, organizations, users, PLTs and deployment groups. Projects, releases and project settings are in `references/projects.md`.

## Administration

Source: `pltcloud/webconsole/`

The PLTcloud web console at https://pltcloud.com/ can be used to manage your PLTs and device test projects from a web browser.

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

## Manage Organizations

Source: `pltcloud/webconsole/org/`

You can see a list of all the organizations you belong to by clicking on the Organization menu and then select Manage Organizations.

**View Organization**

Click on the Organization menu and then click Manage Organizations. The Organization list will come up, showing all the organizations you belong to.

**Add Users**

- In the left-hand menu, click on Users.
- Click Add User.
- Enter the email and in the Teams section set their permission level.
- Click Add twice and the user will be added to their organization.
- The new member can now log in to your organization using that same email address.

> **NOTE:** If a user attempts to log in using Github, PLTcloud will use the email address found within that profile.

## Organization Details

Source: `pltcloud/webconsole/org/detail/`

The Organization Details page has the following fields:

- Name - The name of the organization.
- Owner - The User who has Owner permissions.
- Administrators - the Users who have Administrator permissions
- Managers - the User who have Manager permissions
- Viewers - the Users who have View permissions
- Limits - The maximum allowed projects, users, and deployment groups. If any of these limits are exceeded, you will see a warning to upgrade your subscription, and functionality will be degraded.

**Change Information (Administrator)**

- Navigate to the Organization Details page
- Click the Edit button next to the Name field.
- Update Name or Host Name fields as needed
- Click the Change button
- Click the Dismiss button to return to the Organization Details page.

> **NOTE:** When changing Host Name, you may have to log in again to be able to use the new host name.

**Change Owner (Owner)**

> **NOTE:** Only Administrators are eligible to become Owner

- Navigate to the Organization Details page
- Click the Change Owner button
- Select the User you want to transfer ownership to
- Click the Set Owner button
- Reload the browser page to see the change

**Delete Organization**

- Navigate to the Organization Details page
- Click the Settings button
- Enter the new name in the Name field
- Click the Delete Organization button
- Click the Delete button to confirm

## Manage Users

Source: `pltcloud/webconsole/user/`

**View Users**

- From the left-hand menu, click the Users button. The User list page will appear

The User table has the following fields:

- Email - the email used for logging into the organization
- Name - the name of the User
- Roles - the permission set that the User has

**Change User Permissions (Administrator)**

- From the Manage Profile (`pltcloud/webconsole/user/profile/`) page, Click the Change Team button
- Select the new permission set for that user
- Click the Select button
- Click the Change button
- Click the Dismiss button

**Remove User (Administrator)**

Method 1:

- In the User List page, Click the Remove User button
- Select the User you want to remove
- Click the Remove button to confirm
- Click the Dismiss button.

Method 2:

- From the Manage Profile (`pltcloud/webconsole/user/profile/`) page, click the Remove User button
- Click the Remove button to confirm
- Click the Dismiss button.

Method 3:

- In the Profile Settings (`pltcloud/webconsole/user/profile/`) page, click the Remove User From Organization button
- Click the Remove button to confirm
- Click the Dismiss button

## Manage Profile

Source: `pltcloud/webconsole/user/profile/`

**View Profile**

- Click the Account Menu below your profile image
- Select the Profile option. The profile details page will open

The Profile page has the following fields

- Picture: This is pulled in from the account you logged into PLTcloud with. So if you logged with a Google Account it will show your Google account image.
- Email - the email you logged in with
- Name - Your username
- Time Zone - Sets the report timestamp
- Roles - The roles your profile has
- Teams - Your permission level

**Change User Information**

- From the Profile page, click the Settings button
- Update the name and time zone as needed
- Click the Change button
- Clicking the Dismiss button will take you back the to Profile details page

**Leave Organization**

- From the Profile page, click the Leave Organization button
- Click the Remove button
- Click the Dismiss button

## Manage PLTs

Source: `pltcloud/webconsole/plt/`

You can see a list of all PLTs by pressing LIST from the PLTs view:

Or in grouped by deployment group by clicking on on DEPLOYMENT GROUPS.

## Adding a PLT

Source: `pltcloud/webconsole/plt/add/`

On the PLT UI panel, press the Menu button to enter the PLT Menu, and select Enroll.

The PLT will show an enrollment code on the OLED display.

You can enroll your PLT under the PLTs section of the PLTcloud website. On the PLTcloud website, use this code as the Activation code in the Enroll PLT form.

You can then set the PLT to a specific deployment group by clicking on on SET DEPLOYMENT GROUP.

## PLT Details

Source: `pltcloud/webconsole/plt/detail/`

The PLT Details page has the following fields:

- Serial Number - PLT Serial Number
- Model - PLT Model
- Name - PLT Name
- IP - The last IP address of PLT
- Connection - The status of that connection
- Deployment Group - The deployment group the PLT is part of
- Project - The project the PLT is part of
- Current Release - The release that is downloaded to the PLT
- Available Release - The release that is staged for download

**Change PLT Name**

- On the PLT Details page, click the Settings button
- Enter the new name in the Name field
- Click the Change button
- Click the Dismiss button. You will be taken back to the PLT Details page

**Change Deployment Group**

- On the PLT Details page, click the Set Deployment Group button
- In the listbox, select the new deployment group
- Click the Set Deployment Group button. The PLT will be moved to the new deployment group, and you will be taken back to the PLT Details page
- Click on the PLT button on the side menu to view the new deployment group

**Reset PLT**

> **NOTE:** This functionality is only available if a user belongs to the Administrator or Manager teams.

- On the PLT Details page, click the Reset button
- On the reset page, there are three options

   - Restart - Reboots that PLT remotely.
   - Restart (Debug Mode) - Reboots the PLT into Debug Mode which allows connecting to the PLT over the local network. This option will only appear if there is an active debug key uploaded to the project.
   - Reset deployment - Clear PLT deployment

**Remove PLT**

- On the PLT Details page, click the Remove PLT button.
- Click the Remove button to confirm the change.

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

**Update Deployment Settings**

- On the Deployment Group Details page, click the Settings button
- Update the Name and Description fields as desired
- Click the Change button
- Click the Dismiss button

**Delete Deployment Group**

- On the Deployment Group Details page, click the Delete button.
- Click the Delete button to confirm the change.
- Click the Dismiss button.
