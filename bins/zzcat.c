/*
 *	Copyright (c) 2000,2001,2002 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB License
 */

#include <zzip/zzip.h>
#include <stdio.h>
#include <string.h>

#ifndef O_BINARY
#define O_BINARY 0
#endif

static const char usage[] = /* .. */
    {" zzcat <file>... \n"
     "  - prints the file to stdout, so you may want to redirect the output; \n"
     " the file can be a normal file or an inflated part of a zip-archive, \n"
     " to get 'README' from dist.zip you may write \n"
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

int
main(int argc, char** argv)
{
    int argn;

    if (argc <= 1 || ! strcmp(argv[1], "--help")) {
        return unzzip_help();
    }
    if (! strcmp(argv[1], "--version")) {
        return unzzip_version();
    }

    for (argn = 1; argn < argc; argn++) {
        ZZIP_FILE* fp = zzip_open(argv[argn], O_RDONLY | O_BINARY);

        if (! fp) {
            perror(argv[argn]);
            continue;
        }
        else {
            char buf[17];
            int  n;

            /* read chunks of 16 bytes into buf and print them to stdout */
            while (0 < (n = zzip_read(fp, buf, 16))) {
                buf[n] = '\0';
#ifdef STDOUT_FILENO
                write(STDOUT_FILENO, buf, n);
#else
                fwrite(buf, 1, n, stdout);
#endif
            }

            if (n == -1)
                perror(argv[argn]);

            zzip_close(fp);
        }
    }

    return 0;
}
