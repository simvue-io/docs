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
