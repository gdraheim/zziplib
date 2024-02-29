<date> 2005 </date>

## zzip/mmapped 
zip access for mmapped views

> These routines are fully independent from the traditional zzip
> implementation. They assume a readonly mmapped sharedmem block
> representing a complete zip file. The functions show how to 
> parse the structure, find files and return a decoded bytestream.

### zzip disk handle 

Other than with the [fseeko](fseeko.html) alternative
  interface there is no need to have an actual disk handle to the
  zip archive. Instead you can use a bytewise copy of a file or
  even use a mmapped view of a file. This is generally the fastest
  way to get to the data contained in a zipped file. All it requires
  is enough of virtual memory space but a desktop computer with a
  a modern operating system will easily take care of that.

The zzipmmapped library provides a number of calls to create a
  disk handle representing a zip archive in virtual memory. Per
  default we use the sys/mmap.h (or MappedView) functionality
  of the operating system. The `zzip_disk_open` will
  open a system file descriptor and try to `zzip_disk_mmap`  
  the complete zip content. When finished with the zip archive
  call `zzip_disk_close` to release the mapped view
  and all management data.

```
ZZIP_DISK*  zzip_disk_open(char* filename);
  int         zzip_disk_close(ZZIP_DISK* disk);

  ZZIP_DISK*  zzip_disk_new(void);
  ZZIP_DISK*  zzip_disk_mmap(int fd);
  int         zzip_disk_munmap(ZZIP_DISK* disk);
  int         zzip_disk_init(ZZIP_DISK* disk, 
                            char* buffer, zzip_size_t buflen);
```

### reading the central directory 

To get access to a zipped file, you need a pointer to an entry in the
  mmapped zip disk known  under the type `ZZIP_DISK_ENTRY`. 
  This is again modelled after the `DIR_ENTRY` type in being 
  a representation of a file name inside the zip central directory. To 
  get an initial zzip disk entry pointer, use `zzip_disk_findfirst`,
  to move the pointer to the next entry use `zzip_disk_findnext`.

```
extern ZZIP_ENTRY* zzip_disk_findfirst(FILE* disk);
   extern ZZIP_ENTRY* zzip_disk_findnext(ZZIP_ENTRY*  entry);
```

These two calls will allow to walk all zip archive members in the
  order listed in the zip central directory. To actually implement a
  directory lister ("zzipdir"), you need to get the name string of the
  zzip entry. This is not just a pointer: the zzip disk entry is not
  null terminated actually. Therefore we have a helper function that
  will `strdup` the entry name as a normal C string:

```
  #include <zzip/mmapped.h>
  void _zzip_dir(char* filename)
  {
      ZZIP_DISK* disk = zzip_disk_open (filename);
      if (! disk) return disk;
      for (ZZIP_DISK_ENTRY* entry = zzip_disk_findfirst (disk);
           entry ; entry = zzip_disk_findnext (entry)) {
          char* name = zzip_disk_entry_strdup_name (entry);
          puts (name); free (name);
      }
  }
```

### find a zipped file 

The central directory walk can be used to find any file in the
  zip archive. The `zzipfseeko` library however provides
  two convenience functions that allow to jump directly to the
  zip disk entry of a given name or pattern. You are free to use
  the returned `ZZIP_DISK_ENTRY` pointer for later calls
  that type. There is no need to free this pointer as it is really
  a pointer into the mmapped area of the `ZZIP_DISK`.
  But do not forget to free that one via `zzip_disk_close`.

```
ZZIP_DISK_ENTRY* zzip_disk_findfile(ZZIP_DISK* disk, char* filename, 
                                      ZZIP_DISK_ENTRY* after, 
                                      zzip_strcmp_fn_t compare);

  ZZIP_DISK_ENTRY* zzip_disk_findmatch(ZZIP_DISK* disk, char* filespec, 
                                       ZZIP_ENTRY* after,
                                       zzip_fnmatch_fn_t compare, int flags);
```

In general only the first two arguments are non-null pointing to the
  zip disk handle and the file name to look for. The "after" argument
  is an old value and allows you to walk the zip directory similar to
  `zzip_disk_entry_findnext` but actually leaping forward. The
  compare function can be used for alternate match behavior: the default
  of `strcmp` might be changed to `strncmp` for
  a caseless match. The "flags" of the second call are forwarded to the
  posix `fnmatch` which we use as the default function.

If you do know a specific zzipped filename then you can just use 
  `zzip_disk_entry_findfile` and supply the return value to
  `zzip_disk_entry_fopen`. There is a convenience function 
  `zzip_disk_fopen` that will do just that and therefore
  only requires a disk handle and a filename to find-n-open.

```
  #include <zzip/mmapped.h>

  int _zzip_read(ZZIP_DISK* disk, char* filename, void* buffer, int bytes)
  {
      ZZIP_DISK_FILE* file = zzip_disk_fopen (disk, filename);
      if (! file) return -1;
      int bytes = zzip_disk_fread (buffer, 1, bytes, file);
      zzip_disk_fclose (file);
      return bytes;
  }
```

### reading bytes 

The example has shown already how to read some bytes off the head of
  a zipped file. In general the zzipmmapped api is used to replace a few
  system file routines that access a file. For that purpose we provide three 
  functions that look very similar to the stdio functions of 
  `fopen()`, `fread()` and `fclose()`.
  These work on an active file descriptor of type `ZZIP_DISK_FILE`.

```
ZZIP_DISK_FILE* zzip_disk_entry_fopen  (ZZIP_DISK* disk, 
                                           ZZIP_DISK_ENTRY* entry);
   ZZIP_DISK_FILE* zzip_disk_fopen  (ZZIP_DISK* disk, char* filename);
   zzip_size_t     zzip_disk_fread  (void* ptr, 
                                     zzip_size_t sized, zzip_size_t nmemb,
                                     ZZIP_DISK_FILE* file);
   int             zzip_disk_fclose (ZZIP_DISK_FILE* file);
   int             zzip_disk_feof   (ZZIP_DISK_FILE* file);
```

In all of the examples you need to remember that you provide a single
  `ZZIP_DISK` descriptor for a memory block which is in reality 
  a virtual filesystem on its own. Per default filenames are matched case
  sensitive also on win32 systems. The findnext function will walk all
  files on the zip virtual filesystem table and return a name entry 
  with the full pathname, i.e. including any directory names to the
  root of the zip disk `FILE`.

### ZZIP_DISK_ENTRY inspection 

The `ZZIP_DISK_FILE` is a special file descriptor handle 
  of the `zzipmmapped` library - but the 
  `ZZIP_DISK_ENTRY` is not so special. It is actually a pointer
  directly into the zip central directory managed by `ZZIP_DISK`.
  While `zzip/mmapped.h` will not reveal the structure on its own, 
  you can include `zzip/format.h` to get access to the actual 
  structure content of a `ZZIP_DISK_ENTRY` by its definition  \
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

Additionally the `zzipmmapped` library has two additional
  functions that can convert a mmapped disk entry to (a) the local
  file header of a compressed file and (b) the start of the data area
  of the compressed file. These are used internally upon opening of
  a disk entry but they may be useful too for direct inspection of the
  zip data area in special applications.

```
char*  zzip_disk_entry_to_data(ZZIP_DISK* disk, 
                                 struct zzip_disk_entry* entry);
  struct zzip_file_header*  
         zzip_disk_entry_to_file_header(ZZIP_DISK* disk, 
                                 struct zzip_disk_entry* entry);
```
