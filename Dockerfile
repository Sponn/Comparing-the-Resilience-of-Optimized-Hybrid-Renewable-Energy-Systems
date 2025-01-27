FROM python:3.10-buster
#FROM nvidia/cuda:12.2.2-base-ubuntu22.04
RUN apt-get update \
    && apt-get install -y \
        # python3.10 \
        # python3-pip \
        # python3-wheel \
        # python3-setuptools \
        git \
        sqlite3 \
        postgresql-client \
        build-essential \
        pandoc \
        graphviz \
        libgraphviz-dev \
    && apt-get autoremove -y \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*
COPY manual_requirements.txt /
RUN ls -a
RUN pip3 install git+https://gitlab.com/arl2/palaestrai-mosaik.git@parallel_execution
RUN pip3 install -r ./manual_requirements.txt
RUN midasctl configure -a
RUN midasctl download
RUN mkdir mounted
WORKDIR /mounted/code
#RUN nvidia-smi
ENTRYPOINT ["python3", "src/docker_execution.py"]