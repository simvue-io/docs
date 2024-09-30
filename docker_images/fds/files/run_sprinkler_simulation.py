import os
import shutil
from simvue_integrations.connectors.fds import FDSRun

# Delete old results directory, if present
if os.path.exists("/workdir/results_sprinkler"):
    shutil.rmtree("/workdir/results_sprinkler")
    
# Initialise the FDS Connector
with FDSRun() as run:
    # Update the configuration to enable logging of emission metrics during execution
    run.config(enable_emission_metrics=True,emission_metrics_interval=1)
    
    # Initialise the run, giving a run name, the folder to store results in, and tags to help us find it later
    run.init(f"fds_simulation_sprinkler",folder="/fds/sprinklers", tags=["fds","sprinkler"])

    # Launch the FDS simulation, providing the input file and location where you want results to be stored
    run.launch(
        fds_input_file_path = "/workdir/sprinkler.fds",
        workdir_path = "/workdir/results_sprinkler"
        )