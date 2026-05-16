#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for Windows build                                        #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(windows_build LANGUAGES C CXX)

# ------------------------------------------------------------------------------
# Windows compiler flags
set(CMAKE_C_FLAGS
    "--coverage -ffile-prefix-map=${CMAKE_SOURCE_DIR}/= -DWINDOWS_BUILD"
    CACHE STRING "" FORCE
)

set(CMAKE_CXX_FLAGS
    "--coverage -ffile-prefix-map=${CMAKE_SOURCE_DIR}/= -DWINDOWS_BUILD"
    CACHE STRING "" FORCE
)

set(CMAKE_C_FLAGS_DEBUG
    "-O0 -g3 -Wall -DDEBUG"
    CACHE STRING "" FORCE
)

set(CMAKE_CXX_FLAGS_DEBUG
    "-O0 -g3 -Wall -DDEBUG"
    CACHE STRING "" FORCE
)
# ------------------------------------------------------------------------------

include(FetchContent)

set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(CPPUTEST_MEM_LEAK_DETECTION_DISABLED ON CACHE BOOL "" FORCE)

FetchContent_Declare(
    CppUTest
    GIT_REPOSITORY git@github.com:cpputest/cpputest.git
    GIT_TAG master
)
FetchContent_MakeAvailable(CppUTest)

include(utilities/utilities.cmake)
