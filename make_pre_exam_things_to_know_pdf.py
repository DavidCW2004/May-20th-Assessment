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
                "Next 15 minutes: scan the C, C++, and Rust rule pages, especially red/amber topics.",
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
    add_c_section(story)
    add_cpp_section(story)
    add_rust_section(story)
    add_cross_language(story)
    add_rag_appendix(story, rag_rows)

    doc.build(story)
    print(f"Wrote {OUT}")
    print(f"RAG topics: {len(rag_rows)}")
    print(f"Mock mistake entries: {len(mock_rows)}")
    print(f"Spreadsheet mistake rows: {len(xlsx_rows)}")


if __name__ == "__main__":
    build_pdf()
