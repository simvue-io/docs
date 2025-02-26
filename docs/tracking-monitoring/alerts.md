# Alerts

Alerts can be defined and associated with runs. If the alert definition does not exist it will
be created. There are three main categories of alert which can be defined:

## Metrics Alerts

These are alerts relating to the value of a given metric and fall under two sub-types:

### Metric Threshold Alerts

A metric threshold alert is triggered when a metric has a value that exceeds a specified threshold. The function `create_metric_threshold_alert` takes the arguments:

 * `name`: name of the alert
 * `frequency`: how often (in minutes) to check. Must be an integer, any floats provided to this argument will be rounded up
 * `notification`: type of notification, either `none` (default) or `email`
 * `threshold`: threshold value
 - `rule`: type of alert, which needs to be one of:

    * `is above`,
    * `is below`,
 - `metric`: name of the metric to use
 - `window`: what time period (in minutes) over which to calculate the average of the metric. Must be an integer, any floats provided to this argument will be rounded up
For example, to create a threshold alert:

#### Example
```python
run.create_metric_threshold_alert(
   name='quality too low',
   rule='is below',
   metric='quality',
   frequency=1,
   window=1,
   threshold=0.4
)
```

### Metric Range Alerts

A metric range alert is triggered when a metric value either falls or lies outside of a specified value range. The function `create_metric_range_alert` takes the arguments:

 * `name`: name of the alert
 * `frequency`: how often (in minutes) to check. Must be an integer, any floats provided to this argument will be rounded up
 * `notification`: type of notification, either `none` (default) or `email`
 * `range_low`: lower limit of range
 * `range_high`: upper limit of range
 - `rule`: type of alert, which needs to be one of:

    * `is outside range`,
    * `is inside range`.
 - `metric`: name of the metric to use
 - `window`: what time period (in minutes) over which to calculate the average of the metric. Must be an integer, any floats provided to this argument will be rounded up

```python
run.create_metric_range_alert(
   name='density invalid',
   rule='is outside range',
   metric='density',
   frequency=2,
   window=2,
   range_low=1.0,
   range_high=5.0,
   notification='email'
)
```

## Event Alerts

These alerts are triggered based on pattern matching on the message associated with a logged event. The function `create_event_alert` takes the following arguments:

 * `name`: name of the alert
 * `frequency`: how often (in minutes) to check. Must be an integer, any floats provided to this argument will be rounded up
 * `notification`: type of notification, either `none` (default) or `email`
* `pattern`: search for this string in each message

### Example

``` py
run.create_event_alert(
   name='error detector',
   frequency=1,
   pattern='error',
   notification='email'
)
```

### Manual alert

Finally, manually triggered alerts can also be created. In order to set the alert status at a later point we need to store the identifier:

```py
alert_id = run.create_user_alert(name='manual alert')
...
run.log_alert(alert_id, 'ok' if success else 'critical')
```

### Aborting on alert

By default alerts are raised but no action is taken on the simulation. In cases where a simulation should be aborted if an alert is raised
the argument `trigger_abort` should be set:

```py
run.create_user_alert(
  name='abortable_alert',
  trigger_abort=True
)
```

this argument can be used for any of the alert types above.

??? further-docs "Further Documentation"

    - [^^The create_metric_threshold_alert() method^^](/reference/run/#create_metric_threshold_alert)

    - [^^The create_metric_range_alert() method^^](/reference/run/#create_metric_range_alert)

    - [^^The create_event_alert() method^^](/reference/run/#create_event_alert)

    - [^^The create_user_alert() method^^](/reference/run/#create_user_alert)

    - [^^Example of creating a range based alert in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#alerts-based-on-metrics)
    
    - [^^Example of creating an events based alert in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#alerts-based-on-events)
