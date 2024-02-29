<date> 20. July 2002 </date>

## ZZIP Programmers Interface 
The complete API description.

  The zzip library was originally developed by Tomi Ollila as a
  set of zip decoder routines. Guido Draheim did pick it up and
  wrapped them under a call synopsis matching their posix
  api calls. Therefore `zzip_open()` has the same 
  synopsis as `open(2)` but it can open zipped files.
  Later the distinction was made between magic wrappers and apis
  for direct access to zip archives and the files contained
  in the archive. 

These (three) functional apis have little helper functions 
alongside including those to get the posix filehandle out of a 
zzip handle and to get some attributes about the data handle
represented by a zzip handle. Plus checking for error codes
that may have been generated from internal checks.

<dl>
<dt> <a href="zzip-basics.html">Basics</a> </dt>
<dd> Magic Wrappers, Zip Archive Dir access, Zipped File access </dd>
<dt> <a href="zzip-extras.html">Extras</a> </dt>
<dd> ext/io init, StdC calls, Error defs, ReOpen, FileStat </dd>
</dl>
