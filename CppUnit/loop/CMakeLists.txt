cmake_minimum_required(VERSION 3.14)
project(test_loop_cppunit CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR ${CMAKE_SOURCE_DIR}/deps)

include(FetchContent)

# Make FETCHCONTENT_FULLY_DISCONNECTED a hard configure-time error when
# ./deps/ hasn't been populated yet, instead of a warning followed by a
# build-time failure.
if(POLICY CMP0170)
  cmake_policy(SET CMP0170 NEW)
endif()

# Upstream CppUnit only ships an autotools build. This fork carries an
# equivalent CMake port of that same build (add_library(cppunit ...) from
# the identical sources) so the dependency can be consumed via plain
# FetchContent like every other framework here. It still declares
# cmake_minimum_required(VERSION 2.6); let it configure under modern CMake
# policies instead of failing outright.
set(CMAKE_POLICY_VERSION_MINIMUM 3.5 CACHE STRING "" FORCE)

FetchContent_Declare(
  cppunit
  GIT_REPOSITORY https://github.com/dlrdave/cppunit.git
  GIT_TAG 3c206b6a195d89e659862d88b56344018b85e4e4
)

FetchContent_MakeAvailable(cppunit)

add_executable(test_loop test.cpp main.cpp)

target_compile_options(test_loop PRIVATE -O3)

target_include_directories(test_loop PRIVATE
  ${cppunit_SOURCE_DIR}/include
  ${cppunit_BINARY_DIR}/include
)

target_link_libraries(test_loop PRIVATE cppunit)
