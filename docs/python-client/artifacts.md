# Artifacts

Files, directories or combinations of files and directories can easily be uploaded.

## Saving

### Individual files

Individual files can be saved using the `save` method. One of three categories needs to be specified:

 * `code`: software;
 * `input`: input files;
 * `output`: output files.

For example:
```
run.save('data.png', 'output')
```

An optional `filetype` argument can be used to specify the MIME type of the file. By default the MIME type is determined
autoatically. For example:
```
run.save('in.lj', 'input', 'text/plain')
```

By default the name of the artifact will only be the name of the actual file specified, even if an absolute or relative path is specified.
If the optional argument `preserve_path=True` is added to `save` then paths will be preserved in the names. This can be useful
in situations where the files are naturally grouped together and you want to preserve this information, e.g. `group1/file1` and
`group2/file1`.

### Directories

Multiple files in a directory can be saved using the `save_directory` method which has the same arguments as `save` but
instead of specifying a single filename the name of a directory is specified. A MIME type can be specified but all files
in the directory will be set to the same MIME type.

For example, suppose you have a directory `system` containing the following files:
```
blockMeshDict
controlDict
fvSchemes
fvSolution
meshQualityDict
snappyHexMeshDict
surfaceFeaturesDict
```
Using:
```
run.save_directory('system', 'input', preserve_path=True)
```
will result in 7 artifacts being uploaded with names as follows:
```
system/blockMeshDict
system/controlDict
system/fvSchemes
system/fvSolution
system/meshQualityDict
system/snappyHexMeshDict
system/surfaceFeaturesDict
```

### List of files and/or directories

A list of a combination of files and directories can be provided using the `save_all` method, providing a simple way for saving a group
of files and/or directories. For example:
```
run.save_all(['file1', 'file2', 'directory1'], 'input', preserve_path=True)
```
will save the files `file1` and `file2` in addition to the directory `directory1`.


