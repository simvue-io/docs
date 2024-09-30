# Optimisation
In this example, we will use a basic simulation in FDS (Fire Dynamics Simulator) to illustrate how Simvue can be used to reduce the carbon footprint and improve the sustainability of conducting your simulation campaigns.
## Specifying the Problem
For our problem, let's say that we are testing new possible fire sprinkler designs. Let us imagine that we are simulating a simple test rig for this, where a fire starts inside a room of dimensions 5x3x3 metres, and the sprinkler is positioned directly above it. We can vary some parameters about the sprinkler, such as the temperature at which it activates, the diameter of droplets of water which it produces, and the water flow rate. Let us suppose that we want to minimise the volume of water which the sprinkler uses to extinguish a fire, so long as the fire is extinguished within a set time and the temperature in the room does not exceed some defined limits.

The upper and lower bounds for our design parameters are:

| Parameter | Upper Bound | Lower Bound |
|-----------|-------------|-------------|
| Activation Temperature | 60 | 100 |
| Flow Rate | 120 | 200 |
| Droplet Diameter | 300 | 700 |

TODO: Add units ^^


To begin with, we will perform a naive gridsearch over our parameter space to find the optimal values of these parameters. We will use Simvue to reduce the carbon impact of these by investigating possible early 


## Setup
To Do

## Creating our Input File
Details here

## Exploring the Parameter Space
### First Trial
As an initial trial run, we are going to do a small gridsearch of the parameter space, using the upper and lower bounds for each parameter to do a set of 8 runs. To do this, we will create a Python file which simply loops through the two possible values of each parameter, and uses the `FDSRun` class from the `integrations` repository to run the simulation, automatically tracking key parameters inside the simulation. To update the input FDS file with the current set of parameters we will use the `f90nml` module, which allows us to load, edit and save the kind of Fortran file which the FDS input is based on. The python file to do this may look like this:

??? example "Example Simvue Monitoring Script"
    Here is an example Simvue monitoring script - it uses three For loops to create each combination of potential parameters, and `f90nml` to read the existing FDS input file and update it with those parameters. It then uses the `FDSRun` connector class as a context manager, initializes the run, updates metadata corresponding to the parameters used, and then calls `launch()` to perform and track the simulation.
    
    ```py
    import os
    import shutil
    from simvue_integrations.connectors.fds import FDSRun
    import f90nml
    counter = 0
    # Delete old results directory, if present
    if os.path.exists("/workdir/results_sprinkler"):
        shutil.rmtree("/workdir/results_sprinkler")
        
    # Load original input file, so that we can edit it and update values
    input_file = f90nml.read("/workdir/sprinkler.fds")
    # Load the PART corresponding to the water droplets
    part = input_file["part"][0]

    # Loop through possible values:
    for activation_temperature in range(60, 101, 40):
            for flow_rate in range(120, 201, 80):
                    for droplet_diameter in range(300, 701, 400):
                            counter += 1
                            
                            # Create a new FDS input file with current trial parameters
                            part["diameter"] = droplet_diameter
                            patch = {"prop": {"activation_temperature": activation_temperature, "flow_rate": flow_rate}, "part": part}
                            f90nml.patch("/workdir/sprinkler.fds", patch, "/workdir/sprinklers_patched.fds")
                            
                            # Initialise the FDS Connector
                            with FDSRun() as run:
                                # Update the configuration to enable logging of emission metrics during execution
                                run.config(enable_emission_metrics=True,emission_metrics_interval=1)
                                
                                # Initialise the run, giving a run name, the folder to store results in, and tags to help us find it later
                                run.init(f"fds_simulation_sprinklers_{counter}",folder="/fds/sprinklers-gridsearch", tags=["fds", "sprinkler", "gridsearch", "boundaries"])
                                
                                # Store parameters being used in this run as metadata so that we can filter runs later
                                run.update_metadata({
                                    "activation_temperature": activation_temperature,
                                    "flow_rate": flow_rate,
                                    "droplet_diameter": droplet_diameter,
                                })
                                
                                # We can also define useful alerts for parameters which we want to track
                                # For example, lets make sure that the temperature in the room isn't getting above 200C
                                run.create_alert(
                                    name="thermocouple_temp_above_200_degrees",
                                    metric="Ceiling_Thermocouple.Front_Left", # This is the name of the DEVC device to track
                                    source="metrics",
                                    frequency=1,
                                    rule="is above",
                                    threshold=200,
                                )

                                # Launch the FDS simulation, providing the input file and location where you want results to be stored
                                run.launch(
                                    fds_input_file_path = "/workdir/sprinklers_patched.fds",
                                    workdir_path = f"results_sprinkler"
                                    )

                                # Delete the patched FDS file which we created
                                os.remove("/workdir/sprinklers_patched.fds")
        ```

Once these simulations are complete, we can use Simvue to easily inspect the results. Firstly if we open the run UI and filter based on the tags which we assigned these runs (`fds`, `sprinkler`, `gridsearch`, `boundaries`), we can see that of our 8 runs, X triggered an alert due to the temperature at one of the thermocouples in the room:

TODO: Insert picture

### Early Stopping if Temperature Exceeds 200C

Based on the results above, we can add an early stopping feature which stops the simulation early if the temperature recorded by the thermocouples in all four corners of the room exceeds 200 degrees.