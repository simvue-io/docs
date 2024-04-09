import simvue
import multiparser
import multiparser.parsing.file as mp_file_parser
import multiparser.parsing.tail as mp_tail_parser
import time
import shutil
import os
import re
import multiprocessing
import shutil

trigger = multiprocessing.Event()

@mp_file_parser.file_parser
def moose_header_parser(input_file, **_):
    """Parses the header from the MOOSE log, so that it can be stored as metadata in the Simvue run"""
    # Open the log file, and read lines 1-7 (which contains information about the MOOSE version used etc)
    with open(input_file) as file:
        file_lines = file.readlines()
    file_lines = list(filter(None, file_lines))
    header_lines = file_lines[1:7]

    # Add the data from each line of the header into a dictionary as a key/value pair
    header_data = {}
    for line in header_lines:
        key, value = line.split(":", 1)
        key = key.replace(" ","_").lower()
        value = value.strip()
        header_data[key] = value

    return {}, header_data

def per_event(log_data, metadata, run, results_path):
    """Monitor each line in the MOOSE log, and add relevant information to the Simvue Events log."""

    # Look for relevant keys in the dictionary of data which we are passed in, and log the event with Simvue
    if any(key in ("time_step", "converged", "non_converged") for key in log_data.keys()):
        try:
            run.log_event(list(log_data.values())[0])
        except RuntimeError as e:
            print(e)

        # If run has failed to converge, save outputs, close the run as Failed, terminate multiparser
        if "non_converged" in log_data.keys():
            run.kill_all_processes()
            run.update_tags(["not_converged"])
            run.save(os.path.join(results_path, "mug_thermal.e"), "output")
            run.set_status('failed')
            trigger.set()
            print("Simulation Terminated due to Non Convergence!")
    
    # If simulation has completed successfully, save outputs, close the run, terminate multiparser
    elif "finished" in log_data.keys():
        time.sleep(1) # To allow other processes to complete
        run.update_tags(["handle_ok"])
        run.save(os.path.join(results_path, "mug_thermal.e"), "output")
        trigger.set()

def per_metric(csv_data, sim_metadata, run, client, run_id, results_path):
    """Monitor each line in the results CSV file, and add data from it to Simvue Metrics."""

    metric_time = csv_data.pop('time')

    # If the time is zero (initial reading), then set the temperature of all mug components to room temp (293.15)
    # MOOSE correctly uses this within the simulation, but for some reason still writes temperatures of 0K as the initial point in the CSV
    if metric_time == 0:
        csv_data = {key: 293.15 for key in csv_data.keys()}

    # Log all results for this timestep as Metrics
    run.log_metrics(
        csv_data,
        time = metric_time,
        timestamp = sim_metadata['timestamp']
    )

    # Get status of 'handle too hot' alert, if it is firing then can terminate simulation
    if 'handle_too_hot' in client.get_alerts(run_id):
        print("Handle is too hot!")
        run.update_tags(['handle_too_hot',])
        run.save(os.path.join(results_path, "mug_thermal.e"), "output")
        run.kill_all_processes()
        run.set_status('failed')
        trigger.set()  


def monitor_moose_simulation(run_name, moose_file, results_dir):
    """Begin and monitor the MOOSE simulation for the given material, tracking progress and results with Simvue"""

    # Reset the status of the trigger, so that the run does not terminate immediately due to the previous run setting the trigger
    trigger.clear()

    # Remove any old results
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)

    # Create the Simvue run
    with simvue.Run() as run:
        run.init(
            name=run_name,
            description="A simulation to model the transfer of heat through a coffee cup filled with hot liquid.",
            folder='/mug_thermal'
        )

        # Add the MOOSE simulation as a process, so that Simvue can abort it if alerts begin to fire
        run.add_process(
            identifier='moose_simulation',
            executable='app/moose_tutorial-opt',
            i=moose_file,
            color="off",
            )
        
        # Add alerts which we want to keep track of, so that we can terminate the simulation early if they fire
        run.add_alert(
            name='step_not_converged',
            source='events',
            frequency=1,
            pattern=' Solve Did NOT Converge!',
            notification='email'
            )
        run.add_alert(
            name='handle_too_hot',
            source='metrics',
            metric='handle_temp_avg',
            rule='is above',
            threshold=323.15,
            frequency=1,
            window=1,
            ) 
        
        # Save the MOOSE input file for this run to the Simvue server
        run.save(moose_file, "input")   

        # Create a Client instance for keeping track of which alerts are firing
        client = simvue.Client()
        run_id = client.get_run_id_from_name(run_name)

        # Start an instance of the file monitor, to keep track of log and results files from MOOSE
        with multiparser.FileMonitor(
            termination_trigger=trigger,
            
        ) as file_monitor:
            # Monitor each line added to the MOOSE log file as the simulation proceeds and look out for certain phrases to upload to Simvue
            file_monitor.tail(
                path_glob_exprs = os.path.join(results_dir, "mug_thermal.txt"), 
                callback= lambda data, meta, run=run, results_path=results_dir: per_event(data, meta, run, results_path),
                tracked_values = [re.compile(r"Time Step.*"), " Solve Converged!", " Solve Did NOT Converge!", "Finished Executing"], 
                labels = ["time_step", "converged", "non_converged", "finished"]
            )
            
            # Read the initial information within the log file when it is first created, to parse the header information
            file_monitor.track(
                path_glob_exprs = os.path.join(results_dir, "mug_thermal.txt"), 
                callback = lambda header_data, metadata: run.update_metadata({**header_data, **metadata}), 
                parser_func = moose_header_parser, 
                static = True,
            )

            # Monitor each line added to the MOOSE results file as the simulation proceeds, and upload results to Simvue
            file_monitor.tail(
                path_glob_exprs =  os.path.join(results_dir, "mug_thermal.csv"),
                parser_func=mp_tail_parser.record_csv,
                callback= lambda csv_data, sim_metadata, run=run, client=client, run_id=run_id, results_path=results_dir: per_metric(csv_data, sim_metadata, run, client, run_id, results_path),
            )
            file_monitor.run()

        
script_dir = os.path.dirname(__file__)

# Our three sets of inputs, to run simulations for Copper, Steel and Ceramic mugs
material_inputs = {
    'steel': {
        'run_name': 'mug_thermal_steel-%d' % time.time(),
        'moose_file': os.path.join(script_dir, 'steel_mug.i'),
        'results_dir': os.path.join(script_dir, 'results', 'steel')
    },
    'copper': {
        'run_name': 'mug_thermal_copper-%d' % time.time(),
        'moose_file': os.path.join(script_dir, 'copper_mug.i'),
        'results_dir': os.path.join(script_dir, 'results', 'copper')
    },
    'ceramic': {
        'run_name': 'mug_thermal_ceramic-%d' % time.time(),
        'moose_file': os.path.join(script_dir, 'ceramic_mug.i'),
        'results_dir': os.path.join(script_dir, 'results', 'ceramic')
    }
}

outputs = {}

# Run the MOOSE simulation and monitor it for all materials above
for material_type, inputs in material_inputs.items():
    print("Starting MOOSE Simulation of mug made from", material_type)
    monitor_moose_simulation(**inputs)

print("All simulations complete!")