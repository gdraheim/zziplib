<date> February 2003 </date>

## SFX-Make 
 combining an EXE with a ZIP archive

### How To 

In this section we walk you through the steps of combining an EXE
  with a ZIP archive. The basic scheme goes like this: the final
  file will have an EXE starting at offset null, followed by the
  data entries of a ZIP archive. The *last* part of the ZIP 
  archive is the ZIP central-directory which ends at the end of the file.

The basic problem lies in the fact that the zip central-directory
entries reference their data section with an offset from the 
start-of-file so that you can not just append a zip archive after 
an exe stub. The trick goes like adding the EXE as the first data
part of the ZIP archive - so that the offsets for each entry will
be correct when we are finished with it.

Again, one can not just use a zip tool to put the EXE as the first
part - since each data part is preceded with an infoblock of a 
few bytes. The data of the first data part will therefore not
start at offset zero. We solve this problem with moving the data
a few bytes later - so that the final file will not start with a
"PK" magic (from the zip info header) but with an "MZ" or "ELF"
magic (from the exe info header).

### Step 1: Creating The Zip Combination 

Choose your exe file (example.exe) and wrap that file into a
  zip container - ensure that the zip tool does *not*  
  use any compression algorithm on the data. This is usually
  done with saying "zero compression level" as an option to
  the zip tool. Also note that *no other* file is
  wrapped as some zip tools reorder the entries from the 
  order on the command line to alphabetic order. Here is an
  example with infozip's `zip` (e.g. on linux):

```
zip -0 -j example.zip example.exe
```

There is no zip tool that would reorder the data entries in
  an existing zip archive. This mode is used here - the real
  compressed data entries can now be added to the existing
  zip archive that currently just wraps the exe part. With
  specifying maximum compression ("-9" = compression level 9) 
  and throwing away any subdirectory part ("-j" = junk path)
  it might look like

```
zip -9 -j example.zip data/*
```

Now we need to move the exe part by a few bytes to the
  real start of the file. This can be done as easily as
  writing the exe file again on to the start of the file.
  However, one can not just use a shell-direction or
  copy-operation since that would truncate (!!) the zip
  file to the length of the exe part. The overwrite-operation
  must be done without truncation. For maximum OS independence
  the zziplib ships with a little tool in "test/zzipsetstub.c"
  that you can reuse for this task:

```
zzipsetstub example.zip example.exe
```

This is it - the `unzip` tool can still access all data
entries but the first EXE - the first EXE will be listed
in the central-directory of the ZIP archive but one can
not extract the data since the "PK" magic at offset null
has been overwritten with the EXE magic. The data of all
the other entries can still be extracted with a normal
`unzip` tool - or any tool from the zziplib be used for
the same task.

### Step 2: Accessing The Data From The Program 

There is an example in test/zzipself.c that show how to do
it. The OS will provide each program with its own name in
argv[0] of the main() routine. This program file (!!) is
also the zip archive that carries the compressed data
entries along. Therefore, we can just issue a zzip_opendir
on argv[0] to access the zip central-directory.

Likewise one can open a file within it by just prepending
  the string argv[0] to the filename stem, i.e. you could
  do like 

```
ZZIP_FILE* f = zzip_fopen ("example.exe/start.gif", "rbi")
```

however you are advised to use the _ext_io cousin to be
platform independet - different Operating Systems use
different file extensions for executables, it's not always
an ".exe".

Once the file is opened, the data can be zzip_fread or
passed through an SDL_rwops structure into the inner
parts of your program.

### Step 3: Using Obfuscation Along 

The next level uses obfuscatation on the data part of the
application. That way there is no visible data to be seen
from outside, it looks like it had been compiled right into
the C source part. One can furthermore confuse a possible
attacker with staticlinking the zziplib into the executable
(this is possible in a limited set of conditions).

The first pass is again in creating the zip - here we must
  ensure that only the ZIP archive part is obfuscated but
  the EXE part must be plain data so that the operationg 
  system can read and relocate it into main memory. Using
  xor-obfuscation this is easy - applying xor twice will
  yield the original data. The steps look like this now:

```
zzipxorcopy example.exe example.xor
    zip -0 application.zip example.xor
    zip -9 application.zip data/*
    zzipsetstub application.zip example.xor
    zzipxorcopy application.zip application.exe
```

In the second step the open-routine in your application
  needs to be modified - there are quite some examples in
  the zziplib that show you how to add an xor-read routine
  and passing it in the "io"-part of an zzip_open_ext_io
  routine (see zzipxorcat.c).

```
static int xor_value = 0x55;

   static zzip_ssize_t xor_read (int f, void* p, zzip_size_t l)
   {
       zzip_ssize_t r = read(f, p, l);
       zzip_ssize_t x; char* q; for (x=0, q=p; x < r; x++) q[x] ^= xor_value;
       return r;
   }

   static struct zzip_plugin_io xor_handlers;
   static zzip_strings_t xor_fileext[] = { ".exe", ".EXE", "", 0 };
   
   main(...)
   {
       zzip_init_io (&xor_handlers, 0); xor_handlers.read = &xor_read;
  
       ZZIP_FILE*  fp = zzip_open_ext_io (filename, 
                             O_RDONLY|O_BINARY, ZZIP_CASELESS|ZZIP_ONLYZIP,
                             xor_fileext, &xor_handlers);
      ....
```

You may want to pick your own xor-value instead of the default 0x55,
the zziplib-shipped tool `zzipxorcopy` does know an option to just
set the xor-value with which to obfuscate the data.
