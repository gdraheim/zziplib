/*
 * These routines are fully independent from the traditional zzip
 * implementation. They assume a readonly mmapped sharedmem block
 * representing a complete zip file. The functions show how to 
 * parse the structure, find files and return a decoded bytestream.
 *
 * These routines are a bit simple and really here for documenting
 * the way to access a zip file. The complexity of zip access comes
 * from staggered reading of bytes and reposition of a filepointer in
 * a big archive with lots of files and long compressed datastreams.
 * Plus varaints of drop-in stdio replacements, obfuscation routines,
 * auto fileextensions, drop-in dirent replacements, and so on...
 *
 * Author: 
 *      Guido Draheim <guidod@gmx.de>
 *
 * Copyright (c) 2003,2004 Guido Draheim
 *          All rights reserved,
 *          use under the restrictions of the 
 *          Lesser GNU General Public License
 *          or alternatively the restrictions 
 *          of the Mozilla Public License 1.1
 */

#include <zzip/mmapped.h>
#include <stdlib.h>
#include <sys/stat.h>

#ifdef ZZIP_HAVE_FNMATCH_H
#include <fnmatch.h>
#endif

#if   defined ZZIP_HAVE_UNISTD_H
#include <unistd.h>
#elif defined ZZIP_HAVE_IO_H
#include <io.h>
#endif

#if   defined ZZIP_HAVE_STRING_H
#include <string.h>
#elif defined ZZIP_HAVE_STRINGS_H
#include <strings.h>
#endif

#include <zlib.h>
#include <zzip/format.h>
#include <zzip/fetch.h>
#include <zzip/__mmap.h>

#if __STDC_VERSION__+0 > 199900L
#define ___
#define ____
#else
#define ___ {
#define ____ }
#endif

/** => zzip_disk_mmap
 * This function does primary initialization of a disk-buffer struct.
 */
int
zzip_disk_init(ZZIP_DISK* disk, char* buffer, zzip_size_t buflen)
{
    disk->buffer = buffer;
    disk->endbuf = buffer+buflen;
    disk->reserved = 0;
    disk->flags = 0;
    disk->mapped = 0;
    /* do not touch disk->user */
    /* do not touch disk->code */
    return 0;
}

/** => zzip_disk_mmap
 * This function allocates a new disk-buffer with => malloc(3)
 */
ZZIP_DISK* _zzip_restrict
zzip_disk_new(void)
{
    ZZIP_DISK* disk = malloc(sizeof(disk));
    if (! disk) return disk;
    zzip_disk_init (disk, 0, 0);
    return disk;
}

/** mmap a file
 * This function uses the given file-descriptor to detect the length of the 
 * file and calls the system => mmap(2) to put it in main memory. If it is
 * successful then a newly allocated ZZIP_DISK* is returned with 
 * disk->buffer pointing to the mapview of the zipdisk content.
 */
ZZIP_DISK* _zzip_restrict
zzip_disk_mmap(int fd)
{
    struct stat st;
    if (fstat (fd, &st) || !st.st_size) return 0;
    ___ ZZIP_DISK* disk = zzip_disk_new (); if (! disk) return 0;
    disk->buffer = _zzip_mmap (& zzip->mapped, fd, 0, st.st_size);
    if (disk->buffer == MAP_FAILED) { free (disk); return 0; }
    disk->endbuf = disk->buffer + st.st_size;
    return disk; ____;
}

/** => zzip_disk_mmap
 * This function is the inverse of => zzip_disk_mmap and using the system
 * munmap(2) on the buffer area and => free(3) on the ZZIP_DISK structure.
 */
int
zzip_disk_munmap(ZZIP_DISK* disk)
{
    if (! disk) return 0;
    _zzip_munmap (disk->mapped, disk->buffer, disk->endbuf-disk->buffer);
    free (disk);
    return 0;
}

/** => zzip_disk_mmap
 * open the given archive by name and turn the filehandle to 
 * => zzip_disk_mmap for bringing it to main memory. If it can not
 * be => mmap(2)'ed then we slurp the whole file into a newly => malloc(2)'ed
 * memory block. Only if that fails too then we return null. Since handling
 * of disk->buffer is ambigous it should not be snatched away please.
 */
ZZIP_DISK* _zzip_restrict
zzip_disk_open(char* filename)
{
#  ifndef O_BINARY
#  define O_BINARY 0
#  endif
    struct stat st;
    if (stat (filename, &st) || !st.st_size) return 0;
    ___ int fd = open (filename, O_RDONLY|O_BINARY);
    if (fd <= 0) return 0;
    ___ ZZIP_DISK* disk = zzip_disk_mmap (fd);
    if (disk) return disk;
    ___ char* buffer = malloc (st.st_size);
    if (! buffer) return 0;
    if ((st.st_size == read (fd, buffer, st.st_size)) &&
	(disk = zzip_disk_new ())) 
    {
	disk->buffer = buffer;
	disk->endbuf = buffer+st.st_size;
	disk->mapped = -1;
    }else free (buffer);
    return disk; ____;____;____;
}

int
zzip_disk_close(ZZIP_DISK* disk)
{
    if (! disk) return 0;
    if (disk->mapped != -1) return zzip_disk_munmap (disk);
    free (disk->buffer);
    free (disk);
    return 0;
}

/* ====================================================================== */

#ifdef ZZIP_HAVE_STRNDUP
#define _zzip_strndup strndup
#else
static char* _zzip_restrict _zzip_strndup(char* p, int maxlen)
{
    if (! p) return 0;
    ___ int l = strlen (p);
    if (l > maxlen) l = maxlen;
    ___ char* r = malloc (l+1);
    if (! r) return r;
    memcpy (r, p, l);
    r[l] = '\0';
    return r; ____;____;
}
#endif

#if defined ZZIP_HAVE_STRCASECMP || defined strcasecmp
#define _zzip_strcasecmp strcasecmp
#else
static int _zzip_strcasecmp(char* __zzip_restrict a, char* _zzip_restrict b)
{
    if (! a) return (b) ? 1 : 0;
    if (! b) return -1;
    while (1) 
    {
	int v = tolower(*a) - tolower(*b);
	if (v) return v;
	if (! *a) return 1;
	if (! *b) return -1;
	a++; b++;
    }
}
#endif


char*
zzip_disk_entry_to_data(ZZIP_DISK* disk, struct zzip_disk_entry* entry)
{
    struct zzip_file_header* file = 
	zzip_disk_entry_to_file_header(disk, entry);
    if (file) return zzip_file_header_to_data (file);
    return 0;
}

struct zzip_file_header*
zzip_disk_entry_to_file_header(ZZIP_DISK* disk, struct zzip_disk_entry* entry)
{
    char* file_header = /* (struct zzip_file_header*) */
	(disk->buffer + zzip_disk_entry_fileoffset (entry));
    if (disk->buffer > file_header || file_header >= disk->endbuf) 
	return 0;
    return (struct zzip_file_header*) file_header;
}

char* _zzip_restrict
zzip_disk_entry_strdup_name(ZZIP_DISK* disk, struct zzip_disk_entry* entry)
{
    if (! disk || ! entry) return 0;

    ___ char* name; zzip_size_t len;
    struct zzip_file_header* file;
    if ((len = zzip_disk_entry_namlen (entry)))
	name = zzip_disk_entry_to_filename (entry);
    else if ((file = zzip_disk_entry_to_file_header (disk, entry)) &&
	     (len = zzip_file_header_namlen (file)))
	name = zzip_file_header_to_filename (file);
    else
	return 0;

    if (disk->buffer > name || name+len > disk->endbuf)
	return 0;
    
    return  _zzip_strndup (name, len); ____;
}

/* ====================================================================== */

/**
 * This function should be called first to find the entry point of
 * a zip central directory. The disk_trailer should be _last_ in the 
 * file area, its position would be at a fixed offset from the end of 
 * the file area if not for the comment field allowed to be of variable 
 * length. However, we disregard the disk_trailer info here assuming a
 * singledisk archive.
 * 
 * For an actual means, we are going to search backwards from the end 
 * of the mmaped block looking for the PK-magic signature of a 
 * disk_trailer. If we see one then we check the rootseek value to
 * find the first disk_entry of the root central directory. If we find
 * the correct PK-magic signature there then we are going to return that.
 *
 * The retun value is a pointer to the first zzip_disk_entry being
 * within the bounds of the file area specified by the arguments. If
 * no disk_trailer was found then null is returned, and we only accept
 * a disk_trailer with a seekvalue that points to a disk_entry and both
 * parts have valid PK-magic parts.
 */
struct zzip_disk_entry*
zzip_disk_findfirst(ZZIP_DISK* disk)
{
    if (disk->buffer > disk->endbuf-sizeof(struct zzip_disk_trailer))
	return 0;
    ___ char* p = disk->endbuf-sizeof(struct zzip_disk_trailer);
    for (; p >= disk->buffer ; p--)
    {
	if (! zzip_disk_trailer_check_magic(p)) continue;
	___ char* root = /* (struct zzip_disk_entry*) */ disk->buffer + 
	    zzip_disk_trailer_get_rootseek ((struct zzip_disk_trailer*)p);
	if (root > p) 
	{   /* the first disk_entry is after the disk_trailer? can't be! */
	    zzip_size_t rootsize =
		zzip_disk_trailer_get_rootsize ((struct zzip_disk_trailer*)p);
	    if (disk->buffer+rootsize > p) continue;
	    /* a common brokeness that can be fixed: we just assume that the 
	     * central directory was written directly before the trailer: */
	    root = disk->buffer+rootsize;
	}
	if (root < disk->buffer) continue;
	if (zzip_disk_entry_check_magic(root)) 
	    return (struct zzip_disk_entry*) root;
	____;
    }____;
    return 0;
}

/**
 * This function takes an existing disk_entry in the central root directory
 * (e.g. from zzip_disk_findfirst) and returns the next entry within in
 * the given bounds of the mmapped file area.
 */
struct zzip_disk_entry*
zzip_disk_findnext(ZZIP_DISK* disk, struct zzip_disk_entry* entry)
{
    if ((char*)entry < disk->buffer || 
	(char*)entry > disk->endbuf-sizeof(entry) ||
	zzip_disk_entry_sizeto_end (entry) > 64*1024)
	return 0;
    entry = zzip_disk_entry_to_next_entry (entry);
    if ((char*)entry > disk->endbuf-sizeof(entry) ||
	zzip_disk_entry_sizeto_end (entry) > 64*1024 ||
	zzip_disk_entry_skipto_end (entry) + sizeof(entry) > disk->endbuf)
	return 0;
    else
	return entry;
}

/**
 * given a filename as an additional argument, find the corresponding
 * file_header living right before the file_data. For this function it
 * is unimportant whether the filename was given at the disk_entry or
 * the file_header. The compare-function is usually strcmp or strcasecmp
 * or perhaps strcoll, if null then strcmp is used. - use null as argument
 * for "after"-entry when searching the first matching entry.
 */
struct zzip_disk_entry*
zzip_disk_findfile(ZZIP_DISK* disk, char* filename, 
		    struct zzip_disk_entry* after, zzip_strcmp_fn_t compare)
{
    struct zzip_disk_entry* entry = (! after ? zzip_disk_findfirst (disk) 
				     : zzip_disk_findnext (disk, after));
    if (! compare) 
	compare = (zzip_strcmp_fn_t)( (disk->flags&1) ? 
				      (_zzip_strcasecmp) : (strcmp));
    for (; entry ; entry = zzip_disk_findnext (disk, entry))
    {
	/* filenames within zip files are often not null-terminated! */
	char* realname = zzip_disk_entry_strdup_name (disk, entry);
	if (realname && ! compare(filename, realname))
	{
	    free (realname);
	    return entry;
	}
	free (realname);
    }
    return 0;
}

#ifdef ZZIP_HAVE_FNMATCH_H
#define _zzip_fnmatch fnmatch
# ifdef FNM_CASEFOLD
# define _zzip_fnmatch_CASEFOLD FNM_CASEFOLD
# else
# define _zzip_fnmatch_CASEFOLD 0
# endif
#else
# define _zzip_fnmatch_CASEFOLD 0
static int _zzip_fnmatch(char* pattern, char* string, int flags)
{ 
    puts ("<zzip:strcmp>");
    return strcmp (pattern, string); 
}
#endif

/**
 * This function uses a compare-function with an additional argument
 * and it is called just like fnmatch(3) from POSIX.2 AD:1993), i.e.
 * the argument filespec first and the ziplocal filename second with
 * the integer-flags put in as third to the indirect call. If the
 * platform has fnmatch available then null-compare will use that one
 * and otherwise we fall back to mere strcmp, so if you need fnmatch
 * searching then please provide an implementation somewhere else.
 * - use null as argument for "after"-entry when searching the first 
 * matching entry.
 */
struct zzip_disk_entry*
zzip_disk_findmatch(ZZIP_DISK* disk, char* filespec, 
		    struct zzip_disk_entry* after,
		    zzip_fnmatch_fn_t compare, int flags)
{
    struct zzip_disk_entry* entry = (! after ? zzip_disk_findfirst (disk) 
				     : zzip_disk_findnext (disk, after));
    if (! compare) { 
	compare = (zzip_fnmatch_fn_t) _zzip_fnmatch; 
	if (disk->flags&1) disk->flags |= _zzip_fnmatch_CASEFOLD;
    }
    for (; entry ; entry = zzip_disk_findnext (disk, entry))
    {
	/* filenames within zip files are often not null-terminated! */
	char* realname = zzip_disk_entry_strdup_name(disk, entry);
	if (realname && ! compare(filespec, realname, flags))
	{
	    free (realname);
	    return entry;
	}
	free (realname);
    }
    return 0;
}

/* ====================================================================== */

/**
 * typedef struct zzip_disk_file ZZIP_DISK_FILE;
 */
struct zzip_disk_file
{
    char* buffer;                      /* fopen disk->buffer */
    char* endbuf;                      /* fopen disk->endbuf */
    struct zzip_file_header* header;   /* fopen detected header */
    zzip_size_t avail;                 /* memorized for checks on EOF */
    z_stream zlib;                     /* for inflated blocks */
    char* stored;                      /* for stored blocks */
};

/** => zzip_disk_fopen
 *
 * the ZZIP_DISK_FILE* is rather simple in just encapsulating the
 * arguments given to this function plus a zlib deflate buffer.
 * After _open()ing the given file you can subsequently _read()
 * bytes from the stream. Do not forget to _close() the _FILE
 * or otherwise risk memory leakage.
 */
ZZIP_DISK_FILE*
zzip_disk_entry_fopen (ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry)
{
    ZZIP_DISK_FILE* file = malloc(sizeof(ZZIP_DISK_FILE));
    if (! file) return file;
    file->buffer = disk->buffer;
    file->endbuf = disk->endbuf;
    file->header = zzip_disk_entry_to_file_header (disk, entry);
    if (! file->header) { free (file); return 0; }
    file->avail = zzip_file_header_usize (file->header);

    if (! file->avail || zzip_file_header_data_stored (file->header))
    { file->stored = zzip_file_header_to_data (file->header); return file; }

    file->zlib.opaque = 0;
    file->zlib.zalloc = Z_NULL;
    file->zlib.zfree = Z_NULL;
    file->zlib.avail_in = zzip_file_header_csize (file->header);
    file->zlib.next_in = zzip_file_header_to_data (file->header);

    if (! zzip_file_header_data_deflated (file->header) ||
	inflateInit (& file->zlib) != Z_OK)
    { free (file); return 0; }

    return file;
}

/** 
 * This function opens a file found by name.
 */
ZZIP_DISK_FILE*
zzip_disk_fopen (ZZIP_DISK* disk, char* filename)
{
    ZZIP_DISK_ENTRY* entry = zzip_disk_findfile (disk, filename, 0, 0);
    if (! entry) return 0; else return zzip_disk_entry_fopen (disk, entry);
}


/**
 * This function reads more bytes into the output buffer specified as
 * arguments. The return value is null on eof or error.
 */
zzip_size_t
zzip_disk_fread (void* ptr, zzip_size_t sized, zzip_size_t nmemb,
		 ZZIP_DISK_FILE* file)
{
     zzip_size_t size = sized*nmemb;
    if (size > file->avail) size = file->avail;
    if (file->stored)
    {
	memcpy (ptr, file->stored, size);
	file->stored += size;
	file->avail -= size;
	return size;
    }
    
    file->zlib.avail_out = sized*nmemb;
    file->zlib.next_out = ptr;
    ___ zzip_size_t total_old = file->zlib.total_out;
    ___ int err = inflate (& file->zlib, Z_NO_FLUSH);
    if (err == Z_STREAM_END)
	file->avail = 0;
    else if (err == Z_OK)
	file->avail -= file->zlib.total_out - total_old;
    else
	return 0;
    return file->zlib.total_out - total_old;
    ____;____;
}

int
zzip_disk_fclose (ZZIP_DISK_FILE* file)
{
    if (! file->stored)
	inflateEnd (& file->zlib);
    free (file);
    return 0;
}

int
zzip_disk_feof (ZZIP_DISK_FILE* file)
{
    return ! file || ! file->avail;
}
