#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for AVR32 build                                          #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(avr32_build LANGUAGES C)

add_executable(avr32_build
    ${CMAKE_SOURCE_DIR}/src/main.c
)

target_include_directories(avr32_build PRIVATE

    # \/=== Add each of your library directories
    ${CMAKE_SOURCE_DIR}/src/hello_world # Example for Hello World project

)

target_link_libraries(avr32_build PRIVATE

    # \/=== Link to all libraries defined by your software project needed in the executable
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
