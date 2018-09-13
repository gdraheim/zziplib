PREFIX ?= /usr/local
LOCAL ?= $(PWD)/build/root

all: config build local

it: ; $(MAKE) distclean && $(MAKE) all

.PHONY: build

config:
	test -d build || mkdir build
	cd build && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX)

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
