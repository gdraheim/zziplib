/*
 *	Copyright (c) 2000,2001 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB license.
 *
 *      Modified by Andreas Schiffler, 2001, for the zzipwrap feature
 *      Modified by Guido Draheim in 2002 for the plugin_io feature
 */

#include <stdio.h>
#include <stdlib.h> /* exit */
#include <string.h>

#include <zzip/zzip.h>
#include <zzip/plugin.h>
/* #incl <zzip/wrap.h> */
#include "wrap.h"

#ifndef O_BINARY
#define O_BINARY 0
#endif

#ifndef EX_NOINPUT
#define EX_NOINPUT 66
#endif

#ifndef EX_SOFTWARE
#define EX_SOFTWARE 70
#endif

#ifndef BITS
#define BITS 8
#endif

static const char usage[] = {
    "zzipwrap <dir>.. \n"
    "  - prints a content table to stdout, but the dir can also be a zip-arch."
    "\n"
    " To show the contents of a zip-archive named 'test.zip', you may write \n"
    "     zzipwrap test \n"};

/* This is a demo block callback routine that has access to the buffer */
/* that was just read BEFORE it is used by zziplib.                    */
static void
demo_block_callback(void* buffer, int buffersize, void* data)
{
    fprintf(stderr,
            "demo_block_callback( buffer-pointer=%p"
            " buffer-size=%i  data='%s' )\n",
            buffer, buffersize, (char*) data);
}

int
main(int argc, char** argv)
{
    int              exitcode = 0;
    zzip_plugin_io_t io;
    int              argn;

    if (argc <= 1) {
        printf(usage);
        exit(0);
    }

    /* Enable blocked (32 bytes) memory buffered IO routines with a */
    /* demo callback routine. */
    io = zzipwrap_use_memory_io(32, demo_block_callback, (void*) "Some callback data");
    if (! io) {
        fprintf(stderr, "could not initialize memory-io");
        return EX_SOFTWARE;
    }

    if (! (zzip_io_size_off_t() & (long) (sizeof(off_t)))) {
        fprintf(stderr, "largefile mismatch: bin %libit <> lib %libit\n", /* .. */
                (long) BITS * sizeof(off_t), BITS * zzip_io_size_off_t());
        return EX_SOFTWARE;
    }

    for (argn = 1; argn < argc; argn++) {
        ZZIP_DIR*    dir;
        ZZIP_DIRENT* d;

        dir = zzip_opendir_ext_io(argv[argn], 0, 0, io);
        if (! dir) {
            fprintf(stderr, "did not open %s:", argv[argn]);
            perror(argv[argn]);
            exitcode = EX_NOINPUT;
            continue;
        }

        if (argc > 2)
            printf("%s:\n", argv[argn]);

        /* read each dir entry and show one line of info per file */
        while ((d = zzip_readdir(dir))) {
            /* orignalsize / compression-type / compression-ratio / filename */
            if (d->st_size > 999999) {
                printf("%5dK %-9s %2d%% %s\n", d->st_size >> 10, zzip_compr_str(d->d_compr),
                       100 - (d->d_csize | 1) / ((d->st_size / 100) | 1), d->d_name);
            }
            else {
                printf("%6d %-9s %2d%% %s\n", d->st_size, zzip_compr_str(d->d_compr),
                       100 - (d->d_csize | 1) * 100 / (d->st_size | 1), d->d_name);
            }
        }

        zzip_closedir(dir);
    }

    return exitcode;
}
