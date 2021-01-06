<date>created 1.Jun.2000, last updated 25.Apr.2002 </date>

## History and Links 
plus Installation and Contact Hints

### A Bit Of History 

You'll find [gzip](http://www.gzip.org) using the same compression 
that was written by Jean-loup [Gailly](http://gailly.net)for the [Info-Zip](http://www.info-zip.org) Group
whose [Zip](http://www.info-zip.org/pub/infozip/Zip.html)program is compatible with msdos PKZIP program from [PK&nbsp;Ware](http://www.pkware.com). Then, in collaboration
with [Mark Adler](http://www.alumni.caltech.edu/~madler)he wrote the [zlib](http://www.gzip.org/zlib)compression library which was later standardized in the [
zlib RFCs](ftp://ftp.uu.net/graphics/png/documents/zlib/zdoc-index.html), namely[RFC 1950](http://www.ietf.org/rfc/rfc1950.txt)[
zlib&nbsp;3.3](ftp://ftp.uu.net/graphics/png/documents/zlib/rfc-zlib.html.Z),[RFC 1951](http://www.ietf.org/rfc/rfc1951.txt)[
deflate&nbsp;1.3](ftp://ftp.uu.net/graphics/png/documents/zlib/rfc-deflate.html.Z) and[RFC 1952](http://www.ietf.org/rfc/rfc1952.txt)[
gzip&nbsp;4.3](ftp://ftp.uu.net/graphics/png/documents/zlib/rfc-gzip.html). The free algorithm can be found in lots of places
today including PPP packet compression and PNG picture compression.

### Installation 

The installation is from the source .tar.gz tarball does follow
 the simple gnu style: type `''configure  && make install''` 
 in the unpacked directory. This will actually perform the usual 
 sequence of `''configure && make && make install''`. The
 use of `''make rpm''` will make rpms based on your system
 setup, and using a decent mingw32 compiler (e.g. the crossgcc
 from [libsdl.org/Xmingw32](http://libsdl.org/Xmingw32))
 will allow you to create windows dlls using a gnu development
 environment. MSVC and Borland support (Make-)files should be
 easy to be derived from the [Makefile.am](Makefile.am)

### Contact 

The library was developed by 
 [
 Guido Draheim ](mailto:guidod@gmx.de?subject=zziplib) based on the library 
 [`zip08x`](http://freshmeat.net/appindex/1999/08/02/933593367.html) 
 by [ Tomi Ollila ](mailto:too@iki.fi) (many thanks
 for his support of the zziplib project). He has provided 
 a good deal of testing rounds and very helpful comments. 
 It may be assumed that this library supersedes 
 [`zip08x`](http://www.iki.fi/too/sw/zip08x.readme), and in April 2002, he 
 has even given up copyright restrictions coming from zip08x
 and changed the [zip08x](http://www.iki.fi/too/sw/zip08x.readme) 
 readme to point to [zziplib](http://zziplib.sf.net).
 Anyone who wants to contribute in accessing zip-archives
 with the zlib-library is hereby kindly invited to send us
 comments and sourcecode.

### Links 

The [zziplib library](zziplib.html) must be
linked with the free **[zlib](http://www.gzip.org/zlib/)**
[[1]](http://www.info-zip.org/pub/infozip/zlib)
[[2]](http://www.lifl.fr/PRIVATE/Manuals/gnulang/zlib)
[[3]](http://pobox.com/~newt) package originally developed 
by the [Info-Zip](http://www.info-zip.org) Group
and now maintained at the [GZip](http://www.gzip.org) Group.
As of late, the pkware appnote.txt has been revised into a whitepaper
document named[
    "APPNOTE.TXT - .ZIP File Format Specification"](http://www.pkware.com/products/enterprise/white_papers/appnote.html).
Be also aware of other zzip like projects, e.g. [zipios++](http://zipios.sourceforge.net) that
mangles zip access into C++ iostream facilities.
