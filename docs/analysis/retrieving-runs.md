# Retrieving runs

The Simvue `Client` class can be used to obtain details about runs, including tags and metadata. We first
need to create an instance of this class:
```python
from simvue import Client
client = Client()
```
As with the `Run` class, there must either be a valid `.simvue.ini` file in the user's home directory, a `simvue.ini` file in the current directory or the required environment variables must be defined.

## A single run
The `get_run` method can be used to obtain details about a specified run using its identifier.

For example:
```python
run_id = client.get_run_id_from_name('cool-scene')
client.get_run(run_id)
```

## Multiple runs

Instead of specifying the name of a run, filters can be provided with the `get_runs` method. This returns information on multiple runs.
The output dictionary is in the form of a list, where each run has the same format as the output from the `get_run` method described above.

For example, to get the metadata for all runs in folder `/Burgers_trial` use:
```python
client.get_runs(
  filters=['folder.path == /Burgers_trial'],
  metadata=True
)
```
Any number of filters can be included. For example, here we want to select only runs where metadata attribute `beta` has
a value greater than 2.0:
```python
client.get_runs(
  filters=['folder.path == /Burgers_trial', 'beta > 2.0'],
  metadata=True
)
```

??? further-docs "Further Documentation"

    - [^^The get_run() method^^](/reference/client#get_run)

    - [^^The get_runs() method^^](/reference/client#get_runs)
    
    - [^^Example usage of get_runs() in the Tutorial^^](/tutorial_basic/analysis/#retrieving-runs)