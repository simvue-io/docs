# docker build -t moose-training-workshop --build-arg compile_cores=4  -f docker/Dockerfile  .
# Adding --build-arg wsl=true builds an image that may be converted to wsl

# Base image
FROM lhumph/moose-training-workshop

# Specify the user for the container
ARG USERNAME=dev
ARG GIT_ACCESS_TOKEN_NAME
ARG GIT_ACCESS_TOKEN
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

# Add Simvue (support_v2_server for now), Multiparser (from Gitlab for now)
RUN /home/dev/.pyenv/versions/3.10.13/bin/python3.10 -m pip install git+https://github.com/simvue-io/client.git@support_v2_server#egg=simvue[plot,dataset]
RUN /home/dev/.pyenv/versions/3.10.13/bin/python3.10 -m pip install git+https://${GIT_ACCESS_TOKEN_NAME}:${GIT_ACCESS_TOKEN}@git.ccfe.ac.uk/kzarebsk/multiparser.git

# Some generic settings for building the image
ENV HOME=/home/${USERNAME}
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV TZ=Europe/London

# Remove workshop files
RUN rm -r problems
RUN rm -r tutorial

# Rename home directory
# RUN mv ${HOME}/moose-training-workshop ${HOME}/simvue-moose
# WORKDIR ${HOME}/simvue-moose

# Copy tutorial files
COPY --chown=${USERNAME} files .