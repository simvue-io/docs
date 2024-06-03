# Configuration

The `config` method can be used to set some configuration options. It should be called before calling `init` which starts a run. All arguments must be stated explicitly as keyword arguments.

* `suppress_errors`: if set to `False` problems with the Simvue client will trigger exceptions. By default this is `True`, ensuring that the main application can run successfully even in the event of misconfiguration or problems with the monitoring.
* `queue_blocking`: when set to `True` the metrics and events queues will block if they become full. By default this is `False`, meaning that metrics and/or events will be silently dropped if either of the queues fills.
* `storage_id`: specify, by identifier, the storage instance to use
* `disable_resources_metrics`: when set to `False` resource usage metrics are not collected.
* `resources_metrics_interval`: resource usage metrics are collected at this interval, in seconds. The default is 30 secs.

Example:
```  py
from simvue import Run

with Run() as run:
    run.config(
        queue_blocking=True,
        resources_metrics_interval=5
    )
    run.init()
```
??? further-docs "Further Documentation"

    - [^^The config() method^^](/reference/run/#config)
    
    - [^^Example of configuring a run in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#configuring-the-run)