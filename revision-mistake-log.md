# Revision Mistake Log

Use this table for any topic sheet where an answer was not 100%. The `Topic sheet` column keeps repeated question numbers separate.

| Topic sheet | Question | Topic | My mistake | Correct rule | Redo prompt |
| --- | --- | --- | --- | --- | --- |
| C Pointers and Memory | 1 | Pointer basics | I did not realise that `x` is the integer value itself. | In `int x = 4; int *p = &x;`, `x` is the stored integer value, `&x` is its address, `p` stores that address, `*p` is the value at that address, and `&p` is the address of the pointer variable. | Explain `x`, `&x`, `p`, `*p`, and `&p` for `int x = 4; int *p = &x;`. |
| C Pointers and Memory | 5 | `sizeof` vs `strlen` | I said the length was 5 but did not explain that `strlen` stops at the null terminator. | `strlen(s)` counts characters until it reaches `'\0'`, not including the null terminator. `sizeof(s)` gives the bytes reserved for the array itself. | For `char s[20] = "Hello";`, explain why `strlen(s)` is 5 and `sizeof(s)` is 20. |
| C Pointers and Memory | 6 | Out-of-bounds access | I did not mention that out-of-bounds writes can corrupt nearby data, change another variable, or cause a segmentation fault. | Writing outside an array is undefined behaviour. It might appear to work, corrupt memory, change another variable, or crash with a segmentation fault. | Explain why `array[15] = 999;` is unsafe when `array` has 10 elements. |
| C Pointers and Memory | 7 | `malloc` safety check | I forgot to add the `if (a != NULL)` / `if (a == NULL)` check after `malloc`. | `malloc` can fail and return `NULL`. Check the pointer before writing through it. Only use the array if allocation succeeded, then `free` it afterwards. | Write code that allocates `n` integers, checks for failure, fills them with `1` to `n`, prints them, and frees the memory. |
| C Pointers and Memory | 8 | `strcpy` into `char *` | I did not get the safe fix correct and did not mention that `p` was uninitialised. | `char *p;` is an uninitialised pointer. `strcpy(p, "Hello")` is unsafe because `p` does not point to valid writable memory. Fix with `char p[6];` or with `malloc(6)`, a `NULL` check, `strcpy`, and `free`. | Explain the bug in `char *p; strcpy(p, "Hello");` and give two safe fixes. |
| C Pointers and Memory | 9 | Dynamic 2D array | I got the 2D dynamic array allocation and freeing completely wrong. | For `R` rows and `C` columns: declare `int **X`, allocate the row pointer array with `malloc(R * sizeof *X)`, allocate each row with `malloc(C * sizeof *X[r])`, then free each row before freeing `X`. | Write the full allocation and free pattern for `int **X` with `R` rows and `C` columns. |
| Rust Ownership and Borrowing | 1 | Ownership rules | I forgot that a value can only have one owner. | Rust ownership has three rules: each value has an owner, there can only be one owner at a time, and when the owner goes out of scope the value is dropped. | Write the three Rust ownership rules and explain why the one-owner rule matters. |
| Rust Ownership and Borrowing | 2 | Move semantics | I forgot to mention that Rust prevents use-after-move. | When ownership of a non-`Copy` value such as `String` moves, the old variable becomes invalid. Rust rejects later use of that variable to prevent use-after-move bugs. | Explain why `let s2 = s1; println!("{s1}");` fails when `s1` is a `String`. |
| Rust Ownership and Borrowing | 5 | `&str` parameters and iteration | I used `char in text` instead of `text.chars()`, and I forgot to mention that `&str` reads text but can accept references and literals. | Iterate over text with `text.chars()`. Use `&str` for read-only text parameters because it borrows text and works with both `String` references and string literals. | Write `fn count_vowels(text: &str) -> usize`, using `text.chars()`, and explain why `&str` is the right parameter type. |
| Rust Ownership and Borrowing | 7 | Modifying a `String` | I used `+=` instead of `push`. | To add one `char` to a `String`, use `text.push('a')`. `+=` expects a string slice such as `"a"`, not a `char`. | Write a function that appends `!` to a `String` through `&mut String`. |
| Rust Ownership and Borrowing | 8 | `String` vs `&str` | I did not mention that a `String` owns heap-allocated text and that `&str` is a borrowed slice with no ownership. | `String` owns a block of heap memory containing text. `&str` is a borrowed string slice: pointer plus length, with no ownership. | Explain the difference between `String` and `&str`, including ownership and heap memory. |

## Priority Redo Order

1. Rust Ownership and Borrowing question 8: `String` vs `&str`.
2. Rust Ownership and Borrowing question 5: `&str` parameters and `text.chars()`.
3. Rust Ownership and Borrowing question 1: ownership rules.
4. C Pointers and Memory question 9: dynamic 2D array.
5. C Pointers and Memory question 8: `strcpy` into an uninitialised `char *`.
6. C Pointers and Memory question 7: `malloc` with `NULL` check.

