#! /usr/bin/gmake -f

# the 'all' target is included from the 'configure'd Makefile

default:
	@ test -f Makefile || test -d build || (set -x ; mkdir build ; cd build && sh ../configure --prefix=$$HOME)
	@ test -f Makefile || test ! -f build/Makefile || (set -x ; cd build && $(MAKE) all)
	@ test -f Makefile || test ! -f build/Makefile || echo 'DONE (cd build && make all) - please run (cd build && make check) now'
	@ test ! -f Makefile || test -f build/Makefile || $(MAKE) all
	@ test ! -f Makefile || test -f build/Makefile || echo 'DONE make all - please run make check (before make install)'

.PHONY: build-am build-cm
build-am: ; mkdir build-am; cd build-am && sh ../configure --prefix=$$HOME/local --enable-sdl
build-cm: ; mkdir build-cm; cd build-cm && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$$HOME/local
build-nj: ; mkdir build-nj; cd build-nj && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$$HOME/local -GNinja
build-nm: ; mkdir build-nj; cd build-nj && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$$HOME/local -GNmake
am autom: ; rm -rf build-am; $(MAKE) build-am && cd build-am && $(MAKE) all
cm cmake: ; rm -rf build-cm; $(MAKE) build-cm && cd build-cm && $(MAKE) all
nj ninja: ; rm -rf build-nj; $(MAKE) build-nj && cd build-nj && ninja
cm-install: ; cd build-cm && $(MAKE) install

build-cm2: ; mkdir build-cm2; cd build-cm2 && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$$HOME/local -DZZIP_MANPAGES=OFF -DZZIP_INSTALL_BINS=OFF -DZZIP_TESTCVE=OFF
cm2: ; rm -rf build-cm2; $(MAKE) build-cm2 && cd build-cm2 && $(MAKE) all
cm2-install: ; cd build-cm2 && $(MAKE) install
cm2-checks: ; cd build-cm2 && $(MAKE) checks VERBOSE=1
cm2-check: ; cd build-cm2 && $(MAKE) check VERBOSE=1
un uninstall: ; rm -rf $$HOME/local

new: ; rm -rf build; $(MAKE) default

auto:
	aclocal -I m4 && autoconf -I m4 && autoheader && automake

boottrap:
	rm -rf .deps .libs
	rm -f config.guess config.sub stamp-h.in
	rm -f install-sh ltconfig ltmain.sh depcomp mkinstalldirs
	rm -f config.h config.h.in config.log config.cache configure
	rm -f aclocal.m4 Makefile Makefile.in
	aclocal 
	autoconf 
	autoheader 
	automake -a -c 

-include Makefile

test_%: ; python3 testbuilds.py $@ -vv
tests:  ; python3 testbuilds.py -vv

version:
	oldv=`sed -e '/zziplib.VERSION/!d' -e 's:.*zziplib.VERSION."::' -e 's:".*::' CMakeLists.txt` \
	; oldr=`echo $$oldv | sed -e 's:.*[.]::'` ; newr=`expr $$oldr + 1` \
	; newv=`echo $$oldv | sed -e "s:[.]$$oldr\$$:.$$newr:"` \
	; echo "$$oldv -> $$newv" \
	; sed -i -e "s:$$oldv:$$newv:" zziplib.spec testbuilds.py \
	; sed -i -e "s:$$oldv:$$newv:" */CMakeLists.txt \
	; sed -i -e "s:$$oldv:$$newv:" CMakeLists.txt \
	; git diff -U0
