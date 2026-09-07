cmake_minimum_required(VERSION 3.14)
project(test_loop_gtest CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR ${CMAKE_SOURCE_DIR}/deps)

include(FetchContent)

if(POLICY CMP0170)
  cmake_policy(SET CMP0170 NEW)
endif()

FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.15.2
)

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(googletest)

add_executable(test_loop test.cpp)

target_compile_options(test_loop PRIVATE -O3)

target_link_libraries(test_loop PRIVATE gtest gtest_main)
