FROM dockcross/windows-static-x64:latest
ARG no_check=false
ARG no_install=false

RUN mkdir src
COPY CMakeLists.txt README COPYING.LIB ChangeLog src/
COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip
RUN echo "" > src/CMakeScripts/CodeCoverage.cmake

RUN { echo "[requires]" \
    ; echo "zlib/1.2.13" \
    ; echo "" \
    ; echo "[generators]" \
    ; echo "CMakeToolchain" \
    ; } > src/conanfile.txt

RUN mkdir -p $HOME/.conan2/profiles
RUN { echo "[settings]" \
    ; echo "os=Linux" \
    ; echo "arch=x86_64" \
    ; echo "build_type=Release" \
    ; echo "compiler=gcc" \
    ; echo "compiler.version=12" \
    ; echo "[buildenv]" \
    ; echo "CC=/usr/src/mxe/usr/bin/x86_64-w64-mingw32.static-gcc" \
    ; } > $HOME/.conan2/profiles/default

RUN { echo "[settings]" \
    ; echo "os=Windows" \
    ; echo "arch=x86_64" \
    ; echo "build_type=Release" \
    ; echo "compiler=gcc" \
    ; echo "compiler.version=12" \
    ; } > $HOME/.conan2/profiles/windows

RUN mkdir src/build
RUN cd src/build && conan install ..  --build=missing --profile:host=windows --profile:build=default 
RUN cd src/build && cmake .. -DCMAKE_TOOLCHAIN_FILE=./conan_toolchain.cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_SYSTEM_NAME=Windows -DZZIPTEST=OFF
RUN cd src/build && cmake --build .
# RUN $no_check || (cd src/build && make check)
# RUN $no_install || (cd src/build && make install)
RUN cd src/build && cmake --build . --target install

