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

### Q169 [] - Generic byte copy with element width

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

### Q176 [] - Minimal CMake project and build commands

**Source:** ECM2433 Mock Paper 3, Question 2(a)

**Redo question:** For a C++ project containing `main.cpp` and `sensor.cpp`, write a minimal `CMakeLists.txt` and the two commands that configure into `build/` and then build the executable.

```text
Project files:
main.cpp
sensor.cpp

Executable:
sensor_app
```

### Q177 [] - Base smart pointer polymorphic ownership

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

### Q178 [] - `binary_search` searched value and comparator

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

### Q179 [] - Function object predicate for `count_if`

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

### Q181 [] - Debug bound instead of Display

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

### Q182 [] - First matching slice value with `find`

**Source:** ECM2433 Mock Paper 3, Question 3(c)

**Redo question:** Complete `first_over_limit` so it returns the first value greater than `limit` from a slice, without explicit indexing.

```rust
fn first_over_limit(values: &[i32], limit: i32) -> Option<i32> {
    /* complete */
}
```

### Q183 [] - Parsing `port=<number>` with `Result`

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

### Q185 [] - Binary record seek and read

**Source:** ECM2433 Mock Paper 3, Question 4(a)

**Mistake noted:** Got completely wrong.

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

### Q186 [] - Virtual inheritance in a diamond

**Source:** ECM2433 Mock Paper 3, Question 4(b)

**Mistake noted:** Did not put `virtual` after `class Left :` and `class Right :`.

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

### Q187 [] - `setbuf` before output and `fflush`

**Source:** ECM2433 Mock Paper 3, Question 4(e)

**Mistake noted:** Did not mention that `setbuf` must be called before any output on that stream.

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
