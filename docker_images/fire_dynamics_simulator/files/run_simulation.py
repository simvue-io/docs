import time
from simvue_integrations.connectors.fds import FDSRun

timestamp = time.time()
with FDSRun() as run:
    run.init(f"fds_warehouse_simulation_{timestamp}")

    run.update_tags(["fds", "warehouse"])

    run.create_alert(
        name="thermocouple_temperature_below_threshold",
        metric="THCP01",
        source="metrics",
        frequency=1,
        rule="is above",
        threshold=500,
        trigger_abort=True
    )

    run.create_alert(
        name="visibility_near_eye_level_threshold",
        metric="VIS01",
        source="metrics",
        frequency=1,
        rule="is below",
        threshold=10,
        trigger_abort=True
    )

    run.create_alert(
        name="fractional_effective_dose_threshold",
        metric="FED01",
        source="metrics",
        frequency=1,
        rule="is above",
        threshold=0.5,
        trigger_abort=True
    )

    run.launch(
        fds_input_file_path = "/workdir/input.fds",
        workdir_path = f"results_{timestamp}"
    )
