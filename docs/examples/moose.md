# MOOSE
This example demonstrates how you can use Simvue to track MOOSE simulations. In particular, it will show how you can:
- Extract data from files produced during the execution of MOOSE in real time
- Record Metadata, Metrics and Events based on data from these files
- Trigger Alerts based on Metric values
- Save Artifacts

## Setup

## Specifying the Problem
In our example, we will imagine that we are a coffee cup manufacturer, looking to design a new cup which we want to put onto the market. While we have decided on the shape and thickness of the mug, we aren't sure whether to make the mug out of Copper, Steel or Ceramic. The main factor which will influence our decision is how hot the handle of the mug gets - if it gets too hot, the customer won't be able to pick it up!

To model this scenario, we will model the fluid inside the cup as having an exponentially decaying temperature from 90 degrees Celsius to room temperature (20 degrees Celsius), and we will use MOOSE to simulate the conductive heat through the walls and handle of the mug over time. We will also get MOOSE to output the maximum, minimum and average temperature of the handle at every time step, so that we can monitor it effectively. We will say that if the average temperature of the handle goes above 50 degrees, then it will be too hot to hold, and the simulation can be aborted to save computational time.

## Setup
The easiest way to run this example is to use the provided Docker container:
### Install Docker
You will need to install the Docker CLI tool to be able to use the Docker container for this tutorial. [^^Full instructions for installing Docker can be found here^^](https://docs.docker.com/engine/install/). If you are running Ubuntu (either on a full Linux system or via WSL on Windows), you should be able to do:
```
sudo apt-get update && sudo apt-get install docker.io
```
To check that this worked, run `docker` - you should see a list of help for the commands.
### Pull Docker image
Next we need to obtain the tutorial materials from Docker Hub:
```
docker pull wk9874/simvue-moose
```
This may take some time to download. Once complete, if you run `docker images`, you should see an image with the name `wk9874/simvue-moose` listed.

### Run Docker container
Firstly, add Docker as a valid user of the X windows server, so that we can view results using Paraview:
```
xhost +local:docker
```
Then you can run the container:
```
docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it wk9874/simvue-moose:latest
```
If this is running correctly, you should see your command prompt change to something like:
```
dev:~/moose-training-workshop$
```
### Update Simvue Config File
Finally we need to update the config file inside the Docker container to use your credentials. Login to the web UI, go to the **Runs** page and click **Create new run**. You should then see the credentials which you need to enter into the `simvue.ini` file. Simply open the existing file using `nano simvue.ini`, and replace the contents with the information from the web UI.

!!! note
    If you restart the docker container at any point, you will need to repeat this step as your changes will not be saved

!!! warning
    Currently this tutorial will only work on the Dev02 server as it relies on methods implemented in the `support_v2_server` branch.
