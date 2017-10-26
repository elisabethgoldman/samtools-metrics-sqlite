FROM ubuntu:zesty-20170915

MAINTAINER Jeremiah H. Savage <jeremiahsavage@gmail.com>

ENV VERSION 0.4

RUN apt-get update \
    && apt-get install -y \
       python3-pandas \
       python3-pip \
       python3-sqlalchemy \
    && apt-get clean \
    && pip3 install samtools_metrics_sqlite \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*