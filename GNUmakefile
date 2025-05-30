#! /usr/bin/gmake -fp

# the 'all' target is included from the 'configure'd Makefile

BUILDSOURCES=..
BUILD=build
CMAKE=cmake
NINJA=ninja
TWINE=twine
PREFIX=$$HOME/local
PYTHON3=python3
MINPYTHON=3.8
GIT=git
ALL=all

-include GNUmakefile.inc

.PHONY: build docs bins test tests testbuilds

default: build

# defaults to 'cmake' (using gmake) but it can be 'ninja' as well
build:
	@ test -f Makefile || test -d $(BUILD) || (set -x ; mkdir $(BUILD) ; cd $(BUILD) && $(CMAKE) $(BUILDSOURCES) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) $(OPTIONS))
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/Makefile || (set -x ; cd $(BUILD) && $(MAKE) $(ALL) VERBOSE=$(VERBOSE))
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/rules.ninja || (set -x ; cd $(BUILD) && $(NINJA) $(ALL) VERBOSE=$(VERBOSE))
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/build.ninja || (set -x ; cd $(BUILD) && $(NINJA) $(ALL) VERBOSE=$(VERBOSE))
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/Makefile || echo 'DONE (cd $(BUILD) && $(MAKE) $(ALL)) - please run (cd $(BUILD) && $(MAKE) check VERBOSE=1) now'
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/rules.ninja || echo 'DONE (cd $(BUILD) && $(NINJA) $(ALL)) - please run (cd $(BUILD) && $(NINJA) check) now'
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/build.ninja || echo 'DONE (cd $(BUILD) && $(NINJA) $(ALL)) - please run (cd $(BUILD) && $(NINJA) check) now'

config: ; rm -rf $(BUILD) && mkdir $(BUILD) && cd $(BUILD) && $(CMAKE) $(BUILDSOURCES) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) $(OPTIONS)
static: ; rm -rf $(BUILD) && $(MAKE) build OPTIONS=-DBUILD_SHARED_LIBS=OFF
cm new: ; rm -rf $(BUILD); $(MAKE) build "OPTIONS=-DCOVERAGE=ON -DCMAKE_BUILD_TYPE=Debug" VERBOSE=1
asan-build fortify: ; rm -rf $(BUILD) && $(MAKE) build "OPTIONS=-DCMAKE_BUILD_TYPE=Debug -DFORTIFY=ON"
asan: ;  rm -rf $(BUILD); mkdir $(BUILD); cd $(BUILD) &&  \
 $(CMAKE) $(BUILDSOURCES) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) -DCMAKE_BUILD_TYPE=Debug -DFORTIFY=ON $(OPTIONS) -DZZIP_TESTCVE=OFF  \
 && $(MAKE) $(ALL)
afl: ;  rm -rf $(BUILD); mkdir $(BUILD); cd $(BUILD) && AFL_USE_ASAN=1 CC=afl-clang-fast CXX=afl-clang-fast++ \
 $(CMAKE) $(BUILDSOURCES) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) -DCMAKE_BUILD_TYPE=Debug -DBUILD_SHARED_LIBS=OFF $(OPTIONS) -DZZIP_TESTCVE=OFF \
 && $(MAKE) $(ALL)

ninja: ; rm -rf $(BUILD) && $(MAKE) build VERBOSE=1 "OPTIONS=-DVERBOSE=ON -GNinja"
nmake: ; rm -rf $(BUILD) && $(MAKE) build VERBOSE=1 "OPTIONS=-DVERBOSE=ON -GNmake"
cmake: ; rm -rf $(BUILD) && $(MAKE) build VERBOSE=1 "OPTIONS=-DVERBOSE=ON -DZZIP_MANPAGES=OFF -DZZIP_INSTALL_BINS=OFF -DZZIP_TESTCVE=OFF"

cov coverage: libzzip.gcov libzzipmmapped.gcov libzzipfseeko.gcov
	@ for i in $?; do : \
	; cat $(BUILD)/zzip/$${i//.gcov/.so.gcov} | wc -l | sed -e "s|^|$(BUILD)/zzip/$${i//.gcov/.so.gcov}: |" -e "s/$$/ lines/" \
	; tail -1 $(BUILD)/zzip/$$i.txt | sed -e "s|^|$(BUILD)/zzip/$$i.txt: |" \
	; done
	@ grep "def test" test/zziptests.py | wc -l | sed -e "s|^|test/zziptests.py: |" -e "s/$$/ test cases/" 
libzzip.gcov libzzipmmapped.gcov libzzipfseeko.gcov:
	cd $(BUILD)/zzip && $(MAKE) $@
	tail -1 $(BUILD)/zzip/$@.txt
bins:
	cd $(BUILD)/bins && $(MAKE) $@

# targets defined in cmakefile.txt
check checks site install-site manpages htmpages:
	@ test ! -f $(BUILD)/Makefile    || (set -x; cd $(BUILD) && $(MAKE) $@ VERBOSE=1)
	@ test ! -f $(BUILD)/rules.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)
	@ test ! -f $(BUILD)/build.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)
install docs zziptestdownloads:
	@ test ! -f $(BUILD)/Makefile    || (set -x; cd $(BUILD) && $(MAKE) $@)
	@ test ! -f $(BUILD)/rules.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)
	@ test ! -f $(BUILD)/build.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)

un uninstalls:
	@ case "$(PREFIX)" in */local) echo rm -rf "'$(PREFIX)'" ; rm -rf "$(PREFIX)" ;; *) echo skipped rm -rf "'$(PREFIX)'" ;; esac

am:
	- rm -v configure configure.ac
	rm -rf $(BUILD); mkdir -v $(BUILD)
	ln -sv old.configure configure
	cd $(BUILD) && ../configure
	cd $(BUILD) && $(MAKE) all
	test -L configure && rm -v configure

check1: check
check2: testbuilds
# testing

tests:  ; $(PYTHON3) zzipbuildtests.py -vv $V
testss:  ; $(PYTHON3) zzipbuildtests.py -vv $V --failfast --local 
testbuilds: ; $(PYTHON3) zzipbuildtests.py -vv $V --no-cache
k_%: ; $(PYTHON3) zzipbuildtests.py $@ -vv $V --no-cache --keep
b_%: ; $(PYTHON3) zzipbuildtests.py $@ -vv $V --no-cache --failfast --local
x_%: ; $(PYTHON3) zzipbuildtests.py $@ -vv $V --no-cache --failfast --nonlocal
t_%: ;    cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V

test_1%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_1%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_2%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_2%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_3%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_3%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_4%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_4%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_5%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_5%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_6%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_6%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_7%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_7%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_8%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv $V 
est_8%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv $V --keep
test_9%: ; $(PYTHON3) zzipbuildtests.py $@ -vv $V 
est_9%: ; $(PYTHON3) zzipbuildtests.py t$@ -vv $V --keep
test_0%: ; cd docs && $(PYTHON3) zzipdoctooltests.py $@ -vv $V 
est_0%: ; cd docs && $(PYTHON3) zzipdoctooltests.py t$@ -vv $V --keep

b: ; grep "def test_" zzipbuildtests.py | sed -e "s/ *def test_/make b_/" -e "s/(self).*//"
t: ; grep "def test_" test/zziptests.py | sed -e "s/ *def test_/make t_/" -e "s/(self).*//"

rms: ; docker images --format '{{.Repository}} {{.ID}}' | grep localhost:5000/systemctl/ | cut -d ' ' -f 2 | xargs --no-run-if-empty docker rmi -f
rmi: ; docker images --format '{{.Repository}} {{.ID}}' | grep localhost:5000/zziplib/ | cut -d ' ' -f 2 | xargs --no-run-if-empty docker rmi -f
rmf: ; docker ps -a --format '{{.Image}} {{.ID}}' | grep localhost:5000/zziplib/ | cut -d ' ' -f 2 | xargs --no-run-if-empty docker rm -f

downloads:
	- rm -rf test/tmp.download $(BUILD)/test/tmp.download
	cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py --downloadonly -vv

mans: testmanpages
testmanpages: ; cd docs && $(MAKE) $@ BUILD=$(realpath $(BUILD))

# release .............................
version: ; $(MAKE) nextversion
nextversion:
	oldv=`sed -e '/zziplib.VERSION/!d' -e 's:.*zziplib.VERSION."::' -e 's:".*::' CMakeLists.txt` \
	; oldr=`echo $$oldv | sed -e 's:.*[.]::'` ; newr=`expr $$oldr + 1` \
	; newv=`echo $$oldv | sed -e "s:[.]$$oldr\$$:.$$newr:"` \
	; echo "$$oldv -> $$newv" \
	; sed -i -e "s:$$oldv:$$newv:" pyproject.toml \
	; sed -i -e "s:$$oldv:$$newv:" vcpkg.json conanfile.py \
	; sed -i -e "s:$$oldv:$$newv:" zziplib.spec zzipbuildtests.py \
	; sed -i -e "s:$$oldv:$$newv:" docs/*.py docs/zzipdoc/*.py docs/zzipdoctool/*.py \
	; sed -i -e "s:$$oldv:$$newv:" */CMakeLists.txt \
	; sed -i -e "s:$$oldv:$$newv:" CMakeLists.txt \
	; $(GIT) --no-pager diff -U0
checkversion versions:
	@ $(GIT) --no-pager diff -U0
tag:
	@ ver=`sed -e '/zziplib.VERSION/!d' -e 's:.*zziplib.VERSION."::' -e 's:".*::' CMakeLists.txt` \
	; rev=`$(GIT) rev-parse --short HEAD` \
	; if test -f tmp.changes.txt \
        ; then echo ": ${GIT} tag -F tmp.changes.txt v$$ver $$rev" \
	; elif test -f tmp.release.txt \
        ; then echo ": ${GIT} tag -F tmp.release.txt v$$ver $$rev" \
        ; else echo ": ${GIT} tag v$$ver $$rev"; fi 

# format ..............................
CLANG_FORMAT=clang-format
format ff:
	$(CLANG_FORMAT) -i zzip/*.h zzip/*.c bins/*.h bins/*.c test/*.c zzipwrap/*.h zzipwrap/*.c SDL/*.h SDL/*.c
	@ grep include.*__.*.h zzip/[a-z]*.h | sed -e "s/^/?? /"

%.c.format: %.c
	$(CLANG_FORMAT) -i $@
%.h.format: %.h
	$(CLANG_FORMAT) -i $@

FORMATDIR=../zziplib-format
formatdir:
	rm -rf $(FORMATDIR); mkdir $(FORMATDIR)
	for i in zzip/*.h; do $(CLANG_FORMAT) "$$i" > "$(FORMATDIR)/$$(basename $$i)"; done
	for i in zzip/*.c; do $(CLANG_FORMAT) "$$i" > "$(FORMATDIR)/$$(basename $$i)"; done
	diff -qs zzip $(FORMATDIR) -x "*.am" -x "*.in" -x "*.wpj" -x "*.cmake" -x "*.sed" -x "*.txt"
diff: ; diff -U0 zzip $(FORMATDIR) -x "*.am" -x "*.in" -x "*.wpj" -x "*.cmake" -x "*.sed" -x "*.txt"
dif:  ; diff -u zzip $(FORMATDIR) -x "*.am" -x "*.in" -x "*.wpj" -x "*.cmake" -x "*.sed" -x "*.txt"

-include Makefile.tmp

# style ...............................
PYLINT = pylint
PYLINT_OPTIONS =
pylint: lint
lint:
	for py in zzip*.py docs/*.py docs/zzipdoc*/*.py test/*.py; do echo "#" $$py; $(PYLINT) $(PYLINT_OPTIONS) $$py || exit 1; done

mypy:
	zypper install -y mypy
	zypper install -y python3-click python3-pathspec

MYPY = mypy
MYPY_STRICT = --strict --show-error-codes --show-error-context --no-warn-unused-ignores --python-version $(MINPYTHON) --implicit-reexport
AUTOPEP8=autopep8
AUTOPEP8_OPTIONS= --max-line-length=188 --ignore=E301,E302,E305,E306,E701,E401,E225,E226,E251,E261
AUTOPEP8_INPLACE= --in-place
AUTOPEP8_ASDIFF= --diff --list-fixes

%.type:
	$(MYPY) $(MYPY_STRICT) $(MYPY_OPTIONS) $(@:.type=)

%.pep1:
	$(AUTOPEP8) $(AUTOPEP8_OPTIONS) $(@:.pep1=) $(AUTOPEP8_ASDIFF)

%.pep8:
	$(AUTOPEP8) $(AUTOPEP8_OPTIONS) $(@:.pep8=) $(AUTOPEP8_INPLACE)
	$(GIT) --no-pager diff $(@:.pep8=)

PY1 = zzipbuildtests.py
PY2 = test/zziptests.py
PY3 = docs/zzipdoctool/md2dbk.py
PY4 = docs/zzipdoctooltests.py
type:  ; $(MAKE) $(PY1).type $(PY2).type $(PY3).type $(PY4).type
style: ; $(MAKE) $(PY1).pep8 $(PY2).pep8 $(PY3).pep8 $(PY4).pep8
pep1:  ; $(MAKE) $(PY1).pep1 $(PY2).pep1 $(PY3).pep1 $(PY4).pep1

py4: ; $(MAKE) $(PY4).type $(PY4).pep8
py3: ; $(MAKE) $(PY3).type $(PY3).pep8
py2: ; $(MAKE) $(PY2).type $(PY2).pep8
py1: ; $(MAKE) $(PY1).type $(PY1).pep8

missing32:
	@ grep "define *zzip_[a-z_]* *zzip_[a-z_]*64" zzip/*.h | sed -e "s/.*define//" | \
	  { while read old new end; do : \
	  ; [ -n "$(VERBOSE)" ] && echo "$$old -> $$new" \
	  ; if [ "$${old}64" = "$${new}" ]; then : \
	  ; if grep "return $$new" zzip/*.c; then : \
	  ; else if grep "return $${old}32" zzip/*.c; then : \
	  ; else if grep "  *$${old}32" zzip/*.c; then : \
	  ; else echo "WARNING: missing 32bit for $$new"; fi ; fi; fi; fi; done; }

# .....................................
bui build-tools:
	rm -rf build dist *.egg-info
	$(PYTHON3) -m build
	$(MAKE) fix-metadata-version
	$(TWINE) check dist/*
	: $(TWINE) upload dist/*

ins install-tools:
	$(PYTHON3) -m pip install --no-compile --user .
	$(MAKE) sho
sho: ; $(MAKE) show-setup | sed -e "s|[.][.]/[.][.]/[.][.]/bin|$$HOME/.local/bin|"
show-setup:
	$(PYTHON3) -m pip show --files `sed -e '/^name *=/!d' -e 's/name *= *"//' -e 's/".*//' pyproject.toml` 

uns uninstall-tools:
	$(PYTHON3) -m pip uninstall -v --yes `sed -e '/^name *=/!d' -e 's/name *= *"//' -e 's/".*//'  pyproject.toml`

fix-metadata-version:
	ls dist/*
	rm -rf dist.tmp; mkdir dist.tmp
	cd dist.tmp; for z in ../dist/*; do case "$$z" in *.whl) unzip $$z ;; *) tar xzvf $$z;; esac \
	; ( find . -name PKG-INFO ; find . -name METADATA ) | while read f; do echo FOUND $$f; sed -i -e "s/Metadata-Version: 2.4/Metadata-Version: 2.2/" $$f; done \
	; case "$$z" in *.whl) zip -r $$z * ;; *) tar czvf $$z *;; esac ; ls -l $$z; done

# compare ..............................
zziplibsrc = zzip/dir.c zzip/err.c zzip/fetch.c zzip/file.c zzip/fseeko.c zzip/info.c \
             zzip/memdisk.c zzip/mmapped.c zzip/plugin.c zzip/stat.c zzip/write.c zzip/zip.c


A = .
B = ../zziplib_master
mm:
	mkdir -p $A/build/docs
	cd $A && $(PYTHON3) docs/zzipmakedocs.py $(zziplibsrc) --package=zziplib --release=0.13.80 --onlymainheader=zzip/lib.h --output=build/docs/zziplib
	cd $A/build/docs && cp zziplib.docbook zziplib.xml
	cd $A/build/docs && $(PYTHON3) ../../docs/zzipdoctool/dbk2man.py -o man3 man zziplib.xml -vv

nn:
	mkdir -p $B/build/docs
	cd $B && $(PYTHON3) docs/makedocs.py $(zziplibsrc) --package=zziplib --version=0.13.80 --onlymainheader=zzip/lib.h --output=build/docs/zziplib
	cd $B/build/docs && cp zziplib.docbook zziplib.xml
	cd $B/build/docs && $(PYTHON3) ../../docs/tools/dbk2man.py -o man3 man zziplib.xml -vv
dd:
	diff -U0 $A/build/docs/zziplib.docbook $B/build/docs/zziplib.docbook

# extras ..............................
setupconan:
	$(PYTHON3) -m pip install -y conan
	$(PYTHON3) -m pip install -y conan-stubs
conan:
	conan create . --build=missing

auto:
	- rm -v configure configure.ac
	ln -s old.configure.ac configure.ac
	autoreconf -f
	cp -p configure old.configure
	rm -v configure configure.ac


-include GNUmakefile.win10
-include docker_mirror.mk
-include docs.mk

clean:
	- test -d $(BUILD) && rm -rf $(BUILD)
	- test -d tmp && rm -rf tmp
	- find . -name CMakeCache.txt | xargs --no-run-if-empty rm -v
	- find . -name cmake_install.cmake | xargs --no-run-if-empty rm -v
	- find . -name CMakeFiles | xargs --no-run-if-empty rm -r
	- find . -name Makefile | xargs --no-run-if-empty rm -r
	- rm -r docs/zzipdoc/__pycache__
	- rm -r docs/zzipdoc/*.pyc
	- rm -r autom4te.cache
	- rm -r *.egg-info
	- rm *~
