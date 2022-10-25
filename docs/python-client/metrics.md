# Metrics

To log time-series metrics use the `log_metrics` method, for example:
```
run.log_metrics({'parameter1': 1.2, 'parameter2': 3.5})
```
The argument is a dictionary consisting of the metric names and their values.

The `log_metrics` method can be called as many times as necessary during a run, and the time of each is recorded with microsecond precision. The
timestamp can be overriden if necessary, for example if the metrics are being extracted from another source with its own timestamps. For example:
```
run.log_metrics({'parameter1': 1.2}, timestamp='2021-05-03 14:13:27.281920')
```
In addition to the timestamp the relative time since `init()` was called is also recorded. The relative time can be set manually if needed, e.g.:
```
run.log_metrics({'parameter1': 1.2}, time=time)
```
where here `time` is a floating point number.

Furthermore, an integer `step` is recorded for each metric. Typically it represents some measurement of the progress of the simulation.
By default this starts at 0 and increments by 1 each time `log_metrics` is called.
Alternatively it can be defined explicitly, e.g.
```
run.log_metrics({'parameter1': 1.2}, step=step)
```
