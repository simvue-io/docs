import os
import shutil
import time
import simvue
from simvue_moose.connector import MooseRun

script_dir = os.path.dirname(__file__)

# Delete any results from previous runs, otherwise the MOOSE connector will identify and upload these
if os.path.exists(os.path.join(script_dir, "results")):
    shutil.rmtree(os.path.join(script_dir, "results"))

# Our three sets of inputs, to run simulations for Copper, Steel and Ceramic mugs
material_inputs = {
    "steel": {
        "run_name": "mug_thermal_steel-%d" % time.time(),
        "moose_file": os.path.join(script_dir, "steel_mug.i"),
        "results_dir": os.path.join(script_dir, "results", "steel"),
    },
    "ceramic": {
        "run_name": "mug_thermal_ceramic-%d" % time.time(),
        "moose_file": os.path.join(script_dir, "ceramic_mug.i"),
        "results_dir": os.path.join(script_dir, "results", "ceramic"),
    },
    "copper": {
        "run_name": "mug_thermal_copper-%d" % time.time(),
        "moose_file": os.path.join(script_dir, "copper_mug.i"),
        "results_dir": os.path.join(script_dir, "results", "copper"),
    },
}

# Run the MOOSE simulation and monitor it for all materials above
for material_type, inputs in material_inputs.items():
    print("Starting MOOSE Simulation of mug made from", material_type)

    with MooseRun() as run:
        # Initialize your Simvue run as normal
        run.init(
            name=inputs["run_name"],
            description="A simulation to model the transfer of heat through a coffee cup filled with hot liquid.",
            folder="/mug_thermal",
        )

        # Can add anything to the Simvue run which you want before / after the MOOSE simulation
        run.update_metadata({"material": material_type})
        run.update_tags(
            [
                material_type,
            ]
        )

        # Add an alert which will automatically abort the run if the handle becomes too hot to touch
        run.create_metric_threshold_alert(
            name="handle_too_hot",
            metric="handle_temp_avg",
            rule="is above",
            threshold=323.15,
            frequency=1,
            window=1,
            trigger_abort=True,
        )

        run.log_event("MOOSE simulation - coffee cup, terminating if handle too hot.")

        # Call this to begin your MOOSE simulation
        run.launch(
            moose_application_path="/home/dev/simvue-moose/app/moose_tutorial-opt",
            moose_file_path=inputs["moose_file"],
        )

        # Again can add any custom data to the Simvue run once the simulation is finished
        run.log_event("Simulation is finished!")

print("All simulations complete!")

