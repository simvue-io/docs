import simvue
import multiparser
import multiparser.parsing.file as mp_file_parser
import time
import shutil
import os
import re
import multiprocessing

if os.path.exists('./MOOSE/results'):
    shutil.rmtree('./MOOSE/results')

trigger = multiprocessing.Event()

@mp_file_parser.file_parser
def moose_header_parser(input_file, **_):
    with open(input_file) as file:
        file_lines = file.readlines()
    file_lines = list(filter(None, file_lines))
    header_lines = file_lines[1:7]
    header_data = {}
    for line in header_lines:
        key, value = line.split(":", 1)
        key = key.replace(" ","_").lower()
        value = value.strip()
        header_data[key] = value

    return {}, header_data

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
        file_monitor.track(
            path_glob_exprs = "MOOSE/results/simvue_thermal.txt", 
            callback = lambda header_data, metadata: run.update_metadata({**header_data, **metadata}), 
            parser_func = moose_header_parser, 
            static = True
        )
        file_monitor.run()