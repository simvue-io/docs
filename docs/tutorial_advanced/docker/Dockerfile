# docker build -t moose-training-workshop --build-arg compile_cores=4  -f docker/Dockerfile  .
# Adding --build-arg wsl=true builds an image that may be converted to wsl

# Base image
FROM lhumph/moose-training-workshop

# Specify the user for the container
ARG USERNAME=dev
USER ${USERNAME}

RUN sudo apt-get install -y python3.9
# Add Simvue (support_v2_server for now), Multiparser (from Gitlab for now)
RUN python3.9 -m pip install git+https://github.com/simvue-io/client.git@support_v2_server
RUN python3.9 -m pip install git+https://git.ccfe.ac.uk/kzarebsk/multiparser.git@main

# Some generic settings for building the image
ENV HOME=/home/${USERNAME}
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV TZ=Europe/London

# Remove workshop files
RUN rm -r problems
RUN rm -r tutorial

# Rename home directory
# RUN mv ${HOME}/moose-training-workshop ${HOME}/simue-moose
# WORKDIR ${HOME}/simue-moose

# Copy tutorial files
COPY --chown=${USERNAME} files tutorial