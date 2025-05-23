/*
 * Author:
 *     Guido Draheim <guidod@gmx.de>
 *
 * Copyright (c) Guido Draheim, use under copyleft
 *
 *  the interfaces for the plugin_io system
 *
 * Using the following you can provide your own file I/O functions to
 * e.g. read data directly from memory, provide simple
 * "encryption"/"decryption" of on-disk .zip-files...
 * Note that this currently only provides a subset of the functionality
 * in zziplib. It does not attempt to provide any directory functions,
 * but if your program 1) only uses ordinary on-disk files and you
 * just want this for file obfuscation, or 2) you only access your
 * .zip archives using zzip_open & co., this is sufficient.
 *
 * Currently the default io are the POSIX functions, except
 * for 'filesize' that is zziplibs own provided zzip_filesize function,
 * using standard POSIX fd's. You are however free to replace this with
 * whatever data type you need, so long as you provide implementations
 * for all the functions, and the data type fits an int.
 *
 * all functions receiving ext_io are able to cope with both arguments
 * set to zero which will let them default to a ZIP ext and posix io.
 */
#ifndef _ZZIP_PLUGIN_H /* zzip-io.h */
#define _ZZIP_PLUGIN_H 1

#include <zzip/zzip.h>
#include <zzip/cdecl.h>

#ifdef __cplusplus
extern "C" {
#endif

/* we have renamed zzip_plugin_io.use_mmap to zzip_plugin_io.sys */
#define ZZIP_PLUGIN_IO_SYS 1

/* zzip_init_io flags : */
#define ZZIP_IO_USE_MMAP 1

/* just use sizeof(off_t) to initialize the bit-type */
#define ZZIP_IO_TYPE_DEFAULT 1
#define ZZIP_IO_SIZE_32BIT   4
#define ZZIP_IO_SIZE_64BIT   8
#define ZZIP_IO_SIZE_OFF_T   12

struct zzip_plugin_io { /* use "zzip_plugin_io_handlers" in applications !! */
    int (*open)(zzip_char_t* name, int flags, ...);
    int (*close)(int fd);
    zzip_ssize_t (*read)(int fd, void* buf, zzip_size_t len);
    zzip_off_t (*seeks)(int fd, zzip_off_t offset, int whence);
    zzip_off_t (*filesize)(int fd);
    long sys;
    long type;
    zzip_ssize_t (*write)(int fd, _zzip_const void* buf, zzip_size_t len);
};

typedef union _zzip_plugin_io {
    struct zzip_plugin_io fd;
    struct {
        void* padding[8];
    } ptr;
} zzip_plugin_io_handlers;

#define _zzip_plugin_io_handlers zzip_plugin_io_handlers

/* for backward compatibility, add the following to your application code:
 * #ifndef _zzip_plugin_io_handlers
 * #define _zzip_plugin_io_handlers struct zzip_plugin_io
 */
typedef zzip_plugin_io_handlers* zzip_plugin_io_handlers_t;

_zzip_export long
zzip_io_size_off_t() ZZIP_GNUC_PURE_CONST;

#ifdef ZZIP_LARGEFILE_RENAME
#define zzip_filesize       zzip_filesize64
#define zzip_get_default_io zzip_get_default_io64
#define zzip_init_io        zzip_init_io64
#endif

_zzip_export zzip_off_t
zzip_filesize(int fd);

/* get the default file I/O functions.
 *  This functions returns a pointer to an internal static structure.
 */
_zzip_export zzip_plugin_io_t
zzip_get_default_io(void);

/*
 * Initializes a zzip_plugin_io_t to the zziplib default io.
 * This is useful if you only want to override e.g. the 'read' function.
 * all zzip functions that can receive a zzip_plugin_io_t can
 * handle a zero pointer in that place and default to posix io.
 */
_zzip_export int
zzip_init_io(zzip_plugin_io_handlers_t io, int flags);

#ifdef __cplusplus
}
#endif

#endif
