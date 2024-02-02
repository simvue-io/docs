import multiparser
import simvue
import multiprocessing
import re
import time
import shutil
import os
# Create simvue run
if os.path.exists('./tutorial/results'):
    shutil.rmtree('./tutorial/results')
with simvue.Run() as run:
    run_name = 'thermal-diffusion-monitoring-%d' % time.time()
    trigger = multiprocessing.Event()
    run.init(name=run_name)
    run.add_alert(
        name='step_not_converged',
        source='events',
        frequency=1,
        pattern=' Solve Did NOT Converge!',
        )
    run.add_alert(
    name='temperature_exceeds_maximum',
    source='metrics',
    metric='temp_at_x.3',
    rule='is above',
    threshold=600,
    frequency=1,
    window=1,
    )
    run.add_process('alert_monitor', "python3", "tutorial/moose_analysis.py", run_name, "10", "1000")
    run.add_process('moose-simulation', "app/moose_tutorial-opt", "i=tutorial/simvue_thermal.i")

    # per thread callback: Function which is executed every time
    # This is handed data (dictionary of key/value pairs) which file monitor has scraped
    # Next hands metadata (can leave blank)
    def per_event(data, _, trigger=trigger):
        # Log event of data which has been scraped
        if any(key in ("time_step", "converged", "non_converged") for key in data.keys()):
            run.log_event(list(data.values())[0])
            if "non_converged" in data:
                run.kill_all_processes()
                trigger.set()

    import multiparser.parsing.file as mp_file_parser

    # Using log_parser as a decorator so that it adds the default metadata for all parsers (filename, timestamp etc)
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

    def per_metric(data, metadata):
        step_num = metadata['file_name'].split('_')[-1].split('.')[0]
        run.log_metrics(
            {f"temp_at_x.{data['x']}": data['T']}, 
            step=int(step_num),
            timestamp=metadata['timestamp']
        )

    def per_alert(data, metadata):
        if data['status'] == True:
            run.kill_all_processes()
            trigger.set()
            print("DONE")

    #Add simvue call to run MOOSE
    #run.add_process("run_moose", executable="~/moose-training-workshop/app/moose_tutorial-opt", i="simvue_thermal.i", color="off")

    # Instantiate file monitor
    # flatten_data: Flatten keys so that Simvue can cope with it, instead of nested dict
    # Plain logging: disable loguru coloring
    # termination trigger: Should be sent by Simvue on exit of MOOSE process when 'did not converge' is received
    # terminate_all_on_fail: If one thread which it spins up fo reading files fails, terminates all threads
    with multiparser.FileMonitor(
        flatten_data=True, 
        plain_logging=True, 
        termination_trigger=trigger,
    ) as file_monitor:
        # Tells multiparser which files to keep track of, tail means it is a line by line live updating file
        # Then tell it which lines to look out for and track, either regex or literal string
        # Then pass in a list of strings which represent the 'keys' of the dictionary corresponding the the lines it is looking out for
        file_monitor.tail("tutorial/results/simvue_thermal.txt", tracked_values=[re.compile(r"(Time Step .*)"), " Solve Converged!", " Solve Did NOT Converge!"], labels=["time_step", "converged", "non_converged"], callback=per_event)
        file_monitor.track("tutorial/results/simvue_thermal.txt", callback=lambda header_data, metadata: run.update_metadata({**header_data, **metadata}), parser_func=moose_header_parser, static=True)
        file_monitor.track("tutorial/results/simvue_*.csv", callback=per_metric, static=True)
        file_monitor.tail("tutorial/alert_status.csv", callback=per_alert)
        file_monitor.run()
