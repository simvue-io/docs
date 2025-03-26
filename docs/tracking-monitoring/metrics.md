# Metrics

## User-defined metrics

To log time-series metrics use the `log_metrics` method, for example:
``` py
run.log_metrics({'parameter1': 1.2, 'parameter2': 3.5})
```
The argument is a dictionary consisting of the metric names and their values.

The `log_metrics` method can be called as many times as necessary during a run, and the time of each is recorded with microsecond precision. The
timestamp can be overriden if necessary, for example if the metrics are being extracted from another source with its own timestamps. For example:
```  py
run.log_metrics({'parameter1': 1.2}, timestamp='2021-05-03T14:13:27.281920')
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

### Naming metrics
It can be useful to employ a similar prefixes for metric names. The web interface allows you to group metrics with the same prefix together into a single plot. For example, metrics with names:

* `residuals.Ux`
* `residuals.Uy`
* `residuals.Uz`

would be displayed on the same panel. In order to distinguish between sub-categories we can extend this prefix, for example in the following case:

* `residuals.Ux`
* `residuals.Uy`
* `residuals.Uz`
* `residuals.p`

we can separate the components of `U` from `p`:

* `residuals.U.x`
* `residuals.U.y`
* `residuals.U.z`
* `residuals.p`

this resulting in `residuals.U.x`, `residuals.U.y` and `residuals.U.z` being displayed in one panel  `residuals.p` in another.

!!! note

    You can of course select exactly what you want to displayed in a metrics plot, but for the default view displaying all metrics in a single page the dot notation is taken into account.

## Resource usage metrics

Resource usage metrics are collected automatically by the Python client (unless disabled using the `config` method), which consist of:

* `resources/cpu.usage.percent`: CPU usage as a percentage, where 100% indicates one CPU is 100% utilised. For example, 800% indicates
that 8 CPUs are fully utilised.
* `resources/memory.usage`: memory usage in MB.
* `resources/gpu.utilisation.percent.i`: GPU utilisation as a percentage.
* `resources/gpu.memory.percent.i`: GPU memory utilisation as a percentage.

In the above `i` is the GPU index. If multiple GPUs are used metrics will be available for each separately.

By default the resource usage of the Python script itself is monitored (including any processes added by `Run.add_process`). To monitor an external code execution not handled by the client, for example a FORTRAN or C++
simulation code, the (parent) PID needs to be specified using the `set_pid` method of the `Run` class, e.g.
```sh
run.set_pid(18231)
```
Note that resource utilisation metrics are collected for the sum of the parent PID and all children. The PID must be specified before
calling the `init` method.

!!! important

    There is a limitation currently for MPI jobs: only the resource usage of the processes on the node running the Python 
    client will be measured, not any other node (for the case of multi-node jobs). This limitation will hopefully be removed
    in future.

### Emissions Metrics

The Simvue server supports recording of CO2 emission estimates collected as additional metrics by the `simvue.Run` class. The feature makes use of the [CO2 signal API](https://docs.co2signal.com/#introduction) to obtain a CO2 intensity value for user's current region, using values of CPU and GPU percentage utilisation to then calculate a rough estimate for the amount of equivalent CO2 a run has produced.

!!! warning "Relative not absolute comparison"
  The values given by emission metrics should not be taken as accurate representations of the exact CO2 emission. These values are intended only to demonstrate the relative impact different choices can have (e.g. aborting simulations based on termination criteria) in terms of environmental impact.

#### Configuration

To use the feature you will need to provide a CO2 Signal API token available [here](https://www.co2signal.com/), and update your `simvue.toml` configuration file to include an additional `eco` section:

```toml
[eco]
co2_signal_api_token = "..."
```

In addition it is strongly recommended that the configuration reflect the specifications of your system by specifying the CPU and GPU Thermal Design Power (TDP) values, this information can be easily found online. If not specified the arbitrary values of 80W and 130W are used:

```toml
[eco]
co2_signal_api_token = "..."
cpu_thermal_design_power = 75
gpu_thermal_design_power = 120
```

The rate of requests to the CO2 Signal API is limited to 30 per hour, as multiple Simvue runs will utilise the same API token the Python API caches the CO2 intensity value locally only refreshing at the specified interval, the default being every day. This interval can be manually set as either an integer (in seconds) or a time descriptor string using the configuration. The location for the containing file is set to be the `$SIMVUE_OFFLINE_DIRECTORY` (default is `$HOME/.simvue`), this can also be updated:
```toml
[eco]
...
intensity_refresh_interval = "2 days" # or alternatively 172800
local_data_directory = "/home/shared/simvue_cache"
```

Finally you can skip use of the CO2 Signal API altogether by specifying a value for the CO2 intensity within the configuration file:

```toml
[eco]
...
co2_intensity = 0.04
```

#### Enabling for Runs

Emission metrics are disabled by default, but can be enabled using the `config` method:


```python
import simvue

with simvue.Run():
  run.config(enable_emission_metrics=True)
```

#### Offline Run Emissions

For offline runs the currently cached CO2 Signal API value is used to calculate emission estimates. If `simvue_sender` is then called by a system that has internet access this will instead ensure the CO2 intensity value is kept updated. 


??? further-docs "Further Documentation"

    - [^^The log_metrics() method^^](/reference/run/#log_metrics)
    
    - [^^Example of logging metrics in the Tutorial^^](/tutorial_basic/tracking-and-monitoring/#creating-metrics)

    - [^^Simvue sender^^](/tracking-monitoring/getting-started/#worker-nodes-without-outgoing-internet-access)
