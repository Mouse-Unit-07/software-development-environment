#--------------------------------- FILE INFO ----------------------------------#
# Filename           : utilities.cmake                                         #
#                                                                              #
# cmake file defining functions that invoke supplemental utilities for when    #
# building for Windows                                                         #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)

# ------------------------------------------------------------------------------
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
            # hello-world:
            -I ${CMAKE_SOURCE_DIR}/src/hello_world # Example for Hello World project

            # c:
            ${CMAKE_SOURCE_DIR}/src/main.c
            # cpp:
            # ${CMAKE_SOURCE_DIR}/src/main.cpp

            ${ALL_TEST_SOURCES}
            > "${CPPCHECK_REPORT}" 2>&1
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Running Cppcheck (output -> ${CPPCHECK_REPORT})"
        VERBATIM
    )
endfunction()

# ------------------------------------------------------------------------------
# Formatting: clang-format
function(create_clang_format_build_target)
    get_property(ALL_TEST_SOURCES GLOBAL PROPERTY ALL_TEST_SOURCES)

    message(STATUS "ALL_TEST_SOURCES: ${ALL_TEST_SOURCES}")

    set(CL_FORMAT_OUTPUT_DIR "${CMAKE_SOURCE_DIR}/build/clang-format-output")

    list(LENGTH ALL_TEST_SOURCES NUM_FORMAT_FILES)
    message(STATUS "clang-format will process ${NUM_FORMAT_FILES} files")

    set(FORMAT_COMMANDS
        COMMAND ${CMAKE_COMMAND} -E echo "Formatting ${NUM_FORMAT_FILES} files..."
        COMMAND ${CMAKE_COMMAND} -E remove_directory "${CL_FORMAT_OUTPUT_DIR}"
        COMMAND ${CMAKE_COMMAND} -E make_directory "${CL_FORMAT_OUTPUT_DIR}"
        COMMAND ${CMAKE_COMMAND} -E copy
            "${CMAKE_SOURCE_DIR}/platforms/windows/utilities/.clang-format"
            "${CL_FORMAT_OUTPUT_DIR}/.clang-format"
    )

    foreach(src ${ALL_TEST_SOURCES})
        file(RELATIVE_PATH rel_path "${CMAKE_SOURCE_DIR}" "${src}")
        set(dst "${CL_FORMAT_OUTPUT_DIR}/${rel_path}")

        get_filename_component(dst_dir "${dst}" DIRECTORY)

        list(APPEND FORMAT_COMMANDS
            COMMAND ${CMAKE_COMMAND} -E make_directory "${dst_dir}"
            COMMAND ${CMAKE_COMMAND} -E copy "${src}" "${dst}"
            COMMAND clang-format -i
                -style=file
                -assume-filename="${CMAKE_SOURCE_DIR}/platforms/windows/utilities/dummy.cpp"
                "${dst}"
        )
    endforeach()

    add_custom_target(format_sources
        ${FORMAT_COMMANDS}
        COMMENT "Generating formatted copies"
        VERBATIM
    )
endfunction()
