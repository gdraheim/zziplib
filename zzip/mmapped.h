#ifndef _ZZIP_MMAPPED_H_
#define _ZZIP_MMAPPED_H_

#include <zzip/types.h>

typedef struct zzip_disk_file  ZZIP_DISK_FILE;
typedef struct zzip_disk       ZZIP_DISK;
typedef struct zzip_disk_entry ZZIP_DISK_ENTRY;

struct zzip_disk
{
    char* buffer;      /* start of mmapped area */
    char* endbuf;      /* end of mmapped area, buffer+buflen */
    char* reserved;    /* for later extensions */
    char* user;        /* free for applications */
    long  flags;       /* bit 0: findfile searches case-insensitive */
    long  mapped;      /* helper for mmap() wrappers of zzip/__mmap.h */
    long  unused;      /* for later extensions */
    long  code;        /* free for applications */
};

typedef 
int (*zzip_strcmp_fn_t)(char* _zzip_restrict, char* _zzip_restrict);
typedef 
int (*zzip_fnmatch_fn_t)(char* _zzip_restrict, char* _zzip_restrict, int);

#define zzip_disk_extern extern

zzip_disk_extern int
zzip_disk_init(ZZIP_DISK* disk, char* buffer, zzip_size_t buflen);

zzip_disk_extern ZZIP_DISK* _zzip_restrict
zzip_disk_new(void);

zzip_disk_extern ZZIP_DISK* _zzip_restrict
zzip_disk_mmap(int fd);

zzip_disk_extern int 
zzip_disk_munmap(ZZIP_DISK* disk);

zzip_disk_extern ZZIP_DISK*  _zzip_restrict
zzip_disk_open(char* filename);

zzip_disk_extern int
zzip_disk_close(ZZIP_DISK* disk);


zzip_disk_extern int
zzip_disk_init (ZZIP_DISK* disk, char* buffer, _zzip_size_t buflen);

zzip_disk_extern ZZIP_DISK_ENTRY*
zzip_disk_findfirst(ZZIP_DISK* disk);

zzip_disk_extern ZZIP_DISK_ENTRY*
zzip_disk_findnext(ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry);

char* _zzip_restrict
zzip_disk_entry_strdup_name(ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry);
struct zzip_file_header*
zzip_disk_entry_to_file_header(ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry);
char*
zzip_disk_entry_to_data(ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry);

zzip_disk_extern ZZIP_DISK_ENTRY*
zzip_disk_findfile(ZZIP_DISK* disk, 
		   char* filename, ZZIP_DISK_ENTRY* after,
		   zzip_strcmp_fn_t compare);
zzip_disk_extern ZZIP_DISK_ENTRY*
zzip_disk_findmatch(ZZIP_DISK* disk, 
		    char* filespec, ZZIP_DISK_ENTRY* after,
		    zzip_fnmatch_fn_t compare, int flags);


zzip_disk_extern ZZIP_DISK_FILE*
zzip_disk_entry_fopen (ZZIP_DISK* disk, ZZIP_DISK_ENTRY* entry);

zzip_disk_extern ZZIP_DISK_FILE*
zzip_disk_fopen (ZZIP_DISK* disk, char* filename);

zzip_disk_extern _zzip_size_t
zzip_disk_fread (void* ptr, _zzip_size_t size, _zzip_size_t nmemb,
		 ZZIP_DISK_FILE* file);
zzip_disk_extern int
zzip_disk_fclose (ZZIP_DISK_FILE* file);
int
zzip_disk_feof (ZZIP_DISK_FILE* file);

#endif

