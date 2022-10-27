# Getting started

The Simvue Python client allows users to be easily able to capture information such as metadata, metrics and files from the execution of existing Python codes. It can also be used to create an application to run in parallel to a simulation code written in another language, for
example collecting
metrics from log files.

## Installation

The client can be installed from PyPI:
```
pip install simvue
```

## Setup

The URL of the Simvue server and authentication token need to be provided by means of a configuration file
with content of the form:
```
[server]
url = https://app.simvue.io
token = eyJ0eXAi...
```
This file can either be in the user's home directory (`~/.simvue.ini`) or in the current directory (`simvue.ini`). If both
exist the configuration file in the current directory takes precedance.
The exact values to use can be obtained from the web UI by clicking **Create new run**.

Alternatively environment variables can be used:
```
export SIMVUE_URL=https://app.simvue.io
export SIMVUE_TOKEN=eyJ0eXAi...
```
This may be preferable for workloads running on cloud native resources. Environment variables take precedance over any configuration files.
Again, the values to use for the url and token can be obtained from the web UI by clicking **Create new run**.

!!! warning

    Do not copy the above examples directly. The correct values of the url and token must be obtained from the web UI.

