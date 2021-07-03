FROM debian:testing-slim

RUN apt-get update && apt-get install -y \
  gcc-mingw-w64 \
  python3 \
  python3-dev \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

COPY buildfolder/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
