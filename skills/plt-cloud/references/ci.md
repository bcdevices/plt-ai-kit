# PLTcloud Continuous Integration

Uploading releases from a CI pipeline with the PLTcloud client, and running hardware-in-the-loop tests with the PLT Hardware CI GitHub App and GitHub Action.

## Continuous Integration

Source: `pltcloud/continuous-integration/`

PLTcloud allows for uploading a release utilizing a command line client. This client can be included in a CI pipeline in order to automatically deploy a firmware build to PLTcloud.

**Supported Environments**

The PLTcloud client is distributed as a Debian package and should work on Debian and other distributions supporting .deb files.

The PLTcloud CLI has been tested with Travis CI and GitHub Actions.

Other CI tools can be utilized as long as they run a supported OS and support the installation of custom packages.

**Usage**

```
pltcloud [OPTIONS...] -t <TOKEN> -v <VERSION> -p <UUID> -f <GLOB>

-t <TOKEN>
        PLTcloud API Release Token
-v <VERSION>
        Release version
-p <UUID>
        Project UUID
-f <GLOB>
        Files
-vvv
        Verbose output
```

Files can be specified with patterns such as: **/prefix*, grandparent/**/child?, **/parent/*, or even just ** (which will include all files and directories recursively).

Not bundled; see Example: Travis CI integration (`pltcloud/continuous-integration/#example-travis-ci-integration`).

**Example: GitHub Actions**

**Prerequisites**

- A GitHub account and repository containing DUT firmware image and test plans
- Access to GitHub Actions
- A PLTcloud organization, user and project

**Step 1: Validate firmware build and test plans**

In order to upload a release, the PLT test plan, and any associated assets such as DUT firmware must be available in a directory.

Setup a GitHub Action workflow to build the firmware and copy test plans to a known directory.

For example, the Zephyr Action (https://github.com/bcdevices/ly10-zephyr-fw/tree/main/.github/actions/action-zephyr)

in the Zephyr firmware for demo board project (https://github.com/bcdevices/ly10-zephyr-fw/) is used to build the firmware files and copy the test suites to a dist/ directory.

**Step 2: Configure project and token secrets**

- Log in to PLTcloud and select the Project menu item from the project drop-down in the top banner.
- Copy the UUID from the Project Details (`pltcloud/webconsole/project/detail/`) page and a secret named PROJECT_UUID in your GitHub project.
- Select API Tokens from the drop-down menu under the user menu in PLTcloud
- Select Add Release Token, login and copy the Release Upload Token
- Add the release token to GitHub secrets and name it API_TOKEN

**Step 3: Update the Workflow to deploy to PLTcloud**

- Add a step in .github/workflows/main.yml beneath step that builds the firmware.

   ```yaml
   - uses: bcdevices/pltcloud-action@v1.2.1
     if: contains(github.ref, 'tags')
     with:
       API_TOKEN: ${{ secrets.API_TOKEN }}
       PROJECT_UUID: ${{ secrets.PROJECT_UUID }}
       FILES: "./dist/*demo*"
       VERSION: ${{ github.ref }}
   ```

## PLT Hardware CI

Source: `pltcloud/hardware-ci/`

The PLT Hardware CI GitHub App enables Continuous Integration (CI) testing, automating the production-level testing of firmware on target hardware, using the PLT.

**PLTcloud GitHub Action**

- PLTcloud GitHub Action (https://github.com/bcdevices/pltcloud-action)

   Deploys firmware and test plan build artifacts to PLTs.

**PLT Hardware CI GitHub App**

- PLT Hardware CI GitHub App (https://github.com/apps/plt-hardware-ci)

   Reports PLT test results back to GitHub Actions.

**Setup**

**Prequisites**

- A GitHub repository containing DUT firmware images and test plans
- A PLTcloud organization, user and project
- An enrolled PLT associated with a deployment group that will be used for CI testing

**Step 1: Validate firmware build and test plans**

In order to upload a release, the PLT test plan, and any associated assets such as DUT firmware must be available in a directory.

Your existing GitHub Action workflow should build the firmware and copy test plans to a known directory.

For example, the workflow (https://github.com/bcdevices/ly10-zephyr-fw/blob/main/.github/workflows/main.yml) in the Zephyr firmware for demo board project (https://github.com/bcdevices/ly10-zephyr-fw/) uses the /.github/actions/action-zephyr action to build the firmware files and copy the test plans to a dist/ directory.

**Step 2: Configure project and token secrets**

- Log in to PLTcloud and select the Project menu item from the project drop-down in the top banner.
- Copy the UUID from the Project Details (`pltcloud/webconsole/project/detail/`) and add a secret named PROJECT_UUID in your GitHub project.
- Select API Tokens from the drop-down menu under the user menu in PLTcloud
- Select Add Release Token, login and copy the Release Upload Token
- Add the release token to GitHub secrets and name it API_TOKEN
- Select the PLTs.
- Click on the deployment group name that you want to use for Hardware CI (not the PLT name).
- Copy the UUID from the deployment group detail page and add a secret named DEPLOYMENT_GROUP_UUID in your GitHub project.

**External References**

- Encrypted Secrets (https://docs.github.com/en/actions/security-guides/encrypted-secrets)

**Step 3: Add PLT Hardware CI to repository**

To enable the creation of a GitHub check runs, add the PLT Hardware CI App (https://github.com/apps/plt-hardware-ci).

This will allow the results from the execution of the PLT test plan to result statuses that are visible within pull requests on GitHub.

Please follow the steps below:

- Select the organization where you want to install the PLT Hardware CI App.
- Choose the option Only Select Repositories and select the desired GitHub repositories.
- Select Save

**Step 4: Add PLTcloud deployment to existing action**

- Add a step in the .github/workflows/main.yml workflow file, after the steps that build your firmware.

   ```yaml
   - name: PLTcloud release
     uses: bcdevices/pltcloud-action@v1.2.1
     with:
       FILES: ./dist/*
       API_TOKEN: ${{ secrets.API_TOKEN }}
       PROJECT_UUID: ${{ secrets.PROJECT_UUID }}
       DEPLOYMENT_GROUP_UUID: ${{ secrets.DEPLOYMENT_GROUP_UUID }}
       AUTO_DEPLOY: true
       VERSION: ${{ github.ref }}
   ```

**Step 5: Add Report Connector to PLTcloud Project**

The Report Connector is used to update the status of the GitHub check run after your test plan has been executed.

- Log in to PLTcloud and select the Project menu item on the left side of the screen.
- Click on the name of the relevant project.
- Click the Report Connector button at the top of the page.
- Click the Add Destination button at the top of the page.
- Enter pltcloud-ci-reports-production for S3 Bucket.
- Enter us-west-2 for Region.
- Select json and Add.
