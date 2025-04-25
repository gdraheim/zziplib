# FROM ubuntu:24.04
FROM ubuntu:noble-20240530
ARG no_check=false
ARG no_install=false

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install -y gcc zlib1g-dev python3 cmake unzip zip gzip tar pkg-config  
RUN apt-get install -y curl git build-essential ninja-build jq
RUN cmake --version
RUN : "cmake 3.30 is required" # for vcpkg 2025-04-16
RUN : "ninja 1.21.1 is required" # for vcpkg 2025-04-16
RUN pkg-config --version zlib
# RUN cd tmp || exit 5; curl -LO https://aka.ms/vcpkg-init.sh || exit 1; ls -ltr1 ; head vcpkg-init.sh
# RUN cd tmp; bash ./vcpkg-init.sh --help 
# RUN cd tmp; bash -c "cat ./vcpkg-init.sh" 
# RUN cd tmp; bash -c ". ./vcpkg-init.sh" # the script uses bashisms
RUN :
RUN cd tmp && curl -LO  https://github.com/microsoft/vcpkg-tool/releases/download/2024-03-14/vcpkg-init
RUN cd tmp ; bash ./vcpkg-init --help
RUN cd tmp ; bash -c ". ./vcpkg-init" 
RUN :
RUN find $HOME/.vcpkg/vcpkg-artifacts -type f | wc -l | sed "s:^:.vcpkg/vcpkg-artifacts files =:"
RUN find $HOME/.vcpkg -type f | sed /vcpkg-artifacts/d
RUN export PATH="$PATH:$HOME/.vcpkg"; which vcpkg; vcpkg --help; true
# RUN f=~/.vcpkg/scripts/templates/vcpkg.json.in ; echo "== $f"; cat $f
# RUN f=~/.vcpkg/scripts/vcpkg-tools.json ; echo "== $f"; cat $f
# RUN f=~/.vcpkg/vcpkg-version.txt ; echo "== $f"; cat $f

RUN mkdir src
COPY COPYING.LIB ChangeLog src/
COPY CMakeLists.txt src/
COPY vcpkg.json src/
COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip

RUN mkdir src/build
# RUN mv src/vcpkg.json src/vcpkg.json.orig
# RUN cat src/vcpkg.json.orig | jq '.overrides=[{ "name":"zlib", "version": "2.10" }]' > src/vcpkg.json
RUN { echo '{'; \
   echo '"default-registry"': '{' '"kind"': '"git"', '"baseline"': '"7476f0d4e77d3333fbb249657df8251c28c4faae"', '"repository"': '"https://github.com/microsoft/vcpkg"' '}'; \
   echo '}';  } > src/vcpkg-configuration.json
RUN cat src/vcpkg-configuration.json
RUN git --version
RUN cd src/build && cmake .. -GNinja \
   -DCMAKE_TOOLCHAIN_FILE=$HOME/.vcpkg/scripts/buildsystems/vcpkg.cmake \
   -DCMAKE_BUILD_PROGRAM=/usr/bin/ninja \
   -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja \
   -DCMAKE_C_COMPILER=/usr/bin/gcc ; \
   -DVCPKG_LANGUAGES=C \
   -DZZIPTEST=OFF \
RUN exit 0; \
   set -x ; \
   cat /root/.vcpkg/buildtrees/detect_compiler/config-x64-linux-rel-CMakeCache.txt.log ; \
   cat /root/.vcpkg/buildtrees/detect_compiler/config-x64-linux-rel-out.log \
       /root/.vcpkg/buildtrees/detect_compiler/config-x64-linux-rel-err.log
RUN cd src/build && ninja 
RUN $no_check || (cd src/build && ninja check)
RUN $no_install || (cd src/build && ninja install)

