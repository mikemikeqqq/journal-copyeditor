#!/usr/bin/env python3
"""Heuristic citation/reference audit for academic DOCX manuscripts.

This script is intentionally conservative. It detects common author-date
problems and produces a JSON record plus a report-ready Markdown summary. It
does not replace a citation manager or a human reference check.
"""

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
YEAR_RE = re.compile(r"\b((?:18|19|20)\d{2})([a-z])?\b")
PAREN_CITATION_RE = re.compile(r"\(([^()]{0,500}(?:18|19|20)\d{2}[a-z]?[^()]*)\)")
NARRATIVE_CITATION_RE = re.compile(
    r"\b([A-Z][A-Za-z'\-]+(?:\s+et\s+al\.)?)\s*\(((?:18|19|20)\d{2}[a-z]?)\)"
)
REFERENCE_HEADING_RE = re.compile(r"^\s*(references|bibliography|works cited)\s*$", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://|doi\.org/", re.IGNORECASE)
VOLUME_RE = re.compile(r"\b\d{1,4}\s*(?:\(\d+\))?\s*[:,]\s*\d+")
PAGE_RE = re.compile(r"\b\d{1,6}\s*[-\u2013]\s*\d{1,6}\b|\be\d{3,}\b|\barticle\s+\d+\b", re.IGNORECASE)
NUMERIC_CITATION_RE = re.compile(r"\[(?:\d+(?:[-,\s]\d+)*)\]|\b\^\d+\b")


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


def split_body_references(paragraphs: list[str]) -> tuple[list[str], list[str], int | None]:
    for index, paragraph in enumerate(paragraphs):
        if REFERENCE_HEADING_RE.match(paragraph):
            return paragraphs[:index], paragraphs[index + 1 :], index
    return paragraphs, [], None


def normalize_author(author: str) -> str:
    author = re.sub(r"\bet\s+al\.?\b", "", author, flags=re.IGNORECASE)
    author = author.replace("&", " and ")
    author = re.sub(r"\b(see|e\.g\.|eg|cf|for example|and|also|in|by)\b", " ", author, flags=re.IGNORECASE)
    match = re.search(r"[A-Z][A-Za-z'\-]+", author)
    if not match:
        return ""
    return re.sub(r"[^a-z0-9]", "", match.group(0).lower())


def citation_key(author: str, year: str) -> str:
    normalized = normalize_author(author)
    return f"{normalized}:{year[:4]}" if normalized and year else ""


def split_citation_cluster(cluster: str) -> list[str]:
    parts = [part.strip() for part in cluster.split(";")]
    return [part for part in parts if YEAR_RE.search(part)]


def extract_parenthetical_citations(body_text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    citations: list[dict[str, Any]] = []
    unsorted_clusters: list[dict[str, Any]] = []

    for match in PAREN_CITATION_RE.finditer(body_text):
        cluster = match.group(1).strip()
        items = split_citation_cluster(cluster)
        parsed_items: list[dict[str, Any]] = []
        for item in items:
            year_match = YEAR_RE.search(item)
            if not year_match:
                continue
            year = year_match.group(1)
            author_text = item[: year_match.start()]
            key = citation_key(author_text, year)
            if not key:
                continue
            parsed = {
                "raw": item,
                "author": normalize_author(author_text),
                "year": year,
                "key": key,
                "cluster": f"({cluster})",
            }
            citations.append(parsed)
            parsed_items.append(parsed)

        if len(parsed_items) > 1:
            years = [int(item["year"]) for item in parsed_items]
            if years != sorted(years):
                sorted_items = sorted(parsed_items, key=lambda item: (int(item["year"]), item["raw"].lower()))
                unsorted_clusters.append(
                    {
                        "cluster": f"({cluster})",
                        "years": years,
                        "suggested_cluster": "(" + "; ".join(item["raw"] for item in sorted_items) + ")",
                    }
                )

    return citations, unsorted_clusters


def extract_narrative_citations(body_text: str) -> list[dict[str, Any]]:
    citations: list[dict[str, Any]] = []
    for match in NARRATIVE_CITATION_RE.finditer(body_text):
        author = match.group(1)
        year = match.group(2)[:4]
        key = citation_key(author, year)
        if key:
            citations.append(
                {
                    "raw": match.group(0),
                    "author": normalize_author(author),
                    "year": year,
                    "key": key,
                    "cluster": match.group(0),
                }
            )
    return citations


def group_reference_entries(reference_paragraphs: list[str]) -> list[str]:
    entries: list[str] = []
    current: list[str] = []
    for paragraph in reference_paragraphs:
        if YEAR_RE.search(paragraph) and (not current or re.match(r"^\s*(?:\d+\.?\s+)?[A-Z]", paragraph)):
            if current:
                entries.append(" ".join(current))
            current = [paragraph]
        elif current:
            current.append(paragraph)
        else:
            current = [paragraph]
    if current:
        entries.append(" ".join(current))
    return [entry.strip() for entry in entries if entry.strip()]


def parse_reference_entry(entry: str) -> dict[str, Any]:
    year_match = YEAR_RE.search(entry)
    year = year_match.group(1) if year_match else ""
    author_match = re.match(r"^\s*(?:\d+\.?\s+)?([A-Z][A-Za-z'\-]+)", entry)
    author = normalize_author(author_match.group(1)) if author_match else ""
    key = f"{author}:{year}" if author and year else ""

    missing: list[str] = []
    if not year:
        missing.append("year")
    if not DOI_RE.search(entry) and not URL_RE.search(entry):
        missing.append("doi_or_url")
    if not VOLUME_RE.search(entry):
        missing.append("volume_issue_or_locator")
    if not PAGE_RE.search(entry):
        missing.append("pages_or_article_number")

    # A rough signal that the journal/source title may be absent. This avoids
    # claiming certainty because books and reports use different metadata.
    if entry.count(".") < 2 and "," not in entry:
        missing.append("journal_or_source_title")

    return {
        "raw": entry,
        "author": author,
        "year": year,
        "key": key,
        "missing_metadata": missing,
        "doi": DOI_RE.search(entry).group(0) if DOI_RE.search(entry) else "",
    }


def audit(path: Path) -> dict[str, Any]:
    paragraphs = read_docx_paragraphs(path)
    body_paragraphs, reference_paragraphs, reference_heading_index = split_body_references(paragraphs)
    body_text = " ".join(body_paragraphs)

    parenthetical_citations, unsorted_clusters = extract_parenthetical_citations(body_text)
    narrative_citations = extract_narrative_citations(body_text)
    citations = parenthetical_citations + narrative_citations
    citation_keys = sorted({item["key"] for item in citations if item["key"]})

    reference_entries = group_reference_entries(reference_paragraphs)
    references = [parse_reference_entry(entry) for entry in reference_entries]
    reference_keys = sorted({item["key"] for item in references if item["key"]})

    missing_references = sorted(set(citation_keys) - set(reference_keys))
    uncited_references = sorted(set(reference_keys) - set(citation_keys))

    reference_authors = {}
    for item in references:
        if item["author"]:
            reference_authors.setdefault(item["author"], set()).add(item["year"])

    possible_author_year_mismatches = []
    for key in missing_references:
        author, year = key.split(":", 1)
        if author in reference_authors:
            possible_author_year_mismatches.append(
                {
                    "citation_key": key,
                    "reference_years_for_author": sorted(reference_authors[author]),
                }
            )

    metadata_issues = [
        {
            "key": item["key"],
            "missing_metadata": item["missing_metadata"],
            "reference": item["raw"],
        }
        for item in references
        if item["missing_metadata"]
    ]

    likely_numeric_style = bool(NUMERIC_CITATION_RE.search(body_text)) and len(citations) < 3

    return {
        "file": str(path),
        "reference_heading_found": reference_heading_index is not None,
        "likely_numeric_style": likely_numeric_style,
        "citation_count": len(citations),
        "unique_citation_keys": citation_keys,
        "reference_count": len(references),
        "unique_reference_keys": reference_keys,
        "missing_references_for_citations": missing_references,
        "uncited_references": uncited_references,
        "possible_author_year_mismatches": possible_author_year_mismatches,
        "unsorted_citation_clusters": unsorted_clusters,
        "metadata_issues": metadata_issues,
        "warnings": build_warnings(
            reference_heading_index,
            likely_numeric_style,
            missing_references,
            uncited_references,
            possible_author_year_mismatches,
            unsorted_clusters,
            metadata_issues,
        ),
    }


def build_warnings(
    reference_heading_index: int | None,
    likely_numeric_style: bool,
    missing_references: list[str],
    uncited_references: list[str],
    possible_author_year_mismatches: list[dict[str, Any]],
    unsorted_clusters: list[dict[str, Any]],
    metadata_issues: list[dict[str, Any]],
) -> list[str]:
    warnings: list[str] = []
    if reference_heading_index is None:
        warnings.append("Reference heading was not found; reference matching is incomplete.")
    if likely_numeric_style:
        warnings.append("The manuscript appears to use a numeric citation style; author-date checks may not apply.")
    if missing_references:
        warnings.append(f"{len(missing_references)} in-text citation key(s) were not found in the reference list.")
    if uncited_references:
        warnings.append(f"{len(uncited_references)} reference-list key(s) were not found in in-text citations.")
    if possible_author_year_mismatches:
        warnings.append(f"{len(possible_author_year_mismatches)} possible author-year mismatch(es) detected.")
    if unsorted_clusters:
        warnings.append(f"{len(unsorted_clusters)} citation cluster(s) are not sorted by publication year.")
    if metadata_issues:
        warnings.append(f"{len(metadata_issues)} reference entry or entries have possible missing metadata.")
    return warnings


def markdown_summary(result: dict[str, Any]) -> str:
    lines = [
        "# Citation and Reference Audit Summary",
        "",
        f"File: `{result['file']}`",
        f"Reference heading found: `{result['reference_heading_found']}`",
        f"Likely numeric style: `{result['likely_numeric_style']}`",
        f"In-text citations detected: `{result['citation_count']}`",
        f"Reference entries detected: `{result['reference_count']}`",
        "",
        "## Key Issues",
    ]
    if result["warnings"]:
        lines.extend(f"- {warning}" for warning in result["warnings"])
    else:
        lines.append("- No major citation/reference issues detected by the heuristic audit.")

    def add_items(title: str, items: list[Any], formatter) -> None:
        lines.extend(["", f"## {title}"])
        if not items:
            lines.append("- None detected.")
        else:
            lines.extend(f"- {formatter(item)}" for item in items[:50])

    add_items("Citation Keys Missing From References", result["missing_references_for_citations"], lambda item: f"`{item}`")
    add_items("Uncited Reference Keys", result["uncited_references"], lambda item: f"`{item}`")
    add_items(
        "Possible Author-Year Mismatches",
        result["possible_author_year_mismatches"],
        lambda item: f"`{item['citation_key']}`; reference years for author: {', '.join(item['reference_years_for_author'])}",
    )
    add_items(
        "Unsorted Citation Clusters",
        result["unsorted_citation_clusters"],
        lambda item: f"{item['cluster']} -> suggested {item['suggested_cluster']}",
    )
    add_items(
        "Reference Metadata Issues",
        result["metadata_issues"],
        lambda item: f"`{item['key'] or 'unknown'}` missing {', '.join(item['missing_metadata'])}: {item['reference']}",
    )

    lines.extend(
        [
            "",
            "## Report-Ready Note",
            "This audit is heuristic. Verify all flagged citation and reference issues against the target journal style and the author's citation manager before submission.",
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
