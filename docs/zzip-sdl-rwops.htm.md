<date> 19. Aug 2001 </date>

## SDL rwops 
Example to make an SDL_rwops interface.

<small> some <b>MSVC</b> help in 
   <a href="README.MSVC6">README.MSVC6</a> and
   <a href="README.SDL">README.SDL</a>
</small>

### Source 

The example sources of the [zziplib library](zziplib.html) 
 are usually put under the [ZLIB license](COPYING.ZLIB) so 
 that you can reuse the code freely in your own projects. Here we talk
 about the example that might be most useful for 
 [SDL](http://libsdl.org) based programs.
 Just copy the two files 
 [SDL_rwops_zzip.h](SDL_rwops_zzip.h)
 and
 [SDL_rwops_zzip.c](SDL_rwops_zzip.c) 
 to the directory with your other project sources, and make sure
 to link it somehow to your programs. I did not make the effort to
 create a separate library out of it - it would just export one
 single function `SDL_RWFromZZIP` that has the same call-synopsis
 like `SDL_RWFromFile` (but it can not (yet) write a zip-file).

The source file [SDL_rwops_zzip.c](SDL_rwops_zzip.c) is
 quite short - it just stores a ZZIP_FILE handle in the userdata
 field of the `SDL_rwops` structure. The SDL'rwop calls will then
 fetch that pointer and call the corresponding functions from the
 [zziplib library](zziplib.html). Most of the glue code
 is in the `SDL_RWFromZZIP` function that allocates an 
 `SDL_rwops` structure and fills the handler-functions 
 into the callback fields.

### Usage 

If you link this file to your project, remember that your executables
 do now have additional dependencies - not only -lzzip to link with
 the [zziplib library](zziplib.html) - do not forget to
 link with zlib library via -lz. Of course, there is a lib-config
 script that you can use: `zzip-config --libs` will return these
 linker-infos (unless you have a native-windows system - it is 
 shell-script).

As an example, replace that `SDL_RWFromFile` that accesses your
 game-graphic files - these files are stored in shared/myapp
 of course where they belong. When you've done that
 then go to X/share/myapp and  \
 `(cd graphics/ && zip -9r ../graphics.zip .)`  \
 and rename the graphics/ subfolder - and still all your files
 are found: a filepath like X/shared/graphics/game/greetings.bmp 
 will open X/shared/graphics.zip and return the zipped file 
 game/greetings.bmp in the zip-archive (for reading that is).

### Test 

The [zziplib](zziplib.html) configure script does not
 look for [SDL](http://libsdl.org). If you know that
 you have [SDL](http://libsdl.org) installed 
 then you can check this `SDL_rwops` example by using
 `make testsdl`. This will compile the
 two source files [SDL_rwops_zzip.c](SDL_rwops_zzip.c) 
 and [SDL_rwops_zzcat.c](SDL_rwops_zzcat.c) to be linked
 together into an executable called `zzcatsdl`. The test
 will continue with a `zzcatsdl test/README`
 - just like it is done for `make test3`.

The corresponding section in the [Makefile.am](Makefile.am) 
 is also an example how to use lib-config scripts to build files. Here
 there is no build-processing that had been tweaked much by automake/autoconf.
 Just use sdl-config and zzip-config to add the needed flags.
