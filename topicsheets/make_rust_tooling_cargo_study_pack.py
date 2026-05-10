from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
)


OUT = Path(__file__).with_name("rust-tooling-cargo-study-pack.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TopicTitle", parent=styles["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#111827"), spaceAfter=8))
    styles.add(ParagraphStyle("TopicBody", parent=styles["Normal"], fontSize=9.3, leading=12, textColor=colors.HexColor("#111827"), spaceAfter=6))
    styles.add(ParagraphStyle("SourceText", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#4b5563"), spaceAfter=6))
    styles.add(ParagraphStyle("BlueHeading", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#1d4ed8"), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle("DarkHeading", parent=styles["Heading3"], fontSize=11, leading=13, textColor=colors.HexColor("#111827"), spaceBefore=6, spaceAfter=3))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.3, leading=9.0, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=7))
    return styles


def p(text, styles, style="TopicBody"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=88)


def bullets(items, styles):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=4 * mm) for item in items],
        bulletType="bullet",
        leftIndent=6 * mm,
        bulletFontName="Helvetica",
        bulletFontSize=7,
    )


def numbered(items, styles, start=1):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=5 * mm) for item in items],
        bulletType="1",
        leftIndent=7 * mm,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=8,
        start=start,
    )


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Rust Tooling and Cargo Study Pack",
    )

    story = [
        p("Rust Tooling and Cargo", styles, "TopicTitle"),
        p(
            "Based on ECM2433 rust_01_tooling slides. Covers why Rust exists, "
            "the Cargo build system, key commands, project structure, "
            "and the cargo fmt and cargo clippy quality tools.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),

        # --- Section 1: Why Rust ---
        p("1. Why Rust?", styles, "DarkHeading"),
        p(
            "Rust targets the class of bugs that are common in C and C++ programs and are "
            "difficult to detect at compile time in those languages.",
            styles,
        ),
        bullets(
            [
                "<b>Use-after-free</b>: accessing memory that has already been freed.",
                "<b>Double-free</b>: freeing the same allocation more than once.",
                "<b>Buffer overflow</b>: writing beyond the end of an allocated region.",
            ],
            styles,
        ),
        p(
            "Rust's ownership system catches most of these at compile time. "
            "Array bounds are checked at runtime (panics instead of silent corruption). "
            "Unlike a garbage-collected language, Rust achieves this without a runtime GC, "
            "so performance stays close to C and C++.",
            styles,
        ),
        p(
            "<font face=\"Courier\">rustc</font> is the Rust compiler. In normal projects you usually "
            "run it through <font face=\"Courier\">cargo</font>, which coordinates compiling, dependencies, "
            "tests, and project layout.",
            styles,
        ),

        # --- Section 2: Cargo ---
        p("2. Cargo: build system and package manager", styles, "DarkHeading"),
        p(
            "Cargo replaces the role of Makefiles, CMake, and manual dependency management "
            "in one tool. It handles compiling your code, fetching dependencies, running "
            "tests, and more.",
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">cargo new project_name</font> — create a new project.",
                "<font face=\"Courier\">cargo build</font> — compile to "
                "<font face=\"Courier\">target/debug/</font>.",
                "<font face=\"Courier\">cargo check</font> — type-check without producing "
                "a binary. Faster than build when you only want to catch errors.",
                "<font face=\"Courier\">cargo run</font> — compile (if needed) and run.",
            ],
            styles,
        ),
        code(
            """
$ cargo new hello_rust   # creates the project
$ cd hello_rust
$ cargo run              # compiles and runs src/main.rs
   Compiling hello_rust v0.1.0
    Finished dev [unoptimized + debuginfo] target(s)
    Running `target/debug/hello_rust`
Hello, world!
            """,
            styles,
        ),

        # --- Section 3: Project structure ---
        p("3. Project structure", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">cargo new</font> creates a minimal project with three "
            "important files:",
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">src/main.rs</font> — the entry point. Contains the "
                "<font face=\"Courier\">main</font> function.",
                "<font face=\"Courier\">Cargo.toml</font> — project configuration you edit: "
                "name, version, edition, and dependencies.",
                "<font face=\"Courier\">Cargo.lock</font> — auto-generated record of the "
                "exact dependency versions in use. Do not edit by hand.",
            ],
            styles,
        ),
        code(
            """
# Cargo.toml (you edit this)
[package]
name = "hello_rust"
version = "0.1.0"
edition = "2021"

[dependencies]
# add crates here
            """,
            styles,
        ),

        # --- Section 4: cargo fmt and cargo clippy ---
        p("4. Code quality: cargo fmt and cargo clippy", styles, "DarkHeading"),
        p(
            "The slides state: run both before submitting work.",
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">cargo fmt</font> — reformats your code to the "
                "standard Rust style automatically. No arguments needed.",
                "<font face=\"Courier\">cargo clippy</font> — a linter that catches "
                "mistakes and suggests improvements beyond what the compiler reports.",
            ],
            styles,
        ),
        p(
            "Example: the compiler accepts the following function, but clippy flags it "
            "as unnecessarily verbose and suggests a simpler form.",
            styles,
        ),
        code(
            """
// clippy warning: this if/else can be simplified
fn is_even(n: i32) -> bool {
    if n % 2 == 0 { true } else { false }
}

// clippy suggestion: return the boolean expression directly
fn is_even(n: i32) -> bool {
    n % 2 == 0
}
            """,
            styles,
        ),

        # --- Section 5: Offline docs and rust-analyzer ---
        p("5. Offline documentation and IDE support", styles, "DarkHeading"),
        bullets(
            [
                "<font face=\"Courier\">rustup doc</font> — opens locally installed "
                "Rust documentation in a browser.",
                "<font face=\"Courier\">rustup doc --book</font> — opens the Rust Book "
                "(the primary reference) offline.",
                "<b>rust-analyzer</b> — the Rust language server. Gives autocomplete, "
                "inline errors, go-to-definition, and type hints inside VS Code. "
                "Install the rust-analyzer extension to use it.",
            ],
            styles,
        ),

        # --- Practice Questions ---
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Name three classes of memory bug that Rust's design aims to prevent.",
                "What two roles does Cargo combine that in a C project would require "
                "separate tools?",
                "What files and directories does "
                "<font face=\"Courier\">cargo new hello_rust</font> create?",
                "What is the difference between "
                "<font face=\"Courier\">Cargo.toml</font> and "
                "<font face=\"Courier\">Cargo.lock</font>? "
                "Which one should you edit by hand?",
                "What is the difference between "
                "<font face=\"Courier\">cargo build</font> and "
                "<font face=\"Courier\">cargo check</font>? "
                "When would you prefer check over build?",
                "What does <font face=\"Courier\">cargo run</font> do if the source "
                "has not changed since the last successful build?",
                "What does <font face=\"Courier\">cargo fmt</font> do to your code?",
            ],
            styles,
        ),
        p("Question 8 — state what cargo clippy would say about this function:", styles),
        code(
            """
fn is_even(n: i32) -> bool {
    if n % 2 == 0 { true } else { false }
}
            """,
            styles,
        ),
        numbered(
            [
                "State what cargo clippy would flag in the function above and write the "
                "corrected version.",
                "How do you open the Rust Book without an internet connection?",
                "A student installs the rust-analyzer VS Code extension. "
                "Name two benefits they get while editing a Rust file.",
            ],
            styles,
            start=8,
        ),

        # --- Mark Scheme ---
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Attempt all questions before checking.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "Use-after-free, double-free, buffer overflow (any three of these).",

                "Build system (replaces Makefiles / CMake) and package manager "
                "(handles fetching and versioning dependencies).",

                "<font face=\"Courier\">src/main.rs</font> (entry point with a hello-world "
                "main function), <font face=\"Courier\">Cargo.toml</font> (project config), "
                "<font face=\"Courier\">Cargo.lock</font> (auto-generated dependency lock), "
                "and a <font face=\"Courier\">.git/</font> directory if Git is available.",

                "Cargo.toml is the human-edited project configuration: name, version, "
                "edition, and declared dependencies. "
                "Cargo.lock is auto-generated by Cargo and records the exact versions "
                "actually used — do not edit it by hand.",

                "cargo build compiles and produces a binary in target/debug/. "
                "cargo check only type-checks the code without producing a binary — "
                "it is faster and useful when you want to catch errors quickly during "
                "development without waiting for a full compile.",

                "It skips recompilation and runs the existing binary directly — "
                "Cargo detects that nothing has changed.",

                "It reformats the source files in place to match the standard Rust "
                "style conventions. It makes no logic changes.",

                "Clippy warns that the if/else returning true/false is redundant. "
                "The corrected version is: "
                "<font face=\"Courier\">fn is_even(n: i32) -> bool { n % 2 == 0 }</font>",

                "<font face=\"Courier\">rustup doc --book</font>",

                "Any two of: autocomplete, inline compiler errors as you type, "
                "go-to-definition, type hints / type inference display.",
            ],
            styles,
        ),
        p("Useful Commands", styles, "BlueHeading"),
        code(
            """
cargo new my_project     # create project
cargo build              # compile
cargo check              # type-check only (faster)
cargo run                # compile + run
cargo fmt                # auto-format code
cargo clippy             # lint and suggest improvements
rustup doc               # open local docs
rustup doc --book        # open the Rust Book offline
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
