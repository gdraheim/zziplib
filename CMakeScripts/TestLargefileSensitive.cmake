# simplified largefile support detection for unix (very different from AC_SYS_LARGEFILE)
# returns ${VARIABLE} 1 if largefile support is present - having an off_t (and probably off64_t)
# returns ${VARIABLE}_SENSTITIVE if off_t changes size with -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES
# returns ${VARIABLE}_FLAGS for compiler -Dflags needed to get 64-bit off_t

MACRO(TEST_LARGEFILE_SENSITIVE VARIABLE)
  if(NOT DEFINED ${VARIABLE})
    message(STATUS "Testing off_t sizes with or without -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES")
    set(CMAKE_REQUIRED_DEFINITIONS -D_LARGEFILE_SOURCE -Doff_t_DEF=off_t)
    check_type_size( off_t_DEF LARGEFILE_SIZEOF_OFF_T_DEF )
    set(CMAKE_REQUIRED_DEFINITIONS -D_LARGEFILE_SOURCE -Doff_t_D64=off_t -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES)
    check_type_size( off_t_D64 LARGEFILE_SIZEOF_OFF_T_D64 )
    set(CMAKE_REQUIRED_DEFINITIONS -D_LARGEFILE64_SOURCE)
    check_type_size( off64_t LARGEFILE_SIZEOF_OFF64_T )

    SET(${VARIABLE} 0 CACHE INTERNAL "System has largefile support" FORCE)
    SET(${VARIABLE}_SENSITIVE 0 CACHE INTERNAL "System is largefile sensitive" FORCE)
    SET(${VARIABLE}_FLAGS "" CACHE INTERNAL "Compiler flags for largefile support" FORCE)
    if(LARGEFILE_SIZEOF_OFF_T_DEF)
       message(STATUS "Testing off_t found sizeof(off_t)=${LARGEFILE_SIZEOF_OFF_T_DEF} and BITS=64 sizeof(off_t)=${LARGEFILE_SIZEOF_OFF_T_D64}")
       SET(${VARIABLE} 1 CACHE INTERNAL "System has largefile support" FORCE)
      if(NOT LARGEFILE_SIZEOF_OFF_T_DEF EQUAL LARGEFILE_SIZEOF_OFF_T_D64)
        SET(${VARIABLE}_SENSITIVE 1 CACHE INTERNAL "System is largefile sensitive" FORCE)
        message(STATUS "System is large file sensitive - need to rename symbols to xx64")
        SET(${VARIABLE}_FLAGS -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES)
    endif()
   endif()
  endif()
endmacro(TEST_LARGEFILE_SENSITIVE)