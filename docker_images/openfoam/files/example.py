from simvue_integrations.wrappers.openfoam import OpenfoamRun

with OpenfoamRun() as run:
    # Initialize your Simvue run as normal
    run.init(
        name="testing_openfoam_wrapper",
    )

    # Can add anything to the Simvue run which you want before / after the MOOSE simulation
    run.update_metadata({"simulation": "movingCone"})
    run.create_alert(
        name='ux_residuals_too_high',
        source='metrics',
        metric='residuals.initial.Ux',
        rule='is above',
        threshold=0.1,
        frequency=1,
        window=1,
        trigger_abort=True
        )
    run.log_event("Openfoam simulation.") 
    
    # Call this to begin your MOOSE simulation
    run.launch(
        openfoam_case_dir='/home/openfoam/movingCone',
    )

    # Again can add any custom data to the Simvue run
    run.log_event("Simulation is finished!")
    run.update_tags(["finished"])