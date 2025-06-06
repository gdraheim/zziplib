/*
 *	Copyright (c) 2000,2001,2002 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB License
 *
 *      show zip-reading with xor-obfuscation.
 *      Note that the difference to the standard zzcat.c is quite small.
 */

#include <zzip/zzip.h>
#include <zzip/plugin.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if defined ZZIP_HAVE_UNISTD_H
#include <unistd.h>
#elif defined ZZIP_HAVE_IO_H
#include <io.h>
#else
#error need posix io for this example
#endif

#ifndef O_BINARY
#define O_BINARY 0
#endif

#ifndef EX_SOFTWARE
#define EX_SOFTWARE 70
#endif

#ifndef EX_NOINPUT
#define EX_NOINPUT 66
#endif

#ifndef EX_IOERR
#define EX_IOERR 74
#endif

#ifndef BITS
#define BITS 8
#endif

static const char usage[] = /* .. */
    {" zzxorcat [-#] <file>... \n"
     "  - prints the file to stdout, so you may want to redirect the output; \n"
     " the file is part of an inflated zip-archive obfuscated with xor value,\n"
     " given by the numeric option (default is 0x55). \n"
     " to get 'README' from dist.dat you may write \n"
     "    zzcat dist/README \n"};

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

static zzip_plugin_io_handlers xor_handlers;
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
        ZZIP_FILE* fp;

        if (argv[argn][0] == '-') {
            if (isdigit(argv[argn][1]))
                xor_value = atoi(argv[argn] + 1);
            continue;
        }

        fp = zzip_open_ext_io(argv[argn], O_RDONLY | O_BINARY, /* .. */
                              ZZIP_CASELESS | ZZIP_ONLYZIP,    /* .. */
                              xor_fileext, &xor_handlers);
        if (! fp) {
            perror(argv[argn]);
            exitcode = EX_NOINPUT;
            continue;
        }
        else {
            char         buf[17];
            zzip_ssize_t n;

            /* read chunks of 16 bytes into buf and print them to stdout */
            while (0 < (n = zzip_read(fp, buf, 16))) {
                buf[n] = '\0';
#ifdef STDOUT_FILENO
                if (-1 == write(STDOUT_FILENO, buf, n)) {
                    perror("stdout");
                    exitcode = EX_IOERR;
                    break;
                }
#else
                fwrite(buf, 1, n, stdout);
#endif
            }

            if (n == -1) {
                perror(argv[n]);
                exitcode = EX_IOERR;
            }

            zzip_close(fp);
        }
    }

    return exitcode;
}
