<date> 2004 </date>

## FAQ 
(non)frequently asked questions

> While using the zziplib some people come up with questions and
> problems that need a little longer to be explained. So here is
> a list of these notes for your information. Keep it up.

* [extended ascii characters in names of zipped files ](#latin-1)
* [unicode support for names of zipped files ](#utf-8)
* [timestamps of zipped files ](#timestamps)
* [installation instructions ](#install)
* [php zip module installation ](#php)
* [commercial support ](#license)

[latin-1]:

#### zziplib does not support extended ascii characaters, winzip does

  That's somehow incorrect - the ascii range is the 7bit lower plane of
  an 8bit character encoding. The upper plane had been non-standard for
  decades including the age when the ZIP file format was invented. The
  first instances of pkware's zip compressor were used on DOS with a 
  codepage 437 which has a way different encoding for the upper plane
  than today's latin-1 encoding which in fact used in **all**
  modern operating systems. So what really see is a mismatch of 
  character encodings that you are used to.

  Even more than that the character encoding had never been specified
  at all for the filenames in the central directory part. An alert
  reader will however recognize that **each** file entry does
  also have version-info field telling about the compressor that did
  create the file entry. That version-info has an upper byte telling
  about the host OS being in use while packaging. A heavy-weight
  zip decoder might use that value to infer the character encoding
  on the host OS (while compressing), to detect a mismatch to the
  current OS (while decompressing), and going to re-code the filename
  accordingly.

  Even more than that the zip file format has seen various extensions
  over time that have found their place in an extra info block. There
  are info blocks telling more about the filename / codeset. However
  the zziplib library does not even attempt to decode a single extra
  info block as zziplib is originally meant to be a light-weight library.
  However one might want to put a layer on top of the structure decoding 
  of zziplib that does the necessary detection of character encodings and
  re-coding of name entries. Such a layer has not been written so far.

[utf-8]:

#### zziplib does not support any unicode plane for filenames :

  The pkware's appnote.text has an extra info block (id-8) for the
  unicode name of the file entry but it was never actually being 
  used AFAICS. This might be related to the current developments of
  older systems to drop usage of latin-1 encoding in the upper plane
  of 8bit characters and instead choosing the multibyte encoding
  according to UTF-8. This is again highly system specific.

  Basically, you would need to instruct the compressor to use 
  UTF-8 encoding for the file-entries to arrive at a zip archive 
  with filenames in that specific character encoding. Along with
  this zip archive one can switch the application into utf-8 usage
  as well and take advantage of filename matches in that encoding.
  This will make it so there is not mismatch in character encoding
  and implicit re-coding being needed.

[timestamps]:

#### zziplib does not return stat values for file timestamps :

  That's correct and again a re-coding problem. The original
  timestamp in each file entry is in DOS format (i.e. old-FAT).
  The stat value is usually expected to be in POSIX format. The
  win32 API has an extra function for conversion but none of the
  unix compatibles has one, so it would be needed to ship a
  conversion function along with zziplib.

  However the zziplib is intended to be light-weight system and
  used largely for packaging data for an application. There it
  is not used strictly as a variant of Virtual File System (vfs)
  that would need to map any information from the zip file system
  to native host system. Of course applications are free to cut
  out the DOS file timestamp and re-code it on their own. It's
  ust that zziplib does not provide that re-coding originally.

[install]:

#### how can one install the zziplib package

  The zziplib project is opensource which effectly gives two ways of
  installing the package: one can download the source archive and use
  a C compiler to derive a binary executable for whatever computer
  it needs to be on (see the platform compatibility list). This is
  the preferred way but for convenience one can download a binary
  installation archive with precompiled executables.

  The current project uses autoconf/automake for cross platform
  support which includes most unix compatible systems and their
  native C compilers. The derivates of the GNU C compiler (gcc) have 
  replaced most of these native C compilers in the past years. The
  <a href="http://www.mingw.org">mingw32</a> project has ported a
  unix born C compiler to win32 and zziplib can be compiled with
  it for the various win32 platforms.

  There exist some C compilers which can not be embedded easily into 
  a unix compilation framework. The zziplib source archive ships with
  project files for MSVC6 and MSVC6 (Microsoft Visual C). Adapting
  these project files might help with installation problems of the
  DLL hell on win32 platforms. There exist no sufficient guidelines to
  mix binary helper libraries for many applications on windows.

  There exists win32 binary archives as zip files on the download area
  of zziplib (MSI is always on my wishlist). Including the project as
  a helper library however you should not use it but instead compile
  from source. The general library installation on unix are better, 
  the zziplib download area contains regularly some linux binary
  archives (rpm). Many vendors of unix compatible systems provide 
  precompiled binary packages of zziplib on their own.

[php]:

#### after installing zziplib the php zip module still does not work

  Now that is one of <b>the most</b> frequently asked questions that
  I do receive. There is just one major problem with it: I did not
  write the php zip module (which uses zziplib) and I have no idea
  how php modules work or how to tell apache's php sandbox to make
  it work. Really, I do not have the slightest clue on that.

  I was posting to some php developer sites to spread awareness of
  the fact and hopefully to find a guy that I could forward any
  questions on the php zip module installation. But so far there is
  nothing, it merily seems that such installation problems are in no
  way related to zziplib anyway but exists <b>with any other module with a 
  third party library dependency</b> as well. So the answers on php forum 
  sites will ask for details of the current php and apache configuration.

  Since I do not run a php zip whatever nor any other php stuff, it's
  just that those hints were not quite helpful to me. It would be really 
  really great if someone with a php zip background could be so nice to
  write a short roundup of the areas to check when a php zip module
  installation fails, so that I could post it here. Where are you?
  Yours desperatly...&nbsp;;-)

[license]:

#### how to obtain a license and support contract for a commercial project

  The zziplib has been created as a spare time project and it is put
  under a very easy free public license. Even for commercial projects
  there is hardly any need to negotiate a separate license since the
  restrictions of the GNU LGPL or MPL can be matched easily. As a
  general hint, if the zziplib is shipped unmodified with your project
  then you are right within the limits of the free public license.

  Sometimes the question for a personal license comes up for very
  different reason - the need for a support contract and/or the setting
  of functionality guarantees. The free public licenses include a safeguard
  clause to that end, "in the hope that it will be useful,
  but <em>without any warranty</em>; without even the implied warranty of
  <em>merchantability</em> or <em>fitness for a particular purpose</em>."
  Since the project was developed as a spare time project however there
  have never been personal licenses going beyond.

  In general you can still try to negotiate a support contract but it
  will be very costly. It is much more profitable for you to tell one
  of your developers to have a look at the source code and ensure the
  required functionality is there, with hands on. The source code is 
  written to be very readable, maintainable and extensible. Just be
  reminded that the free public licenses have restrictions on shipping
  modified binaries but I can give you a cheap personal license to
  escape these. (Such licenses can be obtained in return for tax-deductible
  donations to organisations supporting opensource software).

... and as always - ** Patches are welcome ** -
