FROM ubuntu:18.04

# this can be optimized, but for rpi development this was faster

RUN apt update
RUN apt-get -y --no-install-recommends install bluez-tools bluez
RUN apt-get -y --no-install-recommends install python3-pip
RUN apt-get -y --no-install-recommends install build-essential python3-setuptools python3-wheel python3-gi
RUN apt-get -y --no-install-recommends install python3-dev
RUN apt-get -y --no-install-recommends install pkg-config
RUN apt-get -y --no-install-recommends install python3-dbus
RUN apt-get -y --no-install-recommends install locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  
RUN pip3 install gatt

