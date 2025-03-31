# Simvue Command Line Interface
![cli_preview](https://raw.githubusercontent.com/simvue-io/simvue-cli/main/CLI_image.png)

Simvue CLI provides a terminal based approach for interacting with a Simvue server instance allowing the user to access information on runs and other objects
locally as opposed to needing to view information on the Web UI. The tool is written in Python and is built in the [Low Level API](/development/low-level-api).

## Installation
It is recommended that the software be installed using `pipx` as this will allow it to run in an isolated Python environment, and hence there will be no
dependency collision with the central Python installation on your system:

```sh
pipx install simvue-cli
```

You can verify your install by running:

```sh
simvue about
```

which will display the current CLI version, the underlying Python API version and the version of the Simvue server.

## Getting Started
The CLI contains a comprehensive help which gives information on the various sub-commands and the arguments they take:

```
simvue --help

Usage: simvue [OPTIONS] COMMAND [ARGS]...

  Simvue CLI for interacting with a Simvue server instance

  Provides functionality for the retrieval, creation and modification of
  server objects

Options:
  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --version            Show the version and exit.
  --plain              Run without color/formatting
  --help               Show this message and exit.

Commands:
  about     Display full information on Simvue instance
  admin     Administrator commands, requires admin access
  alert     Create and list Simvue alerts
  artifact  View and manage Simvue artifacts
  config    Configure Simvue
  folder    Create or retrieve Simvue folders
  monitor   Monitor stdin for delimited lines sending as metrics
  ping      Ping the Simvue server
  purge     Remove all local Simvue files
  run       Create or retrieve Simvue runs
  storage   View and manage Simvue storages
  tag       Create or retrieve Simvue runs
  venv      Initialise virtual environments from run metadata.
  whoami    Retrieve current user information
```
