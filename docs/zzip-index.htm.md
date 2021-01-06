<date> created 1.Jun.2000, last updated 09.Feb.2003 </date>

## The Library 
Overview

The [zziplib library](zziplib.html) is intentionally
 lightweight, it offers the ability to easily extract data from 
 files archived in a single zip file. Applications can bundle
 files into a single zip archive and access them.
 The implementation is based only on the (free) subset of 
 compression with the [zlib algorithm](http://www.gzip.org/zlib) 
 which is actually used by the `zip/unzip` tools.

The library allows reading zip archives in a number of ways,

* archive mode: \
  reading the zip directory and extracting files from it.
  This is the traditional mode as seen with unzip-utilities.
  Some extra unzip-utiles for transparent/magic mode are 
  shipped as well.
* replacement mode: \
  Use ZZIP_FILE / ZZIP_DIR pointers provided by zziplib and
  put them to work with routines originally developed to
  work with real directories and file handles. The API calls
  do follow traditional synopsis from posix/stdio.
* transparent mode: \
  Use replacement handles and allow the open()-calls to 
  automatically detect when a file is contained in a zip 
  archive or when it is a real file in the file system.
  A filepath can be partly in a real filesystem and partly
  within the zip archive when one is seen.
* ext magic: \
  Use the same filepath to access either a zipped or real
  file - it looks for a real file and there is none then
  every subdirectory of the path is checked, a ".zip"
  extension appended, and the zipped file transparently
  opened. This can speed up dat-file development 
  dramatically.
* io/xor magic: \
  The access to the filesystem can be hooked up - examples
  are given for xor obfuscation which is great for game
  artwork and AI data. A small intro for SDLrwops usage is
  given as well.

