/*
 *	Copyright (c) 2000,2001,2002 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB License
 *
 *      show a simple program to add xor-obfuscation.
 *      look at the resulting file with zzxordir an zzxorcat
 *      Remember that xor'ing data twice will result in the original data.
 *      This file has no dependency with zziplib - it's freestanding.
 */
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include <zzip/_config.h> /* for  ZZIP_PACKAGE_VERSION  */

#ifdef ZZIP_HAVE_SYS_TYPES_H
#include <sys/types.h>
#elif defined SSIZE_T
typedef SSIZE_T ssize_t
#elif defined __SSIZE_T_TYPE
typedef __SSIZE_T_TYPE ssize_t
#else
typedef int ssize_t;
#endif

static const char usage[] = 
{
    " zzxopy [-#] <input-file> <output-file> \n"
    "   copies data from input-file to output-file adding simple \n"
    "   obfuscation by xor-ing each byte with the numeric value given. \n"
    "   the default xor-value is 0x55. Remember that copying data twice \n"
    "   with the same xor-value will result in the original file data. \n"
};

#define BASENAME(x) (strchr((x), '/') ? strrchr((x), '/')+1 : (x))

static int unzzip_version(void)
{
	printf ("%s version %s %s\n", BASENAME(__FILE__), ZZIP_PACKAGE_NAME, ZZIP_PACKAGE_VERSION);
    return 0;
}

static int unzzip_help(void)
{
    printf (usage);
    return 0;
}

static int xor_value;

static ssize_t xor_read (FILE* f, void* p, size_t l)
{
    ssize_t r = fread(p, 1, l, f);
    ssize_t x; char* q; for (x=0, q=p; x < r; x++) q[x] ^= xor_value;
    return r;
}

int 
main (int argc, char ** argv)
{
    int argn;
    xor_value = 0x55;

    if (argc <= 1 || ! strcmp (argv[1], "--help"))
    {
        return unzzip_help();
    }
    if (! strcmp (argv[1], "--version"))
    {
	    return unzzip_version();
    }
    
    for (argn=1; argn < argc; argn++)
    {
	FILE* iF = 0;
	FILE* oF = 0;

	if (argv[argn][0] == '-')
	{
	    if (isdigit(argv[argn][1]))	xor_value = atoi (argv[argn]+1);
	    continue;
	}

	if (argn + 1 >= argc)
	{
	    printf (usage);
	    exit (1);
	}

        iF = fopen (argv[argn], "rb");
	if (! iF) { perror (argv[argn]); exit (2); }
	argn++;
        oF = fopen (argv[argn], "wb");
	if (! oF) { perror (argv[argn]); fclose(iF); exit (3); }

	{
            char buf[17];
            ssize_t n;

	    /* read chunks of 16 bytes into buf and print them to stdout */
            while (0 < (n = xor_read(iF, buf, 16)))
            {
                buf[n] = '\0';
                n = fwrite (buf, 1, n, oF);
		if (n < 0) break;
            }

            if (n < 0 && ferror (iF)) 
                perror (argv[argn]);
        }
    }
    
    return 0;
} 

/* 
 * Local variables:
 * c-file-style: "stroustrup"
 * End:
 */
