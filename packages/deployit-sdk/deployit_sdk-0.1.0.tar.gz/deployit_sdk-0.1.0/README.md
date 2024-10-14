# DeployIt!

[![PyPI version](https://badge.fury.io/py/deployit-sdk.svg)](https://badge.fury.io/py/deployit-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/deployit-sdk.svg)](https://pypi.org/project/deployit-sdk/)

A powerful and user-friendly Python library for interacting with CI/CD servers. This library provides a convenient interface to manage builds, jobs, queues, and other functionalities programmatically.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- Easy-to-use interface for Jenkins, GitHub Actions, GitLab and others CI/CD servers operations
- Comprehensive support for builds, jobs, queues, and build stages
- Advanced filtering and search capabilities
- Robust error handling
- Extensive documentation and examples

## Installation

You can install the deployit using pip:

```bash
pip install deployit-sdk
```

## Quick Start


Currently, there's only the Jenkins SDK implemented, here's a quick example to get you started:

```python
from deployit.providers.jenkins.client import JenkinsClient

# Set up your Jenkins connection details
import os
os.environ["JENKINS_DOMAIN"] = "http://jenkins.example.com"
os.environ["JENKINS_USERNAME"] = "your-username"
os.environ["JENKINS_API_TOKEN"] = "your-api-token"

# Create a Jenkins client
jenkins = JenkinsClient()

# Get information about a job
job = jenkins.job.get_info("/my-project/main")
print(f"Job name: {job.name}, URL: {job.url}")

# Trigger a build
build = jenkins.job.build("/my-project/main")
print(f"Build triggered: {build.number}")
```


## Usage Examples

### Working with Builds

```python
# Get build information
build = jenkins.build.get_build_info("/my-project/main", 42)
print(f"Build number: {build.number}, Result: {build.result}")

# Get console output
console_log = jenkins.build.get_console_log("/my-project/main", 42)
print(console_log['content'])

# Stop a build
jenkins.build.stop("/my-project/main", 42)

# Get build stages
stages = jenkins.build.get_stages("/my-project/main", 42)
for stage in stages:
    print(f"Stage: {stage.name}, Status: {stage.status}")

# Refresh a build
updated_build = jenkins.build.refresh_build(build)
print(f"Updated build status: {updated_build.result}")

# Get environment variables
env_vars = jenkins.build.get_env_vars("/my-project/main", 42)
print(f"Environment variables: {env_vars}")

# Get test report
test_report = jenkins.build.get_test_report("/my-project/main", 42)
print(f"Test report: {test_report}")

# Get a specific artifact
artifact = jenkins.build.get_artifact("/my-project/main", 42, "path/to/artifact.zip")
print(f"Artifact data: {artifact}")

# Get pending stages
pending_stages = jenkins.build.get_pending_stages("/my-project/main", 42)
for stage in pending_stages:
    print(f"Pending stage: {stage.name}")

# Fetch build status
status = jenkins.build.fetch_status(build, "/my-project/main")
print(f"Current build status: {status}")
```

### Working with Jobs

```python
# Get job information
job = jenkins.job.get_info("/my-project/main")
print(f"Job name: {job.name}, URL: {job.url}")

# Trigger a build
build = jenkins.job.build("/my-project/main")
print(f"Build triggered: {build.number}")

# Trigger a build with parameters
params = {"BRANCH": "feature-branch"}
jenkins.job.build_with_params("/my-project/main", params)

# Get all builds for a job
builds = jenkins.job.get_all_builds("/my-project/main")
for build in builds['allBuilds']:
    print(f"Build number: {build['number']}, Result: {build['result']}")

# Get all jobs with a specific tree structure
all_jobs = jenkins.job.get_all("jobs[name,url,color]")
for job in all_jobs['jobs']:
    print(f"Job name: {job['name']}, URL: {job['url']}, Color: {job['color']}")

# Wait for a build to start
build_obj = jenkins.job.build("/my-project/main", wait_until_start=True)
print(f"Build {build_obj.number} has started")

# Fetch detailed job information
detailed_job = jenkins.job.fetch_job_details(job)
print(f"Detailed job info: {detailed_job}")

# Fetch builds with filtering
filtered_builds = jenkins.job.fetch_builds(job, filter_by={"result": "SUCCESS"})
for build in filtered_builds:
    print(f"Successful build: {build.number}")
```

### Working with Build Stages

```python
# Handle an input stage
build_stage = JenkinsBuildStage({"id": "input-stage-id", "build_id": 42})
jenkins.build_stage.handle_input(
    "/my-project/main",
    build_stage,
    action="submit",
    proceed_caption="Proceed",
    parameters={"APPROVE": "YES"}
)
```

### Working with the Queue

```python
# Get the current queue
queue = jenkins.queue.get_queue()
for item in queue.items:
    print(f"Queue item: {item.id}, Task: {item.task_name}")

# Get a specific queue item
queue_item = jenkins.queue.get_queue_item(123)
print(f"Queue item status: {queue_item.why}")

# Cancel a queue item
jenkins.queue.cancel_queue_item(123)
```

## Advanced Usage

### Filtering Builds

```python
# Fetch successful builds
successful_builds = jenkins.job.fetch_builds(job, filter_by={"result": "SUCCESS"})

# Fetch builds by a specific user
user_builds = jenkins.job.fetch_builds(job, filter_by={"actions.causes.userId": "john_doe"})

# Fetch builds with a specific commit
commit_builds = jenkins.job.fetch_builds(job, filter_by={"changeSets.items.commitId": "abcdef123456"})
```

### Working with Build Stages

```python
# Get all stages of a build
stages = jenkins.build.get_stages("/my-pipeline/main", 42)

# Get pending stages (e.g., stages waiting for input)
pending_stages = jenkins.build.get_pending_stages("/my-pipeline/main", 42)

# Handle an input stage
if pending_stages:
    input_stage = pending_stages[0]
    jenkins.build_stage.handle_input(
        "/my-pipeline/main",
        input_stage,
        action="submit",
        proceed_caption="Proceed",
        parameters={"APPROVE": "YES"}
    )
```

### Refreshing Build Information

```python
build = jenkins.job.build("/my-project/main", wait_until_start=True)
while build.is_building:
    time.sleep(30)  # Wait for 30 seconds
    build = jenkins.build.refresh_build(build)
print(f"Build finished with result: {build.result}")
```

### Fetching and Analyzing Test Reports

```python
test_report = jenkins.build.get_test_report("/my-project/main", 42)
total_tests = test_report['totalCount']
failed_tests = test_report['failCount']
skipped_tests = test_report['skipCount']
print(f"Total tests: {total_tests}, Failed: {failed_tests}, Skipped: {skipped_tests}")

# Analyze individual test cases
for suite in test_report['suites']:
    for case in suite['cases']:
        if case['status'] != 'PASSED':
            print(f"Failed test: {case['name']}, Error: {case.get('errorDetails', 'N/A')}")
```

### Error Handling

```python
from deployit.providers.jenkins.utils.errors import JenkinsError, JenkinsConnectionError, JenkinsAPIError

try:
    job = jenkins.job.get_info("/my-project/main")
except JenkinsConnectionError as e:
    print(f"Connection error: {e}")
except JenkinsAPIError as e:
    print(f"API error: {e}")
except JenkinsError as e:
    print(f"General Jenkins error: {e}")
```

For more detailed information and advanced usage, please refer to our [full documentation](#documentation).

## Documentation

For comprehensive documentation, including detailed API references and advanced usage examples, please visit our [documentation site](https://jenkins-api-library.readthedocs.io).

## Contributing

We welcome contributions to the Jenkins API Library! Here are some ways you can contribute:

1. Report bugs or suggest features by opening an issue
2. Improve documentation
3. Submit pull requests with bug fixes or new features

Please read our [Contributing Guide](CONTRIBUTING.md) for more details on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on our [GitHub Issues page](https://github.com/your-repo/jenkins-api-library/issues).

For commercial support or custom development services, please contact us at support@jenkinsapilibrary.com.

---

Made with ❤️ by the Jenkins API Library Team
