<date> 1. June 2000 </date>

## ZIP Access 
Accessing Zip Archives with ZLib Decompression

### The Library 

The [zziplib library](zziplib.html) offers users the
 ability to easily extract data from files archived in a single
 zip file. This way, programs that use many "read-only" files from
 a program specific source directory can have a single zip
 archive

This library offers only a (free) subset of compression methods
 provided in a full implementation but that is well enough. The
 idea here is that `zip/unzip` utilities can be used
 to create archives that will later be read by using this library.
 Yet those programmes (or a library with their functionality)
 is not needed in that final operation.

### Using A Zip-File 

Before a file in the zip-archive is accessed, the application
 must first get a handle to the central directory contained in the
 zip-file. This is achieved by calling
 [ zzip_dir_open ](zziplib.html#zzip_dir_open)
 or 
 [ zzip_dir_fdopen ](zziplib.html#zzip_dir_fdopen).
 The directory entries in the zip-archives can be obtained
 with
 [ zzip_dir_read ](zziplib.html#zzip_dir_read).
 After being done, the zip-dir handle should be closed with
 [ zzip_dir_close ](zziplib.html#zzip_dir_close).

```
ZZIP_DIR* dir = zzip_dir_open("test.zip",0);
 if (dir) {
   ZZIP_DIRENT dirent;
   if (zzip_dir_read(dir,&dirent) {
     /* show info for first file */
     print("%s %i/%i", dirent.d_name, dirent.d_csize, dirent.st_size);
   }
   zzip_dir_close(dir);
 }
```

From the zip-dir handle a compressed file can be opened
 for reading. This is achieved by using 
 [ zzip_file_open ](zziplib.html#zzip_file_open) 
 and providing it with the dir-handle and a name of the file.
 The function
 [ zzip_file_read ](zziplib.html#zzip_file_read) 
 is used to get pieces of uncompressed data from the file, and
 the file-handle should be closed with
 [ zzip_file_close ](zziplib.html#zzip_file_close)

```
ZZIP_FILE* fp = zzip_file_open(dir,"README",0);
 if (fp) {
   char buf[10];
   zzip_ssize_t len = zzip_file_read(fp, buf, 10);
   if (len) {
     /* show head of README */
     write(1, buf, len); 
   }
   zzip_file_close(fp);
 }
```

### Magic Zipped Files 

There is actually no need to directly use the zip-centric functions
 as described above. Instead there are magic replacements for the
 posix calls `open/read/close` and 
 `opendir/readdir/closedir`. The prototypes of these
 functions had been the guideline for the design of their magic
 counterparts of the
 [zziplib library](zziplib.html).

The magic functions are described in a separated document on
 [ Using Zipped Files ](zzip-file.html). In general,
 the functions have a prefix `zzip_` and their argument
 types have a prefix `ZZIP_` where appropriate. Calls
 to the magic functions and the direct functions above can
 be mixed as long as the magic functions have not been opening
 a real file.

To detect a real file (or directory), the info functions
 [ zzip_file_real ](zziplib.html#zzip_file_real)
 and
 [ zzip_dir_real ](zziplib.html#zzip_dir_real)
 can be used.
 If these return a true value, the standard posix functions
 are more appropriate. The posix handles can be obtained with
 a call to
 [ zzip_realdir ](zziplib.html#zzip_realdir) and
 [ zzip_realfd ](zziplib.html#zzip_realfd) respectively.

### Errors & Infos 

There are a set of error and info functions available. To handle
 error conditions specific to the
 [zziplib library](zziplib.html) 
 there are these functions:
 [ zzip_error ](zziplib.html#zzip_error),
 [ zzip_seterror ](zziplib.html#zzip_seterror) 
 and their string representations with
 [ zzip_strerror ](zziplib.html#zzip_strerror),
 [ zzip_strerror_of ](zziplib.html#zzip_strerror_of).
 The magic functions will map any of these specific library
 error conditions to the more generic system `errno` 
 codes with
 [ zzip_errno ](zziplib.html#zzip_errno).

More information on stream can be obtained with
 [ zzip_dir_stat ](zziplib.html#zzip_dir_stat) and
 [ zzip_dirhandle. ](zziplib.html#zzip_dirhandle) 
 The latter is used to obtain the dir-handle that every zipped file 
 handle has even if not explicitly opened.

The usage of many functions are shown in the example programs
 that come along with the
 [zziplib library](zziplib.html). See the files
 [ zzcat.c ](zzcat.c) and
 [ zzdir.c ](zzdir.c). The 
 [ zziptest.c ](zziptest.c) program needs the
 private header file 
 [ zzip.h ](zzip.h) whereas the library installer
 will only copy the public include file 
 [ zziplib.h ](zziplib.h) to your system's
 `include` directory.
