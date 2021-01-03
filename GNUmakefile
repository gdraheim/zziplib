#! /usr/bin/gmake -f

# the 'all' target is included from the 'configure'd Makefile

BUILDSOURCES=..
BUILD=build
CMAKE=cmake
NINJA=ninja
PREFIX=$$HOME/local

.PHONY: build docs bins test

default: build
build:
	@ test -f Makefile || test -d $(BUILD) || (set -x ; mkdir $(BUILD) ; cd $(BUILD) && $(CMAKE) $(BUILDSOURCES) -DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) $(OPTIONS))
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/Makefile || (set -x ; cd $(BUILD) && $(MAKE) all)
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/rules.ninja || (set -x ; cd $(BUILD) && $(NINJA) all)
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/Makefile || echo 'DONE (cd $(BUILD) && $(MAKE) all) - please run (cd $(BUILD) && $(MAKE) check VERBOSE=1) now'
	@ test -f Makefile || test ! -d $(BUILD) || test ! -f $(BUILD)/rules.ninja || echo 'DONE (cd $(BUILD) && $(NINJA) all) - please run (cd $(BUILD) && $(NINJA) check) now'

new: ; rm -rf $(BUILD); $(MAKE) build

ninja: ; rm -rf $(BUILD) && $(MAKE) build OPTIONS=-GNinja
nmake: ; rm -rf $(BUILD) && $(MAKE) build OPTIONS=-GNmake
cmake: ; rm -rf $(BUILD) && $(MAKE) build "OPTIONS=-DZZIP_MANPAGES=OFF -DZZIP_INSTALL_BINS=OFF -DZZIP_TESTCVE=OFF"

check checks:
	@ test ! -f $(BUILD)/Makefile    || (set -x; cd $(BUILD) && $(MAKE) $@ VERBOSE=1)
	@ test ! -f $(BUILD)/rules.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)
install docs:
	@ test ! -f $(BUILD)/Make        || (set -x; cd $(BUILD) && $(MAKE) $@)
	@ test ! -f $(BUILD)/rules.ninja || (set -x; cd $(BUILD) && $(NINJA) $@)

un uninstalls:
	@ case "$(PREFIX)" in */local) echo rm -rf "'$(PREFIX)'" ; rm -rf "$(PREFIX)" ;; *) echo skipped rm -rf "'$(PREFIX)'" ;; esac

st_%: ; python3 testbuilds.py te$@ -vv
tests:  ; python3 testbuilds.py -vv
test_%: ; cd build/test && python3 ../../test/zziptests.py $@ -vv

downloads:
	- rm -rf test/tmp.download build/test/tmp.download
	cd build/test && python3 ../../test/zziptests.py --downloadonly -vv

version:
	oldv=`sed -e '/zziplib.VERSION/!d' -e 's:.*zziplib.VERSION."::' -e 's:".*::' CMakeLists.txt` \
	; oldr=`echo $$oldv | sed -e 's:.*[.]::'` ; newr=`expr $$oldr + 1` \
	; newv=`echo $$oldv | sed -e "s:[.]$$oldr\$$:.$$newr:"` \
	; echo "$$oldv -> $$newv" \
	; sed -i -e "s:$$oldv:$$newv:" zziplib.spec testbuilds.py \
	; sed -i -e "s:$$oldv:$$newv:" */CMakeLists.txt \
	; sed -i -e "s:$$oldv:$$newv:" CMakeLists.txt \
	; git diff -U0
