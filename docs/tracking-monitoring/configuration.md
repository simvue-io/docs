# Configuration

The `config` method can be used to set some configuration options. It should be called before calling `init` which starts a run.

* `suppress_errors`: if set to `False` problems with the Simvue client will trigger exceptions. By default this is `True`, ensuring that the main application can run successfully even in the event of misconfiguration or problems with the monitoring.
* `queue_blocking`: when set to `True` the metrics and events queues will block if they become full. By default this is `False`, meaning that metrics and/or events will be silently dropped if either of the queues fills.
* `queue_size`: maximum numbers of items which can be stored in the metrics and events queues. The default is 10000. For extremely high-frequency metrics or events it might be necessary to increase this number.
* `disable_resources_metrics`: when set to `False` resource usage metrics are not collected.
* `resources_metrics_interval`: resource usage metrics are collected at this interval, in seconds. The default is 30 secs.

Example:
```  py
from simvue import Run
run = Run()
run.config(queue_blocking=True,
           queue_size=20000,
           resources_metrics_interval=5)
run.init()
```
??? further-docs "Further Documentation"

    - [^^View reference documentation for the config() method^^](/reference/run/#config)
    
    - [^^View an example of configuring a run in the Tutorial^^](/tutorial/tracking-and-monitoring/#configuring-the-run)