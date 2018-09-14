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

set(MKZIP zip)
set(EXEEXT ${CMAKE_EXECUTABLE_SUFFIX})
set(README ${CMAKE_SOURCE_DIR}/README)

# targets ########################################################
set(doc_FILES = README.MSVC6 README.SDL COPYING.MPL COPYING.LIB COPYING.ZLIB
            zziplib.html zzipmmapped.html zzipfseeko.html)
set(htm_FILES = zzip-index.htm zzip-zip.htm zzip-file.htm zzip-sdl-rwops.htm
            zzip-extio.htm zzip-xor.htm zzip-crypt.htm zzip-cryptoid.htm
            zzip-api.htm  zzip-basics.htm zzip-extras.htm zzip-parse.htm
            64on32.htm future.htm fseeko.htm mmapped.htm memdisk.htm
            configs.htm sfx-make.htm   developer.htm download.htm
            history.htm referentials.htm  faq.htm copying.htm notes.htm
            functions.htm zip-php.htm)
set(zzipdoc_FILES makedocs.py          zzipdoc/__init__.py
    zzipdoc/commentmarkup.py          zzipdoc/match.py
    zzipdoc/dbk2htm.py                zzipdoc/htm2dbk.py
    zzipdoc/functionheader.py         zzipdoc/options.py
    zzipdoc/functionlisthtmlpage.py   zzipdoc/textfileheader.py
    zzipdoc/functionlistreference.py  zzipdoc/textfile.py
    zzipdoc/functionprototype.py      zzipdoc/htmldocument.py
                                      zzipdoc/docbookdocument.py)

set(topdir ${CMAKE_SOURCE_DIR})
set(srcdir ${CMAKE_CURRENT_SOURCE_DIR})
set(docinfo --package="zziplib" --version=${VERSION})
add_custom_command(OUTPUT zziplib.xml
    COMMAND python ${srcdir}/makedocs.py ${topdir}/zzip/*.c ${docinfo} --onlymainheader=zzip/lib.h --output=zziplib
    COMMAND mv zziplib.docbook zziplib.xml
    DEPENDS libzzip
    BYPRODUCTS zziplib.html)
add_custom_command(OUTPUT zzipmmapped.xml
    COMMAND python ${srcdir}/makedocs.py ${topdir}/zzip/*.c ${docinfo} --onlymainheader=zzip/mmapped.h --output=zzipmmapped
    COMMAND mv zzipmmapped.docbook zzipmmapped.xml
    DEPENDS libzzipmmapped
    BYPRODUCTS zzipmmapped.html)
add_custom_command(OUTPUT zzipfseeko.xml
    COMMAND python ${srcdir}/makedocs.py ${topdir}/zzip/*.c ${docinfo} --onlymainheader=zzip/fseeko.h --output=zzipfseeko
    COMMAND mv zzipfseeko.docbook zzipfseeko.xml
    DEPENDS libzzipfseeko
    BYPRODUCTS zzipfsseko.html)
add_custom_command(OUTPUT manpages.tar
    COMMAND rm -rf man3
    COMMAND mkdir man3
    COMMAND python ${srcdir}/dbk2man.py -o man3 man zziplib.xml
    COMMAND python ${srcdir}/dbk2man.py -o man3 man zzipmmapped.xml
    COMMAND python ${srcdir}/dbk2man.py -o man3 man zzipfseeko.xml
    COMMAND bash -c "test -d man3/man3 && mv man3 man3_; test -d man3_/man3 && mv man3_/man3 .; rm -rf man3_"
    COMMAND bash -c "chmod 664 man3/*.3"
    COMMAND tar cf manpages.tar man3
    DEPENDS zziplib.xml zzipmmapped.xml zzipfseeko.xml
    VERBATIM)

add_custom_target(doc ALL DEPENDS manpages.tar)

# install ########################################################
set(mandir ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_MANDIR})
install(CODE "execute_process(COMMAND bash -c \"set -e
   mkdir -vp $DESTDIR/${mandir} || ls -ld $DESTDIR/${mandir}
   cd $DESTDIR/${mandir} && tar xf ${CMAKE_CURRENT_BINARY_DIR}/manpages.tar
   \")")

