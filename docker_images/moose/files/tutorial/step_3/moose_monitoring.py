import simvue
import multiparser
import time
import shutil
import os
import re
import pathlib
import multiprocessing

trigger = multiprocessing.Event()

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
        elif "finished" in log_data.keys():
            time.sleep(1) # To allow other processes to complete
            run.update_tags(["completed",])
            trigger.set()
    
    with multiparser.FileMonitor(
        per_thread_callback=per_event, 
        termination_trigger=trigger,
    ) as file_monitor:
        file_monitor.tail(
            path_glob_exprs = os.path.join(script_dir, "results", "simvue_thermal.txt"), 
            tracked_values = [re.compile(r"Time Step.*"), " Solve Converged!", " Solve Did NOT Converge!", "Finished Executing"], 
            labels = ["time_step", "converged", "non_converged", "finished"]
        )
        file_monitor.run()