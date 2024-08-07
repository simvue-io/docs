# Simvue documentation
Makes use of https://squidfunk.github.io/mkdocs-material/

## MOOSE Docker File
**Note**: This will not work over the VPN due to (assumed) firewall issues with Dockerhub. If you are working remotely, disconnect from the VPN before following these instructions.

To rebuild the MOOSE Docker file:
1. Go to your Github account -> Account Settings -> Developer settings
2. Create a personal access token, with access to `read:packages`, `write:packages`, and `delete:packages`
3. Copy the personal access token somewhere (you will not be able to access it again)
4. Log into the Github Docker registry using `docker login ghcr.io -u <your username> -p <your access token>`
5. Change directory - `cd docker_images/moose`
6. Build the docker container with `sudo docker build -t ghcr.io/simvue-io/moose_example:latest -f docker/Dockerfile  . --no-cache`
7. Check that you can correctly run the container: `sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/moose_example:latest`
8. Exit the contaner with Ctrl D
9. Push the container into the registry: `docker push ghcr.io/simvue-io/moose_example:latest`

To rebuild the Openfoam Docker file:
1. Go to your Github account -> Account Settings -> Developer settings
2. Create a personal access token, with access to `read:packages`, `write:packages`, and `delete:packages`
3. Copy the personal access token somewhere (you will not be able to access it again)
4. Log into the Github Docker registry using `docker login ghcr.io -u <your username> -p <your access token>`
5. Change directory - `cd docker_images/openfoam`
6. Build the docker container with `sudo docker build -t ghcr.io/simvue-io/openfoam_example:latest -f docker/Dockerfile  . --no-cache`
7. Check that you can correctly run the container: `sudo docker run -e DISPLAY=${DISPLAY} -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -it ghcr.io/simvue-io/openfoam_example:latest`
8. Exit the contaner with Ctrl D
9. Push the container into the registry: `docker push ghcr.io/simvue-io/openfoam_example:latest`
