# Reference

## The Simvue class

### Attributes

#### `name`: `str`

Gets the name of the run.

### Methods

#### `init(name=None, metadata={}, tags=[], description=None, folder='/', status='running')` { #init data-toc-label="init" }

Initialises a run.

##### Parameters

| Name  | Type | Description | Default |
| ----- | ---- | ----------- | ------- |
| `name` | `str` | Name |  |
| `metadata` | `Dict[str, Union[str, int, float]]` | Metadata attributes and values | `{}` |
| `tags` | `List[str]` | List of tags | `[]`  |
| `description` | `str` | Description | `None` |
| `folder` | `str` | Folder | `\` |
| `status` | `str` | Status | `running` |

#### `reconnect(name)`

Reconned to a run in the `created` state.

#### `update_metadata(metadata)`

Update or add new metadata.

#### `update_tags(tags)`

Add new tags.

#### `log_metrics(metrics, time=None, timestamp=None)`

Log metrics.

#### `log_event(message, timestamp=None)`

Log an event.

#### `save(filename, category, filetype=None, preserve_path=False)`

Save a file.

#### `save_directory(directory, category, filetype=None, preserve_path=False)`

Save a directory.

#### `save_all(items, category, filetype=None, preserve_path=False)`

Save a list of files and/or directories.

#### `set_status(status)`

Set the status of a run.

#### `close()`

Close a run.

#### `set_folder_details(path, metadata={}, tags=[], description=None)`

Set metadata for a folder.

#### `add_alert(name, type, metric, frequency, window, threshold=None, range_low=None, range_high=None, notification='none')`

Define an alert and add it to the simulation run.
