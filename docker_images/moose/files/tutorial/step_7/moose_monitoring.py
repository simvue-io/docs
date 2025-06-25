import simvue
import multiparser
import multiparser.parsing.file as mp_file_parser
import time
import shutil
import os
import re
import multiprocessing

script_dir = os.path.dirname(__file__)

if os.path.exists(os.path.join(script_dir, "results")):
    shutil.rmtree(os.path.join(script_dir, "results"))

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
        key = key.replace(" ", "_").lower()
        value = value.strip()
        header_data[key] = value

    return {}, header_data


run_name = "thermal-diffusion-monitoring-%d" % time.time()

with simvue.Run() as run:
    run.init(
        name=run_name,
        description="A simulation to model the diffusion of heat across a metal bar",
        folder="/moose",
    )
    run.add_process(
        identifier="thermal_diffusion_simulation",
        executable="app/moose_tutorial-opt",
        i="tutorial/step_7/simvue_thermal.i",
        color="off",
    )
    run.create_event_alert(
        name="step_not_converged",
        frequency=1,
        pattern=" Solve Did NOT Converge!",
        notification="email",
    )

    def per_event(log_data, metadata):
        if any(
            key in ("time_step", "converged", "non_converged")
            for key in log_data.keys()
        ):
            run.log_event(list(log_data.values())[0])
            if "non_converged" in log_data.keys():
                run.kill_all_processes()
                run.save_file(
                    os.path.join(script_dir, "results", "simvue_thermal.e"), "output"
                )
                run.set_status("failed")
                trigger.set()
                print("Simulation Terminated due to Non Convergence!")
        elif "finished" in log_data.keys():
            time.sleep(1)  # To allow other processes to complete
            run.update_tags(
                [
                    "completed",
                ]
            )
            trigger.set()

    def per_metric(csv_data, sim_metadata):
        step_num = sim_metadata["file_name"].split("_")[-1].split(".")[0]
        run.log_metrics(
            {f"temp_at_x.{csv_data['x']}": csv_data["T"]},
            step=int(step_num),
            timestamp=sim_metadata["timestamp"],
        )

    with multiparser.FileMonitor(
        termination_trigger=trigger,
    ) as file_monitor:
        file_monitor.tail(
            path_glob_exprs=os.path.join(script_dir, "results", "simvue_thermal.txt"),
            callback=per_event,
            tracked_values=[
                re.compile(r"Time Step.*"),
                " Solve Converged!",
                " Solve Did NOT Converge!",
                "Finished Executing",
            ],
            labels=["time_step", "converged", "non_converged", "finished"],
        )
        file_monitor.track(
            path_glob_exprs=os.path.join(script_dir, "results", "simvue_thermal.txt"),
            callback=lambda header_data, metadata: run.update_metadata(
                {**header_data, **metadata}
            ),
            parser_func=moose_header_parser,
            static=True,
        )
        file_monitor.track(
            path_glob_exprs=os.path.join(
                script_dir, "results", "simvue_thermal_temps_*.csv"
            ),
            callback=per_metric,
            static=True,
        )
        file_monitor.run()

