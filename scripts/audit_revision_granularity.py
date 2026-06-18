#!/usr/bin/env python3
"""Audit large delete+insert tracked-change blocks in DOCX paragraphs."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def read_document_root(path: Path) -> ET.Element:
    with zipfile.ZipFile(path) as zf:
        if "word/document.xml" not in zf.namelist():
            raise ValueError("Not a DOCX file: word/document.xml is missing")
        return ET.fromstring(zf.read("word/document.xml").decode("utf-8"))


def joined_text(element: ET.Element, tag: str) -> str:
    return "".join(node.text or "" for node in element.findall(f".//w:{tag}", NS))


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def paragraph_text(paragraph: ET.Element) -> str:
    return joined_text(paragraph, "t") + joined_text(paragraph, "delText")


def audit(path: Path, min_words: int = 25, ratio_threshold: float = 0.45) -> dict[str, Any]:
    root = read_document_root(path)
    issues: list[dict[str, Any]] = []
    paragraphs_checked = 0

    for index, paragraph in enumerate(root.findall(".//w:p", NS), start=1):
        full_text = paragraph_text(paragraph)
        total_words = max(word_count(full_text), 1)
        deleted_text = joined_text(paragraph, "delText")
        inserted_text = ""
        for insertion in paragraph.findall(".//w:ins", NS):
            inserted_text += joined_text(insertion, "t")

        deleted_words = word_count(deleted_text)
        inserted_words = word_count(inserted_text)
        if deleted_words or inserted_words:
            paragraphs_checked += 1

        deletion_ratio = deleted_words / total_words
        insertion_ratio = inserted_words / total_words
        if (
            deleted_words >= min_words
            and inserted_words >= min_words
            and deletion_ratio >= ratio_threshold
            and insertion_ratio >= ratio_threshold
        ):
            issues.append(
                {
                    "paragraph": index,
                    "total_words": total_words,
                    "deleted_words": deleted_words,
                    "inserted_words": inserted_words,
                    "deletion_ratio": round(deletion_ratio, 3),
                    "insertion_ratio": round(insertion_ratio, 3),
                    "deleted_sample": deleted_text.strip()[:180],
                    "inserted_sample": inserted_text.strip()[:180],
                }
            )

    return {
        "file": str(path),
        "paragraphs_with_revisions_checked": paragraphs_checked,
        "large_replacement_count": len(issues),
        "large_replacements": issues,
        "warnings": build_warnings(issues),
    }


def build_warnings(issues: list[dict[str, Any]]) -> list[str]:
    if not issues:
        return []
    return [
        f"{len(issues)} paragraph(s) contain large paired deletion/insertion blocks; redo as local edits unless intentional."
    ]


def markdown_summary(result: dict[str, Any]) -> str:
    lines = [
        "# Revision Granularity Audit Summary",
        "",
        f"File: `{result['file']}`",
        f"Paragraphs with revisions checked: `{result['paragraphs_with_revisions_checked']}`",
        "",
        "## Key Issues",
    ]
    if result["warnings"]:
        lines.extend(f"- {warning}" for warning in result["warnings"])
    else:
        lines.append("- No large paragraph-level delete+insert replacement patterns detected.")

    lines.extend(["", "## Details"])
    if not result["large_replacements"]:
        lines.append("- None detected.")
    else:
        for item in result["large_replacements"][:100]:
            lines.append(
                "- Paragraph {paragraph}: deleted {deleted_words} words ({deletion_ratio}), "
                "inserted {inserted_words} words ({insertion_ratio}).".format(**item)
            )
            lines.append(f"  Deleted sample: {item['deleted_sample']}")
            lines.append(f"  Inserted sample: {item['inserted_sample']}")

    lines.extend(
        [
            "",
            "## Report-Ready Note",
            "This audit flags paragraph-scale replacement patterns. Confirm visually in Word, then redo normal copyediting changes as smaller local tracked edits.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="DOCX file to audit")
    parser.add_argument("--min-words", type=int, default=25, help="Minimum deleted and inserted words to flag")
    parser.add_argument("--ratio-threshold", type=float, default=0.45, help="Minimum paragraph ratio for delete and insert blocks")
    parser.add_argument("--json-output", type=Path, help="Write JSON audit to this path")
    parser.add_argument("--summary-output", type=Path, help="Write Markdown summary to this path")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit with status 1 if large replacements are detected")
    args = parser.parse_args()

    try:
        result = audit(args.docx, args.min_words, args.ratio_threshold)
    except (FileNotFoundError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    json_text = json.dumps(result, ensure_ascii=False, indent=2)
    summary = markdown_summary(result)
    if args.json_output:
        args.json_output.write_text(json_text + "\n", encoding="utf-8")
    if args.summary_output:
        args.summary_output.write_text(summary, encoding="utf-8")

    if not args.json_output and not args.summary_output:
        print(json_text)
    else:
        print(summary)

    if args.fail_on_issues and result["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
