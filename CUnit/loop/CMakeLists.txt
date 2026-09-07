cmake_minimum_required(VERSION 3.14)
project(cunit_loop_benchmark CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Fetch CUnit (CMake-native "cunity" fork) into ./deps ----------------

set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps" CACHE PATH "" FORCE)

include(FetchContent)

# Make a missing, un-populated source directory a hard configure error when
# FETCHCONTENT_FULLY_DISCONNECTED=ON, instead of only a warning.
if(POLICY CMP0170)
    cmake_policy(SET CMP0170 NEW)
endif()

set(CUNIT_DISABLE_TESTS TRUE CACHE INTERNAL "Disable CUnit tests")
set(CUNIT_DISABLE_EXAMPLES TRUE CACHE INTERNAL "Disable CUnit examples")

FetchContent_Declare(
    cunit
    GIT_REPOSITORY https://gitlab.com/cunity/cunit.git
    GIT_TAG 67cee3f06e4bed117738ae4acf0b98f711a621ad
)

FetchContent_MakeAvailable(cunit)

# --- Benchmark executable -------------------------------------------------

add_executable(test_loop test.cpp main.cpp)

target_compile_options(test_loop PRIVATE -O3)
target_link_libraries(test_loop PRIVATE cunit)
