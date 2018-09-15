cmake_minimum_required (VERSION 3.1)
project(zziplib C)
set(VERSION "0.13.69")

string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\1" RELNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\2" VERNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "0.\\3" FIXNUM ${VERSION})
MESSAGE(STATUS "VERSION ${VERSION} -> RELNUM ${RELNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> VERNUM ${VERNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> FIXNUM ${FIXNUM}")
# the "0." on FIXNUM is just for compatibility with automake's libtool.

### Path to additional CMake modules
# set(CMAKE_MODULE_PATH
#     ${CMAKE_SOURCE_DIR}/cmake
#     ${CMAKE_MODULE_PATH})

include ( GNUInstallDirs )

option(BUILD_SHARED_LIBS "Build a shared library" ON)
option(BUILD_STATIC_LIBS "Build the static library" OFF)
option(BUILD_TESTS "Build test programs" OFF)
option(MSVC_STATIC_RUNTIME "Build with static runtime libs (/MT)" ON)
option(ZZIPMMAPPED "Build libzzipmmapped (not fully portable)" ON)
option(ZZIPFSEEKO "Build libzzipfseeko (based on posix.1 api)" ON)
option(ZZIPWRAP "Build libzzipwrap (non-installed example)" ON)
option(ZZIPSDL "Build zzcatsdl (includable example code)" ON)
option(ZZIPBINS "Build bins/unzzip (unzip-like executables)" ON)
option(ZZIPTEST "Build test/zzipself (self-extract example)" ON)
option(ZZIPDOCS "Build docs/manpages (and website content)" ON)

add_subdirectory(zzip)

if(ZZIPWRAP)
add_subdirectory(zzipwrap)
endif()

if(ZZIPSDL)
add_subdirectory(SDL)
endif()

if(ZZIPBINS)
add_subdirectory(bins)
endif()

if(ZZIPTEST)
add_subdirectory(test)
endif()

if(ZZIPDOCS)
add_subdirectory(docs)
endif()
