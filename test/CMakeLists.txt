cmake_minimum_required (VERSION 3.1)
project(zzipbins C)
set(VERSION "0.13.69")

string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\1" RELNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\2" VERNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\3" FIXNUM ${VERSION})
MESSAGE(STATUS "VERSION ${VERSION} -> RELNUM ${RELNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> VERNUM ${VERNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> FIXNUM ${FIXNUM}")

include ( GNUInstallDirs )
include ( FindPkgConfig )

# options ########################################################
option(BUILD_SHARED_LIBS "Build a shared library" ON)
option(BUILD_STATIC_LIBS "Build the static library" OFF)
option(BUILD_TESTS "Build test programs" OFF)
option(MSVC_STATIC_RUNTIME "Build with static runtime libs (/MT)" ON)

# Zlib library needed
find_package ( ZLIB REQUIRED )
# pkg_search_module ( ZZIP zzip )
# find_package ( PythonInterp 2.6 REQUIRED )
# find_package ( UnixCommands REQUIRED ) # bash cp mv rm gzip tar
find_program ( MKZIP zip)

set(EXEEXT ${CMAKE_EXECUTABLE_SUFFIX})
set(README ${CMAKE_SOURCE_DIR}/README)
# targets ########################################################
add_executable(zzipself    zzipself.c)
add_executable(zzipsetstub zzipsetstub.c)

target_link_libraries(zzipself     libzzip        ZLIB::ZLIB)
target_link_libraries(zzipsetstub  libzzip        ZLIB::ZLIB)

target_include_directories(zzipself     PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zzipsetstub  PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")

if(CMAKE_GENERATOR MATCHES "Makefiles")
add_custom_command(OUTPUT zzipshowme${EXEEXT}
   COMMAND rm -f test
   COMMAND ln -s . test
   COMMAND ${MKZIP} -0 -j $@ zzipself${EXEEXT}
   COMMAND ${MKZIP} -9 -j $@ ${README}
   COMMAND test -s $@ || cp test2.zip $@ || true
   COMMAND test ! -f $@.zip || mv $@.zip $@
   COMMAND ./zzipsetstub${EXEEXT} $@ zzipself${EXEEXT}
   COMMAND chmod +x $@
   DEPENDS zzipself zzipsetstub)
add_custom_target(sfx ALL DEPENDS zzipshowme${EXEEXT})
endif()

# install ########################################################
# - nothing -
