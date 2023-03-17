# The `Client` class

The `Client` is used for querying or accessing data from existing runs.

### Methods

#### `get_run()`

Returns details about a specified run.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `str` | Name of the run |
| system | `Boolean`, optional | Return system information |
| tags | `Boolean`, optional | Return tags |
| metadata | `Boolean`, optional | Return metadata |

#### `get_runs()`

Returns details about a list of runs.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| filters | `List[str]` | Filters to select runs |
| system | `Boolean`, optional | Return system information |
| tags | `Boolean`, optional | Return tags |
| metadata | `Boolean`, optional | Return metadata |
| format | `str`, optional | Output format, either `dict` (default) or `dataframe` |

#### `get_events()`

Returns events from the specified run. *Available soon*.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `str` | Name of the run |
| filter | `str`, optional | Return only events matching this filter |

#### `get_metrics()`

Returns metrics from the specified runs. *Available soon*.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `List[str]` | Name(s) of runs |
| metrics | `List[str]` | Name(s) of metrics |
| group_by | `str`, optional | Group by this metadata attribute and return aggregates |
| format | `str`, optional | Output format, either `dict` (default) or `dataframe` |

#### `delete_run()`

Delete the specified run.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `str` | Run name |

#### `delete_runs()`

Delete the runs in the specified folder.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| folder | `str` |  Folder name |

#### `get_folder()`

Returns details about a specified folder.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| folder | `str` | Name of the folder |
| tags | `Boolean`, optional | Return tags |
| metadata | `Boolean`, optional | Return metadata |

#### `get_folders()`

Returns details about a list of folders.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| filters | `List[str]` | Filters to select folders |
| tags | `Boolean`, optional | Return tags |
| metadata | `Boolean`, optional | Return metadata |

#### `delete_folder()`

Delete a folder and optionally any runs in it.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| folder | `str` | Folder name |
| runs | `Boolean`, optional | Delete runs in the folder |

#### `list_artifacts()`

Returns a list of artifacts associated with the specified run.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `str` | Run name |
| category | `Enum[input, code, output`], optional | Only list artifacts of the specified category |

#### `get_artifact()`

Retrieves a single artifact and returns the content.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `str` | Run name |
| name | `str` | Artifact name |

#### `get_artifact_as_file()`

Downloads a single artifact and saves as a file.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `str` | Run name |
| name | `str` | Artifact name |
| path | `str`, optional | Save the file in the specified path 

#### `get_artifacts_as_files()`

Downloads multiple files associated with a run and saves as files.

| Name  | Type | Description |
| ----- | ---- | ----------- |
| run | `str` | Run name |
| category | `Enum[input, code, output`], optional | Only download artifacts of the specified category |
| startswith | `str`, optional | Only download artifacts which start with the specified string |
| contains | `str`, optional | Only download artifacts which contain  the specified string |
| endswith | `str`, optional | Only download artifacts which end with the specified string |
