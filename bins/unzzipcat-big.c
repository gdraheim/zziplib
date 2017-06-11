/*
 *	Copyright (c) 2003 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB license.
 *
 *      This file is used as an example to clarify zzipfseeko api usage.
 */

#include <zzip/fseeko.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <zzip/__debug.h>
#include "unzzipcat-zip.h"

#ifdef ZZIP_HAVE_FNMATCH_H
#include <fnmatch.h>
#else
#define fnmatch(x,y,z) strcmp(x,y)
#endif

#ifndef strnup
static char* strndup (char const *s, size_t n)
{
    size_t len = strnlen (s, n);
    char *new = malloc (len + 1);
    if (new == NULL)
        return NULL;
    new[len] = '\0';
    return memcpy (new, s, len);
}
#endif

static void unzzip_big_entry_fprint(ZZIP_ENTRY* entry, FILE* out)
{
    ZZIP_ENTRY_FILE* file = zzip_entry_fopen (entry, 0);
    if (file) 
    {
	char buffer[1024]; int len;
	while ((len = zzip_entry_fread (buffer, 1024, 1, file)))
	{
	    DBG2("entry read %i", len);
	    fwrite (buffer, len, 1, out);
	}
	DBG2("entry done %s", strerror(errno));
	zzip_entry_fclose (file);
    } else
    {
        DBG2("could not open entry: %s", strerror(errno));
    }
}

static void unzzip_cat_file(FILE* disk, char* name, FILE* out)
{
    ZZIP_ENTRY_FILE* file = zzip_entry_ffile (disk, name);
    if (file) 
    {
	char buffer[1024]; int len;
	while ((len = zzip_entry_fread (buffer, 1024, 1, file)))
	    fwrite (buffer, len, 1, out);
	
	zzip_entry_fclose (file);
    }
}

static void makedirs(const char* name)
{
      char* p = strrchr(name, '/');
      if (p) {
          char* dir_name = strndup(name, p-name);
          makedirs(dir_name);
          free (dir_name);
      } else {
          #ifdef __MINGW32__
          mkdir(name);
          #else
          mkdir(name, 775);
          #endif
          errno = 0;
      }
}

static FILE* create_fopen(char* name, char* mode, int subdirs)
{
   if (subdirs)
   {
      char* p = strrchr(name, '/');
      if (p) {
          char* dir_name = strndup(name, p-name);
          makedirs(dir_name); 
          free (dir_name);
      }
   }
   return fopen(name, mode);      
}


static int unzzip_cat (int argc, char ** argv, int extract)
{
    int argn;
    FILE* disk;

    disk = fopen (argv[1], "r");
    if (! disk) {
	perror(argv[1]);
	return -1;
    }

    if (argc == 2)
    {  /* print directory list */
	ZZIP_ENTRY* entry = zzip_entry_findfirst(disk);
	for (; entry ; entry = zzip_entry_findnext(entry))
	{
	    char* name = zzip_entry_strdup_name (entry);
	    FILE* out = stdout;
	    if (extract) out = create_fopen(name, "w", 1);
	    unzzip_cat_file (disk, name, out);
	    if (extract) fclose(out);
	    free (name);
	}
	return 0;
    }

    if (argc == 3 && !extract)
    {  /* list from one spec */
	ZZIP_ENTRY* entry = 0;
	while ((entry = zzip_entry_findmatch(disk, argv[2], entry, 0, 0)))
	{
	     unzzip_big_entry_fprint (entry, stdout);
	}
	return 0;
    }

    for (argn=1; argn < argc; argn++)
    {   /* list only the matching entries - each in order of commandline */
	ZZIP_ENTRY* entry = zzip_entry_findfirst(disk);
	for (; entry ; entry = zzip_entry_findnext(entry))
	{
	    char* name = zzip_entry_strdup_name (entry);
	    DBG3(".. check '%s' to zip '%s'", argv[argn], name);
	    if (! fnmatch (argv[argn], name, 
			   FNM_NOESCAPE|FNM_PATHNAME|FNM_PERIOD))
	    {
	        FILE* out = stdout;
	        if (extract) out = create_fopen(name, "w", 1);
		unzzip_cat_file (disk, name, out);
		if (extract) fclose(out);
		break; /* match loop */
	    }
	    free (name);
	}
    }
    return 0;
} 

int unzzip_print (int argc, char ** argv)
{
    return unzzip_cat(argc, argv, 0);
}

int unzzip_extract (int argc, char ** argv)
{
    return unzzip_cat(argc, argv, 1);
}

/* 
 * Local variables:
 * c-file-style: "stroustrup"
 * End:
 */
