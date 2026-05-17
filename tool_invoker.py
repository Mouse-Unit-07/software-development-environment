#!/usr/bin/env python3
import subprocess
import shutil
import argparse
from pathlib import Path
import os
import stat
import time
import sys

# Quick and dirty Python script to run all CMake build commands.
# Not intended to be cemented into our development process- this script is just
# a lazy shortcut to typing out build commands.
# ...For robust automation, you'd start building pipelines...


VALID_MOUSE_TARGETS = [
    "rev_a",
    "rev_b"
]


def run(cmd):
    """Run a command and exit on failure."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        sys.exit(result.returncode)


def remove_build_folder(path: Path):
    """Delete build folder safely."""
    if not path.exists():
        return

    print(f"Deleting build folder: {path.resolve()}")

    def onerror(func, p, _):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onerror=onerror)


def ensure_build_folder(path: Path):
    """Ensure build folder exists."""
    path.mkdir(parents=True, exist_ok=True)


def configure(preset, mouse_target):
    run(["cmake", "--preset", preset, f"-DMOUSE_TARGET={mouse_target}"])


def build(preset):
    run(["cmake", "--build", "--preset", preset])


def run_target(preset, target):
    run(["cmake", "--build", "--preset", preset, "--target", target])


def run_tests():
    run(["ctest", "--preset", "windows-build"])


def main():
    parser = argparse.ArgumentParser(
        description="CMake build helper",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--clean", action="store_true", help="Delete build folder first")
    parser.add_argument("--all", action="store_true", help="Run AVR + Windows builds")
    parser.add_argument("--windows", action="store_true", help="Run Windows build + tests")
    parser.add_argument("--avr", action="store_true", help="Run AVR build")
    parser.add_argument("--format", action="store_true", help="Run clang-format target")
    parser.add_argument("--cppcheck", action="store_true", help="Run cppcheck target")
    parser.add_argument("--mouse-target", required=True, choices=VALID_MOUSE_TARGETS, help="Specify mouse hardware target")

    args = parser.parse_args()

    # Show help if no args
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    build_dir = Path("build")

    if args.clean:
        remove_build_folder(build_dir)

    ensure_build_folder(build_dir)

    # Determine what to run
    run_avr = args.avr or args.all
    run_windows = args.windows or args.all

    # ---------------- AVR ----------------
    if run_avr:
        print("\n=== AVR BUILD ===")
        configure("avr32-build", args.mouse_target)
        build("avr32-build")

    # ---------------- WINDOWS ----------------
    if run_windows:
        print("\n=== WINDOWS BUILD ===")
        configure("windows-build", args.mouse_target)
        build("windows-build")
        run_tests()

    # ---------------- OPTIONAL TARGETS ----------------
    if args.format:
        print("\n=== CLANG-FORMAT ===")
        configure("windows-build", args.mouse_target)
        run_target("windows-build", "format_sources")

    if args.cppcheck:
        print("\n=== CPPCHECK ===")
        configure("windows-build", args.mouse_target)
        run_target("windows-build", "cppcheck")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start

    mins, secs = divmod(elapsed, 60)
    print(f"\n=== Total time: {int(mins)}m {secs:.1f}s ===")
