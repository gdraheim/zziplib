FROM ubuntu:18.04
ARG no_check=false
ARG no_install=false

ARG _libdir=/usr/local/lib64
ARG _docdir=/usr/share/doc

RUN apt-get update
RUN apt-get install -y gcc zlib1g-dev python3 cmake unzip zip gzip tar pkg-config

RUN mkdir src
COPY README COPYING.LIB ChangeLog src/
COPY Makefile.am Makefile.in old.configure.ac old.configure config.h.in zziplib.spec src/
RUN test ! -f src/old.configure || mv src/old.configure src/configure
RUN test ! -f src/old.configure.ac || mv src/old.configure.ac src/configure.ac
COPY uses src/uses
# COPY CMakeLists.txt src/
# COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip

RUN mkdir src/build
RUN cd src/build && sh ../configure --libdir=$_libdir --with-docdir=$_docdir --disable-static
# RUN cd src/build && cmake .. `$no_check && echo -DZZIPTEST=OFF`
RUN cd src/build && make
RUN $no_check || (cd src/build && make check)
RUN $no_install || (cd src/build && make install)

