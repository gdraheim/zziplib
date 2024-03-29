<date> 17. December 2002 </date>

## ZIP Format 
About Zip Parsing Internals...

### ZIP Trailer Block 

The general ZIP file format is written sequentially - each file
being added gets a local file header and its inflated data. When
all files are written then a central directory is written - and
this central directory may even span multiple disks. And each
disk gets a descriptor block that contains a pointer to the start
of the central directory. This descriptor is always written last
and therefore we call it the "ZIP File Trailer Block".

Okay, so we know that this ZIP Trailer is always at the end of a zip
  file and that is has a fixed length, and a magic four-byte value at
  its block start. That should make it easy to detect zip files but in
  the real world it is not that easy - it is allowed to add a zip
  archive comment text *after* the Trailer block. It's rarely
  used these days but it turns out that a zip reader must be ready
  to search for the Trailer block starting at the end of the file
  and looking upwards for the Trailer magic (it's "PK\\5\\6" btw).

Now that's what the internal function __zip_find_disk_trailer is
used for. It's somewhat optimized as we try to use mmap features
of the underlying operating system. The returned structure is 
called zzip_disk_trailer in the library source code, and we only
need two values actually: u_rootseek and u_rootsize. The first of
these can be used to lseek to the place of the central directory
and the second value tells us the byte size of the central directory.

### ZIP Central Directory 

So here we are at the central directory. The disk trailer did also
tell us how many entries are there but it is not that easy to read
them. Each directory entry (zzip_root_dirent type) has again a
magic value up front followed by a few items but they all have some
dos format - consider the timestamps, and atleast size/seek values 
are in intel byteorder. So we might want to parse them into a format
that is easier to handle in internal code.

That is also needed for another reason - there are three items in that 
directory entry being size values of three variadic fields following
right after the directory. That's right, three of these. The first
variadic field is the filename of this directory entry. In other
words, the root directory entry does not contain a seek value of
where the filename starts off, the start of the filename is 
implicitly given with the end address of the directory entry.

The size value for the filename does simply say how long the
filename is - however, and more importantly, it allows us to 
compute the start of the next variadic field, called the extra
info field. Well, we do not need any value from that extra info
block (it has unix filemode bits when packed under unix) but we
can be quite sure that this field is not null either. And that
was the second variadic field.

There is a third variadic field however - it's the comment field.
That was pretty heavily used in the good old DOS days. We are not
used to it anymore since filenames are generally self-descriptive
today but in the DOS days a filename was 8+3 chars maximum - and
it was in the comment field that told users what's in there. It
turned out that many software archives used zip format for just
that purpose as their primary distribution format - for being 
able to attach a comment line with each entry.

Now, these three variadic fields have each an entry in the 
directory entry header telling of their size. And after these
three variadic fields the next directory entry follows right in.
Yes, again there is no seek value here - we have to take the sum
of the three field sizes and add that to the end address of the
directory entry - just to be able to get to the next entry.

### Internal Directory 

Now, the external ZIP format is too complicated. We cut it down
to the bare minimum we actually need. The fields in the entry
are parsed into a format directly usable, and from the variadic
fields we only keep the filename. Oh, and we ensure that the
filename gets a trailing null byte, so it can surely be passed
down into libc routines.

There is another trick by the way - we use the u_rootsize value
to malloc a block for the internal directory. That ensures the
internal root directory entries are in nearby locations, and
including the filenames themselves which we put in between the
dirent entries. That's not only similar to the external directory
format, but when calling readdir and looking for a matching
filename of an zzip_open call, this will ensure the memory is
fetched in a linear fashion. Modern cpu architectures are able
to burst through it.

One might think to use a more complicated internal directory
format - like hash tables or something. However, they all suffer
from the fact that memory access patterns will be somewhat random
which eats a lot of speed. It is hardly predictable under what
circumstances it gets us a benefit, but the problem is certainly
not off-world: there are zzip archives with 13k+ entries. In a real
filesystem people will not put 13k files into one directory, of 
course - but for the zip central directory all entries are listed
in parallel with their subdirectory paths attached. So, if the
original subtree had a number of directories, they'll end up in
parallel in the zip's central directory.

### File Entry 

The zip directory entry has one value that is called z_off in the
zziplib sources - it's the seek value to the start of the actual
file data, or more correctly it points to the "local file header".
Each file data block is preceded/followed with a little frame.
There is not much interesting information in these framing blocks, 
the values are duplicates of the ones found in the zip central
directory - however, we must skip the local file header (and a
possible duplicate of filename and extrainfo) to arrive at the
actual file data.

When the start of the actual file data, we can finally read data.
The zziplib library does only know about two choices defined by 
the value in the z_compr field - a value of "0" means "stored"
and data has been stored in uncompresed format, so that we can
just copy it out of the file to the application buffer.

A value of "8" means "deflated", and here we initialize the zlib
and every file data is decompressed before copying it to the
application buffer. Care must be taken here since zlib input data
and decompressed data may differ significantly. The zlib compression
will not even obey byte boundaries - a single bit may expand to
hundreds of bytes. That's why each ZZIP_FILE has a decompression
buffer attached.

All the other z_compr values are only of historical meaning,
the infozip unix tools will only create deflated content, and
the same applies to pkzip 2.x tools. If there would be any other
value than "0" or "8" then zziplib can not decompress it, simple
as that.

### ZZIP_DIR / ZZIP_FILE 

The ZZIP_DIR internal structures stores a posix handle to the
zip file, and a pointer to the parsed central directory block.
One can use readdir/rewinddir to walk each entry in the central
directory and compare with the filenames attached. And that's
what will be done at a zzip_open call to find the file entry.

There are a few more fields in the ZZIP_DIR structure, where 
most of these are related to the use of this struct as a
shared recource. You can use zzip_file_open to walk the 
preparsed central directory and return a new ZZIP_FILE handle
for that entry.

That ZZIP_FILE handle contains a back pointer its ZZIP_DIR
that it was made from - and the back pointer also serves as flag
that the ZZIP_FILE handle points to a file within a ZIP file as
opposed to wrapping a real file in the real directory tree.
Each ZZIP_FILE will increment a shared counter, so that the
next dir_close will be deferred until all ZZIP_FILE have been
destroyed.

Another optmization is the cache-pointer in the ZZIP_DIR. It is
quite common to read data entries sequentially, as that the
zip directory is scanned for files matching a specific pattern,
and when a match is seen, that file is openened. However, each
ZZIP_FILE needs a decompression buffer, and we keep a cache of
the last one freed so that it can be picked up right away for the
next zzip_file_open.

Note that using multiple zzip_open() directly, each will open
and parse a zip directory of its own. That's bloat both in
terms of memory consumption and execution speed. One should try
to take advantage of the feature that multiple ZZIP_FILE's can
share a common ZZIP_DIR with a common preparsed copy of the
zip's central directory. That can be done directly with using
zzip_file_open to use a ZZIP_DIR as a factory for ZZIP_FILE,
but also zzip_freopen can be used to reuse the old internal
central directory, instead of parsing it again.

And while zzip_freopen would release the old ZZIP_FILE handle
only resuing the ZZIP_DIR attached, one can use another routine
directly called zzip_open_shared that will create a ZZIP_FILE
from an existing ZZIP_FILE. Oh, and not need to worry about 
problems when a filepath given to zzip_freopen() happens to
be in another place, another directory, another zip archive.
In that case, the old zzip's internal directory is freed and
the others directory read - the preparsed central directory
is only used if that is actually possible.
