# Launching processes

The Simvue client can launch and monitor commands traditionally launched on the command line via the `add_process` method. The command can be provided in a number of ways.

The simplest form is to provide a set of strings defining the command:
```python
run.add_process("my_process", "echo", "Hello World!")
```

## Specifying command components explicitly
Alternatively we can be more explicit in defining how the command is structured:

```python
run.add_process(
    identifier="my_model_run",
    executable="bash",
    script="run.sh",
    input_file="input.dat",
    env={"DATA_FILE_DIR": os.getcwd()}
)
```

when arguments are specified for `script` and `input_file` these are uploaded as `'code'` and `'input'` object types to Simvue automatically. Additional keyword arguments are treated as options to the command itself:

```python
run.add_process(
    identifier="run_third_party_python",
    executable="python",
    script="code_exe.py",
    input_file="input.dat",
    debug=True,             # Boolean options become flags
    output_dir=os.getcwd(), # Others become options
)
```

The command executed would then have the form:
```sh
python code_exe.py input.dat --debug --output-dir $PWD
```

## Termination triggers and callbacks

In addition the `add_process` method includes parameters relating to when the process completes. The argument `completion_callback` can be set to be a function of the form:

```python
def completion_callback_func(status_code: int, std_out: str, std_err: str) -> None:
    ...
```

and will be called once the process has terminated. Note due to differences in Python between UNIX and Windows based systems `completion_callback` is not supported on Windows at this time.

Alternatively `completion_trigger` is a `multiprocessing.Event` or `threading.Event` object which will be set once the process completes, this can then be used as a trigger:

```python
trigger = threading.Event()
run.add_process("my_process", executable="bash", c="echo 'Hello World!'", completion_trigger=trigger)

while not trigger.is_set():
    time.sleep(10)
```

## Monitoring

When a process is added to a Simvue run:

* The executed command is added to the metadata for that run.
* Any files specified by `input_file` or `script` are uploaded as artifacts.
* If not empty files, the `stdout` and `stderr` for the process are uploaded as artifacts.
* User alerts are created which are set to either "ok" or "critical" depending on process exit status.
