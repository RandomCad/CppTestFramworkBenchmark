cmake_minimum_required(VERSION 3.14)
project(gtest_parameterized_benchmark CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR ${CMAKE_SOURCE_DIR}/deps)

include(FetchContent)

if(FETCHCONTENT_FULLY_DISCONNECTED AND NOT EXISTS ${FETCHCONTENT_BASE_DIR}/googletest-src/CMakeLists.txt)
    message(FATAL_ERROR
        "FETCHCONTENT_FULLY_DISCONNECTED=ON but no GoogleTest source was found "
        "in ${FETCHCONTENT_BASE_DIR}/googletest-src. Configure once without "
        "this flag first so FetchContent can populate ./deps/.")
endif()

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.15.2
)

set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(googletest)

add_executable(test_parameterized test.cpp)

target_link_libraries(test_parameterized PRIVATE gtest_main)

target_compile_options(test_parameterized PRIVATE -O3)
