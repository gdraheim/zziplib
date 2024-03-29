<date> 15. July 2002 </date>

## ZZIP Future 
What next to come.

<!--border -->

### ZIP-Write 

Anybody out there who wants to program the write-support for the
zziplib? Actually, I just do not have the time to do it and no
real need to but I guess it would be nice for people as for
example to spit out savegame files in zipformat. The actual
programming path is almost obvious - start off with the zziplib
as it is, and let it open an existing zip-file. This will parse
the central directory into memory - including the file-offsets
for each file. Then, truncate the zip-realfile to the place that
the central-dir was found (identical with the end of the last
file). If a datafile is opened for writing, either add a new
entry or modify the start-offset of the existing entry to the
end of the zip-realfile - the old data is simply junk. Then
init zlib to do the deflation of the data and append it to the
current zip-realfile. When the zipdir-handle is getting closed
from write-mode, the zip's central-directory needs to be appended
to the file on disk. This coincides with creating a new zip-file 
with an empty central-directory that can be spit out to disk.
During development, do not care about creating temp-files to
guard against corruption for partial writes - the usual application
will use the zziplib to create zip savegames in one turn, no
"update"-operation needs to be implemented like exists in the
standalone zip command utilities.

### readdir for subdir inside zip magicdir 

See the notes in the first paragraphs of [
  ZZIP Programmers Interface](zzip-api.html) description. It would add some
  complexity for something I never needed so far. The question
  came up with using zziplib as the backend of a dynamic webserver
  to store the content in compressed form possibly through the
  incarnation of a php module - and some scripted functionality
  that walks all directories to index the files hosted. I'm not
  going to implement that myself but perhaps someone else wants
  to do it and send me patches for free.

### obfuscation example project 

A subproject that shows **all** the steps from a dat-tree
  to a dat-zip to an obfuscated-dat along with build-files and
  source-files for all helper tools needed to obfuscate and
  deobfuscate, plus a sample program to use the obfuscated 
  dat-file and make some use of it. Along with some extra 
  documentation about 20..40 hours. Don't underestimate the
  amount of work for it! (otherwise a great student project).

### zip/unzip tool 

The infozip tools implement a full set of zip/unzip routines
based on internal code to access the zip-format. The zziplib
has its own set of zip-format routines. Still, it should be
possible to write a frontend to the library that implements 
parts (if not all) of the options of the infozip zip/unzip 
tools. Even without write-support in zziplib it would be
interesting to see an normal unzip-tool that does not use
the magic-wrappers thereby only going off at plain zip-files.
On the upside, such a tool would be smaller than the infozip
tools since it can use the library routines that are shared
with other tools as well. Again - don't underestimate the
amount of work for it, I guess 40..80 hours as there is a lot
of fine-tuning needed to match the infozip model.
