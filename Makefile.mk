
auto:
	aclocal && autoconf && autoheader && automake

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

rpm: dist-bzip $(PACKAGE).spec
	rpmbuild -ta $(PACKAGE)-$(VERSION).tar.bz2

dist-bzip : dist-bzip2
	$(MAKE) dist-bzip-done
dist-bzip-done dist-done :
	cp */$(PACKAGE)-$(VERSION).tar.bz2 .

configsub :
	cp ../savannah.config/config.guess uses/config.guess
	cp ../savannah.config/config.sub   uses/config.sub
cf:
	scp $(PACKAGE)-$(VERSION).tar.bz2 cf-shell.sf.net:
