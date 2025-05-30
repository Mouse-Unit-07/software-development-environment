#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file to build a simple Hello World project                    #
# Targets AVR32 MCU and Windows for unit testing                               #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(hello_world_project LANGUAGES C CXX)

option(TARGET_MCU "Build for AVR32 MCU" OFF)
option(TARGET_WINDOWS "Build for Windows (unit tests)" OFF)

add_subdirectory(src)

if(TARGET_MCU)
    add_subdirectory(avr32)
endif()

if(TARGET_WINDOWS)
    enable_testing()

    # ADD TEST SUBDIRECTORIES HERE
    add_subdirectory(src/hello_world/tests)

    add_subdirectory(tests)
endif()
