FROM openbcl/fds:6.9.1
WORKDIR /workdir
RUN apt update -y && \
apt upgrade -y && \
apt install -y \
    git \
    nano \
    python3 \
    python3-pip && \
apt clean
COPY files/warehouse_w_doors.fds /workdir/input.fds
COPY files/run_simulation.py /workdir/run_simulation.py
COPY files/simvue.ini /workdir/simvue.ini
RUN python3 -m pip install git+https://github.com/simvue-io/integrations.git@wk9874/fds_wrapper#egg=simvue-integrations[fds] --break-system-packages
#ENTRYPOINT [ "python3", "/workdir/run_simulation.py", "/workdir/input.fds" ]
