"""Parse REGCESS result pages saved by the source acquisition step."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


HEADERS = (
    "ccn",
    "name",
    "authorization_id",
    "autonomous_community",
    "province",
    "municipality",
    "center_class",
    "functional_dependency",
    "registry_record_id",
)


class _ResultTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_result_table = False
        self.in_cell = False
        self.current_cell: list[str] = []
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "table" and "tableMain" in (attributes.get("class") or ""):
            self.in_result_table = True
        elif self.in_result_table and tag == "tr":
            self.current_row = []
        elif self.in_result_table and tag == "td":
            self.in_cell = True
            self.current_cell = []
        elif self.in_result_table and self.in_cell and tag == "a":
            href = attributes.get("href") or ""
            marker = "detalleCentro('"
            if marker in href:
                self.current_cell.append(href.split(marker, 1)[1].split("'", 1)[0])

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.in_result_table and tag == "td":
            self.in_cell = False
            value = " ".join("".join(self.current_cell).split())
            if "Ver Detalle" in value:
                value = value.replace("Ver Detalle", "").strip()
            self.current_row.append(value)
        elif self.in_result_table and tag == "tr":
            if len(self.current_row) == len(HEADERS):
                self.rows.append(self.current_row)
        elif self.in_result_table and tag == "table":
            self.in_result_table = False


def read_result_pages(paths: list[Path]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in paths:
        parser = _ResultTableParser()
        parser.feed(path.read_text(encoding="iso-8859-1"))
        for row in parser.rows:
            record = dict(zip(HEADERS, row))
            if record["ccn"] in seen:
                continue
            seen.add(record["ccn"])
            records.append(record)
    return records


def read_result_html(content: str) -> list[dict[str, str]]:
    parser = _ResultTableParser()
    parser.feed(content)
    return [dict(zip(HEADERS, row)) for row in parser.rows]
