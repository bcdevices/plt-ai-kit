# PLTcloud Reports and Notifications

Getting test reports out of PLTcloud: the Report Connector, its project settings, and the Slack app.

## Report Connector

Source: `pltcloud/report-connector/`

The Report Connector allows setting up PLTcloud to act as a data source for analysis and archivation.

**Supported Destinations**

At this point, PLTcloud supports Amazon S3 buckets as Report Destinations.

Data will not begin replication until you've successfully connected a destination to a project, and at least one test plan is executed for the project.

As part of the Enterprise plan, additional destinations can be supported.

> **TIP:** The S3 bucket can be hooking up to various 3rd-party data pipeline (or ETL) tools and services, consolidating data from various sources into a single location.

**Amazon S3 Destination**

**Prerequisites**

- An Amazon Web Services (AWS) account. Signing up is free - go to https://aws.amazon.com to create an account.
- Permissions to create and manage S3 buckets in AWS.

**Step 1: Create an Amazon S3 Bucket**

- Sign into AWS Console
- Click Services on the top-left corner
- Select S3 under the Storage section
- Click the + Create Bucket button

- On the first screen, Name and region, complete the following:

   - Bucket name: Enter a unique DNS-compliant name for the bucket.
   - Region: Select the region you want the bucket to be located in.

- Click Next
- On the Configure Options screen, leave all default settings as-is, and click Next
- On the Set Permissions screen, choose Block all public access and click Next
- On the Review screen, verify all settings and click the Create bucket button.

**Step 2: Set the Report Connector Destination in PLTcloud**

- If you aren't signed into your PLTcloud account, sign in first.
- Select the Project for which you'd like to set a Report Connector destination.
- Navigate to Project Settings (`pltcloud/webconsole/project/settings/`)
- Click on the Report Connector button
- Click on the + Add Destination button
- Fill in the fields as below:

   - S3 Bucket: Fill in the name of your S3 bucket (without any s3:// prefix)
   - Region: Fill in the AWS region of your S3 bucket
   - Report Prefix: Optionally fill in a prefix (folder name) for the reports within the bucket

- Select either csv or json for CSV or JSON reports

**Step 3: Grant bucket access**

- Navigate to the Report Connector Destination detail page.
- Expand the S3 Bucket Policy tab
- Copy the S3 Bucket Policy JSON
- Sign into AWS in another tab, if not currently logged in.
- In AWS Console, navigate to the Permissions tab of the S3 bucket that serves as the Report Connector Destination.
- In the Permissions tab, click the Bucket Policy button.
- In the Bucket Policy editor, paste the bucket policy code from PLTcloud.
- Click the Save button when finished.

At this point, test reports should start to appear in the S3 bucket a few seconds after a test plan associated with the Project is executed on a PLT.

## Report Connector Settings

Source: `pltcloud/webconsole/project/settings/report-connector/`

The Report Connector Settings page allows users with the Administrator role to manager Report Connector settings.

## PLTcloud Slack App

Source: `slack/`

First we invented cloud native hardware test automation, now we’re bringing it to Slack!

The PLTcloud app lets the whole team see test report notifications, without having to log into PLTcloud.

PLTcloud is a cloud-native backend for Production Line Tools (PLTs), automating both programming and testing IoT devices during manufacturing.

Use the PLTcloud app to

1. list your projects,
2. subscribe Slack channels to report notifications, and
3. view test report notifications in real time!

|  |  |  |

**Installation**

To install the PLTcloud Slack App, first install it to your workspace by clicking on the Add to Slack button below.

Add to Slack (https://slack.pltcloud.com/install)

Once the PLTcloud Slack App is installed in your Slack Workspace, type /pltcloud in any channel to install the PLTcloud Slack App in that channel.

The PLTcloud Slack app will respond with a notification stating "To use /pltcloud, install PLTcloud in this channel", with an Install button. Click on the Install button to install PLTcloud in the channel.

After installing this plug-in into a channel, use /pltcloud projects to list the PLTcloud projects you're a member of. Click on the Subscribe button next to the Project for which you'd like to receive test report notifications in the current channel.

**PLTcloud App Commands**

```
/pltcloud help
```

Show online help

```
/pltcloud projects
```

Lists the PLTcloud projects you're a member of. Next to each listed project is a Subscribe or Unsubscribe button.

Click on the Subscribe button to start receiving test report notifications for this project in the current Slack channel.

Click on the Unsubscribe button to stop receiving such notifications on the current channel.

```
/pltcloud subscriptions
```

List subscriptions of PLTcloud projects in the current Slack channel.

Next to each listed project is an Unsubscribe button. Click on the Unsubscribe button to stop receiving test report notifications for that project on the current channel.
