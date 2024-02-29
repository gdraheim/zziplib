<date> 1. June 2000 </date>

## ZIP File Access 
Using Zipped Files Transparently 

### The Typedef

The typedef `ZZIP_FILE` can serve as a replacement 
 for a normal file descriptor. As long as it is only used
 for reading a file, the zzlib-user can actually replace
 the posix functions `open/read/close` 
 by their counterparts from the 
 [zziplib library](zziplib.html):
 `zzip_open/zzip_read/zzip_close`.

As long as the filename path given to `zzip_open` 
 refers to a real file in the filesystem, it will almost
 directly forward the call to the respective posix `open` 
 call. The returned file descriptor is then stored in
 a member-variable of the `ZZIP_FILE` structure.

Any subsequent calls to `zzip_read` will then
 be forwarded to the posix `read` call on the
 memorized file descriptor. The same about `zzip_close` 
 which will call the posix `close` function and then
 `free` the `ZZIP_FILE` structure.

The real benefit of the 
 [zziplib library](zziplib.html) 
 comes about when the filename argument does actually refer
 to a file that is zipped in a zip-archive. It happens that
 even both a real file and a zipped file can live under the
 same pathname given to the `zzip_open` call,
 whereas the real file is used in preference.

### Zipped File

Suppose you have subdirectory called '`test/`'. In
 this directory is just one file, called '`README`'.
 Calling the `zzip_open` function with an
 argument of '*optional-path/*`test/README`',
 then it will open that file for subsequent reading with
 `zzip_read`. In this case the real (*stat'able*)
 file is opened.

Now you can go to the '`test/`' directory and zip up
 the files in there by calling 
 `zip ../test.zip *`.
 After this, you can delete the '`test/`' directory and
 the call to `zzip_open` will still succeed.
 The reason is that the part of the path saying 
 '`test/README`' will be replaced by sth. like 
 '`test.zip:README`' - that is the real file '`test.zip`'
 is opened and searched for a contained file '`README`'.

Calling `zzip_read` on the zipped '`README`' file
 will return the very same data as if it is a real file in a
 real directory. If the zipped file is compressed it will be 
 decompressed on the fly.

### Zip Directory

The same applies to the use of `opendir/readdir/closedir` 
which can safely be replaced with their counterparts from the
 [zziplib library](zziplib.html) - again their prototype
 follows the scheme of the original calls, just prepend `zzip_` 
 to the function calls and `ZZIP_` to the struct-typedefs.

To call `zzip_opendir` on a real directory will then
 return a `ZZIP_DIR` whose member-variable 
 `realdir` points to the actual `DIR`-structure
 returned by the underlying posix `opendir`-call.

If a real directory '`test`' does not exist, then the
 `zzip_opendir` will try to open a file '`test.zip`'
 with a call to `zzip_dir_open`.
 Subsequent calls to `zzip_readdir` will then return
 information as being obtained from the central archive directory
 of the zip-file.

### Differences

There are no differences between the posix calls and their counterparts
 from the      [zziplib library](zziplib.html) - well, just
 as long as the zip-file contains just the plain files from a directory.

If the zip-file contains directory entries you may be prompted with
 some awkward behaviour, since in zip-file a directory happens to be
 just an empty file. Note that the posix function `open` 
 may also open a directory for reading - it will only return 
 `EISDIR` if the `open` mode-argument included
 write-access.

What the current of version of the 
 [zziplib library](zziplib.html) 
 can definitely not do: calling zzip_opendir on a directory zippend
 *inside* a zip-file.

To prevent the enrollment of directories into the zip-archive, you
 can use the `-D` option of the `zip` program. That
 is in any `Makefile` you may want to use
 `cd $(dir) && zip -D ../$(dir).zip *`.

### Advantages

Distribution of a set of files is much easier if it just means
 to wrap up a group of files into a zip-archive - and copy that
 zip-archive to the respective destination directory.
 Even more the files can be compressed and unlike a `tar.gz` 
 archive there is no need to decompress the archive in temporary
 location before accessing a member-file.

On the other hand, there is no chance to scatter files around
 on the disk like it could easily happen with a set of gzip'ed
 man-pages in a single `man`-directory. The reader
 application does not specifically need to know that the file
 is compressed, so that reading a script like 
 `share/guile/x.x.x/ice-9/popen.scm` is done by simple
 calls to `zzip_read` which works on zip-file named
 `share/guile/x.x.x/ice-9.zip`.

A version mismatch between different files in a group is now
 obvious: either the opened file belongs to the distribution
 archive, or otherwise in resides in a real directory **just
 next to the zip-archive that contains the original**.

### Issues

The  [zziplib library](zziplib.html) does not
 use any code piece from the `zip` programs, neither
 *pkzip* nor *infozip*, so there is no license
 issue here. The decompression is done by using the free
 [zlib library](http://www.gzip.org/zlib) which has no special
 issues with respect to licensing. 
 The  rights to the [zziplib library](zziplib.html) 
 are reserved to the copyright holders, there is a public
 license that puts most the sources themselves under 
 [the GNU Lesser General Public License](COPYING.LIB),
 so that the use of a shared library instance of the
 [zziplib library](zziplib.html) 
 has no restrictions of interest to application programmers.
 For more details and hints about static linking, check
 the [COPYING](copying.html) information.

The only issue you have with the
 [zziplib library](zziplib.html) 
 is the fact that you can only *read* the contained files.
 Writing/Compression is not implemented. Even more, a compressed
 file is not seekable at the moment although I hope that someone
 will stand up to implement that functionality someday.
