# docker build -t moose-training-workshop --build-arg compile_cores=4  -f docker/Dockerfile  .
# Adding --build-arg wsl=true builds an image that may be converted to wsl

# Base image
FROM lhumph/moose-training-workshop

# Specify the user for the container
ARG USERNAME=dev
USER ${USERNAME}

RUN sudo apt-get update && \
    sudo apt-get install -y \
    gcc-10 g++-10 \
    make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl && sudo apt clean

RUN curl https://pyenv.run | bash

COPY --chown=${USERNAME} docker/bashrc ${HOME}/.bashrc

RUN CC=gcc-10 CXX=g++-10 /home/dev/.pyenv/bin/pyenv install 3.10.13
RUN /home/dev/.pyenv/bin/pyenv global 3.10.13

# Add Simvue (dev for now), Multiparse
RUN /home/dev/.pyenv/versions/3.10.13/bin/python3.10 -m pip install git+https://github.com/simvue-io/client.git@v1.0-rc3#egg=simvue[plot,dataset]
RUN /home/dev/.pyenv/versions/3.10.13/bin/python3.10 -m pip install ukaea-multiparser

# Some generic settings for building the image
ENV HOME=/home/${USERNAME}
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV TZ=Europe/London

# Remove workshop files
RUN rm -r problems
RUN rm -r tutorial

# Copy Makefile which has Thermal Dynamics module enabled into app directory
COPY --chown=${USERNAME} docker/Makefile app/Makefile
WORKDIR ${HOME}/moose-training-workshop/app
RUN make clobber
RUN cp -r ${HOME}/moose-training-workshop ${HOME}/simvue-moose
WORKDIR ${HOME}/simvue-moose/app
RUN rm -r ${HOME}/moose-training-workshop
RUN make 
WORKDIR ${HOME}/simvue-moose

# Copy tutorial and example files
COPY --chown=${USERNAME} files .