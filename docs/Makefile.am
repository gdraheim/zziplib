AUTOMAKE_OPTIONS = 1.4 foreign
AUTOTOOL_VERSION=autoconf-2.52 automake-1.5 libtool-1.4.2

PYRUN = $(PYDEFS) @PYTHON@ $(PYFLAGS)
PLRUN = $(PLDEFS) @PERL@   $(PLFLAGS)
DELETE = echo deleting...

doc_FILES = README.MSVC6 README.SDL COPYING.MPL COPYING.LIB COPYING.ZLIB \
            zziplib.html zzipmmapped.html zzipfseeko.html
htm_FILES = zzip-index.htm zzip-zip.htm zzip-file.htm zzip-sdl-rwops.htm \
            zzip-extio.htm zzip-xor.htm zzip-crypt.htm zzip-cryptoid.htm \
            zzip-api.htm  zzip-basics.htm zzip-extras.htm zzip-parse.htm \
            64on32.htm future.htm fseeko.htm mmapped.htm memdisk.htm \
            configs.htm sfx-make.htm   developer.htm download.htm \
            history.htm referentials.htm  faq.htm copying.htm notes.htm \
            functions.htm zip-php.htm
htms_FILES = changes.htm
SDL = @top_srcdir@/SDL
SDL_RWOPS = $(SDL)/SDL_rwops_zzcat.c \
            $(SDL)/SDL_rwops_zzip.c $(SDL)/SDL_rwops_zzip.h
changelog = @top_srcdir@/ChangeLog

EXTRA_DIST = make-doc.py $(doc_FILES) $(htm_FILES) $(SDL_RWOPS) \
             make-doc.pl make-dbk.pl   mksite.sh mksite.pl body.htm \
             $(zzipdoc_FILES) sdocbook.css \
             zziplib-manpages.dbk zziplib-master.dbk \
             zziplib-manpages.ar 
CLEANFILES = *.pc *.omf
DISTCLEANFILES = zziplib.spec manpages.ar htmpages.ar *.html *.xml

zzipdoc_FILES = makedocs.py               zzipdoc/__init__.py \
	zzipdoc/commentmarkup.py          zzipdoc/match.py    \
	zzipdoc/dbk2htm.py                zzipdoc/htm2dbk.py  \
	zzipdoc/functionheader.py         zzipdoc/options.py  \
	zzipdoc/functionlisthtmlpage.py   zzipdoc/textfileheader.py \
	zzipdoc/functionlistreference.py  zzipdoc/textfile.py \
	zzipdoc/functionprototype.py      zzipdoc/htmldocument.py \
                                          zzipdoc/docbookdocument.py

html_FILES = $(htm_FILES:.htm=.html)       $(htms_FILES:.htm=.html) \
             $(htm_FILES:.htm=.print.html) $(htms_FILES:.htm=.print.html) \
             site.html site.print.html

all : all-am default
default : doc @MAINTAINER_MODE_FALSE@ mans
clean-doc clean-docs : clean-unpack
	- rm $(DISTCLEANFILES) 
	- rm $(MAINTAINERCLEANFILES)
install-data-local : @MAINTAINER_MODE_FALSE@ install-mans

# -------------------------------------------------------------------
zziplib.spec : @top_srcdir@/$(PACKAGE).spec
	@ $(LN_S) $? $@ # the two zzip-doc.* will grep thru zziplib.spec
doc  : $(doc_FILES) site.html
docs : doc manpages.ar htmpages.ar
# docu : docs
docu : 
	- rm zziplib2.html zzipmmapped.html zzipfseeko.html
	$(MAKE) manpages.ar htmpages.ar DELETE=exit

zziplib.html zziplib.xml : zziplib.spec $(srcdir)/Makefile.am \
                 $(srcdir)/zzipdoc/*.py \
                 $(srcdir)/makedocs.py @top_srcdir@/zzip/*.c
	$(PYRUN) $(srcdir)/makedocs.py @top_srcdir@/zzip/*.c $(zziplib) \
                   "--package=$(PACKAGE)" "--version=$(VERSION)" \
                   "--onlymainheader=zzip/lib.h" "--output=zziplib"
	test -s zziplib.docbook && mv zziplib.docbook zziplib.xml
zzipmmapped.html zzipmmapped.xml : zziplib.spec $(srcdir)/Makefile.am \
                 $(srcdir)/zzipdoc/*.py \
                 $(srcdir)/makedocs.py @top_srcdir@/zzip/*.c
	$(PYRUN) $(srcdir)/makedocs.py @top_srcdir@/zzip/*.c $(zziplib) \
                   "--package=$(PACKAGE)" "--version=$(VERSION)" \
                   "--onlymainheader=zzip/mmapped.h" "--output=zzipmmapped"
	test -s zzipmmapped.docbook && mv zzipmmapped.docbook zzipmmapped.xml
zzipfseeko.html zzipfseeko.xml : zziplib.spec $(srcdir)/Makefile.am \
                 $(srcdir)/zzipdoc/*.py \
                 $(srcdir)/makedocs.py @top_srcdir@/zzip/*.c
	$(PYRUN) $(srcdir)/makedocs.py @top_srcdir@/zzip/*.c $(zziplib) \
                   "--package=$(PACKAGE)" "--version=$(VERSION)" \
                   "--onlymainheader=zzip/fseeko.h" "--output=zzipfseeko"
	test -s zzipfseeko.docbook && mv zzipfseeko.docbook zzipfseeko.xml

omfdir=${datadir}/omf
pkgomfdir=${omfdir}/${PACKAGE}
SFNETDIR=/groups/z/zz/zziplib/htdocs
pkgdocdir=${mandir}/../doc/${PACKAGE}
bins = @top_srcdir@/bins
DOCEXAMPLES = $(bins)/zzdir.c $(bins)/zzcat.c \
	      $(bins)/zzobfuscated.c $(bins)/zziptest.c \
              $(bins)/zzxordir.c $(bins)/zzxorcat.c \
	      $(bins)/zzxorcopy.c        $(SDL_RWOPS)

install-docs: $(doc_FILES) $(man_FILES) site.html htmpages.ar
	$(mkinstalldirs) $(DESTDIR)$(pkgdocdir)
	$(INSTALL_DATA) $(html_FILES) $(DESTDIR)$(pkgdocdir)
	for i in $(doc_FILES) $(DOCEXAMPLES) $(changelog) $(srcdir)/README.* \
	; do $(INSTALL_DATA) `test -f $$i || echo $(srcdir)/`$$i \
	    $(DESTDIR)$(pkgdocdir) ; done
	cd $(DESTDIR)$(pkgdocdir) && ln -sf zzip-index.html index.html
	$(mkinstalldirs) $(DESTDIR)$(pkgdocdir)/man
	@ echo ar x htmpages.ar '>>>' $(DESTDIR)$(pkgdocdir)/man/ \
	; test -f htmpages.ar || cd "$srcdir" ; P=`pwd` \
	; cd $(DESTDIR)$(pkgdocdir)/man && ar x $$P/htmpages.ar

install-doc : install-docs $(PACKAGE)-doc.omf
	$(mkinstalldirs) $(DESTDIR)$(pkgomfdir)
	$(INSTALL_DATA) $(PACKAGE)-doc.omf $(DESTDIR)$(pkgomfdir)/
	- test ".$(DESTDIR)" != "." || scrollkeeper-update

install-sf:
	$(MAKE) install-docs DESTDIR=/tmp/zziplib-htdocs-$$USER/
	echo scp ... shell.sf.net:$(pkgdocdir)/ ; sleep 4
	scp -r /tmp/zziplib-htdocs-$$USER/$(pkgdocdir)/* \
               shell.sf.net:/home/$(SFNETDIR)/
	rm -r /tmp/zziplib-htdocs-$$USER/

# ------------------------------------------------------------ package manpages
mans : manpages
install-mans : install-man3

man3 man manpages : manpages.ar
html htm htmpages : htmpages.ar

zziplib-manpages.ar : manpages.ar
	test -s "$@" || test -s "$(srcdir)/$@"
manpages.ar : zziplib.xml zzipmmapped.xml zzipfseeko.xml
	: "unix man format of the manpages - goes to ../share/man/man3"
	@ if test "$(XMLTO)" != ":" \
	; then echo going to regenerate "$@" in subdir "'"man"'" \
	; echo 'test ! -d man3 || rm man3/* ; test -d man3 || mkdir man3' \
	;       test ! -d man3 || rm man3/* ; test -d man3 || mkdir man3  \
	; echo '$(XMLTO) -o man3 man zziplib.xml' \
	;       $(XMLTO) -o man3 man zziplib.xml  \
	; echo '$(XMLTO) -o man3 man zzipmmapped.xml' \
	;       $(XMLTO) -o man3 man zzipmmapped.xml  \
	; echo '$(XMLTO) -o man3 man zzipfseeko.xml' \
	;       $(XMLTO) -o man3 man zzipfseeko.xml  \
	; echo 'ar qc "$@" man3/*.3' \
	;       ar qc "$@" man3/*.3  \
	; echo '$(DELETE); rm man3/*.3 ; rmdir man3' \
	;       $(DELETE); rm man3/*.3 ; rmdir man3  \
	; fi ; true
	@ if test -s $@ \
	; then echo cp $@ zziplib-$@ "(saved)"; cp $@ zziplib-$@ \
	; else echo cp $(srcdir)/zziplib-$@ $@; cp $(srcdir)/zziplib-$@ $@ \
	; fi

zziplib-htmpages.ar : htmpages.ar
	test -s "$@" || test -s "$(srcdir)/$@"
htmpages.ar : zziplib.xml zzipmmapped.xml zzipfseeko.xml zziplib-manpages.dbk
	: "html format of the manpages - put into zziplib/htdocs/man/*"
	@ if test "$(XMLTO)" != ":" \
	; then echo going to regenerate "$@" in subdir "'"html"'" \
	; echo 'test ! -d html || rm /* ; test -d html || mkdir html' \
	;       test ! -d html || rm html/* ; test -d html || mkdir html  \
	; echo 'cp $(srcdir)/zziplib-manpages.dbk zziplib-manpages.xml' \
	;       cp $(srcdir)/zziplib-manpages.dbk zziplib-manpages.xml \
	; echo '$(XMLTO) -o html html zziplib-manpages.xml | tee written.lst' \
	;       $(XMLTO) -o html html zziplib-manpages.xml | tee written.lst \
	; echo 'ar qc $@ html/*.*' \
	;       ar qc $@ html/*.*  \
	; echo '$(DELETE); rm html/*.* ; rmdir html' \
	;       $(DELETE); rm html/*.* ; rmdir html  \
	; fi ; true
	@ if test -s $@ \
	; then echo cp $@ zziplib-$@ "(saved)"; cp $@ zziplib-$@ \
	; else echo cp $(srcdir)/zziplib-$@ $@; cp $(srcdir)/zziplib-$@ $@ \
	; fi

install-man3 : manpages.ar
	$(mkinstalldirs) $(DESTDIR)$(mandir)/man3
	P=`pwd` ; cd $(DESTDIR)$(mandir)/man3 \
        && ar x $$P/manpages.ar && chmod 664 *

unpack : manpages.ar htmpages.ar
	(rm -rf _htm && mkdir _htm && cd _htm && ar x ../htmpages.ar)
	(rm -rf _man && mkdir _man && cd _man && ar x ../manpages.ar)
clean-unpack : 
	rm -rf _htm
	rm -rf _man

# --------------------------------------------------------------- OMF handling
spec_file=$(top_srcdir)/$(PACKAGE).spec
DOCSERIES= 775fb73e-1874-11d7-93e9-e18cd7ea3c2e
FROMSPEC= $(spec_file) | head -1 | sed -e 's,<,\&lt;,g' -e 's,>,\&gt;,g'
DATESPEC= `date +%Y-%m-%d`

$(PACKAGE)-doc.omf : $(spec_file) Makefile
	: "OMF for the html documentation - a copy of zziplib.sf.net"
	echo '<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>' >$@
	echo '<omf><resource><creator> Guido Draheim </creator>' >>$@
	grep Packager $(FROMSPEC) | sed -e 's,Packager *: *, <maintainer>,' \
                                    -e '/<maintainer>/s,$$,</maintainer>,' >>$@
	grep Summary  $(FROMSPEC) | sed -e 's,Summary *: *, <title>,' \
		       -e '/<title>/s,$$,</title>,' >>$@
	echo ' <date>'$(DATESPEC)'</date>' >>$@
	echo ' <version identifier="$(VERSION)" date="'$(DATESPEC)'"/>' >>$@
	grep Group  $(FROMSPEC) | sed -e 's,Group *: *, <subject category=",' \
	                -e 's,/,|,g' -e '/<subject/s,$$," />,' >>$@
	echo ' <format mime="text/html"/>' >>$@
	pkgdocdir=`echo "$(pkgdocdir)" | sed -e "s|/[a-z][a-z]*/[.][.]/|/|"` \
	echo ' <identifier url="file:'"$$pkgdocdir"'/zzip-index.html"/>' >>$@
	echo ' <language code="C"/>' >>$@
	echo ' <relation seriesid="$(DOCSERIES)"/>' >>$@
	echo ' <rights type="GNU LGPL" holder="Guido Draheim"' >>$@
	pkgdocdir=`echo "$(pkgdocdir)" | sed -e "s|/[a-z][a-z]*/[.][.]/|/|"` \
	echo '         license="'"$$pkgdocdir"')/COPYING.LIB"/>' >>$@
	echo '</resource></omf>' >>$@

DOCBOOKDTD= -//OASIS/DTD Docbook V4.1.2//EN
MANSERIES= a302c642-1888-11d7-86f6-ba4b52ef847d
$(PACKAGE)-man.omf : $(PACKAGE)-doc.omf $(PACKAGE).xml
	: "OMF for functions reference - the docbook master of the manpages"
	sed -e 's,"text/html","text/xml" dtd="$(DOCBOOKDTD)",' \
	    -e 's,</title>, (Function Reference)</title>,' \
	    -e 's,/index.html,/xml/manpages.xml,' \
	    -e 's,$(DOCSERIES),$(MANSERIES),' $(PACKAGE)-doc.omf > $@
	test -s $@ || rm $@

omf : $(PACKAGE)-doc.omf $(PACKAGE)-man.omf 
install-omf : omf zziplib.xml zzipmmapped.xml zzipfseeko.xml
	: "not installed by default anymore - 'make install-doc' has one OMF"
	$(mkinstalldirs) $(DESTDIR)$(pkgomfdir)
	$(INSTALL_DATA) $(PACKAGE)-doc.omf $(DESTDIR)$(pkgomfdir)/
	$(mkinstalldirs) $(DESTDIR)$(pkgdocdir)
	$(INSTALL_DATA) $(srcdir)/zziplib-manpages.xml \
               $(DESTDIR)$(pkgdocdir)/xml/manpages.xml
	$(INSTALL_DATA)  zziplib.xml zzipmmapped.xml zzipfseeko.xml \
               $(DESTDIR)$(pkgdocdir)/xml/
	$(INSTALL_DATA) $(PACKAGE)-man.omf $(DESTDIR)$(pkgomfdir)/
	- test ".$(DESTDIR)" != "." || scrollkeeper-update -v

# ----------------------------------------------- mksite.sh for the main html
site.htm : body.htm
	cp $(srcdir)/body.htm site.htm
mksite_sh_args = --VERSION=$(VERSION) --xml --src-dir=$(srcdir) --print
site.html : body.htm site.htm mksite.sh $(htm_FILES) $(htms_FILES)
	cp $(srcdir)/body.htm site.htm
	perl $(srcdir)/mksite.pl $(mksite_sh_args) site.htm || \
	$(SHELL) $(srcdir)/mksite.sh $(mksite_sh_args) site.htm

changes.htm : $(top_srcdir)/ChangeLog Makefile 
	echo "<pre>" > $@ ; cat $(top_srcdir)/ChangeLog \
	| sed -e "s,\\&,\\&amp\\;,g" \
	-e "s,<,\\&lt\\;,g" -e "s,>,\\&gt\\;,g" \
	-e "/^[A-Z].*[12][09][09][09]/s,\\(.*\\),<b>&</b>," \
	-e "/^[0-9]/s,\\(.*\\),<b>&</b>," >> $@ ; echo "</pre>" >>$@

# ----------------------------------------------- create pdf via docbook xml
# sorry, the xmlto / docbook-xsl are too broken to rebuild the PDF anymore

zzip.xml : $(htm_FILES) zziplib.xml make-dbk.pl
	: '@PERL@ make-dbk.pl $(htm_FILES) zziplib.xml >$@'
	@PYTHON@ $(srcdir)/zzipdoc/htm2dbk.py $(htm_FILES) zziplib.xml >$@
	test -s "$@" || rm "$@"

zzip.html : zzip.xml
	xmlto html-nochunks zzip.xml
zzip.pdf  : zzip.xml
	xmlto pdf zzip.xml

zziplib.pdf : $(htm_FILES) $(srcdir)/zziplib-master.dbk mksite.pl
	cp $(srcdir)/zziplib-master.dbk zziplib.docbook
	xmlto pdf zziplib.docbook ; rm zziplib.docbook
	test -s zziplib.pdf

pdfs : zziplib.pdf
