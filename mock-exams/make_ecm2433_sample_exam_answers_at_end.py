from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer


OUT = Path(__file__).with_name("ECM2433-sample-paper-answers-at-end.pdf")


def code(text):
    return text.strip("\n")


PAPER = [
    {
        "num": 1,
        "total": 37,
        "parts": [
            {
                "label": "a",
                "marks": 8,
                "question": (
                    "A programmer uses the following macro construction to find the square of two numbers. "
                    "Using this macro, what is the result of running the code below? Explain how the macro might "
                    "be modified to yield the square of k + 1. Give an advantage and a disadvantage of this method "
                    "compared with defining an equivalent function."
                ),
                "code": [
                    code(
                        """
#define square(x) x * x

int k = 8;
printf("%d\\n", square(k + 1));
"""
                    )
                ],
                "answer": [
                    (
                        "The macro expands textually, so square(k + 1) becomes k + 1 * k + 1. "
                        "With k = 8 this evaluates as 8 + 1 * 8 + 1 = 17, not 81."
                    ),
                    code(
                        """
#define square(x) ((x) * (x))
"""
                    ),
                    (
                        "The parentheses force each argument and the whole expression to be grouped correctly. "
                        "An advantage of a macro is that there is no function call overhead. A disadvantage is that "
                        "macro arguments can have side effects because they may be evaluated more than once, for "
                        "example square(i++)."
                    ),
                ],
            },
            {
                "label": "b",
                "marks": 4,
                "question": "Give the definition of a C preprocessor macro swap(a, b) which interchanges its int arguments.",
                "answer": [
                    code(
                        """
#define swap(a, b) do { \\
    int tmp = (a);     \\
    (a) = (b);         \\
    (b) = tmp;         \\
} while (0)
"""
                    ),
                    (
                        "A simpler block macro using a temporary int also receives credit. "
                        "The temporary stores one value while the two arguments are exchanged."
                    ),
                ],
            },
            {
                "label": "c",
                "marks": 8,
                "question": (
                    "Given the declarations below, write code to allocate memory and then copy str into dup. "
                    "You may use malloc, but no other variables or functions."
                ),
                "code": [
                    code(
                        """
char str[] = "By Divine Aid";
char *dup, *p, *q;
"""
                    )
                ],
                "answer": [
                    code(
                        """
#include <assert.h>
#include <stdlib.h>

for (p = str; *p; p++)
    ;

dup = malloc((size_t)(p - str + 1) * sizeof *dup);
assert(dup != NULL);

for (p = str, q = dup; *p; )
    *q++ = *p++;

*q = '\\0';
"""
                    ),
                    (
                        "Marks are for finding the string length with pointer arithmetic, allocating space for the "
                        "terminator, checking malloc did not return NULL, copying with pointer increments, and "
                        "writing the final null terminator."
                    ),
                ],
            },
            {
                "label": "d",
                "marks": 6,
                "question": "Write a function int **alloc2d(int rows, int cols) to allocate a two-dimensional array of integers.",
                "answer": [
                    code(
                        """
#include <assert.h>
#include <stdlib.h>

int **alloc2d(int rows, int cols)
{
    int **a = malloc((size_t)rows * sizeof *a);
    assert(a != NULL);

    a[0] = malloc((size_t)rows * (size_t)cols * sizeof **a);
    assert(a[0] != NULL);

    for (int r = 1; r < rows; r++)
        a[r] = a[0] + r * cols;

    return a;
}
"""
                    ),
                    (
                        "Answers that allocate each row separately are also acceptable. Award credit for allocating "
                        "the row-pointer array, allocating rows * cols integers or separate rows, setting each row "
                        "pointer correctly, and checking allocation failure."
                    ),
                ],
            },
            {
                "label": "e",
                "marks": 5,
                "question": "Explain the difference between global and static variables in C.",
                "answer": [
                    (
                        "A global variable has global scope and can be accessed from other code where it is visible. "
                        "A static local variable has scope limited to the function in which it is declared, but it "
                        "persists between calls to that function."
                    )
                ],
            },
            {
                "label": "f",
                "marks": 6,
                "question": (
                    "A programmer writes the following code but is surprised to see no output until the program exits. "
                    "Explain why and how the result of each printf can be seen immediately."
                ),
                "code": [
                    code(
                        """
int i;
for (i = 0; i < 10; i++)
    printf("%d ", i);
sleep(10);
exit(0);
"""
                    )
                ],
                "answer": [
                    (
                        "printf writes to a buffered stream. The output may stay in stdout's buffer until the buffer "
                        "is full, a newline is written on a line-buffered terminal stream, or the program exits "
                        "normally. To force output immediately after each printf, call fflush(stdout)."
                    ),
                    code(
                        """
printf("%d ", i);
fflush(stdout);
"""
                    ),
                ],
            },
        ],
    },
    {
        "num": 2,
        "total": 20,
        "intro": "A class is defined as follows:",
        "intro_code": code(
            """
class ClockType
{
    unsigned int hours;
    unsigned int minutes;
    unsigned int seconds;

protected:
    char *maker;

public:
    unsigned int seconds_since_midnight()
    {
        return seconds + minutes * 60 + hours * 60 * 60;
    }
};
"""
        ),
        "parts": [
            {
                "label": "a",
                "marks": 4,
                "question": (
                    "Give code to derive a class, Watch, from the ClockType base class. Your Watch class should "
                    "have an additional member function printMaker that prints the maker string."
                ),
                "answer": [
                    code(
                        """
class Watch : public ClockType
{
public:
    void printMaker()
    {
        std::cout << maker << std::endl;
    }
};
"""
                    ),
                    "Marks are for public inheritance and a printMaker function that accesses maker.",
                ],
            },
            {
                "label": "b",
                "marks": 4,
                "question": "Explain why the Watch class can access the maker attribute, but not the hours, minutes and seconds variables.",
                "answer": [
                    (
                        "maker is protected, so it is accessible inside derived classes such as Watch. "
                        "hours, minutes, and seconds are private because they appear before any public or protected "
                        "access specifier, so derived classes cannot access them directly."
                    )
                ],
            },
            {
                "label": "c",
                "marks": 4,
                "question": (
                    "Why might the designer of the ClockType class prefer to make the hours, minutes and seconds "
                    "variables inaccessible to derived classes?"
                ),
                "answer": [
                    (
                        "Keeping them private hides the implementation and forces users or derived classes to work "
                        "through the public/protected interface. The implementation can then be changed later without "
                        "breaking code that uses the class."
                    )
                ],
            },
            {
                "label": "d",
                "marks": 4,
                "question": (
                    "The programmer of another class wishes to obtain and change the hours, minutes and seconds "
                    "variables. Suggest two mechanisms that could be used to accomplish this."
                ),
                "answer": [
                    (
                        "Two possible mechanisms are: provide getter and setter member functions in ClockType, or "
                        "declare selected functions/classes as friends. Making everything public receives limited credit "
                        "because it weakens encapsulation."
                    )
                ],
            },
            {
                "label": "e",
                "marks": 4,
                "question": (
                    "A further class, SmartWatch, is derived from the Watch class with access modifier public. "
                    "State the access control of each of the variables and member functions of the ClockType class "
                    "in the SmartWatch class."
                ),
                "answer": [
                    (
                        "hours, minutes, and seconds remain inaccessible because they are private in ClockType. "
                        "maker is protected and remains accessible inside Watch and SmartWatch. "
                        "seconds_since_midnight is public in ClockType, Watch, and SmartWatch."
                    )
                ],
            },
        ],
    },
    {
        "num": 3,
        "total": 19,
        "parts": [
            {
                "label": "a",
                "marks": 4,
                "question": (
                    "Consider the Rust code below. Explain why it fails to compile, then explain how Rust's approach "
                    "to memory management here differs from copying a pointer in C."
                ),
                "code": [
                    code(
                        """
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;
    println!("{}", s1);
}
"""
                    )
                ],
                "answer": [
                    (
                        "The code fails because ownership of the String is moved from s1 to s2 by let s2 = s1. "
                        "After the move, s1 is no longer valid, so println cannot use it."
                    ),
                    (
                        "In C, copying a pointer would usually create a shallow copy where both pointers refer to "
                        "the same memory. Rust enforces that a value has only one owner at a time, preventing "
                        "double frees and dangling pointers."
                    ),
                ],
            },
            {
                "label": "b",
                "marks": 6,
                "question": (
                    "Consider the Rust code below. State which assignment performs a copy and which performs a move, "
                    "explain why the program does not compile, and suggest a modification that preserves printing all four values."
                ),
                "code": [
                    code(
                        """
fn main() {
    let x: i32 = 10;
    let y = x;

    let s1 = String::from("hi");
    let s2 = s1;

    println!("{x} {y} {s1} {s2}");
}
"""
                    )
                ],
                "answer": [
                    (
                        "let y = x performs a copy because i32 implements Copy. let s2 = s1 performs a move because "
                        "String owns heap data and does not implement Copy."
                    ),
                    (
                        "The program does not compile because s1 is used after it has been moved into s2. "
                        "One fix is to clone s1 before assigning to s2."
                    ),
                    code(
                        """
let s2 = s1.clone();
"""
                    ),
                ],
            },
            {
                "label": "c",
                "marks": 9,
                "question": (
                    "In C, iterating over an array typically requires manual index management, while Rust can iterate "
                    "over references. Give two potential errors with C's manual indexing that Rust's iterator approach "
                    "prevents, state the type of x in the Rust loop, and write one iterator expression that takes a "
                    "Vec<i32> called numbers and produces a new Vec<i32> containing only the even numbers, each multiplied by 2."
                ),
                "code": [
                    code(
                        """
int arr[] = {1, 2, 3, 4, 5};
for (int i = 0; i < 5; i++) {
    printf("%d\\n", arr[i]);
}
"""
                    ),
                    code(
                        """
let arr = [1, 2, 3, 4, 5];
for x in &arr {
    println!("{}", x);
}
"""
                    ),
                ],
                "answer": [
                    (
                        "C manual indexing can cause off-by-one errors, such as using <= instead of <, and "
                        "out-of-bounds access if the hard-coded length does not match the actual array size."
                    ),
                    "In the Rust loop, x has type &i32.",
                    code(
                        """
let result: Vec<i32> = numbers
    .into_iter()
    .filter(|x| x % 2 == 0)
    .map(|x| x * 2)
    .collect();
"""
                    ),
                    "An answer using .iter() with appropriate dereferencing is also acceptable.",
                ],
            },
        ],
    },
    {
        "num": 4,
        "total": 24,
        "parts": [
            {
                "label": "a",
                "marks": 15,
                "question": (
                    "Memory management is handled differently in C, C++, and Rust. In C, give two errors that can "
                    "occur if free is used incorrectly and explain the consequences. Explain RAII in C++ and how it "
                    "helps prevent those errors. Explain how Rust's ownership system achieves memory safety without "
                    "a garbage collector, referring to the three ownership rules. Finally, identify the Rust analogues "
                    "of std::unique_ptr and std::shared_ptr and state a key difference in how Rust enforces correct usage."
                ),
                "answer": [
                    (
                        "Two C errors are double free and use-after-free. A double free can corrupt the heap allocator's "
                        "internal data structures, causing crashes or security vulnerabilities. A use-after-free happens "
                        "when memory is accessed after it has been released, giving undefined behaviour."
                    ),
                    (
                        "RAII means Resource Acquisition Is Initialization. A resource is acquired by an object and "
                        "released in that object's destructor. When the object goes out of scope, the destructor runs "
                        "automatically, helping ensure the resource is released exactly once."
                    ),
                    (
                        "Rust's ownership rules are: each value has an owner; there can only be one owner at a time; "
                        "when the owner goes out of scope, the value is dropped. The borrow checker enforces these "
                        "rules at compile time, preventing double-free and use-after-free errors."
                    ),
                    (
                        "Box<T> is analogous to std::unique_ptr for unique ownership. Rc<T> is analogous to "
                        "std::shared_ptr for reference-counted shared ownership. Rust enforces ownership and borrowing "
                        "rules through the type system at compile time, while C++ smart pointers rely more on runtime "
                        "mechanisms and programmer discipline."
                    ),
                ],
            },
            {
                "label": "b",
                "marks": 9,
                "question": (
                    "Error handling is approached differently in C, C++, and Rust. Give two disadvantages of C's "
                    "return-code approach, give one advantage and one disadvantage of C++ exceptions, and explain how "
                    "Rust's Result<T, E> and ? operator combine explicit error types with concise propagation."
                ),
                "code": [
                    code(
                        """
FILE *f = fopen("data.txt", "r");
if (f == NULL) {
    /* handle error */
}
"""
                    ),
                    code(
                        """
use std::fs::File;
use std::io::{self, Read};

fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
"""
                    ),
                ],
                "answer": [
                    (
                        "Two disadvantages of C return codes are that the programmer can forget to check them, and "
                        "the same return type often has to represent both successful values and error indicators. "
                        "Error information can also be limited."
                    ),
                    (
                        "An advantage of C++ exceptions is that errors cannot be silently ignored if they are not caught; "
                        "they propagate up the call stack. A disadvantage is that exceptions can make control flow harder "
                        "to follow and require care with exception safety."
                    ),
                    (
                        "Rust makes recoverable errors explicit in the function return type with Result<T, E>. The ? "
                        "operator unwraps Ok values and returns Err values early from the current function. This gives "
                        "concise propagation like exceptions, but the possible error path remains visible in the type system."
                    ),
                ],
            },
        ],
    },
]


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            alignment=1,
            spaceAfter=8,
        ),
        "front": ParagraphStyle(
            "Front",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            alignment=1,
            spaceAfter=3,
        ),
        "heading": ParagraphStyle(
            "Heading",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=11.2,
            spaceAfter=4,
        ),
        "question": ParagraphStyle(
            "Question",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=11.5,
            spaceBefore=5,
            spaceAfter=3,
        ),
        "bold": ParagraphStyle(
            "Bold",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.7,
            leading=11.2,
            spaceBefore=2,
            spaceAfter=5,
        ),
        "label": ParagraphStyle(
            "Label",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            spaceAfter=1,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.0,
            leading=8.4,
            backColor=colors.whitesmoke,
            borderPadding=3,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=1,
            spaceAfter=5,
        ),
    }


def p(text, style):
    return Paragraph(escape(text), style)


def labelled(label, text, style):
    return Paragraph(f"<b>({label})</b> {escape(text)}", style)


def add_code(story, text, styles):
    story.append(Preformatted(text, styles["code"]))


def add_front_page(story, styles):
    story.append(Paragraph("ECM2433 Sample Paper", styles["title"]))
    story.append(p("The C Family", styles["front"]))
    story.append(p("On Campus Exam", styles["front"]))
    story.append(p("Closed Book", styles["front"]))
    story.append(p("Additional Materials: None", styles["front"]))
    story.append(p("Permitted Materials: No Calculators Permitted", styles["front"]))
    story.append(Spacer(1, 5))
    for line in [
        "Guidelines:",
        "The duration of this paper is 2hr 00.",
        "Word Count: No Word Count.",
        "Write all answers in the answer booklet provided.",
        "Do not open the exam paper until instructed by the Invigilator.",
        "Use only black pen or pencil.",
        "Mobile and electronic devices are not allowed.",
        "Do not communicate with other candidates during the exam.",
        "Exam Instructions: Answer ALL questions.",
        "This version has the questions first and the skeleton answers at the end.",
    ]:
        story.append(p(line, styles["front"]))
    story.append(Spacer(1, 8))


def add_question_section(story, styles):
    add_front_page(story, styles)
    for question in PAPER:
        story.append(p(f"Question {question['num']}", styles["heading"]))
        if question.get("intro"):
            story.append(p(question["intro"], styles["body"]))
        if question.get("intro_code"):
            add_code(story, question["intro_code"], styles)
        for part in question["parts"]:
            story.append(labelled(part["label"], f"{part['question']} ({part['marks']} marks)", styles["question"]))
            for block in part.get("code", []):
                add_code(story, block, styles)
        story.append(p(f"(Total {question['total']} marks)", styles["bold"]))


def add_answer_section(story, styles):
    story.append(PageBreak())
    story.append(p("Answers and marking notes", styles["heading"]))
    story.append(p("Equivalent correct code and reasoning should receive credit.", styles["body"]))

    for question in PAPER:
        story.append(p(f"Question {question['num']}", styles["heading"]))
        if question.get("intro_code"):
            story.append(p("Shared code from question:", styles["label"]))
            add_code(story, question["intro_code"], styles)
        for part in question["parts"]:
            story.append(
                labelled(
                    part["label"],
                    f"Question ({part['marks']} marks): {part['question']}",
                    styles["question"],
                )
            )
            for block in part.get("code", []):
                story.append(p("Code from question:", styles["label"]))
                add_code(story, block, styles)
            for item in part["answer"]:
                if "\n" in item:
                    add_code(story, item, styles)
                else:
                    story.append(Paragraph(f"<b>Answer:</b> {escape(item)}", styles["body"]))


def main():
    styles = make_styles()
    story = []
    add_question_section(story, styles)
    add_answer_section(story, styles)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
