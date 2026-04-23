from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"


def run(command: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        shell=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0, output


def main() -> int:
    BUILD.mkdir(exist_ok=True)

    gcc = shutil.which("gcc")
    gxx = shutil.which("g++")
    if not gcc or not gxx:
        print("Missing compiler. Expected both gcc and g++ to be installed.")
        return 1

    jobs = [
        {
            "name": "C: duplicate_array",
            "compile": [
                gcc,
                "-std=c11",
                "-Wall",
                "-Wextra",
                "-pedantic",
                "c/duplicate_array.c",
                "c/duplicate_array_test.c",
                "-o",
                str(BUILD / "duplicate_array_test.exe"),
            ],
            "run": [str(BUILD / "duplicate_array_test.exe")],
        },
        {
            "name": "C: normalise_letters",
            "compile": [
                gcc,
                "-std=c11",
                "-Wall",
                "-Wextra",
                "-pedantic",
                "c/normalise_letters.c",
                "c/normalise_letters_test.c",
                "-o",
                str(BUILD / "normalise_letters_test.exe"),
            ],
            "run": [str(BUILD / "normalise_letters_test.exe")],
        },
        {
            "name": "C++: temperature_sensor",
            "compile": [
                gxx,
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                "cpp/temperature_sensor.cpp",
                "cpp/temperature_sensor_test.cpp",
                "-o",
                str(BUILD / "temperature_sensor_test.exe"),
            ],
            "run": [str(BUILD / "temperature_sensor_test.exe")],
        },
        {
            "name": "C++: rectangle",
            "compile": [
                gxx,
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-pedantic",
                "cpp/rectangle.cpp",
                "cpp/rectangle_test.cpp",
                "-o",
                str(BUILD / "rectangle_test.exe"),
            ],
            "run": [str(BUILD / "rectangle_test.exe")],
        },
    ]

    failures = 0

    for job in jobs:
        print(f"\n== {job['name']} ==")
        ok, output = run(job["compile"])
        if not ok:
            failures += 1
            print("Compile failed")
            if output:
                print(output)
            continue

        ok, output = run(job["run"])
        if not ok:
            failures += 1
            print("Test failed")
            if output:
                print(output)
            continue

        print(output or "Passed")

    if failures:
        print(f"\n{failures} test target(s) failed.")
        return 1

    print("\nAll tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
