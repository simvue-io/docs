# Obtaining data

If a simulation or processing step needs to read output (or input) data from an existing run in Simvue
and the data isn't already available then it will be first necessary to download the required data.

In order to download artifacts we first need to create an instance of the Simvue `Client` class:
```
from simvue import Client
client = Client()
```
As with the `Run` class, there must be a valid `.simvue.ini` file in the user's home directory, a `simvue.ini` file in
the current directory or the required environment variables must be defined.

## Downloading a named artifact

The method `get_artifact_as_file` can be used to download a single named artifact from an exsting run. For example:
```
client.get_artifact_as_file(run_name, artifact_name, path='/tmp')
```
will download `artifact_name` from run `run_name` into `/tmp`.
If a path is not provided the file will be downloaded into the current working directory.

## Downloading multiple artifacts

The method `get_artifacts_as_files` can be used to download multiple artifacts from an existing run. For example:
```
client.get_artifacts_as_files(run_name, path='/tmp')
```
will download all artifacts from run `run_name` into `/tmp`.

!!! note

    If any artifacts already exist in the appropriate location they will not be re-downloaded.

A category can be specified in order to restrict which files are
downloaded, for example:
```
client.get_artifacts_as_files(run_name, path='/tmp', category='output')
```
There are additional optional arguments for further restricting what files are downloaded:

* `startswith`: only files which begin with the specified text,
* `contains`: only files which contain the specified text,
* `endswith`: only files which end with the specified text.

These can be combined with specification of a `category`. For example, to download all input files starting with `system/`:
```
client.get_artifacts_as_files(run_name, category='input', startswith='system/')
```

## Simple example

Here is a simple example where we download all output artifacts from `run1` and use them as input into `run2`.
```
from simvue import Client, Run

# Download output files from previous run
client = Client()
client.get_artifacts_as_files('run1', category='output', path='data')

# Create a new run
run = Run()
run.init('run2')
run.save_directory('data', 'input')
...
run.close()
```
It's important to note that the `save_directory` step will not upload and store the same files again if they already exist in Simvue.
Instead they will automatically be registered as being associated with `run2` but will not be re-uploaded.
