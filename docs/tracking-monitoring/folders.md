# Folders

If a new folder is specified in `init` we can use `set_folder_details` to specify more information about the folder, specifically metdata, tags and a description. For
example:
```  py
run.set_folder_details('/tests',
                       metadata={'environment': 'testing'},
                       tags=['test'],
                       description='My first tests')
```
All of these are optional so only the information required by the user needs to be set. The folder `tests` will be created if it
does not exist already:
``` mermaid
graph LR
  A[root] --> B[tests];
  style A fill:#A7C7E7,stroke: #A7C7E7;
  style B fill:#A7C7E7,stroke: #A7C7E7;
```

Intermediate folders are created automatically as necessary.
For example, if a name like `/tests/test1/sim` is specified, the folders `tests` and `test1` will be created if they do not already exist.
``` mermaid
graph LR
  A[root] --> B[tests];
  B[tests] --> C[test1];
  C --> D[sim];
  style A fill:#A7C7E7,stroke: #A7C7E7;
  style B fill:#A7C7E7,stroke: #A7C7E7;
  style C fill:#A7C7E7,stroke: #A7C7E7;
  style D fill:#A7C7E7,stroke: #A7C7E7;
```
??? further-docs "Further Documentation"

    - [^^View reference documentation for the set_folder_details() method^^](/reference/run/#set_folder_details)
    
    - [^^View an example of adding details to folders in the Tutorial^^](/tutorial/tracking-and-monitoring/#add-information-for-folders)