FROM openfoam/openfoam10-paraview56

USER root
RUN apt-get update && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.10 && \
    apt-get install -y python3.10-distutils && \
    apt-get install -y python3-pip && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 && \
    apt-get install python3.10-venv && \
    apt-get install -y git

RUN python3.10 -m venv venv && \
    venv/bin/python -m pip install git+https://github.com/simvue-io/integrations.git && \
    cp -r /opt/openfoam10/tutorials/incompressible/pimpleFoam/laminar/movingCone/ . && \
    cp -r /opt/openfoam10/tutorials/heatTransfer/buoyantFoam/hotRoom/ . && \
    cp -r /opt/openfoam10/tutorials/incompressible/simpleFoam/airFoil2D/ .

COPY --chown=${USERNAME} files .