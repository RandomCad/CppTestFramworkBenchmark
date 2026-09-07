cmake_minimum_required(VERSION 3.14)
project(test_loop CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps" CACHE PATH "Fetched content base directory" FORCE)

include(FetchContent)

FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.7.1
)

FetchContent_MakeAvailable(Catch2)

add_executable(test_loop test.cpp)
target_compile_options(test_loop PRIVATE -O3)
target_link_libraries(test_loop PRIVATE Catch2::Catch2WithMain)
