# Fire Dynamics Simulator (FDS)

This example demonstrates integration of Simvue into simulations created using the [Fire Dynamics Simulator (FDS)](https://pages.nist.gov/fds-smv/) framework available from the National Institute of Standards and Technology (NIST). FDS is a freely available software which models the fluid dynamics and evolution of fire based events.

## Specifying the Problem

As example we will use 

## Setup

It is recommended that you use the provided Docker image which combines an FDS setup with the _Simvue_ client, and the _Multiparser_ module used to parse and handle output files.

```sh
docker pull ghcr.io/simvue-io/fds_example
```

## Executing a Simulation

You will also need a valid `simvue.ini` Simvue configuration file 