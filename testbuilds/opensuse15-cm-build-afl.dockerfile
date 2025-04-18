FROM opensuse/leap:15.6
ARG no_check=false
ARG no_install=false
ENV GPG --no-gpg-checks
ENV src src

RUN zypper $GPG refresh repo-oss
RUN zypper $GPG install -r repo-oss -y gcc zlib-devel python3 cmake unzip zip gzip tar
RUN cmake --version
RUN zypper $GPG install -y afl clang15
RUN { echo '#! /bin/bash'; echo 'args=()' \
   ; echo 'while [ 0 -lt "$#" ]; do case "$1" in *experimental-new-pass-manager*) : ;; *) args=("${args[@]}" "$1");; esac; shift; done' \
   ; echo 'echo args "${args[0]}"'; echo 'set +x'; echo 'exec clang-15 "${args[@]}"'; } > /usr/bin/clang.sh
RUN cat /usr/bin/clang.sh
RUN chmod +x /usr/bin/clang.sh
RUN ln -sf /usr/bin/clang.sh /etc/alternatives/clang
RUN zypper $GPG install -y wget

RUN mkdir -p $src
COPY CMakeLists.txt README COPYING.LIB ChangeLog $src/
COPY CMakeScripts $src/CMakeScripts
COPY bins $src/bins
COPY docs $src/docs
COPY test $src/test
COPY SDL $src/SDL
COPY zzipwrap $src/zzipwrap
COPY zzip $src/zzip

RUN mkdir $src/build
RUN cd $src/build && AFL_USE_ASAN=1 CC=afl-clang-fast CXX=afl-clang-fast++ cmake .. \
    -DZZIPTEST=OFF  -DCMAKE_C_FLAGS="-g2" -DCMAKE_BUILD_TYPE=Debug # -DBUILD_SHARED_LIBS=OFF

RUN cd $src/build && AFL_USE_ASAN=1 make
# RUN cd /src/build/bins && wget https://github.com/user-attachments/files/19536762/cl1.zip
# RUN cd $src/build/bins && wget https://github.com/user-attachments/files/19536855/cl2.zip
# RUN cd $src/build/bins && wget https://github.com/user-attachments/files/19536956/cl3.zip
# RUN cd $src/build/bins && unzip cl3.zip
# RUN cd $src/build/bins && ls -l && cat poc3.casrep
# RUN cd $src/build/bins && ./unzip-mem -tvX poc3 critical.bin *.dll

RUN $no_check || (cd $src/build && make check)
RUN $no_install || (cd $src/build && make install)
