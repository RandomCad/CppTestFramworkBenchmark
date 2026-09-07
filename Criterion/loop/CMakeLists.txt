cmake_minimum_required(VERSION 3.14)
project(criterion_loop_benchmark CXX)

include(FetchContent)

set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps" CACHE PATH "" FORCE)

# Criterion (https://github.com/Snaipe/Criterion) builds with Meson, not CMake
# -- it ships no CMakeLists.txt, so it cannot be add_subdirectory()'d the way
# FetchContent_MakeAvailable() expects. We fetch its official prebuilt Linux
# x86_64 release archive instead and consume the plain include/lib tree it
# contains directly, still driven entirely by FetchContent.
if(POLICY CMP0135)
  cmake_policy(SET CMP0135 NEW)
endif()
if(POLICY CMP0169)
  cmake_policy(SET CMP0169 OLD)
endif()

FetchContent_Declare(
  criterion
  URL      https://github.com/Snaipe/Criterion/releases/download/v2.4.3/criterion-2.4.3-linux-x86_64.tar.xz
  URL_HASH SHA256=f1b3dd5186783dcdd63433c1facd3b4d6af5244a151057370b53bdda80f16121
)

FetchContent_GetProperties(criterion)
if(NOT criterion_POPULATED)
  FetchContent_Populate(criterion)
endif()

set(CRITERION_INCLUDE_DIR "${criterion_SOURCE_DIR}/include")
set(CRITERION_LIB_DIR "${criterion_SOURCE_DIR}/lib")

if(NOT EXISTS "${CRITERION_INCLUDE_DIR}/criterion/criterion.h" OR
   NOT EXISTS "${CRITERION_LIB_DIR}/libcriterion.so")
  message(FATAL_ERROR
    "Criterion was not found under ${criterion_SOURCE_DIR}. "
    "Configure once without FETCHCONTENT_FULLY_DISCONNECTED so it can be "
    "fetched into ${CMAKE_SOURCE_DIR}/deps, or place it there manually before "
    "reconfiguring with FETCHCONTENT_FULLY_DISCONNECTED=ON.")
endif()

add_executable(test_loop test.cpp)

target_include_directories(test_loop PRIVATE "${CRITERION_INCLUDE_DIR}")
target_link_directories(test_loop PRIVATE "${CRITERION_LIB_DIR}")
target_link_libraries(test_loop PRIVATE criterion)

target_compile_features(test_loop PRIVATE cxx_std_17)
target_compile_options(test_loop PRIVATE -O3)

set_target_properties(test_loop PROPERTIES
  BUILD_RPATH "${CRITERION_LIB_DIR}"
)
