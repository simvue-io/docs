# The `Run` class

The `Run` is used to track and monitor simulations, processing or training tasks.

### Attributes

#### `name`: `str`

Gets the name of the run.

### Methods

#### `Run()`

Creates an instance of the `Run` class. The argument `mode` enables tracking and monitoring to be disabled or set to
`offline` if being used on worker nodes without outgoing internet access.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ------- |
| mode | `Enum[online, offline, disabled]` | Specify if tracking and monitoring should be disabled or if `offline` mode should be used

#### `config()`

Configures a run. should be called before calling the init method for the run.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ------- |
| `suppress_errors` | `bool`, optional | Whether to suppress errors from Simvue to allow the simulation code to continue, by default True |
| `queue_blocking` | `bool`, optional | Whether metrics and events queues will block if they become full, otherwise metrics/events will be silently dropped, by default False |
| `queue_size` | `int`, optional | Maximum number of items which can be stored in metrics or events queues, by default 10000 |
| `disable_resources_metrics` | `bool`, optional | Whether resource metric collection should be disabled, by default False |
| `resources_metrics_interval` | `int`, optional | How often resource metrics are collected in seconds, by default 30 |

#### `init()`

Initialises a run. If a name is not provided a random name will be assigned in the form of `<adjective>-<noun>`.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ------- |
| `name` | `str`, optional | Name |
| `metadata` | `Dict[str, Union[str, int, float]]`, optional | Metadata attributes and values |
| `tags` | `List[str]`, optional | List of tags |
| `description` | `str`, optional | Description |
| `folder` | `str`, optional | Folder name |
| `running` | `Boolean`, optional | Automatically set the run to the `running` state |

#### `set_pid()`

Set the process ID (PID) of the process to be monitored.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ------- |
| `pid` | `int` | The PID of the process to be monitored |

#### `reconnect()`

Reconned to a run in the `created` state.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ----------- |
| `name` | `str` | Name |

#### `update_metadata()`

Update or add new metadata.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- |
| `metadata` | `Dict[str, Union[str, int, float]]` | Metadata attributes and values |

#### `update_tags()`

Add new tags.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ----------- |
| `tags` | `List[str]` | List of tags |

#### `log_metrics()`

Log metrics in the form of a dictionary of metrics names and values.
By default:

* `step` is an integer which starts at zero and increments automatically each time `log_metrics` is called,
* `time` is the time in seconds since `init` was called,
* `timestamp` is the current time.

but these can all be overridden if necessary.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- |
| `metrics` | `Dict[str, Union[int, float]]` | Dictionary containing metric names and values | 
| `step` | `int`, optional | Step or epoch | 
| `time` | `float`, optional | Time in seconds |
| `timestamp` | `YYYY-MM-DD hh:mm:ss.zzzzzz`, optional | Timestamp, with up to microsecond precision |


#### `log_event()`

Log an event.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ----------- |
| `message` | `str` | Text message |
| `timestamp` | `YYYY-MM-DD hh:mm:ss.zzzzzz`, optional | Timestamp, with up to microsecond precision |

#### `save()`

Save a file.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ----------- |
| `filename` | `str` | Filename |
| `category` | `Enum[code, input, output]` | Type of file | 
| `filetype` | `str`, optional | MIME type | 
| `preserve_path` | `Boolean`, optional | Preserve path of file |
| `name` | `str`, optional | Name of artifact, required for saving Python objects |
| `allow_pickle` | `Boolean`, optional | Allow use of pickle to serialize Python object |

#### `save_directory()`

Save all files in the directory.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- | 
| `directory` | `str` | Directory name | 
| `category` | `Enum[code, input, output]` | Type of file | 
| `filetype` | `str`, optional | MIME type | 
| `preserve_path` | `Boolean`, optional | Preserve path of files | 

#### `save_all()`

Save a list of files and/or directories.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- | 
| `directory` | `List[str]` | List of files and/or directories | 
| `category` | `Enum[code, input, output]` | Type of file | 
| `filetype` | `str`, optional | MIME type | 
| `preserve_path` | `Boolean`, optional | Preserve path of files | 

#### `set_status()`

Set the status of a run.

**Parameters**

| Name  | Type | Description | Default |
| ----- | ---- | ----------- | ------- |
| `status` | `Enum` | Name |  |

#### `close()`

Close a run. Only needed if a context manager is not used.

#### `set_folder_details()`

Set metadata, tags and a description for a folder.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- | 
| `path` | `str` | Name | 
| `metadata` | `Dict[str, Union[str, int, float]]`, optional | Metadata attributes and values | 
| `tags` | `List[str]`, optional | List of tags | 
| `description` | `str`, optional | Description | 

#### `add_alert()`

Define an alert and add it to the simulation run. If the alert is not already defined a new one
will be created.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- |
| `name` | `str` | Name |  
| `source` | `Enum[metrics, events]`| Source of the alert, either metrics or events |
| `frequency` | `int` | How often the alert should be evaulated and checked |  
| `window` | `int`, optional | Time period to average metrics over |
| `rule` | `Enum[is above, is below, is outside range, is inside range]`, optional | Rule to use for metrics-based alerts |
| `metric` | `str`, optional | Metric to use for metrics-based alerts |  
| `threshold` | `Union[int, float]`, optional | Threshold to use for a metrics-based alert using `is above` or `is below` |  
| `range_low` | `Union[int, float]`, optional | Lower limit to use for a metrics-based alert using `is outside range` or `is inside range` |
| `range_high` | `Union[int, float]`, optional | Upper limit to use for a metrics-based alert using `is outside range` or `is inside range` |  
| `notification` | `Enum[none, email]`, optional | Type of notification |
| `pattern` | `str`, optional | Pattern to search for for the case of an event-based alert |
