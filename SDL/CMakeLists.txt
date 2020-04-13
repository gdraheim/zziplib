cmake_minimum_required (VERSION 3.1)
project(zzipsdl VERSION "0.13.69" LANGUAGES C)

if(NOT CMAKE_BUILD_TYPE) 
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

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
pkg_search_module ( SDL sdl2)

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
target_link_libraries(zzcatsdl libzzip "${SDL_LIBRARIES}" ZLIB::ZLIB)
target_include_directories(zzcatsdl PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}" "${SDL_INCLUDE_DIRS}")
endif()

# install ########################################################
install(FILES ${ZZIPSDL_SRCS} ${ZZIPSDL_HDRS}
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/SDL_rwops_zzip)
