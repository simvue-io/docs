# Introduction

## Welcome

Welcome to a step by step tutorial of how to use Simvue, using a very simple example to demonstrate how the functionality provided by Simvue allows the tracking, monitoring, and analysis of scripts. This example demonstrates using Simvue to track a simple Python code, adding in different features on a step by step basis. The ordering of topics introduced in this example roughly matches that of the documentation in the 'Tracking and Monitoring' and 'Analysis' sections. For first time users, it is recommended that you follow along with this example step by step, to get a good understanding of what each command does.

## Setup

### Create a virtual environment

Run the following commands to create and activate a new virtual environment:

```sh
python3 -m venv venv
source ./venv/bin/activate
```

### Install

Install the Python client:

```sh
pip install simvue
```

### Configuring Simvue

The next step is to specify the URL of the Simvue server and provide an access token used to authenticate to the server.

Login to the web UI, go to the **Runs** page and click **Create new run**. Create a file called `simvue.toml` containing
the contents as provided.
The file should look something like:

```toml
[server]
url = "https://uk.simvue.io"
token = "eyJ0eXAi..."
```

