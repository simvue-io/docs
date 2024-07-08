# MOOSE Wrapper

MOOSE is an open source, parallel finite element framework for solving complex multiphysics problems. To make tracking a MOOSE simulation as simple as possible, a wrapper has been created which can automatically track key metrics from any MOOSE simulation.

[See here to view a full example of implementing the MooseRun wrapper to track a MOOSE simulation.](/examples/moose)

## What is tracked

By default, the following things are tracked by the `MooseRun` wrapper:

- Upload the MOOSE input file and application Makefile as input artifacts
- Launch the MOOSE simulation as a process, triggering an alert if it encounters an error or exception
- Upload information from the top of the console log (MOOSE version, parallelism information, mesh information etc) as metadata
- Upload key information from the console log as events
- Create an alert which notifies the user if a step fails to converge
- Upload any variable values being written to the CSV file as metrics
- Once complete, upload the Exodus file as an output artifact

## Usage

To use the `MooseRun` class, you must have the `simvue_integrations` repository installed. Create a virtual environment if you haven't already:
```
python -m venv venv
source venv/bin/activate
```
Then install the repository using `pip`:
```
pip install git+https://github.com/simvue-io/integrations.git
```

You can then use the `MooseRun` class as a context manager, in the same way that you would use the base Simvue `Run` class. Initialize the run, and then call `run.launch()`, passing in the following parameters:

- `moose_application_path`: Path to the compiled MOOSE application
- `moose_input_file`: Path to the MOOSE input file, usually ending in `.i`
- `output_dir_path`: Path to the directory where output files are generated and stored
- `results_prefix`: The prefix to all results files
- `moose_env_vars`: A dictionary of any environment variables to pass to the MOOSE application (optional)

Your Python script may look something like this:
```py
from simvue_integrations.wrappers.moose import MooseRun

with MooseRun() as run:
   run.init("my_moose_run")

   run.launch(
      "/opt/moose/moose-opt",
      "/home/my_user/moose/moose_input.i",
      "/home/my_user/moose/results",
      "output_file
   )
```

You may also need to edit the `Outputs` section of your MOOSE input file. You need to set the console log to output to a file, and set the `file_base` parameter to match the parameters you passed in above (ie, it should be `file_base = <output_dir_path>/<results_prefix>). For example:
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
## Adding functionality
You can extend your script to upload extra information which is specific to your simulation:

### Adding data before/after the simulation
Since the `MooseRun` class inherits from the base Simvue `Run` class, all of the methods provided by base Simvue are available to use. This means that you can upload any extra data before or after you call the `launch()` method. For example:

```py
from simvue_integrations.wrappers.moose import MooseRun

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
      "/home/my_user/moose/results",
      "output_file
   )

   # And then can upload anything after the simulation, for example extra results files
   run.save_file("outputs.json", "output")
   run.update_tags["finished",]
```

### Adding files to track during the simulation
If there are extra files being produced by your specific MOOSE simulation which you would like to keep track of in addition to the functionality provided by the base `MooseRun` class, you can create a new class which inherits from `MooseRun` and add extra files to keep track of to the `during_simulation()` method. For example, say that we have a MOOSE simulation which will produce a JSON file which contains some key metadata which we want to have uploaded to our Simvue run. We create a custom class, `MyMooseRun`, as follows:

```py
# Use file parser from multiparser
import import multiparser.parsing.file as mp_file_parser

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