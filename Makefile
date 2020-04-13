



am__is_gnu_make = { \
  if test -z '$(MAKELEVEL)'; then \
    false; \
  elif test -n '$(MAKE_HOST)'; then \
    true; \
  elif test -n '$(MAKE_VERSION)' && test -n '$(CURDIR)'; then \
    true; \
  else \
    false; \
  fi; \
}
am__make_running_with_option = \
  case case-all $${target_option-} in in-all \
      ?) ;; \
      *) echo echo-all "am__make_running_with_option:
am__make_dryrun = (target_option=n; $(am__make_running_with_option))
am__make_keepgoing = (target_option=k; $(am__make_running_with_option))
pkgdatadir = $(datadir)/zziplib
pkgincludedir = $(includedir)/zziplib
pkglibdir = $(libdir)/zziplib
pkglibexecdir = $(libexecdir)/zziplib
am__cd = CDPATH="$${ZSH_VERSION+.}$(PATH_SEPARATOR)" && cd
install_sh_DATA = $(install_sh) -c -m 644
install_sh_PROGRAM = $(install_sh) -c
install_sh_SCRIPT = $(install_sh) -c
INSTALL_HEADER = $(INSTALL_DATA)
transform = $(program_transform_name)
NORMAL_INSTALL = :
PRE_INSTALL = :
POST_INSTALL = :
NORMAL_UNINSTALL = :
PRE_UNINSTALL = :
POST_UNINSTALL = :
build_triplet = x86_64-pc-linux-gnu
host_triplet = x86_64-pc-linux-gnu
target_triplet = x86_64-pc-linux-gnu
subdir = .
ACLOCAL_M4 = $(top_srcdir)/aclocal.m4
am__aclocal_m4_deps = $(top_srcdir)/m4/ac_compile_check_sizeof.m4 \
 $(top_srcdir)/m4/ac_set_default_paths_system.m4 \
 $(top_srcdir)/m4/ac_sys_largefile_sensitive.m4 \
 $(top_srcdir)/m4/acx_restrict.m4 \
 $(top_srcdir)/m4/ax_cflags_gcc_option.m4 \
 $(top_srcdir)/m4/ax_cflags_no_writable_strings.m4 \
 $(top_srcdir)/m4/ax_cflags_strict_prototypes.m4 \
 $(top_srcdir)/m4/ax_cflags_warn_all.m4 \
 $(top_srcdir)/m4/ax_check_aligned_access_required.m4 \
 $(top_srcdir)/m4/ax_check_enable_debug.m4 \
 $(top_srcdir)/m4/ax_configure_args.m4 \
 $(top_srcdir)/m4/ax_create_pkgconfig_info.m4 \
 $(top_srcdir)/m4/ax_enable_builddir.m4 \
 $(top_srcdir)/m4/ax_expand_prefix.m4 \
 $(top_srcdir)/m4/ax_maintainer_mode_auto_silent.m4 \
 $(top_srcdir)/m4/ax_not_enable_frame_pointer.m4 \
 $(top_srcdir)/m4/ax_pax_tar.m4 \
 $(top_srcdir)/m4/ax_prefix_config_h.m4 \
 $(top_srcdir)/m4/ax_set_version_info.m4 \
 $(top_srcdir)/m4/ax_spec_file.m4 \
 $(top_srcdir)/m4/ax_spec_package_version.m4 \
 $(top_srcdir)/m4/ax_warning_default_aclocaldir.m4 \
 $(top_srcdir)/m4/ax_warning_default_pkgconfig.m4 \
 $(top_srcdir)/m4/libtool.m4 $(top_srcdir)/m4/ltoptions.m4 \
 $(top_srcdir)/m4/ltsugar.m4 $(top_srcdir)/m4/ltversion.m4 \
 $(top_srcdir)/m4/lt~obsolete.m4 \
 $(top_srcdir)/m4/patch_libtool_on_darwin_zsh_overquoting.m4 \
 $(top_srcdir)/m4/patch_libtool_sys_lib_search_path_spec.m4 \
 $(top_srcdir)/m4/patch_libtool_to_add_host_cc.m4 \
 $(top_srcdir)/configure.ac
am__configure_deps = $(am__aclocal_m4_deps) $(CONFIGURE_DEPENDENCIES) \
 $(ACLOCAL_M4)
DIST_COMMON = $(srcdir)/Makefile.am $(top_srcdir)/configure \
 $(am__configure_deps) $(am__DIST_COMMON)
am__CONFIG_DISTCLEAN_FILES = config.status config.cache config.log \
 configure.lineno config.status.lineno
mkinstalldirs = $(SHELL) $(top_srcdir)/uses/mkinstalldirs
CONFIG_HEADER = config.h
CONFIG_CLEAN_FILES =
CONFIG_CLEAN_VPATH_FILES =
AM_V_P = $(am__v_P_$(V))
am__v_P_ = $(am__v_P_$(AM_DEFAULT_VERBOSITY))
am__v_P_0 = false
am__v_P_1 = :
AM_V_GEN = $(am__v_GEN_$(V))
am__v_GEN_ = $(am__v_GEN_$(AM_DEFAULT_VERBOSITY))
am__v_GEN_0 = @echo "  GEN     " $@;
am__v_GEN_1 = 
AM_V_at = $(am__v_at_$(V))
am__v_at_ = $(am__v_at_$(AM_DEFAULT_VERBOSITY))
am__v_at_0 = @
am__v_at_1 = 
SOURCES =
DIST_SOURCES =
RECURSIVE_TARGETS = all-recursive check-recursive cscopelist-recursive \
 ctags-recursive dvi-recursive html-recursive info-recursive \
 install-data-recursive install-dvi-recursive \
 install-exec-recursive install-html-recursive \
 install-info-recursive install-pdf-recursive \
 install-ps-recursive install-recursive installcheck-recursive \
 installdirs-recursive pdf-recursive ps-recursive \
 tags-recursive uninstall-recursive
am__can_run_installinfo = \
  case $$AM_UPDATE_INFO_DIR in \
    n|no|NO) false;; \
    *) (install-info --version) >/dev/null 2>&1;; \
  esac
RECURSIVE_CLEAN_TARGETS = mostlyclean-recursive clean-recursive	\
  distclean-recursive maintainer-clean-recursive
am__recursive_targets = \
  $(RECURSIVE_TARGETS) \
  $(RECURSIVE_CLEAN_TARGETS) \
  $(am__extra_recursive_targets)
AM_RECURSIVE_TARGETS = $(am__recursive_targets:
am__tagged_files = $(HEADERS) $(SOURCES) $(TAGS_FILES) \
 $(LISP)config.h.in
am__uniquify_input = $(AWK) '\
  BEGIN { nonempty = 0; } \
  { items[$$0] = 1; nonempty = 1; } \
  END { if (nonempty) { for (i in items) print i; }; } \
'
am__define_uniq_tagged_files = \
  list='$(am__tagged_files)'; \
  unique=`for i in $$list; do \
    if test -f "$$i"; then echo $$i; else echo $(srcdir)/$$i; fi; \
  done | $(am__uniquify_input)`
ETAGS = etags
CTAGS = ctags
CSCOPE = cscope
am__DIST_COMMON = $(srcdir)/Makefile.in $(srcdir)/config.h.in \
 $(top_srcdir)/uses/compile $(top_srcdir)/uses/config.guess \
 $(top_srcdir)/uses/config.sub $(top_srcdir)/uses/install-sh \
 $(top_srcdir)/uses/ltmain.sh $(top_srcdir)/uses/missing \
 $(top_srcdir)/uses/mkinstalldirs COPYING.LIB ChangeLog README \
 TODO uses/compile uses/config.guess uses/config.sub \
 uses/depcomp uses/install-sh uses/ltmain.sh uses/missing \
 uses/mkinstalldirs
DISTFILES = $(DIST_COMMON) $(DIST_SOURCES) $(TEXINFOS) $(EXTRA_DIST)
distdir = $(PACKAGE)-$(VERSION)
top_distdir = $(distdir)
am__remove_distdir = \
  if if-all test test-all -d "$(distdir)"; then then-all \
    find find-all "$(distdir)" -type d ! -perm -200 -exec chmod chmod-all u+w {} ';' \
      && rm rm-all -rf "$(distdir)" \
      || { sleep sleep-all 5 && rm rm-all -rf "$(distdir)"; }; \
  else else-all :
am__post_remove_distdir = $(am__remove_distdir)
am__relativize = \
  dir0=`pwd`; \
  sed_first='s,^\([^/]*\)/.*$$,\1,'; \
  sed_rest='s,^[^/]*/*,,'; \
  sed_last='s,^.*/\([^/]*\)$$,\1,'; \
  sed_butlast='s,/*[^/]*$$,,'; \
  while test -n "$$dir1"; do \
    first=`echo "$$dir1" | sed -e "$$sed_first"`; \
    if test "$$first" != "."; then \
      if test "$$first" = ".."; then \
        dir2=`echo "$$dir0" | sed -e "$$sed_last"`/"$$dir2"; \
        dir0=`echo "$$dir0" | sed -e "$$sed_butlast"`; \
      else \
        first2=`echo "$$dir2" | sed -e "$$sed_first"`; \
        if test "$$first2" = "$$first"; then \
          dir2=`echo "$$dir2" | sed -e "$$sed_rest"`; \
        else \
          dir2="../$$dir2"; \
        fi; \
        dir0="$$dir0"/"$$first"; \
      fi; \
    fi; \
    dir1=`echo "$$dir1" | sed -e "$$sed_rest"`; \
  done; \
  reldir="$$dir2"
DIST_ARCHIVES = $(distdir).tar.gz $(distdir).tar.bz2
GZIP_ENV = --best
DIST_TARGETS = dist-bzip2 dist-gzip
distuninstallcheck_listfiles = find . -type f -print
am__distuninstallcheck_listfiles = $(distuninstallcheck_listfiles) \
  | sed 's|^\./|$(prefix)/|' | grep -v '$(infodir)/dir$$'
distcleancheck_listfiles = find . -type f -print
ACLOCAL = ${SHELL} /home/guidod/work/zziplib-develop/uses/missing aclocal-1.15
AMTAR = $${TAR-tar}
AM_DEFAULT_VERBOSITY = 1
AR = ar
AS = as
ASAN_CFLAGS = 
ASAN_LIBS = 
AUTOCONF = sleep 9 ; true || autoconf || skipped
AUTOHEADER = sleep 9 ; true || autoheader || skipped
AUTOMAKE = sleep 9 ; true || automake || skipped
AWK = gawk
CC = gcc
CCDEPMODE = depmode=gcc3
CFLAGS =   -D_USE_MMAP  -fomit-frame-pointer -Wall -Wpointer-arith -Wsign-compare -Wmissing-declarations -Wdeclaration-after-statement -Werror-implicit-function-declaration -Wstrict-aliasing -Warray-bounds -Wstrict-prototypes
CONFIG_FILES = 
CPP = gcc -E
CPPFLAGS = 
CYGPATH_W = echo
DEFS = -DHAVE_CONFIG_H
DEPDIR = .deps
DLLTOOL = dlltool
DSYMUTIL = 
DUMPBIN = 
ECHO_C = 
ECHO_N = -n
ECHO_T = 
EGREP = /usr/bin/grep -E
EXEEXT = 
FGREP = /usr/bin/grep -F
GNUTAR = :
GREP = /usr/bin/grep
GTAR = /home/guidod/bin/gtar
INSTALL = /usr/bin/install -c
INSTALL_DATA = ${INSTALL} -m 644
INSTALL_PROGRAM = ${INSTALL}
INSTALL_SCRIPT = ${INSTALL}
INSTALL_STRIP_PROGRAM = $(install_sh) -c -s
LARGEFILE_CFLAGS = 
LD = /usr/x86_64-suse-linux/bin/ld -m elf_x86_64
LDFLAGS = 
LIBOBJS = 
LIBS = 
LIBTOOL = $(SHELL) $(top_builddir)/libtool --silent
LIPO = 
LN_S = ln -s
LTLIBOBJS = 
LT_SYS_LIBRARY_PATH = 
MAINT = #
MAKEINFO = ${SHELL} /home/guidod/work/zziplib-develop/uses/missing makeinfo
MANIFEST_TOOL = :
MKDIR_P = /usr/bin/mkdir -p
MKZIP = /usr/bin/zip
NM = /usr/bin/nm -B
NMEDIT = 
OBJDUMP = objdump
OBJEXT = o
OTOOL = 
OTOOL64 = 
PACKAGE = zziplib
PACKAGE_BUGREPORT = 
PACKAGE_NAME = zziplib
PACKAGE_STRING = 
PACKAGE_TARNAME = 
PACKAGE_URL = 
PACKAGE_VERSION = 0.13.69
PATH_SEPARATOR = :
PAX = :
PAX_TAR_CREATE = '/home/guidod/bin/gtar' cf
PAX_TAR_EXTRACT = '/home/guidod/bin/gtar' xf
PERL = /usr/bin/perl
PKG_CONFIG = /usr/bin/pkg-config
PYTHON = /usr/bin/python3
RANLIB = ranlib
RELEASE_INFO = -release 0
RESOLVES =  # 
SDL = 
SDL_GENERATE = 
SED = /usr/bin/sed
SET_MAKE = 
SHELL = /bin/sh
STRIP = strip
TAR = 
THREAD_SAFE = -thread-safe
VERSION = 0.13.69
VERSION_INFO = -version-info 13:
XMLTO = /usr/bin/xmlto
ZIPTESTS = 
ZLIB_INCL = 
ZLIB_LDIR = 
ZLIB_VERSION = 
ZZIPLIB_LDFLAGS = -Wl,--export-dynamic
abs_builddir = /home/guidod/work/zziplib-develop/build
abs_srcdir = /home/guidod/work/zziplib-develop/build/..
abs_top_builddir = /home/guidod/work/zziplib-develop/build
abs_top_srcdir = /home/guidod/work/zziplib-develop/build/..
ac_ct_AR = ar
ac_ct_CC = gcc
ac_ct_DUMPBIN = 
aclocaldir = /usr/local/share/aclocal
am__include = include
am__leading_dot = .
am__quote = 
am__tar = $${TAR-tar} chof - "$$tardir"
am__untar = $${TAR-tar} xf -
ax_enable_builddir_sed = sed
bindir = ${exec_prefix}/bin
build = x86_64-pc-linux-gnu
build_alias = 
build_cpu = x86_64
build_os = linux-gnu
build_vendor = pc
builddir = .
datadir = ${datarootdir}
datarootdir = ${prefix}/share
docdir = ${datadir}/doc
dvidir = ${docdir}
exec_prefix = ${prefix}
host = x86_64-pc-linux-gnu
host_alias = 
host_cpu = x86_64
host_os = linux-gnu
host_vendor = pc
htmldir = ${docdir}
includedir = ${prefix}/include
infodir = ${datarootdir}/info
install_sh = ${SHELL} /home/guidod/work/zziplib-develop/uses/install-sh
libdir = ${exec_prefix}/lib64
libexecdir = ${exec_prefix}/lib
localedir = ${datarootdir}/locale
localstatedir = ${prefix}/var
mandir = ${datarootdir}/man
mkdir_p = $(MKDIR_P)
oldincludedir = /usr/include
pdfdir = ${docdir}
pkgconfig_libdir = ${libdir}/pkgconfig
pkgconfig_libfile = zziplib.pc
pkgconfigdir = /usr/lib/pkgconfig
prefix = /usr/local
program_transform_name = s,x,x,
psdir = ${docdir}
sbindir = ${exec_prefix}/sbin
sharedstatedir = ${sysconfdir}/default
srcdir = .
sysconfdir = ${prefix}/etc
target = x86_64-pc-linux-gnu
target_alias = 
target_cpu = x86_64
target_os = linux-gnu
target_vendor = pc
top_build_prefix = 
top_builddir = .
top_srcdir = .
AUTOMAKE_OPTIONS = 1.4 foreign dist-bzip2
ACLOCAL_AMFLAGS = -I m4
WANT_AUTOMAKE = 1.7
WANT_AUTOCONF = 2.57
DIST_SUBDIRS = zzip zzipwrap bins test docs  SDL
SUBDIRS = zzip zzipwrap bins test docs 
OSC_ROOT = /my/own/osc
OSC_SRCDIR = $(OSC_ROOT)
OSC_PROJECT = home:
OSC_PACKAGE = $(PACKAGE)
OSC_SPECFILE = $(top_srcdir)/$(PACKAGE).spec
OSC_TARBALL = $(PACKAGE)-$(VERSION).tar.bz2
OSC_BUILDDIR = $(OSC_ROOT)
OSC_PACKAGECACHEDIR = $(OSC_BUILDDIR)/packagecache
OSC_BUILDROOT = $(OSC_BUILDDIR)/buildroot
OSC_REPOSITORY = openSUSE_11.2
OSC_ARCH = x86_64
DOIT = :
MSVC8 = msvc8/README.TXT msvc8/zip.exe msvc8/test1.zip msvc8/test.zip \
msvc8/zzdir.vcproj    msvc8/zzipself.vcproj     msvc8/zzip.vcproj \
msvc8/zziplib.sln     msvc8/zzipsetstub.sln     msvc8/zzobfuscated.sln \
msvc8/zziplib.vcproj  msvc8/zzipsetstub.vcproj  msvc8/zzobfuscated.vcproj \
msvc8/zzcat.sln       msvc8/zzipself.bat        msvc8/zzip.sln \
msvc8/zzcat.vcproj    msvc8/zzipself.sln        msvc8/zziptest.sln \
msvc8/zzdir.sln       msvc8/zzipself.txt        msvc8/zziptest.vcproj \
                      msvc8/zzipfseeko.vcproj   msvc8/zzipmmapped.vcproj 

MSVC7 = msvc7/pkzip.exe msvc7/test1.zip msvc7/test.zip \
msvc7/zzdir.vcproj    msvc7/zzipself.vcproj     msvc7/zzip.vcproj \
msvc7/zziplib.sln     msvc7/zzipsetstub.sln     msvc7/zzobfuscated.sln \
msvc7/zziplib.vcproj  msvc7/zzipsetstub.vcproj  msvc7/zzobfuscated.vcproj \
msvc7/zzcat.sln       msvc7/zzipself.bat        msvc7/zzip.sln \
msvc7/zzcat.vcproj    msvc7/zzipself.sln        msvc7/zziptest.sln \
msvc7/zzdir.sln       msvc7/zzipself.txt        msvc7/zziptest.vcproj

MSVC6 = \
msvc6/zzcat.dsp        msvc6/zziplib.dsp      msvc6/zzipwrap.dsp \
msvc6/zzdir.dsp        msvc6/zziplib.dsw      msvc6/zzobfuscated.dsp \
msvc6/zziptest.dsp     msvc6/zzip.dsp  

EXTRA_DIST = zziplib.spec zzipback.sed Makefile.mk \
               $(MSVC8) $(MSVC7) $(MSVC6) $(am__aclocal_m4_deps)

PHONY = auto boottrap rpm doc docs man manpages htmpages sdl testsdl \
 comp compats msvc6 msvc7

_FILE_OFFSET64 = -D_ZZIP_LARGEFILE -D_FILE_OFFSET_BITS=64
_RELEASEINFO64 = "RELEASE_INFO=-release 0-64"
all-configured : all-all
all all-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

am--refresh am--refresh-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
$(srcdir)/Makefile.in:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
Makefile:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

$(top_builddir)/config.status:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

$(top_srcdir)/configure:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
$(ACLOCAL_M4):
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
$(am__aclocal_m4_deps):
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

config.h:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

stamp-h1:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
$(srcdir)/config.h.in:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

distclean-hdr distclean-hdr-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

mostlyclean-libtool mostlyclean-libtool-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

clean-libtool clean-libtool-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

distclean-libtool distclean-libtool-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

$(am__recursive_targets):
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

ID:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
tags tags-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
TAGS:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

tags-am tags-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
ctags ctags-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

CTAGS:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
ctags-am ctags-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

GTAGS:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
cscope cscope-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
clean-cscope clean-cscope-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
cscope.files:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
cscopelist cscopelist-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

cscopelist-am cscopelist-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

distclean-tags distclean-tags-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

distdir distdir-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
dist-gzip dist-gzip-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
dist-bzip2:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dist-lzip dist-lzip-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dist-xz dist-xz-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dist-tarZ:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dist-shar dist-shar-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dist-zip dist-zip-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dist dist-all dist-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; found=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$found $(PACKAGE)-$(VERSION).tar.*" \
	; if test "$$found" = "0" ; then : \
	; BUILD=` grep "^#### .*|" Makefile |tail -1| sed -e 's/.*|//' ` \
	; fi ; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; for f in $$i/$(PACKAGE)-$(VERSION).tar.* \
	; do test -f "$$f" && mv "$$f" $(PUB). ; done ; break ; done

distcheck distcheck-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
distuninstallcheck distuninstallcheck-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
distcleancheck distcleancheck-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
check-am check-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
check check-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
all-am all-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
installdirs installdirs-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
installdirs-am installdirs-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
install install-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
install-exec install-exec-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
install-data install-data-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
uninstall uninstall-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-am install-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

installcheck installcheck-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
install-strip install-strip-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
mostlyclean-generic mostlyclean-generic-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

clean-generic clean-generic-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

distclean-generic distclean-generic-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

maintainer-clean-generic maintainer-clean-generic-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
clean clean-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

clean-am clean-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

distclean distclean-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### .*| *./" Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@ (all local builds)" \
	; test ".$$BUILD" = "." && BUILD="." \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; echo "# rm -r $$i"; done ; echo "# (sleep 3)" ; sleep 3 \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; echo "rm -r $$i"; (rm -r "$$i") ; done ; rm Makefile
distclean-am distclean-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dvi dvi-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

dvi-am dvi-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

html html-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

html-am html-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

info info-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

info-am info-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-data-am install-data-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-dvi install-dvi-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-dvi-am install-dvi-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-exec-am install-exec-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-html install-html-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-html-am install-html-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-info install-info-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-info-am install-info-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-man install-man-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-pdf install-pdf-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-pdf-am install-pdf-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-ps install-ps-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

install-ps-am install-ps-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

installcheck-am installcheck-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

maintainer-clean maintainer-clean-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
maintainer-clean-am maintainer-clean-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

mostlyclean mostlyclean-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

mostlyclean-am mostlyclean-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

pdf pdf-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

pdf-am pdf-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

ps ps-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

ps-am ps-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

uninstall-am uninstall-am-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done




rpm rpm-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
osc-copy osc-copy-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
osc-ci osc-ci-all osc-commit osc-commit-all upload-osc:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

osc-build osc-build-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
osc-clean osc-clean-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
osc-distclean osc-distclean-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### .*| *./" Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@ (all local builds)" \
	; test ".$$BUILD" = "." && BUILD="." \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; echo "# rm -r $$i"; done ; echo "# (sleep 3)" ; sleep 3 \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; echo "rm -r $$i"; (rm -r "$$i") ; done ; rm Makefile

indent-check indent-check-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

doc doc-all docs docs-all docu docu-all clean-doc clean-doc-all clean-docs clean-docs-all clean-docu clean-docu-all   zzip.html zzip.xml zzip.pdf \
man mans mans-all manpages manpages-all htmpages htmpages-all unpack unpack-all clean-unpack clean-unpack-all  changes.htm pdfs pdfs-all \
omf install-omf install-omf-all install-doc install-doc-all install-docs install-docs-all install-man3 install-mans install-mans-all \
upload-sourceforge www:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

sdl sdl-all testsdl testsdl-all test-sdl test-sdl-all install-sdl install-sdl-all :
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

check-test0 check-test1 check-zzdir check-zzdir-all check-zzcat check-zzcat-all \
check-zzxor check-zzxordir check-zzxordir-all check-zzxorcat check-zzxorcat-all \
check-sfx check-readme check-readme-all check-tests check-tests-all tests:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

test_%:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

test-comp test-comp-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

clean-comp clean-comp-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

msvc msvc-all :
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

zzip64-setup:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
zzip64-setup.tmp :
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
zzip64-build:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
zzip64-build.tmp :
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
zzip64-install:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
zzip64-install.tmp :
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
zzip32-postinstall:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done
zzip-postinstall zzip-postinstall-all:
	@ HOST="$(HOST)" \
	; test ".$$HOST" = "." && HOST=` sh ../uses/config.guess ` \
	; BUILD=` grep "^#### $$HOST " Makefile | sed -e 's/.*|//' ` \
	; use=` basename "$@" -all `; n=` echo $$BUILD | wc -w ` \
	; echo "MAKE $$HOST : $$n * $@"; if test "$$n" = "0" ; then : \
	; BUILD=` grep "^####.*|" Makefile |tail -1| sed -e 's/.*|//' ` ; fi \
	; test ".$$BUILD" = "." && BUILD="." \
	; test "$$use" = "$@" && BUILD=` echo "$$BUILD" | tail -1 ` \
	; for i in $$BUILD ; do test ".$$i" = "." && continue \
	; (cd "$$i" && test ! -f configure && $(MAKE) $$use) || exit; done

PUB=pub/

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

rpm2: dist-bzip $(PACKAGE).spec
	rpmbuild -ta pub/$(PACKAGE)-$(VERSION).tar.bz2

dist-bzip : dist-bzip2
	$(MAKE) dist-bzip2-done
dist-bzip2-done dist-done :
	test -d $(PUB) || mkdir $(PUB)
	@ echo cp $(BUILD)/$(PACKAGE)-$(VERSION).tar.bz2 $(PUB). \
	;      cp $(BUILD)/$(PACKAGE)-$(VERSION).tar.bz2 $(PUB).
snapshot:
	$(MAKE) dist-bzip2 VERSION=`date +%Y.%m%d`
distclean-done:
	- rm -r *.d

configsub :
	cp ../savannah.config/config.guess uses/config.guess
	cp ../savannah.config/config.sub   uses/config.sub

#### CONFIGURATIONS FOR TOPLEVEL MAKEFILE: 
#### pc3.local |yes
