# Revision Mock Exam Mistakes

Mock exam mistakes live here instead of `revision-mistake-log.xlsx` so the relevant code snippets can be included. Correct answers and explanations are in `revision-correct-rules.md` using the same question numbers.

## Mock Paper 1

### Q143 - Makefile clean rule

**Source:** ECM2433 Mock Paper 1, Question 1(b)

**Mistake noted:** The `clean` command was not correct.

**Redo question:** For the mock project with `main.c`, `stats.c`, and `stats.h`, write only the `clean` target recipe that removes all object files and the `report` executable. Explain what each part of the command removes.

```text
Project files:
main.c
stats.c
stats.h

Executable:
report
```

### Q144 - Heap string copy allocation

**Source:** ECM2433 Mock Paper 1, Question 1(c)

**Mistake noted:** Forgot to allocate `strlen(src) + 1`.

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

### Q145 - `qsort` comparator ordering

**Source:** ECM2433 Mock Paper 1, Question 1(d)

**Mistake noted:** Got the comparator question completely wrong.

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

### Q146 - Dangling pointer after `free`

**Source:** ECM2433 Mock Paper 1, Question 1(e)

**Mistake noted:** Did not mention that `p` is dangling.

**Redo question:** For the mock code below, explain why `p` is dangling and what C behaviour dereferencing it gives.

```c
int *p = malloc(sizeof *p);
*p = 10;
free(p);
printf("%d\n", *p);
```

### Q147 - Rule of three for raw heap arrays

**Source:** ECM2433 Mock Paper 1, Question 2(b)

**Mistake noted:** Did not mention that if a class owns heap memory manually, it also needs correct copy constructor and copy assignment behaviour.

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

### Q148 - `shared_ptr` last owner lifetime

**Source:** ECM2433 Mock Paper 1, Question 2(d)

**Mistake noted:** Did not mention that the shared object is destroyed when the last `shared_ptr` is gone.

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

### Q149 - Catching exceptions by const reference

**Source:** ECM2433 Mock Paper 1, Question 2(e)

**Mistake noted:** Got the exception question completely wrong.

**Redo question:** For `catch (const std::invalid_argument& error)` after throwing `std::invalid_argument("negative age")`, explain why const reference is used and what `error.what()` prints.

```cpp
try {
    throw std::invalid_argument("negative age");
} catch (const std::invalid_argument& error) {
    std::cerr << error.what() << "\n";
}
```

### Q150 - Float sorting unwrap after `partial_cmp`

**Source:** ECM2433 Mock Paper 1, Question 3(d)

**Mistake noted:** Did not put `unwrap()` after `partial_cmp`.

**Redo question:** Given the readings below, write the first comparison inside `sort_by` using `partial_cmp(...).unwrap()`, then add the id-descending tie-breaker.

```rust
let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];
/* sort here */
```

### Q151 - Semicolon after Rust `let` parse statement

**Source:** ECM2433 Mock Paper 1, Question 3(e)

**Mistake noted:** Forgot the semicolon at the end of the parsing `let` statement.

**Redo question:** In the mock `parse_count` function, write the parsing `let n = ...?;` line with the correct semicolon. Then explain why that `let` line needs `;` but the final `Ok(n)` does not.

```rust
fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = /* parse with ? */;
    Ok(n)
}
```

### Q152 - Channel send and dropping original sender

**Source:** ECM2433 Mock Paper 1, Question 4(a)

**Mistake noted:** Did not write `tx.send(id * 10).unwrap()` and did not explain why `drop(tx)` was needed.

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

### Q153 - Mutex lock result and guard lifetime

**Source:** ECM2433 Mock Paper 1, Question 4(b)

**Mistake noted:** Did not mention that `lock()` returns a `Result` containing a guard that must be unwrapped, and did not mention the lock unlocks automatically when the guard is dropped.

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

### Q154 - Generic bounds for compare and display

**Source:** ECM2433 Mock Paper 1, Question 4(c)

**Mistake noted:** Got the generic bounds question completely wrong.

**Redo question:** For the mock `show_larger<T>` body using `if a > b` and `println!("{winner}")`, fix the generic signature and name the trait bounds needed for those two operations.

```rust
fn show_larger<T>(a: T, b: T) {
    let winner = if a > b { a } else { b };
    println!("{winner}");
}
```

### Q155 - Boxed recursive enum size

**Source:** ECM2433 Mock Paper 1, Question 4(d)

**Mistake noted:** Did not mention that `Box` creates a fixed-size pointer and that the unboxed recursive list has no known size.

**Redo question:** For the mock enum below, explain why the unboxed recursive field gives `List` no known size, then state how `Box<List>` fixes that by storing a fixed-size pointer.

```rust
enum List {
    Cons(i32, List),
    Nil,
}
```

## Mock Paper 2

### Q156 - `strtol` validation checks

**Source:** ECM2433 Mock Paper 2, Question 1(a)

**Mistake noted:** Did not check `end == text`, and did not include the range/positive/int-size check.

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

### Q157 - Safe first-line file read

**Source:** ECM2433 Mock Paper 2, Question 1(b)

**Mistake noted:** Got the file-read question completely wrong.

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

### Q158 - `static` helper vs public header function

**Source:** ECM2433 Mock Paper 2, Question 1(c)

**Mistake noted:** Did not put `static` before `make_node` and wrote `public` before `push`.

**Redo question:** For the mock `stack.c` declarations, fix the two access/linkage mistakes: make `make_node` private to the file with the correct C keyword, and explain why `public` is not used before `push` in C.

```c
/* stack.c */
Node *make_node(char value);
Stack push(Stack stack, char value);
```

### Q159 - Remove first matching linked-list node

**Source:** ECM2433 Mock Paper 2, Question 1(d)

**Mistake noted:** Got the linked-list removal question completely wrong.

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

### Q160 - `fgetc` EOF vs read error

**Source:** ECM2433 Mock Paper 2, Question 1(e)

**Mistake noted:** Got the EOF/read-error question completely wrong.

**Redo question:** After the mock `while ((ch = fgetc(fp)) != EOF)` loop, add the stream error check and explain why EOF alone cannot prove the loop ended cleanly.

```c
int ch;
long count = 0;

while ((ch = fgetc(fp)) != EOF) {
    count++;
}

/* error check here */
```

### Q161 - C++ subscript operator returning a reference

**Source:** ECM2433 Mock Paper 2, Question 2(a)

**Mistake noted:** Got the `operator[]` question completely wrong.

**Redo question:** Complete `operator[]` so assignment through `grades[2]` changes the stored element. Include a simple bounds check.

```cpp
#include <stdexcept>

class Grades {
    int data[4] = {0, 0, 0, 0};

public:
    /* operator[] here */
};
```

### Q162 - C++ output operator stream references

**Source:** ECM2433 Mock Paper 2, Question 2(b)

**Mistake noted:** Forgot `std::ostream&` as the return type and `std::ostream& os` as the stream parameter.

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

### Q163 - Template member definitions with `Box<T>::`

**Source:** ECM2433 Mock Paper 2, Question 2(c)

**Mistake noted:** Did not write `Box<T>::` for both out-of-class definitions, and did not explain correctly why template definitions normally live in the header.

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
