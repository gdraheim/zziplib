#! /usr/bin/gmake -f

# the 'all' target is included from the 'configure'd Makefile

default:
	@ test -f Makefile || test -d build || (set -x ; mkdir build ; cd build && sh ../configure --prefix=$$HOME)
	@ test -f Makefile || test ! -f build/Makefile || (set -x ; cd build && $(MAKE) all)
	@ test -f Makefile || test ! -f build/Makefile || echo 'DONE (cd build && make all) - please run (cd build && make check) now'
	@ test ! -f Makefile || test -f build/Makefile || $(MAKE) all
	@ test ! -f Makefile || test -f build/Makefile || echo 'DONE make all - please run make check (before make install)'

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

