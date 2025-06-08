#--------------------------------- FILE INFO ----------------------------------#
# Filename           : CMakeLists.txt                                          #
#                                                                              #
# CMakeLists.txt file for AT32UC3L0256 MCU executable build                    #
#                                                                              #
#------------------------------------------------------------------------------#
cmake_minimum_required(VERSION 4.0.2)
project(mcu_build_target LANGUAGES C)

add_executable(mcu_build_target
    ${CMAKE_SOURCE_DIR}/src/main.c
)

target_include_directories(mcu_build_target PRIVATE

    # \/ === ADD SOURCE SUBDIRECTORIES HERE === \/
    ${CMAKE_SOURCE_DIR}/src/hello_world

    "C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/UC3L_DFP/1.0.59/include/AT32UC3L0256"
)

# \/ === LINK TO ALL LIBRARIES HERE === \/
target_link_libraries(mcu_build_target PRIVATE
    hello_world_lib
)

set_target_properties(mcu_build_target PROPERTIES SUFFIX ".elf")

add_custom_command(TARGET mcu_build_target POST_BUILD
    COMMAND "$CACHE{AVR32_OBJCOPY}" -O ihex -R .eeprom -R .fuse -R .lock -R .signature $<TARGET_FILE:mcu_build_target> hello_world.hex
    COMMAND "$CACHE{AVR32_OBJCOPY}" -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O ihex $<TARGET_FILE:mcu_build_target> hello_world.eep
    COMMAND "$CACHE{AVR32_OBJCOPY}" -O srec -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures $<TARGET_FILE:mcu_build_target> hello_world.srec
    COMMAND "$CACHE{AVR32_OBJDUMP}" -h -S $<TARGET_FILE:mcu_build_target> > hello_world.lss
    COMMAND ${AVR32_SIZE} --format=berkeley $<TARGET_FILE:mcu_build_target>
    COMMENT "Generating HEX, EEP, SREC, LSS"
)
