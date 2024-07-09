# OpenFOAM Wrapper

OpenFOAM is an open source Computational Fluid Dynamics solver. To make tracking an OpenFOAM simulation as simple as possible, a wrapper has been created which can automatically track key metrics from any OpenFOAM simulation.

!!! further-docs
    To view a detailed example of monitoring an OpenFOAM simulation using the OpenfoamRun wrapper, [^^see the example here.^^](/examples/openfoam)

## What is tracked

By default, the following things are tracked by the `OpenfoamRun` wrapper:

- Uploads the input files stored in the `Constant` and `System` directories, as well as the initial conditions in the `0` directory, as `input` artifacts
- Uploads the `Allrun` script as a `code` artifact
- Uploads information from the top of the log files, such as the OpenFOAM build used, as metadata
- Uploads information from the log files before the solve begins to the events log
- Tracks the residuals being calculated for each parameter as metrics
- Once complete, uploads all of the outputs for each time step as `output` artifacts

## Usage

To use the `OpenfoamRun` class, you must have the `simvue_integrations` repository installed. Create a virtual environment if you haven't already:
```
python -m venv venv
source venv/bin/activate
```
Then install the repository using `pip`:
```
pip install git+https://github.com/simvue-io/integrations.git
```

You can then use the `OpenfoamRun` class as a context manager, in the same way that you would use the base Simvue `Run` class. Initialize the run, and then call `run.launch()`, passing in the following parameters:

- `openfoam_case_dir`: Path to the OpenFOAM case directory, containing an AllRun script and all required inputs
- `upload_as_zip`: Whether to upload inputs and outputs as `zip` archive files, or instead upload each file individually. Default is True.
- `openfoam_env_vars`: A dictionary of any environment variables to pass to the OpenFOAM application (optional)

Your Python script may look something like this:
```py
from simvue_integrations.wrappers.openfoam import OpenfoamRun

with OpenfoamRun() as run:
   run.init("my_openfoam_run")

   run.launch(
      openfoam_case_dir="/home/openfoam_cases/my_case",
      upload_as_zip=True,
   )
```

## Adding functionality
You can extend your script to upload extra information which is specific to your simulation:

### Adding data before/after the simulation
Since the `OpenfoamRun` class inherits from the base Simvue `Run` class, all of the methods provided by base Simvue are available to use. This means that you can upload any extra data before or after you call the `launch()` method. For example:

```py
from simvue_integrations.wrappers.openfoam import OpenfoamRun

with OpenfoamRun() as run:
   run.init("my_openfoam_run")

   # Can use any of the base Simvue run methods before calling launch():
   run.update_metadata({"simulation_type": "openfoam"})
   run.update_tags["openfoam",]
   run.save_file(os.path.abspath(__file__), "code")
   run.log_event("Starting Openfoam simulation...")

   run.launch(
      openfoam_case_dir="/home/openfoam_cases/my_case",
      upload_as_zip=True,
   )

   # And then can upload anything after the simulation
   run.log_event("Openfoam simulation complete!")
   run.update_tags["finished",]
```

### Adding files to track during the simulation
If there are extra files being produced by your specific OpenFOAM simulation which you would like to keep track of in addition to the functionality provided by the base `OpenfoamRun` class, you can create a new class which inherits from `OpenfoamRun` and add extra files to keep track of to the `during_simulation()` method. For example, say that we have a OpenFOAM simulation which will produce a JSON file which contains some key metadata which we want to have uploaded to our Simvue run. We create a custom class, `MyOpenfoamRun`, as follows:

```py
# Use file parser from multiparser
import import multiparser.parsing.file as mp_file_parser

class MyOpenfoamRun:
   def during_simulation(self):
      # Call the 'track' method to the file monitor produced by OpenfoamRun
      # Use the JSON parser, and upload data produced as metadata
      self.file_monitor.track(
         path_glob_exprs = os.path.join(self.openfoam_case_dir, f"{self.results_prefix}.json"),
         callback = lambda data, metadata: self.update_metadata({**data, **metadata}), 
         parser_func = mp_file_parser.record_json, 
         static = True,
      )

      # Then don't forget to call the function from MooseRun to get the default behaviour too!
      super().during_simulation()
```