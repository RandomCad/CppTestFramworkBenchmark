cmake_minimum_required(VERSION 3.24)
project(test_loop_boosttest CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps" CACHE PATH "Base directory for FetchContent sources" FORCE)

include(FetchContent)

FetchContent_Declare(
  boost
  URL https://archives.boost.io/release/1.84.0/source/boost_1_84_0.tar.gz
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  SOURCE_SUBDIR does-not-exist # header-only use: never add_subdirectory into Boost's own build
)

# FetchContent silently no-ops when the source dir is absent and downloads are
# disabled, so fail configure explicitly instead of pretending to succeed.
if(FETCHCONTENT_FULLY_DISCONNECTED AND NOT EXISTS "${FETCHCONTENT_BASE_DIR}/boost-src/boost/test/included/unit_test.hpp")
  message(FATAL_ERROR
    "Boost sources not found under ${FETCHCONTENT_BASE_DIR}/boost-src. "
    "Configure once without -DFETCHCONTENT_FULLY_DISCONNECTED=ON to populate ./deps first.")
endif()

FetchContent_MakeAvailable(boost)

add_executable(test_loop test.cpp)
target_include_directories(test_loop PRIVATE "${boost_SOURCE_DIR}")
target_compile_options(test_loop PRIVATE -O3)
