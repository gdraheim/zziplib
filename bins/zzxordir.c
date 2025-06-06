/*
 *	Copyright (c) 2000,2001,2002 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB license.
 *
 *      show zip-reading with xor-obfuscation.
 *      Note that the difference to the standard zzdir.c is quite small.
 */

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <zzip/zzip.h>
#include <zzip/plugin.h>

#if defined ZZIP_HAVE_UNISTD_H
#include <unistd.h>
#elif defined ZZIP_HAVE_IO_H
#include <io.h>
#else
#error need posix io for this example
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

static const char usage[] = /* .. */
    {"zzdir <dir>.. \n"
     "  - prints a content table to stdout, but the dir can also be a zip-arch."
     "\n"
     " the file is part of an inflated zip-archive obfuscated with xor value,\n"
     " given by the numeric option (default is 0x55). \n"
     "\n"
     " To show the contents of a zip-archive named 'test.zip', you may write \n"
     "     zzdir test \n"};

#define BASENAME(x) (strchr((x), '/') ? strrchr((x), '/') + 1 : (x))

static int
unzzip_version(void)
{
    printf("%s version %s %s\n", BASENAME(__FILE__), ZZIP_PACKAGE_NAME, ZZIP_PACKAGE_VERSION);
    return 0;
}

static int
unzzip_help(void)
{
    printf(usage);
    return 0;
}

static int xor_value;

static zzip_ssize_t
xor_read(int f, void* p, zzip_size_t l)
{
    zzip_ssize_t r = read(f, p, l);
    zzip_ssize_t x;
    char*        q;
    for (x = 0, q = p; x < r; x++)
        q[x] ^= xor_value;
    return r;
}

static zzip_plugin_io_handlers xor_handlers  = {};
static zzip_strings_t          xor_fileext[] = {".dat", "", 0};

int
main(int argc, char** argv)
{
    int argn;
    int exitcode = 0;
    xor_value    = 0x55;

    if (argc <= 1 || ! strcmp(argv[1], "--help")) {
        return unzzip_help();
    }
    if (! strcmp(argv[1], "--version")) {
        return unzzip_version();
    }

    zzip_init_io(&xor_handlers, 0);
    xor_handlers.fd.read = &xor_read;

    if (! (xor_handlers.fd.type & (long) (sizeof(off_t)))) {
        fprintf(stderr, "largefile mismatch: bin %libit <> lib %libit\n", /* .. */
                (long) BITS * sizeof(off_t), BITS * zzip_io_size_off_t());
        return EX_SOFTWARE;
    }

    for (argn = 1; argn < argc; argn++) {
        ZZIP_DIR*    dir;
        ZZIP_DIRENT* d;

        if (argv[argn][0] == '-') {
            if (isdigit(argv[argn][1]))
                xor_value = atoi(argv[argn] + 1);
            continue;
        }

        dir = zzip_opendir_ext_io(argv[argn], /*..*/
                                  ZZIP_ONLYZIP, xor_fileext, &xor_handlers);
        if (! dir) {
            fprintf(stderr, "did not open %s: ", argv[argn]);
            perror(argv[argn]);
            exitcode = EX_NOINPUT;
            continue;
        }

        if (argc > 2)
            printf("%s: \n", argv[argn]);

        /* read each dir entry and show one line of info per file */
        while ((d = zzip_readdir(dir))) {
            /* orignalsize / compression-type / compression-ratio / filename */
            if (d->st_size > 999999) {
                printf("%5dK %-9s %2d%% %s\n",                            /* .. */
                       d->st_size >> 10,                                  /*.. */
                       zzip_compr_str(d->d_compr),                        /* .. */
                       100 - (d->d_csize | 1) / ((d->st_size / 100) | 1), /* .. */
                       d->d_name);
            }
            else {
                printf("%6d %-9s %2d%% %s\n",                           /* .. */
                       d->st_size,                                      /* .. */
                       zzip_compr_str(d->d_compr),                      /* .. */
                       100 - (d->d_csize | 1) * 100 / (d->st_size | 1), /* .. */
                       d->d_name);
            }
        }

        zzip_closedir(dir);
    }

    return exitcode;
}
