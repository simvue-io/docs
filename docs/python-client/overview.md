# Overview

## Initialisation

Firstly import the required class:
```
from simvue import Run
```
and create an instance of the Simvue `Run` object:
```
run = Run()
```
The `init` method needs to be called in order to create a run. The following can be specified but all are optional:

 * `name`: name of the run. If no name is provided a name will be genenerated consisting of two random words (in the form adjective-noun);
 * `metadata`: metadata in the form of a dictionary of key-value pairs;
 * `tags`: tags in the form of a list;
 * `description`: plain text description of the run;
 * `folder`: folder for the run. If none is provided the folder is assumed to be `/`. If the folder doesn't already exist it will be created.
 * `status`: if set to `created` it is assume that the simulation will not immediately start running, e.g. a job has been submitted to a batch system
 * `offline`: if set to `True` then no attempts will be made to contact the remote Simvue server, and everything will be written to disk.

For example:
```
run.init(name='my-first-run',
         metadata={'environment': 'test'},
         tags=['test'],
         description='This is a test',
         folder='/tests')
```

## Tracking queued runs

In HPC environments it's normal for jobs to be submitted to a batch system queue. Queued jobs can also be registered with
Simvue so that they can also be tracked.

Firstly initialise a run with the status set to `created`, e.g.
```
run = Run()
run.init(name=name, status='created')
```
Any required tags, metadata etc can be provided here too. If you want to use the default randomly-generated name, this can be
retrieved using the `name` property, e.g.
```
name = run.name
```

Later, when the simulation can be executed, the `reconnect` method can be used to start the run:
```
run = Run()
run.reconnect(name)
```
At this point the status of the run is changed to `running` and metrics can be collected.

## Updating tags and metadata

In some situations it may be useful to update tags or metadata at later points in the lifetime of a run, not just the start. A simple example could be adding a tag `unconverged` if a simulation fails to converge:
```
run.update_tags(['unconverged'])
```
Any tags specified here will be added to any existing tags.

Metadata can be added in a similar way, for example:
```
run.update_metadata({'status': 'unconverged'})
```
All existing metadata is preserved. If a metadata attribute already exists its value will be replaced.


## Ending the run
To cleanly finish a run:
```
run.close()
```
Any batches of metrics or events not yet sent to the remote server will be sent at this point.

An alternative to this is to use a context manager, for example:
```
with Run() as run:
   run.init(...)

   ...
```
In this case it is not necessary to explicitly run `run.close()`.

If a code crashes without calling `close()` after a few minutes the state of the run will change to `lost`.

## Multiple runs in one code

Sometimes it may be necessary to create multiple Simvue runs from within a single Python code, for example for a parameter
scan. One simple way of doing this is to make use of the context manager as mentioned above:
```
with Run() as run:
   run.init(...)

   ...
```
Each time the above is executed a new Simvue run is created and is automatically closed.
