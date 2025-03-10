# MOOSE Connector

MOOSE is an open source, parallel finite element framework for solving complex multiphysics problems. To make tracking a MOOSE simulation as simple as possible, a connector has been created which can automatically track key metrics from any MOOSE simulation.

!!! further-docs
    To view a detailed example of monitoring a MOOSE simulation using the MooseRun connector, [^^see the example here.^^](/examples/moose)

## What is tracked

By default, the following things are tracked by the `MooseRun` connector:

- Upload the MOOSE input file and application Makefile as input artifacts
- Launch the MOOSE simulation as a process, triggering an alert if it encounters an error or exception
- Upload information from the MOOSE input file as metadata
- Upload information from the top of the console log (MOOSE version, parallelism information, mesh information etc) as metadata
- Upload key information from the console log as events
- Create an alert which notifies the user if a step fails to converge
- Upload any variable values being written to CSV files as metrics
- Add relevant metadata and tags to the run if the [MOOSE Terminator](https://mooseframework.inl.gov/source/userobjects/Terminator.html) stopped the run early
- Once complete, upload the Exodus file as an output artifact

## Usage

To use the `MooseRun` class, you must have the `simvue-moose` package installed. Create a virtual environment if you haven't already:
```
python -m venv venv
source venv/bin/activate
```
Then install the repository using `pip`:
```
pip install simvue-moose
```

You can then use the `MooseRun` class as a context manager, in the same way that you would use the base Simvue `Run` class. Initialize the run, and then call `run.launch()`, passing in the following parameters:

- `moose_application_path`: Path to the compiled MOOSE application
- `moose_file_path`: Path to the MOOSE input file, usually ending in `.i`
- `track_vector_postprocessors`: Whether to track Vector PostProcessor CSV files as metrics (optional, default is False)
- `track_vector_positions`: If tracking Vector PostProcessors is enabled, whether to track the vector positions (x, y, z, or radius) as their own metrics (optional, default is False)
- `moose_env_vars`: A dictionary of any environment variables to pass to the MOOSE application (optional)
- `run_in_parallel`: Whether to use `mpiexec` to run your simulation across multiple processors in parallel (optional, default is False)
- `num_processors`: If running in parallel, the number of processors to use (default is 1)
- `mpiexec_env_vars`: A dictionary of any environment variables to pass to mpiexec on startup if running in parallel (optional)

Your Python script may look something like this:
```py
from simvue_moose.connector import MooseRun

with MooseRun() as run:
   run.init("my_moose_run")

   run.launch(
      "/opt/moose/moose-opt",
      "/home/my_user/moose/moose_input.i",
   )
```

You may also need to edit the `Outputs` section of your MOOSE input file. You need to set the console log to output to a file, and set the `file_base` parameter to `output_directory_path`/`results_prefix`. For example:
```
[Outputs]
file_base = results/output_file
[exodus]
   type = Exodus
[]
[console]
   type = Console
   output_file = true
[]
[csv]
   type = CSV
[]
```
!!! note
      If you wish to use the [MOOSE Terminator](https://mooseframework.inl.gov/source/userobjects/Terminator.html) to stop your runs early when certain conditions are breached, make sure you set the `error_level` parameter to `WARNING` in your MOOSE input file - otherwise Simvue will not be able to detect a run which was terminated early.


## Adding functionality
You can extend your script to upload extra information which is specific to your simulation:

### Adding data before/after the simulation
Since the `MooseRun` class inherits from the base Simvue `Run` class, all of the methods provided by base Simvue are available to use. This means that you can upload any extra data before or after you call the `launch()` method. For example:

```py
from simvue_integrations.connectors.moose import MooseRun

with MooseRun() as run:
   run.init("my_moose_run")

   # Can use any of the base Simvue run methods before calling launch():
   run.update_metadata({"simulation_type": "moose"})
   run.update_tags["moose",]
   run.save_file(os.path.abspath(__file__), "code")
   run.log_event("Starting MOOSE simulation...")

   run.launch(
      "/opt/moose/moose-opt",
      "/home/my_user/moose/moose_input.i",
   )

   # And then can upload anything after the simulation, for example extra results files
   run.save_file("outputs.json", "output")
   run.update_tags["finished",]
```

### Adding files to track during the simulation
If there are extra files being produced by your specific MOOSE simulation which you would like to keep track of in addition to the functionality provided by the base `MooseRun` class, you can create a new class which inherits from `MooseRun` and add extra files to keep track of to the `during_simulation()` method. For example, say that we have a MOOSE simulation which will produce a JSON file which contains some key metadata which we want to have uploaded to our Simvue run. We create a custom class, `MyMooseRun`, as follows:

```py
# Use file parser from multiparser
import multiparser.parsing.file as mp_file_parser

class MyMooseRun:
   def during_simulation(self):
      # Call the 'track' method to the file monitor produced by MooseRun
      # Use the JSON parser, and upload data produced as metadata
      self.file_monitor.track(
         path_glob_exprs = os.path.join(self.output_dir_path, f"{self.results_prefix}.json"),
         callback = lambda data, metadata: self.update_metadata({**data, **metadata}), 
         parser_func = mp_file_parser.record_json, 
         static = True,
      )

      # Then don't forget to call the function from MooseRun to get the default behaviour too!
      super().during_simulation()
```