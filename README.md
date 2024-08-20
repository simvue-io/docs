# Simvue documentation
Makes use of https://squidfunk.github.io/mkdocs-material/

## Launching the Docs website locally
To launch the docs locally:
1. Clone the docs repository: `git clone git@github.com:simvue-io/docs.git`
2. Create a virtual environment within the repo: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install the required modules: `pip install -r requirements.txt`
5. Launch the docs website: `mkdocs serve`
6. Open the locally hosted docs in a web browser - the address should be printed to the terminal, will most likely be `127.0.0.1:8000`

## MOOSE Example Docker Container
**Note**: This will not work over the UKAEA VPN due to (assumed) firewall issues with Dockerhub. If you are working remotely, disconnect from the VPN before following these instructions.

To rebuild the MOOSE Docker container:
1. Go to your Github account -> Account Settings -> Developer settings
2. Create a personal access token, with access to `read:packages`, `write:packages`, and `delete:packages`
3. Copy the personal access token somewhere (you will not be able to access it again)
4. Log into the Github Docker registry using `docker login ghcr.io -u <your username> -p <your access token>`
5. Change directory - `cd docker_images/moose`
6. Build the docker container with `sudo docker build -t ghcr.io/simvue-io/moose_example:latest -f docker/Dockerfile  . --no-cache`
7. Check that you can correctly run the container: `sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/moose_example:latest`
8. Exit the contaner with Ctrl D
9. Push the container into the registry: `docker push ghcr.io/simvue-io/moose_example:latest`

## Openfoam Example Docker Container
**Note**: This will not work over the UKAEA VPN due to (assumed) firewall issues with Dockerhub. If you are working remotely, disconnect from the VPN before following these instructions.

To rebuild the Openfoam Docker container:
1. Go to your Github account -> Account Settings -> Developer settings
2. Create a personal access token, with access to `read:packages`, `write:packages`, and `delete:packages`
3. Copy the personal access token somewhere (you will not be able to access it again)
4. Log into the Github Docker registry using `docker login ghcr.io -u <your username> -p <your access token>`
5. Change directory - `cd docker_images/openfoam`
6. Build the docker container with `sudo docker build -t ghcr.io/simvue-io/openfoam_example:latest -f docker/Dockerfile  . --no-cache`
7. Check that you can correctly run the container: `sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/openfoam_example:latest`
8. Exit the contaner with Ctrl D
9. Push the container into the registry: `docker push ghcr.io/simvue-io/openfoam_example:latest`

## FDS Example Docker Container
**Note**: This will not work over the UKAEA VPN due to (assumed) firewall issues with Dockerhub. If you are working remotely, disconnect from the VPN before following these instructions.

To rebuild the FDS Docker container:
1. Go to your Github account -> Account Settings -> Developer settings
2. Create a personal access token, with access to `read:packages`, `write:packages`, and `delete:packages`
3. Copy the personal access token somewhere (you will not be able to access it again)
4. Log into the Github Docker registry using `docker login ghcr.io -u <your username> -p <your access token>`
5. Change directory - `cd docker_images/fds`
6. Build the docker container with `sudo docker build -t ghcr.io/simvue-io/fds_example:latest -f docker/Dockerfile  . --no-cache`
7. Check that you can correctly run the container: `sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/fds_example:latest`
8. Exit the contaner with Ctrl D
9. Push the container into the registry: `docker push ghcr.io/simvue-io/fds_example:latest`
