#!/usr/bin/env python3
"""Acquire official REGCESS detail coordinates for the U.20 public result set."""

from __future__ import annotations

import argparse
import http.cookiejar
import json
from pathlib import Path
import re
import time
from urllib.parse import urlencode, urljoin
from urllib.request import HTTPCookieProcessor, Request, build_opener

from regcess_reader import read_result_html

BASE = "https://regcess.mscbs.es/regcessWeb/"
START = BASE + "inicioBuscarCentrosAction.do"
TOKEN_NAME = "org.apache.struts.taglib.html.TOKEN"


def token_from(html: str) -> str:
    match = re.search(r'name="org\.apache\.struts\.taglib\.html\.TOKEN" value="([^"]+)', html)
    if not match:
        raise ValueError("REGCESS token not found")
    return match.group(1)


def post(opener, url: str, data: dict[str, str]) -> str:
    request = Request(url, data=urlencode(data).encode(), headers={"User-Agent": "PedsData-Canarias/phase1 research"})
    for attempt in range(3):
        try:
            return opener.open(request, timeout=60).read().decode("iso-8859-1")
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def new_search():
    opener = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))
    landing = opener.open(Request(START, headers={"User-Agent": "PedsData-Canarias/phase1 research"}), timeout=60).read().decode("iso-8859-1")
    action = re.search(r'<form name="buscarCentrosForm" method="POST" action="([^"]+)', landing)
    if not action:
        raise ValueError("REGCESS search action not found")
    fields = {
        TOKEN_NAME: token_from(landing), "metodo": "", "comboPadre": "",
        "vieneDesdePantallaFormulario": "true", "codCentro": "",
        "codAgente": "3", "provincia": "-1", "municipio": "-1",
        "codTipoVia": "-1", "nombreVia": "", "numeroVia": "",
        "nombreCentro": "", "codServicio": "U20", "codTipoDependencia": "0",
    }
    return opener, post(opener, urljoin(BASE, action.group(1)), fields)


def move_to_page(opener, html: str, page_number: int) -> str:
    for requested in range(2, page_number + 1):
        html = post(opener, BASE + "tramitarBuscarCentrosAction2.do", {
            TOKEN_NAME: token_from(html), "numeroPaginaSolicitada": str(requested),
            "campoOrdenacion": "", "sentidoOrdenacion": "",
        })
    return html


def detail_values(html: str) -> dict[str, object]:
    coordinate = re.search(r"Coord1=([-0-9.]+),([-0-9.]+)", html)
    ccn = re.search(r'class="etiquetaSeccionDetalleCentro ">CCN</div>\s*<div class="campoSeccionDetalleCentro">([^<]+)', html)
    if not ccn:
        raise ValueError("CCN missing from REGCESS detail")
    codes = sorted(set(re.findall(r"\bU[.]?(\d{1,3})\b", html)))
    return {
        "ccn": ccn.group(1).strip(),
        "latitude": float(coordinate.group(1)) if coordinate else None,
        "longitude": float(coordinate.group(2)) if coordinate else None,
        "service_codes": [f"U{code}" for code in codes],
    }


def detail_page(opener, token: str, record_id: str, next_center: bool) -> str:
    return post(opener, BASE + "obtenerDetalleCentroAction.do", {
        TOKEN_NAME: token, "codRegistro": record_id,
        "siguienteCentro": "true" if next_center else "false",
        "anteriorCentro": "false",
    })


def acquire_page(page_number: int, cache: dict[str, object], cache_path: Path) -> None:
    opener, listing = new_search()
    listing = move_to_page(opener, listing, page_number)
    records = read_result_html(listing)
    if not records:
        raise ValueError(f"No REGCESS records on page {page_number}")
    detail = detail_page(opener, token_from(listing), records[0]["registry_record_id"], False)
    current_record_id = records[0]["registry_record_id"]
    for index, expected in enumerate(records):
        if index:
            detail = detail_page(opener, token_from(detail), current_record_id, True)
            current_record_id = expected["registry_record_id"]
        values = detail_values(detail)
        if values["ccn"] != expected["ccn"]:
            raise ValueError(f"REGCESS sequence mismatch: {values['ccn']} != {expected['ccn']}")
        cache[expected["ccn"]] = values
        if (index + 1) % 10 == 0 or index + 1 == len(records):
            cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"page {page_number}: {index + 1}/{len(records)}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw/regcess_u20_public_details.json"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cache = json.loads(args.output.read_text()) if args.output.exists() else {}
    for page_number in range(1, 5):
        acquire_page(page_number, cache, args.output)
    print(f"wrote {len(cache)} REGCESS details to {args.output}")


if __name__ == "__main__":
    main()
