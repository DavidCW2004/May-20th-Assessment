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


OUT = Path(__file__).with_name("rust-control-flow-sorting-tooling-study-pack.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TopicTitle", parent=styles["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#111827"), spaceAfter=8))
    styles.add(ParagraphStyle("TopicBody", parent=styles["Normal"], fontSize=9.0, leading=11.4, textColor=colors.HexColor("#111827"), spaceAfter=5))
    styles.add(ParagraphStyle("SourceText", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#4b5563"), spaceAfter=6))
    styles.add(ParagraphStyle("BlueHeading", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#1d4ed8"), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle("DarkHeading", parent=styles["Heading3"], fontSize=11, leading=13, textColor=colors.HexColor("#111827"), spaceBefore=6, spaceAfter=3))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.0, leading=8.4, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=6))
    return styles


def p(text, styles, style="TopicBody"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=92)


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
        title="Rust Control Flow, Sorting, and Tooling Study Pack",
    )

    story = [
        p("Rust Control Flow, Sorting, and Tooling", styles, "TopicTitle"),
        p(
            "Grounded in ECM2433 rust_01_tooling, rust_02_crash_course, rust_08_closures_iterators, and Rust worksheets on sorting practical data.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),
        p("1. Tooling: rustc, Cargo, rust-analyzer, fmt, and clippy", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">rustc</font> is the compiler. <font face=\"Courier\">cargo</font> is the build system and package manager. Cargo replaces manual Makefiles/CMake for normal Rust projects and manages building, running, testing, and dependencies.",
            styles,
        ),
        code(
            """
cargo new demo
cargo check
cargo build
cargo run
cargo test
cargo fmt
cargo clippy
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">cargo check</font> type-checks quickly without producing the final binary.",
                "<font face=\"Courier\">cargo fmt</font> formats code in standard Rust style.",
                "<font face=\"Courier\">cargo clippy</font> runs extra lints and catches common mistakes.",
                "<font face=\"Courier\">rust-analyzer</font> is the editor language server: autocomplete, inline errors, go-to-definition, and type hints.",
            ],
            styles,
        ),
        p("2. Functions, returns, and unit", styles, "DarkHeading"),
        p(
            "Rust functions use <font face=\"Courier\">fn</font>. Parameters need type annotations. Return types go after <font face=\"Courier\">-&#62;</font>. If no return type is written, the function returns unit, written <font face=\"Courier\">()</font>.",
            styles,
        ),
        code(
            """
fn double(n: i32) -> i32 {
    n * 2        // no semicolon: final expression is returned
}

fn print_value(n: i32) {
    println!("{n}"); // returns ()
}
            """,
            styles,
        ),
        p(
            "A semicolon turns an expression into a statement. That matters because a block returns its final expression.",
            styles,
        ),
        p("3. if expressions and loop control", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">if</font> is an expression, so it can produce a value. The condition must be <font face=\"Courier\">bool</font>; Rust has no C-style truthy integers.",
            styles,
        ),
        code(
            """
let label = if score >= 40 {
    "pass"
} else {
    "fail"
};
            """,
            styles,
        ),
        p(
            "Rust has <font face=\"Courier\">loop</font>, <font face=\"Courier\">while</font>, and <font face=\"Courier\">for</font>. <font face=\"Courier\">continue</font> skips to the next iteration. <font face=\"Courier\">break</font> exits a loop. A <font face=\"Courier\">loop</font> can return a value with <font face=\"Courier\">break value</font>.",
            styles,
        ),
        code(
            """
let mut n = 0;
let answer = loop {
    n += 1;
    if n == 3 {
        break n * 10;
    }
};
            """,
            styles,
        ),
        p("4. Loop labels and doc comments", styles, "DarkHeading"),
        p(
            "Loop labels let <font face=\"Courier\">break</font> or <font face=\"Courier\">continue</font> target an outer loop. Doc comments use <font face=\"Courier\">///</font> before the item they document.",
            styles,
        ),
        code(
            """
'outer: for row in 0..3 {
    for col in 0..3 {
        if row + col > 3 {
            break 'outer;
        }
    }
}

/// Returns true if the mark is a pass.
fn is_pass(mark: u32) -> bool {
    mark >= 40
}
            """,
            styles,
        ),
        p("5. Sorting practical data", styles, "DarkHeading"),
        p(
            "For basic values, <font face=\"Courier\">sort</font> is enough. For custom ordering, use <font face=\"Courier\">sort_by</font> with a closure. Integer and string values implement <font face=\"Courier\">Ord</font>, so use <font face=\"Courier\">cmp</font>. Floating-point values use <font face=\"Courier\">partial_cmp</font> because NaN means not every pair has a total ordering.",
            styles,
        ),
        code(
            """
let mut teams = vec![
    (5, "pear"),
    (5, "apple"),
    (2, "orange"),
];

teams.sort_by(|(count_a, word_a), (count_b, word_b)| {
    count_b
        .cmp(count_a)
        .then_with(|| word_a.cmp(word_b))
});
            """,
            styles,
        ),
        p(
            "This sorts by count descending, then word ascending. <font face=\"Courier\">then_with</font> only runs the tie-breaker if the first comparison is equal.",
            styles,
        ),
        p("6. Sorting floats with partial_cmp", styles, "DarkHeading"),
        code(
            """
let mut measurements = vec![
    (0.25, 2),
    (0.25, 0),
    (0.5, 1),
];

measurements.sort_by(|(value_a, id_a), (value_b, id_b)| {
    value_a
        .partial_cmp(value_b)
        .unwrap()
        .then_with(|| id_a.cmp(id_b))
});
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">partial_cmp</font> returns <font face=\"Courier\">Option&#60;Ordering&#62;</font>. In controlled worksheet data with ordinary finite floats, <font face=\"Courier\">unwrap()</font> is usually acceptable. In production code, consider how to handle NaN.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        p("Question 1 - choose the Cargo command:", styles),
        code(
            """
// You want fast compiler feedback but do not need a runnable binary yet.
            """,
            styles,
        ),
        numbered(["Give the Cargo command and explain why it fits."], styles),
        p("Question 2 - identify rust-analyzer's role:", styles),
        code(
            """
// VS Code shows inline Rust errors and type hints while you type.
            """,
            styles,
        ),
        numbered(["Name the tool normally responsible for this editor support and say what it is not responsible for."], styles, start=2),
        p("Question 3 - fix the return value:", styles),
        code(
            """
fn double(n: i32) -> i32 {
    n * 2;
}
            """,
            styles,
        ),
        numbered(["Explain why this does not return an <font face=\"Courier\">i32</font>, then fix it."], styles, start=3),
        p("Question 4 - use if as an expression:", styles),
        code(
            """
let score = 72;
let result = /* pass if score >= 40, otherwise fail */;
            """,
            styles,
        ),
        numbered(["Complete the expression so <font face=\"Courier\">result</font> is either <font face=\"Courier\">\"pass\"</font> or <font face=\"Courier\">\"fail\"</font>."], styles, start=4),
        p("Question 5 - break with a value:", styles),
        code(
            """
let mut n = 0;
let found = loop {
    n += 1;
    if n * n > 20 {
        /* return n from the loop */
    }
};
            """,
            styles,
        ),
        numbered(["Complete the missing line."], styles, start=5),
        p("Question 6 - labelled break:", styles),
        code(
            """
'outer: for row in 0..4 {
    for col in 0..4 {
        if row + col == 5 {
            /* exit both loops */
        }
    }
}
            """,
            styles,
        ),
        numbered(["Complete the statement that exits both loops."], styles, start=6),
        p("Question 7 - doc comment placement:", styles),
        code(
            """
// Add a doc comment for this function.
fn is_even(n: i32) -> bool {
    n % 2 == 0
}
            """,
            styles,
        ),
        numbered(["Write the doc comment line in the correct place."], styles, start=7),
        p("Question 8 - sort counts with a tie-breaker:", styles),
        code(
            """
let mut items = vec![
    (2, "red"),
    (5, "blue"),
    (5, "amber"),
];

/* sort by count descending, then word ascending */
            """,
            styles,
        ),
        numbered(["Write the <font face=\"Courier\">sort_by</font> call."], styles, start=8),
        p("Question 9 - sort floating-point values:", styles),
        code(
            """
let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];

/* sort by float ascending, then id ascending */
            """,
            styles,
        ),
        numbered(["Write the <font face=\"Courier\">sort_by</font> call using <font face=\"Courier\">partial_cmp</font>."], styles, start=9),
        p("Question 10 - top n after sorting:", styles),
        code(
            """
let mut scores = vec![
    (String::from("Ada"), 12),
    (String::from("Grace"), 18),
    (String::from("Linus"), 15),
];

/* return the top 2 scores, highest first */
            """,
            styles,
        ),
        numbered(["Sort the vector and produce a <font face=\"Courier\">Vec</font> containing the top two entries."], styles, start=10),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "<font face=\"Courier\">cargo check</font>. It type-checks quickly without producing the final binary.",
                "<font face=\"Courier\">rust-analyzer</font>. It provides editor/language-server support; it is not Cargo and it does not replace the compiler.",
                "The semicolon makes <font face=\"Courier\">n * 2</font> a statement, so the block returns <font face=\"Courier\">()</font>. Fix by removing the semicolon or writing <font face=\"Courier\">return n * 2;</font>.",
                "<font face=\"Courier\">let result = if score &#62;= 40 { \"pass\" } else { \"fail\" };</font>",
                "<font face=\"Courier\">break n;</font>",
                "<font face=\"Courier\">break 'outer;</font>",
                "Place <font face=\"Courier\">/// Returns true when n is even.</font> immediately before <font face=\"Courier\">fn is_even</font>.",
                "Expected pattern: <font face=\"Courier\">items.sort_by(|(count_a, word_a), (count_b, word_b)| count_b.cmp(count_a).then_with(|| word_a.cmp(word_b)));</font>",
                "Expected pattern: <font face=\"Courier\">readings.sort_by(|(value_a, id_a), (value_b, id_b)| value_a.partial_cmp(value_b).unwrap().then_with(|| id_a.cmp(id_b)));</font>",
                "Expected pattern: sort by descending score, then use <font face=\"Courier\">into_iter().take(2).collect::&#60;Vec&#60;_&#62;&#62;()</font>.",
            ],
            styles,
        ),
        p("Useful Pattern for Question 10", styles, "BlueHeading"),
        code(
            """
scores.sort_by(|(_, score_a), (_, score_b)| score_b.cmp(score_a));

let top_two: Vec<_> = scores
    .into_iter()
    .take(2)
    .collect();
            """,
            styles,
        ),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
