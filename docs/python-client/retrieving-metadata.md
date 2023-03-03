# Retrieving metadata

The Simvue `Client` class can be used to obtain details about runs, including tags and metadata. We first
need to create an instance of this class:
```
from simvue import Client
client = Client()
```
As with the `Run` class, there must either be a valid `.simvue.ini` file in the user's home directory, a `simvue.ini` file in the current directory or the required environment variables must be defined.

## A single run
The `get_run` method can be used to obtain details about a specified run. By default only basic information is returned, which includes:
* name,
* current status,
* folder,
* timestamps (e.g. created, started, ended)

For example:
```
client.get_run('cool-scene')
```
gives:
```
{
  "name": "cool-scene",
  "status": "completed",
  "folder": "/Burgers_trial",
  "created": "2023-03-03 09:36:34.003906",
  "ended": "2023-03-03 09:36:53.966751",
  "started": "2023-03-03 09:36:34.003906"
}
```
If tags and metadata are also required then the optional arguments `tags` and `metadata` can be set to `True`, for example:
```
client.get_run('cool-scene', tags=True, metadata=True)
```
gives:
```
{
  "name": "cool-scene",
  "status": "completed",
  "folder": "/Burgers_trial",
  "created": "2023-03-03 09:36:34.003906",
  "ended": "2023-03-03 09:36:53.966751",
  "started": "2023-03-03 09:36:34.003906",
  "tags": [
    "Burgers1D",
    "Spectral"
  ],
  "metadata": {
    "alpha": -1.6485646847026731,
    "beta": 1.309960396151581,
    "discretisation": 1000,
    "domain length": 2,
    "dt": 0.0025,
    "gamma": 2.1133877980965643,
    "iterations": 500,
    "viscosity": 0.002
  }
}
```
The argument `system` can also be set to `True` in order to return information about the system the run executed on.

## Multiple runs

Instead of specifying the name of a run, filters can be provided with the `get_runs` method. This returns information on multiple runs.
The output dictionary is in the form of a list, where each run has the same format as the output from the `get_run` method described above.

For example, to get the metadata for all runs in folder '/Burgers_trial' use:
```
data = client.get_runs(['/Burgers_trial'], metadata=True)
```
