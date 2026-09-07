cmake_minimum_required(VERSION 3.20)
project(test_loop_tau C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR ${CMAKE_SOURCE_DIR}/deps)

include(FetchContent)

FetchContent_Declare(
  tau
  GIT_REPOSITORY https://github.com/jasmcaus/tau.git
  GIT_TAG 0bfd1868dc9deb4b8fea1cd71b249f109020b11a
)

set(TAU_BUILDINTERNALTESTS OFF CACHE BOOL "" FORCE)
set(TAU_BUILDTHIRDPARTYTESTS OFF CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(tau)

add_executable(test_loop test.cpp)

target_compile_options(test_loop PRIVATE -O3)

target_link_libraries(test_loop PRIVATE Tau::Tau)
