FROM python:3.8.12-buster

WORKDIR /opt

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" \
    apt-get install --yes --no-install-recommends \
        jq \
        libmagic-dev \
        libxml2 \
        p7zip-full &&\
    apt-get autoremove --purge --yes && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/wagga40/Zircolite --branch=v2.6 --depth=1 && \
    python -m pip install pip setuptools wheel --upgrade && \
    pip install --requirement Zircolite/requirements.txt

WORKDIR /opt/Zircolite

ENTRYPOINT ["/usr/local/bin/python", "zircolite.py"]
