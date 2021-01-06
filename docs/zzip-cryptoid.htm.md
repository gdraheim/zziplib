<date> 11. May 2004 </date>

## ZIP Ext Encryption 
ext/io used for cryptoid plugins

### Stronger Obfuscation For ZZip 

Some people feel that a simple bytewise xor is not strong enough
  as an obfuscation for the data. There we have the question how to
  implant a stronger obfuscation routine to protect that data of an
  application from artwork theft. Perhaps there is even the idea to
  use an obfuscation in the range of a real crypt routine - in which
  case I want to recommend strongly to read the 
  [ reasoning page ](zzip-crypt.html) why it can not be
  real encryption and that the resulting obfuscation has an upper 
  limit being *lower* than the crypt routine complexity.

After reminding you of this fact we can go at evaluationg how to
implant a stronger obfusction routine to protect your data. The
ext/io feature uses a callback routine "read" that must read a
block of the given size - for the obfuscation case it will call
the "read()" function of the underlying operation system, and
the obfuscated block will be deobfuscated before returning it to
the caller.

In this mechanism there is not asseration at which file-offset
the ext/io-read() callback is triggered. That is the reason we
have shown obfuscation with bytewise xor-key example - formally
this is using obfuscation blocks of 8bit width being aligned
on 8bit boundaries in the data file, and our decryption stream
is stateless being the same for each obfuscation block (of 8bit
width). 

In order for a stronger obfuscation we have to break those 
 limitations which are directly derived from the natural way
 of the handling of files by a contemporary operating system.
 This is triggered as the call synopsis of the ext/io read()
 callback matches *exactly* the one of posix, so that
 one can use the posix read() function reference as the default
 for ensuring the most minimal overhead in accessing non-obfuscated 
 zip files.   

<small>And btw, the abbreviation "posix" stands for 
   "Portable Open System in Unix".</small>

The trick we show here: the first argument of the ext/io read
callback is the file descriptor of the underlying operationg
system. While we can not add another argument to the ext/io
read call we can pick up additional information with the help
of that file descriptor id being globally unique even across
multiple threads. One solution would make the application map
that descriptor id to a special argument but this is often too
much overhead: the current file position is enough. 

The current file position is managed by the operation system
 via the file descriptor table. There is a function call to
 map a file descriptor to the current read position offset
 usually named "tell(fd)". Since this call is not mandated by
 posix, you can emulate it with the posix lseek() call which
 returns the resulting offset after the operation was performed,
 so we just seek by a zero offset: \
`#define tell(fd) lseek(fd,0,SEEK_CUR)`

That file offset is measured from the start of the zip archive,
not per each zipped file. Remind yourself of that fact when
creating your own "zzobfuscate.exe" which should work on the
zip archive and not per file before zipping. That is a difference
over normal zip archives where the user can atleast recognized the
dat file as a zip archive and see a list of files contained in the 
archive, atleast their names and data start offset.

Now, let's use the file read offset to break the blocking
limitations of 8bit/8bit to a larger xor-key. In our example
we expand to a 32bit/32bit xor-key giving a search space of
4 billion keys instead of the just 256 keys in 8bit blocking.
That is simply done by a static 4 byte xor-key sequence and using
modulo operations for alignment. For the 2^X cases any modulo
operations shrink to a set of ultra-fast bitwise-and operations.

```
static char xor_value[4] = { 0x55, 0x63, 0x27, 0x31 };
      static zzip_ssize_t xor_read (int f, void* p, zzip_size_t l)
      {
          zzip_off_t  y = tell(f);
          zzip_size_t r = read(f, p, l);
	  zzip_size_t x;  char* q = p;
          for (x=0; x < r; x++) q[x] ^= xor_value[(y+x)&3];
          return r;
      }
```
