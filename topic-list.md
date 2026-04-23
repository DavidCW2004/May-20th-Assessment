# ECM2433 Topic List

Checked against `slides/`, `worksheet/`, and the exam PDF, so brief slide mentions, explicit exam themes, and worksheet-driven practice topics are included.

## C

- Basic C syntax and program layout: `main`, comments, `#include`, blocks, semicolons, `printf`, escape sequences, automatic variables, stack allocation, static typing, format specifiers.
- Types and conversions: integer division, signed vs unsigned behaviour, promotion, casting, chars, floats, booleans, `typedef`, `size_t`, structs as data types, brief mention of enums/unions.
- Arrays and strings: 1D/2D arrays, contiguous memory, indexing, bounds errors, arrays of chars, null terminator, string formatting and printing, common string functions from `<string.h>`.
- Pointers and memory: addresses, dereferencing, arrays as pointers, arrays of strings, dynamic allocation with `malloc`, freeing with `free`, dangling pointers, double-free, memory leaks, segmentation faults.
- Functions with pointers: pass by value vs pointer-based update, arrays as function parameters, pointers to pointers, modifying caller state, allocating inside helper functions.
- Function pointers and callbacks, including `qsort`.
- Structures and dynamic data structures: `struct`, `typedef`, member access, linked lists, arrays vs linked lists tradeoffs.
- Files and streams: console input with `scanf`, standard streams, text vs binary streams, file open modes, file I/O, buffering and flushing, `feof`, `ferror`, `fseek`, `rewind`, `errno`, `strerror`, error checking.
- Preprocessor and macros: `#include`, macro expansion, stringification, search paths, macro pitfalls, precedence problems, safe macro design.
- Program structure and compilation: separate compilation, headers, APIs, `extern`, `static` for private functions, scope/visibility, multiple includes, include guards, simple makefiles and dependencies.

## C++

- Moving from C to C++: history, standards, compile/link flow, `iostream`, standard streams, `bool`, `std::string`, `using`, `auto`, scope resolution, function overloading, operator overloading, default parameter values, pass by reference.
- Classes and structs: class declarations, struct vs class, access specifiers, constructors, destructors, parameterised/default/copy constructors, member functions, encapsulation, `this`.
- Memory, pointers, and references: `new`/`delete`, constructors/destructors, `nullptr`, references, pass-by-reference, `const &`, pointers to class members.
- Inheritance: public/protected/private inheritance, base vs derived access, constructor/destructor order, interface design.
- Operator overloading: why use it, overloadable vs non-overloadable operators, member vs friend functions, `[]`, `()`, `<<`, and least-surprise design.
- Templates and STL: macros vs templates, function templates, class templates, type safety, STL containers including `stack` and `vector`, iterators, `auto` with iterators.
- Error handling and lambdas: `try`/`catch`/`throw`, standard exceptions, good exception practice, lambda syntax, capture by value/reference.

## Rust

- Tooling and motivation: why Rust, memory-safety goals, `rustc`, `cargo`, Rust Book/docs.
- Crash-course basics: `let`, `mut`, shadowing, `const`, integer types, tuples, arrays, runtime bounds checks, printing.
- Ownership fundamentals: stack vs heap, `String`, moves, copies, drop, the three ownership rules, references and borrowing, mutable borrowing, dangling references.
- Borrowing and slices: references, `&[T]`, `&str`, `String` vs `&str`, avoiding dangling references.
- Collections and data modelling: `Vec<T>`, strings, structs, methods, associated functions, enums, `Option<T>`, `match`, `if let`.
- Error handling and file I/O: `panic!`, `Result<T, E>`, explicit error handling, `?` for propagation, parsing, file reading, iterating over lines.
- Project structure, testing, and `HashMap`: `main.rs` vs `lib.rs`, `pub`, modules, unit tests, integration tests, assertions, `HashMap` basics, `entry` API.
- Generics and traits: generic functions/structs/methods, trait bounds, `where` clauses, default trait methods, derivable traits.
- Closures, iterators, and lifetimes: closure syntax/capture, `Fn`/`FnMut`/`FnOnce`, iterator pipelines, `map`, `filter`, `enumerate`, `zip`, `take`, `collect`, custom iterators, lifetime annotations, elision rules, lifetimes with generics, borrow-checker reasoning.

## Easy-To-Miss But Examable

- Macro precedence and fully parenthesised macros.
- Macro vs function tradeoffs.
- Macro stringification and predefined macros.
- Manual string duplication with `malloc`.
- Allocating 2D arrays with pointers.
- Global vs `static` variables.
- Output buffering and forcing `printf` output to appear immediately.
- `errno` usage: only inspect it after an actual failure, not after a successful call.
- Access control details in inheritance: `private`, `protected`, `public`.
- Why derived classes can access `protected` members but not `private` members.
- Getter/setter style access when direct member access is restricted.
- RAII vs manual `malloc`/`free`.
- Smart-pointer ownership models in C++ vs Rust ownership/reference-counting.
- Rust move vs copy, and why iterator-based loops avoid C indexing errors.
- Rust `?` as explicit error propagation without exceptions.

## Worksheet-Driven Additions

These showed up clearly in the worksheets and are worth revising even when they are only mentioned briefly in the slides.

### C

- Control flow and early problem-solving patterns: `if`, `for`, `while`, factorial, numerical approximation of `e`, compile/link/run workflow.
- Arrays and memory layout in practice: out-of-bounds access, undefined behaviour, segmentation faults, memory corruption.
- `sizeof` vs `strlen`, and what each actually measures.
- Custom string routines: `mystrlen`, `string_copy`, pointer-based versions of string functions.
- Command-line arguments in C: `argc`, `argv`, quoting, `atoi`, `atof`.
- Multi-dimensional arrays and array-based simulations, including Game of Life style evolution.
- Struct-based exercises: points/rectangles, area tests, inside/outside checks.
- String-processing exercises: substitution/translation, palindrome detection, normalisation, `<ctype.h>` helpers such as `ispunct` and `tolower`.
- Pointer exercises: basic pointers, pointers with arrays, tricky pointers, pointer arithmetic.
- Generic low-level programming with `void *`: type-generic swap, comparison functions, generic merge sort.
- Debugging tools for memory bugs: Valgrind and address sanitiser.
- Stack implementation practice using linked structures, `push`/`pop`, recursion for printing, and checking empty-stack edge cases.

### C++

- Splitting classes across header and source files.
- Reference parameters in practice, such as swapping values by reference.
- Constructor/destructor tracing to understand object lifetime.
- Virtual functions and dynamic binding through base-class pointers.
- Member initialiser lists for constructors.
- Multiple inheritance.
- Smart-pointer practice with `std::unique_ptr`.

### Rust

- Cargo workflow beyond `build`/`run`: `cargo check`, `cargo fmt`, `cargo clippy`, tests.
- Expressions vs statements, and how semicolons affect return values.
- Command-line input, parsing, and comparing `expect`, `match`, and `?`.
- Array/slice processing, threshold-style scans, and tuple destructuring.
- `Option`, `Some`/`None`, `match`, and `if let` in small data-structure exercises.
- Unit tests, integration tests, assertion patterns, and float comparisons with tolerances.
- File parsing exercises, including CSV-style parsing into structs and `Box<dyn Error>` return types.
- Custom iterators and more involved iterator pipelines over `HashMap`/`Vec`.
- Smart pointers beyond the lecture slides: `Box<T>` and `Rc<T>`.
- Concurrency topics from the later worksheets: spawned threads, `move` closures, joining, `mpsc` channels, `Arc<T>`, `Mutex<T>`, poisoned mutex handling, and parallel aggregation patterns.
- Applied parallel exercises such as Caesar cipher, league tables, word frequencies, Monte Carlo estimation, and bigram text models.
