# Minimal-Diff Tracked Changes

Use this reference whenever a tracked-change output shows whole paragraphs deleted and reinserted. That pattern is not acceptable for copyediting unless the user explicitly requested a heavy rewrite.

## Hard Rule

Only revise the words, phrases, punctuation, or sentence parts that need revision. Do not delete an entire paragraph and insert a revised version when only local wording changes are needed.

The tracked-change view should let the author see exactly what changed.

## Preferred Editing Granularity

Use the smallest safe range:

- punctuation or article: edit the character or word;
- word choice: replace only the word or short phrase;
- grammar: replace only the affected clause;
- sentence clarity: revise the sentence, not the paragraph, unless paragraph structure truly changes;
- paragraph flow: move or split only the needed sentence(s), with a report note if this is a substantive structural edit.

## When Whole-Sentence or Whole-Paragraph Edits Are Allowed

Whole-sentence edits are acceptable only when:

- the original sentence is structurally broken;
- the sentence has multiple grammar problems that cannot be fixed locally;
- the user requested heavier polishing.

Whole-paragraph replacement is acceptable only when:

- the paragraph is being reorganized for logic, not merely polished;
- the user requested heavy editing or rewriting;
- a report note explains why the paragraph-level revision was necessary.

## Word COM Pattern

Avoid:

- assigning `Range.Text` to an entire paragraph;
- selecting a paragraph and typing the polished paragraph over it;
- using Word Compare to generate changes from a clean rewritten copy;
- deleting a paragraph and pasting a rewritten paragraph.

Prefer:

- find the exact phrase range and replace that range;
- split long edits into several local replacements;
- preserve formatting for every local replacement;
- inspect tracked changes after each paragraph or section.

## Validation

Run:

```powershell
python scripts/audit_revision_granularity.py "edited.docx" --summary-output "revision_granularity_audit.md" --json-output "revision_granularity_audit.json"
```

Investigate warnings before delivery. If the audit flags a paragraph with large deletion and insertion blocks, visually inspect it in Word. Redo that paragraph as local edits unless the large replacement was intentional and documented.

## Stop Conditions

Do not deliver a tracked DOCX if:

- a normal copyediting paragraph appears as fully deleted and fully reinserted;
- many paragraphs contain large paired deletion/insertion blocks;
- the author cannot easily identify what changed;
- revision granularity warnings are confirmed visually and not justified in the report.
