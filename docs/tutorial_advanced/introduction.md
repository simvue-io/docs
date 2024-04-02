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

## Option 1: Setup using Docker container **(Recommended)**
When running inside the provided docker container, each step in the tutorial has a corresponding file stored in the container. To run these, look out for boxes in each step which look like this:
!!! docker "Run in Docker Container"
    The commands to run on the docker container will be inside boxes like this.

### Install Docker
You will need to install the Docker CLI tool to be able to use the Docker container for this tutorial. [^^Full instructions for installing Docker can be found here^^](https://docs.docker.com/engine/install/). If you are running Ubuntu (either on a full Linux system or via WSL on Windows), you should be able to do:
```
sudo apt-get update && sudo apt-get install docker.io
```
To check that this worked, run `docker` - you should see a list of help for the commands.
### Pull Docker image
Next we need to pull the container, which is stored in the Simvue repository's registry:
```
sudo docker pull ghcr.io/simvue-io/moose_example:latest
```
This may take some time to download. Once complete, if you run `sudo docker images`, you should see an image with the name `ghcr.io/simvue-io/moose_example` listed.

### Run Docker container
Firstly, add Docker as a valid user of the X windows server, so that we can view results using Paraview:
```
xhost +local:docker
```
Then you can run the container:
```
sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/moose_example:latest
```
If this is running correctly, you should see your command prompt change to something like:
```
dev:~/simvue-moose$
```
### Update Simvue Config File
Finally we need to update the config file inside the Docker container to use your credentials. Login to the web UI, go to the **Runs** page and click **Create new run**. You should then see the credentials which you need to enter into the `simvue.ini` file. Simply open the existing file using `nano simvue.ini`, and replace the contents with the information from the web UI.

!!! note
    If you restart the docker container at any point, you will need to repeat this step as your changes will not be saved

!!! warning
    Currently this tutorial will only work on the Dev02 Simvue server as it relies on methods implemented in the `dev` branch.
## Option 2: Custom Setup
### Create a virtual environment

Run the following commands to create and activate a new virtual environment:
```
python3 -m venv venv
source ./venv/bin/activate
```

### Install Simvue

Install the Python client:
```
pip install git+https://github.com/simvue-io/client.git@dev
pip install ukaea-multiparser
```

### Configuring Simvue

The next step is to specify the URL of the Simvue server and provide an access token used to authenticate to the server.

Login to the web UI, go to the **Runs** page and click **Create new run**. Create a file called `simvue.ini` containing the contents as provided.
The file should look something like:
```
[server]
url = https://dev02.simvue.io
token = eyJ0eXAi...
```

!!! warning
    Currently this tutorial will only work on the Dev02 server as it relies on methods implemented in the `dev` branch.
### Install MOOSE
Next you will need to setup MOOSE on your computer. [^^See the installation instructions here^^](https://mooseframework.inl.gov/getting_started/installation/index.html), using the link corresponding to your operating system. 

You will also need to create your MOOSE application - [^^see the instructions for creating a MOOSE application here^^](https://mooseframework.inl.gov/getting_started/new_users.html). You will not need to enable any extra Physics modules for this tutorial, so can leave the Makefile with the default values.

### Install Paraview
If you would like to see the solution generated by the MOOSE script, you will also want CAD software to view the output. Paraview is an open source program which can be used, [^^which can be downloaded here^^](https://www.paraview.org/download/). While this is not strictly necessary to follow along with the tutorial, it may give you a better picture of what the MOOSE simulation is doing.