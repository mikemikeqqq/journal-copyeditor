#!/usr/bin/env python3
"""Validate a DOCX tracked-change copy-edit deliverable."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

CJK_CLASS = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
CJK_RE = re.compile(f"[{CJK_CLASS}]")
CJK_RUN_RE = re.compile(f"[{CJK_CLASS}]{{2,}}")
REPLACEMENT_RE = re.compile(r"\ufffd")
WORD_TEXT_PART_RE = re.compile(r"^word/(document|footnotes|endnotes|header\d+|footer\d+)\.xml$")
WORD_XML_RE = re.compile(r"^word/.*\.xml$")
REPORT_HEADING_RE = re.compile(r"copy\s+editing\s+and\s+proofreading\s+report", re.IGNORECASE)


def read_zip_text(zf: zipfile.ZipFile, name: str) -> str:
    with zf.open(name) as f:
        return f.read().decode("utf-8")


def xml_text(xml: str, tag: str = "t") -> str:
    root = ET.fromstring(xml)
    return "".join(node.text or "" for node in root.findall(f".//w:{tag}", NS))


def analyze_text(text: str) -> dict[str, Any]:
    cjk_chars = CJK_RE.findall(text)
    cjk_runs = CJK_RUN_RE.findall(text)
    replacement_chars = REPLACEMENT_RE.findall(text)
    return {
        "length": len(text),
        "cjk_count": len(cjk_chars),
        "cjk_sample": "".join(cjk_chars[:30]),
        "cjk_run_count": len(cjk_runs),
        "cjk_run_sample": cjk_runs[:5],
        "replacement_char_count": len(replacement_chars),
    }


def comment_info(comments_xml: str | None) -> dict[str, Any]:
    if not comments_xml:
        return {"count": 0, "authors": {}, "ids": []}

    authors: Counter[str] = Counter()
    ids: list[str] = []
    root = ET.fromstring(comments_xml)
    for comment in root.findall(".//w:comment", NS):
        authors[comment.attrib.get(W + "author", "")] += 1
        comment_id = comment.attrib.get(W + "id")
        if comment_id is not None:
            ids.append(comment_id)
    return {"count": sum(authors.values()), "authors": dict(authors), "ids": ids}


def revision_counts(word_xml: str) -> dict[str, int]:
    counts = {
        "insertions": len(re.findall(r"<w:ins\b", word_xml)),
        "deletions": len(re.findall(r"<w:del\b", word_xml)),
        "move_from": len(re.findall(r"<w:moveFrom\b", word_xml)),
        "move_to": len(re.findall(r"<w:moveTo\b", word_xml)),
        "format_changes": len(re.findall(r"<w:[A-Za-z0-9]+PrChange\b", word_xml)),
    }
    counts["total"] = sum(counts.values())
    return counts


def analyze_docx(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        if "word/document.xml" not in names:
            raise ValueError("Not a valid DOCX package: word/document.xml is missing")

        text_parts = sorted(name for name in names if WORD_TEXT_PART_RE.match(name))
        word_xml_parts = sorted(name for name in names if WORD_XML_RE.match(name))

        visible_text_chunks: list[str] = []
        deleted_text_chunks: list[str] = []
        part_errors: list[str] = []
        for name in text_parts:
            xml = read_zip_text(zf, name)
            try:
                visible_text_chunks.append(xml_text(xml, "t"))
                deleted_text_chunks.append(xml_text(xml, "delText"))
            except ET.ParseError as exc:
                part_errors.append(f"{name}: XML parse error: {exc}")

        comments_xml = read_zip_text(zf, "word/comments.xml") if "word/comments.xml" in names else None
        comments_text = ""
        if comments_xml:
            try:
                comments_text = xml_text(comments_xml, "t")
                deleted_text_chunks.append(xml_text(comments_xml, "delText"))
            except ET.ParseError as exc:
                part_errors.append(f"word/comments.xml: XML parse error: {exc}")

        settings_xml = read_zip_text(zf, "word/settings.xml") if "word/settings.xml" in names else ""
        combined_word_xml = "\n".join(read_zip_text(zf, name) for name in word_xml_parts)

    body_text = "".join(visible_text_chunks)
    deleted_text = "".join(deleted_text_chunks)
    comments = comment_info(comments_xml)
    revisions = revision_counts(combined_word_xml)

    return {
        "file": str(path),
        "parts_checked": text_parts + (["word/comments.xml"] if comments_xml else []),
        "part_errors": part_errors,
        "body_visible": analyze_text(body_text),
        "comments_visible": analyze_text(comments_text),
        "deleted_revision_text": analyze_text(deleted_text),
        "copyediting_report_present": bool(REPORT_HEADING_RE.search(body_text)),
        "mojibake_suspect_count": (
            CJK_RUN_RE.subn("", body_text + comments_text)[1]
            + REPLACEMENT_RE.subn("", body_text + comments_text)[1]
        ),
        "revision_markers": revisions,
        "insertions": revisions["insertions"],
        "deletions": revisions["deletions"],
        "track_revisions_enabled": "<w:trackRevisions" in settings_xml,
        "comments": comments,
        "comment_authors": comments["authors"],
    }


def delta(output: dict[str, Any], source: dict[str, Any], section: str, key: str) -> int:
    return int(output[section][key]) - int(source[section][key])


def compare_to_source(output: dict[str, Any], source: dict[str, Any]) -> list[str]:
    warnings: list[str] = []

    if output["part_errors"]:
        warnings.extend(output["part_errors"])

    if not output["track_revisions_enabled"]:
        warnings.append("Track Changes is not enabled in word/settings.xml.")

    if output["comments"]["count"] < source["comments"]["count"]:
        warnings.append(
            f"Comment count decreased from {source['comments']['count']} to {output['comments']['count']}."
        )

    missing_comment_ids = sorted(set(source["comments"]["ids"]) - set(output["comments"]["ids"]))
    if missing_comment_ids:
        shown = ", ".join(missing_comment_ids[:10])
        suffix = " ..." if len(missing_comment_ids) > 10 else ""
        warnings.append(f"Source comment IDs missing from output: {shown}{suffix}")

    if output["revision_markers"]["total"] <= source["revision_markers"]["total"]:
        warnings.append(
            "Revision marker count did not increase; confirm the copyediting pass was performed with Track Changes on."
        )

    for section, label in (
        ("body_visible", "visible manuscript text"),
        ("comments_visible", "comment text"),
    ):
        cjk_delta = delta(output, source, section, "cjk_count")
        if cjk_delta > 0:
            warnings.append(f"New CJK characters detected in {label}: +{cjk_delta}.")

        run_delta = delta(output, source, section, "cjk_run_count")
        if run_delta > 0:
            warnings.append(f"New CJK text runs detected in {label}: +{run_delta}.")

        replacement_delta = delta(output, source, section, "replacement_char_count")
        if replacement_delta > 0:
            warnings.append(f"New Unicode replacement characters detected in {label}: +{replacement_delta}.")

    if output["mojibake_suspect_count"] > source["mojibake_suspect_count"]:
        warnings.append(
            "Mojibake-suspect count increased "
            f"from {source['mojibake_suspect_count']} to {output['mojibake_suspect_count']}."
        )

    return warnings


def check_required_comment_authors(result: dict[str, Any], required_authors: list[str]) -> list[str]:
    warnings: list[str] = []
    authors = result["comments"]["authors"]
    for author in required_authors:
        if authors.get(author, 0) <= 0:
            warnings.append(f"Required comment author not found in output comments: {author}.")
    return warnings


def suspicious_without_source(
    result: dict[str, Any],
    require_report: bool = False,
    required_comment_authors: list[str] | None = None,
) -> list[str]:
    warnings: list[str] = []
    if result["part_errors"]:
        warnings.extend(result["part_errors"])
    if result["body_visible"]["replacement_char_count"] or result["comments_visible"]["replacement_char_count"]:
        warnings.append("Unicode replacement characters detected.")
    if result["mojibake_suspect_count"]:
        warnings.append("CJK text runs or replacement characters detected; verify they are intentional.")
    if require_report and not result["copyediting_report_present"]:
        warnings.append("Copy Editing and Proofreading Report heading was not found.")
    if required_comment_authors:
        warnings.extend(check_required_comment_authors(result, required_comment_authors))
    return warnings


def print_text_report(result: dict[str, Any]) -> None:
    keys = [
        "file",
        "track_revisions_enabled",
        "insertions",
        "deletions",
        "comment_authors",
    ]
    for key in keys:
        print(f"{key}: {result[key]}")

    print(f"revision_markers: {result['revision_markers']}")
    print(f"comment_count: {result['comments']['count']}")
    print(f"copyediting_report_present: {result['copyediting_report_present']}")
    print(f"visible_cjk_count: {result['body_visible']['cjk_count']}")
    print(f"visible_cjk_sample: {result['body_visible']['cjk_sample']}")
    print(f"comment_cjk_count: {result['comments_visible']['cjk_count']}")
    print(f"mojibake_suspect_count: {result['mojibake_suspect_count']}")
    print(f"replacement_char_count: {result['body_visible']['replacement_char_count']}")

    warnings = result.get("warnings", [])
    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("warnings: []")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="DOCX file to validate")
    parser.add_argument("--source", type=Path, help="Original source DOCX for baseline comparison")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument(
        "--require-report",
        action="store_true",
        help="Warn when the in-document Copy Editing and Proofreading Report heading is missing",
    )
    parser.add_argument(
        "--require-comment-author",
        action="append",
        default=[],
        help="Warn when a required comment author, such as Catherine, is absent. Repeatable.",
    )
    parser.add_argument(
        "--fail-on-suspect",
        action="store_true",
        help="Exit with status 1 when corruption or preservation warnings are detected",
    )
    args = parser.parse_args()

    try:
        result = analyze_docx(args.docx)
        source_result = analyze_docx(args.source) if args.source else None
    except (FileNotFoundError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if source_result:
        result["source"] = source_result
        result["warnings"] = compare_to_source(result, source_result)
        if args.require_report and not result["copyediting_report_present"]:
            result["warnings"].append("Copy Editing and Proofreading Report heading was not found.")
        result["warnings"].extend(check_required_comment_authors(result, args.require_comment_author))
    else:
        result["warnings"] = suspicious_without_source(result, args.require_report, args.require_comment_author)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text_report(result)

    if args.fail_on_suspect and result["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
