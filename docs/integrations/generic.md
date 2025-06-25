# Custom Connector

When integrating Simvue with a new Non-Python simulation software, a connector to the Simvue `Run` class must be created which adds functionality for tracking any generic run for this software. This connector should inherit from the generic `WrappedRun` class.

For monitoring generic simulations (which are not Python based), we will typically parse log and results files as they are written by the simulation. We do this using the `multiparser` module - [^^see here for full documentation.^^](https://ukaea.github.io/Multiparser/) You can also view an example of using Multiparser with Simvue to track a simulation [^^in the advanced tutorial^^](/tutorial_advanced/introduction).
## WrappedRun

The `WrappedRun` class is included in the `simvue-connector` package. To get this functionality, create a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Then install the `simvue-connector` package:
```
pip install simvue-connector
```

This class contains four methods, which should be overriden with the functionality for tracking your specific simulation.

### The pre_simulation method

The `pre_simulation` method is called when the `launch()` method is called, but before the file monitor is started. This means that it should include:

- Upload of any input or code files
- Adding any tags or metadata which are present before the simulation begins
- Creating alerts
- Logging events messages required before the simulation begins
- Adding the process for the simulation, using parameters which will be input into the `launch` method

Because this class inherits from the base Simvue `Run` class, all methods associated with that are available through `self`.

You should also call the functionality from the `WrappedRun` class at the top of your method - this creates a trigger which can be used to abort the file monitor, and checks that a simvue Run has been initialized before the `launch` method was called.

```py
from simvue_connector.connector import WrappedRun

class MyWrappedRun(WrappedRun):
    def pre_simulation(self):
        """Simvue commands which are ran before the simulation begins.
        """
        super().pre_simulation()

        self.save_file(self.input_file_path, "input")
    
        # Run my custom simulation
        self.add_process(
            identifier='moose_simulation',
            executable=str(self.application_path),
            i=str(self.input_file_path),
            )
        ...
```

### The during_simulation method

The `during_simulation` method is called when the `launch()` method is called, and within the `self.file_monitor` context manager. This is an instance of the `FileMonitor` class from `multiparser`, which monitors any files which you wish to track. You should include all of your `multiparser` code inside this method, eg:

- Calls to the `.track()` method, detailing a file to read and the methods or functions used to process and upload data from it
- Calls to the `.tail()` method, detailing a file to read line by line as it is written and the methods or functions used to process and upload data from it

As an example, if we wanted to read a results CSV file line by line as it is written, and upload the data received as metrics, we would first need to create a new method which defines what happens when a new line is written to the file:
```py
class MyWrappedRun(WrappedRun):
    def _per_metric_callback(self, csv_data: typing.Dict[str, float], sim_metadata: typing.Dict[str, str]):
        """Monitor each line in the results CSV file, and add data from it to Simvue Metrics.
        """
        metric_time = csv_data.pop('time')

        # Log all results for this timestep as Metrics
        self.log_metrics(
            csv_data,
            time = metric_time,
            timestamp = sim_metadata['timestamp']
        )
```

and then in our `during_simulation` method, we create a call to the `tail()` method of `self.file_monitor`, specifying the file to read and the callback to use:
```py
class MyWrappedRun(WrappedRun):
    def during_simulation(self):
        """Describes which files should be monitored during the simulation by Multiparser
        """
        # Monitor each line added to the results file as the simulation proceeds, and upload results to Simvue
        self.file_monitor.tail(
            path_glob_exprs = ["results.csv",],
            parser_func = multiparser.parsing.tail.record_csv,
            callback = self._per_metric_callback
        )
```

### The post_simulation method

The `post_simulation` method is called when the `launch()` method is called, but after the file monitor is finished. This means that it should include:

- Upload of any output files
- Adding any tags or metadata which are generated after the simulation finishes
- Logging events messages required after the simulation finishes

Because this class inherits from the base Simvue `Run` class, all methods associated with that are available through `self`.

```py
class MyWrappedRun(WrappedRun):
    def post_simulation(self):
        """Simvue commands which are ran after the simulation finishes.
        """
        self.log_event("Simulation complete!")
        self.update_tags(["finished",])
        ...
```

### The launch method
The `launch` method is the overall method which starts the file monitor and calls the three methods above. This should be overriden to require the user to provide any inputs relevant to running the simulation, for example the path to an executable, the path of an input file, and/or the path of an output directory.

Once you have created your set of required parameters, make sure to call the parent `launch` method:

```py
class MyWrappedRun(WrappedRun):
    @pydantic.validate_call
    def launch(
        self, 
        application_path: pydantic.FilePath,
        input_file_path: pydantic.FilePath,
    ):
    self.application_path = application_path
    self.input_file_path = input_file_path
    
    super().launch()
```