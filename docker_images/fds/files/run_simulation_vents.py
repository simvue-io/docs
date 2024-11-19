import os
import shutil
import time
from simvue_integrations.connectors.fds import FDSRun

timestamp = int(time.time())

# Delete old results directory, if present
if os.path.exists("/workdir/results_with_vents"):
    shutil.rmtree("/workdir/results_with_vents")
    
with FDSRun() as run:
    run.init(f"fds_simulation_with_vents_{timestamp}")

    run.update_tags(["fds", "vents"])

    run.create_alert(
        name="temperature_above_100_degrees",
        metric="air_temperature",
        source="metrics",
        frequency=1,
        rule="is above",
        threshold=100,
        trigger_abort=True
    )

    run.create_alert(
        name="visibility_below_three_metres",
        metric="eye_level_visibility",
        source="metrics",
        frequency=1,
        rule="is below",
        threshold=3,
        trigger_abort=True
    )

    run.launch(
        fds_input_file_path = "/workdir/input_with_vents.fds",
        workdir_path = f"results_with_vents",
        clean_workdir=True
    )
