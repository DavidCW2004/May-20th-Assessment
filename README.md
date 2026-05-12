# Revision Content Notes

- Do not put HTML/XML escaped ampersand entities in human-facing revision text for xlxs.
- In spreadsheet content, avoid raw ampersand syntax where a viewer might expose XML escapes; prefer wording such as "borrowed string slice", "borrow `text`", or "address of `k`".
- In ReportLab paragraph markup, use numeric character entities for required ampersand symbols inside code examples.
- Before regenerating outputs, scan source text for escaped ampersand entities and preserve existing `Completed` marks in `revision-mistake-log.xlsx`.
- Before regenerating `revision-mistake-log.xlsx`, explicitly inspect the current spreadsheet's `Completed` column and carry every existing `Yes` value into the regenerated workbook. If the user has just marked rows complete, make sure those rows are also represented as `Yes` after regeneration.
- Revision questions should test active recall and problem-solving. Do not write questions that tell the user exactly what to include, and do not use prompts that only ask the user to restate or parrot a rule back.
- For mistake-log redo prompts, ask the user to apply the missed idea to a small concrete example instead of listing the missing phrases from the mark scheme.
- When adding new mistake-log rows, append them to the end of the spreadsheet instead of inserting them into the middle of older rows.

## Topic Sheet Notes

- Topic sheet content must be grounded in the actual course slides and worksheets in `slides/` and `worksheet/`. Read the relevant PDFs before writing questions or explanations - do not rely solely on general knowledge of the topic.
- Match the slide language to the sheet's language. Do not pull C-specific content (e.g. `gcc`, `extern`/`static` storage classes from L10) into a C++ sheet, or vice versa. C++ sheets must use `g++` for compilation, `.cpp`/`.hpp` extensions, and source from C++ slides (cppIntro, L09, L11-L17). Audit every command and keyword for language correctness before regenerating.
- When making a new topic sheet, check existing topic sheets first and put genuinely relevant material into an existing related sheet if that avoids unnecessary duplication.
- If a RAG item is broad enough to need its own focused sheet, create both the ReportLab generator script and the generated PDF in `topicsheets/`.
- Each topic sheet must include exactly 10 practice questions.
- Any practice question that asks the student to inspect, fix, trace, or complete code must include the corresponding code snippet on the sheet. Do not ask the student to look through code that is not provided.
- Practice questions should test active recall and application. Prefer concrete mini-tasks, traces, and fixes over questions that only ask for a definition.
- Do not write questions that test memory of a specific function or exercise from the worksheets or CA. Questions should test general knowledge of the language, not whether the student remembers what a particular past exercise asked them to implement.
- Include a mark scheme after the practice questions, and make sure every practice question has a corresponding answer.
- Update `revision-rag-topic-list.md` when a new topic sheet is created, changing the relevant row to `Yes:` with a link to the PDF.

## Mock Exam Paper Notes

- Mock exam paper topics must come from the RAG revision, course slides, worksheets, and topic sheets.
- Do not reuse worksheet, CA, topic-sheet, or sample-paper questions directly. Questions may be inspired by those materials, but they must change the context, data, wording, or required reasoning so the paper tests understanding rather than recall of a seen question.
- Format mock papers like `mock-exams/ECM2433-sample-answers.pdf` for overall structure and exam style.
- Put all answers and mark schemes at the end of the paper, not throughout the question section.
- Any question that asks the student to inspect, fix, trace, or complete code must include the corresponding code snippet in the paper.
- Mock exam questions should test application and problem-solving. Avoid prompts that tell the student exactly what to include or only ask them to restate a rule.
- Include a clear answer or mark scheme for every question.
- Save generated mock exam files in `mock-exams/`.
- After generating a mock exam paper, ChatGPT/Codex must check every question and answer against the relevant course material and the generated mark scheme.
- If a question is ambiguous, missing required code, not grounded in the course material, duplicated from an existing worksheet/CA/topic sheet, or has an incorrect/incomplete answer, ChatGPT/Codex must fix the paper before reporting it as complete.
