<date> 2004-05-18 </date>

## Download 
what to get to get it

#### Sourceforge File Area

<center>
<a href="http://sourceforge.net/project/showfiles.php?group_id=6389">
                sourceforge.net/project/showfiles.php?group_id=6389 </a>
</center>

All source releases and some binary releases are listed at the
sourceforge download area under the link show above. The sourceforge
file area is replicated all over the world and should be accessible
with highest bandwidth in all corners of the world.

#### Which Version To Download 

Do not use 0.10.x anymore! It is listed as stable since it is the
only release of zziplib tested to work on a few dozen platforms.
However there were some problematic zip files out there that can
trigger segfaults. Later zzip file decoders have extra checks and
helper routines for that. It's just that the later zziplib have not
been given as many crossplatform build tets as the 0.10.x generation.

Use a 0.12.x (proto-stable) or a 0.13.x (developer) variant of 
zziplib, especially if you intend to make heavy usage of the zip
decoders in specialized environments - I will not add any fixes to
the 0.10.x series anymore (it's deep frozen) but if you hit a 
problem with 0.13.x I can help you quickly with a patch and official
bugfix release. The later versions are regulary checked crossplatform
atleast for **Linux, Solaris, FreeBSD, Darwin/MacOSX, Win32/NT** 
including i386, amd64, sparc, sparc64, powerpc where available.

Note that all generations 0.10.x through 0.13.x are strictly
**backward compatible**. There is a core API (file and dir
handling) being binary compatible, which is also true for most
of the helper routines (data getters). Only some rarely used
entries are made source level compatible, and so far no one had 
ever any problem with binary compatibility of the zziplib DLLs.

The MSVC users are strongly advised to use a a later version as
well since I have tested the 0.12.x/0.13.x myself and making
some msc binary dll releases directly - prior versions were 
thirdparty contributions which were working smoothly since I have 
been preparing zziplib for win32 using the gcc/mingw compile suite.
Please check also the [developer pages](developer.html).
