# Interacting with Artifacts
The following commands provide interaction with Simvue artifacts.

## Listing Artifacts

To list alerts on the server execute:

```sh
simvue artifact list
```

By default this will return only the identifiers of the first 20 alerts in descending order of creation time. The command
features a number of flags which can be used to expand on this information:

|**Option**    |**Description**|**Default**|
|------|-----------|-------|
|`--format`|Display format of table, see help string.|`plain`|
|`--enumerate`|Adds an additional enumeration column to the output.|`False`|
|`--count`|Set the number of results to return.|`20`|
|`--original-path`|Display the original file path.|`False`|
|`--mime-type`|Display the MIME type for the artifact file.|`False`|
|`--name`|Display the name of each run.|`False`|
|`--user`|Display the user associated with the artifact.|`False`|
|`--created`|Display the time the artifact was created.|`False`|
|`--size`|Display the artifact size.|`False`|
|`--uploaded`|Display whether the artifact has successfully uploaded data.|`False`|
|`--sort-by`|Column to sort by `created`, `started`, `endtime`, `modified`, `name`.<br>Can be called more than once.|`['created']`|
|`--reverse`|Reverse the sorting order.|`False`|

!!! example

    ```sh
    $ simvue artifact list --name --count 2 --format fancy_grid
    
    ╒════════════════════════╤═══════════════╕
    │ id                     │ name          │
    ╞════════════════════════╪═══════════════╡
    │ XKv6FowQkFDkUS4RknXkf  │ run_input.in  │
    ╞════════════════════════╪═══════════════╡
    │ G5DVHhGssje92nhdsUHsd  │ run_test.out  │
    ╘════════════════════════╧═══════════════╛
    ```
