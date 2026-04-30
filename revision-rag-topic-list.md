# ECM2433 RAG Revision Tracker

Generated from `revision-rag-topic-list.pdf`.

Status key: `R` = red / cannot do it yet, `A` = amber / partly confident, `G` = green / exam-ready.

Topic sheet key: `Yes` = a focused sheet exists, `Related` = partly covered by a broader sheet, `No` = no topic sheet yet.

## C

| Status | Topic | Topic sheet created? |
|---|---|---|
| A | Basic C syntax and program layout: `main`, comments, `#include`, blocks, semicolons, `printf`, escape sequences, automatic variables, stack allocation, static typing, format specifiers. | No |
| R | Types and conversions: integer division, signed vs unsigned behaviour, promotion, casting, chars, floats, booleans, `typedef`, `size_t`, structs as data types, enums/unions. | Yes: [c-types-conversions-study-pack.pdf](topicsheets/c-types-conversions-study-pack.pdf) |
| A | Arrays and strings: 1D/2D arrays, contiguous memory, indexing, bounds errors, char arrays, null terminator, string formatting/printing, `<string.h>` functions. | Related: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| A | Pointers and memory: addresses, dereferencing, arrays as pointers, arrays of strings, `malloc`, `free`, dangling pointers, double-free, memory leaks, segmentation faults. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Functions with pointers: pass by value vs pointer update, arrays as parameters, pointers to pointers, modifying caller state, allocating inside helper functions. | Related: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Function pointers and callbacks, including `qsort`. | Yes: [c-function-pointers-callbacks-study-pack.pdf](topicsheets/c-function-pointers-callbacks-study-pack.pdf) |
| R | Structures and dynamic data structures: `struct`, `typedef`, member access, linked lists, arrays vs linked lists tradeoffs. | Yes: [c-structures-dynamic-data-study-pack.pdf](topicsheets/c-structures-dynamic-data-study-pack.pdf) |
| R | Files and streams: `scanf`, standard streams, text vs binary streams, file modes, file I/O, buffering/flushing, `feof`, `ferror`, `fseek`, `rewind`, `errno`, `strerror`. | Yes: [c-files-streams-study-pack.pdf](topicsheets/c-files-streams-study-pack.pdf) |
| R | Preprocessor and macros: `#include`, macro expansion, stringification, search paths, macro pitfalls, precedence problems, safe macro design. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Program structure and compilation: separate compilation, headers, APIs, `extern`, `static`, scope/visibility, multiple includes, include guards, simple makefiles and dependencies. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Macro precedence and fully parenthesised macros. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Macro vs function tradeoffs. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Macro stringification and predefined macros. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| A | Manual string duplication with `malloc`. | Related: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| A | Allocating 2D arrays with pointers. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Global vs `static` variables. | Related: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Output buffering and forcing `printf` output to appear immediately. | Yes: [c-files-streams-study-pack.pdf](topicsheets/c-files-streams-study-pack.pdf) |
| R | `errno` usage: only inspect it after an actual failure. | Related: [c-files-streams-study-pack.pdf](topicsheets/c-files-streams-study-pack.pdf) |
| A | Control flow and early problem-solving patterns: `if`, `for`, `while`, factorial, numerical approximation of `e`, compile/link/run workflow. | No |
| R | Arrays and memory layout in practice: out-of-bounds access, undefined behaviour, segmentation faults, memory corruption. | Related: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| G | `sizeof` vs `strlen`, and what each actually measures. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| G | Custom string routines: `mystrlen`, `string_copy`, pointer-based string functions. | Related: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| A | Command-line arguments in C: `argc`, `argv`, quoting, `atoi`, `atof`. | Yes: [c-command-line-arguments-study-pack.pdf](topicsheets/c-command-line-arguments-study-pack.pdf) |
| A | Multi-dimensional arrays and array-based simulations, including Game of Life style evolution. | Related: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| G | Struct-based exercises: points/rectangles, area tests, inside/outside checks. | No |
| A | String-processing exercises: substitution/translation, palindrome detection, normalisation, `<ctype.h>` helpers such as `ispunct` and `tolower`. | No |
| R | Pointer exercises: basic pointers, pointers with arrays, tricky pointers, pointer arithmetic. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Generic low-level programming with `void *`: type-generic swap, comparison functions, generic merge sort. | Related: [c-function-pointers-callbacks-study-pack.pdf](topicsheets/c-function-pointers-callbacks-study-pack.pdf) |
| R | Debugging tools for memory bugs: Valgrind and address sanitiser. | No |
| A | Stack implementation practice using linked structures, `push`/`pop`, recursion for printing, and empty-stack edge cases. | Related: [c-structures-dynamic-data-study-pack.pdf](topicsheets/c-structures-dynamic-data-study-pack.pdf) |

## C++

| Status | Topic | Topic sheet created? |
|---|---|---|
| R | Moving from C to C++: standards, compile/link flow, `iostream`, streams, `bool`, `std::string`, `using`, `auto`, scope resolution, function/operator overloading, default parameters, pass by reference. | Yes: [cpp-moving-from-c-study-pack.pdf](topicsheets/cpp-moving-from-c-study-pack.pdf) |
| A | Classes and structs: declarations, struct vs class, access specifiers, constructors, destructors, parameterised/default/copy constructors, member functions, encapsulation, `this`. | Related: [cpp-operator-overloading-study-pack.pdf](topicsheets/cpp-operator-overloading-study-pack.pdf), [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf) |
| A | Memory, pointers, and references: `new`/`delete`, constructors/destructors, `nullptr`, references, pass-by-reference, `const &`, pointers to class members. | Related: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf) |
| A | Inheritance: public/protected/private inheritance, base vs derived access, constructor/destructor order, interface design. | Related: [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf) |
| R | Operator overloading: overloadable vs non-overloadable operators, member vs friend functions, `[]`, `()`, `<<`, least-surprise design. | Yes: [cpp-operator-overloading-study-pack.pdf](topicsheets/cpp-operator-overloading-study-pack.pdf) |
| R | Templates and STL: macros vs templates, function templates, class templates, type safety, STL containers including `stack` and `vector`, iterators, `auto` with iterators. | Yes: [cpp-templates-stl-study-pack.pdf](topicsheets/cpp-templates-stl-study-pack.pdf) |
| A | Error handling and lambdas: `try`/`catch`/`throw`, standard exceptions, good exception practice, lambda syntax, capture by value/reference. | No |
| A | Access control details in inheritance: `private`, `protected`, `public`. | Related: [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf) |
| A | Why derived classes can access `protected` members but not `private` members. | No |
| G | Getter/setter style access when direct member access is restricted. | No |
| R | RAII vs manual `malloc`/`free`. | Related: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf) |
| R | Smart-pointer ownership models in C++ vs Rust ownership/reference-counting. | Related: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf), [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| G | Splitting classes across header and source files. | No |
| R | Reference parameters in practice, such as swapping values by reference. | Related: [cpp-templates-stl-study-pack.pdf](topicsheets/cpp-templates-stl-study-pack.pdf) |
| R | Constructor/destructor tracing to understand object lifetime. | Related: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf), [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf) |
| R | Virtual functions and dynamic binding through base-class pointers. | Yes: [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf) |
| R | Member initialiser lists for constructors. | Related: [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf) |
| A | Multiple inheritance. | No |
| R | Smart-pointer practice with `std::unique_ptr`. | Yes: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf) |

## Rust

| Status | Topic | Topic sheet created? |
|---|---|---|
| A | Tooling and motivation: why Rust, memory-safety goals, `rustc`, `cargo`, Rust Book/docs. | No |
| R | Crash-course basics: `let`, `mut`, shadowing, `const`, integer types, tuples, arrays, runtime bounds checks, printing. | No |
| R | Ownership fundamentals: stack vs heap, `String`, moves, copies, drop, ownership rules, references and borrowing, mutable borrowing, dangling references. | Yes: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| R | Borrowing and slices: references, `&[T]`, `&str`, `String` vs `&str`, avoiding dangling references. | Yes: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| R | Collections and data modelling: `Vec<T>`, strings, structs, methods, associated functions, enums, `Option<T>`, `match`, `if let`. | Yes: [rust-collections-data-modelling-study-pack.pdf](topicsheets/rust-collections-data-modelling-study-pack.pdf) |
| R | Error handling and file I/O: `panic!`, `Result<T, E>`, explicit error handling, `?`, parsing, file reading, iterating over lines. | Yes: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| A | Project structure, testing, and `HashMap`: `main.rs` vs `lib.rs`, `pub`, modules, unit tests, integration tests, assertions, `HashMap`, `entry` API. | Related: [rust-generics-traits-study-pack.pdf](topicsheets/rust-generics-traits-study-pack.pdf), [rust-collections-data-modelling-study-pack.pdf](topicsheets/rust-collections-data-modelling-study-pack.pdf) |
| R | Generics and traits: generic functions/structs/methods, trait bounds, `where` clauses, default trait methods, derivable traits. | Yes: [rust-generics-traits-study-pack.pdf](topicsheets/rust-generics-traits-study-pack.pdf) |
| R | Closures, iterators, and lifetimes: closure syntax/capture, `Fn`/`FnMut`/`FnOnce`, iterator pipelines, `map`, `filter`, `enumerate`, `zip`, `take`, `collect`, custom iterators, lifetime annotations, elision rules. | Related: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| R | Rust move vs copy, and why iterator-based loops avoid C indexing errors. | Related: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| R | Rust `?` as explicit error propagation without exceptions. | Yes: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| A | Cargo workflow beyond `build`/`run`: `cargo check`, `cargo fmt`, `cargo clippy`, tests. | No |
| G | Expressions vs statements, and how semicolons affect return values. | No |
| R | Command-line input, parsing, and comparing `expect`, `match`, and `?`. | Related: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| R | Array/slice processing, threshold-style scans, and tuple destructuring. | Related: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf), [rust-collections-data-modelling-study-pack.pdf](topicsheets/rust-collections-data-modelling-study-pack.pdf) |
| R | `Option`, `Some`/`None`, `match`, and `if let` in small data-structure exercises. | Yes: [rust-collections-data-modelling-study-pack.pdf](topicsheets/rust-collections-data-modelling-study-pack.pdf) |
| A | Unit tests, integration tests, assertion patterns, and float comparisons with tolerances. | Related: [rust-generics-traits-study-pack.pdf](topicsheets/rust-generics-traits-study-pack.pdf) |
| R | File parsing exercises, including CSV-style parsing into structs and `Box<dyn Error>` return types. | Yes: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| R | Custom iterators and more involved iterator pipelines over `HashMap`/`Vec`. | No |
| A | Smart pointers beyond the lecture slides: `Box<T>` and `Rc<T>`. | Related: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| R | Concurrency topics: spawned threads, `move` closures, joining, `mpsc` channels, `Arc<T>`, `Mutex<T>`, poisoned mutex handling, parallel aggregation. | Yes: [rust-concurrency-parallelism-study-pack.pdf](topicsheets/rust-concurrency-parallelism-study-pack.pdf) |
| A | Applied parallel exercises: Caesar cipher, league tables, word frequencies, Monte Carlo estimation, and bigram text models. | No |
