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

add_subdirectory(src)

if(TARGET_AVR32)
    add_subdirectory(avr32)
endif()

if(TARGET_WINDOWS)
    enable_testing()

    # \/=== Add each of your library test directories
    add_subdirectory(src/hello_world/tests) # Example for Hello World project

    add_subdirectory(tests)
endif()
