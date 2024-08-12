
/*
 * Author:
 *	Guido Draheim <guidod@gmx.de>
 *      Mike Nordell <tamlin-@-algonet-se>
 *
 * Copyright (c) Guido Draheim, use under copyleft (LGPL,MPL)
 */

#include <zzip/lib.h>
#include <zzip/plugin.h>

#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#ifdef DEBUG
#include <stdio.h>
#endif

#include <zzip/file.h>
#include <zzip/format.h>

/** get
 * This function works on a real file descriptor.
 */
long
zzip_plugin_off_t()
{
    return sizeof(off_t);
}

/** get file size.
 * This function works on a real file descriptor.
 */
zzip_off_t
zzip_filesize(int fd)
{
    struct stat st;

    if (fstat(fd, &st) < 0)
        return -1;

#if defined DEBUG && ! defined _WIN32
    if (! st.st_size && st.st_blocks > 1) /* seen on some darwin 10.1 machines */
        fprintf(stderr, "broken fstat(2) ?? st_size=%ld st_blocks=%ld\n", /* .. */
                (long) st.st_size, (long) st.st_blocks);
#endif

    return st.st_size;
}

/* clang-format off */
static const struct zzip_plugin_io default_io = {
    &open,
    &close,
    &_zzip_read,
    &_zzip_lseek,
    &zzip_filesize,
    1,
    ZZIP_PLUGIN_TYPE_DEFAULT | (long)(sizeof(zzip_off_t)),
    &_zzip_write
};
/* clang-format on */

/** => zzip_init_io
 * This function returns a zzip_plugin_io_t handle to static defaults
 * wrapping the posix io file functions for actual file access. The
 * returned structure is shared by all threads in the system.
 */
zzip_plugin_io_t
zzip_get_default_io(void)
{
    return (zzip_plugin_io_t) &default_io;
}

/** init plugin struct.
 *
 * This function initializes the users handler struct to default values
 * being the posix io functions in default configured environments.
 *
 * Note that the target io_handlers_t structure should be static or
 * atleast it should be kept during the lifetime of zzip operations.
 */
int
zzip_init_io(zzip_plugin_io_handlers_t io, int flags)
{
    if (! io) {
        return ZZIP_ERROR;
    }
    memcpy(io, &default_io, sizeof(default_io));
    io->fd.sys = flags;
    return 0;
}

/* 64on32 - define functions with "long" instead of "off_t" */
#ifndef EOVERFLOW
#define EOVERFLOW EFBIG
#endif

/** ==> zzip_filesize
 * 64on32 compability
 */
long
zzip_filesize32(int fd)
{
    if (sizeof(zzip_off_t) == sizeof(long)) {
        return zzip_filesize(fd);
    }
    else {
        off_t off = zzip_filesize(fd);
        if (off >= 0) {
            register long off32 = off;
            if (off32 == off)
                return off32;
            errno = EOVERFLOW;
        }
        return -1;
    }
}

/* keep these at the end of the file */
#if defined ZZIP_LARGEFILE_RENAME && defined EOVERFLOW
/* DLL compatibility layer - so that 32bit code can link with a 64on32 too */
#undef zzip_filesize

long
zzip_filesize(int fd)
{
    return zzip_filesize32(fd);
}

/* ignoring zzip_init_io32 */
/* ignoring zzip_get_default_io32 */

#endif