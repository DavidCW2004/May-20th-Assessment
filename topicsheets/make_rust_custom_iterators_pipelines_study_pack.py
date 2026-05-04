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


OUT = Path(__file__).with_name("rust-custom-iterators-pipelines-study-pack.pdf")


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


def numbered(items, styles):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=5 * mm) for item in items],
        bulletType="1",
        leftIndent=7 * mm,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=8,
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
        title="Rust Custom Iterators and Pipelines Study Pack",
    )

    story = [
        p("Rust Custom Iterators and Pipelines", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: custom iterators and more involved iterator pipelines over HashMap and Vec.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Iterators are lazy", styles, "DarkHeading"),
        p(
            "Iterator adapters such as <font face=\"Courier\">map</font> and <font face=\"Courier\">filter</font> describe work, but they do not run until a consuming operation asks for values.",
            styles,
        ),
        code(
            """
let values = vec![1, 2, 3, 4];

let doubled = values.iter().map(|n| n * 2);
let total: i32 = doubled.sum();
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">map</font> creates a new iterator. <font face=\"Courier\">sum</font> consumes it and actually performs the work.",
            styles,
        ),
        p("2. <font face=\"Courier\">iter</font>, <font face=\"Courier\">iter_mut</font>, and <font face=\"Courier\">into_iter</font>", styles, "DarkHeading"),
        bullets(
            [
                "<font face=\"Courier\">iter()</font> yields shared references such as <font face=\"Courier\">&#38;T</font>.",
                "<font face=\"Courier\">iter_mut()</font> yields mutable references such as <font face=\"Courier\">&#38;mut T</font>.",
                "<font face=\"Courier\">into_iter()</font> consumes the collection and yields owned values when possible.",
            ],
            styles,
        ),
        code(
            """
let mut values = vec![1, 2, 3];

for n in values.iter() {
    println!("{n}");
}

for n in values.iter_mut() {
    *n += 1;
}

for n in values.into_iter() {
    println!("{n}");
}
            """,
            styles,
        ),
        p(
            "After <font face=\"Courier\">into_iter()</font> consumes a vector of owned values, the original vector cannot be used again.",
            styles,
        ),
        p("3. Common adapters", styles, "DarkHeading"),
        p(
            "Adapters transform an iterator into another iterator. They are usually chained before a final consuming operation.",
            styles,
        ),
        code(
            """
let values = vec![1, 2, 3, 4, 5, 6];

let result: Vec<i32> = values
    .iter()
    .filter(|n| **n % 2 == 0)
    .map(|n| n * n)
    .collect();

// result is [4, 16, 36]
            """,
            styles,
        ),
        p(
            "With <font face=\"Courier\">iter()</font>, the closure often receives references. That is why the filter example uses <font face=\"Courier\">**n</font>: the closure argument is a reference to an iterator item that is itself a reference.",
            styles,
        ),
        p("4. Useful consumers", styles, "DarkHeading"),
        bullets(
            [
                "<font face=\"Courier\">collect()</font>: builds a collection from iterator items.",
                "<font face=\"Courier\">sum()</font>: adds numeric items.",
                "<font face=\"Courier\">count()</font>: counts items.",
                "<font face=\"Courier\">any()</font>: checks whether at least one item matches.",
                "<font face=\"Courier\">all()</font>: checks whether every item matches.",
                "<font face=\"Courier\">fold()</font>: accumulates a result using a closure.",
            ],
            styles,
        ),
        code(
            """
let values = vec![1, 2, 3, 4];

let total: i32 = values.iter().sum();
let big = values.iter().any(|n| *n > 3);
let product = values.iter().fold(1, |acc, n| acc * n);
            """,
            styles,
        ),
        p("5. Pipelines over strings", styles, "DarkHeading"),
        p(
            "String and text exercises often combine splitting, normalising, filtering, and collecting.",
            styles,
        ),
        code(
            """
let text = "Rust, rust! C?";

let words: Vec<String> = text
    .split_whitespace()
    .map(|word| {
        word.trim_matches(|ch: char| !ch.is_alphanumeric())
            .to_lowercase()
    })
    .filter(|word| !word.is_empty())
    .collect();

// ["rust", "rust", "c"]
            """,
            styles,
        ),
        p(
            "Each stage does one job: split into rough words, trim punctuation, lower-case, remove empty strings, then collect.",
            styles,
        ),
        p("6. Pipelines over <font face=\"Courier\">HashMap</font>", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">HashMap</font> iterator yields key-value pairs. With <font face=\"Courier\">iter()</font>, those pairs are references.",
            styles,
        ),
        code(
            """
use std::collections::HashMap;

let mut scores = HashMap::new();
scores.insert("red", 12);
scores.insert("blue", 7);
scores.insert("green", 15);

let mut high: Vec<(&str, i32)> = scores
    .iter()
    .filter(|(_, score)| **score >= 10)
    .map(|(team, score)| (*team, *score))
    .collect();

high.sort_by_key(|(_, score)| *score);
            """,
            styles,
        ),
        p(
            "The filter closure gets references from the map iterator. The map step copies out the borrowed key and integer score so the resulting vector has simpler values.",
            styles,
        ),
        p("7. Custom iterator structure", styles, "DarkHeading"),
        p(
            "A custom iterator is a type that stores iteration state and implements the <font face=\"Courier\">Iterator</font> trait. The important method is <font face=\"Courier\">next</font>.",
            styles,
        ),
        code(
            """
struct Counter {
    current: u32,
    end: u32,
}

impl Counter {
    fn new(end: u32) -> Counter {
        Counter { current: 0, end }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current >= self.end {
            None
        } else {
            let value = self.current;
            self.current += 1;
            Some(value)
        }
    }
}
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">next</font> returns <font face=\"Courier\">Some(item)</font> while there is another value and <font face=\"Courier\">None</font> when iteration is finished.",
            styles,
        ),
        code(
            """
let values: Vec<u32> = Counter::new(4).collect();
// [0, 1, 2, 3]
            """,
            styles,
        ),
        p("8. Custom iterators still use adapters", styles, "DarkHeading"),
        p(
            "Once a type implements <font face=\"Courier\">Iterator</font>, it can use the standard iterator adapters and consumers.",
            styles,
        ),
        code(
            """
let total: u32 = Counter::new(10)
    .filter(|n| n % 2 == 0)
    .map(|n| n * n)
    .sum();
            """,
            styles,
        ),
        p(
            "This pipeline keeps even numbers from 0 to 9, squares them, then sums the squares.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Explain why <font face=\"Courier\">values.iter().map(|n| n * 2)</font> alone does not produce a vector.",
                "Choose <font face=\"Courier\">iter</font>, <font face=\"Courier\">iter_mut</font>, or <font face=\"Courier\">into_iter</font> for reading, modifying in place, and consuming a vector.",
                "Write a pipeline that keeps even numbers from a vector and collects their squares into a new vector.",
                "Use <font face=\"Courier\">fold</font> to multiply all numbers in a vector.",
                "Given a sentence, split it into words, lowercase them, and collect into <font face=\"Courier\">Vec&lt;String&gt;</font>.",
                "Given a <font face=\"Courier\">HashMap&lt;&#38;str, i32&gt;</font>, collect entries with score at least 10 into a vector.",
                "Write the struct fields needed for a simple counter iterator from 0 up to but not including an end value.",
                "Implement the <font face=\"Courier\">next</font> method for that counter iterator.",
                "Explain why <font face=\"Courier\">next</font> returns <font face=\"Courier\">Option</font>.",
                "Use your custom counter with <font face=\"Courier\">filter</font>, <font face=\"Courier\">map</font>, and <font face=\"Courier\">sum</font>.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Strong answers should distinguish adapters from consumers and ownership from borrowing.", styles, "SourceText"),
        numbered(
            [
                "<font face=\"Courier\">map</font> is lazy and returns another iterator. Use a consumer such as <font face=\"Courier\">collect</font>, <font face=\"Courier\">sum</font>, or a <font face=\"Courier\">for</font> loop to run it.",
                "Use <font face=\"Courier\">iter</font> for shared reads, <font face=\"Courier\">iter_mut</font> for in-place mutation, and <font face=\"Courier\">into_iter</font> when consuming owned values.",
                "Expected pattern: <font face=\"Courier\">values.iter().filter(|n| **n % 2 == 0).map(|n| n * n).collect::&lt;Vec&lt;_&gt;&gt;()</font>.",
                "Expected pattern: <font face=\"Courier\">values.iter().fold(1, |acc, n| acc * n)</font>.",
                "Expected stages: <font face=\"Courier\">split_whitespace</font>, <font face=\"Courier\">map</font> to lower-case or clean, then <font face=\"Courier\">collect</font>.",
                "Expected: iterate with <font face=\"Courier\">map.iter()</font>, filter by score, and collect copied or cloned key-value pairs into a vector.",
                "Expected fields include current position and end limit, such as <font face=\"Courier\">current: u32</font> and <font face=\"Courier\">end: u32</font>.",
                "Expected: return <font face=\"Courier\">None</font> when current reaches end; otherwise save current, increment it, and return <font face=\"Courier\">Some(value)</font>.",
                "<font face=\"Courier\">Option</font> represents either a next item with <font face=\"Courier\">Some</font> or finished iteration with <font face=\"Courier\">None</font>.",
                "Expected pattern: <font face=\"Courier\">Counter::new(10).filter(...).map(...).sum()</font>.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Forgetting that adapters are lazy until a consumer runs.",
                "Using <font face=\"Courier\">into_iter</font> and then trying to use the consumed vector again.",
                "Getting confused by references in <font face=\"Courier\">filter</font> closures.",
                "Returning a plain value from <font face=\"Courier\">next</font> instead of <font face=\"Courier\">Option&lt;Item&gt;</font>.",
                "Forgetting to update iterator state before returning <font face=\"Courier\">Some</font>.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
