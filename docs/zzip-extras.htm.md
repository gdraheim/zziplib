<date> 20. July 2002 </date>

## ZZIP API extras 
The check/init API description.

### Extras 

The next requests circulated around other file-extensions to 
automagically look inside filetypes that have zip-format too but 
carry other fileextensions - most famous might be the ".PK3"
files of ID's Quake game. There have been a number of these
requests and in a lot of cases it dawned to me that those guys
may have overlooked the zzip_dir_open functions to travel
through documents of zipformat under any name - that is that the
"magic" was not actually needed but they just wanted to read
files in zipformat with the zziplib.

Other requests circulated around encryption but I did reject
those bluntly, always. Instead there have been always examples
for doing some obfuscation around the zip-format so that the
stock zip/unzip tools do not recognize them but a game
software developer can pack/unpack his AI scripts and bitmaps
into such a zipformat-like file.

After some dead-end patches (being shipped along with the
  zziplib as configure-time compile-options - greetings to
  Lutz Sammer and Andreas Schiffler), the general approach 
  of _ext_io came up, and finally implemented (greetings go
  to Mike Nordell). The _open()-calls do now each have a
  cousin of _open_ext_io() with two/three additional arguments
  being a set of extensions to loop through our magic testing,
  a callback-handler plugin-table for obfuscation-means, 
  and (often) a bit-mask for extra-options - this bitmask even
  has "PREFERZIP" and "ONLYZIP" options to skip the real-file
  test magic in those `zzip_*open` functions.

<table cellpadding="10" width="100%"><tr><td><table border="1" width="100%">
<tr><td width="50%"> zzip_open(name,flags) </td>
<td width="50%"> zzip_open_ext_io(name,flags,mode,ext,io) </td></tr>
<tr><td width="50%"> zzip_opendir(name) </td>
<td width="50%"> zzip_opendir_ext_io(name,mode,ext,io) </td></tr>
<tr><td width="50%"> zzip_dir_open(name,errp) </td>
<td width="50%"> zzip_dir_open_ext_io(name,errp,ext,io) </td></tr>
<tr><td width="50%"> zzip_dir_fdopen(fd,errp) </td>
<td width="50%"> zzip_dir_fdopen_ext_io(fd,errp,ext,io) </td></tr>
<tr><td width="50%"> zzip_file_open(dir,name,mode) </td>
<td width="50%"> zzip_file_open_ext_io(dir,name,mode,ext,io) </td></tr>
</table></td></tr></table>

Oh, and note that the mode,ext,io extras are memorized 
  in the respecitive ZZIP_DIR handle attached, so each
  of the other calls like `zzip_file_open()`
  and `zzip_read()` will be using them. There
  are a few helper routines to help setup a new io-plugin
  where the init_io will currently just memcopy the
  default_io entries into the user-supplied plugin-struct.

<table cellpadding="10" width="100%"><tr><td><table border="1" width="100%">
<tr><td width="50%"> zzip_init_io </td>
<td width="50%"> the recommended way to do things </td></tr>
<tr><td width="50%"> zzip_get_default_io </td>
<td width="50%"> used internally whenever you supply a null
                     for the io-argument of a _ext_io()-call </td></tr>
<tr><td width="50%"> zzip_get_default_ext </td>
<td width="50%"> used internally but not exported </td></tr>
</table></td></tr></table>

And last some stdio-like replacements were build but these
happen to be actually just small wrappers around the other
posix-like magic-calls. It just offers some convenience
since wrappers like "SDL_rwops" tend to use a stringised
open-mode - and I took the occasion to fold the zzip-bits
for the _ext_io-calls right in there recognized via 
special extensions to the openmode-string of zzip_fopen().

<table cellpadding="10" width="100%"><tr><td><table border="1" width="100%">
<tr><td width="50%"> zzip_fopen </td>
<td width="50%"> convert stringmode and call zzip_open_ext_io </td></tr>
<tr><td width="50%"> zzip_fread </td>
<td width="50%"> slower way to say zzip_read </td></tr>
<tr><td width="50%"> zzip_fclose </td>
<td width="50%"> a synonym of zzip_close </td></tr>
</table></td></tr></table>

For some reason, people did need the full set of function-calls()
  to be working on zzip-wrappers too, so here they are - if the
  ZZIP_FILE instance did wrap a real file, then the real posix-call
  will be used, otherwise it is simulated on the compressed stream
  with a zip-contained file - especially `seek()` can be 
  a slow operation:
  if the new point is later then just read out more bytes till we
  hit that position but if it is an earlier point then rewind to the
  beginning of the compressed data and start reading/decompression
  until the position is met.

<table cellpadding="10" width="100%"><tr><td><table border="1" width="100%">
<tr><td width="50%"> zzip_rewind </td>
<td width="50%"> magic for rewind() </td></tr>
<tr><td width="50%"> zzip_tell </td>
<td width="50%"> magic for tell() </td></tr>
<tr><td width="50%"> zzip_seek </td>
<td width="50%"> magic for seek() </td></tr>
</table></td></tr></table>

And last not least, there are few informative functions to
use function-calls to read parts of the opaque structures
of zzip-objects and their zzip-factory.

<table cellpadding="10" width="100%"><tr><td><table border="1" width="100%">
<tr><td width="50%"> zzip_dir_stat </td>
<td width="50%"> a stat()-like thing on a file within a ZZIP_DIR </td></tr>
<tr><td width="50%"> zzip_dir_real </td>
<td width="50%"> check if ZZIP_DIR wraps a stat'able posix-dirent</td></tr>
<tr><td width="50%"> zzip_file_real </td>
<td width="50%"> check if ZZIP_FILE wraps a stat'able posix-file </td></tr>
<tr><td width="50%"> zzip_realdir </td>
<td width="50%"> if zzip_dir_real then return the posix-dirent </td></tr>
<tr><td width="50%"> zzip_realfd </td>
<td width="50%"> if zzip_file_real then return the posix-file </td></tr>
<tr><td width="50%"> zzip_dirhandle </td>
<td width="50%"> the attached ZZIP_DIR of compressed ZZIP_FILE </td></tr>
<tr><td width="50%"> zzip_dirfd </td>
<td width="50%"> the attached posix-file of ZZIP_DIR zip-file </td></tr>
<tr><td width="50%"> zzip_set_error </td>
<td width="50%"> set the last ZZIP_DIR error-code </td></tr>
<tr><td width="50%"> zzip_error </td>
<td width="50%"> get the last ZZIP_DIR error-code </td></tr>
<tr><td width="50%"> zzip_strerror </td>
<td width="50%"> convert a zzip_error into a readable string </td></tr>
<tr><td width="50%"> zzip_strerror_of </td>
<td width="50%"> combine both above zzip_strerror of zzip_error </td></tr>
<tr><td width="50%"> zzip_errno </td>
<td width="50%"> helper to wrap a zzip-error to a posix-errno </td></tr>
<tr><td width="50%"> zzip_compr_str </td>
<td width="50%"> helper to wrap a compr-number to a readable string
                     </td></tr>
<tr><td width="50%"> zzip_dir_free </td>
<td width="50%"> internally called by zzip_dir_close if the ref-count 
                     of the ZZIP_DIR has gone zero</td></tr>
<tr><td width="50%"> zzip_freopen </td>
<td width="50%"> to reuse the ZZIP_DIR from another ZZIP_FILE so it does
                     not need to be parsed again </td></tr>
<tr><td width="50%"> zzip_open_shared_io </td>
<td width="50%"> the ext/io cousin but it does not close the old ZZIP_FILE
                     and instead just shares the ZZIP_DIR if possible</td></tr>
</table></td></tr></table>
