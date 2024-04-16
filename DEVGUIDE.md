# DEVELOPMENT GUIDELINES

* workplace setup
* makefile targets
* release process

## WORKPLACE SETUP

Development can be done with a pure text editor and a terminal session.

### VSCode setup

Use python and mypy extensions for Visual Studio Code (from Microsoft).

* Control-P: "ext list"
  * look for "Python", "Pylance" (style checker), "Mypy Type Checker" (type checker)
  * optional "Makefile Tools"
  * and install the "CMake" tools
* Control-P: "ext install ms-python.mypy-type-checker"
  * this one pulls the latest mypy from the visualstudio marketplace
  * https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker

The make targets are defaulting to tests with python3.6 but the mypy plugin
for vscode requires atleast python3.8. All current Linux distros provide an
additional package with a higher version number, e.g "zypper install python311".
Be sure to also install "python311-mypy" or compile "pip3 install mypy". 
Implant the paths to those tools into the workspace settings = `.vscode/settings.json`

    {
        "mypy-type-checker.reportingScope": "workspace",
        "mypy-type-checker.interpreter": [
                "/usr/bin/python3.11"
        ],
        "mypy-type-checker.path": [
                "mypy-3.11"
        ],
        "mypy-type-checker.args": [
                "--strict",
                "--show-error-codes",
                "--show-error-context",
                "--no-warn-unused-ignores",
                "--ignore-missing-imports",
                "--exclude=build"
        ],
        "python.defaultInterpreterPath": "python3"
    }

The python files at the toplevel are not checked in vscode. I dont know why (yet).

### Makefile setup

Common distro packages are:
* `zypper install python3 python3-pip` # atleast python3.6
* `zypper install python3-wheel python3-twine`
* `zypper install python3-coverage python3-unittest-xml-reporting`
* `zypper install python3-mypy python3-mypy_extensions python3-typing_extensions`
* `zypper install python3-autopep8`
* `zypper install libsdl2-dev` # includes gcc and make tools
* `zypper install cmake` # should be installed with libsdl2 already
* `zypper install clang` # only for release checks with clang-format
* `zypper install ninja` # only for release checks wiht alternative cmake build
* `zypper install automake` # only for release checks of obsolete automake builds

For ubuntu you can check the latest Github workflows under
* `grep apt-get .github/workflows/*.yml`

## Makefile targets

### static code checking

* `make type`
* `make style`
* `make format` # if clang-format available

## compiling targets

* `make cmake` # does not compile manpages or testbins or downloads testzips
* `make build` # compiling the defaults for a release (autodetects SDL)
* `make ninja` # should be faster that makefile-build from `make build`
* `make nmake` # another cmake build variant
* `make docs`  # needs to run seperately sometimes
* `make am`    # if you want to run the obsolete automake build again

and the variants

* `make static`
* `make fortify`

### testing targets

Note that zziptests require some test-zips that are downloaded from the internet.
If you do not have direct access then run `make downloads` and carry the tmp.download
directory to the development host inside.

* `make check` # running zziptests.py 
* `make tests` # running testbuilds.py 
* `make install` and `make uninstalls`
* `make testmanpages`

### release targets

* `make version`
* `make build`
* consider running alternative cmake variants like ninja and nmake

Note that the `testbuilds.py` are currently comparing `make am` builds with cmake ones

## RELEASE PROCESS

* `make type`   # python mypy
* `make style`  # python style
* `make format` # cxx style
* `make check`
* `make version` # or `make version FOR=tomorrow`
* `make install` 
* `make uninstalls`
* `make build`
* `make docs` # includes `make mans`
* `make auto` # update automake variant
* `make am`   # remake with obsolete autotools
* consider running alternative cmake variants like ninja and nmake
* `make new check coverage` 
* update README.md with the result from coverage
* `git push` # if necessary
* wait for github workflows to be okay
* prepare a tmp.changes.txt 
* `git tag -F tmp.changes.txt v1.x` to the version in zziplib.spec
* `git push --tags`
* update the short description on github
* consider making a github release with the latest news

Currently there is a problem with the testzip downloads during "make check" on Github
`You have exceeded a secondary rate limit. Please wait a few minutes before you try again.`

## TODO

* there should be a coverage value for the cxx code
* there is a longer wishlist in `TODO` - it should be cleaned up
