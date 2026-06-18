# Validation Checklist

Use this reference before delivering a copy-edited DOCX.

## Baseline

Run validation on the source before editing when possible:

```powershell
python scripts/validate_docx.py "source.docx" --json
```

Record:

- visible manuscript CJK count and samples;
- mojibake-suspect count;
- existing insertion/deletion/move/format-change counts;
- comment count and comment authors;
- Track Changes status.

## Final Script Gate

Run the final output against the source:

```powershell
python scripts/validate_docx.py "edited.docx" --source "source.docx" --require-report --require-comment-author Catherine --fail-on-suspect
```

Investigate every warning. Do not deliver until the warning is understood and either fixed or explicitly explained.

## Required Checks

- The output opens in Word without repair prompts.
- Track Changes is enabled or the user explicitly requested a clean copy.
- Existing comments are still present unless the user asked to remove/resolve them.
- New comments are authored by the requested editor identity.
- Catherine comments are present when Catherine is the requested editor or when the source/output should preserve Catherine's comments.
- There are visible tracked changes for the copyediting work.
- Tracked changes are local and reviewable, not ordinary paragraphs deleted and reinserted wholesale.
- Inserted tracked-change text matches the surrounding manuscript font, size, style, paragraph formatting, table formatting, and reference/caption formatting.
- The edited Word document contains a visible `Copy Editing and Proofreading Report` section unless the user requested a separate report.
- Citations, equations, tables, figures, cross-references, field codes, and reference entries are intact.
- Multi-source author-date citation clusters are sorted by publication year ascending where safe to edit.
- Citation and reference issues are listed in the report when they cannot be safely corrected.
- Citation audit and statistics/number audit outputs have been incorporated into the report when relevant.
- Revision granularity audit output has been reviewed, and any confirmed whole-paragraph replacement pattern has been redone as local edits or justified in the report.
- Formatting audit output has been reviewed, and any confirmed drift has been fixed.
- Reviewer-risk items are labelled `minor`, `moderate`, or `serious` when the report identifies likely reviewer challenges.
- No unexpected CJK characters, replacement characters, or mojibake-like sequences appear in visible manuscript text.
- PDF export, if possible, visually matches the DOCX and does not reveal broken layout.

## High-Risk Text To Inspect Manually

- Greek letters, mathematical operators, superscripts/subscripts, and equations.
- Accented author names, non-English titles, and species names.
- Statistical notation: p-values, confidence intervals, sample sizes, effect sizes, coefficients.
- Reference entries and citation-manager fields.
- Tables with merged cells or footnotes.
- Figure captions and supplementary-material callouts.
- Existing comments and replies.
- Inserted tracked changes in paragraphs, tables, captions, headings, and references.
- Any paragraph where Word shows large red deletion followed by large red insertion.
- The final report section and any author action items.

## Readiness Labels

Use these labels when reporting the deliverable:

- `ready`: final DOCX passes script and visual checks.
- `ready_with_notes`: deliverable is safe, but the user should review named comments or style choices.
- `needs_author_input`: editor comments flag factual, evidentiary, or interpretive decisions before submission.
- `blocked`: corruption, lost comments/revisions, Word automation failure, or unverified repair prevents delivery.

Never label a file `ready` if the script reports unexplained suspect text, missing comments, missing Catherine comments, missing report, confirmed whole-paragraph replacement, formatting drift, or no tracked changes after an editing pass.

## Triage

If CJK or mojibake appears unexpectedly:

1. Compare against the source validation output.
2. Open the affected text in Word and PDF.
3. Check whether the characters are intentional manuscript content, existing author comments, citation titles, or newly introduced corruption.
4. If corruption is confirmed, revert to the last clean copy and redo the affected edits through Word COM.

If comments disappear:

1. Stop editing.
2. Recover from the source or last checkpoint.
3. Avoid operations that rebuild the DOCX package or use Word Compare.
4. Check whether a clean copy, accepted-revisions copy, PDF-export-only file, or report-only copy was accidentally delivered instead of the tracked copy.
5. Rerun validation with `--require-comment-author Catherine` when Catherine comments are expected.

If revision counts are unexpectedly low:

1. Confirm Track Changes was on during edits.
2. Check whether edits were made before Track Changes was enabled.
3. Redo the affected edits if tracked changes are required.
