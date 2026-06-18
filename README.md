# Journal Copyeditor DOCX

`journal-copyeditor-docx` is a Codex skill for professional academic manuscript copyediting in Microsoft Word `.docx` files. It focuses on tracked changes, editor comments, formatting preservation, citation/reference checks, statistics and number audits, reviewer-risk notes, and final DOCX validation.

## What It Helps With

- Copy-edit academic manuscripts with Word tracked changes.
- Preserve existing comments, revisions, citations, fields, tables, figures, equations, and formatting.
- Add concise editor comments for author decisions.
- Append a `Copy Editing and Proofreading Report`.
- Audit citations, references, numbers, formatting, and revision granularity.
- Package tracked, clean, PDF, report, and audit deliverables.

## Installation

Copy or clone this folder into your Codex skills directory:

```powershell
git clone https://github.com/mikemikeqqq/journal-copyeditor.git "$env:USERPROFILE\.codex\skills\journal-copyeditor-docx"
```

Restart Codex after installing the skill.

## Basic Usage

Ask Codex to use the skill on a manuscript, for example:

```text
Use $journal-copyeditor-docx to copy-edit this academic manuscript with tracked changes, Catherine comments, citation/reference checks, and a final validation report.
```

The skill expects Microsoft Word automation for final tracked-change deliverables when available. The bundled Python scripts provide validation and audit support.

## Helper Scripts

Run scripts from the skill root:

```powershell
python scripts/validate_docx.py "edited.docx" --source "source.docx" --require-report --require-comment-author Catherine --fail-on-suspect
python scripts/audit_citations.py "manuscript.docx" --json-output "citation_audit.json" --summary-output "citation_audit.md"
python scripts/audit_numbers.py "manuscript.docx" --json-output "numbers_audit.json" --summary-output "numbers_audit.md"
python scripts/audit_revision_granularity.py "edited.docx" --summary-output "revision_granularity_audit.md" --json-output "revision_granularity_audit.json"
python scripts/audit_formatting.py "edited.docx" --summary-output "formatting_audit.md" --json-output "formatting_audit.json"
python scripts/create_delivery_package.py "edited.docx" --output-dir "output/doc" --clean-copy --pdf
```

## Repository Structure

```text
journal-copyeditor-docx/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

## License

MIT License. See [LICENSE](LICENSE).
