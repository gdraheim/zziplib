#ifndef __ZZIP_MEMDISK_H
#define __ZZIP_MEMDISK_H

#include <zzip/mmapped.h>

typedef struct _zzip_mem_disk ZZIP_MEM_DISK;
typedef struct _zzip_mem_disk_entry ZZIP_MEM_DISK_ENTRY;

struct _zzip_mem_disk {
    ZZIP_DISK* disk;
#  ifdef _ZZIP_MEM_DISK_PRIVATE
    ZZIP_MEM_DISK_ENTRY* list;
    ZZIP_MEM_DISK_ENTRY* last;
#  endif
};

#ifndef zzip_mem_disk_extern
#define zzip_mem_disk_extern
#endif

zzip_mem_disk_extern ZZIP_MEM_DISK* _zzip_new
zzip_mem_disk_open (char* filename);
zzip_mem_disk_extern ZZIP_MEM_DISK* _zzip_new
zzip_mem_disk_fdopen (int fd);
zzip_mem_disk_extern void 
zzip_mem_disk_close (ZZIP_MEM_DISK* _zzip_restrict dir);

zzip_mem_disk_extern int 
zzip_mem_disk_load (ZZIP_MEM_DISK* dir, ZZIP_DISK* disk);
zzip_mem_disk_extern void 
zzip_mem_disk_unload (ZZIP_MEM_DISK* dir);

#ifdef USE_INLINE
_zzip_inline ZZIP_DISK_ENTRY*
zzip_mem_disk_findfirst(ZZIP_MEM_DISK* dir) {
    return zzip_disk_findfirst(dir->disk); }
_zzip_inline ZZIP_DISK_ENTRY*
zzip_mem_disk_findnext(ZZIP_MEM_DISK* dir, ZZIP_DISK_ENTRY* entry) {
    return zzip_mem_disk_findnext(dir->disk, entry);
}
#else
#define zzip_mem_disk_findfirst(__dir) \
             zzip_disk_findfirst((__dir)->disk)
#define zzip_mem_disk_findnext(__dir,__entry) \
            zzip_disk_findnext((__dir)->disk,(__entry))
#endif

#ifdef USE_INLINE
_zzip_inline char* _zzip_new
zzip_mem_disk_entry_strdup_name(ZZIP_MEM_DISK* dir, 
                                ZZIP_DISK_ENTRY* entry) {
    return zzip_disk_entry_strdup_name(dir->disk, entry); }
_zzip_inline struct zzip_file_header*
zzip_mem_disk_entry_to_file_header(ZZIP_MEM_DISK* dir, 
				   ZZIP_DISK_ENTRY* entry) {
    return zzip_disk_entry_to_file_header(dir->disk, entry); }
_zzip_inline char*
zzip_mem_disk_entry_to_data(ZZIP_MEM_DISK* dir, ZZIP_DISK_ENTRY* entry) {
    return zzip_disk_entry_to_data(dir->disk, entry); }
#else
#define zzip_mem_disk_entry_strdup_name(__dir,__entry) \
            zzip_disk_entry_strdup_name((__dir)->disk,(__entry))
#define zzip_mem_disk_entry_to_file_header(__dir,__entry) \
            zzip_disk_entry_to_file_header((__dir)->disk,(__entry))
#define zzip_mem_disk_entry_to_data(__dir,__entry) \
            zzip_disk_entry_to_data((__dir)->disk,(__entry))
#endif

#ifdef USE_INLINE
_zzip_inline ZZIP_DISK_ENTRY*
zzip_mem_disk_findfile(ZZIP_MEM_DISK* dir, 
                       char* filename, ZZIP_DISK_ENTRY* after,
		       zzip_strcmp_fn_t compare) {
    return zzip_disk_findfile(dir->disk, filename, after, compare); }
_zzip_inline ZZIP_DISK_ENTRY*
zzip_mem_disk_findmatch(ZZIP_MEM_DISK* dir, 
                        char* filespec, ZZIP_DISK_ENTRY* after,
			zzip_fnmatch_fn_t compare, int flags) {
    return zzip_disk_findmatch(dir->disk, filespec, after, compare, flags); }
#else
#define zzip_mem_disk_findfile(__dir,__name,__after,__compare) \
            zzip_disk_findfile((__dir)->disk,(__name),(__after), \
                                                    (__compare))
#define zzip_mem_disk_findmatch(__dir,__spec,__after,__compare,__flags) \
            zzip_disk_findmatch((__dir)->disk,(__spec),(__after), \
                                           (__compare),(__flags))
#endif

#ifdef USE_INLINE
_zzip_inline ZZIP_DISK_FILE* _zzip_new
zzip_mem_disk_entry_fopen (ZZIP_MEM_DISK* dir, ZZIP_DISK_ENTRY* entry) {
    return zzip_disk_entry_fopen(dir->disk, entry); }
_zzip_inline ZZIP_DISK_FILE* _zzip_new
zzip_mem_disk_fopen (ZZIP_MEM_DISK* dir, char* filename) {
    return zzip_disk_fopen(dir->disk, filename); }
_zzip_inline _zzip_size_t
zzip_mem_disk_fread (void* ptr, _zzip_size_t size, _zzip_size_t nmemb,
                     ZZIP_DISK_FILE* file) {
    return zzip_disk_fread(ptr, size, nmemb, file); }
_zzip_inline int
zzip_mem_disk_fclose (ZZIP_DISK_FILE* file) {
    return zzip_disk_fclose(file); }
_zzip_inline int
zzip_mem_disk_feof (ZZIP_DISK_FILE* file) {
    return zzip_disk_feof(file); }
#else
#define zzip_mem_disk_entry_fopen(__dir,__entry) \
            zzip_disk_entry_fopen((__dir)->disk,(__entry))

#define zzip_mem_disk_fopen(__dir,__name) \
            zzip_disk_fopen((__dir)->disk,(__name))

#define zzip_mem_disk_fread(__ptr,__size,__nmemb,__file) \
            zzip_disk_fread((__ptr),(__size),(__nmemb),(__file))
#define zzip_mem_disk_fclose(__file) \
        zzip_disk_fclose((__file))
#define zzip_mem_disk_feof(__file) \
            zzip_disk_feof((__file))
#endif

#endif
