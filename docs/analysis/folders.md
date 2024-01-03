# Folders

In a similar way to retrieving runs, methods exist in the `Client()` class for retrieving information about folders. 

## Retrieving Single Folders
The `get_folder` method can be used to obtain details about a specified folder. By default only basic information is returned, which includes:

* Path,
* ID,
* Description,
* Timestamp at which folder was created,
* User which created the folder,
* Number of runs stored in the folder

For example:
```
client.get_folder('/rand_nums')
```
gives:
```
{
  "path": "/rand_nums",
  "created": "2023-12-01 13:58:01.492625",
  "id": "kLwNUm4KXSR7SXUi7TsnAe",
  "user": "my_user",
  "description": 'Stores runs for monitoring random number generation.',
  "runs": 20
}
```
If tags and metadata are also required then the optional arguments `tags` and `metadata` can be set to `True`, for example:
```
client.get_folder('/rand_nums', tags=True, metadata=True)
```
gives:
```
{
  "path": "/rand_nums",
  "created": "2023-12-01 13:58:01.492625",
  "id": "kLwNUm4KXSR7SXUi7TsnAe",
  "user": "my_user",
  "description": 'Stores runs for monitoring random number generation.',
  "runs": 20
  "tags": [
    "random-numbers",
  ],
  "metadata": {
    "environment": 'testing',
  }
}
```
## Retrieving Multiple Folders
Instead of specifying the path of a single folder, filters can be provided with the `get_folders()` method. This returns information on multiple folders.
The output dictionary is in the form of a list, where the information about each folder has the same format as the output from the `get_run` method described above.

For example, to get details of all folders which contain runs which were ran in the 'testing' environment:
```
client.get_folders(['environment' == 'testing'], tags=True, metadata=True)
```

## Deleting Folders
Folders can also be deleted using the `delete_folder()` method. You can select whether to only delete the folder itself, or whether to also recursively delete all of the runs which are stored inside of it, by specifying the `runs` parameter. For example, say we wanted to create a Python script which is executed every day, which checks for any folders which are marked with the `expiring` tag and deletes them (and all runs contained within them) if they are more than 30 days old:

```py
date_30d_ago = datetime.now() - timedelta(days=30)
folders = client.get_folders(['expiring'])

for folder in folders:
    if datetime.strptime(folder['created'], "%Y-%m-%d %H:%M:%S.%f") < date_30d_ago:
            client.delete_folder(folder['path'], runs=True)
```
??? further-docs "Further Documentation"

    - [^^View reference documentation for the get_folder() method^^](/reference/client#get_folder)

    - [^^View reference documentation for the get_folders() method^^](/reference/client#get_folders)
    
    - [^^View reference documentation for the delete_folder() method^^](/reference/client#delete_folder)