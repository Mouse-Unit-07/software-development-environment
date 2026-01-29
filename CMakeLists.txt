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

add_subdirectory(src)

if(TARGET_AVR32)
    if(SUPPORTS_AVR32)
        add_subdirectory(cmake/avr32)
    else()
        message(FATAL_ERROR "...Aborting- project does not support AVR32 build")
    endif()
endif()

if(TARGET_WINDOWS)
    if(SUPPORTS_WINDOWS)
        enable_testing()

        # \/=== Add each of your library test directories
        add_subdirectory(src/hello_world/tests) # Example for Hello World project

        add_subdirectory(cmake/tests)
    else()
        message(FATAL_ERROR "...Aborting- project does not support Windows build")
    endif()
endif()
