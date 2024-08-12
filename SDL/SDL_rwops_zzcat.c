/*
 *      Copyright (c) 2001 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB License
 *
 *      (this example uses errno which might not be multithreaded everywhere)
 */

#include <SDL_rwops_zzip.h>
#include <stdlib.h> /* exit */

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

/* mostly a copy from zzcat.c */

int
main(int argc, char** argv)
{
    static const char usage[]  = " zzcat <file>... \n"
                                 "  - prints the file to stdout. the file can be a normal file\n"
                                 "  or an inflated part of a zip-archive \n";
    int               exitcode = 0;
    int               argn;
    if (argc <= 1) {
        printf(usage);
        exit(EX_USAGE);
    }

    for (argn = 1; argn < argc; argn++) {
        SDL_RWops* rwops;

        rwops = SDL_RWFromZZIP(argv[argn], "rb");
        if (! rwops) {
            perror(argv[argn]);
            exitcode = EX_NOINPUT;
            continue;
        }
        else {
            char buf[17];
            int  n;

            /* read chunks of 16 bytes into buf and print them to stdout */
            while (0 < (n = SDL_RWread(rwops, buf, 1, 16))) {
                buf[n] = '\0';
#ifdef STDOUT_FILENO
                write(STDOUT_FILENO, buf, n);
#else
                fwrite(buf, 1, n, stdout);
#endif
            }

            if (n == -1) {
                perror(argv[argn]);
                exitcode = EX_IOERR;
            }

            SDL_RWclose(rwops);
        }
    }

    return exitcode;
}
