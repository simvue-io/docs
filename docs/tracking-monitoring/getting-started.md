# Getting started

The Simvue Python client allows users to be easily able to capture information such as metadata, metrics and files from the execution of existing Python codes. It can also be used to create an application to run in parallel to a simulation code written in another language, for
example collecting
metrics from log files.

## Installation

The client can be installed from PyPI:
```sh
pip install simvue
```
It is usually best to make use of a Python virtual environment, for example in a Linux environment run:
```sh
python3 -m venv simvue_venv
source ./simvue_venv/bin/active
```
in a Windows environment run:
```sh
python3 -m venv simvue_venv
simvue_venv/Scripts/activate
```
before running `pip`.

## Setup

The URL of the Simvue server and authentication token need to be provided by means of a configuration file
with content of the form:

```toml
[server]
url = "https://uk.simvue.io"
token = "eyJ0eXAi..."
```

This file can either be in the user's home directory (`~/.simvue.toml`) or in the current directory (`simvue.toml`). If both
exist the configuration file in the current directory takes precedance.
The exact values to use can be obtained from the web UI by clicking **Create new run**.

Alternatively environment variables can be used:

```sh
export SIMVUE_URL=https://uk.simvue.io
export SIMVUE_TOKEN=eyJ0eXAi...
```

This may be preferable for workloads running on cloud native resources. Environment variables take precedance over any configuration files.
Again, the values to use for the url and token can be obtained from the web UI by clicking **Create new run**.

!!! warning

    Do not copy the above examples directly. The correct values of the url and token must be obtained from the web UI.

### Setting project defaults
The Simvue configuration file `simvue.toml` supports the setting of defaults for key run properties which are set for all runs launched from the current location.
The key `run` allows the user to define tags, folder path, description, name, and metadata:

```toml
[server]
url = "https://uk.simvue.io"
token = "eyJ0eXAi..."

[run]
name = "my_amazing_project"
folder = "/amazing_project_runs"
tags = [
  "amazing",
  "demonstration"
]
description = "Running my amazing project"

[run.metadata]
my_favourite_colour = "green"
```

Any additional metadata or tags applied within an instance of `Run` are appended to those defined within this file, other values are superseded by definitions in `Run.init`.

## Worker nodes without outgoing internet access

Many HPC systems don't provide outgoing internet access from worker nodes. This is a problem for the Simvue Python client by default
because it needs to connect to a remote REST API.

``` mermaid
graph LR
subgraph "worker node"
  A[Simvue Python client]
end
A[Simvue Python client] --> B[Simvue server];
```

To get around this it is necessary to use the **offline** mode. With this the
Python client does not attempt to connect to the remote Simvue server, but instead writes everything to a filesystem which is shared
with login nodes.

``` mermaid
graph LR
subgraph "worker node"
  A[Simvue Python client];
  style B stroke-dasharray: 5 5
end
A[Simvue Python client] --> B[Filesystem];
```

A process (`simvue_sender`) running as a cron on a login node asynchronously sends all the required metadata, metrics and data to the
Simvue server.

``` mermaid
graph LR
subgraph "login node"
  C[Simvue sender];
  style B stroke-dasharray: 5 5
end
B[Filesystem] --> C[Simvue sender];
C --> D[Simvue server];
```

A single `simvue_sender` can be used for any number of running tasks being monitored by Simvue. Note that in offline mode metrics and
events will not quite be real time (there will be a delay of up to a minute or so), as data is sent to the Simvue server as a cron running
every minute. A cron is recommended rather than having a continuously running process because HPC login nodes sometimes have
restrictions on the maximum run time of processes, e.g. 5 minutes.

### Setup

By default the directory `~/.simvue` is used to store data being passed from worker nodes to Simvue, but this can
be customized if needed.
Create a `.simvue.toml` file in your home directory as described above, but with an additional `offline` section:

```toml
[server]
url = "https://uk.simvue.io"
token = "eyJ0eXAi..."

[offline]
cache = "/data/username/.simvue"
```

The path `/data/username/.simvue` should be replaced with an appropriate directory. The directory should be accessible from
both the login node(s) and worker nodes.

!!! warning "Deprecation of INI configuration"
    As of `simvue>=1.1.0` the `simvue.ini` form of configuration has been deprecated, users should move to using the newer `simvue.toml`.

It is also necessary to setup a cron to run the command `simvue_sender` (available from the Simvue Python module) every minute.
Firstly it is necessary to create a script called `$HOME/simvue_sender.sh`, for example, containing:

```  sh hl_lines="2 2"
#!/bin/sh
source $HOME/simvue_venv/bin/activate
simvue_sender
```

The highlighted line will need to be adjusted as appropriate to point to a virtual environment where the Simvue module is installed
(see the top of this page).

Then setup a cron to run this script every minute, for example:

```sh
chmod a+xr $HOME/simvue_sender.sh
echo "* * * * * $HOME/simvue_sender.sh" | crontab - 
```

!!! warning

    Artifacts, e.g. input or output files, can be saved to Simvue when offline is used. However, it is important to note that it is currently
    assumed that the login node has access to the required files.
