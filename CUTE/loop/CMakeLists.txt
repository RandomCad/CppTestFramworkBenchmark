cmake_minimum_required(VERSION 3.14)
project(cute_loop_benchmark CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
set(FETCHCONTENT_BASE_DIR ${CMAKE_SOURCE_DIR}/deps)

# CUTE (https://github.com/PeterSommerlad/CUTE) is a pure header library with
# no CMakeLists.txt of its own, so FetchContent only needs to populate the
# source tree; there is nothing to add_subdirectory().
FetchContent_Declare(
  cute
  GIT_REPOSITORY https://github.com/PeterSommerlad/CUTE.git
  GIT_TAG        065a05b5cc4deaca066972a76fc39c900d905460
)

if(FETCHCONTENT_FULLY_DISCONNECTED AND NOT EXISTS "${FETCHCONTENT_BASE_DIR}/cute-src/cute/cute.h")
  message(FATAL_ERROR
    "FETCHCONTENT_FULLY_DISCONNECTED=ON but CUTE sources are not present in "
    "${FETCHCONTENT_BASE_DIR}/cute-src. Configure once without that flag to "
    "populate ./deps/, then reconfigure disconnected.")
endif()

FetchContent_MakeAvailable(cute)

add_executable(test_loop main.cpp test.cpp)
target_include_directories(test_loop PRIVATE ${cute_SOURCE_DIR}/cute)
target_compile_options(test_loop PRIVATE -O3)
