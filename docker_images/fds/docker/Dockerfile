FROM ubuntu:22.04
WORKDIR /workdir
RUN apt update -y && \
apt upgrade -y && \
apt install -y \
    git \
    nano \
    python3 \
    python3-pip \
    libxmu6 \
    libglu1 \
    libgl1 && \
apt-get install wget && \
apt clean
COPY files /workdir
RUN python3 -m pip install git+https://github.com/simvue-io/python-api.git@dev && \
python3 -m pip install git+https://github.com/simvue-io/integrations.git@main#egg=simvue-integrations[fds] && \
wget https://github.com/firemodels/fds/releases/download/FDS-6.9.1/FDS-6.9.1_SMV-6.9.1_lnx.sh && \
bash FDS-6.9.1_SMV-6.9.1_lnx.sh y && \
echo 'source /root/FDS/FDS6/bin/FDS6VARS.sh' >> /root/.bashrc && \
echo 'source /root/FDS/FDS6/bin/SMV6VARS.sh' >> /root/.bashrc && \
echo 'alias python=python3' >> ~/.bashrc && \
rm FDS-6.9.1_SMV-6.9.1_lnx.sh