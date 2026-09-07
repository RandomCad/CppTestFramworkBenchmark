cmake_minimum_required(VERSION 3.24)
project(test_parameterized LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps" CACHE PATH "Base directory for FetchContent-managed dependencies" FORCE)

# Only build Boost.Test itself (plus whatever headers it transitively needs)
# out of the full Boost source tree, instead of the whole library set.
set(BOOST_INCLUDE_LIBRARIES test CACHE STRING "" FORCE)
set(BOOST_ENABLE_CMAKE ON CACHE BOOL "" FORCE)

FetchContent_Declare(
  boost
  URL https://archives.boost.io/release/1.86.0/source/boost_1_86_0.tar.gz
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)

FetchContent_MakeAvailable(boost)

add_executable(test_parameterized test.cpp)

target_link_libraries(test_parameterized PRIVATE Boost::test)

target_compile_options(test_parameterized PRIVATE -O3)
