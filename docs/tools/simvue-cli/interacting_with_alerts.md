# Interacting with Alerts
The following commands provide interaction with Simvue alerts, including creation of user defined alerts.

## Listing Alerts

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
|`--auto`|Show if alert tag auto-assign is enabled.|`False`|
|`--alert-tags`|Show tags automatically assigned from alerts.|`False`|
|`--enabled`|Show if alert is enabled.|`False`|
|`--source`|Show alert source.|`False`|
|`--notification`|Show notification setting.|`False`|
|`--abort`|Show if alert can abort alerts.|`False`|
|`--name`|Display the name of each alert.|`False`|
|`--created`|Display the created timestamp.|`False`|
|`--description`|Display the description for each alert.|`False`|
|`--sort-by`|Column to sort by `created`, `started`, `endtime`, `modified`, `name`.<br>Can be called more than once.|`['created']`|
|`--reverse`|Reverse the sorting order.|`False`|

!!! example
    
    ```sh
    $ simvue alert list --name --count 5 --format fancy_grid
    ╒════════════════════════╤══════════════════════════════╕
    │ id                     │ name                         │
    ╞════════════════════════╪══════════════════════════════╡
    │ XXXXXXXXXXXXXXXXXXXXX  │ cli_alert_3846f4a1           │
    ├────────────────────────┼──────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ cli_alert_8c88d3f9           │
    ├────────────────────────┼──────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ alert_4                      │
    ├────────────────────────┼──────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ alert_3                      │
    ├────────────────────────┼──────────────────────────────┤
    │ XXXXXXXXXXXXXXXXXXXXX  │ alert_2                      │
    ╘════════════════════════╧══════════════════════════════╛
    ```

## JSON View
All available information for a alert can be obtained using the `json` sub-command:

```sh
simvue alert json <ALERT-ID>
```

this will return a JSON dump of the response from the server for the given alert. 

!!! example "Combining Commands"
    As commands are designed to work together, as an example we can view and query the metadata for the latest Simvue alert using the tool [`jq`](https://jqlang.org/download/) by executing:
    
    ```sh
    simvue alert list --count 1 | simvue alert json | jq '.source'
    ```

## Creating and Removing Alerts


### Creating a User Alert

User alerts can be created on the command line, these are alerts which are manually updated by the user as opposed to being based on metrics or events:

```sh
simvue alert create
```

The command has the following options:

|**Option**|**Description**|**Default**|
|------|-----------|-------|
|`--abort`|The alert can abort runs. |`False`|
|`--description`|Description for the alert.|`None`|
|`--email`|Add email notification to this alert.|`False`|

### Removing an Alert

Alerts can be removed by their identifier:

```sh
simvue alert remove <alert-ID>
```
