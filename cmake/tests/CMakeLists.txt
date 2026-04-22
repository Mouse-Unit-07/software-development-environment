#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for Windows build                                        #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(windows_build LANGUAGES C CXX)

include(FetchContent)

set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(CPPUTEST_MEM_LEAK_DETECTION_DISABLED ON CACHE BOOL "" FORCE)

FetchContent_Declare(
    CppUTest
    GIT_REPOSITORY git@github.com:cpputest/cpputest.git
    GIT_TAG master
)
FetchContent_MakeAvailable(CppUTest)

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
            -I ${CMAKE_SOURCE_DIR}/src/hello_world # Example for Hello World project
            
            ${CMAKE_SOURCE_DIR}/src/main.c
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
    message(STATUS "ALL_TEST_SOURCES: ${ALL_TEST_SOURCES}")

    set(CL_FORMAT_OUTPUT_DIR "${CMAKE_SOURCE_DIR}/build/clang-format-output")

    list(LENGTH ALL_TEST_SOURCES NUM_FORMAT_FILES)
    message(STATUS "clang-format will process ${NUM_FORMAT_FILES} files")

    set(FORMAT_COMMANDS
        COMMAND ${CMAKE_COMMAND} -E echo "Formatting ${NUM_FORMAT_FILES} files..."
        COMMAND ${CMAKE_COMMAND} -E remove_directory "${CL_FORMAT_OUTPUT_DIR}"
        COMMAND ${CMAKE_COMMAND} -E make_directory "${CL_FORMAT_OUTPUT_DIR}"
        COMMAND ${CMAKE_COMMAND} -E copy
            "${CMAKE_SOURCE_DIR}/cmake/utilities/.clang-format"
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
                -assume-filename="${CMAKE_SOURCE_DIR}/cmake/utilities/dummy.cpp"
                "${dst}"
        )
    endforeach()

    add_custom_target(format_sources
        ${FORMAT_COMMANDS}
        COMMENT "Generating formatted copies"
        VERBATIM
    )
endfunction()

# ------------------------------------------------------------------------------
# Run functions
create_cppcheck_build_target()
create_clang_format_build_target()