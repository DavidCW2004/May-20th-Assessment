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

## C Structures and Dynamic Data Structures

### Q58 - Front insertion pointer order

**Question:** Given `root` points to `C -> Q -> NULL` and `new_node` points to `A -> NULL`, write the assignments that make the list `A -> C -> Q -> NULL` without losing any nodes.

For front insertion, the safe order is:

```c
new_node->next = root;
root = new_node;
```

Start:

```text
root -> C -> Q -> NULL
new_node -> A -> NULL
```

First:

```c
new_node->next = root;
```

Now the new node points at the old list:

```text
new_node -> A -> C -> Q -> NULL
root ------------^
```

Then:

```c
root = new_node;
```

Now the list starts at the new node:

```text
root -> A -> C -> Q -> NULL
```

If you assign `root = new_node` first, you lose the only pointer to the old list unless you saved it somewhere else.

### Q59 - Linked-list stack pop

**Question:** Given `Node *root` points at `A -> C -> Q -> NULL`, complete `char pop(Node **root_ptr)` so it returns `A`, updates the caller's root to `C`, and frees the removed node.

The caller has a `Node *root`, but `pop` must change that pointer. That is why the function receives the address of the root pointer:

```c
char popped = pop(&root);
```

Inside `pop`, use a clearer parameter name such as `root_ptr`:

```c
char pop(Node **root_ptr) {
    if (*root_ptr == NULL) {
        return '\0';
    }

    Node *old = *root_ptr;
    char data = old->data;

    *root_ptr = old->next;

    free(old);
    return data;
}
```

The roles are:

- `root_ptr` is the address of the caller's root pointer.
- `*root_ptr` is the actual current top node pointer.
- `old` is the node being removed.
- `old->next` is the new top of the stack.

The data must be saved before freeing the node. The caller's root must be updated before the function returns, otherwise it would still point at freed memory.

## C++ Moving from C

### Q60 - Compile and link flow

**Question:** For a program split across `main.cpp` and `stack.cpp`, write the separate compile commands that create object files, then write the link command that creates the executable.

The compile step turns each source file into an object file:

```bash
g++ -std=c++17 -c main.cpp -o main.o
g++ -std=c++17 -c stack.cpp -o stack.o
```

The `-c` flag means compile only, do not link. That is why these commands produce `.o` object files.

The link step combines object files into the final executable:

```bash
g++ main.o stack.o -o program
```

The output is `program`, not `program.o`, because it is the executable. An `.o` file is an intermediate object file, not the final runnable program.

### Q61 - Stream input operator

**Question:** Write the C++ stream line that reads an integer from standard input into `count`, then explain why the opposite arrow direction would be wrong.

Use the extraction operator:

```cpp
std::cin >> count;
```

Read it as:

```text
get input from standard input into count
```

The direction matters. For output, data flows to `std::cout`:

```cpp
std::cout << count;
```

For input, data flows from `std::cin` into the variable:

```cpp
std::cin >> count;
```

So `std::cin << count` is the wrong direction for reading.

### Q62 - `auto` and static typing

**Question:** Given `auto x = 10; x = "hello";`, explain the compile error and what `auto` did, without describing it as dynamic typing.

`auto` asks the compiler to deduce the variable's type from the initializer:

```cpp
auto x = 10;
```

Here, the initializer is an integer, so `x` is deduced as `int`.

This later assignment fails:

```cpp
x = "hello";
```

because `x` is still an `int`. `auto` does not make the variable dynamically typed. It only saves you from writing the type explicitly; the variable still has one fixed compile-time type.

## C Command-line Arguments

### Q63 - `atoi` invalid input vs zero

**Question:** For `int n = atoi(argv[1]);`, compare `argv[1]` values `"abc"` and `"0"`: state what each returns and why the return value alone cannot prove the input was valid.

`atoi` converts a string to an `int`, but it does not give you a separate error result.

```c
#include <stdlib.h>

int a = atoi("abc");
int b = atoi("0");
```

Both calls produce `0`:

```text
atoi("abc") -> 0
atoi("0")   -> 0
```

The first case is invalid input: the string does not start with a valid integer. The second case is valid input: it is the integer zero. Since both return the same value, `atoi` alone cannot tell you whether parsing succeeded.

For checked parsing, use `strtol` instead:

```c
#include <errno.h>
#include <limits.h>
#include <stdlib.h>

char *end = NULL;
errno = 0;

long value = strtol(argv[1], &end, 10);

if (end == argv[1] || *end != '\0' || errno == ERANGE ||
    value < INT_MIN || value > INT_MAX) {
    /* invalid integer */
}
```

The key point is that `atoi` is short but weak. It is fine for quick examples, but it cannot reliably distinguish bad input from a real zero.

### Q64 - `strtol` no digits consumed

**Question:** For `char *end; long n = strtol(text, &end, 10);`, explain what `end == text` means for `text = "abc"`, then say what `*end` should be after a clean full-number parse.

`strtol` writes the stopping position into `end`. That is why `end` is passed by address:

```c
char *end = NULL;
long n = strtol(text, &end, 10);
```

For this input:

```c
char text[] = "abc";
```

there are no digits at the start of the string. `strtol` cannot parse a number, so it leaves `end` pointing at the start:

```c
end == text
```

That means no characters were consumed.

For a clean full-number parse:

```c
char text[] = "123";
char *end = NULL;
long n = strtol(text, &end, 10);
```

the parsed value is `123`, and `end` points at the string terminator:

```c
*end == '\0'
```

So the usual checks are:

```c
if (end == text) {
    /* no digits at the start */
}

if (*end != '\0') {
    /* extra junk after the number */
}
```

For example, `"123abc"` parses `123`, but `end` points at `'a'`, so it is not a clean full-number parse.

## Rust Concurrency and Parallelism

### Q65 - Spawned thread lifetime and `move`

**Question:** In `fn start() { let text = String::from("hi"); thread::spawn(|| println!("{text}")); }`, explain why borrowing `text` is rejected, then fix the spawn with `move` and say why the thread must own the value.

A spawned thread may keep running after the function that created it has returned. The local variable `text` lives in the stack frame of `start`, and that stack frame is destroyed when `start` returns.

This is rejected:

```rust
use std::thread;

fn start() {
    let text = String::from("hi");

    thread::spawn(|| {
        println!("{text}");
    });
}
```

Without `move`, the closure tries to borrow `text`. That would be unsafe because the thread might use the borrow after `start` has returned and `text` has been dropped.

Fix it by moving ownership into the closure:

```rust
use std::thread;

fn start() {
    let text = String::from("hi");

    thread::spawn(move || {
        println!("{text}");
    });
}
```

Now the thread owns `text`, so the value remains valid for as long as the thread needs it. After the move, the parent scope cannot use the original `text` again unless it cloned it first.

### Q66 - Cloned channel transmitters

**Question:** Write the loop for four workers that all send through one `mpsc` channel: clone `tx` for each worker, move the clone into the closure, then explain why every clone still reaches the same `rx`.

An `mpsc` channel has one receiver and one or more transmitters. Cloning `tx` creates another sender handle to the same channel, not a separate channel.

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let mut handles = Vec::new();

    for worker_id in 0..4 {
        let tx = tx.clone();

        handles.push(thread::spawn(move || {
            tx.send(worker_id * 10).unwrap();
        }));
    }

    drop(tx);

    for value in rx {
        println!("{value}");
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
```

Each worker needs its own owned transmitter because the closure is moved into a thread. All the cloned transmitters still feed the same receiver, `rx`, because they are handles to the same channel.

The `drop(tx)` line drops the original sender in `main`. Without it, the `for value in rx` loop could wait forever because one sender would still exist.

### Q67 - `Arc<Mutex<i32>>` shared counter

**Question:** Trace two threads incrementing the same `Arc<Mutex<i32>>` counter and explain how shared ownership is provided and why each update is exclusive.

`Arc` provides shared ownership across threads. `Mutex` protects the value so only one thread can access it through the lock at a time.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();

    for _ in 0..2 {
        let counter = Arc::clone(&counter);

        handles.push(thread::spawn(move || {
            let mut value = counter.lock().unwrap();
            *value += 1;
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("{}", *counter.lock().unwrap());
}
```

Trace:

- Both threads own an `Arc` pointing at the same `Mutex<i32>`.
- A thread calls `lock()` and gets a `MutexGuard`.
- While that guard exists, the mutex is locked.
- The thread updates the protected integer with `*value += 1`.
- When the guard goes out of scope, the mutex unlocks.
- The next thread can then acquire the lock and update the value.

The updates are exclusive because only one thread can hold the mutex guard at a time. With two successful increments, the final value is `2`.

### Q68 - Poisoned mutex lock result

**Question:** For a mutex that was held by a thread when it panicked, write how `lock()` reports the problem and how you would handle the returned result instead of blindly assuming the lock succeeded.

`lock()` returns a `Result`, not the protected value directly. The success case contains a mutex guard.

For a `Mutex<i32>`, the return is roughly:

```rust
Result<MutexGuard<i32>, PoisonError<MutexGuard<i32>>>
```

A mutex becomes poisoned if a thread panics while holding the lock. Later, `lock()` returns `Err(...)` to warn that the protected data may be inconsistent.

Handle the result explicitly:

```rust
use std::sync::Mutex;

let counter = Mutex::new(0);

match counter.lock() {
    Ok(mut value) => {
        *value += 1;
    }
    Err(poisoned) => {
        let mut value = poisoned.into_inner();
        *value += 1;
    }
}
```

For a simple counter, recovering with `into_inner()` may be reasonable. For more complex state, the better answer may be to report the error or stop, because the panic could have left the data halfway through an update.

### Q69 - Local results then final merge

**Question:** For a word-count task split across four threads, compare one global locked `HashMap` updated for every word with each thread building a local map and merging once at the end. Explain which is better and why.

A single global locked `HashMap` is correct but often slow. Every word update needs the same lock:

```text
lock map -> update one word -> unlock map
```

With four threads, they spend a lot of time waiting for the map rather than counting in parallel.

The better pattern is:

```text
thread 1 builds local map for chunk 1
thread 2 builds local map for chunk 2
thread 3 builds local map for chunk 3
thread 4 builds local map for chunk 4
main thread merges the four maps
```

Each worker owns its local `HashMap`, so it does not need to lock for every word:

```rust
use std::collections::HashMap;

fn count_words(words: &[String]) -> HashMap<String, usize> {
    let mut counts = HashMap::new();

    for word in words {
        *counts.entry(word.clone()).or_insert(0) += 1;
    }

    counts
}
```

Then merge local maps:

```rust
let mut final_counts = HashMap::new();

for local_counts in all_local_counts {
    for (word, count) in local_counts {
        *final_counts.entry(word).or_insert(0) += count;
    }
}
```

Local results plus a final merge is usually better because most of the work runs independently without lock contention. The only shared step is the final merge, which is smaller and easier to reason about than locking a global map for every word.

## C++ Error Handling and Lambdas

### Q70 - Stack unwinding and RAII cleanup

**Question:** In a function that creates a local `std::vector<int>` and then calls a function that throws, explain what happens to the vector during stack unwinding and why this is safer than manual cleanup after the throwing call.

When an exception leaves a scope, C++ performs stack unwinding. That means it exits scopes and destroys local objects that were already constructed.

```cpp
#include <vector>

void process() {
    std::vector<int> values(100);

    risky();  // throws
}
```

If `risky()` throws, normal execution does not continue to the next line in `process`. But `values` is still destroyed as the scope is unwound. Its destructor releases the memory it owns.

This is why RAII-managed objects are safer than manual cleanup:

```cpp
void process() {
    int *values = new int[100];

    risky();       // throws

    delete[] values;  // skipped
}
```

In the manual version, the cleanup line is skipped if `risky()` throws. In the RAII version, cleanup is tied to the object's destructor, so it still runs during stack unwinding.

### Q71 - Reference-capture lambda syntax

**Question:** Write the full lambda assignment that captures `counter` by reference, increments the original counter, and includes the required semicolon after the lambda expression.

Capture by reference with `&counter` when the lambda should modify the original variable:

```cpp
int counter = 0;

auto increment = [&counter]() {
    counter += 1;
};
```

The final semicolon is required because this is an assignment statement:

```cpp
auto increment = /* lambda expression */;
```

Calling the lambda changes the original `counter`:

```cpp
increment();
increment();

// counter is now 2
```

Without the reference capture, a value capture would copy `counter` into the lambda. With `[&counter]`, the lambda works with the original variable.

### Q72 - Complete `count_if` lambda call

**Question:** Write a complete `std::count_if` call that counts values greater than 5 in `v`, making sure the lambda body and the algorithm call both have their closing brackets.

`std::count_if` takes a start iterator, an end iterator, and a predicate. The predicate can be a lambda:

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v = {1, 7, 3, 9, 2};

int count = std::count_if(
    v.begin(),
    v.end(),
    [](int value) {
        return value > 5;
    }
);
```

The closing pieces matter:

```cpp
    }   // closes the lambda body
)       // closes the count_if argument list
;       // ends the statement
```

This counts `7` and `9`, so `count` becomes `2`.

## Rust Crash-course Basics

### Q73 - Shadowing parse syntax

**Question:** Starting from `let value = "12";`, use shadowing to parse it as an `i32`, then shadow it again so the final value is one larger.

Use `parse::<i32>()` to tell Rust what type you want from the string. The `::<i32>` part is the turbofish syntax for supplying the target type.

```rust
let value = "12";
let value = value.parse::<i32>().unwrap();
let value = value + 1;

println!("{value}");
```

The first `value` is a string slice. The second `let value` shadows it with an `i32`. The third `let value` shadows that integer with the result of adding one.

After these lines, `value` is:

```text
13
```

This is shadowing, not mutation. Each `let value = ...` creates a new variable with the same name.

### Q74 - `const` declaration syntax

**Question:** A Rust program needs a compile-time maximum user count of 100. Write the constant declaration with the required type annotation and Rust naming style.

Rust constants use `const`, require an explicit type annotation, and are usually named in uppercase with underscores.

```rust
const MAX_USERS: usize = 100;
```

The pieces are:

- `const` means this is a compile-time constant.
- `MAX_USERS` is the constant name.
- `: usize` is the required type annotation.
- `= 100;` assigns the value and ends the declaration.

This is different from a normal local variable:

```rust
let max_users = 100;
```

Use `const` when the value is fixed for the program and should not be an ordinary runtime variable.

### Q75 - Array debug printing

**Question:** Create an array of three integers and print the whole array using the correct debug-format placeholder, then explain why normal display formatting is not the right choice.

Use `{:?}` to print an array with debug formatting:

```rust
let values = [1, 2, 3];
println!("{:?}", values);
```

This prints:

```text
[1, 2, 3]
```

The normal `{}` placeholder uses the `Display` trait. Arrays do not implement `Display` for whole-array printing. They do implement `Debug`, so `{:?}` is the correct placeholder for printing the array structure.

Named formatting also works:

```rust
let values = [1, 2, 3];
println!("{values:?}");
```

### Q76 - Semicolon returns unit

**Question:** Compare `fn f() -> i32 { 5 }` with `fn f() -> i32 { 5; }`: explain which one returns an `i32`, which one returns unit `()`, and why.

In Rust, a final expression without a semicolon becomes the return value of the block.

This works:

```rust
fn f() -> i32 {
    5
}
```

The final expression is `5`, so the function returns an `i32`.

This does not work:

```rust
fn f() -> i32 {
    5;
}
```

The semicolon turns `5` into a statement. A statement does not produce the `i32` return value. The block then evaluates to unit:

```rust
()
```

So the second function effectively returns unit `()`, not `i32`, which conflicts with the declared return type.

## C Memory Debugging Tools

### Q77 - Use-after-free dereference

**Question:** Given `free(p); return *p;`, explain why `p` is stale after `free`, what dereferencing it means, and what kind of behaviour C gives for that access.

After `free(p)`, the allocation that `p` used to point at no longer belongs to your program.

```c
free(p);
return *p;
```

The pointer variable `p` still contains an address, but that address is stale. Dereferencing means using `*p` to read the object at that address. Since the allocation has already been freed, there is no valid object there for your program to read.

This is undefined behaviour:

```text
the program might appear to work
the program might crash
the program might read old data
the program might corrupt later behaviour
```

A safer pattern is to stop using the pointer after `free`. If the pointer remains in scope and might accidentally be reused, set it to `NULL` after freeing:

```c
free(p);
p = NULL;
```

### Q78 - Valgrind full leak-check command

**Question:** Write the command to run `./app` under Valgrind with full leak checking, then add one useful option for tracing where uninitialised values came from.

Build the program with debug information first:

```bash
gcc -g -Wall -Wextra -o app main.c
```

Then run it under Valgrind:

```bash
valgrind --leak-check=full --track-origins=yes ./app
```

The important pieces are:

- `--leak-check=full` asks Valgrind for detailed leak reports.
- `--track-origins=yes` helps trace where uninitialised values came from.
- `./app` is the program being checked.

Valgrind runs the already-built executable under a memory checker. This is different from AddressSanitizer, which is compiled into the program with `-fsanitize=address`.

### Q79 - Debug info for memory-tool reports

**Question:** Explain what `-g` adds to a debug build and why memory tools give more useful reports when source-level debug information is present.

The `-g` flag adds debug information to the compiled program:

```bash
gcc -g -Wall -Wextra -o app main.c
```

This debug information maps machine code back to source-level details such as file names, function names, and line numbers. Memory tools can still detect some problems without it, but their reports are less useful because they may only show raw addresses or less precise locations.

With `-g`, a report can point you toward the relevant source line:

```text
Invalid write of size 4
    at main.c:8
```

That makes it much faster to connect the runtime report to the actual bad access in your code.

### Q80 - First memory-tool error

**Question:** A memory tool prints several invalid reads and writes. Explain which report you would investigate first and why later reports may be consequences of earlier corruption.

Start with the first invalid access reported.

Memory bugs often cascade. One out-of-bounds write can corrupt nearby memory, and that corruption can cause later invalid reads, invalid writes, crashes, or strange values. If you start with the later reports, you may be debugging symptoms instead of the original cause.

Practical workflow:

1. Find the first invalid read or write in the report.
2. Use the file and line number to inspect that source operation.
3. Identify the object being accessed and its valid lifetime or bounds.
4. Fix that first bug.
5. Run the memory tool again.

After the first bug is fixed, some later reports may disappear because they were consequences of the earlier memory corruption.

### Q81 - Memory bugs and undefined behaviour

**Question:** A C program prints the expected answer but AddressSanitizer reports an invalid access. Explain why the program is still wrong and connect this to undefined behaviour.

Correct-looking output does not prove a C program used memory correctly.

If AddressSanitizer reports an invalid access, the program has done something outside the rules of C, such as reading past an array, writing past an allocation, or using memory after `free`. Those are undefined behaviour.

Undefined behaviour means C gives no reliable meaning to the program after that operation. The program might:

- print the expected answer today
- crash tomorrow
- behave differently with another compiler
- corrupt unrelated memory
- fail only when input size changes

So the sanitizer report matters even if the visible output looks right. The correct fix is to remove the invalid access, not to ignore the report because one run happened to print the expected result.

## Rust Custom Iterators and Pipelines

### Q82 - Lazy `map` adapter

**Question:** Given `let doubled = values.iter().map(|n| n * 2);`, explain what `doubled` contains before any consumer runs, then show one way to produce actual values.

`map` is lazy. It does not immediately loop over the vector and build a new vector.

This line creates another iterator:

```rust
let values = vec![1, 2, 3, 4];
let doubled = values.iter().map(|n| *n * 2);
```

At that point, `doubled` means:

```text
an iterator that knows how to double each value when asked
```

No doubled values have been produced yet. A consumer must ask the iterator for values.

For example, `collect` consumes the iterator and builds a vector:

```rust
let values = vec![1, 2, 3, 4];

let doubled: Vec<i32> = values
    .iter()
    .map(|n| *n * 2)
    .collect();

println!("{doubled:?}"); // [2, 4, 6, 8]
```

Other consumers include `sum`, `count`, `any`, `all`, `fold`, and a `for` loop.

### Q83 - Even-square pipeline collection

**Question:** Starting with `let values = vec![1, 2, 3, 4];`, write the full iterator chain that filters even numbers, maps them to squares, and collects with an explicit `Vec` type.

The chain needs three main stages:

1. `filter` keeps only even numbers.
2. `map` turns each kept number into its square.
3. `collect::<Vec<_>>()` builds the final vector.

```rust
let values = vec![1, 2, 3, 4];

let squares = values
    .iter()
    .filter(|n| **n % 2 == 0)
    .map(|n| *n * *n)
    .collect::<Vec<_>>();

println!("{squares:?}"); // [4, 16]
```

The `map` must come before `collect` because `collect` is the consumer at the end of the chain. Once you collect, you are no longer building the iterator pipeline.

The explicit type can also be written on the variable:

```rust
let squares: Vec<i32> = values
    .iter()
    .filter(|n| **n % 2 == 0)
    .map(|n| *n * *n)
    .collect();
```

Both versions tell Rust what collection type to build.

### Q84 - Text word pipeline

**Question:** Given `let text = "Rust, rust! C?";`, write a pipeline that splits into words, lowercases each cleaned word, removes empty strings, and collects into `Vec<String>`.

Use `split_whitespace` to split the sentence, then use `map` to clean and lowercase each word.

```rust
let text = "Rust, rust! C?";

let words: Vec<String> = text
    .split_whitespace()
    .map(|word| {
        word.trim_matches(|ch: char| !ch.is_alphanumeric())
            .to_lowercase()
    })
    .filter(|word| !word.is_empty())
    .collect();

println!("{words:?}"); // ["rust", "rust", "c"]
```

The stages are:

- `split_whitespace()` produces rough word pieces.
- `trim_matches(...)` removes punctuation from the outside of each word.
- `to_lowercase()` creates a lowercase `String`.
- `filter(...)` removes any empty result.
- `collect()` builds the `Vec<String>`.

You do not use `iter_mut` here because `split_whitespace` already returns an iterator over borrowed string slices. The usual Rust style is to create new cleaned strings rather than mutate the original string letter by letter.

### Q85 - HashMap score pipeline

**Question:** Given a map of team names to scores, collect entries with scores at least 10 into a vector, making clear where filtering and copying out borrowed values happen.

With `HashMap<&str, i32>`, `iter()` gives borrowed key-value pairs. The filter checks the borrowed score, then the map step copies out simpler values for the result vector.

```rust
use std::collections::HashMap;

let mut scores: HashMap<&str, i32> = HashMap::new();
scores.insert("red", 12);
scores.insert("blue", 7);
scores.insert("green", 15);

let high: Vec<(&str, i32)> = scores
    .iter()
    .filter(|(_, score)| **score >= 10)
    .map(|(team, score)| (*team, *score))
    .collect();

println!("{high:?}");
```

The `filter` stage decides which entries stay:

```rust
.filter(|(_, score)| **score >= 10)
```

The `map` stage changes the item shape:

```rust
.map(|(team, score)| (*team, *score))
```

That turns borrowed pieces from the map iterator into a cleaner `Vec<(&str, i32)>`.

If you leave out the `map`, you can still collect, but the vector contains references into the original map instead:

```rust
let high_refs: Vec<(&&str, &i32)> = scores
    .iter()
    .filter(|(_, score)| **score >= 10)
    .collect();
```

So the `map` is needed when the target answer wants copied-out key-value pairs rather than the direct borrowed iterator items.

### Q86 - Custom iterator field access

**Question:** In `Counter::next`, fix a body that tries to read `self[current]`; write the correct field access syntax for `current` and explain why indexing syntax is wrong.

For a struct field, use dot syntax:

```rust
self.current
```

not:

```rust
self[current]
```

`self[current]` means “index into `self` using `current` as an index”. That syntax is for indexable things such as arrays, slices, vectors, or types that implement indexing. A `Counter` struct is not being indexed here. You are reading its named field.

Correct `next` body:

```rust
fn next(&mut self) -> Option<Self::Item> {
    if self.current >= self.end {
        None
    } else {
        let value = self.current;
        self.current += 1;
        Some(value)
    }
}
```

The key field accesses are:

```rust
self.current
self.end
```

### Q87 - `next` returns `Option`

**Question:** For a custom counter iterator, explain both possible `next` results: what is returned when there is another value and what is returned when the iterator is finished.

The `next` method returns:

```rust
Option<Self::Item>
```

That means it has two possible result shapes:

```rust
Some(item)
None
```

Use `Some(item)` when the iterator has another value to produce:

```rust
let value = self.current;
self.current += 1;
Some(value)
```

Use `None` when the iterator is finished:

```rust
if self.current >= self.end {
    None
}
```

So for `Counter::new(3)`, repeated calls to `next` produce:

```text
Some(0)
Some(1)
Some(2)
None
```

`Some` means “here is the next item”. `None` means “there are no more items”.

## C Basic Syntax and Program Layout

### Q88 - Semicolons after declarations

**Question:** Given a short program containing `int x = 4`, `double y = 2.5`, and a `printf` call without statement endings, fix every missing semicolon and explain why the declarations need them.

In C, declaration statements and function-call statements normally end with semicolons.

Broken version:

```c
#include <stdio.h>

int main(void) {
    int x = 4
    double y = 2.5
    printf("%d %f\n", x, y)
    return 0;
}
```

Fixed version:

```c
#include <stdio.h>

int main(void) {
    int x = 4;
    double y = 2.5;
    printf("%d %f\n", x, y);
    return 0;
}
```

The second declaration needs its semicolon here:

```c
double y = 2.5;
```

Without it, the declaration statement is unfinished. The compiler then tries to parse the next line as if it is still part of the previous statement, which can make the error appear slightly later than the actual missing semicolon.

### Q89 - Tab escape sequence

**Question:** Write a `printf` statement that prints two integer values separated by a tab and followed by a newline, using the correct escape sequence for the tab.

Use `\t` for a tab and `\n` for a newline:

```c
int a = 10;
int b = 20;

printf("%d\t%d\n", a, b);
```

The output is laid out like this:

```text
10    20
```

The exact width of the gap depends on the terminal's tab stops, but the important escape sequence is:

```c
\t
```

Do not write `/t`. Escape sequences use a backslash:

```c
\t   /* tab */
\n   /* newline */
```

### Q90 - `return 0` from `main`

**Question:** For a small `int main(void)` program that finishes normally, write the final return statement and explain what status it reports to the operating system.

A normal successful `main` usually ends with:

```c
return 0;
```

Full example:

```c
#include <stdio.h>

int main(void) {
    printf("Done\n");
    return 0;
}
```

The return value from `main` is the program's exit status. Returning `0` indicates successful program termination to the operating system.

Non-zero return values usually mean failure or some kind of abnormal result:

```c
return 1;
```

So the key idea is:

```text
return 0 from main = program finished successfully
```

## C Control Flow and Problem Solving

### Q91 - Factorial loop variable

**Question:** Write a factorial loop that counts down from `n` to `1`, then trace `n = 4` and identify which variable must be multiplied into the accumulator each iteration.

Counting down is fine, but the accumulator must multiply by the loop variable, not by `n` every time.

Correct version:

```c
int factorial(int n) {
    int acc = 1;

    for (int i = n; i > 0; i--) {
        acc *= i;
    }

    return acc;
}
```

For `n = 4`, this does:

```text
acc = 1
acc *= 4  -> 4
acc *= 3  -> 12
acc *= 2  -> 24
acc *= 1  -> 24
```

The wrong version is:

```c
acc *= n;
```

because `n` stays the same for the whole loop. For `n = 4`, that would multiply by `4` repeatedly:

```text
1 * 4 * 4 * 4 * 4
```

That is not factorial. The changing loop variable is `i`, so use:

```c
acc *= i;
```

### Q92 - `e` approximation loop bounds

**Question:** Write an `approximate_e(int terms)` loop using factorial terms, making sure the division is floating-point and the loop produces exactly `terms` terms.

The series is:

```text
e = 1/0! + 1/1! + 1/2! + 1/3! + ...
```

If `terms` is the number of terms to include, loop while `n < terms`, not `n <= terms`.

Using the previous `factorial` function:

```c
double approximate_e(int terms) {
    double sum = 0.0;

    for (int n = 0; n < terms; n++) {
        sum += 1.0 / factorial(n);
    }

    return sum;
}
```

The `1.0` matters because it forces floating-point division:

```c
1.0 / factorial(n)
```

If you write:

```c
1 / factorial(n)
```

then both operands are integers, so C performs integer division first. For terms such as `1 / 2`, `1 / 6`, and `1 / 24`, the result becomes `0`, which ruins the approximation.

The loop condition matters too. For `terms = 5`, this loop:

```c
for (int n = 0; n < terms; n++)
```

uses:

```text
n = 0, 1, 2, 3, 4
```

That is exactly five terms. If you used `n <= terms`, you would get six terms.

### Q93 - Object file compile and link workflow

**Question:** For a program split across `main.c` and `maths.c`, write the commands that produce `main.o` and `maths.o`, then link them into an executable.

Use `-c` to compile each source file into an object file without linking:

```bash
gcc -Wall -Wextra -std=c11 -c main.c
gcc -Wall -Wextra -std=c11 -c maths.c
```

These commands produce:

```text
main.c  -> main.o
maths.c -> maths.o
```

Then link the object files into an executable:

```bash
gcc -o app main.o maths.o
```

Then run it:

```bash
./app
```

The important idea is:

```text
.c file -> compile with -c -> .o file
.o files -> link together -> executable program
```

So `maths.o` comes from compiling `maths.c`:

```bash
gcc -c maths.c
```

## C String Processing

### Q94 - `sizeof` on char arrays

**Question:** For `char s[20] = "Hello world";`, calculate the storage size and visible character count, then explain why the two numbers are different.

For a real array, `sizeof` gives the total storage reserved for the whole array.

```c
char s[20] = "Hello world";
```

Here:

```c
sizeof(s)   /* 20 */
strlen(s)   /* 11 */
```

`sizeof(s)` is `20` because `s` is an array with 20 bytes of storage. `strlen(s)` is `11` because it counts only the visible characters before the first null terminator.

The stored string is:

```text
H e l l o   w o r l d \0
```

The array has extra unused space after that. The important rule is:

```text
sizeof = storage size
strlen = characters before '\0'
```

### Q95 - Null terminator and `sizeof`

**Question:** For `char s[20] = "Hello world"; s[0] = '\0';`, calculate `sizeof(s)` and `strlen(s)`, then identify which result changed.

Changing the contents of the string can change `strlen`, but it does not change the size of the array.

```c
char s[20] = "Hello world";
s[0] = '\0';
```

After this:

```c
sizeof(s)   /* still 20 */
strlen(s)   /* now 0 */
```

`sizeof(s)` is still `20` because the array still has 20 bytes of storage. `strlen(s)` is `0` because the first character is now the null terminator, so the string appears empty.

The key point is that `strlen` stops at the first `'\0'`; it does not care what old characters remain later in the array.

### Q96 - In-place normalise write index

**Question:** Trace what goes wrong if an in-place normalise loop increments `write` when punctuation is skipped, then write the corrected loop for `"A, B!"` and the required character-function include.

For in-place filtering, `read` moves through every original character. `write` should move only when a character is kept.

Wrong idea:

```c
if (isalpha(ch)) {
    s[write++] = tolower(ch);
} else {
    write++;   /* wrong */
}
```

That leaves gaps in the output because skipped punctuation still advances the write position. For `"A, B!"`, the comma, space, and exclamation mark should not reserve output positions.

Correct version:

```c
#include <ctype.h>

void normalise(char s[]) {
    int write = 0;

    for (int read = 0; s[read] != '\0'; read++) {
        unsigned char ch = (unsigned char)s[read];

        if (isalnum(ch)) {
            s[write++] = (char)tolower(ch);
        }
    }

    s[write] = '\0';
}
```

For `"A, B!"`, the result is:

```text
ab
```

The required header is:

```c
#include <ctype.h>
```

because `isalnum` and `tolower` come from that header.

### Q97 - Bounded copy loop limit

**Question:** For `char dest[5]` copying from `"Hello"`, compare loop guards `i <= len - 1` and `i < len - 1`; choose the safe one and show where the null terminator is written.

If `dest` has length 5, its valid indexes are:

```text
0 1 2 3 4
```

Index `4` must be saved for the null terminator.

Safe version:

```c
void string_copy(char *dest, size_t len, const char *src) {
    size_t i = 0;

    if (len == 0) {
        return;
    }

    while (i < len - 1 && src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }

    dest[i] = '\0';
}
```

For `len = 5`, this copies at most indexes `0`, `1`, `2`, and `3`, then writes:

```c
dest[4] = '\0';
```

The guard `i <= len - 1` is unsafe because it allows copying into index `len - 1`, leaving no space for the null terminator. The correct guard is:

```c
i < len - 1
```

or equivalently:

```c
i + 1 < len
```

## C++ Multiple Inheritance

### Q98 - Protected member access in derived methods

**Question:** Given a base class with private `i` and protected `j`, and a derived method containing `i = 0; j = 0;`, mark which assignment compiles and explain the access rule using the derived method context.

`protected` means the member can be accessed inside the class that defines it and inside derived class member functions. `private` means only the class that defines it can access it directly.

```cpp
class Base {
    int i;
protected:
    int j;
};

class Derived : public Base {
public:
    void reset() {
        i = 0;  // error
        j = 0;  // ok
    }
};
```

`j = 0;` compiles because `j` is protected in `Base`, so `Derived` member functions may use it.

`i = 0;` does not compile because `i` is private in `Base`. A derived object still contains the base part, including private data, but derived code cannot directly name the private member.

### Q99 - Diamond ambiguity is compile-time

**Question:** For `Bottom` inheriting from both `Left` and `Right`, where each path contains `Base::value`, decide what happens to `b.value = 10;` and whether the issue is compile-time or runtime.

In a non-virtual diamond, the bottom class contains two separate `Base` subobjects.

```cpp
class Base { public: int value; };
class Left : public Base {};
class Right : public Base {};
class Bottom : public Left, public Right {};

Bottom b;
b.value = 10;   // error: ambiguous
```

The object layout is conceptually:

```text
Bottom
- Left
  - Base
    - value
- Right
  - Base
    - value
```

So `b.value` is ambiguous because the compiler cannot tell whether you mean the `value` through `Left` or the `value` through `Right`.

This is a compile-time error. The compiler does not panic at runtime; the program is rejected before it runs.

### Q100 - Selecting one diamond base path

**Question:** In a non-virtual diamond with `Bottom b`, write the assignment that sets the `value` reached through `Left` rather than the one reached through `Right`.

Use scope resolution to choose the path explicitly.

```cpp
class Base { public: int value; };
class Left : public Base {};
class Right : public Base {};
class Bottom : public Left, public Right {};

Bottom b;
b.Left::value = 10;
```

That sets the `Base::value` inside the `Left` part of `Bottom`.

This would set the other copy:

```cpp
b.Right::value = 10;
```

Scope resolution fixes the immediate ambiguity, but it does not remove the duplicated base subobjects. To remove the root cause, make the intermediate classes inherit the common base virtually:

```cpp
class Left : virtual public Base {};
class Right : virtual public Base {};
```

### Q101 - Virtual dispatch trace

**Question:** Given `Animal::speak` is virtual, `Dog::speak` prints `Bark Fido`, and an `Animal *` points at a `Dog`, trace the call through the base pointer and explain why the dog version runs.

When a function is virtual, a call through a base pointer or reference is chosen using the actual object type at runtime.

```cpp
class Animal {
public:
    virtual void speak() const {
        std::cout << "Animal\n";
    }
};

class Dog : public Animal {
public:
    void speak() const override {
        std::cout << "Bark Fido\n";
    }
};

Dog pet;
Animal *ptr = &pet;
ptr->speak();
```

The pointer type is `Animal *`, but the actual object is a `Dog`. Because `speak` is virtual, the call runs:

```cpp
Dog::speak()
```

So the output is:

```text
Bark Fido
```

Without `virtual`, the call through `Animal *` would use the base-class version instead.

### Q102 - Abstract base class instantiation

**Question:** Given `virtual void speak() const = 0;` in `Animal`, decide whether `Animal a("Rex");` compiles, then show what a concrete derived class must provide before it can be instantiated.

This declaration is a pure virtual function:

```cpp
virtual void speak() const = 0;
```

That makes `Animal` an abstract class. You cannot instantiate an abstract class directly:

```cpp
Animal a("Rex");  // error
```

A concrete derived class must override the pure virtual function:

```cpp
class Animal {
public:
    virtual void speak() const = 0;
    virtual ~Animal() = default;
};

class Dog : public Animal {
public:
    void speak() const override {
        std::cout << "Bark\n";
    }
};

Dog d;  // ok
```

The key rule is:

```text
pure virtual function = base class can define an interface, but cannot be created directly
```

## C++ Classes: Access Control and Header Files

### Q103 - Complete guarded class header

**Question:** A header `counter.h` declares a `Counter` class and may be included through several files. Write the complete guarded header around the class declaration so repeated inclusion is safe.

Use an include guard around the whole header contents. The guard name is usually based on the header filename.

```cpp
#ifndef COUNTER_H
#define COUNTER_H

class Counter {
private:
    int count;
public:
    Counter();
    void increment();
    int value() const;
};

#endif /* COUNTER_H */
```

The first include defines `COUNTER_H`. If the same header is included again in the same translation unit, the `#ifndef` fails and the class declaration is skipped. This prevents repeated class definitions.

### Q104 - Scope resolution for member definitions

**Question:** In `counter.cpp`, fix `void increment() { count++; }` so it defines the member declared in `Counter`, then explain what the prefix connects the function body to.

Outside the class body, a member function definition needs the class name and scope-resolution operator:

```cpp
void Counter::increment() {
    count++;
}
```

`Counter::` tells the compiler that this function body belongs to the `Counter` class. Without the prefix, this would define a separate free function called `increment`, not the class member. A free function would also not have direct access to the private member `count`.

### Q105 - Balanced include guard

**Question:** Complete a guarded `sensor.h` header from the opening conditional directive through the final closing directive, using a sensible guard name.

The guard needs an opening `#ifndef`, a matching `#define`, and a final `#endif`.

```cpp
#ifndef SENSOR_H
#define SENSOR_H

class Sensor {
public:
    double read() const;
};

#endif /* SENSOR_H */
```

A common mistake is to write the opening lines but forget the closing `#endif`. The guarded region must cover the declarations in the header.

### Q106 - Repeated include redefinition fix

**Question:** `grandparent.h` defines `struct Data` and is included both directly and through `parent.h`. Wrap `grandparent.h` so `child.cpp` does not see two definitions.

Put the include guard in the header that is being included more than once:

```cpp
#ifndef GRANDPARENT_H
#define GRANDPARENT_H

struct Data {
    int value;
};

#endif /* GRANDPARENT_H */
```

If `child.cpp` includes `grandparent.h` directly and also gets it through `parent.h`, the first include defines `GRANDPARENT_H`. The second include then skips the guarded contents, so `struct Data` is only seen once.

### Q107 - Destructor for owned array

**Question:** Given `class Buffer { char *data; public: Buffer(int size) { data = new char[size]; } };`, add the destructor and explain why a default destructor is not enough.

The class owns a dynamic array, so the destructor must release it with `delete[]`.

```cpp
class Buffer {
    char *data;
public:
    Buffer(int size) {
        data = new char[size];
    }

    ~Buffer() {
        delete[] data;
    }
};
```

The default destructor would destroy the pointer variable itself, but it would not delete the heap array that the pointer points to. That would leak memory.

For a real owning class, also think about copying: if copying is allowed, you need proper copy behavior or deleted copy operations to avoid double deletion.

### Q108 - `new`/`delete` vs `malloc`/`free` for objects

**Question:** For a class with a constructor and destructor, compare allocation with `new` and `malloc`, then compare cleanup with `delete` and `free`; say which operations run object lifetime code.

`new` allocates storage and runs the constructor:

```cpp
Widget *w = new Widget(5);
```

`delete` runs the destructor and releases the storage:

```cpp
delete w;
```

`malloc` only allocates raw bytes. It does not run a C++ constructor:

```cpp
Widget *w = static_cast<Widget *>(std::malloc(sizeof(Widget))); // raw storage only
```

`free` releases raw storage. It does not run a destructor.

So for normal C++ objects, use `new`/`delete` or, better, RAII containers/smart pointers. Do not allocate an object with `new` and clean it with `free`, and do not allocate with `malloc` then clean with `delete`.

## C Struct Exercises: Points and Rectangles

### Q109 - Semicolons in struct field declarations

**Question:** Repair `typedef struct { double x double y } Point;` so it is a valid C type definition, then declare one `Point` variable.

Each field declaration needs a semicolon, and the whole typedef declaration also ends with a semicolon.

```c
typedef struct {
    double x;
    double y;
} Point;

Point pt;
```

The final `Point` is the typedef alias. It lets you write `Point pt;` instead of `struct ...` syntax.

### Q110 - Nested struct field semicolons

**Question:** Write a `Rectangle` type containing `Point bottom_left` and `Point top_right`, making sure the field declarations and the whole type definition are correctly terminated.

A struct can contain fields whose type is another struct type. Each field still needs its own semicolon.

```c
typedef struct {
    Point bottom_left;
    Point top_right;
} Rectangle;
```

The semicolon after `top_right` ends that field declaration. The semicolon after `} Rectangle` ends the typedef declaration.

### Q111 - Updating caller-owned struct through pointer

**Question:** Fix `void move_point(Point p, double dx, double dy)` so the caller's point is changed, then show the corrected call for a variable named `pt`.

Passing a struct by value gives the function a copy. Changing that copy does not change the caller's original variable.

Broken version:

```c
void move_point(Point p, double dx, double dy) {
    p.x += dx;
    p.y += dy;
}
```

For the C worksheet version, pass a pointer to the caller's object and use `->`:

```c
void move_point(Point *p, double dx, double dy) {
    p->x += dx;
    p->y += dy;
}

Point pt = {1.0, 2.0};
move_point(&pt, dx, dy);
```

`&pt` passes the address of the caller's variable. Inside the function, `p->x` accesses the `x` field of the pointed-to `Point`.

### Q112 - Choosing pass-by-value for structs

**Question:** A function only reads a small `Point` to calculate a result and must not modify the caller's value. Choose a by-value or pointer parameter and justify the choice.

Passing by value is reasonable for a small read-only struct such as:

```c
typedef struct {
    double x;
    double y;
} Point;
```

Example:

```c
double distance_sq(Point a, Point b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return dx * dx + dy * dy;
}
```

The function only reads the points, and copying two `double` fields is simple. Passing by value also prevents the function from accidentally modifying the caller's objects.

Use a pointer when the function needs to modify the caller's struct or when copying a large struct would be wasteful.

### Q113 - Struct size, padding, and alignment

**Question:** Compare `sizeof` for a two-double `Point` with a struct containing `char c; double x;`. Explain why the mixed-field struct may be larger than the simple sum of field sizes.

A two-double `Point` is typically 16 bytes on a system where `sizeof(double)` is 8:

```c
typedef struct {
    double x;
    double y;
} Point;
```

```text
sizeof(Point) is typically 16
```

A mixed-field struct can be larger than the simple sum of its fields because the compiler may insert padding for alignment:

```c
typedef struct {
    char c;
    double x;
} Mixed;
```

The fields themselves might total 1 + 8 = 9 bytes, but the struct may be 16 bytes because padding is inserted between `c` and `x`, and possibly at the end, so the `double` is correctly aligned.

## Rust Tooling and Cargo

### Q114 - Cargo as build tool and package manager

**Question:** A Rust project uses Cargo where a C project might need separate build and dependency tools. Name the two jobs Cargo handles and give one command or file connected to each job.

Cargo is both a build system and a package manager.

As a build system, it compiles, checks, runs, and tests the project:

```bash
cargo check
cargo build
cargo run
cargo test
```

As a package manager, it reads dependency information from `Cargo.toml` and records exact resolved versions in `Cargo.lock`.

```toml
[dependencies]
rand = "0.9"
```

So the two jobs are:

- build system: commands such as `cargo build`, `cargo run`, `cargo test`
- package manager: dependency configuration in `Cargo.toml` and locked versions in `Cargo.lock`

### Q115 - `cargo new` project layout

**Question:** After running `cargo new hello_rust`, list the generated source entry point path and the main Cargo config files, then say which file contains the starting `main` function.

A basic binary project looks like this:

```text
hello_rust/
  Cargo.toml
  Cargo.lock        # may appear after building/resolving dependencies
  src/
    main.rs
```

The starting `main` function is in:

```text
src/main.rs
```

`Cargo.toml` stores the package name, version, edition, and dependencies. `Cargo.lock` records exact dependency versions once generated.

### Q116 - `cargo run` with unchanged source

**Question:** After a successful build, no source files have changed. Explain what `cargo run` does next and whether it recompiles or runs the existing binary.

`cargo run` checks whether the project is up to date. If no relevant source files or dependencies have changed, Cargo does not need to recompile the crate.

It runs the existing binary from the target directory, usually under:

```text
target/debug/
```

If a source file, dependency, or build setting has changed, Cargo rebuilds what is needed before running.

### Q117 - Opening Rust Book offline

**Question:** On a machine with Rust docs installed but no internet connection, write the command that opens the Rust Book and distinguish it from opening the general local Rust documentation.

To open the Rust Book directly:

```bash
rustup doc --book
```

To open the broader local Rust documentation:

```bash
rustup doc
```

The `--book` flag targets the Rust Book specifically. Without it, `rustup doc` opens the general installed documentation index.

## Rust Ownership, Closures, Lifetimes, and Smart Pointers

### Q118 - Closure capture mode for copied values

**Question:** Given `let factor = 3; let scale = |n: i32| n * factor;` and then a `move` version of the same closure, explain how `factor` is captured in each case and whether the original `factor` can still be printed.

Without `move`, the closure can borrow `factor` from the surrounding scope because it only needs to read it:

```rust
let factor = 3;
let scale = |n: i32| n * factor;
println!("{}", scale(4));
println!("{factor}");
```

With `move`, the closure captures `factor` by value:

```rust
let factor = 3;
let scale = move |n: i32| n * factor;
println!("{}", scale(4));
println!("{factor}");
```

This still allows printing the original `factor` because `i32` is `Copy`. The moved value is copied into the closure. If `factor` were a non-`Copy` type such as `String`, a `move` closure could move ownership into the closure and the original binding might no longer be usable.

### Q119 - Returning owned data or input borrows

**Question:** Given `fn bad() -> &str { let text = String::from("hello"); &text }`, explain why the returned reference is invalid, then rewrite it once by returning an owned `String` and once by returning a reference to input data.

This is invalid:

```rust
fn bad() -> &str {
    let text = String::from("hello");
    &text
}
```

`text` is local to the function and is dropped when the function returns. Returning `&text` would leave the caller with a dangling reference, so Rust rejects it.

Return owned data instead:

```rust
fn good_owned() -> String {
    String::from("hello")
}
```

Or return a reference to input data that outlives the function call:

```rust
fn good_borrowed(text: &str) -> &str {
    text
}
```

The borrowed version is valid because the returned reference points into data owned by the caller, not into a local variable that is about to be dropped.

### Q120 - Dereferencing a borrowed Box

**Question:** Complete `fn read_boxed(n: &Box<i32>) -> i32` so it returns the inner integer, then explain what each dereference step is doing.

A `Box<i32>` owns an `i32` on the heap. A `&Box<i32>` is a reference to that box. To read the integer, dereference twice:

```rust
fn read_boxed(n: &Box<i32>) -> i32 {
    **n
}
```

The first dereference follows the `&Box<i32>` to the `Box<i32>`. The second dereference follows the `Box<i32>` to the inner `i32` on the heap. Returning the `i32` is fine because `i32` is `Copy`.

## Rust Practical Projects and Data

### Q121 - Unit test module shape

**Question:** Inside `src/lib.rs`, write the unit test module for `pub fn square(n: i32) -> i32 { n * n }`, importing the parent module correctly and ending the assertion statement properly.

Unit tests beside the code can use `super::*` to import items from the parent module.

```rust
pub fn square(n: i32) -> i32 {
    n * n
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn square_works() {
        assert_eq!(square(5), 25);
    }
}
```

The `assert_eq!` line is a statement, so it ends with a semicolon.

### Q122 - Integration tests use public API

**Question:** Given a private `helper` used by public `public_api`, explain why `tests/basic.rs` cannot import `helper`, then write the valid import and assertion against the public function.

Integration tests in `tests/` are compiled like outside crates. They can only use the crate's public API.

If the library is:

```rust
fn helper(n: i32) -> i32 {
    n + 1
}

pub fn public_api(n: i32) -> i32 {
    helper(n)
}
```

Then `tests/basic.rs` should test through the public function:

```rust
use calc::public_api;

#[test]
fn public_api_works() {
    assert_eq!(public_api(4), 5);
}
```

Do not import `helper` from an integration test unless it is intentionally made `pub` as part of the public API.

### Q123 - Command-line argument positions

**Question:** For `cargo run -- 12 2.5`, label `args[0]`, `args[1]`, and `args[2]`, including what kind of value `args[0]` usually contains.

`std::env::args()` gives strings. For:

```bash
cargo run -- 12 2.5
```

The program usually sees:

```text
args[0] = path/name of the program, such as target/debug/app
args[1] = "12"
args[2] = "2.5"
```

All of these are `String` values. The numeric-looking arguments still need parsing before they can be used as numbers.

### Q124 - Parse error handling with `match`

**Question:** Replace `let count: i32 = args[1].parse().unwrap();` with a `match` that uses the parsed value on success and prints an error before returning on invalid input.

Avoid `unwrap()` when invalid input should be handled gracefully.

```rust
let count: i32 = match args[1].parse() {
    Ok(n) => n,
    Err(_) => {
        eprintln!("invalid count");
        return;
    }
};
```

The `Ok(n)` arm gives the parsed integer. The `Err(_)` arm handles any parse error, prints a message, and returns early from the current function.

### Q125 - Parse target type syntax

**Question:** Complete `let n = text.trim().____?;` inside `parse_count` so the parse target is `i32` and the surrounding `Result` can return parse errors early.

Use turbofish syntax to state the parse target type:

```rust
pub fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = text.trim().parse::<i32>()?;
    Ok(n)
}
```

`parse::<i32>()` tells Rust which type to parse. The `?` returns the parse error early if parsing fails.

### Q126 - Accumulating totals in a `HashMap`

**Question:** A totals map already contains `tea -> 2.50`. Given another tea item with quantity 3 and unit price 1.25, write the update so the stored tea total becomes 6.25 rather than being replaced or ignored.

Use the `entry` API to get a mutable reference to the existing total, inserting `0.0` only if the key is missing.

```rust
*totals.entry(item.name.clone()).or_insert(0.0) +=
    item.quantity as f64 * item.unit_price;
```

For the given numbers, the new line total is:

```text
3 * 1.25 = 3.75
```

The old total was `2.50`, so the updated total is:

```text
2.50 + 3.75 = 6.25
```

The dereference `*` is needed because `or_insert` returns a mutable reference to the value stored in the map.

### Q127 - Dereferencing iterator values

**Question:** In `for (index, value) in values.iter().enumerate()`, complete the comparison that returns `Some(index)` when the borrowed value is greater than `threshold`.

`values.iter()` yields references to the values, so `value` is a borrowed integer. Dereference it before comparing with `threshold`:

```rust
pub fn first_greater_than(values: &[i32], threshold: i32) -> Option<usize> {
    for (index, value) in values.iter().enumerate() {
        if *value > threshold {
            return Some(index);
        }
    }

    None
}
```

`index` comes from `enumerate()`. `Some(index)` is returned for the first matching value. If no value matches, the function returns `None` after the loop.

### Q128 - Tuple destructuring from borrowed iteration

**Question:** Given `for (name, score) in rows.iter()`, explain what `(name, score)` pulls out and why those bindings are references rather than owned values.

If `rows` is a vector of tuples, `rows.iter()` borrows each tuple rather than moving it out of the vector.

```rust
let rows = vec![
    (String::from("red"), 10),
    (String::from("blue"), 7),
];

for (name, score) in rows.iter() {
    println!("{name}: {score}");
}
```

The pattern `(name, score)` destructures each tuple into its two fields. Because the loop is over `rows.iter()`, those fields are borrowed. So `name` is a reference to the `String`, and `score` is a reference to the integer.

This avoids taking ownership of the values out of `rows`, so `rows` can still be used after the loop.

## C++ Build Systems, STL Algorithms, and Shared Ownership

### Q129 - CMake role vs compiler role

**Question:** Given `cmake -S . -B build` followed by `cmake --build build`, explain what CMake configures or drives, and whether the actual compile/link work is still done by compiler tools such as `g++`.

CMake is a build-system generator and build driver. It is not the C++ compiler itself.

```bash
cmake -S . -B build
cmake --build build
```

The first command reads the project files from the current source directory and creates build files in the `build` directory. The second command asks the generated build system to build the project.

The actual compiling and linking is still done by compiler/linker tools, such as `g++`, underneath the build system.

### Q130 - `binary_search` requires matching sorted order

**Question:** Given `std::vector<int> values = {8, 2, 5, 1};` followed by `std::binary_search(values.begin(), values.end(), 5)`, add the minimum fix for the default search and explain why a descending sort comparator would not match that default search.

`std::binary_search` only works correctly when the range is already sorted using the same ordering that the search expects.

With the default `binary_search`, sort ascending first:

```cpp
std::vector<int> values = {8, 2, 5, 1};

std::sort(values.begin(), values.end());
bool found = std::binary_search(values.begin(), values.end(), 5);
```

Do not add a descending comparator here unless the `binary_search` call uses the same comparator too. This would be inconsistent:

```cpp
std::sort(values.begin(), values.end(), [](int a, int b) {
    return a > b;
});

bool found = std::binary_search(values.begin(), values.end(), 5);
```

The vector is sorted descending, but the search still assumes the default ascending order.

### Q131 - Descending `std::sort` comparator direction

**Question:** Complete a `std::sort` comparator for largest-first integer scores, then explain what the comparator's true result means about the order of its two arguments.

For descending order, the comparator should return `true` when the first value should come before the second value.

```cpp
std::vector<int> scores = {4, 10, 7};

std::sort(scores.begin(), scores.end(), [](int a, int b) {
    return a > b;
});
```

`a > b` means the larger value comes first, so the sorted result is:

```text
10, 7, 4
```

Using `a < b` would sort ascending instead:

```text
4, 7, 10
```

## C Builds, Libraries, and Buffering

### Q132 - Flushing buffered stdout

**Question:** Given `printf("A"); printf("B"); fflush(stdout); printf("C\n");`, explain what `fflush(stdout)` forces to happen before the newline is printed.

`printf` writes to the `stdout` stream, but that stream may buffer output before it appears on the terminal.

```c
printf("A");
printf("B");
fflush(stdout);
printf("C\n");
```

`fflush(stdout)` forces any pending buffered `stdout` output to be written immediately. In this fragment, it forces `A` and `B` out before the later `printf("C\n")`.

Without the flush, `A` and `B` might wait until a newline, a full buffer, or program exit.

### Q133 - Makefile object compile rule

**Question:** Complete the Makefile command for `stack.o: stack.c stack.h`, using the compiler, C standard flag, compile-only step, source file, and named object output.

The rule is for building one object file from one C source file:

```make
stack.o: stack.c stack.h
	$(CC) $(CFLAGS) -c stack.c -o stack.o
```

If the variables are:

```make
CC = gcc
CFLAGS = -std=c99
```

then the command expands to:

```bash
gcc -std=c99 -c stack.c -o stack.o
```

`-c` means compile only and stop before linking. `-o stack.o` names the object-file output.

### Q134 - Recompile one source and reuse object file

**Question:** Given `stack.o` already exists, `main.c` changed, and `stack.c` did not change, write the commands that recompile only `main.c` into `main.o` and then link with the existing `stack.o`.

Only `main.c` needs recompiling:

```bash
gcc -std=c99 -c main.c -o main.o
```

Then link the fresh `main.o` with the existing `stack.o`:

```bash
gcc main.o stack.o -o program
```

Do not recompile `stack.c` if `stack.o` is already up to date. The `-c` flag is needed on the compile step because you are producing an object file, not the final executable yet.

### Q135 - Recompile objects then relink executable

**Question:** Given `program` depends on `main.o` and `stack.o`, and both object files depend on `stack.h`, explain exactly what happens to the two object files and to `program` after `stack.h` changes.

For this dependency graph:

```make
program: main.o stack.o
main.o: main.c stack.h
stack.o: stack.c stack.h
```

If `stack.h` changes, both object files are out of date because both list `stack.h` as a prerequisite.

So `make` recompiles:

```text
main.c  -> main.o
stack.c -> stack.o
```

Then `program` is **relinked**:

```bash
gcc main.o stack.o -o program
```

The final step is specifically linking again, not recompiling `program.c`. `program` is the executable made from object files.

### Q136 - Make target already up to date

**Question:** Given `make: 'program' is up to date`, explain what this says about whether `program` exists and how its timestamp compares with the files it depends on.

This message means `make` found no work to do for that target.

For example:

```make
program: main.o stack.o
	gcc main.o stack.o -o program
```

If `program` exists and is newer than, or the same age as, `main.o` and `stack.o`, then none of its prerequisites have changed since it was built.

So `make` does not run the link command again.

If one prerequisite becomes newer than `program`, such as after recompiling `main.o`, then `program` is out of date and must be relinked.

### Q137 - Makefile clean command

**Question:** Write a `clean` recipe command that removes all `.o` files and the `program` executable, then explain what `-f` and `*.o` do.

A typical clean rule is:

```make
clean:
	rm -f *.o program
```

`rm` removes files.

`-f` means force: do not ask for confirmation and do not complain if a matching file is missing.

`*.o` matches all object files in the current directory, such as:

```text
main.o
stack.o
maths.o
```

So the command deletes object files and the final executable named `program`.

## Rust Control Flow, Sorting, and Tooling

### Q138 - Semicolon turns return expression into statement

**Question:** Given `fn double(n: i32) -> i32 { n * 2; }`, explain what the function body evaluates to and fix it so it returns an `i32`.

In Rust, the final expression in a block is returned if it has no semicolon.

This does not compile:

```rust
fn double(n: i32) -> i32 {
    n * 2;
}
```

The semicolon turns `n * 2` into a statement. A statement does not produce the function's return value, so the block evaluates to unit:

```rust
()
```

Fix it by removing the semicolon:

```rust
fn double(n: i32) -> i32 {
    n * 2
}
```

Or use an explicit return:

```rust
fn double(n: i32) -> i32 {
    return n * 2;
}
```

### Q139 - `if` as an expression needs both branch values

**Question:** Given `let score = 72;`, write one `let result = ...;` binding using `if` as an expression to produce `"pass"` or `"fail"`, and explain why the assigned expression needs an `else` branch.

When `if` is used to assign a value, both branches must produce a compatible value.

```rust
let score = 72;

let result = if score >= 40 {
    "pass"
} else {
    "fail"
};
```

The `else` is needed because `result` must always receive a value. If the condition is false and there is no `else`, there is no value to assign.

This block is valid syntax, but it is not the right solution:

```rust
let result = {
    if score >= 40 {
        "pass"
    }

    "fail"
};
```

The final expression in that block is always `"fail"`, so the earlier `"pass"` value is ignored.

### Q140 - Rust `sort_by` with descending primary key

**Question:** Given `let mut items = vec![(2, "red"), (5, "blue"), (5, "amber")];`, write the `sort_by` call with `|a, b|` that sorts by count descending and then word ascending.

Use `sort_by` on the vector itself, not on `items.iter()`, because sorting must rearrange the actual vector.

```rust
let mut items = vec![
    (2, "red"),
    (5, "blue"),
    (5, "amber"),
];

items.sort_by(|a, b| {
    b.0.cmp(&a.0).then_with(|| a.1.cmp(&b.1))
});
```

`b.0.cmp(&a.0)` reverses the count comparison, so larger counts come first.

`then_with(|| a.1.cmp(&b.1))` is the tie-breaker. It only runs when the counts are equal, and it sorts the words alphabetically.

The result is:

```rust
[(5, "amber"), (5, "blue"), (2, "red")]
```

### Q141 - Sorting floats with `partial_cmp`

**Question:** Given `let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];`, write the `sort_by` call with `|a, b|` that sorts by float ascending and then id ascending.

Floating-point values use `partial_cmp` because `NaN` means floats do not always have a total ordering.

```rust
let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];

readings.sort_by(|a, b| {
    a.0.partial_cmp(&b.0)
        .unwrap()
        .then_with(|| a.1.cmp(&b.1))
});
```

`partial_cmp` returns an `Option<Ordering>`. For ordinary finite values, `unwrap()` gives the ordering. If a value is `NaN`, `partial_cmp` can return `None`.

The tie-breaker:

```rust
then_with(|| a.1.cmp(&b.1))
```

sorts the id ascending when the float values are equal.

### Q142 - Sort then collect top entries

**Question:** Given a mutable vector of `(String, i32)` scores, sort highest score first and collect an owned `Vec` containing the top two entries.

Sort the vector by the score field descending, then consume the vector and take the first two entries.

```rust
let mut scores = vec![
    (String::from("Ada"), 12),
    (String::from("Grace"), 18),
    (String::from("Linus"), 15),
];

scores.sort_by(|a, b| {
    b.1.cmp(&a.1)
});

let top_two: Vec<_> = scores
    .into_iter()
    .take(2)
    .collect();
```

`b.1.cmp(&a.1)` sorts by the second tuple field descending.

`into_iter()` consumes `scores` and yields owned `(String, i32)` values, so `top_two` owns its entries.

If you used `iter()` instead:

```rust
let top_two: Vec<_> = scores.iter().take(2).collect();
```

the result would contain references to entries inside `scores`, not owned entries.

### Q143 - Makefile clean rule

**Question:** For the mock project with `main.c`, `stats.c`, and `stats.h`, write the full Makefile fragment for `report`, then include the `clean` recipe that removes all object files and the `report` executable.

The Makefile needs rules for the executable, each object file, and cleanup.

```make
CC = gcc
CFLAGS = -std=c99 -Wall -Wextra

report: main.o stats.o
<TAB>$(CC) $(CFLAGS) main.o stats.o -o report

main.o: main.c stats.h
<TAB>$(CC) $(CFLAGS) -c main.c -o main.o

stats.o: stats.c stats.h
<TAB>$(CC) $(CFLAGS) -c stats.c -o stats.o

clean:
<TAB>rm -f *.o report
```

The command line under a Makefile target must start with a real tab.

`rm` removes files. The `-f` option means force: do not complain if a file is already missing. The pattern `*.o` matches object files such as `main.o` and `stats.o`. The final `report` removes the executable.

`clean` is not part of normal compilation unless you run it explicitly:

```sh
make clean
```

### Q144 - Heap string copy allocation

**Question:** In the `copy_label(const char *src)` stub, fill in `char *copy = ...`, the allocation failure check, and the copy step so the result includes room for the string terminator.

`strlen(src)` counts the visible characters before the string terminator. It does not count the final `'\0'`, so the allocation needs one extra byte.

```c
#include <stdlib.h>
#include <string.h>

char *copy_label(const char *src) {
    char *copy = malloc(strlen(src) + 1);
    if (copy == NULL) {
        return NULL;
    }

    strcpy(copy, src);
    return copy;
}
```

The caller owns the returned heap allocation and must later call:

```c
free(copy);
```

### Q145 - `qsort` comparator ordering

**Question:** For `typedef struct { char name[16]; int score; } Entry;`, complete `compare_entries` and `sort_entries` so `qsort` orders score descending and name ascending on ties.

`qsort` does not want a true or false answer. Its comparator must return a negative value, zero, or a positive value:

```text
negative: left item comes before right item
zero: equal for sorting purposes
positive: left item comes after right item
```

For score descending, the larger score should come first:

```c
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[16];
    int score;
} Entry;

int compare_entries(const void *left, const void *right) {
    const Entry *a = left;
    const Entry *b = right;

    if (a->score > b->score) {
        return -1;
    }
    if (a->score < b->score) {
        return 1;
    }

    return strcmp(a->name, b->name);
}

void sort_entries(Entry entries[], size_t len) {
    qsort(entries, len, sizeof entries[0], compare_entries);
}
```

The final `strcmp` is the tie-breaker. It sorts names ascending when the scores are equal.

This is not enough:

```c
return a->score > b->score;
```

That only returns `1` or `0`, so it cannot properly distinguish less-than, equal, and greater-than cases. It also gives the wrong sign for descending order.

### Q146 - Dangling pointer after `free`

**Question:** For the mock code `int *p = malloc(sizeof *p); *p = 10; free(p); printf("%d\n", *p);`, explain why `p` is dangling and what C behaviour dereferencing it gives.

After `free(p)`, the heap object that `p` pointed to is no longer owned by your program.

```c
int *p = malloc(sizeof *p);
*p = 10;

free(p);
printf("%d\n", *p);
```

The variable `p` may still contain the old address, but that address is stale. A pointer in this state is called a dangling pointer.

Dereferencing it means trying to read the object at that old address:

```c
*p
```

Because the object has already been freed, this is a use-after-free. In C, that gives undefined behaviour. The program might print the old value, print nonsense, crash, or appear to work.

### Q147 - Rule of three for raw heap arrays

**Question:** For the mock `Buffer` class with `char *data`, `new char[size]`, and `~Buffer() = default`, identify the leak and explain why a raw-owning fix also needs a copy constructor and copy assignment operator.

If a class allocates a raw heap array:

```cpp
class Buffer {
    char *data;

public:
    Buffer(int size) {
        data = new char[size];
    }
};
```

then the destructor must release it:

```cpp
~Buffer() {
    delete[] data;
}
```

However, that alone is not enough. The compiler-generated copy constructor and copy assignment operator would copy only the pointer value.

```cpp
Buffer a(10);
Buffer b = a;
```

Now `a.data` and `b.data` point to the same heap array. If both destructors call `delete[] data`, the same allocation can be deleted twice.

This is why the rule of three says that if you need one of these, you probably need all three:

```cpp
~Buffer();
Buffer(const Buffer& other);
Buffer& operator=(const Buffer& other);
```

A simpler modern fix is to use an RAII member such as:

```cpp
#include <vector>

class Buffer {
    std::vector<char> data;

public:
    explicit Buffer(int size) : data(size) {}
};
```

The vector handles destruction and copying correctly.

### Q148 - `shared_ptr` last owner lifetime

**Question:** Trace the mock `shared_ptr`/`weak_ptr` code with `a`, `watch`, `b = a`, and `a.reset()`: decide whether `watch.lock()` succeeds and when the shared int is destroyed.

`std::shared_ptr` destroys the owned object only when the last shared owner is gone.

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

After:

```cpp
auto b = a;
```

there are two shared owners: `a` and `b`.

After:

```cpp
a.reset();
```

`a` owns nothing, but `b` still owns the integer. The object is still alive, so `watch.lock()` succeeds and returns a `shared_ptr` to the same integer.

The integer is destroyed only when the final `shared_ptr` owner is gone.

### Q149 - Catching exceptions by const reference

**Question:** For `catch (const std::invalid_argument& error)` after throwing `std::invalid_argument("negative age")`, explain why const reference is used and what `error.what()` prints.

Catch exception objects by const reference:

```cpp
#include <stdexcept>
#include <iostream>

try {
    throw std::invalid_argument("negative age");
} catch (const std::invalid_argument& error) {
    std::cerr << error.what() << "\n";
}
```

The reference avoids copying the exception object. The `const` part means the handler promises not to modify the exception.

This matters especially when catching through a base type such as `std::exception`, because catching by reference preserves the real dynamic exception object. Catching by value can copy and slice exception objects.

`error.what()` returns a C-style string describing the exception. In this example, it returns the message:

```text
negative age
```

### Q150 - Float sorting unwrap after `partial_cmp`

**Question:** Given `let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];`, write the `sort_by` call for float ascending and id descending, including `partial_cmp(...).unwrap()`.

Floating-point comparison uses `partial_cmp` because a float can be `NaN`. If either value is `NaN`, Rust cannot produce a normal ordering.

```rust
let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];

readings.sort_by(|a, b| {
    a.0.partial_cmp(&b.0)
        .unwrap()
        .then_with(|| b.1.cmp(&a.1))
});
```

The `unwrap()` belongs immediately after `partial_cmp` because `partial_cmp` returns:

```rust
Option<std::cmp::Ordering>
```

For normal float values, it returns `Some(Ordering::Less)`, `Some(Ordering::Equal)`, or `Some(Ordering::Greater)`. The `unwrap()` extracts that ordering.

If a `NaN` is involved, `partial_cmp` returns `None`, and `unwrap()` would panic. In exam code, this usually means you are assuming the readings do not contain `NaN`.

The tie-breaker:

```rust
then_with(|| b.1.cmp(&a.1))
```

sorts the id descending when the float values are equal.

### Q151 - Semicolon after Rust `let` parse statement

**Question:** In the mock `parse_count` function returning `Result<i32, ParseIntError>`, write the parsing `let n = ...?;` line and explain why that line needs a semicolon but `Ok(n)` does not.

A `let` binding is a statement, so it needs a semicolon:

```rust
fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = text.trim().parse::<i32>()?;
    Ok(n)
}
```

The `?` means: if parsing succeeds, put the parsed `i32` into `n`; if parsing fails, return the parse error early from the function.

The final line has no semicolon:

```rust
Ok(n)
```

because it is the function's final expression. Adding a semicolon would turn it into a statement and the function body would evaluate to unit `()`, not `Result<i32, ParseIntError>`.

### Q152 - Channel send and dropping original sender

**Question:** In the mock `mpsc` program with `let (tx, rx) = mpsc::channel()` and `for id in 0..4`, spawn workers that send `id * 10`, then explain why `drop(tx)` is needed before `for value in rx` can finish.

Each worker needs its own cloned sender, moved into the thread:

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    for id in 0..4 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(id * 10).unwrap();
        });
    }

    drop(tx);

    for value in rx {
        println!("{value}");
    }
}
```

`tx.send(id * 10).unwrap()` sends the worker's value and panics if the receiver has already gone away.

All cloned `tx` values send to the same `rx`, because they are handles to the same channel.

The receiving loop:

```rust
for value in rx
```

ends only when all senders have been dropped. The worker senders disappear when their threads finish, but the original `tx` in `main` would still exist unless you call:

```rust
drop(tx);
```

Without that, the receiver may keep waiting because it thinks another value could still be sent.

### Q153 - Mutex lock result and guard lifetime

**Question:** In the mock `Arc<Mutex<i32>>` counter loop, complete the spawned closure so it locks, unwraps, increments through the guard, and explain when the guard unlocks the mutex.

Use `Arc` for shared ownership across threads and `Mutex` for exclusive mutable access:

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = Vec::new();

for _ in 0..4 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut value = counter.lock().unwrap();
        *value += 1;
    }));
}

for handle in handles {
    handle.join().unwrap();
}
```

`lock()` returns a `Result`, not the integer directly. The result can be an error if the mutex was poisoned by a panic while locked.

This line unwraps the result:

```rust
let mut value = counter.lock().unwrap();
```

The unwrapped value is a mutex guard. The guard acts like a pointer or reference to the protected `i32`, so this updates the inner value:

```rust
*value += 1;
```

The mutex is unlocked automatically when the guard is dropped, usually at the end of the closure block.

### Q154 - Generic bounds for compare and display

**Question:** For the mock `show_larger<T>` body using `if a > b` and `println!("{winner}")`, fix the generic signature and name the trait bounds needed for those two operations.

The `>` operator needs `PartialOrd`. Printing with normal braces `{}` needs `Display`.

```rust
use std::fmt::Display;

fn show_larger<T>(a: T, b: T)
where
    T: PartialOrd + Display,
{
    let winner = if a > b { a } else { b };
    println!("{winner}");
}
```

This equivalent shorter form is also valid:

```rust
fn show_larger<T: PartialOrd + Display>(a: T, b: T) {
    let winner = if a > b { a } else { b };
    println!("{winner}");
}
```

Without `PartialOrd`, Rust cannot know that `>` is valid for `T`. Without `Display`, Rust cannot know that `T` can be printed using `{}`.

### Q155 - Boxed recursive enum size

**Question:** For the mock enum `List { Cons(i32, List), Nil }`, replace the recursive field with `Box<List>` and explain why the boxed pointer gives the enum a known size.

This version is invalid:

```rust
enum List {
    Cons(i32, List),
    Nil,
}
```

`List` would contain another full `List`, which contains another full `List`, and so on. Rust cannot calculate a finite size for the type.

Use `Box<List>` for the recursive part:

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

`Box<List>` stores the next list node on the heap and keeps only a fixed-size pointer inside the enum variant. Because the pointer has a known size, Rust can calculate the size of `List`.

### Q156 - `strtol` validation checks

**Question:** In the mock `parse_positive` function after `strtol(text, &end, 10)`, write the checks that reject no digits, trailing junk, range errors, zero, and values too large for `int`.

The question is not just asking you to call `strtol`. It is asking you to prove that the whole input is a valid positive `int`.

```c
#include <errno.h>
#include <limits.h>
#include <stdlib.h>

int parse_positive(const char *text, int *out) {
    char *end = NULL;
    errno = 0;
    long value = strtol(text, &end, 10);

    if (end == text) {
        return 0;
    }
    if (*end != '\0') {
        return 0;
    }
    if (errno == ERANGE || value <= 0 || value > INT_MAX) {
        return 0;
    }

    *out = (int)value;
    return 1;
}
```

`end == text` means `strtol` did not consume any digits, so input like `"abc"` is rejected.

`*end != '\0'` means there was trailing junk after the number, so input like `"12abc"` is rejected.

`errno == ERANGE` catches range errors reported by `strtol`. The `value <= 0` check rejects zero and negative values. The `value > INT_MAX` check rejects a `long` value that was parsed successfully but cannot fit into an `int`.

### Q157 - Safe first-line file read

**Question:** In the mock `print_first_line` stub, complete the `fopen` failure path, the `fgets` failure handling, the successful print, and the `fclose` calls.

The stream must be checked before it is used. If opening fails, report the error and return.

```c
#include <errno.h>
#include <stdio.h>
#include <string.h>

int print_first_line(const char *path) {
    FILE *fp = fopen(path, "r");
    char line[80];

    if (fp == NULL) {
        fprintf(stderr, "cannot open %s: %s\n", path, strerror(errno));
        return 1;
    }

    if (fgets(line, sizeof line, fp) == NULL) {
        if (ferror(fp)) {
            fprintf(stderr, "read error: %s\n", strerror(errno));
        }
        fclose(fp);
        return 1;
    }

    printf("%s", line);
    fclose(fp);
    return 0;
}
```

The second `if` is needed because `fgets` returning `NULL` can mean end-of-file or a real read error. `ferror(fp)` distinguishes the real error case.

The file is closed on both paths after a successful `fopen`, because the program owns an open stream at that point.

### Q158 - `static` helper vs public header function

**Question:** For the mock `stack.c` declarations, make `make_node` private to the file and keep `push` callable from other files, then state which declaration belongs in `stack.h`.

In C, `static` at file level gives a function internal linkage. That means only this `.c` file can call it.

```c
/* stack.c */
static Node *make_node(char value);
Stack push(Stack stack, char value);
```

`make_node` is a helper, so it should stay in `stack.c` and be marked `static`.

`push` is part of the stack API, so its prototype belongs in the header:

```c
/* stack.h */
Stack push(Stack stack, char value);
```

C does not use `public` before functions. Public access in C is normally controlled by whether the declaration appears in a header and whether the definition is externally visible.

### Q159 - Remove first matching linked-list node

**Question:** Complete the mock `remove_first(Node **head, char key)` so it can remove the head or a later node, updates the caller's head pointer if needed, frees the removed node, and returns success or failure.

Because the function may need to change the caller's head pointer, it receives `Node **head`.

The clean solution is to keep a pointer to the pointer that leads to the current node:

```c
#include <stdlib.h>

typedef struct Node {
    char key;
    struct Node *next;
} Node;

int remove_first(Node **head, char key) {
    Node **link = head;

    while (*link != NULL) {
        Node *current = *link;

        if (current->key == key) {
            *link = current->next;
            free(current);
            return 1;
        }

        link = &current->next;
    }

    return 0;
}
```

At the start, `link` points at the caller's head pointer. Later, it points at a node's `next` field.

This one assignment removes either the head node or a later node:

```c
*link = current->next;
```

After unlinking the node, the removed node must be freed. If the loop finishes without finding the key, return `0`.

### Q160 - `fgetc` EOF vs read error

**Question:** After the mock `while ((ch = fgetc(fp)) != EOF)` loop, add the stream error check and explain why EOF alone cannot prove the loop ended cleanly.

`fgetc` returns `EOF` in two different cases:

```text
the stream reached end-of-file
a read error happened
```

So after the loop, check the stream:

```c
int ch;
long count = 0;

while ((ch = fgetc(fp)) != EOF) {
    count++;
}

if (ferror(fp)) {
    return -1;
}

return count;
```

If `ferror(fp)` is true, the loop ended because of a read error. If `ferror(fp)` is false, then the loop reached the end of the file cleanly.

### Q161 - C++ subscript operator returning a reference

**Question:** Complete `operator[]` so assignment through `grades[2]` changes the stored element. Include a simple bounds check.

The important part is the return type:

```cpp
int&
```

It must return a reference to the stored element, not a copy. If it returned `int`, then this would not update the array element:

```cpp
grades[2] = 99;
```

A direct answer matching the mock code is:

```cpp
#include <stdexcept>

class Grades {
    int data[4] = {0, 0, 0, 0};

public:
    int& operator[](unsigned int i) {
        if (i >= 4) {
            throw std::out_of_range("grade index");
        }
        return data[i];
    }
};
```

The valid indexes for `data[4]` are `0`, `1`, `2`, and `3`, so `i >= 4` must be rejected.

Using `int` is also acceptable if you check negative indexes:

```cpp
int& operator[](int i) {
    if (i < 0 || i >= 4) {
        throw std::out_of_range("grade index");
    }
    return data[i];
}
```

### Q162 - C++ output operator stream references

**Question:** Complete the output operator for `Date` so `std::cout << d` prints `day/month/year` and can still be chained with another output.

The stream is the left operand:

```cpp
std::cout << d
```

So `operator<<` is normally written as a non-member function that receives the stream as its first parameter.

```cpp
#include <iostream>

class Date {
    int day;
    int month;
    int year;

public:
    Date(int d, int m, int y) : day(d), month(m), year(y) {}
    friend std::ostream& operator<<(std::ostream& os, const Date& d);
};

std::ostream& operator<<(std::ostream& os, const Date& d) {
    os << d.day << "/" << d.month << "/" << d.year;
    return os;
}
```

The parameter:

```cpp
std::ostream& os
```

is the stream being written to.

The return type:

```cpp
std::ostream&
```

returns the same stream so output can be chained:

```cpp
std::cout << d << "\n";
```

The function is declared as a `friend` because `day`, `month`, and `year` are private.

### Q163 - Template member definitions with `Box<T>::`

**Question:** Write the out-of-class definitions for the `Box` template constructor and `get` method. Use the correct template headers and qualified names, and state where template definitions should normally live.

For each out-of-class template member definition, repeat the template header:

```cpp
template<typename T>
```

Then qualify the member with the instantiated class pattern:

```cpp
Box<T>::
```

Full answer:

```cpp
template<typename T>
class Box {
    T value;

public:
    Box(T value);
    T get() const;
};

template<typename T>
Box<T>::Box(T value) : value(value) {}

template<typename T>
T Box<T>::get() const {
    return value;
}
```

It is not enough to write:

```cpp
Box::get()
```

because `Box` by itself is the template name, not a concrete class type. The member belongs to `Box<T>`.

Template definitions normally live in the header because the compiler must see the full template body at the point where a specific type is used. For example, if another file writes:

```cpp
Box<int> b(5);
```

the compiler needs the constructor and `get` bodies so it can instantiate the `Box<int>` version.
