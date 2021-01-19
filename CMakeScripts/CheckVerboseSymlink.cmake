# This module checks for a verbose symlink command which will be used
# on unix to symlink shared libraries to older compatible versions.
#
# __author__ = "Guido Draheim"
# __license__ = "MIT OR CC0-1.0"

macro(find_ln_svf)
    if(NOT DEFINED ln_svf)
        execute_process(COMMAND bash -c "ln --help"
            OUTPUT_VARIABLE ln_verbose_help
            ERROR_QUIET
        )
        string(FIND "${ln_verbose_help}" "verbose" ln_verbose_found)
        if(${ln_verbose_found} STREQUAL "-1")
            set(ln_svf "ln -sf")
        else()
            set(ln_svf "ln -svf")
        endif()
        message(STATUS "Can symlink verbose with: ${ln_svf}")
    endif()
endmacro()

macro(find_shared_library_ln_svf)
    if(CMAKE_SHARED_LIBRARY_SONAME_C_FLAG)
        find_ln_svf()
    endif()
endmacro()
