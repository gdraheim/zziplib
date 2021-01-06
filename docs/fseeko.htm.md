<date> 2005 </date>

## zzip/fseeko 
zip access for stdio handle

  These routines are fully independent from the traditional zzip
  implementation. They assume a readonly seekable stdio handle
  representing a complete zip file. The functions show how to 
  parse the structure, find files and return a decoded bytestream.

### stdio disk handle 

  Other than with the [mmapped](mmapped.html) alternative
  interface there is no need to build special handle for the zip
  disk file. The normal stdio file handle (of type **`FILE`**)
  serves as the disk access representation. You can open that stdio file
  handle any way you want. Note however that the `zzipfseeko` 
  routines modify the access state of that file handle, especially the
  read position.

  To get access to a zipped file, you need a zip archive entry known 
  under the type `ZZIP_ENTRY`. This is again modelled after
  the `DIR_ENTRY` type in being a representation of a file
  name inside the zip central directory. To get a fresh zzip entry, use
  `zzip_entry_findfirst`, to get the next use 
  `zzip_entry_findnext`, and do not forget to free the
  resource with `zzip_entry_free`.

```
extern ZZIP_ENTRY* zzip_entry_findfirst(FILE* disk);
   extern ZZIP_ENTRY* zzip_entry_findnext(ZZIP_ENTRY*  entry);
   extern int         zzip_entry_free(ZZIP_ENTRY* entry);
```

  These three calls will allow to walk all zip archive members in the
  order listed in the zip central directory. To actually implement a
  directory lister ("zzipdir"), you need to get the name string of the
  zzip entry. This is not just a pointer: the zzip disk entry is not
  null terminated actually. Therefore we have a helper function that
  will `strdup` the entry name as a normal C string:

```
#include <zzip/fseeko.h>
  void _zzip_dir(FILE* disk)
  {
      for (ZZIP_ENTRY* entry = zzip_findfirst (disk);
           entry ; entry = zzip_findnext (entry)) {
          char* name = zzip_entry_strdup_name (entry);
          puts (name); free (name);
      }
  }
```

### find a zipped file 

The central directory walk can be used to find any file in the
  zip archive. The `zzipfseeko` library however provides
  two convenience functions that allow to jump directly to the
  zip disk entry of a given name or pattern. You are free to use
  the newly allocated `ZZIP_ENTRY` for later calls on
  that handle type. Do not forget to `zzip_entry_free` 
  the handle unless the handle is consumed by a routine, e.g. 
  `zzip_entry_findnext` to hit the end of directory.

```
  extern ZZIP_ENTRY* zzip_entry_findfile(FILE* disk, char* filename, 
                                         ZZIP_ENTRY* _zzip_restrict entry, 
                                         zzip_strcmp_fn_t compare);

  extern ZZIP_ENTRY* zzip_entry_findmatch(FILE* disk, char* filespec, 
                                         ZZIP_ENTRY* _zzip_restrict entry,
                                         zzip_fnmatch_fn_t compare, int flags);
```

In general only the first two arguments are non-null pointing to the
  stdio disk handle and the file name to look for. The "entry" argument
  is an old value and allows you to walk the zip directory similar to
  `zzip_entry_findnext` but actually leaping forward. The
  compare function can be used for alternate match behavior: the default
  of `strcmp` might be changed to `strncmp` for
  a caseless match. The "flags" of the second call are forwarded to the
  posix `fnmatch` which we use as the default function.

If you do know a specific filename then you can just use 
  `zzip_entry_findfile` and supply the return value to
  `zzip_entry_fopen` with the second argument set to "1"
  to tell the function to actually consume whichever entry was given.
  That allows you to skip an explicit `zzip_entry_free` 
  as it is included in a later `zzip_entry_fclose`.

```
  #include <zzip/fseeko.h>

       /* zzipfseeko already exports this convenience function: */
  ZZIP_ENTRY_FILE* zzip_entry_ffile(FILE* disk, char* filename) {
      return zzip_entry_fopen (zzip_entry_findfile (filename, 0, 0), 1);
  }

  int _zzip_read(FILE* disk, char* filename, void* buffer, int bytes)
  {
      ZZIP_ENTRY_FILE* file = zzip_entry_ffile (disk, filename);
      if (! file) return -1;
      int bytes = zzip_entry_fread (buffer, 1, bytes, file);
      zzip_entry_fclose (file);
      return bytes;
  }
```

### reading bytes 

The example has shown already how to read some bytes off the head of
  a zipped file. In general the zzipfseeko api is used to replace a few
  stdio routines that access a file. For that purpose we provide three 
  functions that look very similar to the stdio functions of 
  `fopen()`, `fread()` and `fclose()`.
  These work on an active file descriptor of type `ZZIP_ENTRY_FILE`.
  Note that this `zzip_entry_fopen()` uses `ZZIP_ENTRY` 
  argument as returned by the findfile api. To open a new reader handle from 
  a disk archive and file name you can use the `zzip_entry_ffile()` 
  convenience call.

```
ZZIP_ENTRY_FILE* zzip_entry_ffile  (FILE* disk, char* filename);
   ZZIP_ENTRY_FILE* zzip_entry_fopen  (ZZIP_ENTRY* entry, int takeover);
   zzip_size_t      zzip_entry_fread  (void* ptr, 
                                       zzip_size_t sized, zzip_size_t nmemb,
                                       ZZIP_ENTRY_FILE* file);
   int              zzip_entry_fclose (ZZIP_ENTRY_FILE* file);
   int              zzip_entry_feof   (ZZIP_ENTRY_FILE* file);
```

In all of the examples you need to remember that you provide a single
  stdio `FILE` descriptor which is in reality a virtual
  filesystem on its own. Per default filenames are matched case
  sensitive also on win32 systems. The findnext function will walk all
  files on the zip virtual filesystem table and return a name entry 
  with the full pathname, i.e. including any directory names to the
  root of the zip disk `FILE`.

### ZZIP_ENTRY inspection 

The `ZZIP_ENTRY_FILE` is a special file descriptor handle 
  of the `zzipfseeko` library - but the `ZZIP_ENTRY`  
  is not so special. It is actually a bytewise copy of the data inside the
  zip disk archive (plus some internal hints appended). While 
  `zzip/fseeko.h` will not reveal the structure on its own, 
  you can include `zzip/format.h` to get access to the actual 
  structure content of a `ZZIP_ENTRY` by (up)casting it to  \
  **`struct zzip_disk_entry`**.

In reality however it is not a good idea to actually read the bytes
  in the `zzip_disk_entry` structure unless you seriously know
  the internals of a zip archive entry. That includes any byteswapping
  needed on bigendian platforms. Instead you want to take advantage of
  helper macros defined in `zzip/fetch.h`. These will take
  care to convert any struct data member to the host native format.

```
extern uint16_t    zzip_disk_entry_get_flags( zzip_disk_entry* entry);
extern uint16_t    zzip_disk_entry_get_compr( zzip_disk_entry* entry);
extern uint32_t    zzip_disk_entry_get_crc32( zzip_disk_entry* entry);

extern zzip_size_t zzip_disk_entry_csize( zzip_disk_entry* entry);
extern zzip_size_t zzip_disk_entry_usize( zzip_disk_entry* entry);
extern zzip_size_t zzip_disk_entry_namlen( zzip_disk_entry* entry);
extern zzip_size_t zzip_disk_entry_extras( zzip_disk_entry* entry);
extern zzip_size_t zzip_disk_entry_comment( zzip_disk_entry* entry);
extern int         zzip_disk_entry_diskstart( zzip_disk_entry* entry);
extern int         zzip_disk_entry_filetype( zzip_disk_entry* entry);
extern int         zzip_disk_entry_filemode( zzip_disk_entry* entry);

extern zzip_off_t  zzip_disk_entry_fileoffset( zzip_disk_entry* entry);
extern zzip_size_t zzip_disk_entry_sizeof_tail( zzip_disk_entry* entry);
extern zzip_size_t zzip_disk_entry_sizeto_end( zzip_disk_entry* entry);
extern char*       zzip_disk_entry_skipto_end( zzip_disk_entry* entry);
```
