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
RUN apt-get install -y gcc ${pythonx} ${pythonx}-pip
RUN ${python} --version
RUN ${python} -m pip --version
RUN ${python} -m pip --version| { read n ver x; [ 24 -le ${ver%%.*} ] || echo "need atleast pip 24 (have pip $ver)" >&2; }

RUN mkdir src
COPY pyproject.toml zzipbuildtests.py src/
COPY docs src/docs
COPY test src/test

RUN cd src && ${python} -m pip install . --no-compile --user --break-system-packages
RUN ${python} -m pip show --files zzipmakedocs
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









