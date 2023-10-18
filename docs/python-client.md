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

## Tracking simulations

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

### Updating tags and metadata

In some situations it may be useful to update tags or metadata at later points in the lifetime of a run, not just the start. A simple example could be adding a tag `unconverged` if a simulation fails to converge:
```
run.update_tags(['unconverged'])
```
Metadata can be added in a similar way, for example:
```
run.update_metadata({'status': 'unconverged'})
```

### Metrics

To log time-series metrics use the `log_metrics` method, for example:
```
run.log_metrics({'parameter1': 1.2, 'parameter2': 3.5})
```
The argument is a dictionary consisting of the metric names and their values.

The `log_metrics` method can be called as many times as necessary during a run, and the time of each is recorded with microsecond precision. The
timestamp can be overriden if necessary, for example if the metrics are being extracted from another source with its own timestamps. For example:
```
run.log_metrics({'parameter1': 1.2}, timestamp='2021-05-03 14:13:27.281920')
```
In addition to the timestamp the relative time since `init()` was called is also recorded. The relative time can be set manually if needed, e.g.:
```
run.log_metrics({'parameter1': 1.2}, time=time)
```
where here `time` is a floating point number.

### Artifacts

#### Individual files

Individual files can be saved using the `save` method. One of three categories needs to be specified:

 * `code`: software;
 * `input`: input files;
 * `output`: output files.

For example:
```
run.save('data.png', 'output')
```

An optional `filetype` argument can be used to specify the MIME type of the file. By default the MIME type is determined
autoatically. For example:
```
run.save('in.lj', 'input', 'text/plain')
```

By default the name of the artifact will only be the name of the actual file specified, even if an absolute or relative path is specified.
If the optional argument `preserve_path=True` is added to `save` then paths will be preserved in the names. This can be useful
in situations where the files are naturally grouped together and you want to preserve this information, e.g. `group1/file1` and
`group2/file1`.

#### Directories

Multiple files in a directory can be saved using the `save_directory` method which has the same arguments as `save` but
instead of specifying a single filename the name of a directory is specified. A MIME type can be specified but all files
in the directory will be set to the same MIME type.

For example, suppose you have a directory `system` containing the following files: `blockMeshDict`, `controlDict`, `fvSchemes`,
`fvSolution`, `meshQualityDict`, `snappyHexMeshDict` and `surfaceFeaturesDict`. Using:
```
run.save_directory('system', 'input', preserve_path=True)
```
will result in 7 artifacts being uploaded with names `system/blockMeshDict`, `system/controlDict`, `system/fvSchemes`,
`system/fvSolution`, `system/meshQualityDict`, `system/snappyHexMeshDict` and `system/surfaceFeaturesDict`

#### List of files and/or directories

A list of a combination of files and directories can be provided using the `save_all` method, providing a simple way for saving a group
of files and/or directories. For example:
```
run.save_all(['file1', 'file2', 'directory1'], 'input', preserve_path=True)
```
will save the files `file1` and `file2` in addition to the directory `directory1`.

### Folders

If a new folder is specified in `init` we can use `folder_details` to specify more information about the folder, specifically metdata, tags and a description. For
example:
```
run.folder_details('/tests',
                   metadata={'environment': 'testing'},
                   tags=['test'],
                   description='My first tests')
```
All of these are optional so only the information required by the user needs to be set.

### Events

Arbitrary text can be logged using the `log_event` method. These can be used for storing log messages, exceptions or any other useful
information. For example:
```
try:
    ...
except Exception as exc:
    run.log_event(exc)
    ...
```
The timestamp at which the `log_event` method is called is recorded, and similar to metrics this can be overriden if necessary, for example:
```
run.log_event(message, timestamp='2022-01-03 16:42:30.849617')
```

#### Python logging module

Logs from the standard [Python logging module](https://docs.python.org/3/library/logging.html) can be captured. This is done
by adding the `SimvueHandler` to the `logger`, for example:
```
from simvue import Simvue, SimvueHandler

run = Simvue()
run.init()

logger = logging.getLogger(__name__)
logger.addHandler(SimvueHandler(run))
```

### Alerts

The `add_alert` method can be used to associate an alert with the current run. If the alert definition does not exist it will
be created. The arguments are:

 * `name`: name of the alert
 * `type`: type of alert, which needs to be one of `is above`, `is below`, `is outside range`, `is inside range`
 * `metric`: name of the metric to use
 * `frequency`: how often (in minutes) to calculate the average of the metric
 * `window`: what time period (in minutes) over which to calculate the average of the metric
 * `notification`: type of notification, either `none` (default) or `email`

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

If `notification` is set to `email` an email will be sent to the user when the alert first goes critical.

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

### Configuration

The `config` method can be used to set some configuration options. It should be called before calling `init`.

* `suppress_errors`: if set to `False` problems with the Simvue client will trigger exceptions. By default this is `True`, ensuring that the main application can run successfully even in the event of misconfiguration or problems with the monitoring.
* `queue_blocking`: when set to `True` the metrics and events queues will block if they become full. By default this is `False`, meaning that metrics and/or events will be silently dropped if either of the queues fills.
* `queue_size`: maximum numbers of items which can be stored in the metrics and events queues. The default is 10000. For extremely high-frequency metrics or events it might be necessary to increase this number.

## Querying existing runs and obtaining existing data

The Simvue Python client can also be used for querying existing runs and downloading data from existing runs. In this case the `init`
method does not need to be called.

### Listing artifacts associated with a run

The method `list_artifacts(run, category=None)` can be used to obtain a list of artifacts associated with an existing run. By default
all artifacts are listed but the `category` argument can be used to specify either `input`, `output` or `code` if needed.

For example, assuming the variable `run_name` is set to the name of the run:
```
client = Simvue()
artifacts = client.list_artifacts(run_name, category='input')
```
will create an array `artifacts` listing all input files associated with run `run_name`.

### Downloading a single artifact

The method `get_artifact_as_file` can be used to download a single artifact from an exsting run. For example:
```
client.get_artifact_as_file(run_name, artifact_name, path='/tmp')
```
will download `artifact_name` from run `run_name` into `/tmp`. If a path is not provided the file will be downloaded into the current working directory.

### Downloading multiple artifacts

The method `get_artifacts_as_files` can be used to download multiple artifacts from an existing run. For example:
```
client.get_artifacts_as_files(run_name, path='/tmp')
```
will download all artifacts from run `run_name` into `/tmp`. A category can be specified in order to restrict which files are
downloaded, for example:
```
client.get_artifacts_as_files(run_name, path='/tmp', category='output')
```
There are additional optional arguments for further restricting what files are downloaded:

* `startswith`: only files which begin with the specified text,
* `contains`: only files which contain the specified text,
* `endswith`: only files which end with the specified text.

These can be combined with specification of a `category`. For example, to download all input files starting with `system/`:
```
client.get_artifacts_as_files(run_name, category='input', startswith='system/')
```
