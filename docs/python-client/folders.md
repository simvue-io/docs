# Folders

If a new folder is specified in `init` we can use `folder_details` to specify more information about the folder, specifically metdata, tags and a description. For
example:
```
run.folder_details('/tests',
                   metadata={'environment': 'testing'},
                   tags=['test'],
                   description='My first tests')
```
All of these are optional so only the information required by the user needs to be set. The folder `tests` will be created if it
does not exist already:
``` mermaid
graph LR
  A[root] --> B[tests];
```

Intermediate folders are created automatically as necessary.
For example, if a name like `/tests/test1/sim` is specified, the folders `tests` and `test1` will be created if they do not already exist.
``` mermaid
graph LR
  A[root] --> B[tests];
  B[tests] --> C[test1];
  C --> D[sim];
```
