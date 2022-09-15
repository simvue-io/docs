# Python client

The Simvue Python client allows users to be easily able to capture information such as metadata, metrics and files from the execution of existing Python codes. It can also be used to create a sidecar in order to capture information from an application written in another language.

## Installation

The client can be installed from PyPI:
```
pip install simvue
```

## Setup

The URL of the Simvue server and authentication token need to be provided.
This information is provided by either a `simvue.ini` file of the form:
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
Environment variables take precedance over the configuration file.

The exact values to use can be obtained from the web UI by clicking **Create new run**.

## Usage

### Initialisation

Firstly import the required class:
```
from simvue import Simvue
```
and create an instance of the `Simvue` object:
```
run = Simvue()
```
The `init` method needs to be called in order to create a run. The following can be specified but all are optional:

 * `name`: name of the run. If no name is provided a name will be genenerated consisting of two random words (in the form adjective-noun);
 * `metadata`: metadata in the form of a dictionary of key-value pairs;
 * `tags`: tags in the form of a list;
 * `description`: plain text description of the run;
 * `folder`: folder for the run. If none is provided the folder is assumed to be `/`. If the folder doesn't already exist it will be created.

For example:
```
run.init(name='my-first-run',
         metadata={'environment': 'test'},
         tags=['test'],
         description='This is a test',
         folder='/tests')
```

### Metrics

To log time-series metrics use the `log` method, for example:
```
run.log({'parameter1': 1.2, 'parameter2': 3.5})
```
The argument is a dictionary consisting of the metric names and their values.

The `log` method can be called as many times as necessary during a run, and the time of each is recorded with microsecond precision.

### Artifacts

Files can be saved using the `save` method. One of three categories needs to be specified:

 * `code`: software;
 * `input`: input files;
 * `output`: output files.

For example:
```
run.save('data.png', 'output')
```

### Folders

If a new folder is specified in `init` we can use `folder_details` to specify more information about the folder, specifically metdata, tags and a description. For
example:
```
run.folder_details('/tests',
                   metadata={'environment': 'testing'},
                   tags=['test'],
                   description='My first tests')
```
Each of these are optional so only the information required by the user needs to be set.

### Events

Arbitrary text can be logged using the `event` method. These can be used for storing log messages, exceptions or any other useful
information. For example, 
```
try:
    ...
except Exception as exc:
    run.event(exc)
    ...
```
The timestamp at which the `event` method is called is recorded.

### Alerts

The `add_alert` method can be used to associate an alert with the current run. If the alert definition does not exist it will
be created. The arguments are:

 * `name`: name of the alert
 * `type`: type of alert, which needs to be one of `is above`, `is below`, `is outside range`, `is inside range`
 * `metric`: name of the metric to use
 * `frequency`: how often (in minutes) to calculate the average of the metric
 * `window`: what time period (in minutes) over which to calculate the average of the metric

In addition, for the case of `is above` and `is below`:

 * `threshold`: threshold

and for `is outside range` and `is inside range`:

 * `range_low`: lower limit of range
 * `range_high`: upper limit of range

For example, to create a threshold alert:
```
run.add_alert(name='quality too low',
              type='is below',
              metric='quality',
              frequency=1,
              window=1,
              threshold=0.4)
```
In this case if the 1-minute average of the `quality` metric, calculated at 1-minute intervals, goes below 0.4 the alert will be triggered.

Similarly, here is an example of a range-based alert:
```
run.add_alert(name='density invalid',
              type='is outside range',
              metric='density',
              frequency=1,
              window=1,
              range_low=1.0,
              range_high=5.0)
```
In this case, if the 1-minute average of the `density`, calculated at 1-minute intervals, goes below 1.0 or above 5.0 the alert will be triggered.

### Ending the run
To cleanly finish a run:
```
run.close()
```
Any batches of metrics or events not yet sent to the remote server will be sent at this point.

An alternative to this is to use a context manager, for example:
```
with Simvue() as run:
   run.init(...)

   ...
```
In this case it is not necessary to explicitly run `run.close()`.

If a code crashes without calling `close()` after a few minutes the state of the run will change to `lost`.
