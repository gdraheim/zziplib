/*
 *	Copyright (c) 2003 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB license.
 *
 *      This file is used as an example to clarify zzipfseeko api usage.
 */

#include <zzip/fseeko.h>
#include <stdlib.h>
#include <string.h>

#ifdef ZZIP_HAVE_FNMATCH_H
#include <fnmatch.h>
#else
#define fnmatch(x,y,z) strcmp(x,y)
#endif

#ifndef O_BINARY
#define O_BINARY 0
#endif

#ifdef DEBUG
#define debug1(msg) do { fprintf(stderr, "%s : " msg "\n", __func__); } while(0)
#define debug2(msg, arg1) do { fprintf(stderr, "%s : " msg "\n", __func__, arg1); } while(0)
#define debug3(msg, arg1, arg2) do { fprintf(stderr, "%s : " msg "\n", __func__, arg1, arg2); } while(0)
#else
#define debug1(msg) 
#define debug2(msg, arg1) 
#define debug3(msg, arg1, arg2) 
#endif

static const char usage[] = 
{
    "unzzipcat-seeko <zip> [names].. \n"
    "  - unzzip data content of files contained in a zip archive.\n"
};

static void zzip_entry_fprint(ZZIP_ENTRY* entry, FILE* out)
{
    ZZIP_ENTRY_FILE* file = zzip_entry_fopen (entry, 0);
    if (file) 
    {
	char buffer[1024]; int len;
	while ((len = zzip_entry_fread (buffer, 1024, 1, file)))
	{
	    debug2("entry read %i", len);
	    fwrite (buffer, len, 1, out);
	}
	debug2("entry done %s", strerror(errno));
	zzip_entry_fclose (file);
    } else
    {
        debug2("could not open entry: %s", strerror(errno));
    }
}

static void zzip_cat_file(FILE* disk, char* name, FILE* out)
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

int 
main (int argc, char ** argv)
{
    int argn;
    FILE* disk;

    if (argc <= 1 || ! strcmp (argv[1], "--help"))
    {
        printf (usage);
	return 0;
    }
    if (! strcmp (argv[1], "--version"))
    {
	printf (__FILE__" version "ZZIP_PACKAGE" "ZZIP_VERSION"\n");
	return 0;
    }

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
	    printf ("%s\n", name);
	    free (name);
	}
	return 0;
    }

    if (argc == 3)
    {  /* list from one spec */
	ZZIP_ENTRY* entry = 0;
	while ((entry = zzip_entry_findmatch(disk, argv[2], entry, 0, 0)))
	{
	     zzip_entry_fprint (entry, stdout);
	}
	return 0;
    }

    for (argn=1; argn < argc; argn++)
    {   /* list only the matching entries - each in order of commandline */
	ZZIP_ENTRY* entry = zzip_entry_findfirst(disk);
	for (; entry ; entry = zzip_entry_findnext(entry))
	{
	    char* name = zzip_entry_strdup_name (entry);
	    debug3(".. check '%s' to zip '%s'", argv[argn], name);
	    if (! fnmatch (argv[argn], name, 
			   FNM_NOESCAPE|FNM_PATHNAME|FNM_PERIOD))
		zzip_cat_file (disk, name, stdout);
	    free (name);
	}
    }
    return 0;
} 

/* 
 * Local variables:
 * c-file-style: "stroustrup"
 * End:
 */
