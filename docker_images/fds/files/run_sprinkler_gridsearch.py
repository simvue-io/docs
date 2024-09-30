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
