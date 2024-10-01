# Optimisation
In this example, we will use a basic simulation in FDS (Fire Dynamics Simulator) to illustrate how Simvue can be used to reduce the carbon footprint and improve the sustainability of conducting your simulation campaigns.
## Specifying the Problem
For our problem, let's say that we are testing new possible fire sprinkler designs. Let us imagine that we are simulating a simple test rig for this, where a fire starts inside a room of dimensions 5x3x3 metres, and the sprinkler is positioned directly above it. We can vary some parameters about the sprinkler, such as the temperature at which it activates, the diameter of droplets of water which it produces, and the water flow rate. Let us suppose that we want to minimise the volume of water which the sprinkler uses to extinguish a fire, so long as the fire is extinguished within a set time and the temperature in the room does not exceed some defined limits.

The upper and lower bounds for our design parameters are:

| Parameter | Upper Bound | Lower Bound |
|-----------|-------------|-------------|
| Activation Temperature ($^oC$) | 60 | 100 |
| Flow Rate ($L/min$) | 120 | 200 |
| Droplet Diameter ($\mu m$) | 300 | 700 |

TODO: Add units ^^


To begin with, we will perform a naive gridsearch over our parameter space to find the optimal values of these parameters. We will use Simvue to reduce the carbon impact of this gridsearch by investigating possible early stopping parameters which can be added to the FDS input file. We will then further improve the sustainability by using the built in Simvue optimisation framework to perform a Bayesian Optimisation of the parameters instead of a gridsearch.


## Setup
To Do

## Creating our Input File
Next we need to setup our FDS problem by creating an input file.

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
                                
                                # Launch the FDS simulation, providing the input file and location where you want results to be stored
                                run.launch(
                                    fds_input_file_path = "/workdir/sprinklers_patched.fds",
                                    workdir_path = f"results_sprinkler"
                                    )

                                # Delete the patched FDS file which we created
                                os.remove("/workdir/sprinklers_patched.fds")
        ```

Once these simulations are complete, we can use Simvue to easily inspect the results. Firstly if we open the run UI and filter by clicking on the tags which we assigned these runs (`fds`, `sprinkler`, `gridsearch`, `boundaries`), we can visualise our eight runs in this gridsearch:

TODO: Insert picture

We can then create custom plots to inspect some of the metrics which we have stored for these runs. Since measurements from all of our `DEVC` devices are automatically tracked, we can create a plot of the temperature measured by the thermocouple at any of the corners of the room. To do this:

1. Click on the 'zig-zag' line at the top left of the list of runs
2. Click 'Add plot'
3. Select 'Time Series'
4. In the Data tab, select 'Ceiling_Thermocouple.Front_Left'
5. Go back to the list of Runs, and select all of our runs

TODO: Insert picture

From this plot, we can see that some of the runs caused the temperature in the room to exceed 200 degrees, which is one of our failure conditions. There is no point continuing the simulation if that happens, so we can add an early stopping trigger to stop the simulation if this happens.

### Early Stopping if Temperature Exceeds 200C

Based on the results above, we can add an early stopping feature which stops the simulation early if the temperature recorded by the thermocouples in all four corners of the room exceeds 200 degrees. To do this, we will use the `CTRL` functions built into FDS - however we could also use the Simvue alerts themselves to terminate a run. Open the FDS input file and add the following section:

TODO: Add CTRL for temp

We will then update our python file before running the script again to add an extra tag and some metadata:

TODO: Updates to python file

We can then rerun our mini gridsearch, and see the impact which this had - go to the run UI, and add the extra tag to our filters. Let us then create a custom plot, showing the temperature in one of the corners over all runs - we should see that runs where the temperature exceeded 200 degrees were automatically terminated shortly after, saving compute time and therefore reducing our carbon footprint.

TODO: Pic of custom plot

Let us try to find some more ways in which we can stop the simulations early to further reduce our carbon footprint. Change the custom plot to show the Heat Release Rate (HRR) during the simulation. We can see that in some of these simulations, the fire is not extinguished after 90 seconds as we require (ie, the HRR is above zero at 90s) - so we may as well stop our simulations early at that point as they are guaranteed to fail.

### Early Stopping if Fire Not Extinguished after 90s

To stop the simulation if the fire is not extinguished after 90 seconds inside the simulation, we can add another `CTRL` line:

TODO: CTRL line

Again we can add a new tag and piece of metadata to our Python code:

TODO: Python code

We can then rerun the gridsearch again, and create a custom plot like before for our latest set of runs. From this, we can see that simulations where the HRR is above zero at 90 seconds are terminated, again increasing our sustainability. Finally, we can notice here that in simulations where the HRR has reached zero and the fire has successfully been extinguished, we can also stop the simulation early.

### Early Stopping when Fire is Extinguished
To determine when the fire is extinguished, we could monitor for the first moment when the HRR reaches zero after some initial time period (to avoid the simulation stopping immediately, before the fire begins). However we will use the thermocouple temperature at the centre of the room instead as a good proxy, since this is what could potentially be used in real life in a test rig like this to automatically shut off the water supply. In our case we can use the plots in Simvue to see that the central thermocouple reaches 30 degrees shortly after the fire is extinguished each time. Therefore we will add a `CTRL` line which looks for this:

TODO: Add CTRL line

And as before, add some extra metadata and a tag:

TODO: Add python

We can then look at our Simvue plots again - each simulation is now stopped early for one of these reasons! We have been able to greatly reduce the time taken, and hence the energy consumed by our simulations, without compromising on results.

### Sustainability Improvements
Simvue is able to automatically estimate and track carbon emissions of your simulations using `CodeCarbon`, which we enabled in our `run.config()` calls in each Python script. To visualise the improvement in sustainability, we will compare the emissions from our four sets of grid searches which we have performed.

TODO: How to do in simvue UI

The plot looks something like this - the vertical dashed lines indicate the start of a new grid search, where a new rule for early stopping was defined. Each coloured bar represents a single run, and the colour represents the percentage of emissions which that run produced when compared to the run with the highest emissions.

TODO: Add image

From this we can see that the emissions from the fourth gridsearch (to the right of the pink line) are greatly reduced compared to the emissions from the initial gridsearch. In fact, the total reduction in emissions over our eight grid searches is as follows:

TODO: Add bar chart

This means that when we run a full gridsearch performing hundreds or even thousands of simulations to find the optimal parameters, we can use our early stopping routines to reduce the overall emissions by around TODO: X percent.

## Running a Full Gridsearch
Run a full gridsearch

Use the parallel coordinates plot

Droplet diameter of 300 is best, fix that, tweak the other two

Overall best:

Second best:

Pull the results from Simvue and run smokeview

## Using Bayesian Optimisation
Bays Opt