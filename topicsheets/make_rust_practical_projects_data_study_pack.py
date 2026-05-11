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


OUT = Path(__file__).with_name("rust-practical-projects-data-study-pack.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TopicTitle", parent=styles["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#111827"), spaceAfter=8))
    styles.add(ParagraphStyle("TopicBody", parent=styles["Normal"], fontSize=9.1, leading=11.6, textColor=colors.HexColor("#111827"), spaceAfter=5))
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
        title="Rust Practical Projects and Data Study Pack",
    )

    story = [
        p("Rust Practical Projects and Data", styles, "TopicTitle"),
        p(
            "Grounded in ECM2433 Rust project-structure, testing, slices/strings/data, "
            "HashMap, command-line parsing, and practical worksheet data-file material.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),

        p("1. Project structure: lib.rs, main.rs, crate names, and pub", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">src/lib.rs</font> is the library crate: put reusable "
            "logic here so it can be called from <font face=\"Courier\">main.rs</font> and "
            "tested. <font face=\"Courier\">src/main.rs</font> is the binary crate: it is "
            "the program entry point and contains <font face=\"Courier\">fn main()</font>. "
            "A good main usually collects input, calls library functions, then prints output.",
            styles,
        ),
        p(
            "The crate name used in <font face=\"Courier\">use</font> normally comes from "
            "the <font face=\"Courier\">[package] name</font> in "
            "<font face=\"Courier\">Cargo.toml</font>. Items are private by default. Mark "
            "functions, structs, fields, or modules with <font face=\"Courier\">pub</font> "
            "when code outside that module needs to use them.",
            styles,
        ),
        code(
            """
my_project/
  Cargo.toml          # [package] name = "my_project"
  src/
    lib.rs            # reusable library logic
    main.rs           # binary entry point
  tests/
    cli_tests.rs      # integration tests
            """,
            styles,
        ),
        code(
            """
/* src/lib.rs */
pub struct Item {
    pub name: String,
    pub quantity: u32,
    pub unit_price: f64,
}

pub fn line_total(item: &Item) -> f64 {
    item.quantity as f64 * item.unit_price
}

fn round_money(value: f64) -> f64 {
    (value * 100.0).round() / 100.0
}

/* src/main.rs */
use my_project::{line_total, Item};

fn main() {
    let item = Item {
        name: String::from("tea"),
        quantity: 3,
        unit_price: 1.25,
    };
    println!("{}", line_total(&item));
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">line_total</font> is public, so "
                "<font face=\"Courier\">main.rs</font> and integration tests can call it.",
                "<font face=\"Courier\">round_money</font> is private, so it can still be "
                "tested by unit tests inside <font face=\"Courier\">lib.rs</font>, but not "
                "called from <font face=\"Courier\">tests/</font>.",
                "<font face=\"Courier\">use</font> imports a path into scope. It does not "
                "copy text like C's <font face=\"Courier\">#include</font>.",
            ],
            styles,
        ),

        p("2. Unit tests and integration tests", styles, "DarkHeading"),
        p(
            "Unit tests usually sit beside the code in the same file. The usual shape is "
            "<font face=\"Courier\">#[cfg(test)] mod tests</font>. Inside that module, "
            "<font face=\"Courier\">use super::*;</font> imports the parent module, so unit "
            "tests can access private helpers.",
            styles,
        ),
        p(
            "Integration tests live in <font face=\"Courier\">tests/</font>. Each file there "
            "is compiled as a separate crate, like outside code using your library. That means "
            "integration tests can only use public API; they cannot use "
            "<font face=\"Courier\">super</font> to reach private helpers.",
            styles,
        ),
        code(
            """
/* src/lib.rs */
pub fn double(n: i32) -> i32 {
    hidden_double(n)
}

fn hidden_double(n: i32) -> i32 {
    n * 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn private_helper_works() {
        assert_eq!(hidden_double(4), 8);
    }
}

/* tests/basic.rs */
use my_project::double;

#[test]
fn public_api_works() {
    assert_eq!(double(4), 8);
}
            """,
            styles,
        ),
        p(
            "Tests can also return <font face=\"Courier\">Result</font>. That lets the test "
            "use <font face=\"Courier\">?</font> instead of <font face=\"Courier\">unwrap</font>.",
            styles,
        ),
        code(
            """
#[test]
fn parses_number() -> Result<(), std::num::ParseIntError> {
    let n: i32 = "42".parse()?;
    assert_eq!(n, 42);
    Ok(())
}
            """,
            styles,
        ),

        p("3. Command-line arguments and parsing", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">std::env::args()</font> gives command-line arguments as "
            "<font face=\"Courier\">String</font> values. They are text first, even if they "
            "look like numbers. Convert them with <font face=\"Courier\">parse</font>, then "
            "handle the <font face=\"Courier\">Result</font> with "
            "<font face=\"Courier\">match</font>, <font face=\"Courier\">expect</font>, or "
            "<font face=\"Courier\">?</font>.",
            styles,
        ),
        code(
            """
/* cargo run -- 12 2.5 */
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let program = &args[0];  // target/debug/my_project or similar
    let count_text = &args[1];  // "12"
    let scale_text = &args[2];  // "2.5"

    let count: i32 = match count_text.parse() {
        Ok(n) => n,
        Err(_) => {
            eprintln!("usage: {program} count scale");
            return;
        }
    };

    let scale: f64 = scale_text.parse().expect("scale must be a number");
    println!("{}", count as f64 * scale);
}
            """,
            styles,
        ),
        p(
            "A cleaner practical pattern is to put parsing in a library function that returns "
            "<font face=\"Courier\">Result</font>, then keep <font face=\"Courier\">main</font> "
            "as a small caller.",
            styles,
        ),
        code(
            """
/* src/lib.rs */
pub fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = text.trim().parse::<i32>()?;
    Ok(n)
}

/* src/main.rs */
fn main() {
    let arg = std::env::args().nth(1).expect("missing count");
    let count = my_project::parse_count(&arg).expect("bad count");
    println!("{count}");
}
            """,
            styles,
        ),

        p("4. Reading data files and parsing records", styles, "DarkHeading"),
        p(
            "Practical projects often read text files with "
            "<font face=\"Courier\">std::fs::read_to_string</font>. That gives one "
            "<font face=\"Courier\">String</font>. Then split it into lines, parse each line, "
            "and store structured data in a <font face=\"Courier\">struct</font>.",
            styles,
        ),
        code(
            """
#[derive(Debug, Clone)]
pub struct Item {
    pub name: String,
    pub quantity: u32,
    pub unit_price: f64,
}

pub fn parse_item(line: &str) -> Result<Item, String> {
    let parts: Vec<&str> = line.split(',').collect();
    if parts.len() != 3 {
        return Err("expected name,quantity,unit_price".to_string());
    }

    let quantity = parts[1]
        .trim()
        .parse::<u32>()
        .map_err(|_| "bad quantity".to_string())?;

    let unit_price = parts[2]
        .trim()
        .parse::<f64>()
        .map_err(|_| "bad price".to_string())?;

    Ok(Item {
        name: parts[0].trim().to_string(),
        quantity,
        unit_price,
    })
}
            """,
            styles,
        ),
        code(
            """
pub fn load_items(path: &str) -> Result<Vec<Item>, String> {
    let text = std::fs::read_to_string(path)
        .map_err(|err| err.to_string())?;

    let mut items = Vec::new();
    for line in text.lines() {
        if !line.trim().is_empty() {
            items.push(parse_item(line)?);
        }
    }
    Ok(items)
}
            """,
            styles,
        ),

        p("5. HashMap aggregation", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">HashMap&#60;K, V&#62;</font> stores key-value data. "
            "Use <font face=\"Courier\">get</font> when looking up a value: it returns "
            "<font face=\"Courier\">Option</font> because the key might not exist. Use "
            "<font face=\"Courier\">entry(...).or_insert(...)</font> when counting or "
            "accumulating because it handles the missing-key case and gives a mutable value.",
            styles,
        ),
        code(
            """
use std::collections::HashMap;

pub fn print_score(scores: &HashMap<String, u32>, team: &str) {
    match scores.get(team) {
        Some(score) => println!("{team}: {score}"),
        None => println!("{team} has no score"),
    }
}

pub fn count_words(words: &[&str]) -> HashMap<String, u32> {
    let mut counts = HashMap::new();

    for word in words {
        let key = word.to_lowercase();
        *counts.entry(key).or_insert(0) += 1;
    }

    counts
}

pub fn total_by_name(items: &[Item]) -> HashMap<String, f64> {
    let mut totals = HashMap::new();

    for item in items {
        let total = item.quantity as f64 * item.unit_price;
        *totals.entry(item.name.clone()).or_insert(0.0) += total;
    }

    totals
}
            """,
            styles,
        ),
        p(
            "The star in <font face=\"Courier\">*map.entry(...).or_insert(...)</font> is "
            "there because <font face=\"Courier\">or_insert</font> returns a mutable reference "
            "to the value in the map. Dereferencing lets you update the stored value.",
            styles,
        ),

        p("6. Slices, iterators, enumerate, and chunks", styles, "DarkHeading"),
        p(
            "Use slices when a function only needs to read a sequence. "
            "<font face=\"Courier\">&#38;[T]</font> borrows a view of contiguous data, so the "
            "same function can accept a whole <font face=\"Courier\">Vec&#60;T&#62;</font>, "
            "an array slice, or a chunk. Iterating with "
            "<font face=\"Courier\">enumerate</font> gives both the index and a borrowed value.",
            styles,
        ),
        code(
            """
pub fn first_greater_than(values: &[i32], threshold: i32) -> Option<usize> {
    for (index, value) in values.iter().enumerate() {
        if *value > threshold {
            return Some(index);
        }
    }
    None
}

pub fn batch_totals(values: &[i32], chunk_size: usize) -> Vec<i32> {
    values
        .chunks(chunk_size)
        .map(|chunk| chunk.iter().sum())
        .collect()
}
            """,
            styles,
        ),

        p("Practice Questions", styles, "BlueHeading"),
        p("Question 1 - fix the project visibility:", styles),
        code(
            """
/* src/lib.rs */
fn triple(n: i32) -> i32 { n * 3 }

/* src/main.rs */
use calc::triple;

fn main() {
    println!("{}", triple(4));
}
            """,
            styles,
        ),
        numbered(["Explain why this fails, then fix the library function."], styles),

        p("Question 2 - write the unit test:", styles),
        code(
            """
pub fn square(n: i32) -> i32 { n * n }

/* write the test module here */
            """,
            styles,
        ),
        numbered(["Write a unit test module that checks <font face=\"Courier\">square(5)</font>."], styles, start=2),

        p("Question 3 - integration test access:", styles),
        code(
            """
/* src/lib.rs */
fn helper(n: i32) -> i32 { n + 1 }
pub fn public_api(n: i32) -> i32 { helper(n) }

/* tests/basic.rs */
use calc::helper;
            """,
            styles,
        ),
        numbered(["Explain why the integration test cannot import <font face=\"Courier\">helper</font>, then give the normal fix."], styles, start=3),

        numbered(
            [
                "For <font face=\"Courier\">cargo run -- 12 2.5</font>, say what usually appears in <font face=\"Courier\">args[0]</font>, <font face=\"Courier\">args[1]</font>, and <font face=\"Courier\">args[2]</font>.",
            ],
            styles,
            start=4,
        ),

        p("Question 5 - replace the unsafe parse:", styles),
        code(
            """
let count: i32 = args[1].parse().unwrap();
            """,
            styles,
        ),
        numbered(["Rewrite this with <font face=\"Courier\">match</font> so invalid input prints an error and returns."], styles, start=5),

        p("Question 6 - complete the parsing helper:", styles),
        code(
            """
pub fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = /* parse text as i32 using ? */;
    Ok(n)
}
            """,
            styles,
        ),
        numbered(["Complete the missing expression."], styles, start=6),

        p("Question 7 - complete the HashMap counter update:", styles),
        code(
            """
use std::collections::HashMap;

let mut counts: HashMap<String, u32> = HashMap::new();
let name = String::from("Ada");

/* increment the count for name */
            """,
            styles,
        ),
        numbered(["Write the <font face=\"Courier\">entry</font> API line that increments the count for <font face=\"Courier\">name</font>."], styles, start=7),

        p("Question 8 - complete the accumulating totals update:", styles),
        code(
            """
struct Item {
    name: String,
    quantity: u32,
    unit_price: f64,
}

let mut totals: HashMap<String, f64> = HashMap::new();
let item = Item {
    name: String::from("tea"),
    quantity: 3,
    unit_price: 1.25,
};

/* add this line total to any existing total for the same product name */
            """,
            styles,
        ),
        numbered(["Write the update line so repeated items with the same name are accumulated, not replaced or ignored."], styles, start=8),

        p("Question 9 - write the slice scan:", styles),
        code(
            """
pub fn first_greater_than(values: &[i32], threshold: i32) -> Option<usize> {
    /* complete this */
}
            """,
            styles,
        ),
        numbered(["Complete the function so it returns the index of the first value greater than the threshold, or <font face=\"Courier\">None</font>."], styles, start=9),

        p("Question 10 - destructuring and references:", styles),
        code(
            """
let rows = vec![
    (String::from("red"), 10),
    (String::from("blue"), 7),
];

for (name, score) in rows.iter() {
    println!("{name}: {score}");
}
            """,
            styles,
        ),
        numbered(["Explain what <font face=\"Courier\">(name, score)</font> does here and why <font face=\"Courier\">score</font> is a reference."], styles, start=10),

        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "Functions are private by default. Fix: <font face=\"Courier\">pub fn triple(n: i32) -&#62; i32 { n * 3 }</font>.",
                "Expected shape: <font face=\"Courier\">#[cfg(test)] mod tests { use super::*; #[test] fn square_works() { assert_eq!(square(5), 25); } }</font>.",
                "Integration tests are separate crates and can only use public API. Normal fixes: test through <font face=\"Courier\">public_api</font>, or make the helper public if it is genuinely part of the public API.",
                "<font face=\"Courier\">args[0]</font> is the program path/name. <font face=\"Courier\">args[1]</font> is <font face=\"Courier\">12</font>. <font face=\"Courier\">args[2]</font> is <font face=\"Courier\">2.5</font>. They are all strings.",
                "Expected pattern: <font face=\"Courier\">let count: i32 = match args[1].parse() { Ok(n) =&#62; n, Err(_) =&#62; { eprintln!(\"invalid count\"); return; } };</font>",
                "<font face=\"Courier\">let n = text.trim().parse::&#60;i32&#62;()?;</font>. The function returns <font face=\"Courier\">Result</font>, so <font face=\"Courier\">?</font> can return parse errors early.",
                "<font face=\"Courier\">*counts.entry(name).or_insert(0) += 1;</font>",
                "<font face=\"Courier\">*totals.entry(item.name.clone()).or_insert(0.0) += item.quantity as f64 * item.unit_price;</font>. The starting value is 0.0 only for a missing key; existing totals are increased.",
                "Loop with <font face=\"Courier\">values.iter().enumerate()</font>. If <font face=\"Courier\">*value &#62; threshold</font>, return <font face=\"Courier\">Some(index)</font>. After the loop, return <font face=\"Courier\">None</font>.",
                "Tuple destructuring splits each pair into its two parts. Because <font face=\"Courier\">rows.iter()</font> borrows rows, <font face=\"Courier\">name</font> and <font face=\"Courier\">score</font> are references to the tuple fields rather than owned values.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
/* Unit test */
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn works() {
        assert_eq!(double(4), 8);
    }
}

/* Integration test: tests/basic.rs */
use my_project::double;

#[test]
fn public_api_works() {
    assert_eq!(double(4), 8);
}

/* Parse with match */
let n: i32 = match text.parse() {
    Ok(value) => value,
    Err(_) => {
        eprintln!("invalid number");
        return;
    }
};

/* HashMap counting */
*counts.entry(key).or_insert(0) += 1;

/* Slice scan */
for (index, value) in values.iter().enumerate() {
    if *value > threshold {
        return Some(index);
    }
}
None
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
