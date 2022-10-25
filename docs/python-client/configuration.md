# Configuration

The `config` method can be used to set some configuration options. It should be called before calling `init` which starts a run.

* `suppress_errors`: if set to `True` problems with the Simvue client will trigger exceptions. By default this is `False`, ensuring that the main application can run successfully even in the event of misconfiguration or problems with the monitoring.
* `queue_blocking`: when set to `True` the metrics and events queues will block if they become full. By default this is `False`, meaning that metrics and/or events will be silently dropped if either of the queues fills.
* `queue_size`: maximum numbers of items which can be stored in the metrics and events queues. The default is 10000. For extremely high-frequency metrics or events it might be necessary to increase this number.

Example:
```
from simvue import Simvue
run = Simvue()
run.config(queue_blocking=True, queue_size=20000)
run.init()
```
