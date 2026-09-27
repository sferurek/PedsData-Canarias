#!/usr/bin/env python3
"""Geocode the pediatric facility seed with official CartoCiudad."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import json
from pathlib import Path
import re
import time
import unicodedata
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://www.cartociudad.es/geocoder/api/geocoder/candidates"
BOUNDS = {
    "el-hierro": (-18.20, -17.85, 27.60, 27.90),
    "la-gomera": (-17.40, -17.00, 28.00, 28.25),
    "la-palma": (-18.00, -17.65, 28.45, 28.90),
    "tenerife": (-16.95, -16.00, 27.95, 28.65),
    "gran-canaria": (-15.85, -15.35, 27.70, 28.20),
    "fuerteventura": (-14.55, -13.75, 28.00, 28.80),
    "lanzarote": (-13.90, -13.40, 28.80, 29.30),
}
EXTRA = ("geocoding_source", "geocoding_match_status",
         "geocoding_candidate_id", "geocoding_query", "registered_service_codes",
         "routing_eligible_pediatric_ap")


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c)).lower()
    return " ".join(re.findall(r"[a-z0-9]+", value))


def same_place(left: str, right: str) -> bool:
    return sorted(normalized(left).split()) == sorted(normalized(right).split())


def address_number(address: str) -> int | None:
    cleaned = re.sub(r"\bS\s*/?\s*N\b", "", address, flags=re.IGNORECASE)
    labelled = re.search(r"\bN(?:[º°O]|UMERO)?\s*(\d{1,4})", cleaned, flags=re.IGNORECASE)
    if labelled:
        return int(labelled.group(1))
    values = re.findall(r"\b(\d{1,4})\b", cleaned)
    return int(values[-1]) if values else None


def clean_query(address: str, municipality: str) -> str:
    value = re.sub(r"\bS\s*/?\s*N\b", "", address, flags=re.IGNORECASE)
    value = re.sub(r"\bN(?:[º°O]|UMERO)?\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"[,;]", " ", value)
    value = " ".join(value.split())
    return value + " " + municipality


def inside(row: dict[str, str], candidate: dict[str, object]) -> bool:
    lon, lat = candidate.get("lng"), candidate.get("lat")
    if not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)):
        return False
    west, east, south, north = BOUNDS[row["island_id"]]
    return west <= lon <= east and south <= lat <= north


def choose(row: dict[str, str], candidates: list[dict[str, object]]) -> tuple[dict[str, object] | None, str]:
    number = address_number(row["address"])
    scored: list[tuple[int, dict[str, object], bool, bool, bool]] = []
    for candidate in candidates:
        if candidate.get("comunidadAutonoma") != "Canarias" or not inside(row, candidate):
            continue
        municipality = same_place(row["municipality_name"], str(candidate.get("muni", "")))
        postal = not row["postal_code"] or row["postal_code"] == str(candidate.get("postalCode", ""))
        portal = number is not None and number == candidate.get("portalNumber")
        score = 4 * municipality + 3 * postal + 4 * portal + (candidate.get("type") == "portal")
        scored.append((score, candidate, municipality, postal, portal))
    if not scored:
        return None, "no_candidate"
    _, candidate, municipality, postal, portal = max(scored, key=lambda item: item[0])
    exact = municipality and postal and portal and candidate.get("type") == "portal"
    return candidate, "exact_portal" if exact else "approximate"


def fetch(row: dict[str, str]) -> tuple[str, str, list[dict[str, object]]]:
    if not row["address"]:
        return row["facility_id"], "", []
    query = clean_query(row["address"], row["municipality_name"])
    params = urlencode({"q": query, "limit": 10, "comunidad_autonoma_filter": "Canarias"})
    request = Request(f"{API}?{params}", headers={"User-Agent": "PedsData-Canarias/phase1 research"})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=45) as response:
                return row["facility_id"], query, json.load(response)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise AssertionError("unreachable")


def load_cache(path: Path) -> dict[str, dict[str, object]]:
    return json.loads(path.read_text()) if path.exists() else {}


def save_cache(path: Path, cache: dict[str, dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/staging/pediatric_facility_seed.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/curated/pediatric_facilities.csv"))
    parser.add_argument("--cache", type=Path, default=Path("data/raw/cartociudad_facility_geocodes_v2.json"))
    parser.add_argument("--regcess-details", type=Path, default=Path("data/raw/regcess_u20_public_details.json"))
    args = parser.parse_args()
    with args.input.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        rows = list(reader)
    cache = load_cache(args.cache)
    pending = [row for row in rows if row["facility_id"] not in cache and row["address"]]
    geocode_pending(pending, cache, args.cache)
    details = json.loads(args.regcess_details.read_text())
    write_curated(rows, cache, details, fieldnames, args.output)


def geocode_pending(rows, cache, cache_path):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fetch, row): row for row in rows}
        for index, future in enumerate(as_completed(futures), start=1):
            row = futures[future]
            try:
                facility_id, query, candidates = future.result()
                cache[facility_id] = {"query": query, "candidates": candidates, "error": ""}
            except Exception as error:
                cache[row["facility_id"]] = {"query": "", "candidates": [], "error": str(error)}
            if index % 10 == 0 or index == len(rows):
                save_cache(cache_path, cache)
                print(f"geocoded {index}/{len(rows)}", flush=True)


def write_curated(rows, cache, details, fieldnames, output):
    for row in rows:
        cached = cache.get(row["facility_id"], {"query": "", "candidates": []})
        candidate, match = choose(row, cached.get("candidates", []))
        row["geocoding_source"] = API
        row["geocoding_match_status"] = match
        row["geocoding_candidate_id"] = ""
        row["geocoding_query"] = str(cached.get("query", ""))
        row["registered_service_codes"] = "|".join(details[row["official_id"]]["service_codes"])
        if candidate:
            apply_candidate(row, candidate, match)
        apply_regcess_detail(row, details[row["official_id"]])
        apply_phase2_evidence(row)
        eligible = row["verification_status"] == "VERIFIED" and row["pediatrics_ap"] == "observed"
        row["routing_eligible_pediatric_ap"] = str(eligible).lower()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames + EXTRA)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} facilities to {output}")


def apply_regcess_detail(row, detail):
    services = set(detail["service_codes"])
    if row["facility_type"] == "hospital":
        row["pediatric_inpatient"] = "needs_validation"
        row["neonatology"] = "observed" if services & {"U22", "U23"} else "not_available"
        row["nicu"] = "observed" if "U23" in services else "not_available"
    if "U68" in services:
        row["notes"] += " U.68 Urgencias registrada; no prueba una urgencia pediátrica diferenciada."
    if detail["latitude"] is None:
        return
    row["latitude"] = str(detail["latitude"])
    row["longitude"] = str(detail["longitude"])
    row["geocoding_source"] = "REGCESS/eGeo"
    row["geocoding_match_status"] = "official_registry_point"
    row["geocoding_candidate_id"] = row["official_id"]
    mismatch = "no aparece en el Catálogo AP" in row["notes"]
    row["verification_status"] = "PARTIAL" if mismatch else "VERIFIED"
    row["notes"] += " Coordenada oficial publicada por REGCESS/eGeo."


def apply_phase2_evidence(row):
    """Apply dated SCS evidence that is stronger than registry-code inference."""
    official_id = row["official_id"]
    if official_id == "0538005432":
        row.update(verification_status="VERIFIED", health_zone_name_source="LOS SILOS-BUENAVISTA")
        row["source_url"] += "|https://www3.gobiernodecanarias.org/noticias/sanidad-invierte-mas-de-22-millones-de-euros-en-la-puesta-en-marcha-del-nuevo-consultorio-local-de-buenavista/"
        row["notes"] += " SCS confirma apertura, consulta de Pediatría y cobertura compartida con Los Silos (17/07/2025)."
    elif official_id == "0538005357":
        row["health_zone_name_source"] = "TACORONTE"
        row["source_url"] += "|https://www3.gobiernodecanarias.org/noticias/la-gerencia-de-atencion-primaria-de-tenerife-amplia-la-cartera-de-servicios-del-consultorio-local-de-el-sauzal/"
        row["notes"] += " SCS confirma Pediatría operativa; falta coordenada oficial."

    observed_all = {"0535001838", "0538001821", "0538001932"}
    if official_id in observed_all:
        for field in ("pediatric_emergency", "pediatric_inpatient", "neonatology", "nicu", "picu"):
            row[field] = "observed"
    hospital_sources = {
        "0535001838": "https://www3.gobiernodecanarias.org/sanidad/scs/scs/as/gc/30/memorias/24/docs/MEMORIA_%20CHUIMI_2024_DIGITAL.pdf",
        "0538001821": "https://www3.gobiernodecanarias.org/sanidad/scs/contenidoGenerico.jsp?idCarpeta=3da5f513-541b-11de-9665-998e1388f7ed&idDocument=1d1229fb-3520-11e0-919a-bdaa63e0a438",
        "0538001932": "https://www3.gobiernodecanarias.org/sanidad/scs/content/213b498d-c7e1-11e4-b8de-159dab37263e/PediatriayAreasEspecificas.pdf",
    }
    if official_id in hospital_sources:
        row["source_url"] += "|" + hospital_sources[official_id]

    partial_hospitals = {"0535002243", "0535001908", "0538002289", "0538002290"}
    if official_id in partial_hospitals:
        row["pediatric_inpatient"] = "observed"
    if official_id in {"0535002243", "0535001908"}:
        row["pediatric_emergency"] = "observed"
    partial_sources = {
        "0535002243": "https://www3.gobiernodecanarias.org/sanidad/scs/content/3017ea34-b2f5-11ef-ba3e-0f9d182f8154/Memoria-GSS-Lanzarote-2023.pdf",
        "0535001908": "https://www3.gobiernodecanarias.org/sanidad/scs/scs/ftv/at_especializada/hospital.jsp",
        "0538002289": "https://www3.gobiernodecanarias.org/sanidad/scs/contenidoGenerico.jsp?idCarpeta=7db198c4-ab2a-11dd-970d-d73a0633ac17&idDocument=b3596b34-4251-11df-875b-a3a23aaf73b8",
        "0538002290": "https://www3.gobiernodecanarias.org/sanidad/scs/contenidoGenerico.jsp?idCarpeta=d4df6819-5419-11de-9665-998e1388f7ed&idDocument=297458c3-50ff-11e3-a0f5-65699e4ff786",
    }
    if official_id in partial_sources:
        row["source_url"] += "|" + partial_sources[official_id]


def apply_candidate(row, candidate, match):
    row["latitude"] = str(candidate["lat"])
    row["longitude"] = str(candidate["lng"])
    row["geocoding_candidate_id"] = str(candidate.get("id", ""))
    row["verification_status"] = "VERIFIED" if match == "exact_portal" else "PARTIAL"
    row["notes"] += f" Geocodificación CartoCiudad: {match}."


if __name__ == "__main__":
    main()
