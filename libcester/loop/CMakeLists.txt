cmake_minimum_required(VERSION 3.14)
project(libcester_loop_benchmark CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps" CACHE PATH "Location for fetched dependency sources" FORCE)

include(FetchContent)

FetchContent_Declare(
    libcester
    GIT_REPOSITORY https://github.com/exoticlibraries/libcester.git
    GIT_TAG v0.4
)

# libcester is header-only and ships no CMakeLists.txt, so FetchContent only
# needs to populate ./deps/libcester-src; there is nothing to add_subdirectory().
set(LIBCESTER_SOURCE_DIR "${FETCHCONTENT_BASE_DIR}/libcester-src")
set(LIBCESTER_HEADER "${LIBCESTER_SOURCE_DIR}/include/exotic/cester.h")

if(FETCHCONTENT_FULLY_DISCONNECTED AND NOT EXISTS "${LIBCESTER_HEADER}")
    message(FATAL_ERROR
        "FETCHCONTENT_FULLY_DISCONNECTED is ON but ${LIBCESTER_HEADER} does not exist. "
        "Configure once without -DFETCHCONTENT_FULLY_DISCONNECTED=ON to fetch libcester into ./deps first.")
endif()

FetchContent_MakeAvailable(libcester)

add_executable(test_loop test.cpp)

target_include_directories(test_loop PRIVATE "${LIBCESTER_SOURCE_DIR}/include")

target_compile_options(test_loop PRIVATE -O3)
