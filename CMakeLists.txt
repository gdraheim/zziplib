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

include ( GNUInstallDirs )

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
