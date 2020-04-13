FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y gcc zlib1g-dev python3 cmake unzip zip gzip tar

RUN mkdir src
COPY CMakeLists.txt README COPYING.LIB ChangeLog src/
COPY bins src/bins
COPY docs src/docs
COPY test src/test
copy SDL src/SDL
copy zzipwrap src/zzipwrap
copy zzip src/zzip

RUN mkdir src/build
RUN cd src/build && cmake ..
RUN cd src/build && make
RUN cd src/build && make check
