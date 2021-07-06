FROM debian:testing-slim

RUN apt-get update && apt-get install -y \
  gcc-mingw-w64 \
  python3 \
  python3-dev \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /npi
WORKDIR /npi

COPY buildfolder/thearchitect /npi/thearchitect

COPY buildfolder/requirements.txt /npi/requirements.txt
RUN python3 -m pip install -r /npi/requirements.txt

COPY buildfolder/entrypoint.sh /npi/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/npi/entrypoint.sh"]
