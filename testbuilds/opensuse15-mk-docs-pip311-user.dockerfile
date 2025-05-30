FROM opensuse/leap:15.6
ARG no_check=false
ARG no_install=false
ENV GPG --no-gpg-checks
ENV python python3.11
ENV pythonx python311
ARG version=0.13.79
ENV version ${version}

RUN zypper $GPG refresh repo-oss
RUN zypper $GPG install -r repo-oss -y gcc zlib-devel ${pythonx} ${pythonx}-pip
RUN ${python} --version
RUN ${python} -m pip --version

RUN mkdir src
COPY pyproject.toml zzipbuildtests.py src/
COPY docs src/docs
COPY test src/test

RUN cd src && ${python} -m pip install . --no-compile --user 
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









