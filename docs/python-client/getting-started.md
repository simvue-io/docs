# Getting started

The Simvue Python client allows users to be easily able to capture information such as metadata, metrics and files from the execution of existing Python codes. It can also be used to create an application to run in parallel to a simulation code written in another language, collecting
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
url = 
token = 
```
This file can either be in the user's home directory (`~/.simvue.ini`) or in the current directory (`simvue.ini`). If both
exist the configuration file in the current directory takes precedance.

Alternatively environment variables can be used:
```
export SIMVUE_URL=
export SIMVUE_TOKEN=
```
Environment variables take precedance over the configuration file.

The exact values to use can be obtained from the web UI by clicking **Create new run**.

