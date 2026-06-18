#!/usr/bin/env python3
"""Insert a Copy Editing and Proofreading Report into a DOCX via Word COM."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="DOCX file to update")
    parser.add_argument("--output", type=Path, help="Output DOCX path. Defaults to in-place update.")
    parser.add_argument("--report-file", type=Path, help="Plain-text or Markdown report content to insert")
    parser.add_argument("--editor-name", default="Catherine", help="Word reviewer name")
    parser.add_argument("--editor-initials", default="C", help="Word reviewer initials")
    parser.add_argument("--no-track-changes", action="store_true", help="Insert report without Track Changes")
    parser.add_argument("--pdf-output", type=Path, help="Optional PDF export path")
    return parser.parse_args()


def default_report() -> str:
    return """Copy Editing and Proofreading Report

Copy Editing Scope
- Editing level:
- Reviewer identity:
- Existing comments/revisions preserved:

Language and Proofreading Issues
- 

Citation and Reference Issues
- 

Potential Reviewer Challenges
- 

Author Action Items
- 
"""


def insert_with_word(
    docx: Path,
    output: Path,
    report_text: str,
    editor_name: str,
    editor_initials: str,
    track_changes: bool,
    pdf_output: Path | None,
) -> None:
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "pywin32 is required for Word COM automation. Install pywin32 or run inside an environment that provides it."
        ) from exc

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    old_name = word.UserName
    old_initials = word.UserInitials
    doc = None
    try:
        word.UserName = editor_name
        word.UserInitials = editor_initials
        doc = word.Documents.Open(str(output.resolve()))
        doc.TrackRevisions = bool(track_changes)

        end_range = doc.Range(doc.Content.End - 1, doc.Content.End - 1)
        end_range.InsertBreak(7)  # wdPageBreak
        end_range = doc.Range(doc.Content.End - 1, doc.Content.End - 1)
        end_range.InsertAfter(report_text.rstrip() + "\n")

        doc.SaveAs2(str(output.resolve()))
        if pdf_output:
            doc.ExportAsFixedFormat(str(pdf_output.resolve()), 17)  # wdExportFormatPDF
    finally:
        if doc is not None:
            doc.Close(SaveChanges=True)
        word.UserName = old_name
        word.UserInitials = old_initials
        word.Quit()


def main() -> int:
    args = parse_args()
    if not args.docx.exists():
        print(f"error: file not found: {args.docx}", file=sys.stderr)
        return 2

    output = args.output or args.docx
    if output != args.docx:
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.docx, output)

    report_text = default_report()
    if args.report_file:
        if not args.report_file.exists():
            print(f"error: report file not found: {args.report_file}", file=sys.stderr)
            return 2
        report_text = args.report_file.read_text(encoding="utf-8")

    try:
        insert_with_word(
            args.docx,
            output,
            report_text,
            args.editor_name,
            args.editor_initials,
            not args.no_track_changes,
            args.pdf_output,
        )
    except Exception as exc:  # Word COM failures should be clear to the caller.
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"updated: {output}")
    if args.pdf_output:
        print(f"pdf: {args.pdf_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
