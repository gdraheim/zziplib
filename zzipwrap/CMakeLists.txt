cmake_minimum_required (VERSION 3.1)
project(zzipwrap VERSION "0.13.74" LANGUAGES C)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeScripts")

include ( CheckIncludeFiles )
include ( GNUInstallDirs )
include ( FindPkgConfig )
include ( JoinPaths )

# options ########################################################
option(BUILD_SHARED_LIBS "Build a shared library" ON)
option(BUILD_TESTS "Build test programs" OFF)
option(MSVC_STATIC_RUNTIME "Build with static runtime libs (/MT)" ON)

if(UNIX OR MINGW)
option(ZZIP_LIBTOOL "Ensure binary compatibility with libtool" ON)
option(ZZIP_PKGCONFIG "Generate pkg-config files for linking" ON)
else()
option(ZZIP_LIBTOOL "Ensure binary compatibility with libtool" OFF)
option(ZZIP_PKGCONFIG "Generate pkg-config files for linking" OFF)
endif()

if((CMAKE_BUILD_TYPE STREQUAL "Release") AND (ZZIP_LIBTOOL OR ZZIP_PKGCONFIG))
option(ZZIP_LIBLATEST "Ensure libname.lib links to libname-REL.lib" ON)
else()
option(ZZIP_LIBLATEST "Ensure libname.lib links to libname-REL.lib" OFF)
endif()

check_include_files ( unistd.h ZZIP_HAVE_UNISTD_H )
# set ( ZZIP_HAVE_ZLIB_H 1 )

# Zlib library needed
find_package ( ZLIB REQUIRED )
pkg_search_module ( ZZIP zzip )

set(RELNUM "${PROJECT_VERSION_MAJOR}")
set(VERNUM "${PROJECT_VERSION_MINOR}")
set(FIXNUM "0.${PROJECT_VERSION_PATCH}")
# the "0." on FIXNUM is just for compatibility with automake's libtool.

# targets ########################################################
set(zzipwrap_SRCS
    zzipwrap.c)

set(libzzipwrap_SRCS 
    wrap.c)

set(libzzipwrap_HDRS
    wrap.h)

add_library(libzzipwrap ${libzzipwrap_SRCS} )
target_link_libraries(libzzipwrap libzzip ZLIB::ZLIB )
target_include_directories(libzzipwrap PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")

set_target_properties(libzzipwrap PROPERTIES OUTPUT_NAME "zzipwrap" RELEASE_POSTFIX "-${RELNUM}")
SET_TARGET_PROPERTIES(libzzipwrap PROPERTIES VERSION ${VERNUM}.${FIXNUM} SOVERSION ${VERNUM})
set_target_properties(libzzipwrap PROPERTIES DEFINE_SYMBOL "libzzip_EXPORTS")

add_executable(zzipwrap ${zzipwrap_SRCS} )
target_link_libraries(zzipwrap libzzipwrap )
target_include_directories(zzipwrap PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")

if(ZZIP_PKGCONFIG)
join_paths(libdir "\${prefix}" "${CMAKE_INSTALL_LIBDIR}")
join_paths(includedir "\${prefix}" "${CMAKE_INSTALL_INCLUDEDIR}")
add_custom_command(OUTPUT zzipwrap.pc
   COMMAND ${BASH} -c "echo 'prefix=${CMAKE_INSTALL_PREFIX}' > zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'libdir=${libdir}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'includedir=${includedir}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo '' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Name: ${PROJECT_NAME}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Version: ${PROJECT_VERSION}' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Description: Callback Wrappers for ZZipLib' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Requires: zziplib' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Libs: -L\${libdir} -lzzipwrap' >> zzipwrap.pc"
   COMMAND ${BASH} -c "echo 'Cflags: -I\${includedir}' >> zzipwrap.pc"
   VERBATIM)
add_custom_target(pkgconfigs ALL DEPENDS zzipwrap.pc)
endif()

# install ########################################################
set(outdir ${CMAKE_CURRENT_BINARY_DIR})

if(ZZIP_PKGCONFIG)
install(FILES ${outdir}/zzipwrap.pc 
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/pkgconfig" )
endif()

install(FILES ${libzzipwrap_HDRS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/zzip )
install(TARGETS libzzipwrap EXPORT zziplibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

if(ZZIP_LIBLATEST)
  if(BUILD_SHARED_LIBS)
    set(lib ${CMAKE_SHARED_LIBRARY_PREFIX})
    set(dll ${CMAKE_SHARED_LIBRARY_SUFFIX})
  else()
    set(lib ${CMAKE_STATIC_LIBRARY_PREFIX})
    set(dll ${CMAKE_STATIC_LIBRARY_SUFFIX})
  endif()
    set(libdir ${CMAKE_INSTALL_FULL_LIBDIR})
    get_target_property(libname libzzipwrap OUTPUT_NAME)
    get_target_property(librelease libzzipwrap RELEASE_POSTFIX)
    add_custom_target(libzzipwrap_latest ALL
        COMMAND ${CMAKE_COMMAND} -E create_symlink $<TARGET_FILE_NAME:libzzipwrap> ${lib}${libname}${dll}
        )
    install(FILES
        ${outdir}/${lib}${libname}${dll}
        DESTINATION ${CMAKE_INSTALL_LIBDIR})
endif()

# messages #######################################################

message(STATUS "lib zzipwrap symlinks as by libtool: ${ZZIP_LIBTOOL}")
message(STATUS "installing zzipwrap pkgconfig files: ${ZZIP_PKGCONFIG}")
