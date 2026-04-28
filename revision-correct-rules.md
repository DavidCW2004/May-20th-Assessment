# Revision Correct Rules

These notes replace the old `Correct Rules` sheet in `revision-mistake-log.xlsx`. Each entry expands the short rule from the spreadsheet into the reasoning you need to reproduce the answer in code or in an exam explanation.

## C Pointers and Memory

### Q2 - Pointer basics

**Question:** Given `int x = 4; int *p` pointing at `x`; then `*p += 3; int y = *p;`, work out `x` and `y`, then identify which expression is the address.

Rule: a pointer stores an address, and `*p` accesses the object at the address stored in `p`.

```c
int x = 4;
int *p = &x;

*p += 3;
int y = *p;
```

After `int *p = &x;`, `p` contains the address of `x`. The expression `*p += 3;` therefore changes `x` itself from `4` to `7`. The next line reads the same object through the pointer, so `y` also becomes `7`.

The address-related expressions are different:

- `&x` is the address of `x`.
- `p` is the stored address, which is currently the address of `x`.
- `&p` is the address of the pointer variable itself.
- `x` and `*p` are integer values, not addresses.

### Q3 - `sizeof` vs `strlen`

**Question:** For `char s[20] = "Hello";`, work out how many more visible characters can be appended safely, leaving room for `\0`.

`sizeof` on an array gives the total storage size of the array. `strlen` counts visible characters up to the first null terminator.

```c
char s[20] = "Hello";
```

For this array, `sizeof s` is `20` because the array has 20 bytes of storage. `strlen(s)` is `5` because `"Hello"` has five visible characters. A C string also needs one byte for `'\0'`, so the safe remaining visible capacity is:

```text
20 total bytes - 5 visible characters - 1 null terminator = 14
```

So 14 more visible characters can be appended safely.

### Q4 - Out-of-bounds access

**Question:** Find the bug in `int a[5]; for (int i = 0; i <= 5; i++) a[i] = 0;`, fix the loop condition, and give one likely symptom.

An array declared as `int a[5];` has valid indexes `0`, `1`, `2`, `3`, and `4`. The loop condition `i <= 5` incorrectly allows `i == 5`.

```c
int a[5];

for (int i = 0; i <= 5; i++) {
    a[i] = 0;       /* BUG when i is 5 */
}
```

The fixed loop stops before `5`:

```c
for (int i = 0; i < 5; i++) {
    a[i] = 0;
}
```

A more general version avoids repeating the array length:

```c
for (size_t i = 0; i < sizeof a / sizeof a[0]; i++) {
    a[i] = 0;
}
```

Writing past the end is undefined behavior. Possible symptoms include corrupted nearby variables, strange output, or a crash.

### Q5 - `malloc` safety check

**Question:** Complete the missing failure path after `int *a = malloc(n * sizeof *a);` before a loop writes to `a[i]`.

`malloc` returns `NULL` if it cannot allocate the requested memory. You must check that result before writing through the pointer.

```c
int *a = malloc(n * sizeof *a);
if (a == NULL) {
    perror("malloc");
    return 1;
}

for (size_t i = 0; i < n; i++) {
    a[i] = 0;
}

free(a);
```

The important rule is that no expression such as `a[i]` or `*a` is safe until the allocation has been checked.

### Q6 - `strcpy` into `char *`

**Question:** Rewrite `char *p; strcpy(p, "Hello");` in one safe way, and make clear where the writable storage comes from.

This is wrong:

```c
char *p;
strcpy(p, "Hello");
```

The variable `p` is only a pointer. It does not automatically point at writable storage. `strcpy` needs enough writable space for all characters plus the null terminator.

One safe stack-array version is:

```c
char p[6];
strcpy(p, "Hello");
```

The size is `6` because `"Hello"` needs five characters plus `'\0'`.

One safe dynamic allocation version is:

```c
char *p = malloc(sizeof "Hello");
if (p == NULL) {
    return 1;
}

strcpy(p, "Hello");

free(p);
```

The key is to make the storage exist before copying into it.

### Q7 - Dynamic 2D array cleanup

**Question:** If row `r` fails while allocating `int **X`, write the cleanup for rows `0` to `r - 1` and then `X` itself.

When building a dynamic 2D array row by row, a later row allocation can fail after earlier rows have already succeeded. Only the rows already allocated should be freed.

```c
int **X = malloc(rows * sizeof *X);
if (X == NULL) {
    return 1;
}

for (size_t r = 0; r < rows; r++) {
    X[r] = malloc(cols * sizeof *X[r]);
    if (X[r] == NULL) {
        for (size_t i = 0; i < r; i++) {
            free(X[i]);
        }
        free(X);
        return 1;
    }
}
```

If row `r` fails, rows `0` to `r - 1` are the only valid row pointers. After freeing those rows, free the top-level pointer array `X`.

## Rust Ownership and Borrowing

### Q8 - Ownership rules

**Question:** For `let s1 = String::from("hi"); let s2 = s1; println!("{s1} {s2}");`, explain the compiler error and give one fix.

Assigning a `String` to another variable moves ownership.

```rust
let s1 = String::from("hi");
let s2 = s1;
println!("{s1} {s2}"); // error: s1 was moved
```

After `let s2 = s1;`, `s2` owns the heap allocation and `s1` can no longer be used. This prevents two owners from both trying to free the same allocation.

Clone if you need two owned strings:

```rust
let s1 = String::from("hi");
let s2 = s1.clone();
println!("{s1} {s2}");
```

Borrow if the second operation only needs to read:

```rust
let s1 = String::from("hi");
let s2 = &s1;
println!("{s1} {s2}");
```

### Q9 - Move semantics

**Question:** Fix `fn takes(s: String) {}` followed by `takes(name); println!("{name}");` so `name` can still be printed.

This version moves `name` into the function:

```rust
fn takes(s: String) {
    println!("{s}");
}

let name = String::from("Ada");
takes(name);
println!("{name}"); // error: name was moved
```

If the function only needs to read the text, make it borrow a string slice:

```rust
fn takes(s: &str) {
    println!("{s}");
}

let name = String::from("Ada");
takes(&name);
println!("{name}");
```

Passing `&name` lends the string to the function temporarily. Ownership stays with `name`, so it can still be printed afterwards.

### Q10 - Borrowed string-slice parameters and iteration

**Question:** Write a `count_a` function that borrows a string slice and returns `usize`, so it counts `a` characters using the right string iteration method.

For read-only text, take `&str`. To count characters, use `.chars()` rather than iterating over bytes.

```rust
fn count_a(text: &str) -> usize {
    text.chars().filter(|&ch| ch == 'a').count()
}
```

`.chars()` yields Unicode scalar values, so the loop is about characters. Byte iteration with `.bytes()` is different: it yields raw `u8` bytes and can split non-ASCII characters into multiple values.

An explicit loop version is:

```rust
fn count_a(text: &str) -> usize {
    let mut count = 0;

    for ch in text.chars() {
        if ch == 'a' {
            count += 1;
        }
    }

    count
}
```

### Q11 - Modifying a `String`

**Question:** Starting from `let mut text = String::from("Hi");`, write the two lines that produce `Hi! there`.

Use `push` for one `char` and `push_str` for a string slice.

```rust
let mut text = String::from("Hi");

text.push('!');
text.push_str(" there");

assert_eq!(text, "Hi! there");
```

The argument to `push` uses single quotes because it is a single `char`. The argument to `push_str` uses double quotes because it is a string slice.

### Q12 - `String` vs borrowed string slices

**Question:** Choose a function parameter type for read-only text that accepts both string literals and `String` values, then show both calls.

For read-only text, prefer `&str` as the parameter type because it accepts both string literals and borrowed `String` values.

```rust
fn print_text(text: &str) {
    println!("{text}");
}

print_text("literal text");

let owned = String::from("owned text");
print_text(&owned);
```

A string literal already has type `&'static str`, so it can be passed directly. A `String` owns heap storage, so pass `&owned` to borrow it as a string slice.

## C Files and Streams

### Q13 - Text vs binary streams

**Question:** You are checking exact file bytes for a checksum. Choose the `fopen` mode and explain what text mode could change.

When exact bytes matter, such as for a checksum, open the file in binary mode.

```c
FILE *fp = fopen(path, "rb");
if (fp == NULL) {
    perror(path);
    return 1;
}
```

Text mode can translate data while reading. On systems such as Windows, newline sequences may be translated between `"\r\n"` and `"\n"`. A checksum must be computed from the actual bytes in the file, so binary mode is the correct choice.

### Q14 - `scanf` basics

**Question:** For `int k = 99; int rc = scanf("%d", address of k);`, handle the case where the user types `abc` instead of a number.

`scanf` returns the number of successful conversions. If the user types `abc` for `%d`, the conversion fails and the return value is `0`.

```c
int k = 99;
int rc = scanf("%d", &k);

if (rc == 1) {
    printf("k = %d\n", k);
} else {
    printf("Expected an integer\n");
}
```

When `rc` is not `1`, do not trust `k` as newly assigned input. In this example it still has its old value, `99`.

### Q15 - Buffering and flushing

**Question:** A long task starts after `printf("Working...");` but nothing appears yet. Add the missing call and explain why it belongs there.

`printf` output may sit in a buffer instead of appearing immediately. Flush `stdout` when the message must be visible before a long task or before waiting for input.

```c
printf("Working...");
fflush(stdout);

do_long_task();
```

`fflush(stdout)` forces buffered output for `stdout` to be written now.

### Q16 - `ferror` vs `feof`

**Question:** After a `while ((ch = fgetc(fp)) != EOF)` loop ends, write the check that distinguishes a read error from clean EOF.

A loop using `fgetc` usually stops when it sees `EOF`, but `EOF` can mean either normal end-of-file or a read error. Check after the loop.

```c
int ch;

while ((ch = fgetc(fp)) != EOF) {
    putchar(ch);
}

if (ferror(fp)) {
    perror("read");
} else {
    /* Clean end-of-file. */
}
```

`feof(fp)` tells you the end-of-file indicator is set. `ferror(fp)` tells you a real stream error happened.

### Q17 - `rewind` and `fseek`

**Question:** After reading some bytes, reset to the start and then jump to byte offset 20. Write the two calls in order.

Use `rewind` to reset to the beginning, then use `fseek` to jump to a specific byte offset.

```c
rewind(fp);

if (fseek(fp, 20, SEEK_SET) != 0) {
    perror("fseek");
}
```

`SEEK_SET` means the offset is measured from the start of the file. `rewind` also clears the stream's EOF and error indicators.

### Q18 - Open, write, flush, and close

**Question:** Write a safe `out.txt` write fragment that does not call `fprintf` if `fopen` fails, and still closes the file.

Always check that `fopen` succeeded before writing. A complete safe fragment also checks write, flush, and close errors if the result matters.

```c
FILE *fp = fopen("out.txt", "w");
if (fp == NULL) {
    perror("out.txt");
    return 1;
}

if (fprintf(fp, "hello\n") < 0) {
    perror("fprintf");
    fclose(fp);
    return 1;
}

if (fflush(fp) == EOF) {
    perror("fflush");
    fclose(fp);
    return 1;
}

if (fclose(fp) == EOF) {
    perror("fclose");
    return 1;
}
```

The main exam rule is simpler: do not call `fprintf` on a `NULL` `FILE *`, and close a file that was opened successfully.

## C Preprocessor, Macros, and Headers

### Q19 - `#include`

**Question:** For `#include "stack.h"` in `main.c`, describe what happens to the contents of `stack.h` before compilation.

`#include "stack.h"` is handled by the preprocessor before compilation. The preprocessor finds `stack.h` and replaces the directive with the contents of that header.

```c
/* main.c */
#include "stack.h"
```

The compiler then sees a single translation unit that contains the included declarations. The quote form usually searches the current/source directory before the configured include paths.

### Q20 - Macro vs function

**Question:** Explain why a macro call such as `MAX(i++, j++)` can change variables more times than a function call would.

Macros are text substitution, not function calls. A typical macro may use its arguments more than once.

```c
#define MAX(A, B) ((A) > (B) ? (A) : (B))

int i = 1;
int j = 2;
int m = MAX(i++, j++);
```

After expansion, the increments appear in more than one place:

```c
int m = ((i++) > (j++) ? (i++) : (j++));
```

Only one branch of the conditional result is evaluated, but the comparison already evaluated both increments once. A function call evaluates each argument once before entering the function.

### Q21 - Stringification

**Question:** Write a tiny macro that prints both an expression's text and its value using stringification.

The `#` operator inside a macro definition turns an argument into a string literal.

```c
#include <stdio.h>

#define REPORT_INT(X) printf("%s = %d\n", #X, (X))

int value = 42;
REPORT_INT(value + 1);
```

This prints the expression text and its value:

```text
value + 1 = 43
```

### Q22 - Include guards

**Question:** Write a complete include guard for `stack.h`, including the closing directive.

An include guard prevents a header's contents from being processed more than once in the same translation unit.

```c
#ifndef STACK_H
#define STACK_H

/* declarations for stack.h go here */

#endif /* STACK_H */
```

The first include defines `STACK_H`. Later includes see that it is already defined and skip the guarded contents.

## C++ Templates and STL

### Q23 - Templates vs macros

**Question:** Given a macro-generated swap function appearing in two `.cpp` files, explain when the text substitution happens and why the linker may complain.

Macros expand as text before compilation. If a macro generates the same ordinary function definition in two `.cpp` files, each compiled object file contains a definition with the same external name.

```cpp
#define MAKE_SWAP(T)                  \
void swap_values(T& a, T& b) {         \
    T tmp = a;                         \
    a = b;                             \
    b = tmp;                           \
}

MAKE_SWAP(int)
```

If two `.cpp` files both expand that macro into `void swap_values(int&, int&)`, the linker may report a multiple-definition error. Templates are different: they are language features with specific instantiation and linkage rules. Prefer a real function template in a header:

```cpp
template<typename T>
void swap_values(T& a, T& b) {
    T tmp = a;
    a = b;
    b = tmp;
}
```

### Q24 - Class template member definitions

**Question:** Complete the outside-class definition header for `pop`: `template<typename T> T ______::pop()`.

For a member function of a class template, the outside-class definition needs both the template header and the qualified class-template name.

```cpp
template<typename T>
T Stack<T>::pop() {
    /* implementation */
}
```

`template<typename T>` introduces `T` for the definition. `Stack<T>::pop` says that `pop` belongs to the `Stack` template instantiated with that same `T`.

### Q25 - Template definitions in headers

**Question:** Given `template<typename T> T max_value(T a, T b);` in a header and the body only in a `.cpp`, explain why another `.cpp` using `max_value(2, 3)` may fail.

A template body must be visible at the point where the compiler instantiates it.

```cpp
// max_value.hpp
template<typename T>
T max_value(T a, T b) {
    return a < b ? b : a;
}
```

If the header only contains this declaration:

```cpp
template<typename T>
T max_value(T a, T b);
```

and the body is hidden in a `.cpp` file, another `.cpp` that calls `max_value(2, 3)` may compile the call but fail to link because no `max_value<int>` definition was generated where it was needed.

### Q26 - Vector iterators

**Question:** Write the full `for` loop using `auto`, `begin()`, `end()`, and dereferencing to print every element of `std::vector<int> v`.

An iterator points at an element in the vector. Dereference it with `*it` to get the current element.

```cpp
#include <iostream>
#include <vector>

std::vector<int> v = {1, 2, 3};

for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << '\n';
}
```

`begin()` gives an iterator to the first element. `end()` gives a past-the-end iterator, so the loop continues while `it != v.end()`.

## Rust Error Handling and File I/O

### Q27 - `?` and return types

**Question:** Given a `parse_num` function that borrows a string slice, parses an `i32` with `?`, and returns plain `i32`, explain why this cannot compile and fix the return type.

The `?` operator either unwraps an `Ok` value or returns the error early from the current function. That means the function must return a compatible `Result`.

This cannot compile because the function promises a plain `i32`:

```rust
fn parse_num(text: &str) -> i32 {
    let n: i32 = text.trim().parse()?;
    n
}
```

Fix it by returning `Result`:

```rust
fn parse_num(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n: i32 = text.trim().parse()?;
    Ok(n)
}
```

Successful values are wrapped in `Ok`. Parse failures are returned automatically by `?`.

### Q28 - Mapping parse errors

**Question:** Convert `parts[1].trim().parse::<u32>()` into a quantity value, returning `Err("bad quantity".to_string())` if parsing fails.

Use `map_err` to turn the parse error into the exact error type and message you want.

```rust
let quantity = parts[1]
    .trim()
    .parse::<u32>()
    .map_err(|_| "bad quantity".to_string())?;
```

If parsing succeeds, `quantity` is the `u32`. If parsing fails, the closure converts the parse error into `String`, and `?` returns `Err("bad quantity".to_string())` from the surrounding function.

### Q29 - `unwrap` in library code

**Question:** Replace a library function that uses `.unwrap()` on a parse result with a version that lets the caller recover.

`unwrap()` panics on failure. In library code, that takes the choice away from the caller.

Avoid this:

```rust
fn parse_age(text: &str) -> u32 {
    text.trim().parse::<u32>().unwrap()
}
```

Return a `Result` instead:

```rust
fn parse_age(text: &str) -> Result<u32, std::num::ParseIntError> {
    text.trim().parse::<u32>()
}
```

Now the caller can decide what recovery means:

```rust
match parse_age(input) {
    Ok(age) => println!("age = {age}"),
    Err(err) => eprintln!("bad age: {err}"),
}
```

### Q30 - `main` returning `Result`

**Question:** Write a `main` signature that can use `?` for file-read and parse errors, and include the final successful return expression.

`main` can return a `Result`, which lets you use `?` for operations such as file reads and parsing.

```rust
use std::error::Error;
use std::fs;

fn main() -> Result<(), Box<dyn Error>> {
    let text = fs::read_to_string("input.txt")?;
    let number: i32 = text.trim().parse()?;

    println!("{number}");
    Ok(())
}
```

`Box<dyn Error>` is a convenient return error type when `main` may produce different error types. `Ok(())` means the program reached the successful end.

## Rust Collections and Data Modelling

### Q31 - Borrowed string-slice parameter calls

**Question:** Given a `print_text` function that borrows a string slice and `let text = String::from("hello");`, write one call with a string literal and one call with the `String` value.

A function that only reads text should normally accept `&str`.

```rust
fn print_text(text: &str) {
    println!("{text}");
}

let text = String::from("hello");

print_text("hello");
print_text(&text);
```

The string literal can be passed directly because it is already a string slice. The `String` value is passed by borrowing it, so ownership of `text` stays with the caller.

### Q32 - Modifying a `String`

**Question:** Starting from `let mut text = String::from("Hi");`, write code that produces exactly `Hi! there`, and identify which method takes a `char` versus a borrowed string slice.

`push` appends one `char`; `push_str` appends a string slice.

```rust
let mut text = String::from("Hi");

text.push('!');
text.push_str(" there");

assert_eq!(text, "Hi! there");
```

`'!'` is a `char`. `" there"` is a `&str`. The string must be declared `mut` because both methods change it.

### Q33 - `Vec::get` missing case

**Question:** For `let v = vec![10, 20, 30];`, compare `v[10]` with `v.get(10)`. Include what happens when the index is missing and show how to handle the `get` result.

Indexing with square brackets panics if the index is out of range.

```rust
let v = vec![10, 20, 30];
let value = v[10]; // panic
```

`get` returns `Option<&T>`, so missing indexes can be handled explicitly.

```rust
let v = vec![10, 20, 30];

match v.get(10) {
    Some(value) => println!("value = {value}"),
    None => println!("no element at index 10"),
}
```

This is safer when absence is a normal possibility.

### Q34 - `String` field construction

**Question:** Given `struct Book { title: String, pages: u32 }`, create a `Book` from the literal `"Rust"` without using a borrowed string slice where a `String` is required.

If a struct field is `String`, give it an owned `String`, not a borrowed string slice.

```rust
struct Book {
    title: String,
    pages: u32,
}

let book = Book {
    title: String::from("Rust"),
    pages: 320,
};
```

This is equivalent:

```rust
let book = Book {
    title: "Rust".to_string(),
    pages: 320,
};
```

Parentheses around a literal, such as `("Rust")`, do not change its type from `&str` into `String`.

### Q35 - Immutable vs mutable self borrows

**Question:** In an `impl Counter`, write one method that only reads `value` using an immutable self borrow and one method that changes `value` using a mutable self borrow. Explain why the second one needs `mut`.

Use `&self` for methods that only read fields. Use `&mut self` for methods that change fields.

```rust
struct Counter {
    value: i32,
}

impl Counter {
    fn value(&self) -> i32 {
        self.value
    }

    fn increment(&mut self) {
        self.value += 1;
    }
}
```

Calling the mutable method also requires a mutable binding:

```rust
let mut counter = Counter { value: 0 };
counter.increment();
```

Without `&mut self`, Rust will not allow `self.value += 1` because the method only has an immutable borrow.

### Q36 - `Option<T>` and null safety

**Question:** Explain why returning `Option` containing a borrowed value from a lookup is safer than returning a possible null pointer. Mention what the caller must handle before using the value.

`Option` makes absence explicit. A lookup can return either `Some(value)` or `None`, and the caller must handle both before using the value.

```rust
fn find_book<'a>(books: &'a [Book], title: &str) -> Option<&'a Book> {
    books.iter().find(|book| book.title == title)
}

match find_book(&books, "Rust") {
    Some(book) => println!("{} has {} pages", book.title, book.pages),
    None => println!("book not found"),
}
```

This avoids the C-style problem of returning a pointer that might be null and then accidentally dereferencing it without checking.

## C Function Pointers and Callbacks

### Q37 - Callback received by `apply`

**Question:** Complete `int apply(int a, int b, int (*fn)(int, int)) { return _____; }`, then trace what happens when it is called as `apply(1, 3, Plus)`.

A function pointer parameter lets `apply` call a function supplied by the caller.

```c
int Plus(int a, int b) {
    return a + b;
}

int apply(int a, int b, int (*fn)(int, int)) {
    return fn(a, b);
}

int result = apply(1, 3, Plus);
```

`Plus` is passed as the callback. Inside `apply`, `fn(a, b)` calls `Plus(1, 3)`, so `result` becomes `4`.

### Q38 - `qsort` arguments

**Question:** Complete the call that sorts `int values[] = {3, 1, 2};` using `compare_ints`: `qsort(_____, _____, _____, _____);`.

`qsort` needs four pieces of information: the base pointer, the number of elements, the size of one element, and the comparator.

```c
#include <stdlib.h>

int values[] = {3, 1, 2};

qsort(
    values,
    sizeof values / sizeof values[0],
    sizeof values[0],
    compare_ints
);
```

For this array, the element count is `3`, and `sizeof values[0]` is the size of one `int`.

### Q39 - Integer comparator steps

**Question:** Fill in the body of `int compare_ints(const void *p, const void *q)` so it works correctly with `qsort` on an integer array.

The comparator receives `const void *` because `qsort` works with arrays of any element type. For an `int` array, cast each pointer back to `const int *`, read the integers, then return negative, zero, or positive.

```c
int compare_ints(const void *p, const void *q) {
    int a = *(const int *)p;
    int b = *(const int *)q;

    return (a > b) - (a < b);
}
```

This avoids the overflow risk of returning `a - b`.

### Q40 - `const void *` comparator parameters

**Question:** `qsort` rejects `int compare_ints(int *a, int *b)`. Fix the signature and explain why the fixed version matches `qsort`.

The comparator signature must match what `qsort` expects:

```c
int compare_ints(const void *p, const void *q);
```

This does not match:

```c
int compare_ints(int *a, int *b);
```

`qsort` is generic, so it cannot call a comparator that only accepts `int *`. It passes pointers to unknown element types as `const void *`. The comparator then casts those pointers to the correct element type internally. `const` also says the comparator should inspect elements, not modify them.

### Q41 - Pointer arithmetic with `char *`

**Question:** In generic array code with `void *array` and `size_t width`, write the expression for the address of element `i` after converting the base pointer to `char *`.

Pointer arithmetic scales by the size of the pointed-to type. If `array` is a generic `void *`, convert it to `char *` so arithmetic moves in bytes.

```c
void *element = (char *)array + i * width;
```

Here, `width` is the size in bytes of one element, so `i * width` is the byte offset of element `i`.

## C++ Operator Overloading

### Q42 - `MyInteger + int` member overload

**Question:** Given `class MyInteger { int i; public: MyInteger(int value) : i(value) {} /* missing */ };`, write the member overload that makes `MyInteger a(4); int x = a + 6;` set `x` to 10.

A member operator handles cases where the left operand is the class object.

```cpp
class MyInteger {
    int i;

public:
    MyInteger(int value) : i(value) {}

    int operator+(int rhs) const {
        return i + rhs;
    }
};

MyInteger a(4);
int x = a + 6; // x is 10
```

The expression `a + 6` is interpreted as `a.operator+(6)`.

### Q43 - Legal and sensible overloads

**Question:** For `Point`, judge these attempted meanings: `Point + Point`, `int + int`, `sizeof point`, and `point.x`. Mark each as legal or illegal to overload, then choose whether the legal one is sensible.

Operator overloading must involve at least one user-defined type, and some operators cannot be overloaded at all.

- `Point + Point`: legal because `Point` is a class type. It is sensible if point addition has a clear meaning in your program, such as vector-style coordinate addition.
- `int + int`: illegal to change because both operands are built-in types.
- `sizeof point`: illegal because `sizeof` cannot be overloaded.
- `point.x`: illegal because member access with `.` cannot be overloaded.

The exam point is not just whether the syntax is legal. A legal overload should still behave in a way readers would expect.

### Q44 - `operator[]` reference return

**Question:** Complete an array class subscript operator so `arr[2] = 99;` changes the stored element. The body should return the element itself, not its address.

To allow assignment through a subscript, return a reference to the stored element.

```cpp
class IntArray {
    int data[10]{};

public:
    int& operator[](std::size_t index) {
        return data[index];
    }

    const int& operator[](std::size_t index) const {
        return data[index];
    }
};

IntArray arr;
arr[2] = 99;
```

Returning `int&` means `arr[2]` names the actual element. Returning `int *` or `&data[index]` would give the address instead, which is not the expected subscript behavior.

## Rust Generics and Traits

### Q45 - Generic `Point` method

**Question:** Given a generic `Point` with fields `x` and `y`, complete the `impl` block so method `x` borrows the object and returns a borrow of the `x` field.

The `impl` block must introduce the generic parameter, and the method can return a borrow of the field.

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}
```

`&self` means the method borrows the whole point. Returning `&self.x` borrows the `x` field without moving it out of the struct.

### Q46 - Borrowed generic `Area` parameter

**Question:** Fix a broken free function that tries to use `self.area()` outside an `impl` block, so it prints the area of any borrowed shape that implements `Area`.

A free function does not have `self`; `self` only exists in methods. Give the function a named parameter and constrain the type with the trait.

```rust
trait Area {
    fn area(&self) -> f64;
}

fn print_area<T: Area>(shape: &T) {
    println!("{}", shape.area());
}
```

This can also be written with `impl Trait`:

```rust
fn print_area(shape: &impl Area) {
    println!("{}", shape.area());
}
```

The borrowed parameter means the function can read the shape without taking ownership of it.

### Q47 - `show_larger` display bound

**Question:** Fix the signature of `show_larger` when its body compares two values and then prints the winning value with normal braces.

The function compares values and prints the selected value. Comparison needs `PartialOrd`; printing with `{}` needs `Display`.

```rust
use std::fmt::Display;

fn show_larger<T>(a: T, b: T)
where
    T: PartialOrd + Display,
{
    let larger = if a > b { a } else { b };
    println!("{larger}");
}
```

If the function used `{:?}` instead of `{}`, it would need `Debug` rather than `Display`.

### Q48 - `derive` attribute syntax

**Question:** Repair the derive line for a custom struct used with `assert_eq!` and debug printing: `#derive Debug, PartialEq`.

Attributes use `#[]`, and `derive` takes its trait list inside parentheses.

```rust
#[derive(Debug, PartialEq)]
struct Item {
    id: u32,
}
```

`Debug` allows debug formatting such as `{:?}`. `PartialEq` allows equality checks such as `assert_eq!`.

### Q49 - `HashMap` key derives

**Question:** A custom `Team` value is used as a key in a `HashMap`. Add the derives needed so insertion and lookup by key compile.

A `HashMap` key must be hashable and must support equality. Derive `Eq`, `PartialEq`, and `Hash`; `Debug` and `Clone` are often useful too.

```rust
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Team {
    name: String,
}

let mut scores = HashMap::new();
let team = Team {
    name: "A".to_string(),
};

scores.insert(team.clone(), 3);
assert_eq!(scores.get(&team), Some(&3));
```

Every field used by the derived implementations must also support the required traits.

## C++ Virtual Functions and Dynamic Binding

### Q50 - Virtual call through base pointer

**Question:** Given virtual `read`, `TemperatureSensor temp("Lab", 21.5);` and a `Sensor *s` pointing at `temp`, work out which `read` function runs and what value is returned.

When a member function is virtual, a call through a base pointer dispatches according to the actual object type.

```cpp
TemperatureSensor temp("Lab", 21.5);
Sensor *s = &temp;

double value = s->read();
```

If `read` is virtual and `temp` is a `TemperatureSensor`, the call runs `TemperatureSensor::read`, not the base version. The returned value is therefore `21.5`.

Without `virtual`, the function would be chosen from the static pointer type `Sensor *`.

### Q51 - Virtual destructor in polymorphic base

**Question:** Complete the destructor declaration in a polymorphic base class: `_____ ~Sensor() = default;`.

A base class intended for polymorphic use should have a virtual destructor.

```cpp
class Sensor {
public:
    virtual ~Sensor() = default;
};
```

This matters when deleting through a base pointer:

```cpp
Sensor *s = new TemperatureSensor("Lab", 21.5);
delete s;
```

With a virtual destructor, the derived destructor runs correctly. Without it, deleting through the base pointer has undefined behavior.

### Q52 - Constructor string reference parameter

**Question:** Complete the `TemperatureSensor` constructor parameter for `name` as a const string reference, then write the initializer list that calls `Sensor(id, name)` and stores `celsius`.

Use a const string reference for a read-only constructor parameter, then pass it to the base-class constructor in the initializer list.

```cpp
#include <string>

class TemperatureSensor : public Sensor {
    double celsius;

public:
    TemperatureSensor(int id, const std::string& name, double celsius)
        : Sensor(id, name), celsius(celsius) {}
};
```

`const std::string& name` avoids an unnecessary copy and allows the constructor to read the name without modifying it. `Sensor(id, name)` initializes the base part of the object, and `celsius(celsius)` initializes the derived class member.

## C++ Smart Pointer Practice with std::unique_ptr

### Q53 - Base-type smart pointer declaration

**Question:** A factory line must store a newly created `TemperatureSensor` in a variable that can later hold any `Sensor` subtype. Write the full smart-pointer declaration and construction call.

When the question asks for a base-type smart pointer, the variable type must be `std::unique_ptr<Sensor>`, not `auto`.

```cpp
std::unique_ptr<Sensor> sensor =
    std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);
```

Using `auto` here would deduce this different type:

```cpp
std::unique_ptr<TemperatureSensor>
```

That is a derived-type smart pointer. It is valid C++, but it does not answer a question asking for a base-type smart pointer. The base-type version is useful when the same variable, parameter, or container should work with different sensor subclasses through the shared `Sensor` interface.

### Q54 - Returning unique ownership

**Question:** Write the return type and body for `make_sensor` so it creates a `TemperatureSensor` and gives ownership to the caller through the base sensor interface.

The return type must include the owned pointer type:

```cpp
std::unique_ptr<Sensor> make_sensor() {
    return std::make_unique<TemperatureSensor>(5, "Office", 19.0);
}
```

`std::unique_ptr` on its own is incomplete because it is a template. It needs the type it owns inside angle brackets. Here, `std::unique_ptr<Sensor>` means the caller receives ownership of a heap object through the base `Sensor` interface.

### Q55 - Polymorphic owned object

**Question:** Trace `std::unique_ptr<Sensor> sensor = std::make_unique<TemperatureSensor>(...); sensor->read();` and identify the pointer type, the owned heap object type, and the function that runs.

The smart pointer variable has base type:

```cpp
std::unique_ptr<Sensor>
```

but the owned heap object was created as:

```cpp
TemperatureSensor
```

So in this code:

```cpp
std::unique_ptr<Sensor> sensor =
    std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);

double value = sensor->read();
```

the pointer is used through the `Sensor` interface, but the actual owned heap object is a `TemperatureSensor`. If `read` is virtual, the call runs `TemperatureSensor::read()`.

The key distinction is:

- pointer/interface type: `Sensor`
- owned heap object type: `TemperatureSensor`
- virtual call target: `TemperatureSensor::read()`

## C Types and Conversions

### Q56 - Floating-point to `short` conversion

**Question:** A program stores `123456.789` in a `short` and then prints the result. Explain what kind of conversion happens and what information can be lost.

This is a conversion from a floating-point value to a smaller integer type:

```c
short x = 123456.789;
```

Two separate problems matter:

- `short` is an integer type, so it cannot store the decimal part. The fractional part is lost.
- `short` has a limited range, so the remaining integer value may still be too large to fit.

C may compile this without a useful error, but the stored value should not be trusted. The exam phrase to remember is: floating-point to `short` is a narrowing conversion, so decimals are discarded and the value may not fit in the target type.

### Q57 - `typedef` order

**Question:** Write the typedef that lets `Temperature today = 8.0f;` compile, then explain which name is the existing type and which name is the new alias.

The order is:

```c
typedef existing_type new_name;
```

So for a temperature alias based on `float`:

```c
typedef float Temperature;

Temperature today = 8.0f;
```

`float` is the existing type. `Temperature` is the new alias. Writing the names the other way around would try to create an alias for a type name that does not exist yet.
