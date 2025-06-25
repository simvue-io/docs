# Artifacts

Files, directories or combinations of files and directories can easily be uploaded. Python objects
such as NumPy arrays, PyTorch tensors, Matplotlib or _Plotly_ plots can also be uploaded. For example,
a trained model created by a machine learning framework such as PyTorch or Tensorflow can be directly
saved without being dumped to a file first.

## Saving

### Files

Individual files can be saved using the `save_file` method. One of three categories needs to be specified:

 * `code`: software;
 * `input`: input files;
 * `output`: output files.

For example:
``` py
run.save_file('data.png', 'output')
```

An optional `filetype` argument can be used to specify the MIME type of the file. By default the MIME type is determined
autoatically. For example:
``` py
run.save_file('in.lj', 'input', 'text/plain')
```

By default the name of the artifact will only be the name of the actual file specified, even if an absolute or relative path is specified.
If the optional argument `preserve_path=True` is added to `save_file` then paths will be preserved in the names. This can be useful
in situations where the files are naturally grouped together and you want to preserve this information, e.g. `group1/file1` and
`group2/file1`.

### Python objects

The `save_object` method can be used to save Python objects, including:

* NumPy arrays,
* PyTorch tensors and state_dicts,
* pandas dataframes,
* Matplotlib figures,
* Plotly figures.

One main difference between files and Python objects is that an arbitrary name must be specified when Python objects. For example,
to create and save a NumPy array:
```python
import numpy as np
array = np.array([1, 2, 3, 4, 5])
run.save_object(array, 'input', name='array')
```

In addition, any Python object which can be pickled can also be saved. This requires the `allow_pickle` to be set to `True`.
For example:
```python
dictionary = {'key': 'value'}

run.save_object(
    obj=dictionary,
    category='input', name='dictionary',
    allow_pickle=True
)
```

!!! warning

    The Simvue client uses a Plotly conversion function ([^^see documentation for the Plotly conversion function^^](https://plotly.github.io/plotly.py-docs/generated/plotly.html#plotly.tools.mpl_to_plotly)) to convert Matplotlib figures to Plotly. This function doesn't support all plot types and has limitations ([^^view the limitations of the Plotly conversion function^^](https://community.plotly.com/t/mpl-to-plotly-limitations/14686)).

### Directories

Multiple files in a directory can be saved using the `save_directory` method which has the same arguments as `save_file` but
instead of specifying a single filename the name of a directory is specified. A MIME type can be specified but all files
in the directory will be set to the same MIME type.

For example, suppose you have a directory `system` containing the following files:
```sh
system
├── blockMeshDict
├── controlDict
├── fvSchemes
├── fvSolution
├── meshQualityDict
├── snappyHexMeshDict
├── surfaceFeaturesDict
└── surfaceFeaturesDictblockMeshDict
```
Using:
```python
run.save_directory(
    directory='system',
    category='input',
    preserve_path=True
)
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

### Saving multiple files and/or directories

A set of files and directories can be saved using the `save_all` method. For example:
``` py
run.save_all(
    items=['file1', 'file2', 'directory1'],
    category='input',
    preserve_path=True
)
```
will save the files `file1` and `file2` in addition to the directory `directory1`.

??? further-docs "Further Documentation"

    - [^^The save_file() method^^](/reference/run/#save_file)

    - [^^The save_object() method^^](/reference/run/#save_object)

    - [^^The save_directory() method^^](/reference/run/#save_directory)

    - [^^The save_all() method^^](/reference/run/#save_all)
    
    - [^^Example of saving artifacts in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#artifacts)
