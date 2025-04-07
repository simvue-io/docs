# Administration
For administrators additional commands are available to handle management of users and tenants within the Simvue server.

## Creating, Viewing and Removing Tenants

### Listing Tenants
To list tenants on the server execute:

```sh
simvue admin tenant list
```

By default this will return only the identifiers of the first 20 tenants in descending order of creation time. The command
features a number of flags which can be used to expand on this information:

|**Option**    |**Description**|**Default**|
|------|-----------|-------|
|`--format`|Display format of table, see help string.|`plain`|
|`--enumerate`|Adds an additional enumeration column to the output.|`False`|
|`--count`|Set the number of results to return.|`20`|
|`--max-runs`|Display the run quota for teach tenant.|`False`|
|`--max-data-volume`|Display the data volume quota for each tenant.|`False`|
|`--name`|Display the tenant name.|`False`|
|`--created`|Display the created timestamp.|`False`|
|`--enabled`|Display whether the tenant is enabled.|`False`|

!!! example

    ```sh
    $ simvue admin tenant list --name --format fancy_grid
    ╒════════════════════════╤══════════════════════════════════════════════╕
    │ id                     │ name                                         │
    ╞════════════════════════╪══════════════════════════════════════════════╡
    │ XXXXXXXXXXXXXXXXXXXXXX │ local                                        │
    ╘════════════════════════╧══════════════════════════════════════════════╛
    ```

### JSON View
All available information for a run can be obtained using the `json` sub-command:

```sh
simvue admin tenant json <TENANT-ID>
```

this will return a JSON dump of the response from the server for the given tenant. 


!!! example "Combining Commands"

    As commands are designed to work together, as an example we can view and query the metadata for the latest Simvue tenant using the tool [`jq`](https://jqlang.org/download/) by executing:

    ```sh
    simvue admin tenant list --count 1 | simvue admin tenant json | jq '.max_runs'
    ```
### Creating a New Tenant

A new tenant can be created on the current Simvue tenant by running the command:

```sh
simvue admin tenant add NAME
```

This will return the unique identifier for the created tenant, additional options are:

|**Option**|**Description**|**Default**|
|------|-----------|-------|
|`--disabled`|Tenant is disabled on creation.|`False`|
|`--max-runs`|Run quota for the tenant.|`None`|
|`--max-request-rate`|The request rate limit for the tenant.|`None`|
|`--max-data-volume`|The data volume quote for the tenant.|`None`|


### Removing a Tenant

To remove a tenant from the server run:

```sh
simvue admin tenant remove <TENANT-ID>
```


## Creating, Viewing and Removing Users
### Listing Users
To list users on the server execute:

```sh
simvue admin user list
```

By default this will return only the identifiers of the first 20 users in descending order of creation time. The command
features a number of flags which can be used to expand on this information:

|**Option**    |**Description**|**Default**|
|------|-----------|-------|
|`--format`|Display format of table, see help string.|`plain`|
|`--enumerate`|Adds an additional enumeration column to the output.|`False`|
|`--count`|Set the number of results to return.|`20`|
|`--full-name`|Display full name of user.|`False`|
|`--email`|Display email of user.|`False`|
|`--manager`|Display whether user has manager privileges.|`False`|
|`--enabled`|Display if user is enabled.|`False`|
|`--deleted`|Display if user has been deleted.|`False`|
|`--read-only`|Display if user has read-only access.|`False`|

!!! example

    ```sh
    $ simvue admin user list --full-name --format fancy_grid
    ╒════════════════════════╤══════════════════════════════════════════════╕
    │ id                     │ fullname                                     │
    ╞════════════════════════╪══════════════════════════════════════════════╡
    │ XXXXXXXXXXXXXXXXXXXXXX │ Joe Bloggs                                   │
    ╘════════════════════════╧══════════════════════════════════════════════╛
    ```

### JSON View
All available information for a run can be obtained using the `json` sub-command:

```sh
simvue admin user json <user-ID>
```

this will return a JSON dump of the response from the server for the given user. 


!!! example "Combining Commands"

    As commands are designed to work together, as an example we can view and query the metadata for the latest Simvue user using the tool [`jq`](https://jqlang.org/download/) by executing:

    ```sh
    simvue admin user list --count 1 | simvue admin user json | jq '.fullname'
    ```
### Creating a New User
A new user can be created on the current Simvue user by running the command:

```sh
simvue admin user add --email <USER-EMAIL> --full-name <USER-FULL-NAME> --tenant <USER-TENANT-ID> USERNAME
```

This will return the unique identifier for the created user, additional options are:

|**Option**|**Description**|**Default**|
|------|-----------|-------|
|`--disabled`|User is disabled on creation.|`False`|
|`--admin`|User to be granted adminstrative access.|`False`|
|`--manager`|User to be registered as a server manager.|`False`|
|`--read-only`|User has read-only access to server data.|`False`|
|`--welcome`|Enabled welcome message on creation.|`False`|


