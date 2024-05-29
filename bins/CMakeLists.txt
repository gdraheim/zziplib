cmake_minimum_required (VERSION 3.1)
project(zzipbins VERSION "0.13.76" LANGUAGES C)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeScripts")

if(NOT CMAKE_BUILD_TYPE) 
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

include ( GNUInstallDirs )
include ( FindPkgConfig )

# options ########################################################
option(BUILD_SHARED_LIBS "Build a shared library" ON)
option(BUILD_TESTS "Build test programs" OFF)
option(MSVC_STATIC_RUNTIME "Build with static runtime libs (/MT)" ON)

option(ZZIP_INSTALL_BINS "Install the bins/ exanple programs" ON)
option(ZZIP_INSTALL_ACLOCAL "Install zziplib.m4 aclocal helper" ON)
option(COVERAGE "Code coverage" OFF)

if(COVERAGE)
include ( CodeCoverage )
endif(COVERAGE)

if(FORTIFY)
   add_definitions(
     -U_FORTIFY_SOURCE 
     -fsanitize=address 
     -g
   )
   add_link_options(
     -fsanitize=address
   )
   set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -DDEBUG")
endif()

if(COVERAGE)
append_coverage_compiler_flags()
endif()

# Zlib library needed
find_package ( ZLIB REQUIRED )

## linking while compiling zziplib itself (in ../zzip)
set(zziplib_libzzip libzzip)
set(zziplib_libzzipfseeko libzzipfseeko)
set(zziplib_libzzipmmapped libzzipmmapped)
## linking when using examples elsewhere
# find_package ( zziplib REQUIRED)
# set(zziplib_libzzip zziplib::libzzip) # find_pack
# set(zziplib_libzzipfseeko zziplib::libzzipfseeko) # find_pack
# set(zziplib_libzzipmmapped zziplib::libzzipmmapped) # find_pack

# targets ########################################################
add_executable(zzcat      zzcat.c)
add_executable(zzdir      zzdir.c)
add_executable(zzxorcat   zzxorcat.c)
add_executable(zzxordir   zzxordir.c)
add_executable(zzxorcopy   zzxorcopy.c)
add_executable(zzobfuscated zzobfuscated.c)
add_executable(zziptest   zziptest.c)
add_executable(unzzip     unzzip.c unzzipcat-zip.c unzzipdir-zip.c)
add_executable(unzzip-mix unzzip.c unzzipcat-mix.c unzzipdir-mix.c)
add_executable(unzzip-big unzzip.c unzzipcat-big.c unzzipdir-big.c)
add_executable(unzzip-mem unzzip.c unzzipcat-mem.c unzzipdir-mem.c)
add_executable(unzip-mem  unzip-mem.c)
if(NOT WIN32)
add_executable(zzip       zzip.c zzipmake-zip.c)
endif()

target_link_libraries(zzcat        ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(zzdir        ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(zzxorcat     ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(zzxordir     ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(zzxorcopy    ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(zzobfuscated ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(zziptest     ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(unzzip       ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(unzzip-mix   ${zziplib_libzzip}        ZLIB::ZLIB)
target_link_libraries(unzzip-big   ${zziplib_libzzipfseeko}  ZLIB::ZLIB)
target_link_libraries(unzzip-mem   ${zziplib_libzzipmmapped} ZLIB::ZLIB)
target_link_libraries(unzip-mem    ${zziplib_libzzipmmapped} ZLIB::ZLIB)
if(NOT WIN32)
target_link_libraries(zzip         ${zziplib_libzzip}        ZLIB::ZLIB)
endif()

target_include_directories(zzcat        PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zzdir        PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zzxorcat     PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zzxordir     PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zzxorcopy    PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zzobfuscated PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zziptest     PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(unzzip       PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(unzzip-mix   PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(unzzip-big   PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(unzzip-mem   PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(unzip-mem    PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
if(NOT WIN32)
target_include_directories(zzip         PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
endif()

if(WIN32)
add_custom_target(bins DEPENDS zzcat zzdir zzxorcat zzxorcopy zzobfuscated zziptest unzzip unzzip-mix unzzip-big unzzip-mem unzip-mem)
else()
add_custom_target(bins DEPENDS zzcat zzdir zzxorcat zzxorcopy zzobfuscated zziptest unzzip unzzip-mix unzzip-big unzzip-mem unzip-mem zzip)
endif()

# install ########################################################
if(ZZIP_INSTALL_BINS)
install(TARGETS zzcat zzdir zzxorcat zzxordir zzxorcopy
                unzzip unzzip-mix unzzip-big unzzip-mem unzip-mem
        DESTINATION "${CMAKE_INSTALL_BINDIR}")
endif()

if(ZZIP_INSTALL_ACLOCAL)
install(FILES zziplib.m4
        DESTINATION "${CMAKE_INSTALL_DATADIR}/aclocal")
endif()
