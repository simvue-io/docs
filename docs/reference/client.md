# The `Client` class

The `Client` is used for querying or accessing data from existing runs.

### Methods

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
