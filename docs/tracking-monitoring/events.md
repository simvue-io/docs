# Events

Arbitrary text can be logged using the `log_event` method. These can be used for storing log messages, exceptions or any other useful
information. For example:
``` py
try:
    ...
except Exception as exc:
    run.log_event(str(exc))
    ...
```
The timestamp at which the `log_event` method is called is recorded, and similar to metrics this can be overriden if necessary, for example:
```python
run.log_event(message, timestamp='2022-01-03T16:42:30.849617')
```
??? further-docs "Further Documentation"

    - [^^The log_event() method^^](/reference/run/#log_event)
    
    - [^^Example of logging events in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#logging)