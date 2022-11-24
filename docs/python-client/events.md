# Events

Arbitrary text can be logged using the `log_event` method. These can be used for storing log messages, exceptions or any other useful
information. For example:
``` py
try:
    ...
except Exception as exc:
    run.log_event(exc)
    ...
```
The timestamp at which the `log_event` method is called is recorded, and similar to metrics this can be overriden if necessary, for example:
```
run.log_event(message, timestamp='2022-01-03 16:42:30.849617')
```
