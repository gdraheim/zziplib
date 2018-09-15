PREFIX ?= /usr/local
LOCAL ?= $(PWD)/build/root

SHARED = -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=OFF
STATIC = -DBUILD_SHARED_LIBS=OFF -DBUILD_STATIC_LIBS=ON

all depend: 
	test -d build || $(MAKE) config
	cd $@
clean edit_cache rebuild_cache help:
	test ! -d build || cd build && $(MAKE) $@
install install/strip install/local list_install_components:
	cd build && $(MAKE) $@ VERBOSE=1
libzzip libzzipmmapped libzzipfseeko libzzipwrap zzipwrap:
	cd build && $(MAKE) $@ VERBOSE=1
zzip unzzip unzzip-mix unzzip-mem unzzip-big zzdir zzcat zzcatsdl zzxorcat zzxordir zzobfuscated:
	cd build && $(MAKE) $@ VERBOSE=1
sfx zzipself zzipsetstub doc htm man htmpages manpages site dbk pdf:
	cd build && $(MAKE) $@ VERBOSE=1
tests checks check:
	cd build && $(MAKE) $@ VERBOSE=1

builds: config build local
static: conf build local

st: ; $(MAKE) distclean && $(MAKE) static
it: ; $(MAKE) distclean && $(MAKE) builds

.PHONY: build
build:
	cd build && $(MAKE) all VERBOSE=1

config:
	test -d build || mkdir build
	cd build && cmake $(SHARED) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) ..

conf:
	test -d build || mkdir build
	cd build && cmake $(STATIC) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) ..

local:
	cd build && $(MAKE) install DESTDIR=$(LOCAL)
distclean:
	rm -rf build
	rm -rf CMakeFiles
