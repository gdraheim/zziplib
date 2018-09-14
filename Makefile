PREFIX ?= /usr/local
LOCAL ?= $(PWD)/build/root

SHARED = -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=OFF
STATIC = -DBUILD_SHARED_LIBS=OFF -DBUILD_STATIC_LIBS=ON

all: config build local
static: conf build local

st: ; $(MAKE) distclean && $(MAKE) static
it: ; $(MAKE) distclean && $(MAKE) all

.PHONY: build

config:
	test -d build || mkdir build
	cd build && cmake $(SHARED) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) ..

conf:
	test -d build || mkdir build
	cd build && cmake $(STATIC) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) ..

build:
	cd build && $(MAKE) VERBOSE=1
local:
	cd build && $(MAKE) install DESTDIR=$(LOCAL)
install:
	cd build && $(MAKE) install

clean:
	cd build && $(MAKE) clean
distclean:
	rm -rf build
	rm -rf CMakeFiles
