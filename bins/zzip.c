/*
 *	Copyright (c) 2003 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB license.
 *
 *      This file is used as an example to clarify zzip api usage.
 *                        (the write-api is work in progress, beware)
 */

#define _ZZIP_WRITE_SOURCE

#include <zzip/write.h>
#include <stdio.h>
#include <string.h>

#ifdef ZZIP_HAVE_UNISTD_H
#include <unistd.h>
#endif
#ifdef ZZIP_HAVE_IO_H
#include <io.h>
#endif

/* common code */
#include "zzipmake-zip.h"

static const char usage[] = /* .. */
    {"zzip <dir> files... \n"
     "  - zzip the files into a zip area."};

#define BASENAME(x) (strchr((x), '/') ? strrchr((x), '/') + 1 : (x))

static int
unzzip_version(void)
{
#if defined _ZZIP_ENABLE_WRITE
#define WRITE_OPTION "W/ -D_ZZIP_ENABLE_WRITE"
#else
#define WRITE_OPTION "NO -D_ZZIP_ENABLE_WRITE"
#endif
    printf("%s version %s %s - %s\n", BASENAME(__FILE__), ZZIP_PACKAGE_NAME, ZZIP_PACKAGE_VERSION,
           WRITE_OPTION);
    return 0;
}

static int
unzzip_help(void)
{
    printf(usage);
    return 0;
}

int
main(int argc, char** argv)
{
    int       argn;
    int       exitcode = 0;
    ZZIP_DIR* dir;

    if (argc <= 1 || ! strcmp(argv[1], "--help")) {
        return unzzip_help();
    }
    if (! strcmp(argv[1], "--version")) {
        return unzzip_version();
    }

    return rezzip_make(argc, argv);
}
