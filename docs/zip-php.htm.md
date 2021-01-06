## PHP-ZIP Installation 

There have been many problems about the installation of the php-zip
module. Since Mid of 2006 the php-zip module does not require the
zziplib anymore - it uses its own implementation (which is a clean
approach in a double sense - there are no source code comments).
So, the following might possibly be only relevant for older
installations.

Chris Branch has been kind enough to jot down the points of a
successful php-zip installation sending it to me in May 2006.
I am quoting his text verbatim - again, I do not know whether
it works or not as I am not using any PHP for real work.

-----

* Software Packages
** Apache 2.4.21 (Linux)
** PHP 4.3.9 
** ZZIPLIB 0.10.82 
** Special requirement: static linking

* Setting up ZZIPLIB
**  Extract files from zziplib-0.10.82.tar.bz2 to a new folder. 
**  ./configure --enable-static 
**  make 
**  make install

* Rebuilding PHP to include ZIP support
** Modify PHP build file and add "--with-zip" 
  [no dir needed because default /usr/local on my machine]
** make 
** make install

* Modifying the Apache Installation
** Change to Apache source code directory 
** Change to "src" subdirectory and edit existing Makefile.  [-1-] \
   Add: EXTRA_LIBS=/usr/local/lib/libzzip.a 
** Change back to parent folder (cd ..) 
** make 
** /usr/local/etc/httpd/bin/apachectl stop 
** make install
** /usr/local/etc/httpd/bin/apachectl start

[-1-] **Note:** That step is the critical step that's not obvious.  Apparently,
when you build PHP as a static library and include the "--with-zip"
option, it creates a static library for PHP with an external dependency on
zziplib.a.  However, the Apache configure script and resulting Makefile
doesn't take this into account, so Apache won't link unless you hand-edit
the Apache Makefile.  (Maybe there's a better place to make this change so
that you don't have to re-fix Apache's Makefile each time you run Apache's
./configure.  However, I didn't spend the time to investigate that).
