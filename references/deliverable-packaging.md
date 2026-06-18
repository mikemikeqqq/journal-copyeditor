# Deliverable Packaging

Use this reference when the user wants submission-ready outputs beyond a single tracked DOCX.

## Default Package

For a normal copyediting task, deliver:

- `manuscript_tracked.docx`: edited Word file with Track Changes and comments.
- optional `manuscript_check.pdf`: PDF exported from the tracked DOCX for visual QA.

The tracked DOCX should contain the `Copy Editing and Proofreading Report` unless the user asks for a separate report.

The tracked DOCX must preserve Catherine comments when Catherine is the requested editor or when Catherine comments already exist.

## Expanded Package

When requested, or when the manuscript is near submission, produce:

- `manuscript_tracked.docx`
- `manuscript_clean.docx`
- `manuscript_check.pdf`
- `copyediting_report.docx` or an embedded report section
- citation audit JSON and/or Markdown summary from `scripts/audit_citations.py`

## Clean Copy Rules

Only create a clean copy when the user asks for it or when it is clearly part of the requested package.

Clean copy means:

- all tracked changes accepted in a duplicate file;
- comments removed or preserved according to user instruction, but never in the tracked copy;
- original tracked copy kept unchanged;
- final validation run on both files when possible.

Never replace the tracked copy with a clean copy.

## Suggested Naming

Use clear, non-destructive suffixes:

- `{stem}_copyedited_tracked.docx`
- `{stem}_copyedited_clean.docx`
- `{stem}_copyedited_check.pdf`
- `{stem}_copyediting_report.docx`
- `{stem}_citation_audit.json`
- `{stem}_citation_audit.md`

## Validation

Before delivery:

- validate the tracked DOCX against the source with `validate_docx.py --source --require-report`;
- add `--require-comment-author Catherine` when Catherine comments are expected;
- visually inspect the PDF check copy if exported;
- if a clean copy is created, open it in Word and confirm comments/revisions were handled exactly as requested;
- confirm the report and audit outputs describe unresolved issues honestly.
