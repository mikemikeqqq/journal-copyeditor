#!/usr/bin/env python3
"""Heuristic statistics and numbering audit for academic DOCX manuscripts."""

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
P_VALUE_RE = re.compile(r"\b[Pp]\s*(=|<|>|<=|>=)\s*(0?\.\d+|\d+(?:\.\d+)?)")
CI_RE = re.compile(r"\b(?:\d{1,3}%\s*)?CI\b", re.IGNORECASE)
CI_BOUNDS_RE = re.compile(r"[\[(]\s*-?\d+(?:\.\d+)?\s*[,;\-\u2013]\s*-?\d+(?:\.\d+)?\s*[\])]")
N_RE = re.compile(r"\b[Nn]\s*=\s*\d+")
SIGNIFICANT_RE = re.compile(r"\b(significant|significantly|non-significant|nonsignificant)\b", re.IGNORECASE)
FIGURE_RE = re.compile(r"\b(?:Fig\.?|Figure)\s+(\d+)", re.IGNORECASE)
TABLE_RE = re.compile(r"\bTable\s+(\d+)", re.IGNORECASE)


def read_docx_paragraphs(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        if "word/document.xml" not in zf.namelist():
            raise ValueError("Not a DOCX file: word/document.xml is missing")
        xml = zf.read("word/document.xml").decode("utf-8")

    root = ET.fromstring(xml)
    paragraphs: list[str] = []
    for para in root.findall(".//w:p", NS):
        text = "".join(node.text or "" for node in para.findall(".//w:t", NS))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def sequence_gaps(numbers: list[int]) -> list[int]:
    if not numbers:
        return []
    unique = sorted(set(numbers))
    return [number for number in range(unique[0], unique[-1] + 1) if number not in unique]


def audit(path: Path) -> dict[str, Any]:
    paragraphs = read_docx_paragraphs(path)
    p_values = []
    invalid_p_values = []
    zero_p_values = []
    ci_without_bounds = []
    significant_without_stats = []
    sample_size_mentions = []
    figure_numbers = []
    table_numbers = []

    for index, paragraph in enumerate(paragraphs, start=1):
        p_matches = list(P_VALUE_RE.finditer(paragraph))
        for match in p_matches:
            value = float(match.group(2))
            record = {"paragraph": index, "value": match.group(0), "context": paragraph}
            p_values.append(record)
            if value > 1:
                invalid_p_values.append(record)
            if match.group(1) == "=" and value == 0:
                zero_p_values.append(record)

        if CI_RE.search(paragraph) and not CI_BOUNDS_RE.search(paragraph):
            ci_without_bounds.append({"paragraph": index, "context": paragraph})

        if SIGNIFICANT_RE.search(paragraph) and not (p_matches or CI_RE.search(paragraph)):
            significant_without_stats.append({"paragraph": index, "context": paragraph})

        if N_RE.search(paragraph):
            sample_size_mentions.append({"paragraph": index, "values": N_RE.findall(paragraph), "context": paragraph})

        figure_numbers.extend(int(match.group(1)) for match in FIGURE_RE.finditer(paragraph))
        table_numbers.extend(int(match.group(1)) for match in TABLE_RE.finditer(paragraph))

    result = {
        "file": str(path),
        "p_values": p_values,
        "invalid_p_values": invalid_p_values,
        "p_equals_zero_values": zero_p_values,
        "ci_without_bounds": ci_without_bounds,
        "significant_without_local_statistic": significant_without_stats,
        "sample_size_mentions": sample_size_mentions,
        "figure_numbers": sorted(set(figure_numbers)),
        "missing_figure_numbers": sequence_gaps(figure_numbers),
        "table_numbers": sorted(set(table_numbers)),
        "missing_table_numbers": sequence_gaps(table_numbers),
    }
    result["warnings"] = build_warnings(result)
    return result


def build_warnings(result: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if result["invalid_p_values"]:
        warnings.append(f"{len(result['invalid_p_values'])} p-value(s) are greater than 1.")
    if result["p_equals_zero_values"]:
        warnings.append(f"{len(result['p_equals_zero_values'])} p-value(s) are reported as exactly 0.")
    if result["ci_without_bounds"]:
        warnings.append(f"{len(result['ci_without_bounds'])} CI mention(s) may be missing bounds.")
    if result["significant_without_local_statistic"]:
        warnings.append(
            f"{len(result['significant_without_local_statistic'])} significance statement(s) lack a nearby p-value or CI."
        )
    if result["missing_figure_numbers"]:
        warnings.append(f"Possible missing figure number(s): {result['missing_figure_numbers']}.")
    if result["missing_table_numbers"]:
        warnings.append(f"Possible missing table number(s): {result['missing_table_numbers']}.")
    return warnings


def markdown_summary(result: dict[str, Any]) -> str:
    lines = [
        "# Statistics and Numbers Audit Summary",
        "",
        f"File: `{result['file']}`",
        "",
        "## Key Issues",
    ]
    if result["warnings"]:
        lines.extend(f"- {warning}" for warning in result["warnings"])
    else:
        lines.append("- No major statistics/numbering issues detected by the heuristic audit.")

    sections = [
        ("Invalid P Values", result["invalid_p_values"]),
        ("P Values Reported As Zero", result["p_equals_zero_values"]),
        ("CI Mentions Without Bounds", result["ci_without_bounds"]),
        ("Significant Language Without Nearby Statistic", result["significant_without_local_statistic"]),
    ]
    for title, items in sections:
        lines.extend(["", f"## {title}"])
        if not items:
            lines.append("- None detected.")
        else:
            for item in items[:50]:
                lines.append(f"- Paragraph {item['paragraph']}: {item['context']}")

    lines.extend(
        [
            "",
            "## Figure/Table Numbering",
            f"- Figures detected: {result['figure_numbers']}",
            f"- Missing figure numbers: {result['missing_figure_numbers']}",
            f"- Tables detected: {result['table_numbers']}",
            f"- Missing table numbers: {result['missing_table_numbers']}",
            "",
            "## Report-Ready Note",
            "This audit is heuristic. Verify flagged statistics and numbering issues against the manuscript tables, figures, and source data before changing values.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="DOCX manuscript to audit")
    parser.add_argument("--json-output", type=Path, help="Write full JSON audit to this path")
    parser.add_argument("--summary-output", type=Path, help="Write report-ready Markdown summary to this path")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit with status 1 if warnings are present")
    args = parser.parse_args()

    try:
        result = audit(args.docx)
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
