/*
 * The mem_disk cache will parse the central information of a zip archive
 * and store it internally. One the one hand it allows to find files
 * faster - no disk access is required and endian conversion is not
 * needed. If zzip is compiled with zip extensions then it is about
 * the only way to build maintainable code around the zip format.
 *
 * Note that 64bit support is almost entirely living in extension 
 * blocks as well as different character encodings and file access
 * control bits that are mostly platform specific.
 *
 * Author:
 *    Guido Draheim <guidod@gmx.de>
 * 
 * Copyright (c) 1999,2000,2001,2002,2003 Guido Draheim
 *          All rights reserved,
 *          use under the restrictions of the 
 *          Lesser GNU General Public License
 *          or alternatively the restrictions 
 *          of the Mozilla Public License 1.1
 */
#define _ZZIP_MEM_DISK_PRIVATE 1

#include <zzip/lib.h>                                  /* archive handling */
#include <zzip/file.h>
#include <zzip/format.h>
#include <zzip/fetch.h>

#include <stdlib.h>
#include <stdio.h>

#include <zzip/mmapped.h>
#include <zzip/memdisk.h>

#define ___ {
#define ____ }

static const char* error[] = {
    "Ok",
#   define _zzip_mem_disk_open_fail 1
    "zzip_mem_disk_open: zzip_disk_open did fail",
#   define _zzip_mem_disk_fdopen_fail 2
    "zzip_mem_disk_fdopen: zzip_disk_mmap did fail"
};

struct _zzip_mem_disk_entry {
    struct _zzip_mem_disk_entry* zz_next;
    char* zz_name;
    char* zz_data;
    int zz_flags;
    int zz_compr;
    long zz_crc32;
    zzip_off_t zz_csize;
    zzip_off_t zz_usize;
    zzip_off_t zz_offset;
    int zz_diskstart;
    int zz_filetype;
    char* zz_comment;
    size_t zz_extcount;
    struct _zzip_mem_disk_extra* zz_extras;
};

struct _zzip_mem_disk_extra {
    int   zz_datatype;
    int   zz_datasize;
    char* zz_data;
};

static ZZIP_MEM_DISK_ENTRY* _zzip_new
zzip_mem_disk_entry_new(ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry);
static void
zzip_mem_disk_entry_free(ZZIP_MEM_DISK_ENTRY* _zzip_restrict item);



/** create new diskdir handle. 
 *  wraps underlying zzip_disk_open. */
ZZIP_MEM_DISK* _zzip_new
zzip_mem_disk_open(char* filename)
{
    ZZIP_DISK* disk = zzip_disk_open(filename);
    if (! disk) { perror(error[_zzip_mem_disk_open_fail]); return 0; }
    ___ ZZIP_MEM_DISK* dir = calloc(1, sizeof(*dir)); 
    zzip_mem_disk_load(dir, disk);
    return dir; ____;
}

/** create new diskdir handle. 
 *  wraps underlying zzip_disk_open. */
ZZIP_MEM_DISK* _zzip_new
zzip_mem_disk_fdopen(int fd)
{
    ZZIP_DISK* disk = zzip_disk_mmap(fd);
    if (! disk) { perror(error[_zzip_mem_disk_fdopen_fail]); return 0; }
    ___ ZZIP_MEM_DISK* dir = calloc(1, sizeof(*dir)); 
    zzip_mem_disk_load(dir, disk);
    return dir; ____;
}

/** parse central dir.
 *  creates an internal copy of each entry converted to the local platform.
 */
int
zzip_mem_disk_load(ZZIP_MEM_DISK* dir, ZZIP_DISK* disk)
{
    if (dir->list) zzip_mem_disk_unload(dir);
    ___ struct zzip_disk_entry* entry = zzip_disk_findfirst(disk);
    for (; entry ; entry = zzip_disk_findnext(disk, entry)) {
	ZZIP_MEM_DISK_ENTRY* item = zzip_mem_disk_entry_new(disk, entry);
	if (dir->last) { dir->last->zz_next = item; }
	else { dir->list = item; }; dir->last = item;
    } ____;
    dir->disk = disk;
    return 0;
}

/** convert a zip disk entry to internal format.
 * creates a new item parsing the information out of the various places
 * in the zip archive. This is a good place to extend functionality if
 * you have a project with extra requirements as you can push more bits
 * right into the diskdir_entry for later usage in higher layers.
 */
ZZIP_MEM_DISK_ENTRY* _zzip_new
zzip_mem_disk_entry_new(ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry) 
{
    ZZIP_MEM_DISK_ENTRY* item = calloc(1, sizeof(*item));
    struct zzip_file_header* header = 
	zzip_disk_entry_to_file_header(disk, entry);
    /*  there is a number of duplicated information in the file header
     *  or the disk entry block. Theoretically some part may be missing
     *  that exists in the other, so each and every item would need to
     *  be checked. However, we assume that the "always-exists" fields
     *  do either (a) exist both and have the same value or (b) the bits
     *  in the disk entry are correct. Only the variable fields are 
     *  checked in both places: file name, file comment, extra blocks.
     *  From mmapped.c we do already have two helper functions for that:
     */
    item->zz_comment =   zzip_disk_entry_strdup_comment(disk, entry);
    item->zz_name =      zzip_disk_entry_strdup_name(disk, entry);
    item->zz_data =      zzip_file_header_to_data(header);
    item->zz_flags =     zzip_disk_entry_get_flags(entry);
    item->zz_compr =     zzip_disk_entry_get_compr(entry);
    item->zz_crc32 =     zzip_disk_entry_get_crc32(entry);
    item->zz_csize =     zzip_disk_entry_get_csize(entry);
    item->zz_usize =     zzip_disk_entry_get_usize(entry);
    item->zz_diskstart = zzip_disk_entry_get_diskstart(entry);
    item->zz_filetype =  zzip_disk_entry_get_filetype(entry);

    { /* scanning the extra blocks and building a fast-access table. */
	size_t count = 0; struct _zzip_mem_disk_extra* cache;
	int   len = zzip_file_header_get_extras(header);
	char* extras = zzip_file_header_to_extras(header);
	while (len > 0) {
	    struct zzip_extra_block* ext = (struct zzip_extra_block*) extras;
	    int size = zzip_extra_block_sizeto_end(ext);
	    len -= size; extras += size; count ++;
	}
	len = zzip_disk_entry_get_extras(entry);
	extras = zzip_disk_entry_to_extras(entry);
	while (len > 0) {
	    struct zzip_extra_block* ext = (struct zzip_extra_block*) extras;
	    int size = zzip_extra_block_sizeto_end(ext);
	    len -= size; extras += size; count ++;
	}
	cache = calloc(count, sizeof(struct _zzip_mem_disk_extra));
	if (item->zz_extras) free(item->zz_extras);
	item->zz_extras = cache;
	item->zz_extcount = count;
	/* ... */
	count = 0;
	len = zzip_file_header_get_extras(header);
	extras = zzip_file_header_to_extras(header);
	while (len > 0) {
	    struct zzip_extra_block* ext = (struct zzip_extra_block*) extras;
	    cache[count].zz_data = extras;
	    cache[count].zz_datatype = zzip_extra_block_get_datatype(ext);
	    cache[count].zz_datasize = zzip_extra_block_get_datasize(ext);
	    ___ register int size = zzip_extra_block_sizeto_end(ext);
	    len -= size; extras += size; count ++; ____;
	}
	len = zzip_disk_entry_get_extras(entry);
	extras = zzip_disk_entry_to_extras(entry);
	while (len > 0) {
	    struct zzip_extra_block* ext = (struct zzip_extra_block*) extras;
	    cache[count].zz_data = extras;
	    cache[count].zz_datatype = zzip_extra_block_get_datatype(ext);
	    cache[count].zz_datasize = zzip_extra_block_get_datasize(ext);
	    ___ register int size = zzip_extra_block_sizeto_end(ext);
	    len -= size; extras += size; count ++; ____;
	}
    }

    { /* scanning the extra blocks for platform specific extensions. */
	register size_t count;
	for (count = 0; count < item->zz_extcount; count++) {
	    /* "http://www.pkware.com/company/standards/appnote/" */
	    switch (item->zz_extras[count].zz_datatype) {
	    case 0x0001: { /* ZIP64 extended information extra field */
		struct {
		    char z_datatype[2]; /* Tag for this "extra" block type */
		    char z_datasize[2]; /* Size of this "extra" block */
		    char z_usize[8]; /* Original uncompressed file size */
		    char z_csize[8]; /* Size of compressed data */
		    char z_offset[8]; /* Offset of local header record */
		    char z_diskstart[4]; /* Number of the disk for file start*/
		} *block = (void*) item->zz_extras[count].zz_data;
		item->zz_usize  =    __zzip_get64(block->z_usize);
		item->zz_csize  =    __zzip_get64(block->z_csize);
		item->zz_offset =    __zzip_get64(block->z_offset);
		item->zz_diskstart = __zzip_get32(block->z_diskstart);
	    } break;
	    case 0x0007: /* AV Info */
	    case 0x0008: /* Reserved for future Unicode file name data (PFS) */
	    case 0x0009: /* OS/2 */
	    case 0x000a: /* NTFS */
	    case 0x000c: /* OpenVMS */
	    case 0x000d: /* Unix */
	    case 0x000e: /* Reserved for file stream and fork descriptors */
	    case 0x000f: /* Patch Descriptor */
	    case 0x0014: /* PKCS#7 Store for X.509 Certificates */
	    case 0x0015: /* X.509 Certificate ID and Signature for file */
	    case 0x0016: /* X.509 Certificate ID for Central Directory */
	    case 0x0017: /* Strong Encryption Header */
	    case 0x0018: /* Record Management Controls */
	    case 0x0019: /* PKCS#7 Encryption Recipient Certificate List */
	    case 0x0065: /* IBM S/390, AS/400 attributes - uncompressed */
	    case 0x0066: /* Reserved for IBM S/390, AS/400 attr - compressed */
	    case 0x07c8: /* Macintosh */
	    case 0x2605: /* ZipIt Macintosh */
	    case 0x2705: /* ZipIt Macintosh 1.3.5+ */
	    case 0x2805: /* ZipIt Macintosh 1.3.5+ */
	    case 0x334d: /* Info-ZIP Macintosh */
	    case 0x4341: /* Acorn/SparkFS  */
	    case 0x4453: /* Windows NT security descriptor (binary ACL) */
	    case 0x4704: /* VM/CMS */
	    case 0x470f: /* MVS */
	    case 0x4b46: /* FWKCS MD5 (see below) */
	    case 0x4c41: /* OS/2 access control list (text ACL) */
	    case 0x4d49: /* Info-ZIP OpenVMS */
	    case 0x4f4c: /* Xceed original location extra field */
	    case 0x5356: /* AOS/VS (ACL) */
	    case 0x5455: /* extended timestamp */
	    case 0x554e: /* Xceed unicode extra field */
	    case 0x5855: /* Info-ZIP Unix (original, also OS/2, NT, etc) */
	    case 0x6542: /* BeOS/BeBox */
	    case 0x756e: /* ASi Unix */
	    case 0x7855: /* Info-ZIP Unix (new) */
	    case 0xfd4a: /* SMS/QDOS */
		break;
	    }
	}
    }
    return item;
}
    
void
zzip_mem_disk_entry_free(ZZIP_MEM_DISK_ENTRY* _zzip_restrict item) 
{
    if (item) {
	if (item->zz_extras) free(item->zz_extras);
	free (item);
    }
}

void
zzip_mem_disk_unload(ZZIP_MEM_DISK* dir)
{
    ZZIP_MEM_DISK_ENTRY* item = dir->list;
    while (item) {
	ZZIP_MEM_DISK_ENTRY* next = item->zz_next;
	zzip_mem_disk_entry_free(item); item = next;
    }
    dir->list = dir->last = 0; dir->disk = 0;
}

void
zzip_mem_disk_close(ZZIP_MEM_DISK* _zzip_restrict dir) 
{
    if (dir) {
	zzip_mem_disk_unload (dir);
	zzip_disk_close(dir->disk);
	free (dir);
    }
}
