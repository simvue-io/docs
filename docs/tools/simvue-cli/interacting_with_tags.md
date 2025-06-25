# Interacting with Tags
The following commands provide interaction with Simvue tags.

## Listing Tags 

To list available storage systems on the server execute:

```sh
simvue tag list
```

By default this will return only the identifiers of the first 20 tags in descending order of creation time. The command
features a number of flags which can be used to expand on this information:

|**Option**    |**Description**|**Default**|
|------|-----------|-------|
|`--format`|Display format of table, see help string.|`plain`|
|`--enumerate`|Adds an additional enumeration column to the output.|`False`|
|`--count`|Set the number of results to return.|`20`|
|`--name`|Display the tag name.|`False`|
|`--color`|Display the tag hexidecimal color value.|`False`|
|`--sort-by`|Column to sort by `created`, `started`, `endtime`, `modified`, `name`.<br>Can be called more than once.|`['created']`|
|`--reverse`|Reverse the sorting order.|`False`|

!!! example
    
    ```sh
    $ simvue tag list --name --count 2 --format fancy_grid
    ╒════════════════════════╤════════════════════════════════════════════════════╕
    │ id                     │ name                                               │
    ╞════════════════════════╪════════════════════════════════════════════════════╡
    │ XXXXXXXXXXXXXXXXXXXXX  │ test_get_metric_values_complete_labels             │
    ├────────────────────────┼────────────────────────────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ test_get_metric_values_complete_ids                │
    ╘════════════════════════╧════════════════════════════════════════════════════╛
    ```
## JSON View
All available information for a run can be obtained using the `json` sub-command:

```sh
simvue tag json <TAG-ID>
```

this will return a JSON dump of the response from the server for the given tag. 

!!! example "Combining Commands"

    As commands are designed to work together, as an example we can view and query the metadata for the latest Simvue tag using the tool [`jq`](https://jqlang.org/download/) by executing:
    
    ```sh
    simvue tag list --count 1 | simvue tag json | jq '.description'
    ```
