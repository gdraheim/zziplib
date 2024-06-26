#ifndef UNZZIP_STATES_H
#define UNZZIP_STATES_H

/* DIAGNOSTICS according to the unzip(1) manpage */

#define EXIT_OK                      0
#define EXIT_WARNINGS                1
#define EXIT_ERRORS                  2
#define EXIT_FILEFORMAT              3
#define EXIT_ENOMEM                  4
#define EXIT_ENOTTY_FOR_PASSWORD     5
#define EXIT_ENOMEM_ZIP_TO_DISK      6
#define EXIT_ENOMEM_ZIP_TO_MEM       7
#define EXIT_ZIP_NOT_FOUND           9
#define EXIT_INVALID_OPTION          10
#define EXIT_FILE_NOT_FOUND          11
#define EXIT_DISKFULL                50
#define EXIT_EARLY_END_OF_FILE       51
#define EXIT_SIGTERM                 80
#define EXIT_UNSUPPORTED_COMPRESSION 81
#define EXIT_WRONG_PASSWORD          82

#endif
