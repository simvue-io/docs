FROM openbcl/fds:6.9.1
RUN apt update -y && \
apt upgrade -y && \
apt install -y \
    git \
    python3 \
    python3-pip && \
apt clean
COPY run_simulation.py run_simulation.py
COPY fds_unlim fds_unlim
RUN python3 -m pip install git+https://github.com/simvue-io/client.git@dev
RUN python3 -m pip install ukaea-multiparser[fortran]