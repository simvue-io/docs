
import os.path
import typing
import re
import os
import logging
import uuid
import multiprocessing
import click

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


@click.command
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--offline", is_flag=True, help="Run Simvue in offline mode", default=False)
def run_fds(input_file: str, offline: bool) -> None:
    if (not os.environ.get("SIMVUE_URL") or not os.environ.get("SIMVUE_TOKEN")) and not os.path.exists("simvue.ini"):
        click.secho("No Simvue credentials provided", fg="red", bold=True)
        raise click.Abort
    logging.getLogger().setLevel(logging.DEBUG)

    _trigger = multiprocessing.Event()

    click.echo(f"Running FDS simulation with input '{input_file}'")

    with Run() as run:
        def debug_callback(data, meta, run_instance: Run=run):
            if offline:
                click.secho(f"Recorded: {data}\n{meta}", bold=True)
                return

            run_instance.log_metrics(data, timestamp=meta["timestamp"])

        def meta_update(data, meta, run_instance: Run=run):
            click.secho(f"Received '{meta}'\n\n'{data}'", bold=True)
            if offline:
                return
            run_instance.update_metadata(metadata={k: v for k, v in data.items() if v})

        _id = str(uuid.uuid4()).split("-")[0]
        run.init(
            f"fire_safety_real_{_id}",
        )

        run.add_process(
            "simulation",
            executable="fds_unlim",
            ulimit="unlimited",
            input_file=input_file,
            completion_callback=lambda *_, **__: _trigger.set(),
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
                path_glob_exprs=input_file,
                callback=meta_update,
                file_type="fortran",
                static=True
            )
            monitor.tail(
                path_glob_exprs=["*.out"],
                parser_func=custom_parser
            )
            monitor.tail(
                path_glob_exprs=["*_devc.csv"],
                parser_func=mp_tail_parse.record_csv,
                parser_kwargs={"header_pattern": "Time"}
            )
            run.create_alert(
                name="thermocouple_temperature_below_threshold",
                metric="THCP*",
                source="metrics",
                frequency=1,
                rule="is above",
                threshold=500,
                trigger_abort=True
            )

            run.create_alert(
                name="visibility_near_eye_level_threshold",
                metric="VIS*",
                source="metrics",
                frequency=1,
                rule="is below",
                threshold=10,
                trigger_abort=True
            )

            run.create_alert(
                name="fractional_effective_dose_threshold",
                metric="FED*",
                source="metrics",
                frequency=1,
                rule="is above",
                threshold=0.5,
                trigger_abort=True
            )
            monitor.run()


if __name__ in "__main__":
    run_fds()
