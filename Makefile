all: config build

.PHONY: build

config:
	test -d build || mkdir build
	cd build && cmake ..

build:
	cd build && $(MAKE) VERBOSE=1

clean:
	cd build && $(MAKE) clean
distclean:
	rm -rf build
	rm -rf CMakeFiles

