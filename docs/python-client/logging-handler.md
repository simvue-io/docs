# Python logging module

Logs from the standard [Python logging module](https://docs.python.org/3/library/logging.html) can be captured. This is done
by adding the Simvue `Handler` to the `logger`, for example:
``` py
from simvue import Run, Handler

run = Run()
run.init()

logger = logging.getLogger(__name__)
logger.addHandler(Handler(run))
```

This enables log messages to be visible in the Simvue UI and alerts can be defined which check for the occurence of
specified string(s) in the logs.

It is important to note that only events which have a serverity above the selected logging level will be displayed in the UI.
The default level for the Python logging module is `logging.WARNING`, so only events of `WARNING`, `ERROR` or `CRITICAL` severities
will be displayed. You can change this for your logger using `logger.setLevel`. For example, to set the level to `DEBUG`:
``` py
logger.setLevel(logging.DEBUG)
```
