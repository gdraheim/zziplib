cmake_minimum_required (VERSION 3.1)
project(zzipwrap C)
set(VERSION "0.13.69")

if(NOT ${RELNUM})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\1" RELNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\2" VERNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\3" FIXNUM ${VERSION})
MESSAGE(STATUS "VERSION ${VERSION} -> RELNUM ${RELNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> VERNUM ${VERNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> FIXNUM ${FIXNUM}")
endif()

include ( CheckIncludeFiles )
include ( GNUInstallDirs )
include ( FindPkgConfig )

# options ########################################################
option(BUILD_SHARED_LIBS "Build a shared library" ON)
option(BUILD_STATIC_LIBS "Build the static library" OFF)
option(BUILD_TESTS "Build test programs" OFF)
option(MSVC_STATIC_RUNTIME "Build with static runtime libs (/MT)" ON)

check_include_files ( unistd.h ZZIP_HAVE_UNISTD_H )
# set ( ZZIP_HAVE_ZLIB_H 1 )

# Zlib library needed
find_package ( ZLIB REQUIRED )
pkg_search_module ( ZZIP zzip )

# targets ########################################################
set(zzipwrap_SRCS
    zzipwrap.c)

set(libzzipwrap_SRCS 
    wrap.c)

set(libzzipwrap_HDRS
    wrap.h)

add_library(libzzipwrap ${libzzipwrap_SRCS} )
target_link_libraries(libzzipwrap libzzip ZLIB::ZLIB )
target_include_directories (libzzipwrap PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${ZZIP_INCLUDE_DIR})

set_target_properties(libzzipwrap PROPERTIES OUTPUT_NAME "zzipwrap" RELEASE_POSTFIX "-${RELNUM}")
SET_TARGET_PROPERTIES(libzzipwrap PROPERTIES VERSION ${VERNUM}.${FIXNUM} SOVERSION ${VERNUM})

add_executable(zzipwrap ${zzipwrap_SRCS} )
target_link_libraries(zzipwrap libzzipwrap )

if(UNIX)
add_custom_command(OUTPUT zzipwrap.pc
   COMMAND ${BASH} -c "echo 'prefix=${CMAKE_INSTALL_PREFIX}' > zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'libdir=\${prefix}/${CMAKE_INSTALL_LIBDIR}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'includedir=\${prefix}/${CMAKE_INSTALL_INCLUDEDIR}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo '' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Name: ${PROJECT_NAME}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Description: Callback Wrappers for ZZipLib' >> zzipwrap.c"
   COMMAND ${BASH} -c "echo 'Version: ${VERSION}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Requires: zziplib' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Libs: -L\${libdir} -lzzipwrap' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Cflags: -I\${includedir}' >> zzipwrap.pc"
   VERBATIM)
add_custom_target(pkgconfigs ALL DEPENDS zzipwrap.pc)
endif()

# install ########################################################
set(outdir ${CMAKE_CURRENT_BINARY_DIR})

if(UNIX)
install(FILES ${outdir}/zzipwrap.pc 
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/pkgconfig" )
endif()

install(FILES ${libzzipwrap_HDRS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/zzip )
install(TARGETS libzzipwrap
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
