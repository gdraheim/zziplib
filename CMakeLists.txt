cmake_minimum_required (VERSION 3.1)
project(zziplib C)

# generate _config.h
include ( CheckIncludeFiles )
include ( CheckFunctionExists )
include ( CheckSymbolExists )
include ( CheckTypeSize )
include ( TestBigEndian )

check_include_files ( byteswap.h ZZIP_HAVE_BYTESWAP_H )
check_include_files ( direct.h ZZIP_HAVE_DIRECT_H )

if(NOT ANDROID)
    check_include_files ( dirent.h ZZIP_HAVE_DIRENT_H )
endif()

check_include_files ( dlfcn.h ZZIP_HAVE_DLFCN_H )
check_include_files ( fnmatch.h ZZIP_HAVE_FNMATCH_H )
check_include_files ( inttypes.h ZZIP_HAVE_INTTYPES_H )
check_include_files ( io.h ZZIP_HAVE_IO_H )
check_include_files ( memory.h ZZIP_HAVE_MEMORY_H )
check_include_files ( ndir.h ZZIP_HAVE_NDIR_H )
check_include_files ( stdint.h ZZIP_HAVE_STDINT_H )
check_include_files ( stdlib.h ZZIP_HAVE_STDLIB_H )
check_function_exists ( strcasecmp ZZIP_HAVE_STRCASECMP )
check_include_files ( strings.h ZZIP_HAVE_STRINGS_H )
check_include_files ( string.h ZZIP_HAVE_STRING_H )
check_function_exists ( strndup ZZIP_HAVE_STRNDUP )
check_include_files ( "sys/dir.h" ZZIP_HAVE_SYS_DIR_H )
check_include_files ( "sys/int_types.h" ZZIP_HAVE_SYS_INT_TYPES_H )
check_include_files ( "sys/mman.h" ZZIP_HAVE_SYS_MMAN_H )
check_include_files ( "sys/ndir.h" ZZIP_HAVE_SYS_NDIR_H )
check_include_files ( "sys/param.h" ZZIP_HAVE_SYS_PARAM_H )
check_include_files ( "sys/stat.h" ZZIP_HAVE_SYS_STAT_H )
check_include_files ( "sys/types.h" ZZIP_HAVE_SYS_TYPES_H )
check_include_files ( unistd.h ZZIP_HAVE_UNISTD_H )
check_include_files ( winbase.h ZZIP_HAVE_WINBASE_H )
check_include_files ( windows.h ZZIP_HAVE_WINDOWS_H )
check_include_files ( winnt.h ZZIP_HAVE_WINNT_H )
set ( ZZIP_HAVE_ZLIB_H 1 )

check_type_size ( int ZZIP_SIZEOF_INT )
check_type_size ( long ZZIP_SIZEOF_LONG )
check_type_size ( short ZZIP_SIZEOF_SHORT )
check_include_files ( "stdlib.h;stdarg.h;string.h;float.h" ZZIP_STDC_HEADERS )
test_big_endian ( ZZIP_WORDS_BIGENDIAN )

configure_file ( ${CMAKE_CURRENT_SOURCE_DIR}/_config.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/zzip/_config.h )

# Zlib library needed
find_package ( ZLIB REQUIRED )

if(UNIX)
    add_definitions(
        -Wpointer-arith
        -Wsign-compare
        -Wmissing-declarations
        -Wdeclaration-after-statement
        -Werror-implicit-function-declaration
        -Wstrict-aliasing
        -Warray-bounds
    )
endif()

# libzlib library
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_definitions ( -DHAVE_CONFIG_H )
set(ZZIPLIB_SRCS 
    zzip/dir.c
    zzip/err.c 
    zzip/file.c 
    zzip/info.c 
    zzip/plugin.c 
    zzip/stat.c
    zzip/write.c 
    zzip/zip.c 
    zzip/fetch.c)

set(ZZIPLIB_HDRS
    zzip/zzip.h
    zzip/types.h
    zzip/conf.h 
    zzip/_msvc.h 
    zzip/plugin.h 
    zzip/fetch.h
    ${CMAKE_CURRENT_BINARY_DIR}/zzip/_config.h)

add_library(zzip ${ZZIPLIB_SRCS} )
target_link_libraries(zzip ZLIB::ZLIB )
target_include_directories (zzip PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})

if(NOT MSVC) # FIXME: syntax error
    add_library(zzipmmapped zzip/mmapped.c zzip/memdisk.c zzip/fetch.c )
    target_link_libraries(zzipmmapped ZLIB::ZLIB )
    target_include_directories (zzipmmapped PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})
endif()

add_library(zzipfseeko zzip/fseeko.c zzip/fetch.c )
target_link_libraries(zzipfseeko ZLIB::ZLIB )
target_include_directories (zzipfseeko PRIVATE ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})

# install
install(FILES ${ZZIPLIB_HDRS} DESTINATION include/zzip )
install(TARGETS zzip 
    LIBRARY DESTINATION lib 
    ARCHIVE DESTINATION lib)
