# Metrics

To log time-series metrics use the `log_metrics` method, for example:
``` py
run.log_metrics({'parameter1': 1.2, 'parameter2': 3.5})
```
The argument is a dictionary consisting of the metric names and their values.

The `log_metrics` method can be called as many times as necessary during a run, and the time of each is recorded with microsecond precision. The
timestamp can be overriden if necessary, for example if the metrics are being extracted from another source with its own timestamps. For example:
```  py
run.log_metrics({'parameter1': 1.2}, timestamp='2021-05-03 14:13:27.281920')
```
In addition to the timestamp the relative time since `init()` was called is also recorded. The relative time can be set manually if needed, e.g.:
```  py
run.log_metrics({'parameter1': 1.2}, time=time)
```
where here `time` is a floating point number.

Furthermore, an integer `step` is recorded for each metric. Typically it represents some measurement of the progress of the simulation.
By default this starts at 0 and increments by 1 each time `log_metrics` is called.
Alternatively it can be defined explicitly, e.g.
```  py
run.log_metrics({'parameter1': 1.2}, step=step)
```

## Naming metrics
It can be useful to employ a *dot notation* for metrics names, as this helps in automatically creating the web UI view of all metrics. Any
metrics where the part of the name before the `.` is the same is displayed in a single panel. For example, metrics with names:

* `residuals.Ux`
* `residuals.Uy`
* `residuals.Uz`

will be displayed on the same panel. However, the following would also be displayed in a single panel:

* `residuals.Ux`
* `residuals.Uy`
* `residuals.Uz`
* `residuals.p`

which might not be what you want. In this case it would be better to use instead:

* `residuals.U.x`
* `residuals.U.y`
* `residuals.U.z`
* `residuals.p`

In this case `residuals.U.x`, `residuals.U.y` and `residuals.U.z` would be displayed in one panel with `residuals.p` in another.

!!! note

    You can of course select exactly what you want to displayed in a metrics plot, but for the default view displaying all metrics in a single page the dot notation is taken into account.
