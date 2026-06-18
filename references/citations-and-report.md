# Citations and Copy Editing Report

Use this reference when checking citations, reference style, and the final in-document report.

## Citation-Year Sorting

Default rule for author-date manuscripts:

- In a multi-source citation cluster, sort citations by publication year ascending.
- Preserve original author spelling, suffixes, year letters, page numbers, and prefixes.
- Keep same-year citations in author order unless the journal style states otherwise.
- Keep narrative citations unchanged unless their surrounding parenthetical cluster needs sorting.

Examples:

- `(Smith, 2020; Chen, 2018; Lee, 2021)` -> `(Chen, 2018; Smith, 2020; Lee, 2021)`
- `(Smith, 2020a, 2020b; Chen, 2018)` -> `(Chen, 2018; Smith, 2020a, 2020b)`
- `(see Chen, 2018; Smith, 2020, for review)` should be edited only if the prefix/suffix remains grammatical.

Do not apply this rule to numeric citation styles such as Vancouver, IEEE, Nature-numbered references, or superscript note systems unless the target journal explicitly requires chronological ordering.

## Citation-Manager Safety

Before changing citation order, check whether the citation is plain text or a field inserted by Zotero, EndNote, Mendeley, Word bibliography, or another manager.

If it is a citation-manager field:

- prefer using the citation manager or Word field-safe operations if available;
- do not manually type inside field codes if that may break live updating;
- if safe editing is not available, leave the citation intact and list the issue in the report;
- add an editor comment only when the citation order may affect submission compliance or reader interpretation.

## Citation and Reference Checks

Check and report:

- citation clusters not sorted by year;
- claims that need citations;
- citations that appear unsupported by the nearby claim;
- citations in text with no matching reference entry;
- reference entries that are not cited in the text;
- inconsistent author-year spelling between citation and reference list;
- incomplete reference metadata: missing year, journal, volume, pages/article number, DOI when required;
- inconsistent reference formatting: capitalization, journal title style, italics, punctuation, hanging indent, DOI/URL format;
- mixed citation styles, such as author-date plus numeric citations in the same manuscript;
- repeated or duplicate reference entries;
- outdated or weak support for a central claim when more current or primary evidence may be needed.

Do not invent corrected metadata. If metadata is missing or appears wrong, flag it for author verification.

## In-Document Report Requirement

Unless the user requests otherwise, append a final section to the edited Word document titled exactly:

`Copy Editing and Proofreading Report`

Place it after the manuscript or after the references, depending on which is least disruptive. Keep Track Changes on so the insertion is visible.

## Report Structure

Use concise headings:

1. `Copy Editing Scope`
2. `Language and Proofreading Issues`
3. `Citation and Reference Issues`
4. `Potential Reviewer Challenges`
5. `Author Action Items`

Keep the report factual and audit-friendly. It should help the author decide what to fix before submission.

## What To Include

`Copy Editing Scope`:

- editing level: light, medium, or heavy;
- editor identity used for tracked changes;
- whether existing comments/revisions were preserved;
- any limitations, such as citation-manager fields not safely editable.

`Language and Proofreading Issues`:

- repeated grammar or article problems;
- terminology inconsistencies;
- ambiguous sentences or paragraphs;
- figure/table callout issues;
- abbreviation definition problems.

`Citation and Reference Issues`:

- unsorted citation clusters corrected or still needing correction;
- missing citations;
- possibly incorrect citations;
- reference list entries with inconsistent or incomplete formatting;
- references not cited or citations not found in references;
- style conflicts with the target journal.
- citation audit outputs from `scripts/audit_citations.py`, after manual sanity checking.

`Potential Reviewer Challenges`:

- unsupported or overstrong claims;
- causal claims from correlational evidence;
- missing methodological details;
- unclear novelty or contribution;
- insufficient limitations;
- inconsistent terminology affecting theory, constructs, variables, or methods;
- claims that may require stronger, newer, or primary-source citations.
- severity labels from `references/reviewer-risk-rubric.md`: `minor`, `moderate`, or `serious`.

`Statistics and Numbers Issues` may be added when relevant:

- p-value or CI formatting problems;
- inconsistent sample sizes, figure/table numbering, or statistical notation;
- significance language that lacks a nearby statistical result;
- outputs from `scripts/audit_numbers.py`, after manual sanity checking.

`Author Action Items`:

- list concrete items the author must check before submission;
- keep each item specific enough to act on;
- do not claim an issue has been fixed unless it is visibly fixed in the manuscript.

## Tone

Use professional, direct language. Do not overstate. Avoid making peer-review predictions sound certain. Prefer:

- `Reviewers may ask whether...`
- `This claim may need a stronger citation because...`
- `Please verify whether...`

Avoid:

- `This will be rejected because...`
- `The author failed to...`
- vague instructions such as `check references`.
