# Alerts

The `add_alert` method can be used to associate an alert with the current run. If the alert definition does not exist it will
be created. The arguments are:

 * `name`: name of the alert
 * `source`: source for the alert, either `metrics` or `events`
 * `frequency`: how often (in minutes) to check. Must be an integer, any floats provided to this argument will be rounded up
 * `notification`: type of notification, either `none` (default) or `email`

When `source` is set to `metrics`, the following are also required:

 - `rule`: type of alert, which needs to be one of:

    * `is above`,
    * `is below`,
    * `is outside range`,
    * `is inside range`.

 - `metric`: name of the metric to use
 - `window`: what time period (in minutes) over which to calculate the average of the metric. Must be an integer, any floats provided to this argument will be rounded up
And, for the case of `is above` and `is below`:

 * `threshold`: threshold

and for `is outside range` and `is inside range`:

 * `range_low`: lower limit of range
 * `range_high`: upper limit of range

When `source` is set to `events`, the following is also required:

* `pattern`: search for this string in each message

## Examples

Here are some examples, illustrating each type of alert.

### Threshold alert

For example, to create a threshold alert:
``` py
run.add_alert(name='quality too low',
              source='metrics',
              rule='is below',
              metric='quality',
              frequency=1,
              window=1,
              threshold=0.4)
```
In this case if the 1-minute average of the `quality` metric, calculated at 1-minute intervals, goes below 0.4 the alert will be triggered.

### Range-based alert

Similarly, here is an example of a range-based alert:
``` py
run.add_alert(name='density invalid',
              source='metrics',
              rule='is outside range',
              metric='density',
              frequency=2,
              window=2,
              range_low=1.0,
              range_high=5.0,
              notification='email')
```
In this case, if the 2-minute average of the `density`, calculated at 2-minute intervals, goes below 1.0 or above 5.0 the alert will be triggered.
Here we set `notification` to `email`, so that an email will be sent to the user when the alert first goes critical.

### Alert based on events

Finally, in this example we trigger an alert if the string `error` appears in an event message and send an email when this first happens:
``` py
run.add_alert(name='error detector',
              source='events',
              frequency=1,
              pattern='error',
              notification='email')
```
??? further-docs "Further Documentation"

    - [^^The add_alert() method^^](/reference/run/#add_alert)

    - [^^Example of creating a range based alert in the Tutorial^^](/tutorial/tracking-and-monitoring/#alerts-based-on-metrics)
    
    - [^^Example of creating an events based alert in the Tutorial^^](/tutorial/tracking-and-monitoring/#alerts-based-on-events)