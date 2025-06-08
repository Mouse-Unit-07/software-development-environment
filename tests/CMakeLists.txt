#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for Windows build                                        #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(test_build_target LANGUAGES C CXX)

include(FetchContent)
FetchContent_Declare(
    CppUTest
    GIT_REPOSITORY https://github.com/cpputest/cpputest.git
    GIT_TAG master
)
FetchContent_MakeAvailable(CppUTest)

# Static Analysis: Cppcheck
function(create_cppcheck_build_target)
    message(STATUS "ALL_TEST_SOURCES: ${ALL_TEST_SOURCES}")

    add_custom_target(cppcheck
        COMMAND cppcheck
            --enable=all
            --inconclusive
            --quiet
            --std=c99
            --force
            --inline-suppr
            --suppress=missingIncludeSystem
            -I ${CMAKE_SOURCE_DIR}/src

            # \/ === ADD SOURCE SUBDIRECTORIES HERE === \/
            -I ${CMAKE_SOURCE_DIR}/src/hello_world
            
            ${CMAKE_SOURCE_DIR}/src/main.c
            ${ALL_TEST_SOURCES}
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Running Cppcheck on source and test files"
        VERBATIM
    )
endfunction()

# Formatting: clang-format
function(create_clang_format_build_target)
    message(STATUS "ALL_TEST_SOURCES: ${ALL_TEST_SOURCES}")

    set(FORMATTED_SOURCES "")
    foreach(src ${ALL_TEST_SOURCES})
        file(RELATIVE_PATH rel_path "${CMAKE_SOURCE_DIR}" "${src}")
        set(formatted_file "${CMAKE_BINARY_DIR}/clang-format-output/${rel_path}")
        list(APPEND FORMATTED_SOURCES "${formatted_file}")

        get_filename_component(formatted_file_dir "${formatted_file}" DIRECTORY)

        add_custom_command(
            OUTPUT "${formatted_file}"
            COMMAND ${CMAKE_COMMAND} -E make_directory "${formatted_file_dir}"
            COMMAND ${CMAKE_COMMAND} -E copy_if_different "${src}" "${formatted_file}"
            COMMAND clang-format -i -style=file "${formatted_file}"
            DEPENDS "${src}"
            COMMENT "Formatting ${rel_path} -> ${formatted_file}"
        )
    endforeach()

    add_custom_target(format_sources DEPENDS ${FORMATTED_SOURCES})
endfunction()

# run functions
create_cppcheck_build_target()
create_clang_format_build_target()