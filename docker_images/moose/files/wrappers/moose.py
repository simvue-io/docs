import simvue
import typing
import pydantic
import multiparser.parsing.file as mp_file_parser
import multiparser.parsing.tail as mp_tail_parser
import os
import time
import re
from generic import WrappedRun
@mp_file_parser.file_parser
def _moose_header_parser(
    input_file: str,
    **_) -> typing.Dict[str, str]:
    """Method which parses the header of the MOOSE log file and returns the data from it as a dictionary.

    Parameters
    ----------
    input_file : str
        The path to the file where the console log is stored.

    Returns
    -------
    typing.Dict[str, str]
        The parsed data from the header of the MOOSE log file
    """
    # Open the log file, and read header lines (which contains information about the MOOSE version used etc)
    with open(input_file) as file:
        file_lines = file.readlines()
    file_lines = list(filter(None, file_lines))

    # Add the data from each line of the header into a dictionary as a key/value pair
    header_data = {}
    for line in file_lines:
        # Ignore blank lines
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        key = key.replace(" ","_").lower()
        # Ignore lines which correspond to 'titles'
        if not value:
            continue
        value = value.strip()
        if not value:
            continue
        header_data[key] = value

    return {}, header_data        

class MooseRun(WrappedRun):
    def _per_event_callback(self, log_data: typing.Dict[str, str], _):
        """Method which looks out for certain phrases in the MOOSE log, and adds them to the Events log

        Parameters
        ----------
        log_data : typing.Dict[str, str]
            Phrases of interest identified by the file monitor
        Returns
        -------
        bool
            Returns False if unable to upload events, to signal an error
        """

        # Look for relevant keys in the dictionary of data which we are passed in, and log the event with Simvue
        if any(key in ("time_step", "converged", "non_converged", "finished") for key in log_data.keys()):
            try:
                self.log_event(list(log_data.values())[0])
            except RuntimeError as e:
                self._error(e)
                return False

        if "time_step" in log_data.keys():
            self._time = time.time()
        
        elif "converged" in log_data.keys():
            self.log_event(f"Step calculation time: {round((time.time() - self._time), 2)} seconds.")
        
        # If simulation has completed successfully, terminate multiparser
        elif "finished" in log_data.keys():
            time.sleep(1) # To allow other processes to complete
            self._trigger.set()

    def _per_metric_callback(self, csv_data, sim_metadata):
        """Monitor each line in the results CSV file, and add data from it to Simvue Metrics."""

        metric_time = csv_data.pop('time')

        # Log all results for this timestep as Metrics
        self.log_metrics(
            csv_data,
            time = metric_time,
            timestamp = sim_metadata['timestamp']
        )

    def pre_simulation(self):
        super().pre_simulation()

        # Add alert for a non converging step
        self.create_alert(
            name='step_not_converged',
            source='events',
            frequency=1,
            pattern=' Solve Did NOT Converge!',
            notification='email'
            )

        # Save the MOOSE file for this run to the Simvue server
        if os.path.exists(self.moose_file_path):
            self.save_file(self.moose_file_path, "code") 

        # Save the MOOSE Makefile
        if os.path.exists(os.path.join(os.path.dirname(self.moose_application_path), "Makefile")):
            self.save_file(os.path.join(os.path.dirname(self.moose_application_path), "Makefile"), 'input')

        # Add the MOOSE simulation as a process, so that Simvue can abort it if alerts begin to fire
        self.add_process(
            identifier='moose_simulation',
            executable=str(self.moose_application_path),
            i=str(self.moose_file_path),
            color="off",
            **self.moose_env_vars
            )
    
    def during_simulation(self):
        # Read the initial information within the log file when it is first created, to parse the header information
        self.file_monitor.track(
            path_glob_exprs = os.path.join(self.output_dir_path, f"{self.results_prefix}.txt"),
            callback = lambda header_data, metadata: self.update_metadata({**header_data, **metadata}), 
            parser_func = _moose_header_parser, 
            static = True,
        )
        # Monitor each line added to the MOOSE log file as the simulation proceeds and look out for certain phrases to upload to Simvue
        self.file_monitor.tail(
            path_glob_exprs = os.path.join(self.output_dir_path, f"{self.results_prefix}.txt"), 
            callback = self._per_event_callback,
            tracked_values = [re.compile(r"Time Step.*"), " Solve Converged!", " Solve Did NOT Converge!", "Finished Executing"], 
            labels = ["time_step", "converged", "non_converged", "finished"]
        )
        # Monitor each line added to the MOOSE results file as the simulation proceeds, and upload results to Simvue
        self.file_monitor.tail(
            path_glob_exprs =  os.path.join(self.output_dir_path, f"{self.results_prefix}.csv"),
            parser_func = mp_tail_parser.record_csv,
            callback = self._per_metric_callback
        )

    def post_simulation(self):
        if os.path.exists(os.path.join(self.output_dir_path, f"{self.results_prefix}.e")):
            self.save_file(os.path.join(self.output_dir_path, f"{self.results_prefix}.e"), "output")
                        
    @pydantic.validate_call
    def launch(
        self, 
        moose_application_path: pydantic.FilePath,
        moose_file_path: pydantic.FilePath,
        output_dir_path: str, # as this might not exist yet
        results_prefix: str,
        moose_env_vars: typing.Optional[typing.Dict[str, typing.Any]] = None
        ):

        self.moose_application_path = moose_application_path
        self.moose_file_path = moose_file_path
        self.output_dir_path = output_dir_path
        self.results_prefix = results_prefix
        self.moose_env_vars = moose_env_vars or {}

        super().launch()