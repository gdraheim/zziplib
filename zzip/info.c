
/*
 * Author:
 *      Guido Draheim <guidod@gmx.de>
 *
 * Copyright (c) Guido Draheim, use under copyleft (LGPL,MPL)
 */

#include <zzip/lib.h> /* exported... */
#include <zzip/file.h>
#include <zzip/format.h>

#ifdef ZZIP_HAVE_SYS_STAT_H
#include <sys/stat.h>
#else
#include <stdio.h>
#include <stdlib.h>
#endif

/** get errror status.
 *  This function just returns dir->errcode of the ZZIP_DIR handle
 *  see: => zzip_dir_open, => zzip_dir_open, => zzip_readdir, => zzip_dir_read
 */
int
zzip_error(ZZIP_DIR* dir)
{
    return dir->errcode;
}

/** => zzip_error
 *  This function just does dir->errcode = errcode
 */
void
zzip_seterror(ZZIP_DIR* dir, int errcode)
{
    dir->errcode = errcode;
}

/** get handle.
 * This function will just return the fp->dir value.
 *
 * If a ZZIP_FILE is contained within a zip-file that one will be a valid
 * pointer, otherwise a NULL is returned and the ZZIP_FILE wraps a real file.
 */
ZZIP_DIR*
zzip_dirhandle(ZZIP_FILE* fp)
{
    return fp->dir;
}

/** => zzip_dirhandle
 *  This function will just return dir->fd
 *
 * If a ZZIP_DIR does point to a zipfile then the file-descriptor of that
 * zipfile is returned, otherwise a NULL is returned and the ZZIP_DIR wraps
 * a real directory DIR (if you have dirent on your system).
 */
int
zzip_dirfd(ZZIP_DIR* dir)
{
    return dir->fd;
}

#define LENGTH(x) (sizeof(x) / sizeof(*x))
static const char* comprlevel[] = {"stored", "shrunk", "redu:1", "redu:2", "redu:3", "redu:4",
                                   "impl:N", "toknze", "defl:N", "defl:B", "impl:B"};

/** compr name.
 * This function returns the static const string of the known compression methods,
 * Unknown id values will return just "zipped" as the string code.
 */
zzip_char_t*
zzip_compr_str(int compr)
{
    if (0 <= compr && (unsigned) compr < LENGTH(comprlevel)) {
        return comprlevel[compr];
    }
    else if (0 < compr && compr < 256) {
        return "zipped";
    }
    else {
#ifdef S_ISDIR
        if (S_ISDIR(compr))
            return "directory";
#endif
#ifdef S_ISCHR
        if (S_ISCHR(compr))
            return "is/chr";
#endif
#ifdef S_ISBLK
        if (S_ISBLK(compr))
            return "is/blk";
#endif
#ifdef S_ISFIFO
        if (S_ISFIFO(compr))
            return "is/fifo";
#endif
#ifdef S_ISSOCK
        if (S_ISSOCK(compr))
            return "is/sock";
#endif
#ifdef S_ISLNK
        if (S_ISLNK(compr))
            return "is/lnk";
#endif
        return "special";
    }
}

/** => zzip_file_real
 * This function checks if the ZZIP_DIR-handle is wrapping
 * a real directory or a zip-archive.
 * Returns 1 for a stat'able directory, and 0 for a handle to zip-archive.
 */
int
zzip_dir_real(ZZIP_DIR* dir)
{
    return dir->realdir != 0;
}

/** check real or zipped file.
 * This function checks if the ZZIP_FILE-handle is wrapping
 * a real file or a zip-contained file.
 * Returns 1 for a stat'able file, and 0 for a file inside a zip-archive.
 */
int
zzip_file_real(ZZIP_FILE* fp)
{
    return fp->dir == 0; /* ie. not dependent on a zip-arch-dir  */
}

/** => zzip_file_real
 * This function returns the posix DIR* handle (if one exists).
 * Check before with => zzip_dir_real if the
 * the ZZIP_DIR points to a real directory.
 */
void*
zzip_realdir(ZZIP_DIR* dir)
{
    return dir->realdir;
}

/** => zzip_file_real
 * This function returns the posix file descriptor (if one exists).
 * Check before with => zzip_file_real if the
 * the ZZIP_FILE points to a real file.
 */
int
zzip_realfd(ZZIP_FILE* fp)
{
    return fp->fd;
}
