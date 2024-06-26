/*
 *	Copyright (c) 2003 Guido Draheim <guidod@gmx.de>
 *      Use freely under the restrictions of the ZLIB license.
 *
 *      This file is used as an example to clarify zzipfseeko api usage.
 */

#include <zzip/fseeko.h>
#include <stdlib.h>
#include <string.h>
#include <zzip/__fnmatch.h>

static const char usage[] = /* .. */
    {"unzzipshow <zip> [names].. \n"
     "  - unzzip data content of files contained in a zip archive.\n"};

static void
zzip_entry_fprint(ZZIP_ENTRY* entry, FILE* out)
{
    ZZIP_ENTRY_FILE* file = zzip_entry_fopen(entry, 0);
    if (file) {
        char buffer[1024];
        int  len;
        while (0 < (len = zzip_entry_fread(buffer, 1024, 1, file)))
            fwrite(buffer, len, 1, out);

        zzip_entry_fclose(file);
    }
}

static void
zzip_cat_file(FILE* disk, char* name, FILE* out)
{
    ZZIP_ENTRY_FILE* file = zzip_entry_ffile(disk, name);
    if (file) {
        char buffer[1024];
        int  len;
        while (0 < (len = zzip_entry_fread(buffer, 1024, 1, file)))
            fwrite(buffer, len, 1, out);

        zzip_entry_fclose(file);
    }
}

#define BASENAME(x) (strchr((x), '/') ? strrchr((x), '/') + 1 : (x))

static int
unzzip_version()
{
    printf("%s version %s %s\n", BASENAME(__FILE__), ZZIP_PACKAGE_NAME, ZZIP_PACKAGE_VERSION);
    return 0;
}

static int
unzzip_help()
{
    printf(usage);
    return 0;
}

int
main(int argc, char** argv)
{
    int   argn;
    FILE* disk;

    if (argc <= 1 || ! strcmp(argv[1], "--help")) {
        return unzzip_help();
    }
    if (! strcmp(argv[1], "--version")) {
        return unzzip_version();
    }

    disk = fopen(argv[1], "r");
    if (! disk) {
        perror(argv[1]);
        return -1;
    }

    if (argc == 2) { /* print directory list */
        ZZIP_ENTRY* entry = zzip_entry_findfirst(disk);
        if (! entry)
            puts("no first entry!\n");
        for (; entry; entry = zzip_entry_findnext(entry)) {
            char* name = zzip_entry_strdup_name(entry);
            printf("%s\n", name);
            free(name);
        }
        return 0;
    }

    if (argc == 3) { /* list from one spec */
        ZZIP_ENTRY* entry = 0;
        while ((entry = zzip_entry_findmatch(disk, argv[2], entry, 0, 0)))
            zzip_entry_fprint(entry, stdout);

        return 0;
    }

    for (argn = 1; argn < argc;
         argn++) { /* list only the matching entries - each in order of commandline */
        ZZIP_ENTRY* entry = zzip_entry_findfirst(disk);
        for (; entry; entry = zzip_entry_findnext(entry)) {
            char* name = zzip_entry_strdup_name(entry);
            if (! _zzip_fnmatch(argv[argn], name,
                                _zzip_FNM_NOESCAPE | _zzip_FNM_PATHNAME | _zzip_FNM_PERIOD))
                zzip_cat_file(disk, name, stdout);
            free(name);
        }
    }
    return 0;
}
