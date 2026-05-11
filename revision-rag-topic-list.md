# ECM2433 RAG Revision Tracker

Generated from `revision-rag-topic-list.pdf`.

Status key: `R` = red / cannot do it yet, `A` = amber / partly confident, `G` = green / exam-ready.

Topic sheet key: `Yes` = a focused sheet exists, `Related` = partly covered by a broader sheet, `No` = no topic sheet yet.

## C

| Status | Topic | Topic sheet created? |
|---|---|---|
| A | Basic C syntax and program layout: `main`, comments, `#include`, blocks, semicolons, `printf`, escape sequences, automatic variables, stack allocation, static typing, format specifiers. | Yes: [c-basic-syntax-program-layout-study-pack.pdf](topicsheets/c-basic-syntax-program-layout-study-pack.pdf) |
| R | Types and conversions: integer division, signed vs unsigned behaviour, promotion, casting, chars, floats, booleans, `typedef`, `size_t`, structs as data types, enums/unions. | Yes: [c-types-conversions-study-pack.pdf](topicsheets/c-types-conversions-study-pack.pdf) |
| A | Arrays and strings: 1D/2D arrays, contiguous memory, indexing, bounds errors, char arrays, null terminator, string formatting/printing, `<string.h>` functions. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf), [c-string-processing-study-pack.pdf](topicsheets/c-string-processing-study-pack.pdf) |
| A | Pointers and memory: addresses, dereferencing, arrays as pointers, arrays of strings, `malloc`, `free`, dangling pointers, double-free, memory leaks, segmentation faults. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Functions with pointers: pass by value vs pointer update, arrays as parameters, pointers to pointers, modifying caller state, allocating inside helper functions. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Function pointers and callbacks, including `qsort`. | Yes: [c-function-pointers-callbacks-study-pack.pdf](topicsheets/c-function-pointers-callbacks-study-pack.pdf) |
| R | Structures and dynamic data structures: `struct`, `typedef`, member access, linked lists, arrays vs linked lists tradeoffs. | Yes: [c-structures-dynamic-data-study-pack.pdf](topicsheets/c-structures-dynamic-data-study-pack.pdf) |
| R | Files and streams: `scanf`, standard streams, text vs binary streams, file modes, file I/O, buffering/flushing, `feof`, `ferror`, `fseek`, `rewind`, `errno`, `strerror`. | Yes: [c-files-streams-study-pack.pdf](topicsheets/c-files-streams-study-pack.pdf) |
| R | Stream buffering details beyond `fflush`: implementation-dependent buffer sizes, `setbuf`, and raw unbuffered `read`/`write`. | Yes: [c-builds-libraries-buffering-study-pack.pdf](topicsheets/c-builds-libraries-buffering-study-pack.pdf) |
| R | Preprocessor and macros: `#include`, macro expansion, stringification, search paths, macro pitfalls, precedence problems, safe macro design. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Program structure and compilation: separate compilation, headers, APIs, `extern`, `static`, scope/visibility, multiple includes, include guards, simple makefiles and dependencies. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Object files and libraries: reusing `.o` files separately from source, linking object files, and libraries as collections of object files. | Yes: [c-builds-libraries-buffering-study-pack.pdf](topicsheets/c-builds-libraries-buffering-study-pack.pdf) |
| R | Makefiles and dependency-based builds: targets, prerequisites/dependencies, tab-indented commands, object-file rules, default target, `clean` target, `make` up-to-date behaviour, and rebuilding when headers or source files change. | Yes: [c-builds-libraries-buffering-study-pack.pdf](topicsheets/c-builds-libraries-buffering-study-pack.pdf) |
| R | Macro precedence and fully parenthesised macros. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Macro vs function tradeoffs. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Macro stringification and predefined macros. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| A | Manual string duplication with `malloc`. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| A | Allocating 2D arrays with pointers. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Global vs `static` variables. | Yes: [c-preprocessor-macros-headers-study-pack.pdf](topicsheets/c-preprocessor-macros-headers-study-pack.pdf) |
| R | Output buffering and forcing `printf` output to appear immediately. | Yes: [c-files-streams-study-pack.pdf](topicsheets/c-files-streams-study-pack.pdf) |
| R | `errno` usage: only inspect it after an actual failure. | Yes: [c-files-streams-study-pack.pdf](topicsheets/c-files-streams-study-pack.pdf) |
| A | Control flow and early problem-solving patterns: `if`, `for`, `while`, factorial, numerical approximation of `e`, compile/link/run workflow. | Yes: [c-control-flow-problem-solving-study-pack.pdf](topicsheets/c-control-flow-problem-solving-study-pack.pdf) |
| R | Arrays and memory layout in practice: out-of-bounds access, undefined behaviour, segmentation faults, memory corruption. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf), [c-memory-debugging-tools-study-pack.pdf](topicsheets/c-memory-debugging-tools-study-pack.pdf) |
| G | `sizeof` vs `strlen`, and what each actually measures. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| G | Custom string routines: `mystrlen`, `string_copy`, pointer-based string functions. | Yes: [c-string-processing-study-pack.pdf](topicsheets/c-string-processing-study-pack.pdf) |
| A | Command-line arguments in C: `argc`, `argv`, quoting, `atoi`, `atof`. | Yes: [c-command-line-arguments-study-pack.pdf](topicsheets/c-command-line-arguments-study-pack.pdf) |
| A | Multi-dimensional arrays and array-based simulations, including Game of Life style evolution. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| G | Struct-based exercises: points/rectangles, area tests, inside/outside checks. | Yes: [c-struct-exercises-study-pack.pdf](topicsheets/c-struct-exercises-study-pack.pdf) |
| A | String-processing exercises: substitution/translation, palindrome detection, normalisation, `<ctype.h>` helpers such as `ispunct` and `tolower`. | Yes: [c-string-processing-study-pack.pdf](topicsheets/c-string-processing-study-pack.pdf) |
| R | Pointer exercises: basic pointers, pointers with arrays, tricky pointers, pointer arithmetic. | Yes: [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Generic low-level programming with `void *`: type-generic swap, comparison functions, generic merge sort. | Yes: [c-function-pointers-callbacks-study-pack.pdf](topicsheets/c-function-pointers-callbacks-study-pack.pdf), [c-pointers-memory-study-pack.pdf](topicsheets/c-pointers-memory-study-pack.pdf) |
| R | Debugging tools for memory bugs: Valgrind and address sanitiser. | Yes: [c-memory-debugging-tools-study-pack.pdf](topicsheets/c-memory-debugging-tools-study-pack.pdf) |
| A | Stack implementation practice using linked structures, `push`/`pop`, recursion for printing, and empty-stack edge cases. | Yes: [c-structures-dynamic-data-study-pack.pdf](topicsheets/c-structures-dynamic-data-study-pack.pdf) |

## C++

| Status | Topic | Topic sheet created? |
|---|---|---|
| R | Moving from C to C++: standards, compile/link flow, `iostream`, streams, `bool`, `std::string`, `using`, `auto`, scope resolution, function/operator overloading, default parameters, pass by reference. | Yes: [cpp-moving-from-c-study-pack.pdf](topicsheets/cpp-moving-from-c-study-pack.pdf) |
| R | C++ build systems at a high level: CMake as the large-project build tool mentioned in the slides, and how it relates to Makefiles/manual dependency management. | Yes: [cpp-build-stl-shared-ownership-study-pack.pdf](topicsheets/cpp-build-stl-shared-ownership-study-pack.pdf) |
| A | Classes and structs: declarations, struct vs class, access specifiers, constructors, destructors, parameterised/default/copy constructors, member functions, encapsulation, `this`. | Yes: [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| A | Memory, pointers, and references: `new`/`delete`, constructors/destructors, `nullptr`, references, pass-by-reference, `const &`, pointers to class members. | Yes: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf), [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| A | Inheritance: public/protected/private inheritance, base vs derived access, constructor/destructor order, interface design. | Yes: [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf), [cpp-multiple-inheritance-study-pack.pdf](topicsheets/cpp-multiple-inheritance-study-pack.pdf), [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| R | Operator overloading: overloadable vs non-overloadable operators, member vs friend functions, `[]`, `()`, `<<`, least-surprise design. | Yes: [cpp-operator-overloading-study-pack.pdf](topicsheets/cpp-operator-overloading-study-pack.pdf) |
| R | Templates and STL: macros vs templates, function templates, class templates, type safety, STL containers including `stack` and `vector`, iterators, `auto` with iterators. | Yes: [cpp-templates-stl-study-pack.pdf](topicsheets/cpp-templates-stl-study-pack.pdf) |
| R | STL algorithms and function objects: `binary_search`, sorting, counting algorithms, and passing functions/lambdas/function objects to algorithms. | Yes: [cpp-build-stl-shared-ownership-study-pack.pdf](topicsheets/cpp-build-stl-shared-ownership-study-pack.pdf) |
| A | Error handling and lambdas: `try`/`catch`/`throw`, standard exceptions, good exception practice, lambda syntax, capture by value/reference. | Yes: [cpp-error-handling-lambdas-study-pack.pdf](topicsheets/cpp-error-handling-lambdas-study-pack.pdf) |
| A | Access control details in inheritance: `private`, `protected`, `public`. | Yes: [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf), [cpp-multiple-inheritance-study-pack.pdf](topicsheets/cpp-multiple-inheritance-study-pack.pdf) |
| A | Why derived classes can access `protected` members but not `private` members. | Yes: [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| G | Getter/setter style access when direct member access is restricted. | Yes: [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| R | RAII vs manual `malloc`/`free`. | Yes: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf), [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| R | Smart-pointer ownership models in C++ vs Rust ownership/reference-counting. | Yes: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf), [rust-ownership-closures-lifetimes-study-pack.pdf](topicsheets/rust-ownership-closures-lifetimes-study-pack.pdf), [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| R | C++ shared ownership smart pointers: `std::shared_ptr`, `std::weak_ptr`, reference counts, copyable shared ownership, and when the managed object is destroyed. | Yes: [cpp-build-stl-shared-ownership-study-pack.pdf](topicsheets/cpp-build-stl-shared-ownership-study-pack.pdf) |
| G | Splitting classes across header and source files. | Yes: [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| R | Reference parameters in practice, such as swapping values by reference. | Yes: [cpp-moving-from-c-study-pack.pdf](topicsheets/cpp-moving-from-c-study-pack.pdf), [cpp-templates-stl-study-pack.pdf](topicsheets/cpp-templates-stl-study-pack.pdf) |
| R | Constructor/destructor tracing to understand object lifetime. | Yes: [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| R | Virtual functions and dynamic binding through base-class pointers. | Yes: [cpp-virtual-functions-dynamic-binding-study-pack.pdf](topicsheets/cpp-virtual-functions-dynamic-binding-study-pack.pdf) |
| R | Member initialiser lists for constructors. | Yes: [cpp-classes-access-headers-study-pack.pdf](topicsheets/cpp-classes-access-headers-study-pack.pdf) |
| A | Multiple inheritance. | Yes: [cpp-multiple-inheritance-study-pack.pdf](topicsheets/cpp-multiple-inheritance-study-pack.pdf) |
| R | Smart-pointer practice with `std::unique_ptr`. | Yes: [cpp-smart-pointers-unique-ptr-study-pack.pdf](topicsheets/cpp-smart-pointers-unique-ptr-study-pack.pdf) |

## Rust

| Status | Topic | Topic sheet created? |
|---|---|---|
| A | Tooling and motivation: why Rust, memory-safety goals, `rustc`, `cargo` as build system and package manager, `Cargo.toml`, Rust Book/docs, and `rust-analyzer` editor support. | Yes: [rust-tooling-cargo-study-pack.pdf](topicsheets/rust-tooling-cargo-study-pack.pdf), [rust-control-flow-sorting-tooling-study-pack.pdf](topicsheets/rust-control-flow-sorting-tooling-study-pack.pdf) |
| R | Crash-course basics: `let`, `mut`, shadowing, `const`, integer types, tuples, arrays, runtime bounds checks, printing. | Yes: [rust-crash-course-basics-study-pack.pdf](topicsheets/rust-crash-course-basics-study-pack.pdf) |
| R | Rust functions and control flow: function parameters/return types, unit type `()`, `if` expressions, `loop`/`while`/`for`, loop labels, `break` values, `break`/`continue`, and doc comments `///`. | Yes: [rust-control-flow-sorting-tooling-study-pack.pdf](topicsheets/rust-control-flow-sorting-tooling-study-pack.pdf) |
| R | Ownership fundamentals: stack vs heap, `String`, moves, copies, drop, ownership rules, references and borrowing, mutable borrowing, dangling references. | Yes: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| R | Borrowing and slices: references, `&[T]`, `&str`, `String` vs `&str`, avoiding dangling references. | Yes: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf) |
| R | Collections and data modelling: `Vec<T>`, strings, structs, methods, associated functions, enums, `Option<T>`, `match`, `if let`. | Yes: [rust-collections-data-modelling-study-pack.pdf](topicsheets/rust-collections-data-modelling-study-pack.pdf) |
| R | Error handling and file I/O: `panic!`, `Result<T, E>`, explicit error handling, `?`, parsing, file reading, iterating over lines. | Yes: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| A | Project structure, testing, and `HashMap`: `main.rs` vs `lib.rs`, `pub`, modules, unit tests, integration tests, assertions, `HashMap`, `entry` API. | Yes: [rust-practical-projects-data-study-pack.pdf](topicsheets/rust-practical-projects-data-study-pack.pdf) |
| R | Generics and traits: generic functions/structs/methods, trait bounds, `where` clauses, default trait methods, derivable traits. | Yes: [rust-generics-traits-study-pack.pdf](topicsheets/rust-generics-traits-study-pack.pdf) |
| R | Closures, iterators, and lifetimes: closure syntax/capture, `Fn`/`FnMut`/`FnOnce`, iterator pipelines, `map`, `filter`, `enumerate`, `zip`, `take`, `collect`, custom iterators, lifetime annotations, elision rules. | Yes: [rust-ownership-closures-lifetimes-study-pack.pdf](topicsheets/rust-ownership-closures-lifetimes-study-pack.pdf), [rust-custom-iterators-pipelines-study-pack.pdf](topicsheets/rust-custom-iterators-pipelines-study-pack.pdf) |
| R | Rust move vs copy, and why iterator-based loops avoid C indexing errors. | Yes: [rust-ownership-borrowing-study-pack.pdf](topicsheets/rust-ownership-borrowing-study-pack.pdf), [rust-custom-iterators-pipelines-study-pack.pdf](topicsheets/rust-custom-iterators-pipelines-study-pack.pdf) |
| R | Rust `?` as explicit error propagation without exceptions. | Yes: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| A | Cargo workflow beyond `build`/`run`: `cargo check`, `cargo fmt`, `cargo clippy`, tests. | Yes: [rust-tooling-cargo-study-pack.pdf](topicsheets/rust-tooling-cargo-study-pack.pdf) |
| G | Expressions vs statements, and how semicolons affect return values. | Yes: [rust-expressions-statements-study-pack.pdf](topicsheets/rust-expressions-statements-study-pack.pdf) |
| R | Command-line input, parsing, and comparing `expect`, `match`, and `?`. | Yes: [rust-practical-projects-data-study-pack.pdf](topicsheets/rust-practical-projects-data-study-pack.pdf), [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| R | Array/slice processing, threshold-style scans, and tuple destructuring. | Yes: [rust-practical-projects-data-study-pack.pdf](topicsheets/rust-practical-projects-data-study-pack.pdf) |
| R | `Option`, `Some`/`None`, `match`, and `if let` in small data-structure exercises. | Yes: [rust-collections-data-modelling-study-pack.pdf](topicsheets/rust-collections-data-modelling-study-pack.pdf) |
| A | Unit tests, integration tests, assertion patterns, and float comparisons with tolerances. | Yes: [rust-practical-projects-data-study-pack.pdf](topicsheets/rust-practical-projects-data-study-pack.pdf) |
| R | File parsing exercises, including CSV-style parsing into structs and `Box<dyn Error>` return types. | Yes: [rust-error-handling-file-io-study-pack.pdf](topicsheets/rust-error-handling-file-io-study-pack.pdf) |
| R | Custom iterators and more involved iterator pipelines over `HashMap`/`Vec`. | Yes: [rust-custom-iterators-pipelines-study-pack.pdf](topicsheets/rust-custom-iterators-pipelines-study-pack.pdf) |
| R | Sorting practical Rust data: `sort_by`, descending order, tie handling, `partial_cmp` for floating-point values, and `Ordering`. | Yes: [rust-control-flow-sorting-tooling-study-pack.pdf](topicsheets/rust-control-flow-sorting-tooling-study-pack.pdf) |
| A | Smart pointers beyond the lecture slides: `Box<T>` and `Rc<T>`. | Yes: [rust-ownership-closures-lifetimes-study-pack.pdf](topicsheets/rust-ownership-closures-lifetimes-study-pack.pdf) |
| R | Concurrency topics: spawned threads, `move` closures, joining, `mpsc` channels, `Arc<T>`, `Mutex<T>`, poisoned mutex handling, parallel aggregation. | Yes: [rust-concurrency-parallelism-study-pack.pdf](topicsheets/rust-concurrency-parallelism-study-pack.pdf) |
