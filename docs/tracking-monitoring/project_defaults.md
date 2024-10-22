# Setting project defaults
The Simvue configuration file `simvue.toml` supports the setting of defaults for key run properties which are set for all runs launched from the current location.
The key `run` allows the user to define tags, folder path, description, name, and metadata:

```toml
[server]
url = "https://app.simvue.io"
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
