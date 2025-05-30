#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for AT32UC3L0256 MCU executable build                    #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(hello_world_avr32 LANGUAGES C)

add_executable(hello_world_avr32
    ${CMAKE_SOURCE_DIR}/src/main.c
)

target_include_directories(hello_world_avr32 PRIVATE
    ${CMAKE_SOURCE_DIR}/src/hello_world
    "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/UC3L_DFP/1.0.59/include/AT32UC3L0256"
)

target_link_libraries(hello_world_avr32 PRIVATE
    hello_world_lib
)

set_target_properties(hello_world_avr32 PROPERTIES SUFFIX ".elf")

# Add post-build commands only if AVR32 tools are defined
add_custom_command(TARGET hello_world_avr32 POST_BUILD
    COMMAND "$CACHE{AVR32_OBJCOPY}" -O ihex -R .eeprom -R .fuse -R .lock -R .signature $<TARGET_FILE:hello_world_avr32> hello_world.hex
    COMMAND "$CACHE{AVR32_OBJCOPY}" -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex $<TARGET_FILE:hello_world_avr32> hello_world.eep
    COMMAND "$CACHE{AVR32_OBJCOPY}" -O srec -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures $<TARGET_FILE:hello_world_avr32> hello_world.srec
    COMMAND "$CACHE{AVR32_OBJDUMP}" -h -S $<TARGET_FILE:hello_world_avr32> > hello_world.lss
    COMMAND ${AVR32_SIZE} --format=berkeley $<TARGET_FILE:hello_world_avr32>
    COMMENT "Generating HEX, EEP, SREC, LSS"
)
