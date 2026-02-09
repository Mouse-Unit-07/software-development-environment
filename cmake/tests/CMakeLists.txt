#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for Windows build                                        #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(windows_build LANGUAGES C CXX)

include(FetchContent)
FetchContent_Declare(
    CppUTest
    GIT_REPOSITORY git@github.com:cpputest/cpputest.git
    GIT_TAG master
)
FetchContent_MakeAvailable(CppUTest)

# Static Analysis: Cppcheck
set(CPPCHECK_OUTPUT_DIR "${CMAKE_SOURCE_DIR}/build/cppcheck-output")
set(CPPCHECK_REPORT     "${CPPCHECK_OUTPUT_DIR}/cppcheck-report.txt")

function(create_cppcheck_build_target)
    message(STATUS "ALL_TEST_SOURCES: ${ALL_TEST_SOURCES}")

    add_custom_target(cppcheck
        COMMAND ${CMAKE_COMMAND} -E make_directory "${CPPCHECK_OUTPUT_DIR}"
        COMMAND cppcheck
            --enable=all
            --inconclusive
            --quiet
            --std=c99
            --force
            --inline-suppr
            --suppress=missingIncludeSystem
            -I ${CMAKE_SOURCE_DIR}/src

            # \/=== Add each of your library directories
            -I ${CMAKE_SOURCE_DIR}/src/hello_world # Example for Hello World project
            
            ${CMAKE_SOURCE_DIR}/src/main.c
            ${ALL_TEST_SOURCES}
            > "${CPPCHECK_REPORT}" 2>&1
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Running Cppcheck (output -> ${CPPCHECK_REPORT})"
        VERBATIM
    )
endfunction()

# Formatting: clang-format
function(create_clang_format_build_target)
    message(STATUS "ALL_TEST_SOURCES: ${ALL_TEST_SOURCES}")

    set(FORMATTED_SOURCES "")
    foreach(src ${ALL_TEST_SOURCES})
        file(RELATIVE_PATH rel_path "${CMAKE_SOURCE_DIR}" "${src}")
        set(formatted_file "${CMAKE_SOURCE_DIR}/build/clang-format-output/${rel_path}")
        list(APPEND FORMATTED_SOURCES "${formatted_file}")

        get_filename_component(formatted_file_dir "${formatted_file}" DIRECTORY)

        add_custom_command(
            OUTPUT "${formatted_file}"
            COMMAND ${CMAKE_COMMAND} -E make_directory "${formatted_file_dir}"
            COMMAND ${CMAKE_COMMAND} -E copy_if_different "${src}" "${formatted_file}"
            COMMAND clang-format -i -style=file:"${CMAKE_SOURCE_DIR}/cmake/utilities/.clang-format" "${formatted_file}"
            DEPENDS "${src}"
            COMMENT "Formatting ${rel_path} -> ${formatted_file}"
        )
    endforeach()

    add_custom_target(format_sources DEPENDS ${FORMATTED_SOURCES})
endfunction()

# Run functions
create_cppcheck_build_target()
create_clang_format_build_target()