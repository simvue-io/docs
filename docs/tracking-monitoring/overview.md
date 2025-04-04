# Overview

## Initialisation

Firstly import the required class:
```python
from simvue import Run
```
and create an instance of the Simvue `Run` object, it is recommended to use the context manager:
```python
with Run() as run:
```
There is an optional `mode` argument to `Run()` which has the following options:

* `online`: (default) everything is sent directly to the remote Simvue server;
* `offline`: no attempts will be made to contact the remote Simvue server, and everything will be written to disk. This is most useful for HPC worker nodes which have no outgoing network access;
* `disabled`: completely disables all monitoring, and as such maybe useful for testing.

The `init` method needs to be called in order to create a run. The following can be specified but all are optional:

 * `name`: name of the run. If no name is provided a name will be genenerated consisting of two random words (in the form adjective-noun);
 * `metadata`: metadata in the form of a dictionary of key-value pairs, where the keys are strings and values can be integers, floating point numbers or strings;
 * `tags`: tags in the form of a list of strings;
 * `description`: plain text description of the run;
 * `folder`: folder for the run. If none is provided the folder is assumed to be `/`. If the folder doesn't already exist it will be created.
 * `notification`: whether to send an email to the user when the run finishes, either `'none'` (default), `'all'` (always send an email on run completion), `'error'` (only email if the run finished in an error state) or `'lost'` (only email if the run finished an a lost state).
 * `running`: if set to `False` it is assume that the simulation will not immediately start running, e.g. a job has been submitted to a batch system. When the job starts running it is necessary to reconnect to the run (see below).
 * `retention_period`: the retention period for this run, this is a time description string consisting of an integer value followed by a unit fo time e.g. `'1 hour'`, `'5 days'` etc. Default of `None` removes the lifetime constraint.
 * `timeout`: the period of time which a run will stay active on the server, after which (if no heartbeat is sent by the client) the run will enter the 'lost' state, default is 180s.
 * `visibility`: visibility of this run to other users, by default a run is private:
      - `'tenant'`: run is visible to all users within current user's tenant group.
      - `'public'`: run is publicly viewable to all within the server.
      - A list of user names.
      * `no_color`: disable colors in terminal logging, default False.

For example:
```python
run.init(
   name='my-first-run',
   metadata={'environment': 'test'},
   tags=['test'],
   description='This is a test',
   folder='/tests',
   running=True,
   retention_period='1 hour',
   resources_metrics_interval=120,
   visibility=['jbloggs']
)
```

## Tracking queued runs

In HPC environments it's normal for jobs to be submitted to a batch system queue. Queued jobs can also be registered with
Simvue so that they can also be tracked.

Firstly initialise a run with `running` set to `False`, i.e.
```python
with Run() as run:
   run.init(name=name, running=False)
```
Any required tags, metadata etc can be provided here too. If you want to use the default randomly-generated name, this can be
retrieved using the `name` property, e.g.
```python
name = run.name
```

Later, when the simulation can be executed, the `reconnect` method can be used to start the run:
```python
with Run() as run:
   run.reconnect(name)
```
At this point the status of the run is changed to `running` and metrics can be collected.

## Updating tags and metadata

In some situations it may be useful to update tags or metadata at later points in the lifetime of a run, not just the start. A simple example could be adding a tag `unconverged` if a simulation fails to converge:
```python
run.update_tags(['unconverged'])
```

alternatively if you wish to instead overwrite the existing tags for this run:
```python
run.set_tags(['unconverged'])
```

Metadata can be added in a similar way, for example:
```python
run.update_metadata({'status': 'unconverged'})
```
All existing metadata is preserved. If a metadata attribute already exists its value will be replaced.


## Ending the run
If using the context manager the run will close automatically and the state of the run will be set to either "completed" or "failed" depending on whether or not the code exited correctly. Any batches of metrics or events not yet sent to the remote server will be sent at this point.

If the context manager is not used, you must ensure the `close` method is closed to correctly terminate monitoring:
```python
run.close()
```
If the method is not called the run will eventually be set to a state of "lost".


## Multiple runs in one code

Sometimes it may be necessary to create multiple Simvue runs from within a single Python code, for example for a parameter
scan. One simple way of doing this is to make use of the context manager as mentioned above:
```python
with Run() as run:
   run.init(...)

   ...
```
Each time the above is executed a new Simvue run is created and is automatically closed.

## Disabling monitoring

During testing it might be useful to disable monitoring by Simvue. To do this, use:
```python
with Run(mode='disabled') as run:
```

??? further-docs "Further Documentation"

    - [^^The init() method^^](/reference/run/#init)

    - [^^The close() method^^](/reference/run/#close)

    - [^^The update_tags() method^^](/reference/run/#update_tags)

    - [^^The update_metadata() method^^](/reference/run/#update_metadata)
    
    - [^^Example of initializing a run in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#initialising-the-run)

    - [^^Example of adding metadata and tags in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#metadata-and-tags)
