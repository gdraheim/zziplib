FROM opensuse/leap:15.2
ARG no_check=false
ARG no_install=false
ARG no_parallel=false

RUN zypper mr --no-gpgcheck repo-oss repo-update
RUN zypper refresh repo-oss
RUN zypper install -r repo-oss -y gcc zlib-devel python3 cmake unzip zip gzip tar

RUN mkdir src
COPY CMakeLists.txt README COPYING.LIB ChangeLog src/
COPY CMakeScripts src/CMakeScripts
COPY bins src/bins
COPY docs src/docs
COPY test src/test
COPY SDL src/SDL
COPY zzipwrap src/zzipwrap
COPY zzip src/zzip

RUN mkdir src/build
# RUN cd src/build && cmake .. -DZZIPSDL=OFF -DZZIPDOCS=ON -DZZIP_HTMLSITE=ON -DZZIP_HTMPAGES=ON -DZZIPTEST=OFF
RUN cd src/build && cmake .. -DZZIPSDL=OFF -DZZIPDOCS=ON -DZZIP_HTMLSITE=ON -DZZIP_HTMPAGES=ON -DZZIP_TESTCVE=OFF
RUN if $no_parallel; then cd src/build && make all VERBOSE=ON; else \
                  cd src/build && make -j8 -w all VERBOSE=ON; fi
RUN $no_check || (cd src/build && make check)
RUN $no_install || (cd src/build && make install)
