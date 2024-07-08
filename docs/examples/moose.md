# MOOSE
This example demonstrates how you can use Simvue to track MOOSE simulations. In particular, it will show how you can:

- Extract data from files produced during the execution of MOOSE in real time
- Record Metadata, Metrics and Events based on data from these files
- Trigger Alerts based on Metric values
- Abort simulation runs based on firing alerts
- Save Artifacts

## Specifying the Problem
In our example, we will imagine that we are a coffee cup manufacturer, looking to design a new cup which we want to put onto the market. While we have decided on the shape and thickness of the mug, we aren't sure whether to make the mug out of Copper, Steel or Ceramic. The main factor which will influence our decision is how hot the handle of the mug gets - if it gets too hot, the customer won't be able to pick it up!

To model this scenario, we will model the fluid inside the cup as having an exponentially decaying temperature from 90 degrees Celsius to room temperature (20 degrees Celsius), and we will use MOOSE to simulate the conductive heat through the walls and handle of the mug over time. We will also get MOOSE to output the maximum, minimum and average temperature of the handle at every time step, so that we can monitor it effectively. We will say that if the average temperature of the handle goes above 50 degrees, then it will be too hot to hold, and the simulation can be aborted to save computational time.

## Setup
The easiest way to run this example is to use the provided Docker container:
### Install Docker
You will need to install the Docker CLI tool to be able to use the Docker container for this tutorial. [^^Full instructions for installing Docker can be found here^^](https://docs.docker.com/engine/install/). If you are running Ubuntu (either on a full Linux system or via WSL on Windows), you should be able to do:
```sh
sudo apt-get update && sudo apt-get install docker.io
```
To check that this worked, run `docker` - you should see a list of help for the commands.

!!! tip
    If you wish to run this on a Windows computer (without using Docker Desktop) via Windows Subsystem for Linux, [^^follow this guide on setting up Docker with WSL.^^](https://dev.to/bowmanjd/install-docker-on-windows-wsl-without-docker-desktop-34m9)

### Pull Docker image
Next we need to pull the container, which is stored in the Simvue repository's registry:
```sh
sudo docker pull ghcr.io/simvue-io/moose_example:latest
```
This may take some time to download. Once complete, if you run `sudo docker images`, you should see an image with the name `ghcr.io/simvue-io/moose_example` listed.

### Run Docker container
Firstly, add Docker as a valid user of the X windows server, so that we can view results using Paraview:
```sh
xhost +local:docker
```
Then you can run the container:
```sh
sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/moose_example:latest
```
If this is running correctly, you should see your command prompt change to something like:
```sh
dev:~/simvue-moose$
```
To test that the graphics packages are working correctly, run the command `paraview` within the container. After a few seconds, this should open up a graphical user interface window for the Paraview visualization tool.

!!! tip
    If you are using WSL and you do not see Paraview open correctly, it may be because your WSL is not set up correctly. To check this, exit the docker container by pressing <kbd>ctrl</kbd> + <kbd>D</kbd>, and then run the following commands:
    ```
    sudo apt-get install -y x11-apps
    xeyes
    ```
    This should open a small graphical display window, with a pair of eyes which follow your mouse around the screen. If you do not see this, [^^follow this guide to get graphical apps working on WSL^^](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps), and [^^look through these debugging tips for WSL^^](https://github.com/microsoft/wslg/wiki/Diagnosing-%22cannot-open-display%22-type-issues-with-WSLg).

### Update Simvue Config File
Finally we need to update the config file inside the Docker container to use your credentials. Login to the web UI, go to the **Runs** page and click **Create new run**. You should then see the credentials which you need to enter into the `simvue.ini` file. Simply open the existing file using `nano simvue.ini`, and replace the contents with the information from the web UI.

!!! note
    If you restart the docker container at any point, you will need to repeat this step as your changes will not be saved

## Using Simvue with MOOSE
To easily use Simvue to track your MOOSE simulations, a wrapper for the Simvue `Run` class has been created, called `MooseRun`. By default, this class will do the following:

- Upload your MOOSE input file as an input artifact
- Upload your MOOSE Makefile as a code artifact, if it is found in the same location as your MOOSE application
- Upload information from the header of the MOOSE console log (such as the MOOSE version, PETSC version etc) as metadata.
- Track your console log file, adding the following information to the Events log:
    * The step which is currently being executed by the solver
    * Whether the step converged or not
    * How long the step took to converge
- Create an alert which monitors the Events log, and notifies the user if any step fails to converge
- Track any variable values which are being output to a CSV file after each step by MOOSE, logging them as Metrics
- Upload the Exodus file as an output artifact (if present) once the simulation has finished

!!! note
    To be able to use the MOOSE wrapper (or any of the other included wrappers and integrations) in your own scripts, you will need to checkout the `simvue-integrations` repository:
    ```
    pip install git+https://github.com/simvue-io/integrations.git
    ```


Firstly we will create our MOOSE input file, which in our case uses the mesh for a coffee cup stored in the file `cup.e`, and defines the heat conduction kernels and functions to use to simulate the flow of heat through the cup. We define the boundary conditions for the system, eg the background temperature and the maximum temperature inside the mug, as well as some properties about the material such as the thermal conductivity and heat capacity. The log is sent to a file for storage, and results of the minimum, maximum and average temperature of the handle are stored in a CSV file after each time step.

??? example "Example MOOSE Input File"

    Here is an example input file for MOOSE - this is for the steel coffee cup, and can be viewed or edited in the Docker container using `nano /example/steel_mug.i`:
    ```ini
    [Mesh]
    file = 'cup.e'
    []
    
    [Variables]
    [temperature]
        family = LAGRANGE
        order = FIRST
        initial_condition = 293.15 # Start at room temperature
    []
    []
    
    [Kernels]
    [heat-conduction]
        type = ADHeatConduction
        variable = temperature
    []
    [heat-conduction-dt]
        type = ADHeatConductionTimeDerivative
        variable = temperature
    []
    []
    
    [Functions]
    [temp-func]
        type = ParsedFunction
        value = 'ambient + (temp_zero*exp(-t*constant))'
        vars = 'ambient temp_zero constant'
        vals = '293.15 90.0 0.01'
    []
    []
    
    [BCs]
    [convective]
        type = ADConvectiveHeatFluxBC
        variable = temperature
        boundary = 'convective'
        T_infinity = '293.15'
        heat_transfer_coefficient = 7.8
    []
    [fixed-temp]
        type = ADFunctionDirichletBC
        variable = temperature
        function = 'temp-func'
        boundary = 'fixed-temp'
    []
    []
    
    [Materials]
    [steel-density]
        type = ADGenericConstantMaterial
        prop_names = 'density'
        prop_values = '7800'
    []
    [steel-conduction]   
        type = ADHeatConductionMaterial
        specific_heat = 420.0
        thermal_conductivity = 45.0
    []
    []

    [Postprocessors]
    [handle_temp_max]
        type = ElementExtremeValue
        value_type = max
        variable = 'temperature'
        block = 'handle'
    []
    [handle_temp_min]
        type = ElementExtremeValue
        value_type = min
        variable = 'temperature'
        block = 'handle'
    []
    [handle_temp_avg]
        type = ElementAverageValue
        variable = 'temperature'
        block = 'handle'
    []
    []

    [Executioner]
    type = Transient
    solve_type = 'NEWTON'
    petsc_options = '-snes_ksp_ew'
    petsc_options_iname = '-pc_type -sub_pc_type -pc_asm_overlap -ksp_gmres_restart'
    petsc_options_value = 'asm lu 1 101'
    line_search = 'none' 
    nl_abs_tol = 1e-9
    nl_rel_tol = 1e-8
    l_tol = 1e-6
    start_time = 0
    dt = 5
    end_time = 200
    []

    [Outputs]
    file_base = ./example/results/steel/mug_thermal
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
    []
    ```


We then want to create our Python script which initializes the `MooseRun` wrapper class. This class can be used as a context manager in the same way as the default Simvue `Run` class. It also has all of the same methods available as the Simvue `Run` class, allowing the user to upload any tags, metadata, artifacts etc which they want to store in addition to the items stored by default by the `MOOSERun` class. 

When we have setup our run, we must call the `launch()` method to start our MOOSE simulation, which takes the following parameters:

- `moose_file_path`: Path to the MOOSE input file
- `output_dir_path`: Path to the directory where results will be stored
- `results_prefix`: The prefix assigned to each output file created by MOOSE (defined in the input file)
- `moose_env_vars`: A dictionary of any environment variables to pass to the MOOSE application on startup


??? example "Example Simvue Monitoring Script"
    Here is an example Simvue monitoring script - for each material, it uses our `MOOSERun` wrapper class as a context manager, initializes the run, adds some data specific to this MOOSE run, and then calls `launch()` to perform and track the simulation. Once the simulation completes, we use the `Client` class to get the status of any alerts, and update the tags of the run if the `handle_too_hot` alert which we defined before the simulation began started firing.
    ```py
    import os
    import shutil
    import time
    import simvue
    from simvue_integrations.wrappers.moose import MooseRun

    script_dir = os.path.dirname(__file__)

    # Delete any results from previous runs, otherwise the MOOSE wrapper will identify and upload these
    if os.path.exists(os.path.join(script_dir, 'results')):
        shutil.rmtree(os.path.join(script_dir, 'results'))

    # Our three sets of inputs, to run simulations for Copper, Steel and Ceramic mugs
    material_inputs = {
        'steel': {
            'run_name': 'mug_thermal_steel-%d' % time.time(),
            'moose_file': os.path.join(script_dir, 'steel_mug.i'),
            'results_dir': os.path.join(script_dir, 'results', 'steel')
        },
        'ceramic': {
            'run_name': 'mug_thermal_ceramic-%d' % time.time(),
            'moose_file': os.path.join(script_dir, 'ceramic_mug.i'),
            'results_dir': os.path.join(script_dir, 'results', 'ceramic')
        },
        'copper': {
            'run_name': 'mug_thermal_copper-%d' % time.time(),
            'moose_file': os.path.join(script_dir, 'copper_mug.i'),
            'results_dir': os.path.join(script_dir, 'results', 'copper')
        }
    }

    # Run the MOOSE simulation and monitor it for all materials above
    for material_type, inputs in material_inputs.items():
        print("Starting MOOSE Simulation of mug made from", material_type)

        with MooseRun() as run:
            # Initialize your Simvue run as normal
            run.init(
                name=inputs['run_name'],
                description="A simulation to model the transfer of heat through a coffee cup filled with hot liquid.",
                folder='/mug_thermal'
            )

            # Can add anything to the Simvue run which you want before / after the MOOSE simulation
            run.update_metadata({"material": material_type})
            run.update_tags([material_type,])

            # Add an alert which will automatically abort the run if the handle becomes too hot to touch
            run.create_alert(
                name='handle_too_hot',
                source='metrics',
                metric='handle_temp_avg',
                rule='is above',
                threshold=323.15,
                frequency=1,
                window=1,
                trigger_abort=True
                )
            
            run.log_event("MOOSE simulation - coffee cup, terminating if handle too hot.") 
            
            # Call this to begin your MOOSE simulation
            run.launch(
                moose_application_path='/home/dev/simvue-moose/app/moose_tutorial-opt',
                moose_file_path=inputs['moose_file'],
                output_dir_path=inputs['results_dir'],
                results_prefix="mug_thermal",
            )

            # Again can add any custom data to the Simvue run once the simulation is finished
            run.log_event("Simulation is finished!")

            # Can create a Client instance for keeping track of if alerts have fired
            client = simvue.Client()
            run_id = client.get_run_id_from_name(inputs['run_name'])
            # If handle got too hot, add a tag for easier categorisation
            if 'handle_too_hot' in client.get_alerts(run_id):
                run.update_tags['handle_too_hot']

    print("All simulations complete!")
    ```

## Running the Simulations
To run the simulations in the Docker container, run the following command:
```
python example/moose_monitoring.py
```
These simulations will take around 20 minutes to complete - look out for the message `All simulations complete!` printed to the command line to indicate when it is complete.

## Results
Once our simulations have completed, you can view the results using Paraview. To do this, for example for the Ceramic mug, you can run `paraview example/results/ceramic/mug_thermal.e`. Then to view the results, do the following steps:

- In the Properties panel in the left hand side, in the Variables tab, tick the box next to `temperature`. Press Apply
- In the second bar of icons at the top of the window, click the 'vtkBlockColours' dropdown and change this to `temperature`
- Next to this dropdown, find the button with an arrow and the letter 't'. Click this to rescale the data range over all timestamps
- Press the green play button in the top bar of the window

You should see the heat flowing from the inside of the cup to the outside and handle over time, and then the whole cup cooling down as the 'fluid' inside cools. It should look something like this:
<figure markdown>
  ![The results of the Ceramic mug simulation in Paraview.](images/moose_paraview.png){ width="1000" }
</figure>

If you log into the Simvue UI and look in the Runs tab, you should see that three runs have been completed. The runs for mugs made from ceramic and steel completed successfully, with no alerts fired. However the mug made of copper failed to complete, with one of the alerts firing and a 'handle_too_hot' tag associated with it.
<figure markdown>
  ![The Simvue run UI showing three runs, corresponding to the Copper, Steel and Ceramic mugs.](images/moose_runs.png){ width="1000" }
</figure>

If we click on the run for the Ceramic mug, we can go through each of the tabs at the top to check that all of the information from the run has been stored as expected. For example:

- Description says 'A simulation to model the transfer of heat through a coffee cup filled with hot liquid.'
- Metadata contains the information we parsed from the MOOSE header, such as the MOOSE version, libmesh version etc
- Artifacts contains the MOOSE file in the Inputs folder, and the `mug_thermal.e` exodus file for viewing in Paraview in the Outputs folder
- Metrics contains three graphs, for the maximum, minimum and average temperatures of the handle
- Events contains each step which was performed, and whether the step converged successfully
- Alerts contains the alerts we defined for the temperature of the handle and for non converging errors, and the alerts are all normal

We can also create a custom plot of our three temperature metrics against each other. Go back to the Metrics page, and in the top left click `View > Single`. You can then press the three dots on the right, and click `Edit`, which will bring up a popup box similar to the one shown below. Change the following settings:

- In Data, check `handle_temp_avg`, `handle_temp_max`, and `handle_temp_min`
- In Axes, change `Steps` to `Time`
- In Axes > Ranges, change the y axis minimum to 290

You should see something like this:
<figure markdown>
  ![A custom plot of all temperature metrics for the Ceramic mug.](images/moose_custom_plot_ceramic.png){ width="1000" }
</figure>

During execution of the simulation, you may have noticed that the Copper mug simulation finished sooner than the others. This is because the handle got too hot, the alert fired, and the simulation was stopped early since there was no point continuing. If you open the run for the copper mug and go to the Alerts page, you can see a graph of the sampled values of the average handle temperature metric. It should show that the handle just breached our threshold of 50 degrees Celsius, and so the alert was triggered:
<figure markdown>
  ![The firing alert for the temperature of the copper mug's handle.](images/moose_firing_alert.png){ width="1000" }
</figure>

This is an important feature of Simvue, since it allows runs which are breach certain conditions and therefore are destined to fail to be terminated early, without intervention from the user. This can give a huge reduction in computational time and cost which is typically wasted on pointless simulations, while also helping to reduce the environmental impacts of running simulations.

We can also plot the metrics from multiple runs all at once, to easily compare the temperatures which each of the different mugs reached. Firstly, Go to the Runs page of the UI and select the check box next to all three of our runs for our different materials. Next, click on the `Show Plots` button in the top right of the page (zig zag lines), which will open a window on the side of the page, where you can press `Add Plot`. You will see that this opens a similar popup to the one we used to create our custom graph above. We will then follow a similar process to before:

- In Type, select `Time Series`
- In Data, select `handle_temp_avg`
- In Axes, change `Steps` to `Time`, and set the minimum y axis limit to be 290
- In Legend, select `Top`

The graph plotted should look look something like this:
<figure markdown>
  ![A plot of the average temperature of each mug's handle.](images/moose_all_materials.png){ width="1000" }
</figure>

This allows us to see that, as we may have expected, the Ceramic mug was better at insulating the heat than the Steel and Copper ones. 

This is of course a relatively simple example, but could be extended to make it more complicated. For example, say we introduced a lid to the mug, and had the heat from the fluid only leave through the walls of the container. How would this change the graphs above? 

We could then also monitor how long the temperature remained within a given range using another alert (say between 50 and 70 degrees, so that it is hot but drinkable). Would the copper mug also let the drink go cold too quickly? Would the ceramic mug be too insulating, and the drink would remain too hot for too long? These are the kinds of questions which Simvue makes much easier to keep track of and solve.