# Revision Content Notes

- Do not put HTML/XML escaped ampersand entities in human-facing revision text.
- In spreadsheet content, avoid raw ampersand syntax where a viewer might expose XML escapes; prefer wording such as "borrowed string slice", "borrow `text`", or "address of `k`".
- In ReportLab paragraph markup, use numeric character entities for required ampersand symbols inside code examples.
- Before regenerating outputs, scan source text for escaped ampersand entities and preserve existing `Completed` marks in `revision-mistake-log.xlsx`.
- Revision questions should test active recall and problem-solving. Do not write questions that tell the user exactly what to include, and do not use prompts that only ask the user to restate or parrot a rule back.
- For mistake-log redo prompts, ask the user to apply the missed idea to a small concrete example instead of listing the missing phrases from the mark scheme.
- When adding new mistake-log rows, append them to the end of the spreadsheet instead of inserting them into the middle of older rows.
