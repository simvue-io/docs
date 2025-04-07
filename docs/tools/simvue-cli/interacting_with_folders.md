# Interacting with Folders
The following commands provide interaction with Simvue folders.

## Listing Folders

To list alerts on the server execute:

```sh
simvue alert list
```

By default this will return only the identifiers of the first 20 alerts in descending order of creation time. The command
features a number of flags which can be used to expand on this information:

|**Option**    |**Description**|**Default**|
|------|-----------|-------|
|`--format`|Display format of table, see help string.|`plain`|
|`--enumerate`|Adds an additional enumeration column to the output.|`False`|
|`--count`|Set the number of results to return.|`20`|
|`--path`|Display the folder path.|`False`|
|`--tags`|Display folder tags.|`False`|
|`--name`|Display the name of each run.|`False`|
|`--created`|Display the created timestamp.|`False`|
|`--description`|Display the description for each run.|`False`|
|`--sort-by`|Column to sort by `created`, `started`, `endtime`, `modified`, `name`.<br>Can be called more than once.|`['created']`|
|`--reverse`|Reverse the sorting order.|`False`|

!!! example

    ```sh
    $ simvue folder list --path --name --count 2 --format fancy_grid
    
    ╒════════════════════════╤═══════════════╤════════╕
    │ id                     │ path          │ name   │
    ╞════════════════════════╪═══════════════╪════════╡
    │ XXXXXXXXXXXXXXXXXXXXX  │ /             │ root   │
    ╞════════════════════════╪═══════════════╪════════╡
    │ XXXXXXXXXXXXXXXXXXXXX  │ /simvue_tests │ test   │
    ╘════════════════════════╧═══════════════╧════════╛
    ```

## JSON View
All available information for a folder can be obtained using the `json` sub-command:

```sh
simvue folder json <ALERT-ID>
```

this will return a JSON dump of the response from the server for the given alert. 

!!! example "Combining Commands"

    As commands are designed to work together, as an example we can view and query the metadata for the latest Simvue folder using the tool [`jq`](https://jqlang.org/download/) by executing:
    
    ```sh
    simvue folder list --count 1 | simvue folder json | jq '.tags'
    ```
