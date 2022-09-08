# Python client

The Simvue Python client allows users to easily collect metadata, time-series metrics, artifacts and log messages from existing Python codes.

## Installation

The client can be installed from PyPI:
```
pip install simvue
```

## Usage

### Setup
The URL of the Simvue server and authentication token need to be provided.
This information is provided by either a `simvue.ini` file:
```
[server]
url =
token =
```
or via environment variables:
```
export SIMVUE_URL=
export SIMVUE_TOKEN=
```
The values to use can be obtained most simply from the web UI by clicking **Create new run**.
