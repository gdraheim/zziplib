# FROM ubuntu:24.04
FROM ubuntu:noble-20240530
ARG no_check=false
ARG no_install=false

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN :
RUN apt-get install -y gcc zlib1g-dev python3 cmake unzip zip gzip tar pkg-config 
RUN cmake --version
RUN apt-get install -y python3-pip python3-requests python3-urllib3 python3-colorama python3-yaml python3-jinja2 python3-dateutil python3-six python3-markupsafe python3-fasteners
RUN apt-get install -y python3-fasteners # python3-distro # (1.9>1.4-1.8) # python3-patch-ng # (1.9<1.18-1.19)
RUN python3 -m pip install conan --break-system-packages
RUN conan --version
RUN cmake --version
# RUN apt-get install -y make build-essential
RUN pkg-config --version zlib

RUN mkdir src
COPY COPYING.LIB ChangeLog src/
COPY CMakeLists.txt src/
COPY conanfile.py src/
COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip

RUN cd src && conan profile detect
RUN { echo "[replace_requires]"; echo "zlib/*: zlib/system"; } >>  "/root/.conan2/profiles/default"
RUN cd src && conan editable add .
RUN mkdir src/build
RUN cd src/build && conan install ..
RUN cd src/build && cmake .. --preset conan-release 
# RUN cd src/build && cmake .. --preset conan-release `$no_check && echo -DZZIPTEST=OFF`
# RUN cd src/build && cmake --build .. --preset conan-release 
RUN cd src/build/Release && make
RUN $no_check || (cd src/build/Release && make check)
RUN $no_install || (cd src/build/Release && make install)

