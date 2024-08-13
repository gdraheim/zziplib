# FROM ubuntu:22.04
FROM ubuntu:jammy-20220428
ARG no_check=false
ARG no_install=false

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install -y gcc-9 zlib1g-dev python3 cmake unzip zip gzip tar pkg-config libsdl2-dev
## libsdl2-dev is on "universe"
## and gcc-14 is on "universe"

RUN mkdir src
COPY README COPYING.LIB ChangeLog src/
COPY CMakeLists.txt src/
COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip

RUN mkdir src/build
RUN cd src/build && cmake .. -DCMAKE_C_COMPILER=/usr/bin/gcc-9 -DZZIP_TESTCVE=OFF
RUN cd src/build && make
RUN $no_check || (cd src/build && make check)
RUN $no_install || (cd src/build && make install)

