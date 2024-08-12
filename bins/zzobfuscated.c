/*
 *	Copyright (c) 2002 Mike Nordell
 *  portions  Copyright (c) 2000,2001,2002 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB License
 *
 * A small example that displays how the plugin I/O functions can be used
 * to read "encrypted" zip archives.
 */

#include <zzip/zzip.h>
#include <zzip/plugin.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#ifndef O_BINARY
#define O_BINARY 0
#endif

#if defined ZZIP_HAVE_UNISTD_H
#include <unistd.h> /* read */
#elif defined ZZIP_HAVE_IO_H
#include <io.h> /* win32 */
#else
#endif

#ifdef _MSC_VER
#define _MSC_VER_NULL NULL
#else
#define _MSC_VER_NULL
#endif

#ifndef EX_USAGE
#define EX_USAGE 64
#endif

#ifndef EX_NOINPUT
#define EX_NOINPUT 66
#endif

#ifndef EX_SOFTWARE
#define EX_SOFTWARE 70
#endif

#ifndef EX_CANTCREAT
#define EX_CANTCREAT 73
#endif

#ifndef EX_IOERR
#define EX_IOERR 74
#endif

#ifndef BITS
#define BITS 8
#endif

/*
 * Only override our the read handler. Let the system take care
 * the rest.
 */

static zzip_ssize_t
our_read(int fd, void* buf, zzip_size_t len)
{
    const zzip_ssize_t bytes = read(fd, buf, len);
    zzip_ssize_t       i;
    char*              pch = (char*) buf;
    for (i = 0; i < bytes; ++i) {
        pch[i] ^= 0x55;
    }
    return bytes;
}

static zzip_plugin_io_handlers our_handlers  = {_MSC_VER_NULL};
static const char* const       our_fileext[] = {".dat", ".sav", 0};

static const char usage[] = {
    " zzobfuscated <file> [in-zip filename]\n"
    "  - Demonstrates the use of installable file I/O handlers.\n"
    " Copies <file> to \"obfuscated[.dat]\" while \"encrypting\" it by xor'ing\n"
    " every byte with 0x55, installs file I/O handlers, and then uses the\n"
    " zzip_open_ext_io function to read and print the file to stdout.\n"
    " The file can be a normal file or an inflated part of a zip-archive,\n"
    " to get 'README' from test.zip you may write \n"
    "    zzobfuscated test.zip README \n"};

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

int
main(int argc, char* argv[])
{
    int exitcode = 0;
    if (argc <= 1 || argc > 3 || ! strcmp(argv[1], "--help")) {
        return unzzip_help();
    }
    if (! strcmp(argv[1], "--version")) {
        return unzzip_version();
    }

    if (strlen(argv[1]) > 128) {
        fprintf(stderr, "Please provide a filename shorter than 128 chars.\n");
        exit(EX_USAGE);
    }

    /* obfuscate the file */
    {
        int   ch;
        FILE* fin;
        FILE* fout;
        fin = fopen(argv[1], "rb");
        if (! fin) {
            fprintf(stderr, "Can't open input file \"%s\"\n", argv[1]);
            exit(EX_NOINPUT);
        }
        fout = fopen((argc == 2) ? "obfuscated" : "obfuscated.dat", "wb");
        if (! fout) {
            fprintf(stderr, "Can't open output file \"obfuscated\"\n");
            exit(EX_CANTCREAT);
        }
        while ((ch = fgetc(fin)) != EOF) {
            ch ^= 0x55;
            fputc(ch, fout);
        }
        fclose(fout);
        fclose(fin);
    }

    /* install our I/O hander */
    zzip_init_io(&our_handlers, 0);
    our_handlers.fd.read = &our_read;

    if (! (our_handlers.fd.type & (long) (sizeof(off_t)))) {
        fprintf(stderr, "largefile mismatch: bin %libit <> lib %libit\n", /* .. */
                (long) BITS * sizeof(off_t), BITS * zzip_plugin_off_t());
        return EX_SOFTWARE;
    }

    {
#define argn 2
        ZZIP_FILE* fp;
        char       name[256];
        if (argc == 3) {
            sprintf(name, "obfuscated/%s", argv[argn]);
        }
        else {
            sprintf(name, "obfuscated");
        }
        fp = zzip_open_ext_io(name, O_RDONLY | O_BINARY, ZZIP_PREFERZIP, /* .. */
                              our_fileext, &our_handlers);

        if (! fp) {
            perror(name);
            exitcode = EX_NOINPUT;
        }
        else {
            char buf[17];
            int  n;

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
                perror(argv[argn]);
                exitcode = EX_IOERR;
            }
        }
    }

    return exitcode;
}
