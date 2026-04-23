# ECM2433 Coding Exercises

These exercises are based on the topics in [topic-list.md](/c:/Users/FoxyG/PythonProjects/May%2020th%20Assessment/topic-list.md).

They are intentionally small and beginner-friendly. The goal is to get you writing code, compiling it, and fixing failing tests.
The starter implementations are incomplete on purpose, so the tests should fail until you finish the functions.

## Included exercises

### C

1. `duplicate_array`
   Practice pointers, dynamic allocation, array copying, and `NULL` handling.

2. `normalise_letters`
   Practice strings, `malloc`, `<ctype.h>`, and manual copying.

### C++

1. `temperature_sensor`
   Practice classes, inheritance, access control, constructors, and virtual dispatch.

2. `rectangle`
   Practice class design, member initialiser lists, `const` methods, and simple geometry logic.

## How to run all tests

From this folder:

```powershell
python run_tests.py
```

## How to run one test manually

### C

```powershell
gcc -std=c11 -Wall -Wextra -pedantic c/duplicate_array.c c/duplicate_array_test.c -o build/duplicate_array_test.exe
.\build\duplicate_array_test.exe
```

### C++

```powershell
g++ -std=c++17 -Wall -Wextra -pedantic cpp/temperature_sensor.cpp cpp/temperature_sensor_test.cpp -o build/temperature_sensor_test.exe
.\build\temperature_sensor_test.exe
```

## What to edit

Edit only the starter files:

- `c/duplicate_array.c`
- `c/normalise_letters.c`
- `cpp/temperature_sensor.cpp`
- `cpp/rectangle.cpp`

The `*_test.*` files are there to check your work.

## Current toolchain note

This workspace currently has `gcc` and `g++`, but no `rustc` or `cargo`.
That means I have not added runnable Rust tests here yet, even though Rust is on the topic list.
