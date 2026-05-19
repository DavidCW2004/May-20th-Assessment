# Revision Mock Exam Mistakes

Mock exam mistakes live here instead of `revision-mistake-log.xlsx` so the relevant code snippets can be included. Correct answers and explanations are in `revision-correct-rules.md` using the same question numbers.

## Mock Paper 1

### Q143 [X] - Makefile clean rule

**Source:** ECM2433 Mock Paper 1, Question 1(b)

**Redo question:** For the mock project with `main.c`, `stats.c`, and `stats.h`, write only the `clean` target recipe that removes all object files and the `report` executable. Explain what each part of the command removes.

```text
Project files:
main.c
stats.c
stats.h

Executable:
report
```

### Q144 [X] - Heap string copy allocation

**Source:** ECM2433 Mock Paper 1, Question 1(c)

**Redo question:** In the `copy_label(const char *src)` stub, fill in only the allocation expression for `copy`. It must allocate enough bytes for all visible characters and the final string terminator.

```c
#include <stdlib.h>
#include <string.h>

char *copy_label(const char *src) {
    char *copy = /* allocate enough space */;
    if (copy == NULL) {
        return NULL;
    }
    /* copy the string */
    return copy;
}
```

### Q145 [X] - `qsort` comparator ordering

**Source:** ECM2433 Mock Paper 1, Question 1(d)

**Redo question:** For `typedef struct { char name[16]; int score; } Entry;`, complete `compare_entries` and `sort_entries` so `qsort` orders score descending and name ascending on ties.

```c
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[16];
    int score;
} Entry;

int compare_entries(const void *left, const void *right) {
    /* complete this comparator */
}

void sort_entries(Entry entries[], size_t len) {
    /* call qsort */
}
```

### Q146 [X] - Dangling pointer after `free`

**Source:** ECM2433 Mock Paper 1, Question 1(e)

**Redo question:** For the mock code below, explain why `p` is dangling and what C behaviour dereferencing it gives.

```c
int *p = malloc(sizeof *p);
*p = 10;
free(p);
printf("%d\n", *p);
```

### Q147 [X] - Rule of three for raw heap arrays

**Source:** ECM2433 Mock Paper 1, Question 2(b)

**Redo question:** For the mock `Buffer` class, assume you replace the default destructor with one that calls `delete[] data`. Explain why that is still not a complete raw-owning fix, and name the two copy operations that also need handling.

```cpp
class Buffer {
    char *data;

public:
    Buffer(int size) {
        data = new char[size];
    }

    ~Buffer() = default;
};
```

### Q148 [X] - `shared_ptr` last owner lifetime

**Source:** ECM2433 Mock Paper 1, Question 2(d)

**Redo question:** In the mock `shared_ptr`/`weak_ptr` code, focus on the lifetime rule: after `auto b = a;` and `a.reset();`, explain why the shared int is still alive and state exactly when it will be destroyed.

```cpp
#include <memory>
#include <iostream>

auto a = std::make_shared<int>(42);
std::weak_ptr<int> watch = a;
auto b = a;
a.reset();

if (auto p = watch.lock()) {
    std::cout << *p << "\n";
}
```

### Q149 [X] - Catching exceptions by const reference

**Source:** ECM2433 Mock Paper 1, Question 2(e)

**Redo question:** For `catch (const std::invalid_argument& error)` after throwing `std::invalid_argument("negative age")`, explain why const reference is used and what `error.what()` prints.

```cpp
try {
    throw std::invalid_argument("negative age");
} catch (const std::invalid_argument& error) {
    std::cerr << error.what() << "\n";
}
```

### Q150 [X] - Float sorting unwrap after `partial_cmp`

**Source:** ECM2433 Mock Paper 1, Question 3(d)

**Redo question:** Given the readings below, write the first comparison inside `sort_by` using `partial_cmp(...).unwrap()`, then add the id-descending tie-breaker.

```rust
let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];
/* sort here */
```

### Q151 [X] - Semicolon after Rust `let` parse statement

**Source:** ECM2433 Mock Paper 1, Question 3(e)

**Redo question:** In the mock `parse_count` function, write the parsing `let n = ...?;` line with the correct semicolon. Then explain why that `let` line needs `;` but the final `Ok(n)` does not.

```rust
fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = /* parse with ? */;
    Ok(n)
}
```

### Q152 [X] - Channel send and dropping original sender

**Source:** ECM2433 Mock Paper 1, Question 4(a)

**Redo question:** In the mock `mpsc` program below, write the worker body line that sends `id * 10` through the cloned transmitter, then explain why `drop(tx)` is needed before `for value in rx` can finish.

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    for id in 0..4 {
        /* spawn a worker that sends id * 10 */
    }

    drop(tx);

    for value in rx {
        println!("{value}");
    }
}
```

### Q153 [X] - Mutex lock result and guard lifetime

**Source:** ECM2433 Mock Paper 1, Question 4(b)

**Redo question:** In the mock `Arc<Mutex<i32>>` counter loop, write the two closure lines that call `lock().unwrap()` and increment through the guard. Then explain what `lock()` returns and when the mutex unlocks.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = Vec::new();

for _ in 0..4 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        /* increment the shared counter */
    }));
}

for handle in handles {
    handle.join().unwrap();
}
```

### Q154 [X] - Generic bounds for compare and display

**Source:** ECM2433 Mock Paper 1, Question 4(c)

**Redo question:** For the mock `show_larger<T>` body using `if a > b` and `println!("{winner}")`, fix the generic signature and name the trait bounds needed for those two operations.

```rust
fn show_larger<T>(a: T, b: T) {
    let winner = if a > b { a } else { b };
    println!("{winner}");
}
```

### Q155 [X] - Boxed recursive enum size

**Source:** ECM2433 Mock Paper 1, Question 4(d)

**Redo question:** For the mock enum below, explain why the unboxed recursive field gives `List` no known size, then state how `Box<List>` fixes that by storing a fixed-size pointer.

```rust
enum List {
    Cons(i32, List),
    Nil,
}
```

## Mock Paper 2

### Q156 [X] - `strtol` validation checks

**Source:** ECM2433 Mock Paper 2, Question 1(a)

**Redo question:** In the mock `parse_positive` function after the `strtol` call, write the `end == text` check and the combined range/positive/int-size check using `errno == ERANGE`, `value <= 0`, and `value > INT_MAX`.

```c
#include <errno.h>
#include <limits.h>
#include <stdlib.h>

int parse_positive(const char *text, int *out) {
    char *end = NULL;
    errno = 0;
    long value = strtol(text, &end, 10);

    /* checks here */

    *out = (int)value;
    return 1;
}
```

### Q157 [X] - Safe first-line file read

**Source:** ECM2433 Mock Paper 2, Question 1(b)

**Redo question:** In the mock `print_first_line` stub, complete the `fopen` failure path, the `fgets` failure handling, the successful print, and the `fclose` calls.

```c
#include <errno.h>
#include <stdio.h>
#include <string.h>

int print_first_line(const char *path) {
    FILE *fp = fopen(path, "r");
    char line[80];

    /* failure handling and read here */

    return 0;
}
```

### Q158 [X] - `static` helper vs public header function

**Source:** ECM2433 Mock Paper 2, Question 1(c)

**Redo question:** For the mock `stack.c` declarations, fix the two access/linkage mistakes: make `make_node` private to the file with the correct C keyword, and explain why `public` is not used before `push` in C.

```c
/* stack.c */
Node *make_node(char value);
Stack push(Stack stack, char value);
```

### Q159 [X] - Remove first matching linked-list node

**Source:** ECM2433 Mock Paper 2, Question 1(d)

**Redo question:** Complete the mock `remove_first(Node **head, char key)` so it can remove the head or a later node, updates the caller's head pointer if needed, frees the removed node, and returns success or failure.

```c
#include <stdlib.h>

typedef struct Node {
    char key;
    struct Node *next;
} Node;

int remove_first(Node **head, char key) {
    /* complete this function */
}
```

### Q160 [X] - `fgetc` EOF vs read error

**Source:** ECM2433 Mock Paper 2, Question 1(e)

**Redo question:** After the mock `while ((ch = fgetc(fp)) != EOF)` loop, add the stream error check and explain why EOF alone cannot prove the loop ended cleanly.

```c
int ch;
long count = 0;

while ((ch = fgetc(fp)) != EOF) {
    count++;
}

/* error check here */
```

### Q161 [X] - C++ subscript operator returning a reference

**Source:** ECM2433 Mock Paper 2, Question 2(a)

**Redo question:** Complete `operator[]` so assignment through `grades[2]` changes the stored element. Include a simple bounds check.

```cpp
#include <stdexcept>

class Grades {
    int data[4] = {0, 0, 0, 0};

public:
    /* operator[] here */
};
```

### Q162 [X] - C++ output operator stream references

**Source:** ECM2433 Mock Paper 2, Question 2(b)

**Redo question:** For the mock `Date` output operator, fill in the missing stream reference pieces: the return type must be `std::ostream&`, and the first parameter must be `std::ostream& os`. Explain why returning the stream reference allows chaining.

```cpp
#include <iostream>

class Date {
    int day;
    int month;
    int year;

public:
    Date(int d, int m, int y) : day(d), month(m), year(y) {}
    /* friend declaration here */
};

/* operator definition here */
```

### Q163 [X] - Template member definitions with `Box<T>::`

**Source:** ECM2433 Mock Paper 2, Question 2(c)

**Redo question:** For the mock `Box` template, write the out-of-class definitions for the constructor and `get` using `Box<T>::` in both definitions. Then explain why template definitions normally live in the header.

```cpp
template<typename T>
class Box {
    T value;

public:
    Box(T value);
    T get() const;
};

/* definitions here */
```

### Q164 [X] - Lifetime annotation for returned input borrow

**Source:** ECM2433 Mock Paper 2, Question 3(a)

**Redo question:** Fix the `choose_label` signature so the returned borrowed string slice can come from either input. Then explain what the single lifetime parameter says about the returned borrow.

```rust
fn choose_label(primary: &str, fallback: &str) -> &str {
    if primary.is_empty() {
        fallback
    } else {
        primary
    }
}
```

### Q165 [X] - Closure capture by mutable borrow and `FnMut`

**Source:** ECM2433 Mock Paper 2, Question 3(b)

**Redo question:** Fix the closure binding below so both calls compile. Then explain how the closure captures `seen` and why the closure trait is `FnMut`.

```rust
let mut seen = 0;

let record = |word: &str| {
    if word.starts_with('a') {
        seen += 1;
    }
};

record("apple");
record("pear");
```

### Q166 [X] - Iterator pipeline for indexed positive readings

**Source:** ECM2433 Mock Paper 2, Question 3(c)

**Redo question:** Starting from the `readings` vector, collect `[(0, 3), (3, 8)]` as `Vec<(usize, i32)>` without explicit indexing. The index must be the original position in the vector.

```rust
let readings = vec![Some(3), None, Some(-2), Some(8)];
/* collect [(0, 3), (3, 8)] */
```

### Q167 [X] - File read with `Result` and question-mark propagation

**Source:** ECM2433 Mock Paper 2, Question 3(d)

**Redo question:** Complete `total_file` so it reads the whole file, parses each line as `i32`, adds the values, and uses `?` to propagate both file-read and parse errors.

```rust
use std::error::Error;
use std::fs;

fn total_file(path: &str) -> Result<i32, Box<dyn Error>> {
    /* complete */
}
```

### Q168 [X] - Safe third-name lookup with `Option`

**Source:** ECM2433 Mock Paper 2, Question 3(e)

**Redo question:** Rewrite `third_name` so it does not panic when the slice is too short. It should return `Option<&str>` borrowed from the input.

```rust
fn third_name(names: &[String]) -> &str {
    &names[2]
}
```

### Q169 [X] - Generic byte copy with element width

**Source:** ECM2433 Mock Paper 2, Question 4(a)

**Redo question:** Complete `copy_slot` so it copies the array element at source index `from` into destination index `to`. Explain why the element width is needed.

```c
#include <stddef.h>
#include <string.h>

void copy_slot(void *array, size_t from, size_t to, size_t width) {
    /* complete */
}
```

### Q170 [X] - Countdown iterator state update

**Source:** ECM2433 Mock Paper 2, Question 4(d)

**Redo question:** Implement `Iterator` for `Countdown` so it yields `current`, `current - 1`, down to `1`, and then stops.

```rust
struct Countdown {
    current: i32,
}

impl Iterator for Countdown {
    type Item = i32;

    fn next(&mut self) -> Option<Self::Item> {
        /* complete */
    }
}
```

### Q171 [X] - Array parameter `sizeof` decay

**Source:** ECM2433 Mock Paper 2, Question 4(e)

**Redo question:** The function tries to calculate an array length using `sizeof` after the array is passed to a function. Explain the bug and rewrite the function signature and call so the length is handled correctly.

```c
#include <stdio.h>

void print_count(int values[]) {
    size_t count = sizeof(values) / sizeof(values[0]);
    printf("%zu\n", count);
}

int main(void) {
    int values[5] = {1, 2, 3, 4, 5};
    print_count(values);
}
```

### Q172 [X] - Unsigned wraparound after subtracting from zero

**Source:** ECM2433 Mock Paper 3, Question 1(a)

**Redo question:** Trace the conversions in the program. State the values printed for `x`, `y`, and `u`, and explain the integer division and unsigned result.

```c
#include <stdio.h>

int main(void) {
    int a = 7;
    int b = 2;
    double x = a / b;
    double y = (double)a / b;
    unsigned int u = 0;

    u = u - 1;
    printf("x=%.1f y=%.1f u=%u\n", x, y, u);
}
```

### Q173 [X] - Destination buffer too small in cleaned string copy

**Source:** ECM2433 Mock Paper 3, Question 1(b)

**Redo question:** Complete `copy_clean` so it keeps only letters and digits, lowercases kept characters, writes a terminator, and returns `0` if the destination buffer is too small.

```c
#include <ctype.h>
#include <stddef.h>

int copy_clean(char *dest, size_t dest_len, const char *src) {
    size_t write = 0;

    if (dest_len == 0) {
        return 0;
    }

    for (size_t read = 0; src[read] != '\0'; read++) {
        /* complete */
    }

    dest[write] = '\0';
    return 1;
}
```

### Q174 [X] - Whole-result parentheses in `SQUARE`

**Source:** ECM2433 Mock Paper 3, Question 1(c)

**Redo question:** Fix the `SQUARE` macro so ordinary expressions are grouped correctly, then explain the remaining problem with `SQUARE(i++)`.

```c
#define SQUARE(X) X * X

int a = 2;
int b = 3;
int r = SQUARE(a + b);
```

### Q175 [X] - Makefile default executable target first

**Source:** ECM2433 Mock Paper 3, Question 1(d)

**Redo question:** For files `main.c`, `image.c`, and `image.h`, write Makefile rules for `main.o`, `image.o`, and the executable `viewer`. Then state what rebuilds after `image.h` changes.

```text
Project files:
main.c
image.c
image.h

Executable:
viewer
```

### Q176 [X] - Minimal CMake project and build commands

**Source:** ECM2433 Mock Paper 3, Question 2(a)

**Redo question:** For a C++ project containing `main.cpp` and `sensor.cpp`, write a minimal `CMakeLists.txt` and the two commands that configure into `build/` and then build the executable.

```text
Project files:
main.cpp
sensor.cpp

Executable:
sensor_app
```

### Q177 [X] - Base smart pointer polymorphic ownership

**Source:** ECM2433 Mock Paper 3, Question 2(c)

**Redo question:** Complete the base class interface and the vector insertion so a `TemperatureSensor` is owned through a base-class smart pointer and read polymorphically.

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Sensor {
public:
    /* base interface */
};

class TemperatureSensor : public Sensor {
    int id;
    double celsius;

public:
    TemperatureSensor(int id, double celsius) : id(id), celsius(celsius) {}
    double read() const override { return celsius; }
};

std::vector<std::unique_ptr<Sensor>> sensors;
/* insert TemperatureSensor 7, 21.5 */

for (const auto& sensor : sensors) {
    std::cout << sensor->read() << "\n";
}
```

### Q178 [X] - `binary_search` searched value and comparator

**Source:** ECM2433 Mock Paper 3, Question 2(d)

**Redo question:** The vector is sorted largest first. Complete the `binary_search` call correctly and explain why the same ordering rule is needed.

```cpp
#include <algorithm>
#include <functional>
#include <vector>

std::vector<int> scores = {90, 70, 100, 80};

std::sort(scores.begin(), scores.end(), std::greater<int>{});

bool found = std::binary_search(/* complete */);
```

### Q179 [X] - Function object predicate for `count_if`

**Source:** ECM2433 Mock Paper 3, Question 2(e)

**Redo question:** Complete the function object so `count_if` counts readings whose value is above the stored limit.

```cpp
#include <algorithm>
#include <vector>

struct Reading {
    int id;
    double value;
};

struct Above {
    double limit;

    /* function call operator */
};

std::vector<Reading> readings = {{1, 18.0}, {2, 22.5}, {3, 25.0}};
int hot = std::count_if(readings.begin(), readings.end(), Above{20.0});
```

### Q180 [X] - Borrowing `String` so the caller can still print it

**Source:** ECM2433 Mock Paper 3, Question 3(a)

**Redo question:** Fix the code so `name` can still be printed after calculating its length. Use borrowing rather than cloning.

```rust
fn label_len(label: String) -> usize {
    label.len()
}

fn main() {
    let name = String::from("sensor");
    let n = label_len(name);
    println!("{name} {n}");
}
```

### Q181 [X] - Debug bound instead of Display

**Source:** ECM2433 Mock Paper 3, Question 3(b)

**Redo question:** Fix the derive line and the generic bounds so the function can compare two values and print the matching value with debug formatting.

```rust
struct Point {
    x: i32,
    y: i32,
}

fn show_if_same<T>(a: T, b: T) {
    if a == b {
        println!("{:?}", a);
    }
}
```

### Q182 [X] - First matching slice value with `find`

**Source:** ECM2433 Mock Paper 3, Question 3(c)

**Redo question:** Complete `first_over_limit` so it returns the first value greater than `limit` from a slice, without explicit indexing.

```rust
fn first_over_limit(values: &[i32], limit: i32) -> Option<i32> {
    /* complete */
}
```

### Q183 [X] - Parsing `port=<number>` with `Result`

**Source:** ECM2433 Mock Paper 3, Question 3(d)

**Redo question:** Complete `parse_port` for lines such as `port=8080`. It should reject a missing equals sign, the wrong key, and a bad integer using `Result`.

```rust
fn parse_port(line: &str) -> Result<u16, String> {
    /* complete */
}
```

### Q184 [X] - Unit tests with `super` and integration tests through public API

**Source:** ECM2433 Mock Paper 3, Question 3(e)

**Redo question:** Given the library code, write one unit test that can call `helper` and one integration-test style assertion that uses only the public API.

```rust
fn helper(n: i32) -> i32 {
    n + 1
}

pub fn double_after_help(n: i32) -> i32 {
    helper(n) * 2
}
```

### Q185 [X] - Binary record seek and read

**Source:** ECM2433 Mock Paper 3, Question 4(a)

**Redo question:** Complete `read_record` so it seeks to record `index` in a binary file and reads exactly one `Record` into `out`.

```c
#include <stdio.h>

typedef struct {
    int id;
    double temperature;
} Record;

int read_record(FILE *fp, long index, Record *out) {
    /* complete */
}
```

### Q186 [X] - Virtual inheritance in a diamond

**Source:** ECM2433 Mock Paper 3, Question 4(b)

**Redo question:** In the diamond inheritance code below, rewrite only the `Left` and `Right` inheritance lines so `Bottom` has one shared `Base` subobject instead of two.

```cpp
class Base {
public:
    int id;
};

class Left : public Base {};
class Right : public Base {};
class Bottom : public Left, public Right {};
```

### Q187 [X] - `setbuf` before output and `fflush`

**Source:** ECM2433 Mock Paper 3, Question 4(e)

**Redo question:** In this program, show where `setbuf(stdout, buffer)` belongs if a custom stdout buffer is used, then add the call that forces `"Working..."` to appear immediately.

```c
#include <stdio.h>

int main(void) {
    char buffer[BUFSIZ];

    /* optional buffer setup */
    printf("Working...");
    /* force output before long task */

    return 0;
}
```

## Ollie Mock Paper 2

### Q188 [X] - Off-by-one heap write and AddressSanitizer report

**Source:** Ollie Mock Paper 2, Question 1(a)

**Redo question:** In the `manage_list` code below, identify the exact loop condition bug, name the memory error it causes, and explain what AddressSanitizer would report differently from a normal run.

```c
#include <stdlib.h>

int *manage_list(int size) {
    int *list = malloc(size * sizeof(int));
    for (int i = 0; i <= size; i++) {
        list[i] = i * 10;
    }
    return list;
}
```

### Q189 [X] - `extern "C"` and C++ name mangling

**Source:** Ollie Mock Paper 2, Question 1(c)

**Redo question:** In C++, explain what `extern "C"` does to name mangling and why it is needed when calling a function compiled from a C source file.

```cpp
extern "C" {
    void c_function(void);
}
```

### Q190 [X] - Generic byte swap with `void *`

**Source:** Ollie Mock Paper 2, Question 1(d)

**Redo question:** Write `swap_anything` so it swaps two objects of unknown type by copying `size` bytes. Explain why `void *` cannot be directly dereferenced for this.

```c
#include <stddef.h>

void swap_anything(void *p, void *q, size_t size) {
    /* complete */
}
```

### Q191 [X] - Safe string input width and terminator space

**Source:** Ollie Mock Paper 2, Question 1(e)

**Redo question:** A program reads into `char buffer[20]`. Explain why `scanf("%s", buffer)` is unsafe, give a width-limited `scanf` format that leaves space for the terminator, and give a safer `fgets` alternative.

```c
char buffer[20];
```

### Q192 [X] - Function overloading and mangled symbols

**Source:** Ollie Mock Paper 2, Question 2(b)

**Redo question:** Explain function overloading in C++, then explain how the compiler/linker can distinguish these two functions at object-code level.

```cpp
void print(int value);
void print(double value);
```

### Q193 [X] - `std::cin` token extraction and `getline`

**Source:** Ollie Mock Paper 2, Question 2(c)

**Redo question:** For the input `21 Computer Science`, explain why `std::cin >> age >> course` stores only `"Computer"` in `course`, then write the corrected code that reads the full course line.

```cpp
int age;
std::string course;

std::cin >> age >> course;
```

### Q194 [X] - Student sort lambda ordering

**Source:** Ollie Mock Paper 2, Question 2(d)

**Redo question:** Sort the students by mark descending, then by name ascending when marks are equal. Use `std::sort` with a lambda comparator.

```cpp
struct Student {
    std::string name;
    int mark;
};

std::vector<Student> students;
```

### Q195 [X] - `Pair<T>` constructor and `are_equal`

**Source:** Ollie Mock Paper 2, Question 2(e)

**Redo question:** Define a simple `Pair<T>` class with two stored `T` values, a constructor that initialises both values, and an `are_equal()` method that compares them with `==`.

### Q196 [X] - Task search result and substring matching

**Source:** Ollie Mock Paper 2, Question 3(a)

**Redo question:** Complete `find_task` so it searches borrowed task strings for a keyword appearing inside the task text, returns a result that can represent no match, and then handle the result with `match`.

```rust
fn find_task(tasks: &[String], keyword: &str) -> /* return type */ {
    for /* index and task */ in /* iterator */ {
        if /* keyword appears inside task */ {
            /* return found index */
        }
    }

    /* return no match */
}
```

### Q197 [X] - Interior mutability with `Arc<Mutex<T>>`

**Source:** Ollie Mock Paper 2, Question 3(b)

**Redo question:** Explain why this shared counter can be changed from more than one thread even though each thread only has a cloned shared owner.

```rust
use std::sync::{Arc, Mutex};

let count = Arc::new(Mutex::new(0));
let shared = Arc::clone(&count);

let mut value = shared.lock().unwrap();
*value += 1;
```

### Q198 [X] - Borrowed `Vec` element before `push`

**Source:** Ollie Mock Paper 2, Question 3(c)

**Redo question:** Explain why this Rust code is rejected. Identify what `r1` borrows, what access `push` needs, and why `Vec` reallocation matters.

```rust
fn main() {
    let mut tasks = vec![String::from("Task 1")];
    let r1 = &tasks[0];
    tasks.push(String::from("Task 2"));
    println!("{}", r1);
}
```

### Q199 [X] - Deref coercion from `Box<Song>` to `Song`

**Source:** Ollie Mock Paper 2, Question 3(e)

**Redo question:** Given a function that reads a `Song` by reference, show how a boxed song can be passed to it and explain why Rust accepts the call.

```rust
struct Song {
    title: String,
}

fn print_song(song: &Song) {
    println!("{}", song.title);
}

let song = Box::new(Song {
    title: String::from("Intro"),
});
```

### Q200 [X] - Rust `?` operator error propagation

**Source:** Ollie Mock Paper 2, Question 4(a)

**Redo question:** In the function below, explain exactly what `?` does when `parse` returns `Ok(value)` and what it does when `parse` returns `Err(error)`.

```rust
fn read_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let count = text.parse::<i32>()?;
    Ok(count + 1)
}
```

### Q201 [X] - Smart pointers as RAII owners

**Source:** Ollie Mock Paper 2, Question 4(b)

**Redo question:** Explain why `std::unique_ptr` is a smart pointer and what happens to the owned object when `sensor` goes out of scope.

```cpp
#include <memory>

std::unique_ptr<Sensor> sensor =
    std::make_unique<TemperatureSensor>("Lab", 21.5);
```

### Q202 [X] - Moving a channel sender into a spawned thread

**Source:** Ollie Mock Paper 2, Question 4(c)

**Redo question:** Complete the worker body so each spawned thread owns its cloned sender and sends `id * 10` back to the receiver. Then explain why the sender clone is moved into the closure.

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

for id in 0..3 {
    let worker_tx = tx.clone();

    thread::spawn(move || {
        /* send id * 10 here */
    });
}
```

### Q203 [X] - `operator+` return type and `const`

**Source:** Ollie Mock Paper 2, Question 4(d)

**Redo question:** Give the member-function prototype for adding integer seconds to a `MyTime` with `operator+`, then explain why it returns `MyTime` and why the function should be `const`.

```cpp
class MyTime {
public:
    /* prototype here */
};
```

### Q204 [X] - Row-major 2D array offset

**Source:** Ollie Mock Paper 3, Question 1(b)

**Redo question:** For the declaration below, calculate the offset in number of integers from the start of the array to `A[2][1]`. Explain why the number of columns matters.

```c
int A[3][4];
```

### Q205 [X] - Pointer-arithmetic string reverse bounds

**Source:** Ollie Mock Paper 3, Question 1(c)

**Redo question:** Complete `reverse_string` using pointer arithmetic in the swap expressions. Make sure the loop does not run one swap too many and make sure the right-hand character expression uses the final valid index.

```c
#include <string.h>

void reverse_string(char *s) {
    size_t len = strlen(s);

    for (size_t i = 0; /* condition */; i++) {
        char tmp = /* left character */;
        /* swap left and right characters */
    }
}
```

### Q206 [X] - Wild pointer, dangling pointer, and Valgrind reports

**Source:** Ollie Mock Paper 3, Question 1(d)

**Redo question:** Explain why the code below uses a wild pointer, contrast that with a dangling pointer, and state what kind of memory access errors Valgrind can report.

```c
int *p;
*p = 10;
```

### Q207 [X] - `stdout` versus `stderr`

**Source:** Ollie Mock Paper 3, Question 1(e)

**Redo question:** Explain why normal output should go to `stdout` but error diagnostics should go to `stderr`, even though both may appear in the terminal by default.

```c
fprintf(stdout, "Log\n");
fprintf(stderr, "Error\n");
```

### Q208 [X] - Function overloading and name mangling

**Source:** Ollie Mock Paper 3, Question 2(b)

**Redo question:** Explain how C++ can have both of these functions in one program. Include what the compiler does at source level and what name mangling does at object-code/linker level.

```cpp
void print(int value);
void print(double value);
```

### Q209 [X] - `std::map` key lookup versus vector scan

**Source:** Ollie Mock Paper 3, Question 2(c)

**Redo question:** Write C++ code to check whether student ID `1001` exists in the map and print the student's name if found. Then explain why this ordered map lookup is normally better than scanning a vector by ID.

```cpp
std::map<int, Student> students;
```

### Q210 [X] - Moving `std::unique_ptr` ownership

**Source:** Ollie Mock Paper 3, Question 2(e)

**Redo question:** Explain why a class containing a `std::unique_ptr` cannot be copied by standard assignment, then write the expression that transfers ownership from `obj1` to `obj2`.

```cpp
obj2 = /* transfer ownership from obj1 */;
```

### Q211 [X] - `Arc`, `Rc`, and mutex poisoning

**Source:** Ollie Mock Paper 3, Question 3(b)

**Redo question:** Explain why `Arc<Mutex<T>>` is used for shared state across threads. Include what `Arc` stands for, why `Rc` is not suitable across threads, and what happens if a thread panics while holding the mutex lock.

```rust
use std::sync::{Arc, Mutex};
```

### Q212 [X] - Folding the sum of squares

**Source:** Ollie Mock Paper 3, Question 3(c)

**Redo question:** Complete the iterator expression so it calculates the sum of the squares of all values. Use `iter` and `fold`, and make the closure return the next accumulator value.

```rust
let values = vec![2, 3, 4];

let total = values
    .iter()
    .fold(0, |acc, n| /* next accumulator */);
```

### Q213 [X] - `String` ownership versus `&str` parameters

**Source:** Ollie Mock Paper 3, Question 3(d)

**Redo question:** Explain which type owns text data and why a read-only function should usually take `&str` instead of `String`.

```rust
fn print_label(label: &str) {
    println!("{label}");
}
```

### Q214 [X] - `unwrap` versus `expect`

**Source:** Ollie Mock Paper 3, Question 3(e)

**Redo question:** Explain the difference between `unwrap()` and `expect("message")` when an `Option` or `Result` is missing or failed, and say why `expect` can be better for debugging a broken assumption.

```rust
let port = text.parse::<u16>().expect("port should be a valid number");
```

### Q215 [X] - Multi-statement swap macro wrapper

**Source:** ECM2433 Sample Paper, Question 1(b)

**Redo question:** Write a `swap(a, b)` macro for two `int` lvalues. Make the macro safe to use as one statement after an `if` without braces.

```c
int x = 3;
int y = 7;

if (x < y)
    swap(x, y);
```

### Q216 [] - Manual string duplication with `malloc`

**Source:** ECM2433 Sample Paper, Question 1(c)

**Redo question:** Given only the declarations below, allocate memory for `dup` and copy `str` into it. Do not use extra variables or string library functions.

```c
char str[] = "By Divine Aid";
char *dup, *p, *q;
```

### Q217 [X] - Static local variable lifetime and scope

**Source:** ECM2433 Sample Paper, Question 1(e)

**Redo question:** Explain what is different about a global variable and a static local variable inside a function. Include both where the static variable can be used and how long its value lasts.

```c
int global_count;

void tick(void) {
    static int local_count;
    local_count++;
}
```

### Q218 [X] - `printf`, buffering, and `fflush`

**Source:** ECM2433 Sample Paper, Question 1(f)

**Redo question:** Explain why this loop may not show output immediately, then place the `fflush` call in the correct position so each printed value can be seen straight away.

```c
int i;
for (i = 0; i < 10; i++)
    printf("%d ", i);
sleep(10);
exit(0);
```

### Q219 [X] - Controlled access with friends or accessors

**Source:** ECM2433 Sample Paper, Question 2(d)

**Redo question:** The time fields are private in `ClockType`. Give two mechanisms that would let another class obtain or change those values without simply making the fields public.

```cpp
class ClockType {
    int hours;
    int minutes;
    int seconds;
protected:
    std::string maker;
public:
    long seconds_since_midnight() const;
};
```

### Q220 [X] - Manual indexing errors in C loops

**Source:** ECM2433 Sample Paper, Question 3(c)

**Redo question:** In the C loop below, name one manual-indexing mistake that Rust iteration avoids. Then state the type of `x` in the Rust loop.

```c
int arr[] = {1, 2, 3, 4, 5};
for (int i = 0; i < 5; i++) {
    printf("%d\n", arr[i]);
}
```

```rust
let arr = [1, 2, 3, 4, 5];
for x in &arr {
    println!("{}", x);
}
```

### Q221 [] - RAII and Rust ownership rules

**Source:** ECM2433 Sample Paper, Question 4(a)

**Redo question:** Explain what RAII stands for and how it helps with resource cleanup in C++. Then state Rust's three ownership rules and explain when Rust checks ownership and borrowing rules.

### Q222 [] - Return codes, exceptions, and Rust `Result`

**Source:** ECM2433 Sample Paper, Question 4(b)

**Redo question:** Compare C return-code errors, C++ exceptions, and Rust `Result`. Include why return codes can be missed, why exceptions can make control flow harder to follow, and what `?` does in the Rust function.

```rust
fn read_file(path: &str) -> Result<String, std::io::Error> {
    let mut file = std::fs::File::open(path)?;
    let mut contents = String::new();
    use std::io::Read;
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```
