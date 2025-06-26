import os
import shutil
import time
from simvue_fds.connector import FDSRun

timestamp = int(time.time())

with FDSRun() as run:
    run.init(f"fds_simulation_powerful_vents_{timestamp}")

    run.load(
        results_dir="example_results",
        slice_parse_quantity = "SOOT VISIBILITY"
    )
