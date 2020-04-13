FROM centos:7.7.1908

RUN yum install -y epel-release
RUN yum install -y gcc zlib-devel python3 cmake3 make unzip zip gzip tar
RUN mkdir src
COPY CMakeLists.txt README COPYING.LIB ChangeLog src/
COPY bins src/bins
COPY docs src/docs
COPY test src/test
copy SDL src/SDL
copy zzipwrap src/zzipwrap
copy zzip src/zzip
RUN ls src
RUN ls src/zzip

RUN yum search cmake
RUN rpm -q --list cmake3
RUN mkdir src/build
RUN cd src/build && cmake3 ..
RUN cd src/build && make
RUN cd src/build && make check
