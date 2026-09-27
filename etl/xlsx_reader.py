"""Small dependency-free XLSX reader for the official source workbooks.

The Phase 1 ETL deliberately avoids converting source workbooks by hand.  This
module reads cells exactly as published, including inline strings and shared
strings, and exposes rows as dictionaries.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CELL_REF = re.compile(r"([A-Z]+)")


def _column_number(reference: str) -> int:
    match = CELL_REF.match(reference)
    if not match:
        raise ValueError(f"Invalid XLSX cell reference: {reference}")
    value = 0
    for letter in match.group(1):
        value = value * 26 + ord(letter) - ord("A") + 1
    return value - 1


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(node.itertext()) for node in root.findall(f"{{{MAIN_NS}}}si")]


def _sheet_path(archive: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationship_id = None
    for sheet in workbook.findall(f".//{{{MAIN_NS}}}sheet"):
        if sheet.attrib.get("name") == sheet_name:
            relationship_id = sheet.attrib[f"{{{REL_NS}}}id"]
            break
    if relationship_id is None:
        raise KeyError(f"Worksheet not found: {sheet_name}")

    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    for relationship in relationships.findall(f"{{{PKG_REL_NS}}}Relationship"):
        if relationship.attrib.get("Id") == relationship_id:
            target = relationship.attrib["Target"].lstrip("/")
            return target if target.startswith("xl/") else f"xl/{target}"
    raise KeyError(f"Worksheet relationship not found: {sheet_name}")


def iter_rows(path: Path, sheet_name: str) -> Iterator[list[str]]:
    """Yield worksheet rows, preserving empty cells between populated cells."""

    with zipfile.ZipFile(path) as archive:
        shared_strings = _shared_strings(archive)
        root = ET.fromstring(archive.read(_sheet_path(archive, sheet_name)))
        for row in root.findall(f".//{{{MAIN_NS}}}row"):
            values: list[str] = []
            for cell in row.findall(f"{{{MAIN_NS}}}c"):
                index = _column_number(cell.attrib["r"])
                while len(values) <= index:
                    values.append("")
                cell_type = cell.attrib.get("t")
                value_node = cell.find(f"{{{MAIN_NS}}}v")
                if cell_type == "s" and value_node is not None:
                    value = shared_strings[int(value_node.text or "0")]
                elif cell_type == "inlineStr":
                    inline = cell.find(f"{{{MAIN_NS}}}is")
                    value = "" if inline is None else "".join(inline.itertext())
                else:
                    value = "" if value_node is None else (value_node.text or "")
                values[index] = value.strip()
            yield values


def read_dicts(path: Path, sheet_name: str) -> list[dict[str, str]]:
    rows = iter_rows(path, sheet_name)
    headers = next(rows)
    result: list[dict[str, str]] = []
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        result.append(dict(zip(headers, padded)))
    return result
