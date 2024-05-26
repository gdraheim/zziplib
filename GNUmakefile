#! /usr/bin/gmake -fp

# the 'all' target is included from the 'configure'd Makefile

BUILDSOURCES=..
BUILD=build
CMAKE=cmake
NINJA=ninja
PREFIX=$$HOME/local
PYTHON3=python3
MINPYTHON=3.8

.PHONY: build docs bins test tests testbuilds

default: build

# defaults to 'cmake' (using gmake) but it can be 'ninja' as well
build:
	@ test -f Makefile || test -d $(BUILD) || (set -x ; mkdir $(BUILD) ; cd $(BUILD) && $(CMAKE) $(BUILDSOURCES) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) $(OPTIONS))
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/Makefile || (set -x ; cd $(BUILD) && $(MAKE) all)
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/rules.ninja || (set -x ; cd $(BUILD) && $(NINJA) all)
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/build.ninja || (set -x ; cd $(BUILD) && $(NINJA) all)
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/Makefile || echo 'DONE (cd $(BUILD) && $(MAKE) all) - please run (cd $(BUILD) && $(MAKE) check VERBOSE=1) now'
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/rules.ninja || echo 'DONE (cd $(BUILD) && $(NINJA) all) - please run (cd $(BUILD) && $(NINJA) check) now'
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/build.ninja || echo 'DONE (cd $(BUILD) && $(NINJA) all) - please run (cd $(BUILD) && $(NINJA) check) now'

static: ; rm -rf $(BUILD) && $(MAKE) build OPTIONS=-DBUILD_SHARED_LIBS=OFF
fortify: ; rm -rf $(BUILD) && $(MAKE) build "OPTIONS=-DFORTIFY=ON -DCMAKE_BUILD_TYPE=Debug"
cm new: ; rm -rf $(BUILD); $(MAKE) build "OPTIONS=-DCOVERAGE=ON -DCMAKE_BUILD_TYPE=Debug"

ninja: ; rm -rf $(BUILD) && $(MAKE) build OPTIONS=-GNinja
nmake: ; rm -rf $(BUILD) && $(MAKE) build OPTIONS=-GNmake
cmake: ; rm -rf $(BUILD) && $(MAKE) build "OPTIONS=-DZZIP_MANPAGES=OFF -DZZIP_INSTALL_BINS=OFF -DZZIP_TESTCVE=OFF"

cov coverage: libzzip.gcov libzzipmmapped.gcov libzzipfseeko.gcov
	@ for i in $?; do : \
	; cat $(BUILD)/zzip/$${i//.gcov/.so.gcov} | wc -l | sed -e "s|^|$(BUILD)/zzip/$${i//.gcov/.so.gcov}: |" -e "s/$$/ lines/" \
	; tail -1 $(BUILD)/zzip/$$i.txt | sed -e "s|^|$(BUILD)/zzip/$$i.txt: |" \
	; done
	@ grep "def test" test/zziptests.py | wc -l | sed -e "s|^|test/zziptests.py: |" -e "s/$$/ test cases/" 
libzzip.gcov libzzipmmapped.gcov libzzipfseeko.gcov:
	cd $(BUILD)/zzip && $(MAKE) $@
	tail -1 $(BUILD)/zzip/$@.txt

# targets defined in cmakefile.txt
check checks site install-site manpages htmpages:
	@ test ! -f $(BUILD)/Makefile    || (set -x; cd $(BUILD) && $(MAKE) $@ VERBOSE=1)
	@ test ! -f $(BUILD)/rules.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)
	@ test ! -f $(BUILD)/build.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)
install docs:
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

# testing

tests:  ; $(PYTHON3) testbuilds.py -vv
testss:  ; $(PYTHON3) testbuilds.py -vv --failfast --local
testbuilds: ; $(PYTHON3) testbuilds.py -vv --no-cache
k_%: ; $(PYTHON3) testbuilds.py $@ -vv --no-cache --keep
b_%: ; $(PYTHON3) testbuilds.py $@ -vv --no-cache --failfast --local
x_%: ; $(PYTHON3) testbuilds.py $@ -vv --no-cache --failfast --nonlocal
t_%: ;    cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv
test_%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py $@ -vv
est_%: ; cd $(BUILD)/test && $(PYTHON3) ../../test/zziptests.py t$@ -vv --keep

b: ; grep "def test_" testbuilds.py | sed -e "s/ *def test_/make b_/" -e "s/(self).*//"
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
	; sed -i -e "s:$$oldv:$$newv:" zziplib.spec testbuilds.py \
	; sed -i -e "s:$$oldv:$$newv:" */CMakeLists.txt \
	; sed -i -e "s:$$oldv:$$newv:" CMakeLists.txt \
	; git --no-pager diff -U0
checkversion versions:
	@ git --no-pager diff -U0

# format ..............................
CLANG_FORMAT=clang-format
format ff: ; $(CLANG_FORMAT) -i zzip/*.h zzip/*.c bins/*.h bins/*.c test/*.c

FORMATDIR=../zziplib-format
formatdir:
	rm -rf $(FORMATDIR); mkdir $(FORMATDIR)
	for i in zzip/*.h; do $(CLANG_FORMAT) "$$i" > "$(FORMATDIR)/$$(basename $$i)"; done
	for i in zzip/*.c; do $(CLANG_FORMAT) "$$i" > "$(FORMATDIR)/$$(basename $$i)"; done
	diff -qs zzip $(FORMATDIR) -x "*.am" -x "*.in" -x "*.wpj" -x "*.cmake" -x "*.sed" -x "*.txt"
diff: ; diff -U0 zzip $(FORMATDIR) -x "*.am" -x "*.in" -x "*.wpj" -x "*.cmake" -x "*.sed" -x "*.txt"
dif:  ; diff -u zzip $(FORMATDIR) -x "*.am" -x "*.in" -x "*.wpj" -x "*.cmake" -x "*.sed" -x "*.txt"

# style ...............................
mypy:
	zypper install -y mypy
	zypper install -y python3-click python3-pathspec

MYPY = mypy
MYPY_STRICT = --strict --show-error-codes --show-error-context --no-warn-unused-ignores --python-version $(MINPYTHON) --implicit-reexport
AUTOPEP8=autopep8
AUTOPEP8_INPLACE= --in-place
AUTOPEP8_ASDIFF= --diff

%.type:
	$(MYPY) $(MYPY_STRICT) $(MYPY_OPTIONS) $(@:.type=)

%.pep1:
	$(AUTOPEP8) $(AUTOPEP8_OPTIONS) $(@:.pep1=) $(AUTOPEP8_ASDIFF)

%.pep8:
	$(AUTOPEP8) $(AUTOPEP8_OPTIONS) $(@:.pep8=) $(AUTOPEP8_INPLACE)
	git --no-pager diff $(@:.pep8=)

PY1 = testbuilds.py
PY2 = test/zziptests.py
PY3 = docs/tools/md2dbk.py
PY4 = docs/toolstests.py
type:  ; $(MAKE) $(PY1).type $(PY2).type $(PY3).type $(PY4).type
style: ; $(MAKE) $(PY1).pep8 $(PY2).pep8 $(PY3).pep8 $(PY4).pep8
pep1:  ; $(MAKE) $(PY1).pep1 $(PY2).pep1 $(PY3).pep1 $(PY4).pep1

py4: ; $(MAKE) $(PY4).type $(PY4).pep8
py3: ; $(MAKE) $(PY3).type $(PY3).pep8
py2: ; $(MAKE) $(PY2).type $(PY2).pep8
py1: ; $(MAKE) $(PY1).type $(PY1).pep8

# extras ..............................
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
	- rm *~
