#!/usr/bin/env python3
"""Create tracked, clean, and PDF delivery files from a copy-edited DOCX."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tracked_docx", type=Path, help="Tracked-change DOCX to package")
    parser.add_argument("--output-dir", type=Path, default=Path("output/doc"), help="Output directory")
    parser.add_argument("--stem", help="Output filename stem. Defaults to source stem.")
    parser.add_argument("--clean-copy", action="store_true", help="Create a clean DOCX by accepting revisions in a duplicate")
    parser.add_argument("--remove-comments", action="store_true", help="Remove comments from the clean copy")
    parser.add_argument("--pdf", action="store_true", help="Export a PDF check copy from the tracked DOCX")
    parser.add_argument(
        "--require-comment-author",
        action="append",
        default=[],
        help="Validate that the tracked copy contains this comment author before packaging. Repeatable.",
    )
    return parser.parse_args()


def open_word():
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "pywin32 is required for Word COM automation when creating clean copies or PDFs."
        ) from exc
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    return word


def accept_revisions(clean_path: Path, remove_comments: bool) -> None:
    word = open_word()
    doc = None
    try:
        doc = word.Documents.Open(str(clean_path.resolve()))
        doc.AcceptAllRevisions()
        if remove_comments:
            for index in range(doc.Comments.Count, 0, -1):
                doc.Comments(index).Delete()
        doc.SaveAs2(str(clean_path.resolve()))
    finally:
        if doc is not None:
            doc.Close(SaveChanges=True)
        word.Quit()


def export_pdf(docx_path: Path, pdf_path: Path) -> None:
    word = open_word()
    doc = None
    try:
        doc = word.Documents.Open(str(docx_path.resolve()))
        doc.ExportAsFixedFormat(str(pdf_path.resolve()), 17)  # wdExportFormatPDF
    finally:
        if doc is not None:
            doc.Close(SaveChanges=False)
        word.Quit()


def comment_authors(docx_path: Path) -> dict[str, int]:
    import zipfile
    from collections import Counter
    from xml.etree import ElementTree as ET

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    with zipfile.ZipFile(docx_path) as zf:
        if "word/comments.xml" not in zf.namelist():
            return {}
        root = ET.fromstring(zf.read("word/comments.xml").decode("utf-8"))
    authors: Counter[str] = Counter()
    for comment in root.findall(".//w:comment", ns):
        authors[comment.attrib.get(w + "author", "")] += 1
    return dict(authors)


def main() -> int:
    args = parse_args()
    if not args.tracked_docx.exists():
        print(f"error: file not found: {args.tracked_docx}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = args.stem or args.tracked_docx.stem
    tracked_out = args.output_dir / f"{stem}_copyedited_tracked.docx"
    clean_out = args.output_dir / f"{stem}_copyedited_clean.docx"
    pdf_out = args.output_dir / f"{stem}_copyedited_check.pdf"

    shutil.copy2(args.tracked_docx, tracked_out)
    authors = comment_authors(tracked_out)
    for author in args.require_comment_author:
        if authors.get(author, 0) <= 0:
            print(f"error: required comment author not found in tracked copy: {author}", file=sys.stderr)
            return 1
    print(f"tracked: {tracked_out}")

    try:
        if args.clean_copy:
            shutil.copy2(args.tracked_docx, clean_out)
            accept_revisions(clean_out, args.remove_comments)
            print(f"clean: {clean_out}")

        if args.pdf:
            export_pdf(tracked_out, pdf_out)
            print(f"pdf: {pdf_out}")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
