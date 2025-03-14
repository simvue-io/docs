# Introduction  

Welcome to the second tutorial on how to use Simvue, which uses the techniques covered in the first tutorial, as well as some more advanced functionality. This tutorial focuses on an example simulation using MOOSE (Multiphysics Object-Oriented Simulation Environment), which is an open-source, parallel finite element framework for solving various Physics problems. However while focussed on MOOSE, the techniques covered are applicable to any software which produces output files which you want to keep track of. In this tutorial we will define a simple problem, briefly discuss how to set up the MOOSE input file to solve this problem, and use Simvue to track the progress of the simulation. If you have not done so yet, we recommend that you [^^work through the first tutorial before attempting this one^^](/tutorial_basic/introduction).

By the end of this tutorial, you will be able to:

- [^^Setup and run a simple MOOSE simulation^^](/tutorial_advanced/defining-the-problem#creating-the-moose-input-file)
- [^^Use Multiparser to track a live updating log file produced during simulations^^](/tutorial_advanced/tracking-the-log/#initializing-the-file-monitor)
- [^^Use callbacks to log Events^^](/tutorial_advanced/tracking-the-log#adding-a-callback-function), and [^^create Alerts based on those Events^^](/tutorial_advanced/tracking-the-log#adding-alerts)
- [^^Run simulations as Processes in Simvue, for starting and stopping automatically^^](/tutorial_advanced/tracking-the-log#creating-simvue-processes)
- [^^Use custom parsers to retrieve and store data from arbitrary files^^](/tutorial_advanced/tracking-the-log#creating-a-custom-parser)
- [^^Use Multiparser to track a series of results files and store them as Metrics^^](/tutorial_advanced/tracking-results#parsing-values-and-adding-metrics)
- [^^Create Alerts based on Metrics^^](/tutorial_advanced/tracking-results#adding-alerts)
- [^^Retrieve Alert values from the server^^](/tutorial_advanced/tracking-results#monitoring-alerts-using-the-client), and [^^abort simulation runs based on Alert values^^](/tutorial_advanced/tracking-results#using-firing-alerts-to-terminate-a-run)

There are two options for following along with this tutorial. The recommended option is to use the provided Docker container, which has MOOSE, Paraview, and Simvue pre installed. The scripts which we produce after each step are also provided in the container so that you can run them more easily. You could alternatively install each component individually, and brief instructions for this are also listed below.

!!! note
    This tutorial uses MOOSE as an example simulation to teach you how to build your own custom scripts for tracking any generic simulation. We do also provide a Connector class for convenient tracking of MOOSE scripts specifically (along with a number of other simulation softwares), so if you just want to easily track your MOOSE simulations then [^^see here for an example of using that Connector.^^](/examples/moose)

## Option 1: Setup using Docker container **(Recommended)**

When running inside the provided docker container, each step in the tutorial has a corresponding file stored in the container. To run these, look out for boxes in each step which look like this:
!!! docker "Run in Docker Container"
    The commands to run on the docker container will be inside boxes like this.

### Install Docker

You will need to install the Docker CLI tool to be able to use the Docker container for this tutorial. [^^Full instructions for installing Docker can be found here^^](https://docs.docker.com/engine/install/). If you are running Ubuntu (either on a full Linux system or via WSL on Windows), you should be able to do:

```sh
sudo apt-get update && sudo apt-get install docker.io
```

To check that this worked, run `docker` - you should see a list of help for the commands.

!!! tip
    If you wish to run this on a Windows computer (without using Docker Desktop) via Windows Subsystem for Linux, [^^follow this guide on setting up Docker with WSL.^^](https://dev.to/bowmanjd/install-docker-on-windows-wsl-without-docker-desktop-34m9)

### Pull Docker image

Next we need to pull the container, which is stored in the Simvue repository's registry:

```sh
sudo docker pull ghcr.io/simvue-io/moose_example:latest
```

This may take some time to download. Once complete, if you run `sudo docker images`, you should see an image with the name `ghcr.io/simvue-io/moose_example` listed.

### Run Docker container

Firstly, add Docker as a valid user of the X windows server, so that we can view results using Paraview:

```sh
xhost +local:docker
```

Then you can run the container:

```sh
sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/moose_example:latest
```

If this is running correctly, you should see your command prompt change to something like:

```sh
dev:~/simvue-moose$
```

To test that the graphics packages are working correctly, run the command `paraview` within the container. After a few seconds, this should open up a graphical user interface window for the Paraview visualization tool.

!!! tip
    If you are using WSL and you do not see Paraview open correctly, it may be because your WSL is not set up correctly. To check this, exit the docker container by pressing <kbd>ctrl</kbd> + <kbd>D</kbd>, and then run the following commands:
    ```
    sudo apt-get install -y x11-apps
    xeyes
    ```
    This should open a small graphical display window, with a pair of eyes which follow your mouse around the screen. If you do not see this, [^^follow this guide to get graphical apps working on WSL^^](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps), and [^^look through these debugging tips for WSL^^](https://github.com/microsoft/wslg/wiki/Diagnosing-%22cannot-open-display%22-type-issues-with-WSLg).

### Update Simvue Config File

Finally we need to update the config file inside the Docker container to use your credentials. Login to the web UI, go to the **Runs** page and click **Create new run**. You should then see the credentials which you need to enter into the `simvue.toml` file. Simply open the existing file using `nano simvue.toml`, and replace the contents with the information from the web UI.

!!! note
    If you restart the docker container at any point, you will need to repeat this step as your changes will not be saved

You're now ready to start the tutorial! [^^Click here to go the first section^^](/tutorial_advanced/defining-the-problem), where we will begin by setting up our MOOSE simulation.

## Option 2: Custom Setup

### Create a virtual environment

Run the following commands to create and activate a new virtual environment:

```sh
python3 -m venv venv
source ./venv/bin/activate
```

### Install Simvue

Install the Python client:

```sh
pip install simvue
pip install ukaea-multiparser
```

### Configuring Simvue

The next step is to specify the URL of the Simvue server and provide an access token used to authenticate to the server.

Login to the web UI, go to the **Runs** page and click **Create new run**. Create a file called `simvue.toml` containing the contents as provided.
The file should look something like:

```toml
[server]
url = "https://dev01.simvue.io"
token = "eyJ0eXAi..."
```

### Install MOOSE

Next you will need to setup MOOSE on your computer. [^^See the installation instructions here^^](https://mooseframework.inl.gov/getting_started/installation/index.html), using the link corresponding to your operating system.

You will also need to create your MOOSE application - [^^see the instructions for creating a MOOSE application here^^](https://mooseframework.inl.gov/getting_started/new_users.html). You will not need to enable any extra Physics modules for this tutorial, so can leave the Makefile with the default values.

### Install Paraview

If you would like to see the solution generated by the MOOSE script, you will also want CAD software to view the output. Paraview is an open source program which can be used, [^^which can be downloaded here^^](https://www.paraview.org/download/). While this is not strictly necessary to follow along with the tutorial, it may give you a better picture of what the MOOSE simulation is doing.

You're now ready to start the tutorial! [^^Click here to go the first section^^](/tutorial_advanced/defining-the-problem), where we will begin by setting up our MOOSE simulation.
