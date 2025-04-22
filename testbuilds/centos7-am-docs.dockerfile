FROM centos:7.9.2009
ARG no_build=false

ARG _libdir=/usr/local/lib64
ARG _docdir=/usr/share/doc

RUN yum install -y epel-release
RUN echo sslverify=false >> /etc/yum.conf
RUN yum install -y gcc zlib-devel python3 make unzip zip gzip tar

RUN mkdir src
COPY Makefile.am Makefile.in old.configure.ac old.configure config.h.in zziplib.spec src/
RUN test ! -f src/old.configure || mv src/old.configure src/configure
RUN test ! -f src/old.configure.ac || mv src/old.configure.ac src/configure.ac
COPY uses src/uses

COPY CMakeLists.txt COPYING.LIB ChangeLog src/
COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip

RUN mkdir src/build
RUN cd src/build && sh ../configure --libdir=$_libdir --with-docdir=$_docdir --disable-static
RUN $no_build || (cd src/build && make)
RUN cd src/build && make docs
RUN cd src/build && make install-docs install-mans
