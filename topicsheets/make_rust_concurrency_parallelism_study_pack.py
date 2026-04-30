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


OUT = Path(__file__).with_name("rust-concurrency-parallelism-study-pack.pdf")


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
        title="Rust Concurrency and Parallelism Study Pack",
    )

    story = [
        p("Rust Concurrency and Parallelism", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: spawned threads, move closures, joining, channels, Arc, Mutex, poisoned mutexes, and parallel aggregation.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Spawning and joining threads", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">std::thread::spawn</font> starts a new thread and returns a <font face=\"Courier\">JoinHandle</font>. Calling <font face=\"Courier\">join</font> waits for the thread to finish.",
            styles,
        ),
        code(
            """
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        println!("work on another thread");
    });

    println!("work on the main thread");
    handle.join().unwrap();
}
            """,
            styles,
        ),
        p(
            "If you drop the handle and the program exits, the spawned thread may not finish. Store handles and join them when the result matters.",
            styles,
        ),
        p("2. Why <font face=\"Courier\">move</font> closures appear", styles, "DarkHeading"),
        p(
            "A spawned thread may outlive the function that created it. Rust therefore often requires the closure to own the values it uses. The <font face=\"Courier\">move</font> keyword moves captured values into the closure.",
            styles,
        ),
        code(
            """
use std::thread;

fn main() {
    let text = String::from("hello");

    let handle = thread::spawn(move || {
        println!("{text}");
    });

    handle.join().unwrap();
}
            """,
            styles,
        ),
        p(
            "After the move, the original variable cannot be used in the parent thread unless it was copied or cloned before spawning.",
            styles,
        ),
        p("3. Returning values from threads", styles, "DarkHeading"),
        p(
            "The closure passed to <font face=\"Courier\">spawn</font> can return a value. <font face=\"Courier\">join</font> gives a <font face=\"Courier\">Result</font>; unwrap it or match it to get the returned value.",
            styles,
        ),
        code(
            """
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        let values = vec![1, 2, 3, 4];
        values.iter().sum::<i32>()
    });

    let total = handle.join().unwrap();
    println!("{total}");
}
            """,
            styles,
        ),
        p(
            "The result is wrapped because a thread can panic. A robust answer can use <font face=\"Courier\">match handle.join()</font> instead of <font face=\"Courier\">unwrap</font>.",
            styles,
        ),
        p("4. Message passing with channels", styles, "DarkHeading"),
        p(
            "Channels let threads communicate by sending values. <font face=\"Courier\">mpsc</font> means multiple producer, single consumer.",
            styles,
        ),
        code(
            """
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        tx.send(42).unwrap();
    });

    let value = rx.recv().unwrap();
    println!("{value}");
}
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">send</font> moves the value into the channel. <font face=\"Courier\">recv</font> blocks until a value is available or all senders are gone.",
            styles,
        ),
        p("5. Multiple senders need cloned transmitters", styles, "DarkHeading"),
        p(
            "To send from several worker threads, clone the transmitter. Each clone is moved into one worker.",
            styles,
        ),
        code(
            """
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    for worker_id in 0..4 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(worker_id * 10).unwrap();
        });
    }

    drop(tx);

    for value in rx {
        println!("{value}");
    }
}
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">drop(tx)</font> closes the original sender. Then the receiver loop ends once all worker-owned senders are dropped.",
            styles,
        ),
        p("6. Shared ownership with <font face=\"Courier\">Arc&lt;T&gt;</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">Rc&lt;T&gt;</font> is not thread-safe. Use <font face=\"Courier\">Arc&lt;T&gt;</font> when several threads need shared ownership of the same read-only data.",
            styles,
        ),
        code(
            """
use std::sync::Arc;
use std::thread;

fn main() {
    let words = Arc::new(vec!["red", "green", "blue"]);
    let mut handles = Vec::new();

    for index in 0..3 {
        let words = Arc::clone(&words);
        handles.push(thread::spawn(move || {
            println!("{}", words[index]);
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">Arc::clone</font> clones the pointer and increments the reference count. It does not clone the whole vector.",
            styles,
        ),
        p("7. Shared mutation with <font face=\"Courier\">Arc&lt;Mutex&lt;T&gt;&gt;</font>", styles, "DarkHeading"),
        p(
            "If multiple threads must mutate shared state, wrap the data in <font face=\"Courier\">Mutex</font> and share that mutex with <font face=\"Courier\">Arc</font>.",
            styles,
        ),
        code(
            """
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();

    for _ in 0..4 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut value = counter.lock().unwrap();
            *value += 1;
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("{}", *counter.lock().unwrap());
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">Arc</font> gives shared ownership across threads.",
                "<font face=\"Courier\">Mutex</font> ensures only one thread mutates the value at a time.",
                "<font face=\"Courier\">lock()</font> returns a guard; the lock is released when the guard is dropped.",
            ],
            styles,
        ),
        p("8. Poisoned mutexes", styles, "DarkHeading"),
        p(
            "A mutex becomes poisoned if a thread panics while holding the lock. <font face=\"Courier\">lock()</font> then returns <font face=\"Courier\">Err</font> to warn that the protected data may be inconsistent.",
            styles,
        ),
        code(
            """
match counter.lock() {
    Ok(mut value) => {
        *value += 1;
    }
    Err(poisoned) => {
        let mut value = poisoned.into_inner();
        *value += 1;  // recover only if this is valid for your data
    }
}
            """,
            styles,
        ),
        p(
            "For simple counters, recovering may be acceptable. For complex state, the safer answer may be to report the error instead of continuing.",
            styles,
        ),
        p("9. Parallel aggregation pattern", styles, "DarkHeading"),
        p(
            "A good pattern is to let each thread compute a local result, then combine the results after joining. This avoids unnecessary shared mutation.",
            styles,
        ),
        code(
            """
use std::thread;

fn main() {
    let data = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let mut handles = Vec::new();

    for chunk in data.chunks(2) {
        let owned_chunk = chunk.to_vec();
        handles.push(thread::spawn(move || {
            owned_chunk.iter().sum::<i32>()
        }));
    }

    let mut total = 0;
    for handle in handles {
        total += handle.join().unwrap();
    }

    println!("{total}");
}
            """,
            styles,
        ),
        p(
            "This is the same idea used in word frequencies, Monte Carlo estimates, league tables, and text-model tasks: split work, compute local results, join, then merge.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write a minimal <font face=\"Courier\">thread::spawn</font> example and show where <font face=\"Courier\">join</font> belongs.",
                "Why does a spawned thread often need a <font face=\"Courier\">move</font> closure?",
                "What happens to a <font face=\"Courier\">String</font> in the parent thread after it is moved into a spawned closure?",
                "Write code where a spawned thread returns the sum of a vector and the main thread receives it through <font face=\"Courier\">join</font>.",
                "In an <font face=\"Courier\">mpsc</font> channel, which side sends and which side receives?",
                "Why do multiple worker threads need cloned transmitters?",
                "Why use <font face=\"Courier\">Arc&lt;T&gt;</font> instead of <font face=\"Courier\">Rc&lt;T&gt;</font> across threads?",
                "Explain why <font face=\"Courier\">Arc&lt;Mutex&lt;i32&gt;&gt;</font> is a common shared counter type.",
                "What does it mean for a mutex to be poisoned?",
                "For a parallel word-count style task, explain why local results plus a final merge is often better than every thread locking one global map for every word.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Strong answers mention ownership, waiting for threads, and controlled sharing.", styles, "SourceText"),
        numbered(
            [
                "Expected: store the handle returned by <font face=\"Courier\">thread::spawn</font>, then call <font face=\"Courier\">handle.join()</font> before the program needs the thread's result or before exit.",
                "The spawned thread may outlive the current stack frame. <font face=\"Courier\">move</font> transfers captured values into the closure so the thread owns what it uses.",
                "The parent can no longer use that <font face=\"Courier\">String</font> unless it cloned it first, because ownership moved into the closure.",
                "Expected pattern: <font face=\"Courier\">let handle = thread::spawn(move || values.iter().sum::&lt;i32&gt;()); let total = handle.join().unwrap();</font>.",
                "<font face=\"Courier\">tx</font> is the transmitter used to send values. <font face=\"Courier\">rx</font> is the receiver used to receive them.",
                "Each thread needs its own owned transmitter to move into its closure. Cloning the transmitter creates another handle to the same channel.",
                "<font face=\"Courier\">Rc</font> is not thread-safe. <font face=\"Courier\">Arc</font> uses atomic reference counting and is designed for shared ownership across threads.",
                "<font face=\"Courier\">Arc</font> lets several threads own the same counter, and <font face=\"Courier\">Mutex</font> makes each update exclusive.",
                "It means a thread panicked while holding the lock, so later <font face=\"Courier\">lock()</font> calls return an error warning that the state may be inconsistent.",
                "Local results reduce locking, avoid contention, and are easier to reason about. The final merge combines complete partial results once each worker has finished.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Spawning threads but never joining them before the program exits.",
                "Trying to borrow a local variable into a thread that may outlive that local variable.",
                "Using <font face=\"Courier\">Rc</font> where cross-thread sharing requires <font face=\"Courier\">Arc</font>.",
                "Trying to mutate through <font face=\"Courier\">Arc&lt;T&gt;</font> without a <font face=\"Courier\">Mutex</font> or another interior-mutability tool.",
                "Holding a mutex lock while doing slow work that could have been done outside the critical section.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
