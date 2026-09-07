cmake_minimum_required(VERSION 3.18)
project(test_parameterized CXX C)

# ---------------------------------------------------------------------------
# Criterion (https://github.com/Snaipe/Criterion) ships a Meson build, not a
# CMake one, so it cannot be pulled in via FetchContent_Declare +
# FetchContent_MakeAvailable (there is no CMakeLists.txt to add_subdirectory).
# We fall back to ExternalProject_Add, driving Meson/Ninja purely through
# CMake COMMAND arguments (no shell scripts involved), and reproduce the same
# FETCHCONTENT_BASE_DIR / FETCHCONTENT_FULLY_DISCONNECTED toggle that
# FetchContent would normally offer.
# ---------------------------------------------------------------------------
include(ExternalProject)

if(NOT DEFINED FETCHCONTENT_BASE_DIR OR FETCHCONTENT_BASE_DIR STREQUAL "")
    set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps")
endif()
set(FETCHCONTENT_BASE_DIR "${FETCHCONTENT_BASE_DIR}" CACHE PATH "Base directory for fetched dependencies" FORCE)

option(FETCHCONTENT_FULLY_DISCONNECTED "Skip downloading/updating dependencies; reuse what is already in FETCHCONTENT_BASE_DIR" OFF)

set(CRITERION_SOURCE_DIR "${FETCHCONTENT_BASE_DIR}/criterion-src")
set(CRITERION_BINARY_DIR "${FETCHCONTENT_BASE_DIR}/criterion-build")
set(CRITERION_INSTALL_DIR "${FETCHCONTENT_BASE_DIR}/criterion-install")

if(FETCHCONTENT_FULLY_DISCONNECTED)
    if(NOT EXISTS "${CRITERION_SOURCE_DIR}/meson.build")
        message(FATAL_ERROR
            "FETCHCONTENT_FULLY_DISCONNECTED is ON but no Criterion checkout was "
            "found at ${CRITERION_SOURCE_DIR}. Configure once with this flag OFF "
            "so it can be fetched into ${FETCHCONTENT_BASE_DIR}, then reconfigure "
            "disconnected.")
    endif()
    set(_criterion_download_args "")
else()
    set(_criterion_download_args
        GIT_REPOSITORY https://github.com/Snaipe/Criterion.git
        GIT_TAG v2.4.3
        GIT_SHALLOW TRUE
    )
endif()

find_program(MESON_EXECUTABLE meson REQUIRED)
find_program(NINJA_EXECUTABLE ninja REQUIRED)

ExternalProject_Add(criterion_ext
    ${_criterion_download_args}
    SOURCE_DIR "${CRITERION_SOURCE_DIR}"
    UPDATE_DISCONNECTED ${FETCHCONTENT_FULLY_DISCONNECTED}
    CONFIGURE_COMMAND ${MESON_EXECUTABLE} setup <BINARY_DIR> <SOURCE_DIR>
        --prefix=${CRITERION_INSTALL_DIR}
        --libdir=lib
        --buildtype=release
        --wrap-mode=default
        -Dtests=false
        -Dsamples=false
        -Dcxx-support=enabled
    BUILD_COMMAND ${NINJA_EXECUTABLE} -C <BINARY_DIR>
    INSTALL_COMMAND ${NINJA_EXECUTABLE} -C <BINARY_DIR> install
    BINARY_DIR "${CRITERION_BINARY_DIR}"
    BUILD_BYPRODUCTS "${CRITERION_INSTALL_DIR}/lib/${CMAKE_SHARED_LIBRARY_PREFIX}criterion${CMAKE_SHARED_LIBRARY_SUFFIX}"
)

# The include dir does not exist until criterion_ext has actually built, but
# CMake requires INTERFACE_INCLUDE_DIRECTORIES to exist at configure time for
# an imported target, so create the (empty, for now) placeholder up front.
file(MAKE_DIRECTORY "${CRITERION_INSTALL_DIR}/include")

add_library(criterion SHARED IMPORTED GLOBAL)
set_target_properties(criterion PROPERTIES
    IMPORTED_LOCATION "${CRITERION_INSTALL_DIR}/lib/${CMAKE_SHARED_LIBRARY_PREFIX}criterion${CMAKE_SHARED_LIBRARY_SUFFIX}"
    INTERFACE_INCLUDE_DIRECTORIES "${CRITERION_INSTALL_DIR}/include"
)
add_dependencies(criterion criterion_ext)

add_executable(test_parameterized test.cpp)
add_dependencies(test_parameterized criterion_ext)
target_compile_options(test_parameterized PRIVATE -O3)
target_link_libraries(test_parameterized PRIVATE criterion)
set_target_properties(test_parameterized PROPERTIES
    BUILD_RPATH "${CRITERION_INSTALL_DIR}/lib"
)
