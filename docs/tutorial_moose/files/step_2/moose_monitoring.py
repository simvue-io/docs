import simvue
import multiparser
import time
import shutil
import os
import re

if os.path.exists('./MOOSE/results'):
    shutil.rmtree('./MOOSE/results')

run_name = 'thermal-diffusion-monitoring-%d' % time.time()

with simvue.Run() as run:
    run.init(
        name=run_name,
        description="A simulation to model the diffusion of heat across a metal bar",
        folder='/moose'
    )
    def per_event(log_data):
        if any(key in ("time_step", "converged", "non_converged") for key in log_data.keys()):
            run.log_event(list(log_data.values())[0])
    
    with multiparser.FileMonitor(
        per_thread_callback=per_event, 
    ) as file_monitor:
        file_monitor.tail(
            path_glob_exprs = "MOOSE/results/simvue_thermal.txt", 
            tracked_values = [re.compile(r"Time Step (.*)"), " Solve Converged!", " Solve Did NOT Converge!"], 
            labels = ["time_step", "converged", "non_converged"]
        )
        file_monitor.run()