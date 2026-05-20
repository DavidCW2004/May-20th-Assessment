from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET
from zipfile import ZipFile
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "pre-exam-things-to-know.pdf"
RAG = ROOT / "revision-rag-topic-list.md"
MOCK = ROOT / "revision-mock-exam-mistakes.md"
XLSX = ROOT / "revision-mistake-log.xlsx"


BUCKETS = [
    (
        "C pointers, memory, arrays, strings",
        [
            "pointer",
            "malloc",
            "free",
            "dangling",
            "wild",
            "leak",
            "array",
            "string",
            "strcpy",
            "strcat",
            "strlen",
            "sizeof",
            "bounds",
            "2d",
            "null terminator",
            "void *",
            "qsort",
            "comparator",
            "struct",
            "linked",
        ],
    ),
    (
        "C files, streams, buffering, diagnostics",
        [
            "file",
            "stream",
            "scanf",
            "fgets",
            "fgetc",
            "fread",
            "fprintf",
            "printf",
            "stdout",
            "stderr",
            "fflush",
            "buffer",
            "ferror",
            "eof",
            "errno",
            "fseek",
            "rewind",
            "binary",
        ],
    ),
    (
        "C preprocessor, headers, build",
        [
            "macro",
            "preprocessor",
            "#include",
            "include",
            "header",
            "guard",
            "extern",
            "static",
            "makefile",
            "cmake",
            "object",
            ".o",
            "link",
            "library",
            "compilation",
        ],
    ),
    (
        "C++ classes, inheritance, polymorphism",
        [
            "class",
            "constructor",
            "destructor",
            "inheritance",
            "derived",
            "base",
            "protected",
            "private",
            "public",
            "virtual",
            "polymorphic",
            "slicing",
            "diamond",
            "friend",
            "getter",
            "setter",
        ],
    ),
    (
        "C++ RAII, smart pointers, exceptions",
        [
            "raii",
            "unique_ptr",
            "shared_ptr",
            "weak_ptr",
            "smart pointer",
            "std::move",
            "make_unique",
            "exception",
            "throw",
            "catch",
            "what",
            "rule of three",
        ],
    ),
    (
        "C++ templates, operators, STL algorithms",
        [
            "template",
            "operator",
            "ostream",
            "subscript",
            "map",
            "vector",
            "sort",
            "binary_search",
            "count_if",
            "lambda",
            "function object",
            "iterator",
            "stl",
            "auto",
            "overload",
            "mangling",
        ],
    ),
    (
        "Rust ownership, borrowing, strings, slices",
        [
            "ownership",
            "borrow",
            "reference",
            "string",
            "&str",
            "slice",
            "vec",
            "move",
            "copy",
            "drop",
            "box",
            "rc",
            "dangling",
            "lifetime",
        ],
    ),
    (
        "Rust Result, Option, parsing, tests",
        [
            "result",
            "option",
            "?",
            "parse",
            "error",
            "expect",
            "unwrap",
            "match",
            "ok_or",
            "map_err",
            "file",
            "test",
            "super",
            "pub",
            "hashmap",
            "entry",
        ],
    ),
    (
        "Rust iterators, traits, closures, concurrency",
        [
            "iter",
            "iterator",
            "filter",
            "map",
            "fold",
            "enumerate",
            "collect",
            "trait",
            "derive",
            "generic",
            "closure",
            "fnmut",
            "arc",
            "mutex",
            "mpsc",
            "thread",
            "channel",
            "sort_by",
        ],
    ),
]


def cell_text(value: str) -> str:
    return value.replace("`", "").strip().lower()


def bucket_for(text: str) -> str:
    haystack = cell_text(text)
    scores: dict[str, int] = {}
    for bucket, terms in BUCKETS:
        score = sum(1 for term in terms if term.lower() in haystack)
        if score:
            scores[bucket] = score
    if not scores:
        return "General exam technique and syntax precision"
    return max(scores, key=scores.get)


def parse_rag() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    language = ""
    for line in RAG.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            language = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or "Status | Topic" in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        status, topic, sheet = parts[:3]
        if status not in {"R", "A", "G"}:
            continue
        rows.append(
            {
                "language": language,
                "status": status,
                "topic": re.sub(r"\[(.*?)\]\(.*?\)", r"\1", topic),
                "sheet": re.sub(r"\[(.*?)\]\(.*?\)", r"\1", sheet),
                "bucket": bucket_for(f"{language} {topic}"),
            }
        )
    return rows


def parse_mock() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in MOCK.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^### Q(\d+) \[(X?)\] - (.+)$", line)
        if match:
            if current:
                rows.append(current)
            current = {
                "number": match.group(1),
                "completed": "Yes" if match.group(2) == "X" else "",
                "title": match.group(3).strip(),
                "source": "",
                "prompt": "",
            }
            continue
        if current and line.startswith("**Source:**"):
            current["source"] = re.sub(r"^\*\*Source:\*\*\s*", "", line).strip()
            continue
        if current and line.startswith("**Redo question:**"):
            current["prompt"] = re.sub(r"^\*\*Redo question:\*\*\s*", "", line).strip()
            continue
    if current:
        rows.append(current)
    for row in rows:
        row["bucket"] = bucket_for(f"{row['title']} {row['prompt']} {row['source']}")
    return rows


def _xlsx_col_name(ref: str) -> str:
    match = re.match(r"([A-Z]+)", ref)
    return match.group(1) if match else ""


def _xlsx_text(cell, ns: dict[str, str]) -> str:
    if cell.attrib.get("t") == "inlineStr":
        return "".join((t.text or "") for t in cell.findall(".//a:t", ns))
    value = cell.find("a:v", ns)
    return "" if value is None else (value.text or "")


def parse_xlsx_rows() -> list[dict[str, str]]:
    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(XLSX) as z:
        root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rows: list[dict[str, str]] = []
    for row in root.findall(".//a:row", ns):
        values: dict[str, str] = {}
        for cell in row.findall("a:c", ns):
            values[_xlsx_col_name(cell.attrib.get("r", ""))] = _xlsx_text(cell, ns)
        if any(values.values()):
            rows.append(values)
    if not rows:
        return []
    headers = rows[0]
    col_to_header = {col: header for col, header in headers.items()}
    output: list[dict[str, str]] = []
    for raw in rows[1:]:
        item = {col_to_header.get(col, col): value for col, value in raw.items()}
        item["bucket"] = bucket_for(
            f"{item.get('Topic sheet', '')} {item.get('Topic', '')} {item.get('Redo prompt', '')}"
        )
        output.append(item)
    return output


def priority_summary(
    rag_rows: list[dict[str, str]],
    mock_rows: list[dict[str, str]],
    xlsx_rows: list[dict[str, str]],
) -> list[dict[str, int | str]]:
    totals: dict[str, Counter] = defaultdict(Counter)
    for row in rag_rows:
        totals[row["bucket"]]["rag"] += 1
        if row["status"] == "R":
            totals[row["bucket"]]["red"] += 1
    for row in mock_rows:
        totals[row["bucket"]]["mock"] += 1
        if row.get("completed") != "Yes":
            totals[row["bucket"]]["open_mock"] += 1
    for row in xlsx_rows:
        totals[row["bucket"]]["xlsx"] += 1
        if str(row.get("Completed", "")).strip().lower() != "yes":
            totals[row["bucket"]]["open_xlsx"] += 1

    summary = []
    for bucket, counts in totals.items():
        score = (
            counts["red"] * 3
            + counts["open_mock"] * 3
            + counts["open_xlsx"] * 2
            + counts["mock"]
            + counts["xlsx"]
        )
        summary.append(
            {
                "bucket": bucket,
                "score": score,
                "red": counts["red"],
                "mock": counts["mock"],
                "open_mock": counts["open_mock"],
                "xlsx": counts["xlsx"],
                "open_xlsx": counts["open_xlsx"],
                "rag": counts["rag"],
            }
        )
    return sorted(summary, key=lambda item: (-int(item["score"]), str(item["bucket"])))


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#17324d"),
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#3f4e5a"),
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#17324d"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#244763"),
            spaceBefore=6,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11.2,
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9.2,
            spaceAfter=2,
        ),
        "tiny": ParagraphStyle(
            "Tiny",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=6.6,
            leading=8.2,
            spaceAfter=1,
        ),
        "note": ParagraphStyle(
            "Note",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.7,
            leading=11,
            textColor=colors.HexColor("#7a2e00"),
            backColor=colors.HexColor("#fff2d7"),
            borderColor=colors.HexColor("#f0b35c"),
            borderWidth=0.5,
            borderPadding=5,
            spaceBefore=4,
            spaceAfter=6,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.2,
            leading=8.6,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=2,
            spaceAfter=4,
        ),
    }


S = styles()


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(escape(text), S[style])


def raw_p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, S[style])


def code(text: str) -> Preformatted:
    return Preformatted(text.strip("\n"), S["code"])


def bullets(items: Iterable[str], style: str = "body") -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, style), leftIndent=7) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=12,
        bulletFontSize=5,
        bulletOffsetY=1,
    )


def status_color(status: str):
    return {
        "R": colors.HexColor("#f8cccc"),
        "A": colors.HexColor("#ffe8a6"),
        "G": colors.HexColor("#d8f0d2"),
    }.get(status, colors.white)


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#5d6972"))
    canvas.drawString(15 * mm, 10 * mm, "ECM2433 pre-exam things to know")
    canvas.drawRightString(195 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def priority_table(summary: list[dict[str, int | str]]):
    data = [
        [
            p("Priority area", "small"),
            p("Open mock", "small"),
            p("Open sheet", "small"),
            p("R topics", "small"),
            p("Why it matters", "small"),
        ]
    ]
    why = {
        "C pointers, memory, arrays, strings": "High bug density: bounds, allocation size, terminators, UB.",
        "C files, streams, buffering, diagnostics": "Exam questions often hide return checks and stream-state details.",
        "C preprocessor, headers, build": "Small syntax details decide many marks: tabs, guards, macro grouping.",
        "C++ classes, inheritance, polymorphism": "Access and virtual dispatch questions are easy to misread.",
        "C++ RAII, smart pointers, exceptions": "Ownership and cleanup comparisons appear across languages.",
        "C++ templates, operators, STL algorithms": "Type signatures and return/reference choices are mark-heavy.",
        "Rust ownership, borrowing, strings, slices": "Core Rust marks depend on exact ownership/borrow wording.",
        "Rust Result, Option, parsing, tests": "Most Rust error-handling answers need exact `Result`/`?` behaviour.",
        "Rust iterators, traits, closures, concurrency": "Iterator item/reference types and closure capture are common traps.",
    }
    for item in summary[:8]:
        bucket = str(item["bucket"])
        data.append(
            [
                p(bucket, "small"),
                p(str(item["open_mock"]), "small"),
                p(str(item["open_xlsx"]), "small"),
                p(str(item["red"]), "small"),
                p(why.get(bucket, "Review exact syntax and wording."), "small"),
            ]
        )
    table = Table(data, colWidths=[52 * mm, 19 * mm, 20 * mm, 17 * mm, 62 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce8f2")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bac7d0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def compact_table(headers: list[str], rows: list[list[str]], widths: list[float]):
    data = [[p(header, "tiny") for header in headers]]
    for row in rows:
        data.append([p(value, "tiny") for value in row])
    table = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef4")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c7d1d8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def rag_table(rows: list[dict[str, str]]):
    data = [[p("Status", "tiny"), p("Topic", "tiny"), p("Priority bucket", "tiny")]]
    for row in rows:
        data.append([p(row["status"], "tiny"), p(row["topic"], "tiny"), p(row["bucket"], "tiny")])
    table = Table(data, colWidths=[13 * mm, 112 * mm, 45 * mm], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce8f2")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c7d1d8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    for idx, row in enumerate(rows, start=1):
        style.append(("BACKGROUND", (0, idx), (0, idx), status_color(row["status"])))
    table.setStyle(TableStyle(style))
    return table


def add_title(story: list):
    story.append(p("ECM2433 Things To Know Before The Exam", "title"))
    story.append(
        p(
            "Fast review pack generated from the RAG tracker, revision spreadsheet, and mock-exam mistakes. "
            "Use before the exam; do not take it into a closed-book exam unless explicitly permitted.",
            "subtitle",
        )
    )


def add_priority_pages(story: list, summary, mock_rows, xlsx_rows, rag_rows):
    add_title(story)
    story.append(p("How to use this in the last 30 minutes", "h1"))
    story.append(
        bullets(
            [
                "First 10 minutes: read the personal priority table and the pinned traps.",
                "Next 15 minutes: scan the personal high-frequency drills, then the C, C++, and Rust rule pages.",
                "Final 5 minutes: test yourself from the mental checklist, not by rereading passively.",
            ]
        )
    )
    story.append(
        p(
            "The counts below are weighted from open mock-exam mistakes, open spreadsheet rows, and red RAG topics. "
            "High count does not mean ignore the rest; it means check these first.",
            "note",
        )
    )
    story.append(priority_table(summary))
    story.append(Spacer(1, 5))
    story.append(p("Pinned Personal Traps", "h1"))
    story.append(
        bullets(
            [
                "Macro answers need full parentheses and multi-statement macros should use do { ... } while (0).",
                "For C strings, always account for the final '\\0'; `sizeof` and `strlen` answer different questions.",
                "After `malloc`, check for failure before writing. After `free`, the pointer value is stale; do not dereference it.",
                "For file/stream questions, say what is returned and what must be checked: `scanf`, `fgets`, `fread`, `ferror`, `errno`.",
                "C++ public inheritance means is-a. `protected` is visible to derived classes; `private` is not directly accessible.",
                "Polymorphic base classes need virtual functions for dispatch and a virtual destructor for deletion through base pointer type.",
                "Rust `&str` is a borrowed string slice; `String` owns heap text. Prefer `&str` for read-only text parameters.",
                "Rust `?` unwraps `Ok` and returns `Err` early. It is explicit propagation, not a hidden exception.",
                "Iterator item types matter: `.iter()` gives references; `.into_iter()` on a `Vec<T>` gives owned `T` values, but `filter` borrows its item.",
            ]
        )
    )
    story.append(Spacer(1, 5))
    story.append(
        p(
            f"Inputs used: {len(rag_rows)} RAG topics, {len(mock_rows)} mock-exam mistake entries, "
            f"and {len(xlsx_rows)} spreadsheet mistake rows.",
            "small",
        )
    )
    story.append(PageBreak())


PERSONAL_DRILLS = {
    "C pointers, memory, arrays, strings": [
        "Before writing through `*p`, say out loud what storage `p` points at: stack object, array element, heap allocation, or nowhere valid.",
        "For every allocation or copy, calculate bytes including the terminator: `strlen(src) + 1` for C strings, `n * sizeof *p` for arrays.",
        "When an array is passed to a function, it decays to a pointer; pass the element count separately because `sizeof(values)` is then pointer size.",
        "For generic helpers, convert `void *` to `char *` before byte offsets: `(char *)array + index * width`.",
        "For linked-list removal, use `Node **` or a previous pointer so removing the head and a later node follow the same ownership rule.",
        "Memory-tool reports are not optional warnings: an invalid read/write, use-after-free, or heap-buffer-overflow means the C program has undefined behaviour even if it prints the expected answer.",
    ],
    "C files, streams, buffering, diagnostics": [
        "`fopen` can fail; handle `fp == NULL` before any read/write and use `errno`/`strerror` only after a function has reported failure.",
        "`fgets` returns `NULL` on EOF or error; after character loops ending on `EOF`, use `ferror(fp)` to check whether a real read error happened.",
        "`fread(out, sizeof *out, 1, fp) == 1` is the exact-record-read test; binary record seek offsets are usually `index * sizeof *out`.",
        "`strtol` validation has three separate ideas: no digits (`end == text`), range (`errno == ERANGE`), and leftover/invalid/range constraints for the target type.",
        "`stdout` is for normal output and may be buffered; `stderr` is for diagnostics. Use `fflush(stdout)` after progress text that must appear immediately.",
        "Do not use unbounded `%s`; for `char buffer[20]`, `%19s` leaves space for `\\0`, and `fgets(buffer, sizeof buffer, stdin)` is usually safer.",
    ],
    "C preprocessor, headers, build": [
        "Macros are text substitution before compilation. Parenthesise each argument and the whole result: `#define SQUARE(X) ((X) * (X))`.",
        "A multi-statement macro used like one statement should be wrapped in `do { ... } while (0)`.",
        "`static` at file scope gives internal linkage; it is how a C helper stays private to one `.c` file. C does not use `public`.",
        "Headers expose declarations and need include guards. Source files define storage/functions. `extern` declares something defined elsewhere.",
        "Makefile recipes start with a tab. The first target is the default. If `image.h` changes, any `.o` that depends on it should rebuild.",
        "Object files are compiled separately, then linked. Libraries are collections of object files; CMake generates project build files but does not replace the compile/link idea.",
    ],
    "C++ classes, inheritance, polymorphism": [
        "`class` defaults to private; `struct` defaults to public. Use accessors or friends for controlled access instead of exposing fields.",
        "`protected` can be used inside derived member functions; `private` base members cannot be directly accessed by derived classes.",
        "Public inheritance means an is-a relationship. Private/protected inheritance changes what outside code can treat as a base interface.",
        "Virtual dispatch only happens through a base pointer/reference and only for virtual functions with a matching derived override.",
        "Polymorphic base classes need `virtual ~Base() = default;` if objects may be deleted through base pointer type.",
        "Diamond inheritance without virtual bases creates two base subobjects; `virtual public Base` shares one base subobject.",
    ],
    "C++ RAII, smart pointers, exceptions": [
        "RAII ties resource lifetime to object lifetime: constructors/object creation acquire resources and destructors release them during normal exit or stack unwinding.",
        "A raw owning pointer plus `delete[]` is not enough if the object is copyable; rule-of-three questions also need copy constructor and copy assignment handling.",
        "`std::unique_ptr` is exclusive and move-only. Use `std::move(obj1)` to transfer ownership and expect the source to be empty but valid.",
        "`std::shared_ptr` destroys the object when the last shared owner disappears. `weak_ptr` observes without extending lifetime and must be locked before use.",
        "Catch standard exceptions as `const std::exception&` or a const reference to the specific exception to avoid copying and preserve the dynamic type.",
        "Exceptions can jump control flow, but RAII objects still clean themselves up during stack unwinding.",
    ],
    "C++ templates, operators, STL algorithms": [
        "`operator[]` returns `T&` when assignment through the subscript should mutate the stored element; return `const T&` for read-only const overloads.",
        "`operator<<` should take and return `std::ostream&`; returning the stream is what lets `std::cout << a << b` chain.",
        "Template member definitions outside the class need both lines: `template<typename T>` and `ReturnType Box<T>::method(...)`.",
        "Template definitions usually live in headers because each translation unit needs the body to instantiate the exact type it uses.",
        "`std::sort`, `std::binary_search`, and tie-breaker comparators must use the same ordering rule; descending data needs a descending comparator for binary search too.",
        "Lambdas and function objects are just callable predicates/comparators. For `count_if`, the callable returns `true` for values to count.",
    ],
    "Rust ownership, borrowing, strings, slices": [
        "A `String` move leaves the old binding unusable unless the type is copied or you borrow instead. Use `&str` for read-only text parameters.",
        "Rust allows many immutable borrows or one mutable borrow. A `Vec::push` needs mutable access and may reallocate, so active element references block it.",
        "A returned borrowed value needs a lifetime when it might come from either input: `fn choose<'a>(x: &'a str, y: &'a str) -> &'a str`.",
        "`Box<T>` owns heap data with a fixed-size pointer; it is how recursive enums get a known size.",
        "`Rc<T>` is single-thread reference counting; `Arc<T>` is atomic reference counting for shared ownership across threads.",
        "Rust checks ownership, borrowing, and lifetimes at compile time; drops happen automatically when owners go out of scope.",
    ],
    "Rust Result, Option, parsing, tests": [
        "`?` unwraps `Ok(value)` or returns the `Err(error)` early from the current function, so the function must return a compatible `Result`.",
        "Use `Option<&T>` for possibly missing borrowed data instead of panicking by indexing. The caller must handle `Some` and `None`.",
        "Convert missing pieces into errors with `ok_or_else`; convert parse errors with `map_err`; use `Box<dyn Error>` when a small exam function may return mixed error types.",
        "`unwrap()` is a quick panic; `expect(\"message\")` is a panic with a useful broken-assumption message. Recoverable code should return `Result` instead.",
        "A `let n = text.parse::<i32>()?;` statement needs a semicolon. A final `Ok(n)` expression usually should not.",
        "Unit tests beside code can use `super::*` and see private helpers; integration tests in `tests/` use only public API.",
    ],
    "Rust iterators, traits, closures, concurrency": [
        "Write the iterator item type at each step: `.iter()` yields references; `enumerate()` wraps items as `(usize, item)`; `filter` borrows each item for the predicate.",
        "`filter_map` is ideal when `Option` values should be skipped and transformed in one pass.",
        "`fold(start, |acc, item| next_acc)` must return the next accumulator. Assignment-style updates often return `()` by accident.",
        "Generic code needs trait bounds for every operation it uses: compare with `PartialOrd`, print with `Display` or `Debug`, hash-map keys with `Eq + Hash`.",
        "A closure that mutates captured state is `FnMut`; bind it with `let mut record = ...` before calling it more than once.",
        "For threads, clone each `mpsc` sender, move the clone into the closure, drop the original sender, and remember `Mutex::lock()` returns a poison-aware `Result`.",
    ],
    "General exam technique and syntax precision": [
        "When a question asks for code, write the exact signature first, then make each operator/return type match what the caller needs.",
        "When a question asks for an explanation, name the rule, apply it to the given line, and state the observable consequence.",
        "Most lost marks are small: missing semicolon, wrong reference type, no terminator space, unchecked return value, or comparator ordering mismatch.",
    ],
}


def add_personal_focus_drills(story: list, summary: list[dict[str, int | str]]):
    story.append(p("Personal High-Frequency Drills", "h1"))
    story.append(
        p(
            "These sections are ordered from your mock mistakes, spreadsheet rows, and red RAG topics. Treat them as active recall prompts: cover the answers and force the rule before looking back.",
            "note",
        )
    )
    added: set[str] = set()
    for item in summary:
        bucket = str(item["bucket"])
        drill_items = PERSONAL_DRILLS.get(bucket)
        if not drill_items or bucket in added:
            continue
        added.add(bucket)
        story.append(
            KeepTogether(
                [
                    p(
                        f"{bucket} - score {item['score']} | RAG red {item['red']} | mock {item['mock']} | sheet {item['xlsx']}",
                        "h2",
                    ),
                    bullets(drill_items, "small"),
                ]
            )
        )
        story.append(Spacer(1, 4))
    story.append(PageBreak())


def add_c_section(story: list):
    story.append(p("C: Must-Know Rules", "h1"))
    story.append(p("Types, conversions, and arrays", "h2"))
    story.append(
        bullets(
            [
                "`7 / 2` with integers gives `3`; cast before division for floating result: `(double)a / b`.",
                "Unsigned arithmetic wraps modulo the type range. `unsigned u = 0; u - 1` gives the maximum unsigned value.",
                "`char` values are commonly promoted to `int` for arithmetic, often using the character code.",
                "`sizeof array` works only while the real array type is visible. Function parameters like `int values[]` are pointers.",
                "C arrays are row-major: for `int A[rows][cols]`, offset of `A[r][c]` is `r * cols + c` integers.",
            ]
        )
    )
    story.append(p("Pointers, allocation, and strings", "h2"))
    story.append(
        bullets(
            [
                "`int *p` creates a pointer variable. It does not allocate an `int`; `p` must point at valid storage before `*p = ...`.",
                "Use `malloc(n * sizeof *p)` or `malloc(n * sizeof(int))`; `sizeof *p` follows the pointed-to type if it changes.",
                "Check `p != NULL` before writing through allocated memory. Free each allocation exactly once.",
                "A wild pointer is uninitialised. A dangling pointer used to point at valid memory, but that memory is no longer valid.",
                "`strcpy` and `strcat` receive pointers. Destination must point to writable space large enough for all characters and `\\0`.",
                "`sizeof s` measures storage bytes for an array; `strlen(s)` counts visible characters before `\\0`.",
            ]
        )
    )
    story.append(code(
        r"""
char str[] = "By Divine Aid";
char *dup, *p, *q;

for (p = str; *p; p++)
    ;
dup = malloc((size_t)(p - str + 1) * sizeof *dup);
assert(dup != NULL);
for (p = str, q = dup; *p; )
    *q++ = *p++;
*q = '\0';
"""
    ))
    story.append(p("Files, streams, and buffering", "h2"))
    story.append(
        bullets(
            [
                "`FILE *fp` is a stream handle, not the file itself. Always check `fp == NULL` after `fopen`.",
                "`scanf(\"%d\", &k)` parses input according to `%d` and writes into `k`, so it needs the address.",
                "`fgets(buf, size, fp)` reads a line or up to `size - 1` chars and writes a terminator.",
                "`fread(out, sizeof *out, 1, fp) == 1` means exactly one object was read successfully.",
                "After a read loop ends on `EOF`, call `ferror(fp)` to distinguish normal end-of-file from a real read error.",
                "`printf` writes to `stdout`, a buffered stream. To force visible output now, call `fflush(stdout)` after `printf`.",
                "`stderr` is for diagnostics/errors so normal output and error output can be redirected separately.",
            ]
        )
    )
    story.append(p("Preprocessor, headers, and build", "h2"))
    story.append(
        bullets(
            [
                "The preprocessor rewrites source before compilation: includes are copied in, macros are text-substituted.",
                "Include guards prevent one header's declarations from being processed twice in the same compilation unit.",
                "`static` on a file-scope helper makes it private to that `.c` file. `extern` declares something defined elsewhere.",
                "Macro pitfalls: precedence, repeated evaluation, and multi-statement expansion. Fully parenthesise macro arguments and result.",
                "Makefiles: first target is default, prerequisites decide rebuilds, recipes must start with a tab.",
                "Compile `.c` to `.o`; link `.o` files into an executable. Libraries are collections of object files.",
            ]
        )
    )
    story.append(code(
        r"""
#define SQUARE(X) ((X) * (X))     /* still bad for SQUARE(i++) */

#define swap(a, b) do { \
    int tmp = (a);     \
    (a) = (b);         \
    (b) = tmp;         \
} while (0)
"""
    ))
    story.append(PageBreak())


def add_cpp_section(story: list):
    story.append(p("C++: Must-Know Rules", "h1"))
    story.append(p("Classes, access, and inheritance", "h2"))
    story.append(
        bullets(
            [
                "`class` members are private by default; `struct` members are public by default.",
                "A constructor initialiser list directly initialises members and base classes: `MyInteger(int value) : i(value) {}`.",
                "`private` base members are not directly accessible in derived code. `protected` members are accessible inside derived member functions.",
                "Public inheritance means is-a. Protected/private inheritance hide the base interface from outside users.",
                "Use getters/setters or `friend` only when controlled access is needed; making fields public weakens encapsulation.",
                "Base constructors run before derived constructors. Destructors run in reverse order.",
            ]
        )
    )
    story.append(p("Virtual dispatch and ownership", "h2"))
    story.append(
        bullets(
            [
                "Without `virtual`, a call through `Sensor *` or `Sensor &` uses the base type's function.",
                "`virtual double read() const = 0;` makes `Sensor` abstract and forces derived classes to implement `read`.",
                "`override` checks the derived signature really matches the base virtual function, including `const`.",
                "Deleting through a base pointer type requires a virtual destructor: `virtual ~Sensor() = default;`.",
                "Pass `const Sensor&` when you only need to read an object owned elsewhere. Use `std::unique_ptr<Sensor>` when the pointer owns it.",
                "Object slicing happens when a derived object is copied into a base object by value; use references or pointers for polymorphism.",
            ]
        )
    )
    story.append(code(
        r"""
class Sensor {
public:
    virtual ~Sensor() = default;
    virtual double read() const = 0;
};

std::vector<std::unique_ptr<Sensor>> sensors;
sensors.push_back(std::make_unique<TemperatureSensor>(7, 21.5));
"""
    ))
    story.append(p("RAII, smart pointers, exceptions", "h2"))
    story.append(
        bullets(
            [
                "RAII = Resource Acquisition Is Initialization: acquire in constructor/object creation, release in destructor.",
                "`std::unique_ptr<T>` has exclusive ownership and cannot be copied; transfer with `std::move`.",
                "`std::shared_ptr<T>` is copyable shared ownership; object is destroyed when the last shared owner is gone.",
                "`std::weak_ptr<T>` observes a shared object without keeping it alive; call `.lock()` to try getting a `shared_ptr`.",
                "C++ exceptions propagate up the call stack until caught. Catch standard exceptions as `const std::exception&` and use `.what()`.",
                "Disadvantage of exceptions: control flow can jump to catch blocks, so paths are harder to follow.",
            ]
        )
    )
    story.append(p("Operators, templates, STL", "h2"))
    story.append(
        bullets(
            [
                "`operator[]` should return `T&` if `arr[i] = value` must modify the stored element.",
                "`operator<<` usually returns `std::ostream&` so output can chain: `std::cout << a << b`.",
                "`operator+` normally returns a new value and should often be `const`; use `+=` for mutation.",
                "Templates are patterns. `Stack` is the template name; `Stack<T>` or `Stack<int>` is a type.",
                "Template definitions usually live in headers because the compiler needs the full definition when instantiating.",
                "Use `std::map::find(key)` for keyed lookup. Ordered map lookup is logarithmic; vector search is usually linear.",
                "Algorithms take iterator ranges and predicates/comparators: `sort`, `binary_search`, `count_if`.",
            ]
        )
    )
    story.append(code(
        r"""
template<typename T>
T find_max(T a, T b) {
    return a < b ? b : a;
}

auto it = students.find(1001);
if (it != students.end()) {
    std::cout << it->second.name << "\n";
}
"""
    ))
    story.append(PageBreak())


def add_rust_section(story: list):
    story.append(p("Rust: Must-Know Rules", "h1"))
    story.append(p("Ownership, borrowing, and text", "h2"))
    story.append(
        bullets(
            [
                "Ownership rules: each value has an owner; only one owner at a time; value is dropped when owner goes out of scope.",
                "`String` owns heap text. `&str` is a borrowed string slice and is best for read-only text parameters.",
                "Passing `String` by value moves ownership. Passing `&String` or `&str` borrows so the caller can still use it.",
                "You can have many immutable references or one mutable reference, but not both active for the same value.",
                "A `Vec` push may reallocate, so Rust rejects holding a reference into a `Vec` and then mutating the `Vec` before using the reference.",
                "`&[T]` is a borrowed slice of contiguous elements. It can accept a whole vector, array, or sub-slice.",
            ]
        )
    )
    story.append(code(
        r"""
fn label_len(label: &str) -> usize {
    label.len()
}

let name = String::from("sensor");
let n = label_len(&name);
println!("{name} {n}");
"""
    ))
    story.append(p("Option, Result, and file parsing", "h2"))
    story.append(
        bullets(
            [
                "`Option<T>` is `Some(value)` or `None` for possibly missing values.",
                "`Result<T, E>` is `Ok(value)` or `Err(error)` for recoverable errors.",
                "`?` unwraps `Ok(value)` and returns `Err(error)` early from the current function.",
                "`unwrap()` panics with a generic message. `expect(\"message\")` panics with your custom explanation.",
                "`parse::<i32>()` tells Rust the target parse type. Handle the result with `match`, `?`, or `expect` only when failure is unrecoverable.",
                "`map_err` converts one error type into another. `ok_or_else` converts `Option` into `Result`.",
            ]
        )
    )
    story.append(code(
        r"""
fn parse_port(line: &str) -> Result<u16, String> {
    let (key, value) = line
        .split_once('=')
        .ok_or_else(|| "missing equals sign".to_string())?;
    if key.trim() != "port" {
        return Err("expected port key".to_string());
    }
    value.trim().parse::<u16>().map_err(|_| "bad port".to_string())
}
"""
    ))
    story.append(p("Iterators, traits, closures", "h2"))
    story.append(
        bullets(
            [
                "`.iter()` gives references. `.into_iter()` on `Vec<T>` consumes the vector and yields owned `T` values.",
                "`filter` receives a reference to each iterator item. If the item is `i32`, the filter closure sees `&i32`.",
                "`enumerate()` gives `(index, value)`. Use brackets around tuple patterns: `|(index, reading)|`.",
                "`filter_map` filters and maps in one step by returning `Some(output)` or `None`.",
                "`fold(start, |acc, item| next_acc)` must return the next accumulator value; `acc += ...` returns `()`.",
                "Trait bounds say what operations generic code may use: `T: PartialOrd + Debug`.",
                "`#[derive(Debug, PartialEq, Eq, Hash)]` asks Rust to generate common trait implementations.",
                "A closure that mutates captured state uses `FnMut` and must be bound as `mut` if called more than once.",
            ]
        )
    )
    story.append(code(
        r"""
let positives: Vec<(usize, i32)> = readings
    .into_iter()
    .enumerate()
    .filter(|(_, reading)| match reading {
        Some(value) => *value > 0,
        None => false,
    })
    .map(|(index, reading)| {
        let value = reading.unwrap();
        (index, value)
    })
    .collect();
"""
    ))
    story.append(p("Projects, testing, concurrency", "h2"))
    story.append(
        bullets(
            [
                "`src/lib.rs` holds reusable library logic. `src/main.rs` should collect input, call library functions, and print output.",
                "Items are private unless marked `pub`. Integration tests in `tests/` use the crate like outside code, so they need public API.",
                "Unit tests beside code can use `use super::*;` to access private items in the parent module.",
                "`Arc<T>` = atomically reference counted shared ownership across threads. `Rc<T>` is not thread-safe.",
                "`Mutex<T>::lock()` returns a `Result`; the guard unlocks when dropped. Poisoning reports a panic while locked.",
                "For `mpsc`, clone senders for workers, move each clone into the thread, and `drop(tx)` so receiver iteration can finish.",
            ]
        )
    )
    story.append(PageBreak())


def add_remaining_rag_quick_hits(story: list):
    story.append(p("Remaining RAG Quick Hits", "h1"))
    story.append(
        p(
            "These are lower-density topics from the tracker that still need a quick memory hook before the exam.",
            "note",
        )
    )
    story.append(p("C basics, command line, and control flow", "h2"))
    story.append(
        bullets(
            [
                "C program layout: `#include` first, then declarations/functions, then `int main(void)` or `int main(int argc, char *argv[])`.",
                "Blocks use `{ ... }`; statements usually end in semicolons; format specifiers must match values, e.g. `%d`, `%f`, `%zu`, `%s`.",
                "Escape sequences include `\\n` for newline and `\\0` for the string terminator.",
                "Automatic local variables usually live for the current block/function call; static local variables persist between calls.",
                "Command-line arguments: `argc` is the count; `argv[0]` is the program name/path; `argv[1]` is the first user argument.",
                "`atoi`/`atof` convert strings but have weak error reporting; `strtol` is better when validation matters.",
                "Control flow patterns: `if`, `for`, and `while` are common for factorials, loops, and repeated approximation tasks.",
                "Compile/link/run workflow: compile source to object files, link object files into an executable, then run the executable.",
            ]
        )
    )
    story.append(code(
        r"""
int main(int argc, char *argv[]) {
    if (argc < 2) {
        return 1;
    }
    int n = atoi(argv[1]);
    printf("%d\n", n);
    return 0;
}
"""
    ))
    story.append(p("C structs, unions, enums, and debugging tools", "h2"))
    story.append(
        bullets(
            [
                "`struct` groups fields together; use `.` for objects and `->` through pointers.",
                "`typedef struct Node { ... } Node;` lets you write `Node *root` instead of `struct Node *root`.",
                "`enum` gives named integer constants. A `union` lets fields share the same memory; only one member should be treated as active.",
                "Linked-list stack practice usually pushes and pops at the head because that is O(1).",
                "Valgrind and AddressSanitizer help catch invalid reads, invalid writes, use-after-free, leaks, and some out-of-bounds accesses.",
            ]
        )
    )
    story.append(p("C++ moving-from-C details and build tools", "h2"))
    story.append(
        bullets(
            [
                "`std::cin >> value` extracts formatted input from standard input; `std::getline` reads a full line.",
                "`auto` asks the compiler to infer a static type; it does not make a variable dynamically typed.",
                "Scope resolution `::` selects a namespace or class scope, e.g. `std::cout` or `Stack<T>::pop`.",
                "Default parameters go in the declaration, e.g. `void log(int level = 1);`.",
                "`new`/`delete` exist in C++, but prefer RAII and smart pointers. Use `nullptr` instead of `NULL` for pointer null values.",
                "CMake quick flow: write `CMakeLists.txt`; `cmake -S . -B build` configures; `cmake --build build` builds using generated build files.",
            ]
        )
    )
    story.append(code(
        r"""
cmake_minimum_required(VERSION 3.10)
project(sensor_app)
add_executable(sensor_app main.cpp sensor.cpp)
"""
    ))
    story.append(p("C++ multiple inheritance and object lifetime", "h2"))
    story.append(
        bullets(
            [
                "Multiple inheritance means one class derives from more than one base class.",
                "A diamond can create two base subobjects; `virtual public Base` makes the shared base appear once.",
                "The most-derived class constructs a virtual base directly. Destructors run in reverse construction order.",
                "Constructor/destructor trace questions usually ask which objects are built first and destroyed last.",
            ]
        )
    )
    story.append(code(
        r"""
class Left : virtual public Base {};
class Right : virtual public Base {};
class Bottom : public Left, public Right {};
"""
    ))
    story.append(p("Rust basics, control flow, and Cargo", "h2"))
    story.append(
        bullets(
            [
                "`let` creates an immutable binding; `let mut` allows reassignment/mutation; shadowing with `let` creates a new binding.",
                "`const` is a named compile-time constant. Tuples group fixed-position values; arrays have fixed length.",
                "Rust has runtime bounds checks for indexing; out-of-bounds indexing panics instead of causing C-style undefined behaviour.",
                "`if` is an expression, so both branches must produce compatible types if used as a value.",
                "`loop` can return a value with `break value`; loop labels let `break 'label` or `continue 'label` target an outer loop.",
                "Doc comments use `///` before the item they document.",
                "Cargo workflow: `cargo check` type-checks quickly, `cargo fmt` formats, `cargo clippy` lints, `cargo test` runs tests.",
            ]
        )
    )
    story.append(p("Rust data modelling and sorting", "h2"))
    story.append(
        bullets(
            [
                "A Rust `struct` names fields. An `impl` block adds methods; associated functions do not take `self`.",
                "Enums model alternatives. `Option<T>` is an enum with `Some(T)` and `None`.",
                "`match` must cover all cases. `if let Some(x) = value` is a compact way to handle one interesting case.",
                "`Vec<T>` is growable heap storage; a slice `&[T]` borrows contiguous data from a vector or array.",
                "`HashMap` lookup with `get` returns `Option<&V>`; `entry(key).or_insert(value)` gives a mutable reference for counting/accumulating.",
                "`sort_by` uses a comparator returning `Ordering`; use `partial_cmp` for floats because `NaN` makes total ordering impossible.",
            ]
        )
    )
    story.append(code(
        r"""
readings.sort_by(|a, b| {
    b.value
        .partial_cmp(&a.value)
        .unwrap_or(Ordering::Equal)
        .then_with(|| a.id.cmp(&b.id))
});
"""
    ))
    story.append(PageBreak())


def add_cross_language(story: list):
    story.append(p("Cross-Language Comparisons", "h1"))
    story.append(
        compact_table(
            ["Issue", "C", "C++", "Rust"],
            [
                [
                    "Heap ownership",
                    "`malloc`/`free`; programmer owns cleanup",
                    "RAII objects and smart pointers clean up in destructors",
                    "Owner drops value automatically; borrow checker prevents invalid use",
                ],
                [
                    "Error handling",
                    "Return codes/NULL; caller must check",
                    "Exceptions propagate to catch blocks",
                    "`Result<T, E>` makes errors explicit; `?` propagates",
                ],
                [
                    "Strings",
                    "char arrays/pointers with `\\0` terminator",
                    "`std::string`, `const std::string&`, `std::string_view`",
                    "`String` owns text; `&str` borrows text",
                ],
                [
                    "Generic code",
                    "`void *`, function pointers, macros",
                    "Templates, STL iterators, function objects/lambdas",
                    "Generics with trait bounds and iterator adapters",
                ],
                [
                    "Polymorphism",
                    "Function pointers/callbacks",
                    "Virtual functions through base refs/pointers",
                    "Traits and trait objects/generic bounds",
                ],
                [
                    "Build flow",
                    "preprocess, compile to `.o`, link; Makefiles",
                    "compile/link with `g++`; CMake for projects",
                    "`cargo check`, `cargo build`, `cargo run`, `cargo test`",
                ],
            ],
            [30, 46, 46, 48],
        )
    )
    story.append(Spacer(1, 8))
    story.append(p("Reading Files In C, C++, And Rust", "h1"))
    story.append(
        compact_table(
            ["Language", "Typical code", "What to remember"],
            [
                [
                    "C",
                    "#include <stdio.h>\nFILE *fp = fopen(\"data.txt\", \"r\");\nif (fp == NULL) { /* handle */ }\nchar line[100];\nwhile (fgets(line, sizeof line, fp) != NULL) { /* use line */ }\nif (ferror(fp)) { /* read error */ }\nfclose(fp);",
                    "`fopen` returns a stream pointer or `NULL`. `fgets` keeps the newline if it fits and writes `\\0`. After a read loop, `ferror` distinguishes read error from normal EOF.",
                ],
                [
                    "C++",
                    "#include <fstream>\n#include <string>\nstd::ifstream file(\"data.txt\");\nif (!file) { /* handle */ }\nstd::string line;\nwhile (std::getline(file, line)) { /* use line */ }",
                    "`std::ifstream` is an input file stream object. Test the stream before reading. `std::getline` reads a whole line into `std::string` and removes the newline.",
                ],
                [
                    "Rust",
                    "use std::fs;\n\nfn load(path: &str) -> Result<String, std::io::Error> {\n    let text = fs::read_to_string(path)?;\n    Ok(text)\n}",
                    "`read_to_string` returns `Result<String, io::Error>`. `?` unwraps `Ok(text)` or returns the `Err` early. Iterate with `text.lines()` for line-by-line parsing.",
                ],
            ],
            [18, 78, 74],
        )
    )
    story.append(Spacer(1, 8))
    story.append(p("Common Includes And Imports", "h1"))
    story.append(
        p(
            "Use this as a fast prompt when a question asks for code. You do not need every include every time; choose the one that matches the functions or types used.",
            "note",
        )
    )
    story.append(
        compact_table(
            ["Language", "Include/import/use", "Needed for"],
            [
                ["C", "#include <stdio.h>", "printf, scanf, fprintf, FILE, fopen, fclose, fgets, fgetc, fread, fwrite, fseek, rewind, fflush, stdout, stderr"],
                ["C", "#include <stdlib.h>", "malloc, free, qsort, exit, atoi, atof, strtol"],
                ["C", "#include <string.h>", "strlen, strcpy, strcat, strcmp, strerror, memcpy, memmove"],
                ["C", "#include <ctype.h>", "isalpha, isdigit, isalnum, ispunct, tolower, toupper"],
                ["C", "#include <errno.h>", "errno; only inspect it after a function has actually reported failure"],
                ["C", "#include <assert.h>", "assert(condition) for exam fragments/tests"],
                ["C", "#include <stddef.h>", "size_t, NULL in low-level helper code"],
                ["C", "#include <limits.h>", "INT_MAX, INT_MIN and integer limits"],
                ["C", "#include <stdbool.h>", "bool, true, false in C"],
                ["C++", "#include <iostream>", "std::cout, std::cin, std::cerr, std::ostream"],
                ["C++", "#include <string>", "std::string"],
                ["C++", "#include <vector>", "std::vector"],
                ["C++", "#include <memory>", "std::unique_ptr, std::shared_ptr, std::weak_ptr, std::make_unique, std::make_shared"],
                ["C++", "#include <algorithm>", "std::sort, std::find, std::binary_search, std::count_if"],
                ["C++", "#include <map>", "std::map"],
                ["C++", "#include <unordered_map>", "std::unordered_map"],
                ["C++", "#include <stdexcept>", "std::runtime_error, std::invalid_argument, out_of_range"],
                ["C++", "#include <utility>", "std::move, std::pair"],
                ["Rust", "use std::fs;", "fs::read_to_string and other filesystem helpers"],
                ["Rust", "use std::io::{self, Read};", "io::Error and read_to_string on File"],
                ["Rust", "use std::collections::HashMap;", "HashMap"],
                ["Rust", "use std::sync::{Arc, Mutex};", "thread-safe shared ownership and locking"],
                ["Rust", "use std::sync::mpsc;", "channels"],
                ["Rust", "use std::thread;", "thread::spawn"],
                ["Rust", "use std::cmp::Ordering;", "custom sort ordering and tie handling"],
                ["Rust", "use std::error::Error;", "Box<dyn Error> function return types"],
            ],
            [18, 45, 107],
        )
    )
    story.append(Spacer(1, 8))
    story.append(p("Final Mental Checklist", "h1"))
    story.append(
        bullets(
            [
                "If code writes through a pointer/reference, identify the actual storage being modified.",
                "If memory is allocated, identify exact byte count, failure check, owner, and matching free/drop.",
                "If a string is copied/appended, identify terminator space and destination capacity.",
                "If a C loop uses indexes, check `<` vs `<=`, length source, and whether the index changes correctly.",
                "If a C stream is used, check the return value and whether the stream may be buffered.",
                "If C++ uses base pointers/references, ask: virtual function? virtual destructor? slicing?",
                "If C++ transfers ownership, look for `std::move` and whether the old owner is left empty but valid.",
                "If Rust code fails, ask: move, borrow conflict, lifetime, missing trait bound, or semicolon return issue?",
                "If Rust iterator code is wrong, write the item type at each step before fixing the code.",
                "If an exam asks 'explain', name the rule, apply it to the code, and state the consequence.",
            ]
        )
    )
    story.append(PageBreak())


def add_rag_appendix(story: list, rag_rows: list[dict[str, str]]):
    story.append(p("RAG Topic Coverage Checklist", "h1"))
    story.append(
        p(
            "Every topic from the RAG tracker is included below. Red topics should get active recall first, then amber, then green.",
            "note",
        )
    )
    for language in ["C", "C++", "Rust"]:
        language_rows = [row for row in rag_rows if row["language"] == language]
        story.append(p(language, "h2"))
        story.append(rag_table(language_rows))
        story.append(Spacer(1, 5))
        if language != "Rust":
            story.append(PageBreak())


def build_pdf():
    rag_rows = parse_rag()
    mock_rows = parse_mock()
    xlsx_rows = parse_xlsx_rows()
    summary = priority_summary(rag_rows, mock_rows, xlsx_rows)

    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=15 * mm,
        title="ECM2433 Things To Know Before The Exam",
        author="Codex",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=page_footer)])

    story: list = []
    add_priority_pages(story, summary, mock_rows, xlsx_rows, rag_rows)
    add_personal_focus_drills(story, summary)
    add_c_section(story)
    add_cpp_section(story)
    add_rust_section(story)
    add_remaining_rag_quick_hits(story)
    add_cross_language(story)
    add_rag_appendix(story, rag_rows)

    doc.build(story)
    print(f"Wrote {OUT}")
    print(f"RAG topics: {len(rag_rows)}")
    print(f"Mock mistake entries: {len(mock_rows)}")
    print(f"Spreadsheet mistake rows: {len(xlsx_rows)}")


if __name__ == "__main__":
    build_pdf()
