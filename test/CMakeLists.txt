cmake_minimum_required (VERSION 3.1)
project(zziptest VERSION "0.13.71" LANGUAGES C)

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
find_package ( PythonInterp 3.5 REQUIRED )
find_package ( UnixCommands REQUIRED ) # bash cp mv rm gzip tar
find_program ( MKZIP zip)

set(EXEEXT ${CMAKE_EXECUTABLE_SUFFIX})
set(README ${CMAKE_SOURCE_DIR}/README)
set(PY ${PYTHON_EXECUTABLE})
set(srcdir ${CMAKE_CURRENT_SOURCE_DIR})
set(topdir ${CMAKE_SOURCE_DIR})

# targets ########################################################
add_executable(zzipself    zzipself.c)
add_executable(zzipsetstub zzipsetstub.c)

target_link_libraries(zzipself     libzzip        ZLIB::ZLIB)
target_link_libraries(zzipsetstub  libzzip        ZLIB::ZLIB)

target_include_directories(zzipself     PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
target_include_directories(zzipsetstub  PRIVATE "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")

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

set(zip_CVE_2017_5977 "00153-zziplib-invalidread-zzip_mem_entry_extra_block")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5977}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5977}"
  EXPECTED_HASH SHA256=95b7f912709fd3e6f252dac1bf0040a029fea7564820bd30021eae9fb7be1c9b
)
set(zip_CVE_2017_5978 "00156-zziplib-oobread-zzip_mem_entry_new")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5978}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5978}"
  EXPECTED_HASH SHA256=abba6f78a6baacb07ffb87c4550fe9ba674be974f8fd9334b97cea9bc5fe36b1
)
set(zip_CVE_2017_5979 "00157-zziplib-nullptr-prescan_entry")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5979}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5979}"
  EXPECTED_HASH SHA256=2f25db0083e15a5b73c954a5abf36cf7614c7ce34a2c52e7b2e9d69da6b37770
)
set(zip_CVE_2017_5974 "00150-zziplib-heapoverflow-__zzip_get32")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5974}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5974}"
  EXPECTED_HASH SHA256=5139e7d6e17458c03a5b6bf43496c6e723233bdda1bb1f8edf2da3c1e77be35e
)
set(zip_CVE_2017_5975 "00151-zziplib-heapoverflow-__zzip_get64")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5975}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5975}"
  EXPECTED_HASH SHA256=f11c6adb4bcbe69d558b49dbd48894eeaaf5ad3520b0208a473c3d982410bde9
)
set(zip_CVE_2017_5976 "00152-zziplib-heapoverflow-zzip_mem_entry_extra_block")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5976}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5976}"
  EXPECTED_HASH SHA256=494bc7543a6dada1f422c4e65656797824865c55d1e20c36e599ca07b21066f2
)
set(zip_CVE_2017_5980 "00154-zziplib-nullptr-zzip_mem_entry_new")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5980}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5980}"
  EXPECTED_HASH SHA256=ba8ec9ffa29709ad05afb4b03daa893d634940acb37937fc4918492c348b35a0
)
set(zip_CVE_2017_5981 "00161-zziplib-assertionfailure-seeko_C")
file(DOWNLOAD
  "https://github.com/asarubbo/poc/raw/2d8ce927e0becebcc29f9bd8bee74be0d3ff2d7a/${zip_CVE_2017_5981}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2017_5981}"
  EXPECTED_HASH SHA256=64224bb1de40421f7ffed28a9bac7407c7a386ec8a677a1bb4fd1b7096520f7b
)
set(zip_CVE_2018_10 "zziplib_0-13-67_zzdir_invalid-memory-access_main.zip")
file(DOWNLOAD
  "https://github.com/ProbeFuzzer/poc/raw/3d7570e5111439f41766107ea77f6285a505bd62/zziplib/${zip_CVE_2018_10}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_10}"
  EXPECTED_HASH SHA256=cf0349d9a80e00f6897c5a78e1d7dbe5211841d771cb6ef5ae132476a2a75e22
)
set(zip_CVE_2018_11 "zziplib_0-13-67_unzzip_infinite-loop_unzzip_cat_file.zip")
file(DOWNLOAD
  "https://github.com/ProbeFuzzer/poc/raw/3d7570e5111439f41766107ea77f6285a505bd62/zziplib/${zip_CVE_2018_11}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_11}"
  EXPECTED_HASH SHA256=73cf63c07e323d355ad2cabd637040c63568a05f067e8b60d8bd0b6f7a5eea81
)
set(zip_CVE_2018_12 "zziplib_0-13-67_unzip-mem_buffer-access-with-incorrect-length-value_zzip_disk_fread.zip")
file(DOWNLOAD
  "https://github.com/ProbeFuzzer/poc/raw/3d7570e5111439f41766107ea77f6285a505bd62/zziplib/${zip_CVE_2018_12}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_12}"
  EXPECTED_HASH SHA256=acd6eb324221edec377e2fcea49e6700306d9608ff650c3a1419f35225ed7eb6
)
set(zip_CVE_2018_14 "zziplib_0-13-67_zzdir_memory-alignment-errors___zzip_fetch_disk_trailer.zip")
file(DOWNLOAD
  "https://github.com/ProbeFuzzer/poc/raw/3d7570e5111439f41766107ea77f6285a505bd62/zziplib/${zip_CVE_2018_14}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_14}"
  EXPECTED_HASH SHA256=51d80a73a29748502bd4fb5b5a45a38be6885618b942f0536f5da564328f0937
)
set(zip_CVE_2018_15 "zziplib_0-13-67_unzip-mem_memory-alignment-errors_zzip_disk_findfirst.zip")
file(DOWNLOAD
  "https://github.com/ProbeFuzzer/poc/raw/3d7570e5111439f41766107ea77f6285a505bd62/zziplib/${zip_CVE_2018_15}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_15}"
  EXPECTED_HASH SHA256=acd6eb324221edec377e2fcea49e6700306d9608ff650c3a1419f35225ed7eb6
)
set(zip_CVE_2018_16 "zziplib_0-13-67_unzzip_memory-aligment-errors___zzip_fetch_disk_trailer.zip")
file(DOWNLOAD
  "https://github.com/ProbeFuzzer/poc/raw/3d7570e5111439f41766107ea77f6285a505bd62/zziplib/${zip_CVE_2018_16}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_16}"
  EXPECTED_HASH SHA256=a3355d4b7aad1307647fbfab6d56c4e67222cc8358e0eadd136fd3324adfe02d
)
set(zip_CVE_2018_17 "zziplib_0-13-67_unzip-mem_memory-alignment-errors_zzip_disk_findfirst_64.zip")
file(DOWNLOAD
  "https://github.com/ProbeFuzzer/poc/raw/3d7570e5111439f41766107ea77f6285a505bd62/zziplib/${zip_CVE_2018_17}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_17}"
  EXPECTED_HASH SHA256=14acb740309b2980956b0843ec6dbedc1e51872c627e64ba7e8247eccc9bca5c
)
set(zip_CVE_2018_42 "c006-unknown-add-main")
file(DOWNLOAD
  "https://github.com/fantasy7082/image_test/raw/52e75d833034b38dbfb13512f894ed2dc801fcf0/${zip_CVE_2018_42}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_42}"
  EXPECTED_HASH SHA256=3bf780d9d42f999fec010b6abf6737daf21da273ee6ed8ba5f95abc1fee753bf
)
set(zip_CVE_2018_43 "c008-main-unknown-de")
file(DOWNLOAD
  "https://github.com/fantasy7082/image_test/raw/52e75d833034b38dbfb13512f894ed2dc801fcf0/${zip_CVE_2018_43}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_43}"
  EXPECTED_HASH SHA256=5ef84ff94ecf56e04e5a7e88eeea6da4108c4482c705c3ea4d235ecd0c9e3da5
)
set(zip_CVE_2018_27 "poc_bypass_fix2.zip")
file(DOWNLOAD
  "https://github.com/ret2libc/---provided-by-email---/${zip_CVE_2018_27}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_27}"
  EXPECTED_HASH SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
)
# CVE-2018-7726
set(zip_CVE_2018_41 "c005-bus-zzip_parse_root_directory") # CVE-2018-7726.
file(DOWNLOAD
  "https://github.com/fantasy7082/image_test/raw/52e75d833034b38dbfb13512f894ed2dc801fcf0/${zip_CVE_2018_41}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_41}"
  EXPECTED_HASH SHA256=5dc676ba9e8a06b2668d566e59bc5f88ff60aa79232b62c3db3a5da6eebce154
)
set(zip_CVE_2018_39 "003-unknow-def-zip")
file(DOWNLOAD
  "https://github.com/fantasy7082/image_test/raw/52e75d833034b38dbfb13512f894ed2dc801fcf0/${zip_CVE_2018_39}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_39}"
  EXPECTED_HASH SHA256=f66d16be2a5a0e05e125c2ab85a56ba54107d1ca99231f9b4e7c2b5b1c6b15dd
)
set(zip_CVE_2018_40 "002-mem-leaks-zip")
file(DOWNLOAD
  "https://github.com/fantasy7082/image_test/raw/52e75d833034b38dbfb13512f894ed2dc801fcf0/${zip_CVE_2018_40}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_40}"
  EXPECTED_HASH SHA256=064b27bd8af1d1a4b98972fb7f9700a3360dcfbafdc101b2865c772acf04e438
)
set(zip_CVE_2018_17828 "evil.zip")
file(DOWNLOAD
  "https://github.com/gdraheim/zziplib/files/2415382/${zip_CVE_2018_17828}"
  "${CMAKE_CURRENT_BINARY_DIR}/${zip_CVE_2018_17828}"
  EXPECTED_HASH SHA256=350832725999fdaee4422a56397b908ae629c37e2ffe6e427af8ee65718ae4e7
)

add_custom_target(tests
   COMMAND ${PY} ${srcdir}/zziptests.py --exeext=${EXEEXT} --topsrcdir=${topdir} --builddir=${CMAKE_CURRENT_BINARY_DIR} -v ${TESTFLAGS}
   DEPENDS ../bins/zzcat ../bins/zzdir ../bins/zziptest ../bins/zzxorcat ../bins/zzxorcopy)
add_custom_command(OUTPUT ../bins/zzcat COMMMAND cd ../bins && $(MAKE) zzcat)
add_custom_command(OUTPUT ../bins/zzdir COMMMAND cd ../bins && $(MAKE) zzdir)
add_custom_command(OUTPUT ../bins/zziptest COMMMAND cd ../bins && $(MAKE) zziptest)
add_custom_command(OUTPUT ../bins/zzxorcat COMMMAND cd ../bins && $(MAKE) zzxorcat)
add_custom_command(OUTPUT ../bins/zzxorcopy COMMMAND cd ../bins && $(MAKE) zzxorcopy)

add_custom_command(OUTPUT test0.zip
    COMMAND ${BASH} -c "test -d tmp || mkdir tmp"
    COMMAND ${CP} ${README} tmp/README
    COMMAND ${BASH} -c "cd tmp && ${MKZIP} ../test0.zip README"
    COMMAND ${CP} test0.zip test.zip
    BYPRODUCTS test.zip
    VERBATIM)
add_custom_target(testzips ALL DEPENDS test0.zip)

add_custom_target(checks
    COMMAND ${BASH} -c "../bins/zzcat test/README > test.out"
    COMMAND ${BASH} -c "if diff test.out ${README} >/dev/null \
       ; then rm test.out ; echo check OK; true \
       ; else rm test.out ; echo check FAIL ; false; fi"
    DEPENDS ../bins/zzcat test0.zip
    VERBATIM)
add_custom_target(check DEPENDS checks tests)

# install ########################################################
# - nothing -
