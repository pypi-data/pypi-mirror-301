FROM python:3.11.9-alpine

# https://stackoverflow.com/a/65670826
ENV PBR_VERSION=6.1.0

RUN apk update && apk add gcc musl-dev linux-headers
RUN pip3 install pytest

#COPY . /opt/openstack-config
#WORKDIR /opt/openstack-config

#RUN pip install -e .

#CMD ["pytest", "tests/*.py"]