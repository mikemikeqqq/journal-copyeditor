---
name: journal-copyeditor-docx
description: Professional academic journal copyediting for .docx manuscripts. Use when the user asks Codex to proofread, line-edit, polish, revise, or prepare an academic manuscript in Microsoft Word with tracked changes, Catherine-style editor comments, formal critical academic English, construct consistency, methodological caution, minimal local tracked edits instead of whole-paragraph replacement, citation-year ordering, citation/reference audits, statistics/number consistency checks, journal style profiles, reviewer-risk audit, clean/tracked/PDF delivery packages, an appended copy editing and proofreading report, preservation of existing comments/revisions/citations/fields/fonts/formatting, native English style, journal or discipline conventions, Chinese-influenced English cleanup, and validation against DOCX corruption, mojibake, unexpected CJK characters, missing Catherine comments, formatting drift, or excessive paragraph-level revision blocks.
---

# Journal Copyeditor DOCX

Use this skill when the deliverable is a copy-edited academic `.docx`, normally with Microsoft Word tracked changes and concise editor comments.

## Operating Contract

- Preserve the source DOCX. Always create a new output file, preferably in `output/doc/` or beside the source with a clear suffix.
- Default to `Catherine` / `C` as the Word reviewer identity unless the user supplies another name. Restore the previous Word user name and initials afterward.
- Use Microsoft Word automation for tracked changes when Word COM is available. Avoid direct OOXML edits for final tracked-change deliverables unless the user explicitly accepts the risk.
- Keep Track Changes enabled for edits. Preserve existing revisions and comments unless the user explicitly asks to accept, reject, remove, or resolve them.
- Treat author-provided text as the factual source. Improve language, structure, and hedging, but never invent data, methods, citations, mechanisms, limitations, p-values, sample sizes, figure panels, or reference metadata.
- Preserve technical meaning, hypotheses, model names, sample sizes, coefficients, p-values, statistical notation, equations, citations, field codes, tables, figures, reference entries, and proper names.
- Use formal academic English with clear, common vocabulary. Be direct, critical, and professional. Pair criticism with concrete revision solutions.
- Maintain strict construct consistency. Do not introduce unmeasured constructs or replace the author's constructs with broader, narrower, or trendier terms unless explicitly requested.
- Treat correlations, regression coefficients, meta-analytic estimates, structural paths, and moderation results as associations unless the research design justifies causal inference.
- Preserve formatting. Edited or inserted tracked-change text must inherit the surrounding font, size, style, spacing, paragraph style, table/caption/reference formatting, and superscript/subscript behavior unless the user explicitly requests formatting changes.
- Use minimal local tracked changes. Replace only the word, phrase, punctuation, clause, or sentence part that needs editing. Do not delete and reinsert whole paragraphs for ordinary copyediting.
- Sort multiple author-date citations within the same citation cluster by publication year ascending unless the target journal explicitly requires another order. Preserve citation-manager fields; if safe reordering is not possible, add a report item or editor comment instead of breaking fields.
- Add comments only for author decisions that copyediting cannot safely settle: unclear meaning, theory or interpretation changes, inconsistent terminology, duplicated examples, missing evidence, unsupported claims, or possible citation/statistical issues.
- Append a `Copy Editing and Proofreading Report` section inside the edited Word document unless the user explicitly asks for a separate report. The report should identify language issues, citation/reference problems, and reviewer-risk points that need author attention.
- Do not use Word Compare as the default path for final tracked changes when the manuscript contains many symbols, accented names, equations, or non-ASCII characters.

## When to Open Extra Files

| File | Open when |
|---|---|
| [references/copyediting-contract.md](references/copyediting-contract.md) | Choosing light, medium, or heavy copyediting; deciding what may be changed, commented, or left untouched |
| [references/academic-critical-style.md](references/academic-critical-style.md) | Applying formal critical academic English, construct consistency, methodological caution, literature standards, and reviewer-response style |
| [references/style-and-argument.md](references/style-and-argument.md) | Editing section logic, paragraph flow, claim-evidence-boundary, discipline voice, or Chinese-influenced English |
| [references/minimal-diff-tracked-changes.md](references/minimal-diff-tracked-changes.md) | Avoiding whole-paragraph delete/reinsert revisions and keeping tracked changes reviewable |
| [references/format-preservation.md](references/format-preservation.md) | Preserving fonts, run formatting, paragraph styles, table/reference/caption formatting, and checking formatting drift |
| [references/citations-and-report.md](references/citations-and-report.md) | Sorting author-date citation clusters by year, checking reference consistency, and writing the final copy editing report |
| [references/journal-styles.md](references/journal-styles.md) | Choosing APA/Harvard/Nature/Elsevier/IEEE/Vancouver conventions, English variety, and reference formatting assumptions |
| [references/reviewer-risk-rubric.md](references/reviewer-risk-rubric.md) | Grading potential reviewer challenges as minor, moderate, or serious |
| [references/statistics-and-numbers.md](references/statistics-and-numbers.md) | Checking p-values, CI, SD/SE, sample sizes, table/figure numbering, and significance language |
| [references/chinese-influenced-english.md](references/chinese-influenced-english.md) | Diagnosing article errors, long translated sentences, unscopeed novelty, and Results/Discussion mixing in Chinese-influenced English |
| [references/deliverable-packaging.md](references/deliverable-packaging.md) | Creating tracked, clean, PDF, report, and audit-output delivery packages |
| [references/word-com-workflow.md](references/word-com-workflow.md) | Using Word COM safely for tracked changes, comments, PDF export, cleanup, or fallback decisions |
| [references/validation-checklist.md](references/validation-checklist.md) | Running final QA, interpreting `validate_docx.py`, checking corruption, or deciding readiness |

## Workflow

1. Intake the task:
   - Identify the manuscript file, requested editor name, target journal or spelling style, and editing level. If unspecified, use medium journal copyediting in US English unless the manuscript or user indicates another convention.
   - If the user supplied style samples, apply them only as a soft guide; discipline, journal norms, factual fidelity, and clarity take priority.
2. Inspect the file:
   - Confirm it opens.
   - Count existing revisions and comments.
   - Identify existing reviewer names.
   - Record whether comments by `Catherine` already exist and must be preserved.
   - Check whether Track Changes is already enabled.
   - Run the validation script on the source when possible to establish a baseline.
   - Run `scripts/audit_citations.py` and `scripts/audit_numbers.py` when the manuscript has citations, references, tables, figures, or statistics.
3. Create a clean output copy.
4. Copy-edit with Word COM:
   - Turn on Track Changes.
   - Work paragraph by paragraph, preserving citations, equations, fields, and reference data.
   - Preserve source formatting at the run/paragraph level. Capture and reapply local font/style when Word does not inherit formatting automatically.
   - Make edits at the smallest safe range. Do not replace an entire paragraph when only local language changes are needed.
   - Sort multi-source author-date citation clusters by year ascending when it can be done without damaging citation fields.
   - Check for citation/reference issues: missing citations, citations with no reference entry, reference entries not cited, inconsistent citation style, wrong order, incomplete metadata, and inconsistent reference formatting.
   - Apply journal style assumptions explicitly. If the target style is uncertain, state the assumed profile in the report.
   - Apply `references/academic-critical-style.md`: keep construct labels consistent, avoid unmeasured constructs, use cautious methodological language, and align theory, hypotheses, results, and implications.
   - Apply the statistics/numbers pass for p-values, CI, sample sizes, figure/table numbering, and unsupported significance language.
   - For Chinese-influenced English, repair translationese and add comments/report items when missing comparators, scope, evidence, or section logic remain unresolved.
   - Prefer targeted sentence and paragraph edits over broad global rewrites.
   - Use global find/replace only for low-risk, verified changes.
5. Add editor comments and the report:
   - Use concise, professional English in the requested editor voice.
   - Comment on genuine author decisions, not every grammar edit.
   - Append a `Copy Editing and Proofreading Report` section in the edited Word document summarizing proofreading issues, citation/reference problems, statistics/number issues, and reviewer-risk points.
   - Use `scripts/insert_copyediting_report.py` when a report can be inserted safely via Word COM.
6. Validate before delivery:
   - Reopen the output with Word.
   - Confirm revision count, comment count, and Track Changes status.
   - Run `scripts/validate_docx.py` on the output, preferably with `--source --require-report --require-comment-author Catherine`.
   - Run `scripts/audit_revision_granularity.py` on the output and redo any confirmed whole-paragraph replacement as local tracked edits.
   - Run `scripts/audit_formatting.py` on the output and visually inspect any flagged inserted text.
   - Export a PDF check copy when possible.
   - Visually check several high-risk pages: title/abstract, equations/statistics, tables, references, and any pages with comments.
   - If unexpected CJK, mojibake, missing comments, missing Catherine comments, missing report, lost revisions, corrupted symbols, whole-paragraph replacement patterns, or formatting drift appear, stop and fix before delivery.
7. Report the deliverable:
   - Provide the edited DOCX path, optional clean DOCX/PDF/audit outputs, validation summary, and a short note that the in-document report lists citation/reference, statistics/number, and reviewer-risk issues.

## Style Guidance

- Language serves argument. Do not make a sentence elegant while leaving the reasoning unclear.
- Edit in this priority order: factual fidelity, claim-evidence-boundary, section job, paragraph flow, sentence clarity, rhythm, word choice.
- Prefer concise journal prose, but do not flatten disciplinary nuance or authorial intent.
- Keep terminology consistent. Do not rotate synonyms for technical concepts merely for variety.
- Hedge unsupported causal, mechanistic, novelty, or generalization claims. Flag major claim-evidence gaps in comments.
- Remove AI-typical filler when encountered, such as `delve`, `pivotal`, `crucial`, `realm`, `landscape` when vague, `it is important to note`, and overused em dashes.
- For Chinese-influenced English, translate intent rather than syntax: identify claim, evidence, condition, comparison, implication, and limitation before rewriting.

## Validation Script

Use `scripts/validate_docx.py` on the final DOCX:

```powershell
python scripts/validate_docx.py "path/to/file.docx"
python scripts/validate_docx.py "edited.docx" --source "source.docx" --require-report --require-comment-author Catherine --fail-on-suspect
```

The script reports:

- visible CJK and mojibake-suspect counts in manuscript text and comments;
- insertion/deletion/move/format-change marker counts;
- comment authors/counts;
- whether required comment authors, such as `Catherine`, are present when requested;
- whether a `Copy Editing and Proofreading Report` heading is present;
- whether `w:trackRevisions` is enabled;
- source-vs-output warnings for missing comments, lost revisions, or newly introduced CJK/mojibake patterns.

Visible CJK count should normally be `0` for English manuscripts unless the source intentionally contains Chinese/Japanese/Korean text.

## Audit and Packaging Scripts

Use these helpers when relevant:

```powershell
python scripts/audit_citations.py "manuscript.docx" --json-output "citation_audit.json" --summary-output "citation_audit.md"
python scripts/audit_numbers.py "manuscript.docx" --json-output "numbers_audit.json" --summary-output "numbers_audit.md"
python scripts/audit_revision_granularity.py "edited.docx" --json-output "revision_granularity_audit.json" --summary-output "revision_granularity_audit.md"
python scripts/audit_formatting.py "edited.docx" --json-output "formatting_audit.json" --summary-output "formatting_audit.md"
python scripts/insert_copyediting_report.py "edited.docx" --report-file "report.md" --editor-name "Catherine" --editor-initials "C"
python scripts/create_delivery_package.py "edited.docx" --output-dir "output/doc" --clean-copy --pdf
```

The audit scripts are heuristic. Use their output as evidence for the copy editing report, then verify high-risk findings manually before changing manuscript content.

## Stop Conditions

- Do not deliver a file with unexpected visible CJK, mojibake-like text, replacement characters, broken equations, missing existing comments, or missing expected tracked changes.
- Do not deliver a tracked-copy DOCX with missing Catherine comments when Catherine comments were added or required.
- Do not deliver a file where ordinary copyediting appears as whole-paragraph deletion plus whole-paragraph insertion.
- Do not deliver a file whose tracked insertions visibly use a different font, size, style, or paragraph/table/reference formatting from the surrounding text.
- Do not rely only on Word opening successfully; corruption can still appear in rendered manuscript text.
- Do not accept/reject revisions, remove comments, update fields, rewrite references, or break citation-manager fields unless the user explicitly asks and the result is verified.
- Do not omit the final in-document copy editing report unless the user explicitly asks for a separate report or no report.
- Do not leave Word automation processes running after finishing.
