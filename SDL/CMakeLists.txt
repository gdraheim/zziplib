cmake_minimum_required (VERSION 3.1)
project(zzipsdl C)
set(VERSION "0.13.69")

string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\1" RELNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\2" VERNUM ${VERSION})
string(REGEX REPLACE "([^.]+)[.]([^.]+)[.]([^.]+)" "\\3" FIXNUM ${VERSION})
MESSAGE(STATUS "VERSION ${VERSION} -> RELNUM ${RELNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> VERNUM ${VERNUM}")
MESSAGE(STATUS "VERSION ${VERSION} -> FIXNUM ${FIXNUM}")

include ( GNUInstallDirs )
include ( FindPkgConfig )

option(BUILD_SHARED_LIBS "Build a shared library" ON)
option(BUILD_STATIC_LIBS "Build the static library" OFF)
option(BUILD_TESTS "Build test programs" OFF)
option(MSVC_STATIC_RUNTIME "Build with static runtime libs (/MT)" ON)

# Zlib library needed
find_package ( ZLIB REQUIRED )
pkg_search_module ( ZZIP zzip )
pkg_search_module ( SDL sdl2)

# use the uninstalled zzip here (don't know to to tell pkg_search_module)
set(lib ${CMAKE_SHARED_LIBRARY_PREFIX})
set(dll ${CMAKE_SHARED_LIBRARY_SUFFIX})
get_target_property(libname zzip OUTPUT_NAME)
set(ZZIP_INCLUDE_DIR ${CMAKE_SOURCE_DIR})
set(ZZIP_LIBRARY ${CMAKE_BINARY_DIR}/${lib}${libname}${dll})

# targets ########################################################
set(ZZIPSDL_SRCS 
    SDL_rwops_zzip.c)

set(ZZIPSDL_HDRS
    SDL_rwops_zzip.h)

set(ZZCATSDL_SRCS
    ${ZZIPSDL_SRCS}
    SDL_rwops_zzcat.c)

if(SDL_FOUND)
add_executable(zzcatsdl ${ZZCATSDL_SRCS} )
target_link_libraries(zzcatsdl "${ZZIP_LIBRARY}" "${SDL_LIBRARIES}" ZLIB::ZLIB)
target_include_directories(zzcatsdl PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}" "${SDL_INCLUDE_DIRS}")
endif()

# install ########################################################
install(FILES ${ZZIPSDL_SRCS} ${ZZIPSDL_HDRS}
        DESTINATION include/SDL_rwops_zzip)
