import simvue
import multiparser
import time
import shutil
import os
import re
import multiprocessing

if os.path.exists('./MOOSE/results'):
    shutil.rmtree('./MOOSE/results')

trigger = multiprocessing.Event()

run_name = 'thermal-diffusion-monitoring-%d' % time.time()

with simvue.Run() as run:
    run.init(
        name=run_name,
        description="A simulation to model the diffusion of heat across a metal bar",
        folder='/moose'
    )
    run.add_process(
        identifier='thermal_diffusion_simulation',
        executable='/path/to/MOOSE/application/file',
        i="tutorial/step_3/simvue_themal.i",
        color="off",
        )
    run.add_alert(
        name='step_not_converged',
        source='events',
        frequency=1,
        pattern=' Solve Did NOT Converge!',
        notification='email'
        )
    def per_event(log_data):
        if any(key in ("time_step", "converged", "non_converged") for key in log_data.keys()):
            run.log_event(list(log_data.values())[0])
            if "non_converged" in log_data.keys():
                run.kill_all_processes()
                run.save("MOOSE/results/simvue_thermal.e", "output")
                trigger.set()
                print("Simulation Terminated due to Non Convergence!")
                
    with multiparser.FileMonitor(
        per_thread_callback=per_event, 
        termination_trigger=trigger, 
    ) as file_monitor:
        file_monitor.tail(
            path_glob_exprs = "MOOSE/results/simvue_thermal.txt", 
            tracked_values = [re.compile(r"Time Step (.*)"), " Solve Converged!", " Solve Did NOT Converge!"], 
            labels = ["time_step", "converged", "non_converged"]
        )
        file_monitor.run()