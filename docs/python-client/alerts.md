# Alerts

The `add_alert` method can be used to associate an alert with the current run. If the alert definition does not exist it will
be created. The arguments are:

 * `name`: name of the alert
 * `type`: type of alert, which needs to be one of `is above`, `is below`, `is outside range`, `is inside range`
 * `metric`: name of the metric to use
 * `frequency`: how often (in minutes) to calculate the average of the metric
 * `window`: what time period (in minutes) over which to calculate the average of the metric
 * `notification`: type of notification, either `none` (default) or `email`

In addition, for the case of `is above` and `is below`:

 * `threshold`: threshold

and for `is outside range` and `is inside range`:

 * `range_low`: lower limit of range
 * `range_high`: upper limit of range

For example, to create a threshold alert:
```
run.add_alert(name='quality too low',
              type='is below',
              metric='quality',
              frequency=1,
              window=1,
              threshold=0.4)
```
In this case if the 1-minute average of the `quality` metric, calculated at 1-minute intervals, goes below 0.4 the alert will be triggered.

Similarly, here is an example of a range-based alert:
```
run.add_alert(name='density invalid',
              type='is outside range',
              metric='density',
              frequency=1,
              window=1,
              range_low=1.0,
              range_high=5.0)
```
In this case, if the 1-minute average of the `density`, calculated at 1-minute intervals, goes below 1.0 or above 5.0 the alert will be triggered.

If `notification` is set to `email` an email will be sent to the user when the alert first goes critical.
