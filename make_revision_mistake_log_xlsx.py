from __future__ import annotations

import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "revision-mistake-log.xlsx"

TRACKER_COLUMNS = ["Topic sheet", "Question number", "Topic", "Redo prompt", "Completed"]
TRACKER_ROWS = [
    ["C Pointers and Memory", "1", "Pointer basics", "Given `int x = 4; int *p` pointing at `x`; then `*p += 3; int y = *p;`, work out `x` and `y`, then identify which expression is the address.", ""],
    ["C Pointers and Memory", "2", "`sizeof` vs `strlen`", "For `char s[20] = \"Hello\";`, work out how many more visible characters can be appended safely, leaving room for `\\0`.", "Yes"],
    ["C Pointers and Memory", "3", "Out-of-bounds access", "Find the bug in `int a[5]; for (int i = 0; i <= 5; i++) a[i] = 0;`, fix the loop condition, and give one likely symptom.", "Yes"],
    ["C Pointers and Memory", "4", "`malloc` safety check", "Complete the missing failure path after `int *a = malloc(n * sizeof *a);` before a loop writes to `a[i]`.", "Yes"],
    ["C Pointers and Memory", "5", "`strcpy` into `char *`", "Rewrite `char *p; strcpy(p, \"Hello\");` in one safe way, and make clear where the writable storage comes from.", "Yes"],
    ["C Pointers and Memory", "6", "Dynamic 2D array", "If row `r` fails while allocating `int **X`, write the cleanup for rows `0` to `r - 1` and then `X` itself.", "Yes"],
    ["Rust Ownership and Borrowing", "7", "Ownership rules", "For `let s1 = String::from(\"hi\"); let s2 = s1; println!(\"{s1} {s2}\");`, explain the compiler error and give one fix.", "Yes"],
    ["Rust Ownership and Borrowing", "8", "Move semantics", "Fix `fn takes(s: String) {}` followed by `takes(name); println!(\"{name}\");` so `name` can still be printed.", ""],
    ["Rust Ownership and Borrowing", "9", "Borrowed string-slice parameters and iteration", "Write a `count_a` function that borrows a string slice and returns `usize`, so it counts `a` characters using the right string iteration method.", ""],
    ["Rust Ownership and Borrowing", "10", "Modifying a `String`", "Starting from `let mut text = String::from(\"Hi\");`, write the two lines that produce `Hi! there`.", "Yes"],
    ["Rust Ownership and Borrowing", "11", "`String` vs borrowed string slices", "Choose a function parameter type for read-only text that accepts both string literals and `String` values, then show both calls.", "Yes"],
    ["C Files and Streams", "12", "Text vs binary streams", "You are checking exact file bytes for a checksum. Choose the `fopen` mode and explain what text mode could change.", ""],
    ["C Files and Streams", "13", "`scanf` basics", "For `int k = 99; int rc = scanf(\"%d\", address of k);`, handle the case where the user types `abc` instead of a number.", ""],
    ["C Files and Streams", "14", "Buffering and flushing", "A long task starts after `printf(\"Working...\");` but nothing appears yet. Add the missing call and explain why it belongs there.", ""],
    ["C Files and Streams", "15", "`ferror` vs `feof`", "After a `while ((ch = fgetc(fp)) != EOF)` loop ends, write the check that distinguishes a read error from clean EOF.", ""],
    ["C Files and Streams", "16", "`rewind` and `fseek`", "After reading some bytes, reset to the start and then jump to byte offset 20. Write the two calls in order.", ""],
    ["C Files and Streams", "17", "Open / write / flush / close", "Write a safe `out.txt` write fragment that does not call `fprintf` if `fopen` fails, and still closes the file.", ""],
    ["C Preprocessor, Macros, and Headers", "2", "`#include`", "For `#include \"stack.h\"` in `main.c`, describe what happens to the contents of `stack.h` before compilation.", ""],
    ["C Preprocessor, Macros, and Headers", "7", "Macro vs function", "Explain why a macro call such as `MAX(i++, j++)` can change variables more times than a function call would.", ""],
    ["C Preprocessor, Macros, and Headers", "8", "Stringification", "Write a tiny macro that prints both an expression's text and its value using stringification.", ""],
    ["C Preprocessor, Macros, and Headers", "9", "Include guards", "Write a complete include guard for `stack.h`, including the closing directive.", ""],
    ["C++ Templates and STL", "2", "Templates vs macros", "Given a macro-generated swap function appearing in two `.cpp` files, explain when the text substitution happens and why the linker may complain.", ""],
    ["C++ Templates and STL", "6", "Class template member definitions", "Complete the outside-class definition header for `pop`: `template<typename T> T ______::pop()`.", ""],
    ["C++ Templates and STL", "7", "Template definitions in headers", "Given `template<typename T> T max_value(T a, T b);` in a header and the body only in a `.cpp`, explain why another `.cpp` using `max_value(2, 3)` may fail.", ""],
    ["C++ Templates and STL", "10", "Vector iterators", "Write the full `for` loop using `auto`, `begin()`, `end()`, and dereferencing to print every element of `std::vector<int> v`.", ""],
    ["Rust Error Handling and File I/O", "6", "`?` and return types", "Given a `parse_num` function that borrows a string slice, parses an `i32` with `?`, and returns plain `i32`, explain why this cannot compile and fix the return type.", ""],
    ["Rust Error Handling and File I/O", "8", "Mapping parse errors", "Convert `parts[1].trim().parse::<u32>()` into a quantity value, returning `Err(\"bad quantity\".to_string())` if parsing fails.", ""],
    ["Rust Error Handling and File I/O", "9", "`unwrap` in library code", "Replace a library function that uses `.unwrap()` on a parse result with a version that lets the caller recover.", ""],
    ["Rust Error Handling and File I/O", "10", "`main` returning `Result`", "Write a `main` signature that can use `?` for file-read and parse errors, and include the final successful return expression.", ""],
    ["Rust Collections and Data Modelling", "1", "Borrowed string-slice parameter calls", "Given a `print_text` function that borrows a string slice and `let text = String::from(\"hello\");`, write one call with a string literal and one call with the `String` value.", ""],
    ["Rust Collections and Data Modelling", "2", "Modifying a `String`", "Starting from `let mut text = String::from(\"Hi\");`, write code that produces exactly `Hi! there`, and identify which method takes a `char` versus a borrowed string slice.", ""],
    ["Rust Collections and Data Modelling", "4", "`Vec::get` missing case", "For `let v = vec![10, 20, 30];`, compare `v[10]` with `v.get(10)`. Include what happens when the index is missing and show how to handle the `get` result.", ""],
    ["Rust Collections and Data Modelling", "7", "`String` field construction", "Given `struct Book { title: String, pages: u32 }`, create a `Book` from the literal `\"Rust\"` without using a borrowed string slice where a `String` is required.", ""],
    ["Rust Collections and Data Modelling", "8", "Immutable vs mutable self borrows", "In an `impl Counter`, write one method that only reads `value` using an immutable self borrow and one method that changes `value` using a mutable self borrow. Explain why the second one needs `mut`.", ""],
    ["Rust Collections and Data Modelling", "12", "`Option<T>` and null safety", "Explain why returning `Option` containing a borrowed value from a lookup is safer than returning a possible null pointer. Mention what the caller must handle before using the value.", ""],
    ["C Function Pointers and Callbacks", "5", "Callback received by `apply`", "Complete `int apply(int a, int b, int (*fn)(int, int)) { return _____; }`, then trace what happens when it is called as `apply(1, 3, Plus)`.", ""],
    ["C Function Pointers and Callbacks", "6", "`qsort` arguments", "Complete the call that sorts `int values[] = {3, 1, 2};` using `compare_ints`: `qsort(_____, _____, _____, _____);`.", ""],
    ["C Function Pointers and Callbacks", "7", "Integer comparator steps", "Fill in the body of `int compare_ints(const void *p, const void *q)` so it works correctly with `qsort` on an integer array.", ""],
    ["C Function Pointers and Callbacks", "9", "`const void *` comparator parameters", "`qsort` rejects `int compare_ints(int *a, int *b)`. Fix the signature and explain why the fixed version matches `qsort`.", ""],
    ["C Function Pointers and Callbacks", "10", "Pointer arithmetic with `char *`", "In generic array code with `void *array` and `size_t width`, write the expression for the address of element `i` after converting the base pointer to `char *`.", ""],
]

RULES_COLUMNS = ["Topic sheet", "Question number", "Topic", "Correct rule"]
RULES_ROWS = [
    ["C Pointers and Memory", "1", "Pointer basics", "The pointer update changes `x`, so `x` and `y` are both 7. The address expressions are the address of `x` and `p`; the integer values are `x` and the value reached through `p`."],
    ["C Pointers and Memory", "2", "`sizeof` vs `strlen`", "`sizeof s` is 20 and `strlen(s)` is 5, so 14 more visible characters fit safely because one byte must remain for `\\0`."],
    ["C Pointers and Memory", "3", "Out-of-bounds access", "The loop writes `a[5]`, which is past the end. Only use index values 0 to 4; possible symptoms include corrupted memory, wrong values, or a crash."],
    ["C Pointers and Memory", "4", "`malloc` safety check", "Use `if (a == NULL) { /* handle failure before using a */ }`; no code should write through `a` unless the allocation succeeded."],
    ["C Pointers and Memory", "5", "`strcpy` into `char *`", "`char *p` has no storage. Use an array such as `char p[6]; strcpy(p, \"Hello\");` or allocate enough bytes with `malloc` and free them later."],
    ["C Pointers and Memory", "6", "Dynamic 2D array", "On row allocation failure, free only rows already allocated: loop from row 0 up to row r - 1, call `free(X[i])` for each, then `free(X)`."],
    ["Rust Ownership and Borrowing", "7", "Ownership rules", "`s1` is moved into `s2`, so printing `s1` is rejected. Fix by cloning with `let s2 = s1.clone();` or by borrowing instead of moving."],
    ["Rust Ownership and Borrowing", "8", "Move semantics", "Change the function to borrow a string slice instead of taking ownership, then call it with a borrow of `name`. A borrow does not move `name`, so it can still be printed."],
    ["Rust Ownership and Borrowing", "9", "Borrowed string-slice parameters and iteration", "Use `text.chars()` to iterate over characters. In the loop, check whether each character is `a` and count matches. Byte iteration is not the same as character iteration."],
    ["Rust Ownership and Borrowing", "10", "Modifying a `String`", "Use `text.push('!');` for one character and `text.push_str(\" there\");` for a string slice."],
    ["Rust Ownership and Borrowing", "11", "`String` vs borrowed string slices", "Use a borrowed string-slice parameter for read-only text. A string literal can be passed directly, and a `String` value can be passed by borrowing it."],
    ["C Files and Streams", "12", "Text vs binary streams", "Use binary mode such as `fopen(path, \"rb\")`. Text mode can translate characters such as newlines, which changes the bytes you read."],
    ["C Files and Streams", "13", "`scanf` basics", "If the input is `abc`, `scanf` returns 0 and `k` is not assigned a new integer. Check `rc == 1` before trusting `k`."],
    ["C Files and Streams", "14", "Buffering and flushing", "Call `fflush(stdout);` after the prompt/progress message if it must appear before later work or before waiting for input."],
    ["C Files and Streams", "15", "`ferror` vs `feof`", "After the loop, `if (ferror(fp)) { ... }` detects a real read error. If not, the `EOF` was just normal end-of-file."],
    ["C Files and Streams", "16", "`rewind` and `fseek`", "Use `rewind(fp);` and then `fseek(fp, 20, SEEK_SET);`; `SEEK_SET` makes the offset relative to the start of the file."],
    ["C Files and Streams", "17", "Open / write / flush / close", "Check `fp == NULL` immediately after `fopen`; only call `fprintf` on a valid `FILE *`, and call `fclose(fp)` before returning."],
    ["C Preprocessor, Macros, and Headers", "2", "`#include`", "`#include \"stack.h\"` makes the preprocessor find the named header and copy its contents into `main.c` at that point."],
    ["C Preprocessor, Macros, and Headers", "7", "Macro vs function", "Macros perform textual substitution and can evaluate arguments multiple times, so `i++` or `j++` may run more than once. Function arguments are evaluated before the function call."],
    ["C Preprocessor, Macros, and Headers", "8", "Stringification", "Use `#` before the macro parameter, for example `#define REPORT_INT(X) printf(\"%s = %d\\n\", #X, X)`."],
    ["C Preprocessor, Macros, and Headers", "9", "Include guards", "A complete guard is `#ifndef STACK_H`, `#define STACK_H`, header contents, then `#endif`."],
    ["C++ Templates and STL", "2", "Templates vs macros", "Macros are expanded as text before compilation. If two `.cpp` files expand the macro into the same normal function definition, the linker sees two definitions and reports an error."],
    ["C++ Templates and STL", "6", "Class template member definitions", "The completed header is `template<typename T> T Stack<T>::pop()`. The `Stack<T>` part is needed because `pop` belongs to the class template instantiated with `T`."],
    ["C++ Templates and STL", "7", "Template definitions in headers", "A template body must be visible wherever the compiler creates a real version. If another file calls `max_value(2, 3)`, it needs the function body in the header, not only the prototype."],
    ["C++ Templates and STL", "10", "Vector iterators", "Use `for (auto it = v.begin(); it != v.end(); ++it) { std::cout << *it; }`. The iterator points at each element, and `*it` reads the current value."],
    ["Rust Error Handling and File I/O", "6", "`?` and return types", "`?` can return the parse error early, so the function must return a compatible `Result`, such as a result containing `i32` on success and `std::num::ParseIntError` on failure, then return `Ok(n)`."],
    ["Rust Error Handling and File I/O", "8", "Mapping parse errors", "Use `let quantity = parts[1].trim().parse::<u32>().map_err(|_| \"bad quantity\".to_string())?;` so a parse failure becomes the requested `Err` message."],
    ["Rust Error Handling and File I/O", "9", "`unwrap` in library code", "`unwrap()` panics and makes the failure unrecoverable for the caller. Return `Result` instead so the caller can decide how to handle the error."],
    ["Rust Error Handling and File I/O", "10", "`main` returning `Result`", "Use `fn main() -> Result<(), Box<dyn std::error::Error>>` so file-read and parse errors can be propagated with `?`. Finish successful execution with `Ok(())`."],
    ["Rust Collections and Data Modelling", "1", "Borrowed string-slice parameter calls", "A function taking a borrowed string slice can be called with a string literal directly. A `String` value must be borrowed, so call with the string literal first and then call again by borrowing `text`."],
    ["Rust Collections and Data Modelling", "2", "Modifying a `String`", "Use `text.push('!')` for a single character and `text.push_str(\" there\")` for a string slice. A one-line `text.push_str(\"! there\")` also gives the same final string, but it does not demonstrate both methods."],
    ["Rust Collections and Data Modelling", "4", "`Vec::get` missing case", "`v[10]` panics if index 10 is missing. `v.get(10)` returns an `Option` containing a possible borrowed value, so the caller can handle `Some(value)` and `None` with `match` or `if let`."],
    ["Rust Collections and Data Modelling", "7", "`String` field construction", "The field type is `String`, so a string literal must be converted with `String::from(\"Rust\")` or `\"Rust\".to_string()`. Parentheses around a literal do not change it from a borrowed string slice to `String`."],
    ["Rust Collections and Data Modelling", "8", "Immutable vs mutable self borrows", "An immutable self borrow is for reading. A mutable self borrow is required when the method changes fields such as `self.value += 1`."],
    ["Rust Collections and Data Modelling", "12", "`Option<T>` and null safety", "Returning an `Option` containing a borrowed value makes absence explicit as `None`. The caller must handle `Some` and `None`, so there is no chance of accidentally dereferencing a null pointer before checking whether a value exists."],
    ["C Function Pointers and Callbacks", "5", "Callback received by `apply`", "The callback is `Plus`. `apply` receives `Plus` through its function pointer parameter, then calls that pointer to decide what operation to perform."],
    ["C Function Pointers and Callbacks", "6", "`qsort` arguments", "`qsort` receives the base pointer, number of elements, size of each element in bytes, and comparator callback. For `int values[] = {3, 1, 2};`, use `values`, 3, `sizeof values[0]`, and `compare_ints`."],
    ["C Function Pointers and Callbacks", "7", "Integer comparator steps", "An integer comparator receives two `const void *` pointers, treats them as `const int *`, compares the pointed-to integer values, and returns negative, zero, or positive."],
    ["C Function Pointers and Callbacks", "9", "`const void *` comparator parameters", "`qsort` is generic, so the comparator receives pointers to elements of unknown type. `const` means those pointed-to elements are read-only inside the comparator."],
    ["C Function Pointers and Callbacks", "10", "Pointer arithmetic with `char *`", "Pointer arithmetic moves by the size of the pointed-to type. Generic array code uses `char *` because one step is one byte, so byte offsets such as `i * width` can locate element `i`."],
]


SHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
XML_NS = {"m": SHEET_NS, "r": REL_NS, "rel": PACKAGE_REL_NS}


def stable_tracker_key(row: list[str]) -> tuple[str, str]:
    return tuple(value.strip() for value in row[:2])


def column_number(cell_ref: str) -> int:
    column = "".join(char for char in cell_ref if char.isalpha())
    number = 0
    for char in column:
        number = number * 26 + ord(char.upper()) - 64
    return number


def cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//m:t", XML_NS))

    value = cell.find("m:v", XML_NS)
    if value is None or value.text is None:
        return ""

    if cell_type == "s":
        index = int(value.text)
        return shared_strings[index] if index < len(shared_strings) else ""

    return value.text


def shared_strings(xlsx: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in xlsx.namelist():
        return []

    root = ET.fromstring(xlsx.read("xl/sharedStrings.xml"))
    return [
        "".join(text.text or "" for text in item.findall(".//m:t", XML_NS))
        for item in root.findall("m:si", XML_NS)
    ]


def workbook_sheet_path(xlsx: zipfile.ZipFile, sheet_name: str) -> str | None:
    workbook = ET.fromstring(xlsx.read("xl/workbook.xml"))
    relationships = ET.fromstring(xlsx.read("xl/_rels/workbook.xml.rels"))
    relationship_targets = {
        relationship.get("Id"): relationship.get("Target")
        for relationship in relationships.findall("rel:Relationship", XML_NS)
    }

    for sheet in workbook.findall("m:sheets/m:sheet", XML_NS):
        if sheet.get("name") != sheet_name:
            continue

        relationship_id = sheet.get(f"{{{REL_NS}}}id")
        target = relationship_targets.get(relationship_id)
        if target is None:
            return None
        return target[1:] if target.startswith("/") else f"xl/{target}"

    return None


def sheet_rows_from_xlsx(path: Path, sheet_name: str) -> list[list[str]]:
    with zipfile.ZipFile(path) as xlsx:
        sheet_path = workbook_sheet_path(xlsx, sheet_name)
        if sheet_path is None:
            return []

        strings = shared_strings(xlsx)
        root = ET.fromstring(xlsx.read(sheet_path))
        rows = []

        for row in root.findall("m:sheetData/m:row", XML_NS):
            by_column: dict[int, str] = {}
            max_column = 0

            for cell in row.findall("m:c", XML_NS):
                reference = cell.get("r", "")
                column = column_number(reference)
                if column == 0:
                    continue

                max_column = max(max_column, column)
                by_column[column] = cell_text(cell, strings)

            rows.append([by_column.get(index, "") for index in range(1, max_column + 1)])

        return rows


def completed_marks_from_existing_workbook(path: Path) -> dict[tuple[str, str], str]:
    if not path.exists():
        return {}

    try:
        rows = sheet_rows_from_xlsx(path, "Tracker")
    except (ET.ParseError, KeyError, ValueError, zipfile.BadZipFile) as error:
        raise RuntimeError(f"Could not read existing completion marks from {path}") from error

    if not rows:
        raise RuntimeError(f"Could not find a Tracker sheet in {path}")

    headers = rows[0]
    try:
        topic_index = headers.index("Topic sheet")
        question_index = headers.index("Question number")
        completed_index = headers.index("Completed")
    except ValueError as error:
        raise RuntimeError(f"Tracker sheet in {path} is missing an expected column") from error

    marks = {}
    needed_columns = max(topic_index, question_index, completed_index)
    for row in rows[1:]:
        if len(row) <= needed_columns:
            continue

        key = (
            row[topic_index].strip(),
            row[question_index].strip(),
        )
        marks[key] = row[completed_index].strip()

    return marks


def tracker_rows_with_existing_completed_marks(path: Path) -> list[list[str]]:
    completed_marks = completed_marks_from_existing_workbook(path)
    rows = []

    for row in TRACKER_ROWS:
        copied_row = row.copy()
        key = stable_tracker_key(copied_row)
        if key in completed_marks:
            copied_row[4] = completed_marks[key]
        rows.append(copied_row)

    return rows


def col_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def inline_cell(ref: str, value: str, style: int = 2) -> str:
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t>{escape(value)}</t></is></c>'


def estimated_row_height(row: list[str], widths: list[float], min_height: int = 54) -> int:
    max_lines = 1
    for value, width in zip(row, widths):
        chars_per_line = max(12, int(width * 1.1))
        lines = value.splitlines() or [""]
        wrapped_lines = sum(max(1, (len(line) + chars_per_line - 1) // chars_per_line) for line in lines)
        max_lines = max(max_lines, wrapped_lines)
    return min(140, max(min_height, 18 * max_lines))


def sheet_xml(
    rows: list[list[str]],
    columns: list[str],
    table_range: str,
    rel_id: str,
    widths: list[float],
    min_body_height: int = 54,
) -> str:
    sheet_rows = [columns] + rows
    xml_rows = []
    for row_index, row in enumerate(sheet_rows, start=1):
        style = 1 if row_index == 1 else 2
        height = 24 if row_index == 1 else estimated_row_height(row, widths, min_body_height)
        cells = []
        for column_index, value in enumerate(row, start=1):
            cells.append(inline_cell(f"{col_name(column_index)}{row_index}", value, style))
        xml_rows.append(f'<row r="{row_index}" ht="{height}" customHeight="1">{"".join(cells)}</row>')

    col_xml = "".join(
        f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>'
        for i, width in enumerate(widths, start=1)
    )

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheetViews>
    <sheetView workbookViewId="0">
      <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
      <selection pane="bottomLeft"/>
    </sheetView>
  </sheetViews>
  <sheetFormatPr defaultRowHeight="15"/>
  <cols>{col_xml}</cols>
  <sheetData>{''.join(xml_rows)}</sheetData>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
  <tableParts count="1"><tablePart r:id="{rel_id}"/></tableParts>
</worksheet>'''


def table_xml(table_id: int, name: str, ref: str, columns: list[str]) -> str:
    table_cols = "".join(
        f'<tableColumn id="{i}" name="{escape(column)}"/>' for i, column in enumerate(columns, start=1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  id="{table_id}" name="{name}" displayName="{name}" ref="{ref}" totalsRowShown="0">
  <autoFilter ref="{ref}"/>
  <tableColumns count="{len(columns)}">{table_cols}</tableColumns>
  <tableStyleInfo name="TableStyleMedium2" showFirstColumn="0" showLastColumn="0" showRowStripes="1" showColumnStripes="0"/>
</table>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><color theme="1"/><name val="Calibri"/><family val="2"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1D4ED8"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color rgb="FFD1D5DB"/></left><right style="thin"><color rgb="FFD1D5DB"/></right><top style="thin"><color rgb="FFD1D5DB"/></top><bottom style="thin"><color rgb="FFD1D5DB"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
  <dxfs count="0"/>
  <tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>
</styleSheet>'''


def build_xlsx() -> None:
    tracker_rows = tracker_rows_with_existing_completed_marks(OUTPUT)
    tracker_ref = f"A1:{col_name(len(TRACKER_COLUMNS))}{len(tracker_rows) + 1}"
    rules_ref = f"A1:{col_name(len(RULES_COLUMNS))}{len(RULES_ROWS) + 1}"
    now = datetime.now(timezone.utc).isoformat()

    files = {
        "[Content_Types].xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/tables/table1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>
  <Override PartName="/xl/tables/table2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>''',
        "_rels/.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>''',
        "xl/workbook.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Tracker" sheetId="1" r:id="rId1"/>
    <sheet name="Correct Rules" sheetId="2" r:id="rId2"/>
  </sheets>
</workbook>''',
        "xl/_rels/workbook.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''',
        "xl/worksheets/sheet1.xml": sheet_xml(tracker_rows, TRACKER_COLUMNS, tracker_ref, "rId1", [28, 14, 24, 68, 14]),
        "xl/worksheets/sheet2.xml": sheet_xml(
            RULES_ROWS, RULES_COLUMNS, rules_ref, "rId1", [28, 14, 28, 95], min_body_height=72
        ),
        "xl/worksheets/_rels/sheet1.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" Target="../tables/table1.xml"/></Relationships>''',
        "xl/worksheets/_rels/sheet2.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" Target="../tables/table2.xml"/></Relationships>''',
        "xl/tables/table1.xml": table_xml(1, "RevisionMistakeTracker", tracker_ref, TRACKER_COLUMNS),
        "xl/tables/table2.xml": table_xml(2, "RevisionCorrectRules", rules_ref, RULES_COLUMNS),
        "xl/styles.xml": styles_xml(),
        "docProps/app.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application></Properties>''',
        "docProps/core.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Revision Mistake Log</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>''',
    }

    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as xlsx:
        for name, content in files.items():
            xlsx.writestr(name, content)


if __name__ == "__main__":
    build_xlsx()
    print(OUTPUT)
