#!/usr/bin/env python3
"""Validate the preserved stock-analysis archive without executing it."""

from __future__ import annotations

import csv
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "green_stocks_javascript.xlsx"
CSV_PATHS = (
    ROOT / "data" / "2017_green_stocks.csv",
    ROOT / "data" / "2018_green_stocks.csv",
)
EXPECTED_COLUMNS = (
    "Ticker",
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
)
EXPECTED_SHEETS = ("2017", "2018", "DQ Analysis")
WORKBOOK_NAMESPACE = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
}


class ValidationError(RuntimeError):
    """Raised when a repository invariant is not satisfied."""


def validate_csv(path: Path) -> int:
    if not path.is_file():
        raise ValidationError(f"missing CSV snapshot: {path.relative_to(ROOT)}")

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        try:
            header = tuple(next(reader))
        except StopIteration as exc:
            raise ValidationError(f"empty CSV snapshot: {path.relative_to(ROOT)}") from exc

        if header != EXPECTED_COLUMNS:
            raise ValidationError(
                f"unexpected columns in {path.relative_to(ROOT)}: {header!r}"
            )

        row_count = 0
        for line_number, row in enumerate(reader, start=2):
            if len(row) != len(EXPECTED_COLUMNS):
                raise ValidationError(
                    f"{path.relative_to(ROOT)}:{line_number} has {len(row)} columns"
                )
            row_count += 1

    if row_count == 0:
        raise ValidationError(f"no data rows in {path.relative_to(ROOT)}")
    return row_count


def validate_workbook() -> tuple[str, ...]:
    if not WORKBOOK.is_file():
        raise ValidationError(f"missing workbook: {WORKBOOK.relative_to(ROOT)}")

    try:
        with ZipFile(WORKBOOK) as archive:
            corrupt_member = archive.testzip()
            if corrupt_member is not None:
                raise ValidationError(f"corrupt workbook member: {corrupt_member}")

            names = set(archive.namelist())
            required_members = {"[Content_Types].xml", "xl/workbook.xml"}
            missing_members = sorted(required_members - names)
            if missing_members:
                raise ValidationError(
                    f"workbook is missing required members: {', '.join(missing_members)}"
                )

            unsafe_members = sorted(
                name
                for name in names
                if name.casefold().endswith("vbaproject.bin")
                or name.casefold().startswith("customui/")
            )
            if unsafe_members:
                raise ValidationError(
                    f"unexpected executable workbook content: {', '.join(unsafe_members)}"
                )

            content_types = archive.read("[Content_Types].xml").decode("utf-8")
            if "macroEnabled" in content_types:
                raise ValidationError("workbook declares a macro-enabled content type")

            workbook_root = ET.fromstring(archive.read("xl/workbook.xml"))
    except (BadZipFile, ET.ParseError) as exc:
        raise ValidationError(f"invalid Open XML workbook: {exc}") from exc

    sheet_names = tuple(
        node.attrib["name"]
        for node in workbook_root.findall(
            "main:sheets/main:sheet", WORKBOOK_NAMESPACE
        )
    )
    if sheet_names != EXPECTED_SHEETS:
        raise ValidationError(
            f"unexpected worksheet sequence: {sheet_names!r}; expected {EXPECTED_SHEETS!r}"
        )
    return sheet_names


def main() -> int:
    try:
        csv_counts = {path.name: validate_csv(path) for path in CSV_PATHS}
        sheet_names = validate_workbook()
    except ValidationError as exc:
        print(f"archive validation failed: {exc}", file=sys.stderr)
        return 1

    print("archive validation passed")
    for filename, row_count in csv_counts.items():
        print(f"- {filename}: {row_count} data rows")
    print(f"- workbook sheets: {', '.join(sheet_names)}")
    print("- executable VBA content: absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
