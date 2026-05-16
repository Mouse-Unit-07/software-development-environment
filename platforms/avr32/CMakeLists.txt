#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for AVR32 build                                          #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(avr32_build LANGUAGES C CXX)

# ------------------------------------------------------------------------------
# AVR32 build flags

set(CMAKE_C_FLAGS_DEBUG
    "-O0 -g3 -Wall -DDEBUG -ffunction-sections -fdata-sections -masm-addr-pseudos -std=gnu99 -mpart=uc3l0256 -DBOARD=USER_BOARD -fno-strict-aliasing"
    CACHE STRING "" FORCE
)

set(CMAKE_ASM_FLAGS_DEBUG
    "-O0 -g3 -DDEBUG -ffunction-sections -masm-addr-pseudos -mpart=uc3l0256 -DBOARD=USER_BOARD"
    CACHE STRING "" FORCE
)

set(CMAKE_EXE_LINKER_FLAGS
    "-Wl,--gc-sections -Wl,--start-group -lm -Wl,--end-group --rodata-writable --direct-data -mpart=uc3l0256"
    CACHE STRING "" FORCE
)
# ------------------------------------------------------------------------------

add_executable(avr32_build
    ${CMAKE_SOURCE_DIR}/src/main.c
)

target_link_libraries(avr32_build PRIVATE

    # \/=== Link to the aggregate library for your software project
    hello_world_lib # Example for Hello World project
)

set_target_properties(avr32_build PROPERTIES SUFFIX ".elf")

add_custom_command(TARGET avr32_build POST_BUILD
    COMMAND "$CACHE{AVR32_OBJCOPY}" -O ihex -R .eeprom -R .fuse -R .lock -R .signature $<TARGET_FILE:avr32_build> avr32_build_output.hex
    COMMAND "$CACHE{AVR32_OBJCOPY}" -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex $<TARGET_FILE:avr32_build> avr32_build_output.eep
    COMMAND "$CACHE{AVR32_OBJCOPY}" -O srec -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures $<TARGET_FILE:avr32_build> avr32_build_output.srec
    COMMAND "$CACHE{AVR32_OBJDUMP}" -h -S $<TARGET_FILE:avr32_build> > avr32_build_output.lss
    COMMAND ${AVR32_SIZE} --format=berkeley $<TARGET_FILE:avr32_build>
    COMMENT "Generating HEX, EEP, SREC, LSS"
)
