# Format Preservation

Use this reference when editing tracked changes in Word. The copy-edited text must visually match the source manuscript unless the user explicitly requests formatting changes.

## Hard Rule

Language edits must inherit the local formatting of the text being edited:

- font family;
- font size;
- bold/italic/underline;
- superscript/subscript;
- paragraph style;
- spacing and indentation;
- table-cell formatting;
- equation/citation field formatting.

Do not introduce a different font or style merely because text was inserted through automation.

## Word COM Editing Pattern

Preferred pattern for replacing text:

1. Capture the target range's `Font`, `Style`, and paragraph formatting before editing.
2. Replace only the intended visible text.
3. Reapply the captured style/font to the inserted range if Word does not inherit it.
4. For mixed-format ranges, split the edit into smaller runs so each inserted phrase inherits the nearest original run.
5. Visually inspect the changed line in Word after high-risk edits.

Avoid:

- pasting plain text from the clipboard without matching destination formatting;
- replacing whole paragraphs when only a sentence needs editing;
- using `Range.Text = ...` across text with mixed formatting, citations, equations, or field codes;
- inserting report text into the manuscript body without separating it from the manuscript section.

## Tables, References, and Captions

These areas are especially sensitive:

- table body and table footnotes;
- figure captions;
- reference list entries;
- headings;
- superscripts/subscripts;
- Greek letters and mathematical notation.

Prefer local, minimal edits. If formatting changes after editing, undo and redo the edit in smaller pieces.

## Formatting Audit

Run:

```powershell
python scripts/audit_formatting.py "edited.docx" --summary-output "formatting_audit.md" --json-output "formatting_audit.json"
```

This script checks explicit run formatting in tracked insertions against nearby paragraph text. It is heuristic: Word style inheritance may not appear fully in XML. Treat warnings as a reason to inspect the page visually.

## Stop Conditions

Do not deliver the tracked DOCX if:

- inserted tracked changes visibly use a different font/size from surrounding text;
- table edits changed alignment, cell spacing, or font;
- reference entries changed formatting inconsistently;
- headings or captions changed style unexpectedly;
- the formatting audit reports drift and visual inspection confirms it.
