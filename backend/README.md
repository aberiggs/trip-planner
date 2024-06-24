# Backend

## Overview
This project uses a build script (build.sh) to manage various tasks such as building, testing, formatting code, and deploying to AWS. If no profile is specified, the default profile will be used.

## Commands

### Run Project Locally
This command builds the project, runs all test cases, and starts the project locally.

```bash
./build.sh -p [your profile name] start
```

### Format Code
This command reformats the code.

```bash
./build.sh -p [your profile name] format
```

### Test Project
This command builds the project and runs all test cases.

```bash
./build.sh -p [your profile name] test
```

### Deploy to AWS
This command builds the project, formats the code, runs all test cases, and deploys the project to AWS.

```bash
./build.sh -p [your profile name] deploy
```

## Package Management

### Install Packages
Use the following command to install dependencies.

```bash
poetry add [package name]
```

### Install Dev Dependencies
Use the following command to install development dependencies.

```bash
poetry add [package name] --dev
```
