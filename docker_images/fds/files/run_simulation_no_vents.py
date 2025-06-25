import os
import shutil
from simvue_fds.connector import FDSRun

# Delete old results directory, if present
if os.path.exists("/workdir/results_no_vents"):
    shutil.rmtree("/workdir/results_no_vents")

with FDSRun() as run:
    run.init("fds_simulation_no_vents")

    run.update_tags(["fds", "no_vents"])

    run.create_metric_threshold_alert(
        name="temperature_above_100_degrees",
        metric="air_temperature",
        frequency=1,
        window=1,
        rule="is above",
        threshold=100,
        trigger_abort=True,
    )

    run.create_metric_threshold_alert(
        name="visibility_below_three_metres",
        metric="eye_level_visibility",
        frequency=1,
        window=1,
        rule="is below",
        threshold=3,
        trigger_abort=True,
    )
    
    run.create_metric_threshold_alert(
        name="average_visibility_below_three_metres",
        metric="soot_visibility.z.2_0.avg",
        frequency=1,
        window=1,
        rule="is below",
        threshold=3,
        trigger_abort=True,
    )

    run.launch(
        fds_input_file_path="/workdir/input_no_vents.fds",
        workdir_path=f"results_no_vents",
        clean_workdir=True,
        slice_parse_quantity = "SOOT VISIBILITY",

    )
