#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file to build a software project for micromouse               #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(micromouse_software_project LANGUAGES C CXX)

option(TARGET_AVR32 "Build for AVR32 MCU" OFF)
option(TARGET_WINDOWS "Build for Windows (unit tests)" OFF)

include("${CMAKE_SOURCE_DIR}/src/platforms.cmake")

# \/=== Enable your project's tests here
set(ENABLE_HELLO_WORLD_TESTS ON) # Example for Hello World project

enable_testing()

if(TARGET_AVR32 AND SUPPORTS_AVR32)
    add_subdirectory(platforms/avr32)
elseif(TARGET_AVR32 AND NOT SUPPORTS_AVR32)
    message(FATAL_ERROR "...Aborting- project does not support AVR32 build")
endif()

if(TARGET_WINDOWS AND SUPPORTS_WINDOWS)
    add_subdirectory(platforms/windows)
elseif(TARGET_WINDOWS AND NOT SUPPORTS_WINDOWS)
    message(FATAL_ERROR "...Aborting- project does not support Windows build")
endif()

add_subdirectory(src)

if(TARGET_WINDOWS AND SUPPORTS_WINDOWS)
    create_cppcheck_build_target()
    create_clang_format_build_target()
endif()
