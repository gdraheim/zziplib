[date]: # February 2003

## Configuration 
of other projects using zziplib

If using the zziplib with other project then you can use a number
of possibility to configure and link. The zziplib had been usually
included within the projects that made use of it - some did even
pick up the advantage to be allowed to staticlink in a limited
set of conditions. Recently however, the zziplib is shipped as a
standard library of various linux/freebsd distros - mostly for
the usage by the php-zip module. This allows third party software
makers to link to the preinstalled library in the system and
consequently reduce the memory consumption - even more than now
with the zziplib being a lightweight anyway (the i386 .so is 
usually less than 20k)

### pkg-config --libs 

Within modern software development, one should be advised to use
pkg-config as soon as it is available. The pkg-config helper can
handle a lot of problems that can usually come up with linking
to third party libraries in case that those link again dynamically
with other libraries themselves. It does correctly order the
list of "libs", it can throw away duplicate "-L" hints, and same
for cflags "-I" hints, plus it will throw away some sys-includes
that gcc3.2 will warn about with a false positive.

There is a number of pkg-config targets installed in the system
but the one you want to use is **pkg-config zziplib**. 
Therefore, a simple Makefile could read like

```
PROGRAM = my_prog
    CFLAGS = -Dhappy `pkg-config zziplib --cflags`
    LIBS   = -Wl,-E  `pkg-config zziplib --libs`

    my_prog.o : my_prog.c
       $(CC) $(CFLAGS) $< -o $@
    my_prog : my_prog.o
       $(LINK) $< $(LIBS)
```

The `pkg-config zziplibs --libs` will usually expand to 
something like `-lzzip -lz` which are the
two (!!) libraries that you need to link with - in that
order. The zziplib builds on top of the z-lib algorithms
for compression of files within the zip-archive. That's
the same for other lib-parts of the zziplib project as
well, e.g. the sdl-rwops part which does also need to
link with the sdl-lib - and that's where the pkg-config
infrastructure can be of great help. That's the reason
why zziplib installs a few more ".pc" files, you can
get a list of them like this:

```
$ pkg-config --list-all | sort | grep zzip
   zziplib               zziplib - ZZipLib - libZ-based ZIP-access Library
   zzip-sdl-config       zzip-sdl-config - SDL Config (for ZZipLib)
   zzip-sdl-rwops        zzip-sdl-rwops - SDL_rwops for ZZipLib
   zzipwrap              zzipwrap - Callback Wrappers for ZZipLib
   zzip-zlib-config      zzip-zlib-config - ZLib Config (for ZZipLib)
```

The two entries like "zzip-sdl-config" and "zzip-zlib-config"
happen to be ".pc" files for the libz.so and libSDL.so that
were seen at configure-time of zziplib - you may want to reuse
these in your projects as well whenever you need to link to
either of zlib or libsdl even in places where there is no direct
need for zziplib. It basically looks like:

```
$ pkg-config zzip-zlib-config --modversion
   1.1.4
   $ pkg-config zzip-zlib-config --libs      
    -lz
```

### zzip-config 

The pkg-config ".pc" files are relatively young in the history of
zziplib. A long time before that there was the `zzip-config`
script installed in the system. These `*-config` were common
before the pkg-config came about, and in fact the pkg-config
infrastructure was invented to flatten away the problems of
using multiple `*-config` scripts for a project. As long as you
do not combine multiple `*-config`s then it should be well okay
to use the `zzip-config` directly - it does also kill another
dependency on the `pkg-config` tool to build your project, the
zziplib is all that's needed.

In its call-structure the `zzip-config` script uses the same
options as `pkg-config`, (well they are historic cousins anyway).
and that simply means you can replace each call above like
`pkg-config zziplib...` with `zzip-config...`.

```
PROGRAM = my_prog
    CFLAGS = -Dhappy `zzip-config --cflags`
    LIBS   = -Wl,-E  `zzip-config --libs`

    my_prog.o : my_prog.c
       $(CC) $(CFLAGS) $< -o $@
    my_prog : my_prog.o
       $(LINK) $< $(LIBS)
```

Be informed that the zzip-config script is low-maintained and
starting with 2004 it will be replaced with a one-line script 
that simply reads `pkg-config zziplib $*`. By that time the
rpm/deb packages will also list "pkgconfig" as a dependency
on the zziplib-devel/zziplib-dev part.

### autoconf macro 

There is currently an autoconf macro installed along into
the usual /usr/share/aclocal space for making it easier for
you to pick up the configure-time cflags/libs needed to
build/link with zziplib. In any way it does look like
this:

```
dnl PKG_CHECK_ZZIPLIB(ZSTUFF, min-version, action-if, action-not)
  AC_DEFUN([PKG_CHECK_ZZIPLIB],[dnl
  PKG_CHECK_MODULES([$1], [zziplib $2], [$3], [$4])])
```

You are strongly advised to take advantage of the pkgconfig's
macro directly - you can find the macro in
`/usr/share/aclocal/pkg.m4` and it allows to
combine the flags of a list of library modules that you
want to have. If it is only zziplib, than you could simply
use this in your configure.ac:

```
 PKG_CHECK_MODULES([ZZIP],[zziplib >= 0.10.75])
```

which will provide you with two autoconf/automake variables
named **`ZZIP_CFLAGS`** and **`ZZIP_LIBS`** respectively.

Up to 2004, the macro in zziplib.m4 will be however carry
a copy of the pkg.m4 so that you do not need another
dependency for your software project. The macro is called
like shown above PKG_CHECK_ZZIPLIB and you would call it
like `PKG_CHECK_ZZIPLIB([ZZIP],[0.10.75])`  
which will give you the two autoconf/automake variables
as well,  `ZZIP_CFLAGS` and `ZZIP_LIBS`
