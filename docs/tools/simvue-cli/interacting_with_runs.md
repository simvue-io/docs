# Interacting with Runs
The primary purpose of the CLI is to be able to interact with any Simvue runs you have stored on the server.
The `run` sub-command provides the interface for creation, view, modification and deletion of runs owned by the current user.

## Listing Runs
To list runs on the server execute:

```sh
simvue run list
```

By default this will return only the identifiers of the first 20 runs in descending order of creation time. The command
features a number of flags which can be used to expand on this information:

|**Option**    |**Description**|**Default**|
|------|-----------|-------|
|`--format`|Display format of table, see help string.|`plain`|
|`--enumerate`|Adds an additional enumeration column to the output.|`False`|
|`--count`|Set the number of results to return.|`20`|
|`--tags`|Display the tags associated with each run.|`False`|
|`--name`|Display the name of each run.|`False`|
|`--user`|Display additional users each run is visible to.|`False`|
|`--created`|Display the created timestamp.|`False`|
|`--description`|Display the description for each run.|`False`|
|`--status`|Display the status of each run.|`False`|
|`--folder`|Display the parent folder of each run.|`False`|
|`--sort-by`|Column to sort by `created`, `started`, `endtime`, `modified`, `name`.<br>Can be called more than once.|`['created']`|
|`--reverse`|Reverse the sorting order.|`False`|

!!! example

    ```sh
    $ simvue run list --name --count 5 --format fancy_grid
    ╒════════════════════════╤══════════════════════════════════════════════╕
    │ id                     │ name                                         │
    ╞════════════════════════╪══════════════════════════════════════════════╡
    │ XXXXXXXXXXXXXXXXXXXXX  │ mild-bassoon                                 │
    ├────────────────────────┼──────────────────────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ test_completion_callbacks_trigger_set        │
    ├────────────────────────┼──────────────────────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ test_completion_trigger_set                  │
    ├────────────────────────┼──────────────────────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ test_completion_callbacks_var_change         │
    ╘════════════════════════╧══════════════════════════════════════════════╛
    ```

## JSON View
All available information for a run can be obtained using the `json` sub-command:

```sh
simvue run json <RUN-ID>
```

this will return a JSON dump of the response from the server for the given run. 


!!! example "Combining Commands"

    As commands are designed to work together, as an example we can view and query the metadata for the latest Simvue run using the tool [`jq`](https://jqlang.org/download/) by executing:
    
    ```sh
    simvue run list --count 1 | simvue run json | jq '.metadata'
    ```

## Modifying Runs

Runs can be updated using the command line, note this is limited to only allow addition of metadata, logging of events, and adding metric values. Only runs which are still active
(i.e. not terminated, lost or completed) can be modified.

### Updating Metadata

For an active run we can update the metadata by parsing a JSON compatible string to the `metadata` sub-command:

```sh
simvue run metadata <RUN-ID> <METADATA>
```

For example:

```sh
simvue run metadata T6xPreaB9cX3KafqkRfQ '{"test_value": 1}'
```

Remember we can verify this was successful using the [`json`](#json-view) command above:

```sh
simvue run json T6xPreaB9cX3KafqkRfQ | jq '.metadata'
```

### Logging Events


Events can be logged to active runs:

```sh
simvue run log.event T6xPreaB9cX3KafqkRfQ "The rain in Spain falls mainly on the plain"
```

### Logging Metrics

Metrics can be logged to active runs using a JSON string. This is useful if running a simple shell script and wanting to forward outputs as metric values.

!!! example "BASH loop metric gathering"
    ```sh
    for i in {0..10}; do simvue run log.metrics T6xPreaB9cX3KafqkRfQ "{\"x\": $i}"; done
    ```


## Creating, Closing and Removing Runs

The CLI can also handle the creation and status of runs. This is particularly useful if you want to open a run on the command line and quickly forward
some metrics from the shell.

### Creating a Run

Creating a run is simple, the following command will return the ID of the new run:

```sh
simvue run create 
```

Note that a run created on the command line does not have a heartbeat and so will time out. The command has additional options for defining timeouts and other
properties:

|**Option**|**Description**|**Default**|
|------|----------|--------|
|`--create-only`|Creates a run but does not start it.|`False`|
|`--timeout`|Specify the timeout period in seconds, after which the run will be lost.||
|`--name`|Set the name for this run.|`None`|
|`--description`|Set the description for this run.|`None`|
|`--folder`|Set the parent folder for this run.|`/`|
|`--retention`|Specify the retention period in seconds.||
|`--environment`|Include the environment metadata for this run.|`False`|

### Closing or Aborting a Run

If creating a run on the command line the run will continue until the timeout period is met, the run will then
be set to "lost". In order to terminate the run and set it to "completed" use the command:

```sh
simvue run close <RUN-ID>
```

or alternatively we can abort it by running:

```sh
simvue run abort <RUN-ID>
```

### Removing Runs

Runs can be removed from the Simvue server by executing:

```sh
simvue run remove <RUN-ID> 
```

## Piping Commands Together

In general the commands above have been designed to add simplicity in creating workflows. 

!!! example "Scripting"
    As an example scenario, say you had a terminal based command that returned an integer metric when executed.
    We could define a workflow in a script `demo.sh`: 

    ```sh
    #!/usr/bin/bash
    set -e
    
    calculate_integer() {
      echo $((RANDOM % (100 - 2) + 1))
    }
    
    SIMVUE_RUN_ID=$(
      simvue run create \
        --name "My Test Simulation" \
        --folder "/shell_demos" \
        --timeout 100
    )
    
    simvue run metadata $SIMVUE_RUN_ID '{"random_meta": "demo"}'
    
    for x_param in {5..10}; do
      simvue run log.event $SIMVUE_RUN_ID "Running simulation with x=$x_param"
      METRIC_VALUE=$(calculate_integer $x_param)
      simvue run log.metrics $SIMVUE_RUN_ID "{\"x\": $x_param, \"y\": $METRIC_VALUE}"
    done
    
    simvue run close $SIMVUE_RUN_ID
    ```

## Monitoring Stdin
The CLI includes a command for creating a run and monitoring outputs from a process via stdin. This is for a very specific use case where
the output is just a list of delimited values which can be directly read as metrics:

```sh
<process> | simvue monitor
```

!!! example "A simple calculation script"
    Say we have a script which generates $$x$$ and $$y$$ values and prints them to the command line:
    ```sh
    #!/usr/bin/bash
    set -e
    
    dummy_sim() {
      echo "x,y"
      for i in {0..100}; do
        echo "$i,$((RANDOM % (100 - 2) + 1))"
      done
    }

    dummy_sim | simvue monitor --name "Test run" --delimiter ','
    ```

The command has additional options:

|**Option**|**Description**|**Default**|
|------|-----------|-------|
|`--name`|Name to give to the created run.|`None`|
|`--description`|Description for the run.|`None`|
|`--tag`|Label the run with a tag.|`None`|
|`--folder`|Folder to place this run.|`/`|
|`--retention`|Time in seconds to keep this run.|`None`|
|`--delimiter`|Specify the delimiter separating values.|
|`--environment`|Include the environment in metadata.|`False`|
