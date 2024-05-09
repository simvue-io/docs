
import os.path
import typing
import re
import os
import logging
import uuid
import argparse
import multiprocessing
import subprocess
import signal
import time

from multiparser import FileMonitor
import multiparser.parsing.tail as mp_tail_parse
from simvue import Run


@mp_tail_parse.log_parser
def custom_parser(file_data: str, **_) -> typing.Tuple[typing.Dict[str, typing.Any], typing.List[typing.Dict[str, typing.Any]]]:
    _regex_parser_str = r"""
    ^\s*Mesh\s+(\d+)\n
    \s*Max\sCFL\snumber:\s+(-*\d+\.\d+e*-*\d+).+\n
    \s*Max\sdivergence:\s+(-*\d+\.\d+e*-*\d+).+\n
    \s*Min\sdivergence:\s+(-*\d+\.\d+e*-*\d+).+\n
    \s*Max\sVN\snumber:\s+(-*\d+\.\d+e*-*\d+).+\n
    """

    _parser = re.compile(_regex_parser_str, re.IGNORECASE | re.MULTILINE | re.VERBOSE)
    _out_data = []

    for match_group in _parser.finditer(file_data):
        _mesh_number = match_group.group(1)
        _out_data += [{
            f"max_cfl_number_{_mesh_number}": float(match_group.group(2)),
            f"max_divergence_{_mesh_number}": float(match_group.group(3)),
            f"min_divergence_{_mesh_number}": float(match_group.group(4)),
            f"max_vn_number_{_mesh_number}": float(match_group.group(5)),
        }]
    return {}, _out_data


if __name__ in "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("tracking_dir")
    parser.add_argument("--execute", help="Execute a process in parallel", default=None)
    parser.add_argument("--offline", action="store_true", help="Run offline", )
    args = parser.parse_args()

    _trigger = multiprocessing.Event()

    with Run() as run:
        def debug_callback(data, meta, run_instance: Run=run):
            if args.offline:
                print(f"Recorded: {data}\n{meta}")
                return

            run_instance.log_metrics(data, timestamp=meta["timestamp"])
        def meta_update(data, meta, run_instance: Run=run):
            print(f"Received '{meta}'\n\n'{data}'")
            if args.offline:
                return
            run_instance.update_metadata(metadata={k: v for k, v in data.items() if v})
        def testing_callback(data, meta):
            print(f"Received '{meta}'\n\n'{data}'")
        _id = str(uuid.uuid4()).split("-")[0]
        run.init(f"fire_safety_real_{_id}",)

        run.add_process(
            "simulation",
            executable="fds_unlim",
            ulimit="unlimited",
            input_file=f"{args.input_file}",
            completion_callback=lambda *_, **__: _trigger.set(),
            print_stdout=True,
            env=os.environ | {"PATH": f"{os.environ['PATH']}:{os.getcwd()}"}
        )
                
        with FileMonitor(
            per_thread_callback=debug_callback,
            exception_callback=run.log_event,
            interval=1,
            log_level=logging.DEBUG,
            flatten_data=True,
            plain_logging=True,
            termination_trigger=_trigger
        ) as monitor:
            monitor.track(
                path_glob_exprs=args.input_file,
                callback=meta_update,
                file_type="fortran",
                static=True
            )
            monitor.tail(
                path_glob_exprs=os.path.join(args.tracking_dir, "*.out"),
                parser_func=custom_parser
            )
            monitor.tail(
                path_glob_exprs=os.path.join(args.tracking_dir, "*_devc.csv"),
                parser_func=mp_tail_parse.record_csv,
                parser_kwargs={"header_pattern": "Time"}
            )
            run.add_alert(
                name="thermocouple_temperature_below_threshold",
                metric="THCP*",
                source="metrics",
                frequency=1,
                rule="is above",
                threshold=500
            )

            run.add_alert(
                name="visibility_near_eye_level_threshold",
                metric="VIS*",
                source="metrics",
                frequency=1,
                rule="is below",
                threshold=10
            )

            run.add_alert(
                name="fractional_effective_dose_threshold",
                metric="FED*",
                source="metrics",
                frequency=1,
                rule="is above",
                threshold=0.5
            )
            monitor.run()

