# Interacting with Storage
The following commands provide interaction with Simvue storage systems.

## Listing Storage Systems

To list available storage systems on the server execute:

```sh
simvue storage list
```

By default this will return only the identifiers of the first 20 storage systems in descending order of creation time. The command
features a number of flags which can be used to expand on this information:

|**Option**    |**Description**|**Default**|
|------|-----------|-------|
|`--format`|Display format of table, see help string.|`plain`|
|`--enumerate`|Adds an additional enumeration column to the output.|`False`|
|`--count`|Set the number of results to return.|`20`|
|`--name`|Display the name for the storage system.|`False`|
|`--backend`|Display the backend for the storage system.|`False`|
|`--default`|Display whether the storage system is the default.|`False`|
|`--tenant-usable`|Display if storage system is usable by the current tenant.|`False`|
|`--enabled`|Display if the storage system is enabled.|`False`|
|`--created`|Display the time the artifact was created.|`False`|
|`--sort-by`|Column to sort by `created`, `started`, `endtime`, `modified`, `name`.<br>Can be called more than once.|`['created']`|
|`--reverse`|Reverse the sorting order.|`False`|

!!! example
    
    ```sh
    $ simvue storage list --name --backend --count 2 --format fancy_grid
    ╒════════════════════════╤═══════════╤═══════════╕
    │ id                     │ name      │ backend   │
    ╞════════════════════════╪═══════════╪═══════════╡
    │ XXXXXXXXXXXXXXXXXXXXX  │ AWS-1     │ S3        │
    ├────────────────────────┼───────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ Local     │ file      │
    ╘════════════════════════╧═══════════╧═══════════╛
    ```
