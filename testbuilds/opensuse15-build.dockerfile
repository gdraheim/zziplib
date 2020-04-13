# docker build -f opensuse15-build.dockerfile .

FROM opensuse/leap:15.1

RUN zypper refresh repo-oss
RUN zypper install -r repo-oss -y gcc zlib-devel python3 cmake unzip zip gzip tar
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

RUN mkdir src/build
RUN cd src/build && cmake ..
RUN cd src/build && make
RUN cd src/build && make check
