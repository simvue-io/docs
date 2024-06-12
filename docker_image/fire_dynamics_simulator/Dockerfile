FROM openbcl/fds:6.9.1
WORKDIR /workdir
RUN apt update -y && \
apt upgrade -y && \
apt install -y \
    git \
    python3 \
    python3-pip && \
apt clean
COPY example/warehouse_w_doors.fds /workdir/input.fds
COPY run_simulation.py /workdir/run_simulation.py
COPY fds_unlim /workdir/fds_unlim
RUN python3 -m pip install git+https://github.com/simvue-io/client.git@v1.0-rc2 --break-system-packages
RUN python3 -m pip install ukaea-multiparser[fortran] click --break-system-packages
ENTRYPOINT [ "python3", "/workdir/run_simulation.py", "/workdir/input.fds" ]