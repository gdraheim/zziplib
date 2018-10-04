/*
 *	Copyright (c) 2003 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB license.
 *
 *      This file is used as an example to clarify zzipmmap api usage.
 */

#include <zzip/memdisk.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <zzip/__mkdir.h>
#include <zzip/__fnmatch.h>
#include <zzip/__string.h>
#include <zzip/__debug.h>
#include "unzzipcat-zip.h"
#include "unzzip-states.h"

#ifdef ZZIP_HAVE_UNISTD_H
#include <unistd.h>
#endif
#ifdef ZZIP_HAVE_IO_H
#include <io.h>
#endif

static int exitcode(int e)
{
    return EXIT_ERRORS;
}

static void unzzip_mem_entry_fprint(ZZIP_MEM_DISK* disk, 
				  ZZIP_MEM_ENTRY* entry, FILE* out)
{
    ZZIP_DISK_FILE* file = zzip_mem_entry_fopen (disk, entry);
    if (file) 
    {
	char buffer[1024]; int len;
	while ((len = zzip_mem_disk_fread (buffer, 1024, 1, file)))
	    fwrite (buffer, len, 1, out);
	
	zzip_mem_disk_fclose (file);
    }
}

static void unzzip_mem_disk_cat_file(ZZIP_MEM_DISK* disk, char* name, FILE* out)
{
    ZZIP_DISK_FILE* file = zzip_mem_disk_fopen (disk, name);
    if (file) 
    {
	char buffer[1025]; int len;
	while ((len = zzip_mem_disk_fread (buffer, 1, 1024, file))) 
	{
	    fwrite (buffer, 1, len, out);
	}
	
	zzip_mem_disk_fclose (file);
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
    ZZIP_MEM_DISK* disk;

    if (argc == 1)
    {
	printf (__FILE__" version "ZZIP_PACKAGE" "ZZIP_VERSION"\n");
	return EXIT_OK; /* better provide an archive argument */
    }

    disk = zzip_mem_disk_open (argv[1]);
    if (! disk) {
        DBG3("disk_open failed [%i] %s", errno, strerror(errno));
	perror(argv[1]);
	return exitcode(errno);
    }

    if (argc == 2)
    {  /* print directory list */
	ZZIP_MEM_ENTRY* entry = zzip_mem_disk_findfirst(disk);
	DBG2("findfirst %p\n", entry);
	for (; entry ; entry = zzip_mem_disk_findnext(disk, entry))
	{
	    char* name = zzip_mem_entry_to_name (entry);
	    FILE* out = stdout;
	    if (extract) out = create_fopen(name, "wb", 1);
	    if (! out) {
	        if (errno != EISDIR) {
	             DBG3("can not open output file %i %s", errno, strerror(errno));
	             done = EXIT_ERRORS;
	        }
	        continue;
	    }
	    unzzip_mem_disk_cat_file (disk, name, out);
	    if (extract) fclose(out);
	}
    } 
    else if (argc == 3 && !extract)
    {  /* list from one spec */
	ZZIP_MEM_ENTRY* entry = 0;
	while ((entry = zzip_mem_disk_findmatch(disk, argv[2], entry, 0, 0)))
	{
	     unzzip_mem_entry_fprint (disk, entry, stdout);
	}
    } else {
	for (argn=1; argn < argc; argn++)
	{   /* list only the matching entries - each in order of commandline */
	    ZZIP_MEM_ENTRY* entry = zzip_mem_disk_findfirst(disk);
	    for (; entry ; entry = zzip_mem_disk_findnext(disk, entry))
	    {
	        char* name = zzip_mem_entry_to_name (entry);
	        if (! _zzip_fnmatch (argv[argn], name, 
		    _zzip_FNM_NOESCAPE|_zzip_FNM_PATHNAME|_zzip_FNM_PERIOD))
	        {
	            FILE* out = stdout;
	            if (extract) out = create_fopen(name, "wb", 1);
		    if (! out) {
		        if (errno != EISDIR) {
		            DBG3("can not open output file %i %s", errno, strerror(errno));
		            done = EXIT_ERRORS;
		        }
		        continue;
		    }
		    unzzip_mem_disk_cat_file (disk, name, out);
		    if (extract) fclose(out);
		    break; /* match loop */
		}
	    }
	}
    }
    zzip_mem_disk_close(disk);
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
