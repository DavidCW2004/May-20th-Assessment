from __future__ import annotations

import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "revision-mistake-log.xlsx"
BACKUP_DIR = ROOT / "backups"

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
    ["C++ Operator Overloading", "2", "`MyInteger + int` member overload", "Given `class MyInteger { int i; public: MyInteger(int value) : i(value) {} /* missing */ };`, write the member overload that makes `MyInteger a(4); int x = a + 6;` set `x` to 10.", ""],
    ["C++ Operator Overloading", "5", "Legal and sensible overloads", "For `Point`, judge these attempted meanings: `Point + Point`, `int + int`, `sizeof point`, and `point.x`. Mark each as legal or illegal to overload, then choose whether the legal one is sensible.", ""],
    ["C++ Operator Overloading", "6", "`operator[]` reference return", "Complete an array class subscript operator so `arr[2] = 99;` changes the stored element. The body should return the element itself, not its address.", ""],
    ["Rust Generics and Traits", "3", "Generic `Point` method", "Given a generic `Point` with fields `x` and `y`, complete the `impl` block so method `x` borrows the object and returns a borrow of the `x` field.", ""],
    ["Rust Generics and Traits", "6", "Borrowed generic `Area` parameter", "Fix a broken free function that tries to use `self.area()` outside an `impl` block, so it prints the area of any borrowed shape that implements `Area`.", ""],
    ["Rust Generics and Traits", "7", "`show_larger` display bound", "Fix the signature of `show_larger` when its body compares two values and then prints the winning value with normal braces.", ""],
    ["Rust Generics and Traits", "9", "`derive` attribute syntax", "Repair the derive line for a custom struct used with `assert_eq!` and debug printing: `#derive Debug, PartialEq`.", ""],
    ["Rust Generics and Traits", "10", "`HashMap` key derives", "A custom `Team` value is used as a key in a `HashMap`. Add the derives needed so insertion and lookup by key compile.", ""],
    ["C++ Virtual Functions and Dynamic Binding", "3", "Virtual call through base pointer", "Given virtual `read`, `TemperatureSensor temp(\"Lab\", 21.5);` and a `Sensor *s` pointing at `temp`, work out which `read` function runs and what value is returned.", ""],
    ["C++ Virtual Functions and Dynamic Binding", "7", "Virtual destructor in polymorphic base", "Complete the destructor declaration in a polymorphic base class: `_____ ~Sensor() = default;`.", ""],
    ["C++ Virtual Functions and Dynamic Binding", "8", "Constructor string reference parameter", "Complete the `TemperatureSensor` constructor parameter for `name` as a const string reference, then write the initializer list that calls `Sensor(id, name)` and stores `celsius`.", ""],
    ["C++ Smart Pointer Practice with std::unique_ptr", "2", "Base-type smart pointer declaration", "A factory line must store a newly created `TemperatureSensor` in a variable that can later hold any `Sensor` subtype. Write the full smart-pointer declaration and construction call.", ""],
    ["C++ Smart Pointer Practice with std::unique_ptr", "4", "Returning unique ownership", "Write the return type and body for `make_sensor` so it creates a `TemperatureSensor` and gives ownership to the caller through the base sensor interface.", ""],
    ["C++ Smart Pointer Practice with std::unique_ptr", "7", "Polymorphic owned object", "Trace `std::unique_ptr<Sensor> sensor = std::make_unique<TemperatureSensor>(...); sensor->read();` and identify the pointer type, the owned heap object type, and the function that runs.", ""],
    ["C Types and Conversions", "4", "Floating-point to `short` conversion", "A program stores `123456.789` in a `short` and then prints the result. Explain what kind of conversion happens and what information can be lost.", ""],
    ["C Types and Conversions", "5", "`typedef` order", "Write the typedef that lets `Temperature today = 8.0f;` compile, then explain which name is the existing type and which name is the new alias.", ""],
    ["C Structures and Dynamic Data Structures", "7", "Front insertion pointer order", "Given `root` points to `C -> Q -> NULL` and `new_node` points to `A -> NULL`, write the assignments that make the list `A -> C -> Q -> NULL` without losing any nodes.", ""],
    ["C Structures and Dynamic Data Structures", "9", "Linked-list stack pop", "Given `Node *root` points at `A -> C -> Q -> NULL`, complete `char pop(Node **root_ptr)` so it returns `A`, updates the caller's root to `C`, and frees the removed node.", ""],
    ["C++ Moving from C", "1", "Compile and link flow", "For a program split across `main.cpp` and `stack.cpp`, write the separate compile commands that create object files, then write the link command that creates the executable.", ""],
    ["C++ Moving from C", "3", "Stream input operator", "Write the C++ stream line that reads an integer from standard input into `count`, then explain why the opposite arrow direction would be wrong.", ""],
    ["C++ Moving from C", "7", "`auto` and static typing", "Given `auto x = 10; x = \"hello\";`, explain the compile error and what `auto` did, without describing it as dynamic typing.", ""],
    ["C Command-line Arguments", "6", "`atoi` invalid input vs zero", "For `int n = atoi(argv[1]);`, compare `argv[1]` values `\"abc\"` and `\"0\"`: state what each returns and why the return value alone cannot prove the input was valid.", ""],
    ["C Command-line Arguments", "9", "`strtol` no digits consumed", "For `char *end; long n = strtol(text, &end, 10);`, explain what `end == text` means for `text = \"abc\"`, then say what `*end` should be after a clean full-number parse.", ""],
    ["Rust Concurrency and Parallelism", "2", "Spawned thread lifetime and `move`", "In `fn start() { let text = String::from(\"hi\"); thread::spawn(|| println!(\"{text}\")); }`, explain why borrowing `text` is rejected, then fix the spawn with `move` and say why the thread must own the value.", ""],
    ["Rust Concurrency and Parallelism", "6", "Cloned channel transmitters", "Write the loop for four workers that all send through one `mpsc` channel: clone `tx` for each worker, move the clone into the closure, then explain why every clone still reaches the same `rx`.", ""],
    ["Rust Concurrency and Parallelism", "8", "`Arc<Mutex<i32>>` shared counter", "Trace two threads incrementing the same `Arc<Mutex<i32>>` counter and explain how shared ownership is provided and why each update is exclusive.", ""],
    ["Rust Concurrency and Parallelism", "9", "Poisoned mutex lock result", "For a mutex that was held by a thread when it panicked, write how `lock()` reports the problem and how you would handle the returned result instead of blindly assuming the lock succeeded.", ""],
    ["Rust Concurrency and Parallelism", "10", "Local results then final merge", "For a word-count task split across four threads, compare one global locked `HashMap` updated for every word with each thread building a local map and merging once at the end. Explain which is better and why.", ""],
    ["C++ Error Handling and Lambdas", "5", "Stack unwinding and RAII cleanup", "In a function that creates a local `std::vector<int>` and then calls a function that throws, explain what happens to the vector during stack unwinding and why this is safer than manual cleanup after the throwing call.", ""],
    ["C++ Error Handling and Lambdas", "8", "Reference-capture lambda syntax", "Write the full lambda assignment that captures `counter` by reference, increments the original counter, and includes the required semicolon after the lambda expression.", ""],
    ["C++ Error Handling and Lambdas", "10", "Complete `count_if` lambda call", "Write a complete `std::count_if` call that counts values greater than 5 in `v`, making sure the lambda body and the algorithm call both have their closing brackets.", ""],
    ["Rust Crash-course Basics", "3", "Shadowing parse syntax", "Starting from `let value = \"12\";`, use shadowing to parse it as an `i32`, then shadow it again so the final value is one larger.", ""],
    ["Rust Crash-course Basics", "4", "`const` declaration syntax", "A Rust program needs a compile-time maximum user count of 100. Write the constant declaration with the required type annotation and Rust naming style.", ""],
    ["Rust Crash-course Basics", "7", "Array debug printing", "Create an array of three integers and print the whole array using the correct debug-format placeholder, then explain why normal display formatting is not the right choice.", ""],
    ["Rust Crash-course Basics", "10", "Semicolon returns unit", "Compare `fn f() -> i32 { 5 }` with `fn f() -> i32 { 5; }`: explain which one returns an `i32`, which one returns unit `()`, and why.", ""],
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
    now = datetime.now(timezone.utc).isoformat()

    if OUTPUT.exists():
        BACKUP_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = BACKUP_DIR / f"{OUTPUT.stem}-{stamp}{OUTPUT.suffix}"
        backup.write_bytes(OUTPUT.read_bytes())

    files = {
        "[Content_Types].xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/tables/table1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>
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
  </sheets>
</workbook>''',
        "xl/_rels/workbook.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''',
        "xl/worksheets/sheet1.xml": sheet_xml(tracker_rows, TRACKER_COLUMNS, tracker_ref, "rId1", [28, 14, 24, 68, 14]),
        "xl/worksheets/_rels/sheet1.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" Target="../tables/table1.xml"/></Relationships>''',
        "xl/tables/table1.xml": table_xml(1, "RevisionMistakeTracker", tracker_ref, TRACKER_COLUMNS),
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
