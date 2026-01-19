# Software Development Environment

- A uniform software development environment for building w/ CMake to target all platforms needed
- An alternative to creating a development Docker image w/ all tools installed for you

## Index

- [Overview](#overview)
- [What To Modify](#what-to-modify)
- [Installations](#installations)
- [Environment Variables](#environment-variables)
- [Build Instructions](#build-instructions)

## Overview

- To use the software development environment defined by this repo, you need to:
  - Install all tools and set up environment variables
  - Clone this repo (into a folder on your `C:/` drive, or wherever you want)
  - **Delete the .git folder created from cloning this repo**
    - ...If this repo is ever updated, you need to move out everything under `src/` to a new clone of this repo
  - Clone your software repository into this repo's `src/` folder
    - Ex: run `git clone https://github.com/Mouse-Unit-07/experiment-software-hello-world .` to clone the Hello World repository into `src/`
  - Build and develop in this new `software-development-environment` directory w/ MSYS2 and command prompt
- Refer to `experiment-software-hello-world` and `experiment-software-repeat-hello-world` for examples of source code repositories that are compatible w/ this development environment

## What To Modify

- Files that must be changed according to the software project you clone into `src/` folder:
  - `software-development-environment/avr32/CMakeLists.txt`
    - All of your interface subdirectories under `src/` must be listed out w/ `target_include_directories()`
    - All libraries must be linked to w/ `target_link_libraries()`
  - `software-development-environment/tests/CMakeLists.txt`
    - For CppCheck, all of your interface subdirectories under `src/` must be listed out w/ `add_custom_target()`
  - `software-development-environment/CMakeLists.txt`
    - Test subdirectories for each of your interfaces must be listed out w/ individual `add_subdirectory()` calls

## Installations

- **Overview**
  - Due to lack of a Linux toolchain for the AVR-32 architecture, we can't create a Docker container w/ all tools installed
  - This means each engineer has to manually configure and install software on their machines
  - We need:
    - MSYS2 MINGW64 installation: `C:/msys64/mingw64/bin`
      - gcc 15.0.1
      - g++ 15.0.1
      - gcov 15.0.1
      - CMake 4.0.2
      - Ninja 1.12.1
      - git 2.49.0 (required for FetchContent)
    - Python 3.9
      - pip 25.1.1 -> gcovr 8.3 (Python wrapper around gcov)
    - CppUTest: https://github.com/cpputest/cpputest.git
    - AVR32 toolchain: C:/Program Files (x86)/Atmel/Studio/7.0/toolchain/avr32/avr32-gnu-toolchain/bin
    - AVR32 include library: C:/Program Files (x86)/Atmel/Studio/7.0/Packs/atmel/UC3L_DFP/1.0.59/include/AT32UC3L0256
- **Installation links**
  - Microchip Studio IDE
    - https://www.microchip.com/en-us/tools-resources/develop/microchip-studio
    - installing the IDE will install the AVR32 toolchain for CMake to use
  - Git Bash
    - https://git-scm.com/downloads/win
  - Python and pip
    - https://www.python.org/downloads/
    - Make sure to check "Add Python to PATH"
    - On **Windows command prompt** run `pip install gcovr`
    - If pip isn't discoverable, follow steps in below Environment Variables section first and then run the pip install again
  - MSYS2
    - https://www.msys2.org/
    - Software distribution and build platform with a package manager
    - Use default path `C:\msys64`
    - Open MSYS2 MINGW64 Terminal and run the following commands:

```
pacman -Syu

[close and restart terminal]

pacman -Su

pacman -S mingw-w64-x86_64-gcc \
            mingw-w64-x86_64-gcc-libs \
            mingw-w64-x86_64-gcov \
            mingw-w64-x86_64-cmake \
            mingw-w64-x86_64-ninja
```

- **Check installations**
  - Run and verify below on MSYS2 MINGW64 terminal to see specified version number or higher:
    - `gcc --version` -> should return 15.0.1+
    - `g++ --version` -> should return 15.0.1+
    - `gcov --version` -> should return 15.0.1+
    - `cmake --version` -> should return 4.0.2+
    - `ninja --version` -> should return 1.12.1+
    - `git --version` -> should return 2.49.0+
  - Run and verify below on Windows command prompt to see specified version number or higher:
    - `python --version` -> should return 3.9.10+
    - `pip --version` -> should return 25.1.1+
    - `gcovr --version` -> should return 8.3+
  - Verify that AVR32 toolchain is installed:
    - `C:\Program Files (x86)\Atmel\Studio\7.0\toolchain\avr32\avr32-gnu-toolchain\bin`

## Environment Variables

- Add below to system PATH variables for:
  - Python (if not done automatically):
    - `C:\Users\`[your_user_name]`\AppData\Local\Programs\Python\Python39`
  - `pip`:
    - `C:\Users\`[your_user_name]`\AppData\Local\Programs\Python\Python39\Scripts`
  - `gcc`, `g++`, `gcov`, `cmake`, `ninja`
    - `C:\msys64\mingw64\bin`

## Build Instructions

- AVR32 MCU build
  - navigate to top level project directory w/ MSYS2 MINGW64 terminal
  - `cmake --preset mcu-build`
  - `cmake --build --preset mcu-build`
- Windows build
  - navigate to top level project directory w/ MSYS2 MINGW64 terminal
  - `cmake --preset windows-build`
  - `cmake --build --preset windows-build`
  - `ctest --preset windows-build` to run CppUTest unit tests
- running CppCheck
  - build Windows build
  - navigate to the Windows build directory `build/windows_build` w/ MSYS2 MINGW64 terminal, then run CMake "build" command to run CppCheck
  - `cmake --build . --target cppcheck`
- running clang-format_sources
  - build Windows build
  - navigate to the Windows build directory `build/windows_build` w/ MSYS2 MINGW64 terminal, then run CMake "build" command to run clang-format
  - `cmake --build . --target format_sources`
  - formatted copies of source files will be in build/windows_build/clang-format-output
- running gcovr
  - build Windows build and run ctest
  - open Windows command prompt where gcovr's been installed through pip
  - navigate to top level project directory
  - `gcovr -r . --filter=src/`
