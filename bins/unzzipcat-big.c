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
#include <zzip/__mkdir.h>
#include <zzip/__string.h>
#include <zzip/__debug.h>
#include <zzip/__fnmatch.h>
#include "unzzipcat-zip.h"
#include "unzzip-states.h"

static int exitcode(int e)
{
    return EXIT_ERRORS;
}

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

/*
 * NAME: remove_dotdotslash
 * PURPOSE: To remove any "../" components from the given pathname
 * ARGUMENTS: path: path name with maybe "../" components
 * RETURNS: Nothing, "path" is modified in-place
 * NOTE: removing "../" from the path ALWAYS shortens the path, never adds to it!
 *	Also, "path" is not used after creating it.
 *	So modifying "path" in-place is safe to do.
 */
static inline void
remove_dotdotslash(char *path)
{
    /* Note: removing "../" from the path ALWAYS shortens the path, never adds to it! */
    char *dotdotslash;
    int warned = 0;

    dotdotslash = path;
    while ((dotdotslash = strstr(dotdotslash, "../")) != NULL)
    {
        /*
         * Remove only if at the beginning of the pathname ("../path/name")
         * or when preceded by a slash ("path/../name"),
         * otherwise not ("path../name..")!
         */
        if (dotdotslash == path || dotdotslash[-1] == '/')
        {
            char *src, *dst;
            if (!warned)
            {
                /* Note: the first time through the pathname is still intact */
                fprintf(stderr, "Removing \"../\" path component(s) in %s\n", path);
                warned = 1;
            }
            /* We cannot use strcpy(), as there "The strings may not overlap" */
            for (src = dotdotslash+3, dst=dotdotslash; (*dst = *src) != '\0'; src++, dst++)
                ;
        }
        else
            dotdotslash +=3;	/* skip this instance to prevent infinite loop */
    }
}

static void makedirs(const char* name)
{
      char* p = strrchr(name, '/');
      if (p) {
          char* dir_name = _zzip_strndup(name, p-name);
          makedirs(dir_name);
          free (dir_name);
      } 
      if (_zzip_mkdir(name, 0775) == -1 && errno != EEXIST) 
      {
          DBG3("while mkdir %s : %s", name, strerror(errno));
      }
      errno = 0;
}

static FILE* create_fopen(char* name, char* mode, int subdirs)
{
   char *name_stripped;
   FILE *fp;
   int mustfree = 0;

   if ((name_stripped = strdup(name)) != NULL)
   {
       remove_dotdotslash(name_stripped);
       name = name_stripped;
       mustfree = 1;
   }
   if (subdirs)
   {
      char* p = strrchr(name, '/');
      if (p) {
          char* dir_name = _zzip_strndup(name, p-name);
          makedirs(dir_name); 
          free (dir_name);
      }
   }
   fp = fopen(name, mode);
   if (mustfree)
       free(name_stripped);
    return fp;
}


static int unzzip_cat (int argc, char ** argv, int extract)
{
    int done = 0;
    int argn;
    FILE* disk;

    disk = fopen (argv[1], "rb");
    if (! disk) {
	perror(argv[1]);
	return exitcode(errno);
    }

    if (argc == 2)
    {  /* print directory list */
	ZZIP_ENTRY* entry = zzip_entry_findfirst(disk);
	for (; entry ; entry = zzip_entry_findnext(entry))
	{
	    char* name = zzip_entry_strdup_name (entry);
	    FILE* out = stdout;
	    if (! name) {
	        done = EXIT_WARNINGS;
	        continue;
	    }
	    if (extract) out = create_fopen(name, "wb", 1);
	    if (! out) {
	        if (errno != EISDIR) done = EXIT_ERRORS;
	        continue;
	    }
	    unzzip_cat_file (disk, name, out);
	    if (extract) fclose(out);
	    free (name);
	}
	return done;
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
	    if (! _zzip_fnmatch (argv[argn], name, 
		_zzip_FNM_NOESCAPE|_zzip_FNM_PATHNAME|_zzip_FNM_PERIOD))
	    {
	        FILE* out = stdout;
	        if (extract) out = create_fopen(name, "wb", 1);
		if (! out) {
		    if (errno != EISDIR) done = EXIT_ERRORS;
		    continue;
		}
		unzzip_cat_file (disk, name, out);
		if (extract) fclose(out);
		break; /* match loop */
	    }
	    free (name);
	}
    }
    return done;
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
