#!/usr/bin/env python3
"""Audit obvious formatting drift in DOCX tracked insertions."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def read_xml(path: Path, part: str) -> ET.Element:
    with zipfile.ZipFile(path) as zf:
        if part not in zf.namelist():
            raise ValueError(f"DOCX part not found: {part}")
        return ET.fromstring(zf.read(part).decode("utf-8"))


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child_value(element: ET.Element | None, child_name: str) -> str:
    if element is None:
        return ""
    child = element.find(f"w:{child_name}", NS)
    if child is None:
        return ""
    return child.attrib.get(W + "val", "present")


def run_text(run: ET.Element) -> str:
    return "".join(node.text or "" for node in run.findall(".//w:t", NS))


def run_signature(run: ET.Element) -> dict[str, str]:
    rpr = run.find("w:rPr", NS)
    fonts = rpr.find("w:rFonts", NS) if rpr is not None else None
    return {
        "style": child_value(rpr, "rStyle"),
        "font_ascii": fonts.attrib.get(W + "ascii", "") if fonts is not None else "",
        "font_hansi": fonts.attrib.get(W + "hAnsi", "") if fonts is not None else "",
        "font_eastasia": fonts.attrib.get(W + "eastAsia", "") if fonts is not None else "",
        "size": child_value(rpr, "sz"),
        "bold": "1" if rpr is not None and rpr.find("w:b", NS) is not None else "",
        "italic": "1" if rpr is not None and rpr.find("w:i", NS) is not None else "",
        "underline": child_value(rpr, "u"),
        "color": child_value(rpr, "color"),
    }


def paragraph_runs(paragraph: ET.Element) -> list[ET.Element]:
    return [child for child in paragraph.iter() if local_name(child.tag) == "r"]


def is_inserted_run(run: ET.Element, paragraph: ET.Element) -> bool:
    parent_map = {child: parent for parent in paragraph.iter() for child in parent}
    current = run
    while current in parent_map:
        current = parent_map[current]
        if local_name(current.tag) == "ins":
            return True
    return False


def majority_signature(signatures: list[dict[str, str]]) -> dict[str, str]:
    result: dict[str, str] = {}
    keys = sorted({key for signature in signatures for key in signature})
    for key in keys:
        values = [signature.get(key, "") for signature in signatures if signature.get(key, "")]
        if values:
            result[key] = Counter(values).most_common(1)[0][0]
        else:
            result[key] = ""
    return result


def signature_diff(inserted: dict[str, str], baseline: dict[str, str]) -> dict[str, dict[str, str]]:
    diff: dict[str, dict[str, str]] = {}
    for key, expected in baseline.items():
        actual = inserted.get(key, "")
        if expected and actual and actual != expected:
            diff[key] = {"expected": expected, "actual": actual}
    return diff


def audit(path: Path) -> dict[str, Any]:
    root = read_xml(path, "word/document.xml")
    issues: list[dict[str, Any]] = []
    paragraph_count = 0
    inserted_run_count = 0

    for paragraph_index, paragraph in enumerate(root.findall(".//w:p", NS), start=1):
        runs = paragraph_runs(paragraph)
        if not runs:
            continue
        paragraph_count += 1
        inserted_runs = [run for run in runs if is_inserted_run(run, paragraph)]
        normal_runs = [run for run in runs if not is_inserted_run(run, paragraph) and run_text(run).strip()]
        if not inserted_runs or not normal_runs:
            continue

        baseline = majority_signature([run_signature(run) for run in normal_runs])
        for run in inserted_runs:
            text = run_text(run).strip()
            if not text:
                continue
            inserted_run_count += 1
            diff = signature_diff(run_signature(run), baseline)
            if diff:
                issues.append(
                    {
                        "paragraph": paragraph_index,
                        "text_sample": text[:80],
                        "differences": diff,
                    }
                )

    return {
        "file": str(path),
        "paragraphs_checked": paragraph_count,
        "inserted_runs_checked": inserted_run_count,
        "formatting_drift_count": len(issues),
        "formatting_drift": issues,
        "warnings": build_warnings(issues),
    }


def build_warnings(issues: list[dict[str, Any]]) -> list[str]:
    if not issues:
        return []
    return [f"{len(issues)} inserted tracked-change run(s) have formatting that differs from nearby paragraph text."]


def markdown_summary(result: dict[str, Any]) -> str:
    lines = [
        "# Formatting Audit Summary",
        "",
        f"File: `{result['file']}`",
        f"Inserted runs checked: `{result['inserted_runs_checked']}`",
        "",
        "## Key Issues",
    ]
    if result["warnings"]:
        lines.extend(f"- {warning}" for warning in result["warnings"])
    else:
        lines.append("- No obvious inserted-run formatting drift detected.")

    lines.extend(["", "## Details"])
    if not result["formatting_drift"]:
        lines.append("- None detected.")
    else:
        for item in result["formatting_drift"][:100]:
            diffs = "; ".join(
                f"{key}: expected {value['expected']}, actual {value['actual']}"
                for key, value in item["differences"].items()
            )
            lines.append(f"- Paragraph {item['paragraph']}, `{item['text_sample']}`: {diffs}")

    lines.extend(
        [
            "",
            "## Report-Ready Note",
            "This audit checks explicit run formatting on tracked insertions against nearby paragraph text. Word styles may inherit formatting not visible in raw XML, so confirm flagged issues visually in Word/PDF.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path, help="DOCX file to audit")
    parser.add_argument("--json-output", type=Path, help="Write JSON audit to this path")
    parser.add_argument("--summary-output", type=Path, help="Write Markdown summary to this path")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit with status 1 if formatting drift is detected")
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
