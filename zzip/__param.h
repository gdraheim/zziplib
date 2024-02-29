#ifndef __ZZIP_INTERNAL_PARAM_H
#define __ZZIP_INTERNAL_PARAM_H

#include <zzip/conf.h>

#ifdef ZZIP_HAVE_SYS_PARAM_H
#include <sys/param.h> /* PATH_MAX */
#endif

#ifndef PATH_MAX
#ifdef MAX_PATH /* windows */
#define PATH_MAX MAX_PATH
#else
#define PATH_MAX 512
#endif
#endif

#endif
