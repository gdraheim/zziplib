FROM almalinux:9.4
ARG no_check=false
ARG no_install=false

RUN echo sslverify=false >> /etc/yum.conf
RUN yum install -y gcc zlib-devel python3 cmake make unzip zip gzip tar diffutils
RUN cmake --version

RUN mkdir src
COPY CMakeLists.txt COPYING.LIB ChangeLog src/
COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip

RUN mkdir src/build
RUN cd src/build && cmake .. `$no_check && echo -DZZIPTEST=OFF`
RUN cd src/build && make
RUN $no_check || (cd src/build && make check)
RUN $no_install || (cd src/build && make install)

