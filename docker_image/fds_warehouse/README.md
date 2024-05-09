# Running with Multiparser

This directory contains an example using _Multiparser_ to process input and output files from the Fire Dynamic Simulator (FDS) live into Simvue. The input Fortran Named List is parsed and the data used as metadata for the run with the `.out` log file being monitored to observe changes to:

* Max CFL number
* Max divergence
* Min divergence
* Max number

Alerts are registered based on values present in the `*devc.csv` files:

* Thermocouple Temperature < 500
* Visibility Near Eye Level > 5
* Fractional Effective Dose < 0.5

## Running a Simulation

To run a simulation you will firstly need to make sure you have cloned the repository:

```sh
git clone https://github.com/simvue-io/fire-risk-use-case.git
```

It is recommended to build the contained Docker image, from the root of this repository run:

```sh
docker build --tag simvue_fds -f images/multiparse/multiparser.Dockerfile .
```

once built, ensure you have a Simvue `simvue.ini` configuration file and launch the simulation:

```sh
docker run --net=host \
--name fire_sim_demo_run \
-v $PWD/images/multiparse/data/test-16.fds:/workdir/simulation_input.fds \
-v $PWD/simvue.ini:/workdir/simvue.ini \
--rm simvue_fds
```

This will launch the simulation and run multiparser with Simvue to firstly collect metadata from the input file provided, then monitor the output file.