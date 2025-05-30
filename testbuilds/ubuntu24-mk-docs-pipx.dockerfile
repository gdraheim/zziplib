# FROM ubuntu:24.04
FROM ubuntu:noble-20240530
ARG no_check=false
ARG no_install=false
ENV python python3
ENV pythonx python3
ARG version=0.13.79
ENV version ${version}

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install -y gcc pipx
RUN :
RUN pipx --version
RUN pipx --help
RUN pipx install --help

RUN mkdir src
COPY pyproject.toml zzipbuildtests.py src/
COPY docs src/docs
COPY test src/test

RUN cd src && pipx install .
RUN PATH="${PATH}:$HOME/.local/bin" zzipmakedocs.py --version
RUN PATH="${PATH}:$HOME/.local/bin" zzip-dbk2man --version

COPY zzip zzip
RUN PATH="${PATH}:$HOME/.local/bin" zzipmakedocs.py --package=zziplib --release=${version} --onlymainheader=zzip/lib.h zzip/*.c
RUN :
RUN PATH="${PATH}:$HOME/.local/bin" zzip-dbk2man man zziplib.docbook -o man
RUN find man -type f
RUN install -d /usr/local/share/man/man3
RUN install man/man3/* /usr/local/share/man/man3/
RUN :
RUN PATH="${PATH}:$HOME/.local/bin" zzip-dbk2man html zziplib.docbook -o html
RUN find html -type f
RUN install -d /usr/local/share/doc/zziplib/man
RUN install html/* /usr/local/share/doc/zziplib/man/









