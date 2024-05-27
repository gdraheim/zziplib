#ifndef __ZZIP_CDECL_H
#define __ZZIP_CDECL_H
#include <zzip/conf.h>

#ifdef ZZIP_HAVE_ANSIDECL_H
/* get originals from GCC */
#include <ansidecl.h>
#endif

#ifndef ZZIP_GNUC_ATLEAST
#if defined __GNUC__ && defined __GNUC_MINOR__
#define ZZIP_GNUC_ATLEAST(_M_, _N_) ((__GNUC__ << 10) + __GNUC_MINOR__ >= ((_M_) << 10) + (_N_))
#elif defined __GNUC__
#define ZZIP_GNUC_ATLEAST(_M_, _N_) ((__GNUC__ << 10) >= ((_M_) << 10))
#else
#define ZZIP_GNUC_ATLEAST(_M_, _N_) 0
#endif
#endif

/* func has no side effects, return value depends only on params and globals */
#ifndef ZZIP_GNUC_PURE
#ifdef ATTRIBUTE_PURE
#define ZZIP_GNUC_PURE ATTRIBUTE_PURE
#elif ZZIP_GNUC_ATLEAST(2, 8)
#define ZZIP_GNUC_PURE __attribute__((__pure__))
#else
#define ZZIP_GNUC_PURE
#endif
#endif

/* func has no side effects, return value depends only on params */
#ifndef ZZIP_GNUC_PURE_CONST
#ifdef ATTRIBUTE_PURE_CONST
#define ZZIP_GNUC_PURE_CONST ATTRIBUTE_CONST
#elif ZZIP_GNUC_ATLEAST(2, 4)
#define ZZIP_GNUC_PURE_CONST __attribute__((__const__))
#else
#define ZZIP_GNUC_PURE_CONST
#endif
#endif

/* typename / variable / function possibly unused */
#ifndef ZZIP_GNUC_UNUSED
#ifdef ATTRIBUTE_UNUSED
#define ZZIP_GNUC_UNUSED ATTRIBUTE_UNUSED
#elif ZZIP_GNUC_ATLEAST(2, 4)
#define ZZIP_GNUC_UNUSED __attribute__((__unused__))
#else
#define ZZIP_GNUC_UNUSED
#endif
#endif

/* obvious. btw, a noreturn-func should return void */
#ifndef ZZIP_GNUC_NORETURN
#ifdef ATTRIBUTE_NORETURN
#define ZZIP_GNUC_NORETURN ATTRIBUTE_NORETURN
#elif ZZIP_GNUC_ATLEAST(2, 5)
#define ZZIP_GNUC_NORETURN __attribute__((__noreturn__))
#else
#define ZZIP_GNUC_NORETURN
#endif
#endif

/* omit function from profiling with -finstrument-functions */
#ifndef ZZIP_GNUC_NO_INSTRUMENT
#ifdef ATTRIBUTE_NO_INSTRUMENT
#define ZZIO_GNUC_NO_INSTRUMENT ATTRIBUTE_NO_INSTRUMENT
#elif ZZIP_GNUC_ATLEAST(2, 4)
#define ZZIP_GNUC_NO_INSTRUMENT __attribute__((__no_instrument_function__))
#else
#define ZZIP_GNUC_NO_INSTRUMENT
#endif
#endif

/* all pointer args must not be null, and allow optimiztons based on the fact*/
#ifndef ZZIP_GNUC_NONNULL
#ifdef ATTRIBUTE_NONNULL
#define ZZIP_GNUC_NONNULL(_X_) ATTRIBUTE_NONNULL(_X_)
#elif ZZIP_GNUC_ATLEAST(3, 1)
#define ZZIP_GNUC_NONNULL(_X_) __attribute__((__nonnull__(_X_)))
#else
#define ZZIP_GNUC_NONNULL(_X_)
#endif
#endif

/* typename / function / variable is obsolete but still listed in headers */
#ifndef ZZIP_GNUC_DEPRECATED
#ifdef ATTRIBUTE_DEPRECATED
#define ZZIP_GNUC_DEPRECATED ATTRIBUTE_DEPRECATED
#elif ZZIP_GNUC_ATLEAST(3, 1)
#define ZZIP_GNUC_DEPRECATED __attribute__((deprecated))
#else
#define ZZIP_GNUC_DEPRECATED
#endif
#endif

#ifndef ZZIP_GNUC_FORMAT
#if ZZIP_GNUC_ATLEAST(2, 4)
#define ZZIP_GNUC_FORMAT(_X_) __attribute__((__format_arg__(_X_)))
#else
#define ZZIP_GNUC_FORMAT(_X_)
#endif
#endif

#ifndef ZZIP_GNUC_SCANF
#if ZZIP_GNUC_ATLEAST(2, 4)
#define ZZIP_GNUC_SCANF(_S_, _X_) __attribute__((__scanf__(_S_, _X_)))
#else
#define ZZIP_GNUC_SCANF(_S_, _X_)
#endif
#endif

#ifndef ZZIP_GNUC_PRINTF
#ifdef ATTRBIUTE_PRINTF
#define ZZIP_GNUC_PRINTF(_S_, _X_) ATTRIBUTE_PRINTF(_S_, _X_)
#elif ZZIP_GNUC_ATLEAST(2, 4)
#define ZZIP_GNUC_PRINTF(_S_, _X_) __attribute__((__printf__(_S_, _X_)))
#else
#define ZZIP_GNUC_PRINTF(_S_, _X_)
#endif
#endif

#ifndef ZZIP_GNUC_PACKED
#ifdef ATTRIBUTE_PACKED
#define ZZIP_GNUC_PACKED ATTRIBUTE_PACKED
#elif defined __GNUC__
#define ZZIP_GNUC_PACKED __attribute__((packed))
#else
#define ZZIP_GNUC_PACKED
#endif
#endif

#ifndef ZZIP_FUNCTION
#if ZZIP_GNUC_ATLEAST(2, 6)
#define ZZIP_FUNC     __FUNCTION__
#define ZZIP_FUNCTION __FUNCTION__
#elif defined __STDC_VERSION__ && __STDC_VERSION__ >= 199901L
#define ZZIP_FUNC     __func__
#define ZZIP_FUNCTION ""
#else
#define ZZIP_FUNC     0
#define ZZIP_FUNCTION ""
#endif
#endif

#ifndef ZZIP_STRING
#define ZZIP_STRING(_X_)  ZZIP_STRING_(_X_)
#define ZZIP_STRING_(_Y_) #_Y_
#endif

#ifndef ZZIP_DIM
#define ZZIP_DIM(_A_) (sizeof(_A_) / sizeof((_A_)[0]))
#endif

#if ! (defined ZZIP_FOR1 && defined ZZIP_END1)
#if defined sun || defined __sun__
#define ZZIP_FOR1 if (1)
#define ZZIP_END1 else(void) 0
#else
#define ZZIP_FOR1 do
#define ZZIP_END1 while (0)
#endif
#endif

#ifndef ZZIP_BRANCH_OVER
#if ZZIP_GNUC_ATLEAST(2, 96)
#define ZZIP_BRANCH_OVER(_X_) __builtin_expect((_X_), 0)
#else
#define ZZIP_BRANCH_OVER(_X_) (_X_)
#endif
#endif

#endif
