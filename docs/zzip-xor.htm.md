<date> 15. July 2002 </date>

## ZIP Obfuscation 
Using obfuscations like XOR.

### The EXT/IO calls 

You really should read the section about the
  [EXT/IO feature](zzip-extio.html) of the zziplib since the
  obfuscation routines are built on top of it. In order to use obfuscation,
  you will generally need to use all the three additional argument that
  can be passsed to _open_ext_io functions. For the XOR-example, only one
  IO-handler is modified being the read()-call that will simply xor each
  data byte upon read with a specific value. It two advantages - doing an
  xor twice does yield the same data, so as a developer you do not have
  to wonder about the encryption/decryption pair, and it is a stateless
  obfuscation that does not need to know about the current position
  within the zip-datafile or zippedfile-datatream.

The examples provided just use a simple routine for xoring data that
  is defined in all the three of the example programs: 

```
static int xor_value = 0x55;
      static zzip_ssize_t xor_read (int f, void* p, zzip_size_t l)
      {
          zzip_size_t r = read(f, p, l);
	  zzip_size_t x;  char* q = p;
          for (x=0; x < r; x++) q[x] ^= xor_value;
          return r;
      }
```

and place this routine into the io-handlers after initializing
  the structure: 

```
zzip_init_io (&xor_handlers, 0); xor_handlers.read = &xor_read;
```

### The examples 

There are three example programs. The first one is
  [zzxorcopy.c](zzxorcopy.c) which actually is not a zziplib 
  based program. It just opens a file via stdio, loops through all data bytes 
  it can read thereby xor'ing it, and writes it out to the output file. A 
  call like `"zzxorcopy file.zip file.dat"` will
  create an obfuscated dat-file from a zip-file that has been possibly
  create with the normal infozip tools or any other archive program to
  generate a zip-file. The output dat-file is not recognized by normal
  zip-enabled apps - the filemagic is obfuscated too. This output
  dat-file however is subject to the other two example programs.

The [zzxordir.c](zzxordir.c) program will open such an obfuscated
  zip file and decode the central directory of that zip. Everything is
  still there in just the way it can be shown with the normal unzip
  programs and routines. And the [zzxorcat.c](zzxorcat.c) program 
  can extract data from this obfuscated zip - and print it un-obfuscated
  to the screen. These example programs can help you jumpstart with
  your own set of obfuscator routines, possibly more complex ones.

By the way, just compare those with their non-xor counterparts that
  you can find in [zzdir.c](zzdir.c) and 
  [zzxorcat.c](zzxorcat.c). Notice that the difference is
  in the setup part until the _open_ call after which one can just
  use the normal zzip_ routines on that obfuscated file. This is
  great for developing since you can start of with the magic-wrappers
  working on real-files then slowly turning to pack-files that hold
  most of the data and finally ending with a zip-only and obfuscated
  dat-file for your project.

<small><small>
<a href="copying.html">staticlinking?</a>
</small></small>
