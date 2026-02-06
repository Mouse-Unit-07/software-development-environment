#!/usr/bin/env python3
import subprocess
import shutil
import argparse
from pathlib import Path
import os
import stat
import time

# Quick and dirty Python script to run all CMake build commands.
# Not intended to be cemented into our development process- this script is just
# a lazy shortcut to typing out build commands.
# ...For robust automation, you'd start building pipelines...

def run(cmd):
    """Run a command and return True if it succeeded, False otherwise."""
    print(f"Running: {' '.join(cmd)}")
    if subprocess.run(cmd).returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        return False
    return True


def run_build(target_name, commands):
    """Run commands for a build target, skipping remaining if one fails."""
    print(f"\n=== Starting {target_name} build ===")
    for cmd in commands:
        if not run(cmd):
            print(f"Skipping remaining {target_name} commands due to failure.\n")
            return
    print(f"=== {target_name} build completed successfully ===\n")


def remove_build_folder(path: Path):
    """Delete a folder safely, handling read-only files."""
    if not path.exists():
        print("Build folder does not exist, nothing to delete.")
        return

    print(f"Deleting build folder: {path.resolve()}")

    def onerror(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(path, onerror=onerror)


def main():
    parser = argparse.ArgumentParser(description="Run CMake build commands")
    parser.add_argument("--clean", action="store_true",
                        help="Delete the build folder and reconfigure")
    args = parser.parse_args()

    build_dir = Path("build")
    if args.clean:
        remove_build_folder(build_dir)

    builds = {
        "AVR32": {
            "configure": [
                ["cmake", "--preset", "avr32-build"],
            ],
            "actions": [
                ["cmake", "--build", "--preset", "avr32-build"],
            ],
        },
        "Windows": {
            "configure": [
                ["cmake", "--preset", "windows-build"],
            ],
            "actions": [
                ["cmake", "--build", "--preset", "windows-build"],
                ["cmake", "--build", "--preset", "windows-build", "--target", "format_sources"],
                ["cmake", "--build", "--preset", "windows-build", "--target", "cppcheck"],
                ["ctest", "--preset", "windows-build"],
            ],
        },
    }

    for target, steps in builds.items():
        commands = []
        if args.clean:
            commands.extend(steps["configure"])
        commands.extend(steps["actions"])

        run_build(target, commands)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start

    mins, secs = divmod(elapsed, 60)
    print(f"\n=== Total time: {int(mins)}m {secs:.1f}s ===")
