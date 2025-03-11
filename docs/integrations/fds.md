# FDS Connector

FDS (Fire Dynamics Simulator) is an open source simulation code for low-speed flows, with an emphasis on smoke and heat transport from fires. To make tracking an FDS simulation as simple as possible, a connector has been created which can automatically track key metrics from any FDS simulation.

!!! further-docs
    To view a detailed example of monitoring an FDS simulation using the FDSRun connector, [^^see the example here.^^](/examples/fds)

## What is tracked

By default, the following things are tracked by the `FDSRun` connector:

- Upload your FDS input file as an input artifact
- Upload information from the FDS input file as metadata
- Track the log file, uploading data produced as metadata and events
- Track variables values output in the DEVC and HRR CSV files after each step, logging them as metrics
- Track the DEVC and CTRL log, recording activations as metadata and events
- Upload selected results files as Output artifacts

## Usage

To use the `FDSRun` class, you must have the `simvue_fds` package installed. Create a virtual environment if you haven't already:
```
python -m venv venv
source venv/bin/activate
```
Then install the repository using `pip`:
```
pip install simvue-fds
```

You can then use the `FDSRun` class as a context manager, in the same way that you would use the base Simvue `Run` class. Initialize the run, and then call `run.launch()`, passing in the following parameters:

- `fds_input_file_path`: Path to the FDS input file. It is typically best practice to specify the full path to the file so that the run can find it, especially if specifying a different working directory below.
- `workdir_path`: Path to the directory where results will be stored - will be created if it does not already exist. Optional, uses the current working directory by default.
- `clean_workdir`: Whether to remove FDS results files from the working directory provided above. Optional, by default False
- `upload_files`: A list of results file names to be uploaded as Output artifacts - optional, will upload all results files if not specified
- `ulimit`: Value to set the stack size to - for Linux, this should be kept at the default value of 'unlimited'
- `fds_env_vars`: A dictionary of any environment variables to pass to the FDS application on startup (optional)
- `run_in_parallel`: Whether to use MPI to run the FDS job in parallel, by fdefault False
- `num_processors`: If running in parallel, the number of processors to use, by default 1
- `mpiexec_env_vars`: Environment variables to pass to `mpiexec` if running in parallel

Your Python script may look something like this:
```py
from simvue_fds.connector import FDSRun

with FDSRun() as run:
   run.init("my_fds_run")

   run.launch(
      "/path/to/my_input_file.fds",
      "/results",
      ['my_output.smv'],
   )
```
## Adding functionality
You can extend your script to upload extra information which is specific to your simulation:

### Adding data before/after the simulation
Since the `FDSRun` class inherits from the base Simvue `Run` class, all of the methods provided by base Simvue are available to use. This means that you can upload any extra data before or after you call the `launch()` method. For example:

```py
from simvue_integrations.connectors.fds import FDSRun

with FDSRun() as run:
   run.init("my_fds_run")

   # Can use any of the base Simvue run methods before calling launch():
   run.update_metadata({"simulation_type": "fds"})
   run.update_tags["fds","warehouse"]
   run.save_file(os.path.abspath(__file__), "code")

   run.launch(
      "/path/to/my_input_file.fds",
      "/results",
      ['my_output.smv'],
   )

   # And then can use any of the base Simvue run methods after the simulation
   run.update_tags["finished",]
```

### Adding files to track during the simulation
If there are extra files being produced by your specific FDS simulation which you would like to keep track of in addition to the functionality provided by the base `FDSRun` class, you can create a new class which inherits from `FDSRun` and add extra files to keep track of to the `during_simulation()` method. For example, say that we want to look out for the file ending in `_git.txt`, which contains the Git version of FDS being used, and upload that information as a piece of metadata. We create a custom class, `MyFDSRun`, as follows:

```py
# Use file parser from multiparser
import multiparser.parsing.file as mp_file_parser

# Create a custom parser for the Git file - simply read it and return the value as a dictionary
@mp_file_parser.file_parser
def _git_file_parser(
    input_file: str,
    **_) -> typing.Dict[str, str]:

    # Open the file, and read the version
    with open(input_file) as file:
        file_lines = file.readlines()

   # Return a dictionary of metadata about the file (empty in our case), and a dictionary of data from the file
    return {}, {"fds_git_version": file_lines[0]}

class MyFDSRun:
   def during_simulation(self):
      # Call the 'track' method to the file monitor produced by FDSRun
      # Use the custom parser which we have created to read the file
      # Upload the information returned from the file as metadata to the Simvue run
      self.file_monitor.track(
         path_glob_exprs = f"{self._results_prefix}_git.txt",
         callback = lambda data, _metadata_: self.update_metadata(data), 
         parser_func = _git_file_parser
         static = True,
      )

      # Then don't forget to call the function from MooseRun to get the default behaviour too!
      super().during_simulation()
```