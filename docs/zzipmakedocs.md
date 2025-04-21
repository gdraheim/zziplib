# zzipmakedocs

## background

The ZZipLib had been embedding documentation into the C source code from the beginning.
For some time a tool `cpp2markdown` was extracting the parts, based on the pygments lexer.
From there the markdown parts were compiled into a docbook `<references>` xml master.
And with the `xmlto` docbook processor the dozens of troff `man.3` pages and `html`
parts were written.

However the `xmlto` docbook processor turned out to be quite unstable, with the results
being not very readable. So a tool `dbk2man` was created to generate the troff pages.
The `cpp2markdown` turned out to be not very configurable, so it was replaced by
a `zzipdoc` transformer that got the function references better and it does not
anymore depend on the pygments lexer.

The `zziplib/docs` are now compiling the source `*.c` input with a tool `zzipmakedocs` that 
generates the intermediate docook.xml format. And `dbk2man` turns that into dozens of
files in subdirectories `man3` or `html` which get packaged as tarball for installation.

As it can be helpful for others, the documentation generator is packaged as pypi tool
as well. The sources for that are still in the `zziplib` project.

## running

* `zzipmakedocs *.py ../zzip/*.c --package MyLibrary --release 0.1 --output mydocbook`
  * there is also a `--onlymainheader mylib.h` option that only scans c-files having that include
* `dbk2man.py man mydocbook.xml -o man3`
  * generates troff format files into subdirectory man3 (arguments similar to xmlto)
* `dbk2man.py html mydocbook.xml -o html`
  * generates html format files into subdirectory html (arguments similar to xmlto)

Using the `--onlymainheader` the zziplib build rules generate the documentation for
three libraries instead of just one. That's because there is a main library and
two derivates that are smaller but sharing the same internal helper functions.

