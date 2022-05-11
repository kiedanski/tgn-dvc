#FROM python:3.10.4-buster
FROM nvidia/cuda:11.6.0-devel-ubuntu20.04
ENV PYTHONBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/home/${USER}/workspace"
ARG USER=worker
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG "en_US.UTF-8"
ENV LANGUAGE "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"
# update system and certificates

COPY infra/apt-list.txt /tmp/apt-list.txt
RUN apt-get update \
    && apt-get install --no-install-recommends -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && xargs -a /tmp/apt-list.txt apt install --no-install-recommends -y \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

RUN ln -s /usr/bin/python3.7 /usr/bin/python
RUN locale-gen en_US.UTF-8

RUN python -m pip install --upgrade pip

RUN useradd -ms /bin/bash ${USER} 
USER ${USER}

COPY infra/requirements/base.txt /tmp/base.txt
RUN python -m pip install --user -r /tmp/base.txt

COPY infra/requirements/devel.txt /tmp/devel.txt
RUN python -m pip install --user -r /tmp/devel.txt

WORKDIR /home/${USER}/workspace
RUN git config --global user.name diego
RUN git config --global user.email diego@kiedanski.com
