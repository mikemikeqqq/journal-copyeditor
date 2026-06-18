# Word COM Workflow

Use Microsoft Word automation for final tracked-change editing whenever Word is available. This reference is procedural because DOCX tracked changes are fragile.

## Preflight

Before editing:

1. Make a filesystem copy of the source DOCX.
2. Open the copy in Word, not the original.
3. Record baseline state:
   - existing revision count;
   - existing comment count and authors;
   - whether comments by `Catherine` already exist and must be preserved;
   - Track Changes setting;
   - Word user name and initials;
   - whether the document opens in Protected View or Compatibility Mode.
4. Run `validate_docx.py` on the source to record CJK/mojibake baseline.

If Word refuses to open the file, do not repair destructively. Make a separate repaired copy or ask for permission before using Word's repair prompt.

## Reviewer Identity

Set:

- `Application.UserName = "Catherine"` unless the user supplies another name;
- `Application.UserInitials = "C"` unless the user supplies initials;
- `Document.TrackRevisions = True` for the editing pass.

Always restore the previous Word user name and initials in a `finally`/cleanup block.

## Editing Safely

Preferred:

- edit visible text through Word ranges or selections;
- replace only the smallest necessary range, such as a word, phrase, punctuation mark, clause, or sentence part;
- capture the target range's style and font before replacing text, then verify that the inserted tracked-change text inherits the same formatting;
- preserve run-level field codes, hyperlinks, cross-references, equations, citation-manager fields, and comments;
- edit paragraph by paragraph;
- save periodically under the output filename.

High risk:

- broad find/replace across the whole document;
- deleting a paragraph and typing or pasting a rewritten paragraph over it;
- selecting whole paragraphs for ordinary sentence-level copyediting;
- pasting or inserting text that uses Word's default font rather than destination formatting;
- replacing text that spans citations, equations, fields, or comments;
- replacing mixed-format ranges as one block instead of editing smaller same-format runs;
- editing `word/document.xml` directly;
- using Word Compare as the main mechanism for tracked changes;
- accepting or rejecting revisions during copyediting.
- deleting, resolving, hiding, or losing comments during tracked-copy preparation.

Only use global find/replace when the change is trivial, unambiguous, and verified in context. Examples: a misspelled author-created term, repeated article error in plain prose, or a renamed abbreviation after author instruction.

For formatting-sensitive edits, open `references/format-preservation.md`.

For revision-granularity problems like whole-paragraph delete/reinsert output, open `references/minimal-diff-tracked-changes.md`.

## Comments

Add comments to a tight range whenever possible. Comments should name the author decision, not summarize the edit.

Good patterns:

- `Please confirm whether "X" refers to the framework or the empirical model.`
- `This appears to imply causation, but the evidence reported here is correlational. Please confirm the intended claim.`
- `Please verify that this citation supports the stronger novelty claim.`

Avoid:

- comments on every grammar edit;
- generic `Please review`;
- comments that introduce new scientific claims;
- deleting or resolving existing comments unless requested.

After editing, confirm that comments authored by `Catherine` are still present if they were added or expected. If they are missing, do not deliver the tracked copy.

## Copy Editing Report

Append the final in-document report after the manuscript or after the references, whichever is least disruptive. Use the exact heading:

`Copy Editing and Proofreading Report`

Default behavior:

- keep the report in the same edited DOCX;
- keep Track Changes on so the report insertion is visible;
- use normal manuscript text, not only comments;
- include citation/reference issues and likely reviewer challenges;
- do not accept/reject tracked changes before inserting the report.

If the user asks for the report to be separate, create it separately and note that the DOCX does not contain the report.

## PDF Export

When possible, export a PDF check copy after saving the DOCX. Use it for visual QA only; the DOCX remains the deliverable.

Check:

- title page and abstract;
- first page after every section heading;
- pages containing equations, tables, figures, comments, or references;
- the `Copy Editing and Proofreading Report` section;
- any page where Word reported repair or conversion behavior.

## Cleanup

At the end:

1. Save the document.
2. Close the document.
3. Restore Word user name and initials.
4. Quit Word if this automation session started it.
5. Confirm no orphaned `WINWORD.EXE` instance remains from the automation.

If automation fails mid-edit, preserve the partial file with a clear suffix and report the last successful step.

## Fallbacks

If Word COM is unavailable:

- For a final tracked-change deliverable, pause and explain that Word is required for safe tracked changes.
- For analysis only, inspect with DOCX tools and produce a separate editing plan or comments list.
- Do not emulate tracked changes with direct XML unless the user explicitly accepts the risk and validation burden.
