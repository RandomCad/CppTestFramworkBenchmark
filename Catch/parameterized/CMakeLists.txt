cmake_minimum_required(VERSION 3.14)
project(test_parameterized_project CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(FETCHCONTENT_BASE_DIR "${CMAKE_SOURCE_DIR}/deps" CACHE PATH "Base directory for FetchContent sources" FORCE)

include(FetchContent)

if(FETCHCONTENT_FULLY_DISCONNECTED)
    if(NOT EXISTS "${FETCHCONTENT_BASE_DIR}/catch2-src/CMakeLists.txt")
        message(FATAL_ERROR
            "FETCHCONTENT_FULLY_DISCONNECTED is ON but Catch2 sources were not "
            "found in ${FETCHCONTENT_BASE_DIR}/catch2-src. Configure once with "
            "-DFETCHCONTENT_FULLY_DISCONNECTED=OFF to populate ./deps first.")
    endif()
endif()

FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.7.1
)
FetchContent_MakeAvailable(Catch2)

add_executable(test_parameterized test.cpp)
target_compile_options(test_parameterized PRIVATE -O3)
target_link_libraries(test_parameterized PRIVATE Catch2::Catch2WithMain)
