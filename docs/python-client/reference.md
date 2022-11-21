# Reference

## The `Run` class

The `Run` is used to track and monitor simulations, processing or training tasks.

### Attributes

#### `name`: `str`

Gets the name of the run.

### Methods

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
| `status` | `str`, optional | Initial status |

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

Log metrics.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- |
| `metrics` | `Dict[str, Union[int, float]]` | Dictionary containing metric names and values | 
| `step` | `int`, optional | Step or epoch | Increments automatically each time `log_metrics` is called |
| `time` | `float`, optional | Time in seconds |
| `timestamp` | `YYYY-MM-DDThh:mm:ss.zzzzzzZ`, optional | Timestamp, with up to microsecond precision |


#### `log_event()`

Log an event.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ----------- |
| `message` | `str` | Text message |
| `timestamp` | `YYYY-MM-DDThh:mm:ss.zzzzzzZ`, optional | Timestamp, with up to microsecond precision |

#### `save()`

Save a file.

**Parameters**

| Name  | Type | Description |
| ----- | ---- | ----------- |
| `filename` | `str` | Filename |
| `category` | `Enum[code, input, output]` | Type of file | 
| `filetype` | `str`, optional | MIME type | 
| `preserve_path` | `Boolean`, optional | Preserve path of file |

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

Close a run. Only needed if a context manager is not used.§

#### `set_folder_details()`

Set metadata, tags and a description for a folder.

**Parameters**

| Name  | Type | Description | 
| ----- | ---- | ----------- | 
| `path` | `str` | Name | 
| `metadata` | `Dict[str, Union[str, int, float]]`, optional | Metadata attributes and values | 
| `tags` | `List[str]`, optional | List of tags | 
| `description` | `str`, optional | Description | 

#### `add_alert`

Define an alert and add it to the simulation run.

**Parameters**

| Name  | Type | Description | Default |
| ----- | ---- | ----------- | ------- |
| `name` | `str` | Name |  |
| `source` | |  |  |
| `frequency` | |  |  |
| `window` | |  |  |
| `rule` | |  |  |
| `metric` | |  |  |
| `threshold` | |  |  |
| `range_low` | |  |  |
| `range_high` | |  |  |
| `notification` | |  |  |
| `pattern` | |  |  |
