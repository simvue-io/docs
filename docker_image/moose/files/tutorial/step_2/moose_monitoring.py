import simvue
import multiparser
import time
import shutil
import os
import re
import pathlib

script_dir = os.path.dirname(__file__)

if os.path.exists(os.path.join(script_dir, "results")):
    shutil.rmtree(os.path.join(script_dir, "results"))

run_name = 'thermal-diffusion-monitoring-%d' % time.time()

with simvue.Run() as run:
    run.init(
        name=run_name,
        description="A simulation to model the diffusion of heat across a metal bar",
        folder='/moose'
    )
    def per_event(log_data, metadata):
        if any(key in ("time_step", "converged", "non_converged") for key in log_data.keys()):
            run.log_event(list(log_data.values())[0])
    
    with multiparser.FileMonitor(
        per_thread_callback=per_event, 
    ) as file_monitor:
        file_monitor.tail(
            path_glob_exprs = os.path.join(script_dir, "results", "simvue_thermal.txt"), 
            tracked_values = [re.compile(r"Time Step.*"), " Solve Converged!", " Solve Did NOT Converge!"], 
            labels = ["time_step", "converged", "non_converged"]
        )
        file_monitor.run()