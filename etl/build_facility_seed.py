#!/usr/bin/env python3
"""Build a non-routeable facility seed from official Ministry snapshots."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from regcess_reader import read_result_pages
from xlsx_reader import read_dicts

AP_URL = "https://www.sanidad.gob.es/estadEstudios/estadisticas/docs/siap/2026_C_Catal_Centros_AP.xlsx"
REGCESS_URL = "https://regcess.mscbs.es/regcessWeb/inicioBuscarCentrosAction.do"
CNH_URL = "https://www.sanidad.gob.es/estadEstudios/estadisticas/sisInfSanSNS/ofertaRecursos/hospitales/docs/CNH_2025.xlsx"
RETRIEVED_AT = "2026-09-27"

ISLAND_IDS = {
    "EL HIERRO": "el-hierro", "LA GOMERA": "la-gomera",
    "LA PALMA": "la-palma", "TENERIFE": "tenerife",
    "GRAN CANARIA": "gran-canaria", "FUERTEVENTURA": "fuerteventura",
    "LANZAROTE": "lanzarote",
}
HOSPITAL_ISLAND = {
    "0535001838": "gran-canaria", "0535001908": "fuerteventura",
    "0535003934": "lanzarote", "0538002288": "el-hierro",
    "0538002289": "la-gomera", "0538001821": "tenerife",
    "0535002243": "lanzarote", "0538002290": "la-palma",
    "0538001932": "tenerife",
}

FIELDS = (
    "facility_id", "official_id", "name", "island_id", "municipality_id",
    "municipality_name", "health_area_id", "health_zone_id",
    "health_zone_name_source", "facility_type", "latitude", "longitude",
    "address", "postal_code", "pediatrics_ap", "pediatric_emergency",
    "pediatric_inpatient", "neonatology", "nicu", "picu", "service_status",
    "source_url", "source_date", "verified_at", "verification_status",
    "registry_record_id", "notes",
)


def base(row: dict[str, str]) -> dict[str, str]:
    return {
        "facility_id": f"regcess:{row['ccn']}", "official_id": row["ccn"],
        "name": row["name"], "municipality_name": row["municipality"],
        "latitude": "", "longitude": "", "pediatric_emergency": "needs_validation",
        "neonatology": "needs_validation", "nicu": "needs_validation",
        "picu": "needs_validation", "service_status": "observed",
        "source_url": REGCESS_URL, "verified_at": RETRIEVED_AT,
        "verification_status": "NEEDS_VALIDATION",
        "registry_record_id": row["registry_record_id"],
    }


def build(raw_dir: Path) -> list[dict[str, str]]:
    ap = read_dicts(raw_dir / "2026_C_Catal_Centros_AP.xlsx", "Catálogo - 2026")
    ap_by_ccn = {r["CODIGO_CCN"].zfill(10): r for r in ap if r.get("SIAP_CCAA.NOMBRE") == "CANARIAS"}
    cnh = read_dicts(raw_dir / "CNH_2025.xlsx", "DIRECTORIO DE HOSPITALES")
    hospital_by_ccn = {r["CCN"].zfill(10): r for r in cnh if r.get("CCAA") == "Canarias"}
    registry = read_result_pages(sorted(raw_dir.glob("regcess_canarias_u20_public_p*.html")))
    facilities: list[dict[str, str]] = []
    for reg in registry:
        if reg["center_class"] in {"Centros de salud", "Consultorios de atencion primaria"}:
            facilities.append(build_ap(reg, ap_by_ccn.get(reg["ccn"])))
        elif "Hospitales" in reg["center_class"]:
            facilities.append(build_hospital(reg, hospital_by_ccn.get(reg["ccn"])))
    return sorted(facilities, key=lambda r: (r["island_id"], r["name"]))


def build_ap(reg: dict[str, str], ap: dict[str, str] | None) -> dict[str, str]:
    facility = base(reg)
    facility.update({"municipality_id": "", "health_zone_id": "",
                     "pediatrics_ap": "observed", "pediatric_inpatient": "not_available"})
    if ap is None:
        # Both unmatched records are in Tenerife municipalities.  Their island is
        # explicit in REGCESS, while their address and current AP membership are not.
        facility.update({
            "island_id": "tenerife", "health_area_id": "tenerife",
            "health_zone_name_source": "", "address": "", "postal_code": "",
            "facility_type": "primary_care_consultorio" if "Consultorios" in reg["center_class"] else "primary_care_center",
            "source_date": RETRIEVED_AT,
            "notes": "U.20 Pediatría consta en REGCESS, pero el CCN no aparece en el Catálogo AP 2026; dirección y vigencia pendientes.",
        })
        return facility
    island = ISLAND_IDS[ap["SIAP_AREASALUD_CD.NOMBRE"]]
    facility.update({
        "island_id": island, "health_area_id": island,
        "municipality_name": ap["MUNICIPIO"],
        "health_zone_name_source": ap["SIAP_ZONABASICA.NOMBRE"],
        "facility_type": "primary_care_center" if ap["TIPOCENTRO"] == "CENTRO SALUD" else "primary_care_consultorio",
        "address": ap["DIRECCION"], "postal_code": ap["CP"],
        "source_url": f"{REGCESS_URL}|{AP_URL}", "source_date": "2025-12-31",
        "notes": "U.20 Pediatría verificada en REGCESS; dirección, Área de Salud y nombre ZBS proceden del Catálogo AP 2026. El código ZBS queda pendiente del gate B.",
    })
    return facility


def build_hospital(reg: dict[str, str], hospital: dict[str, str] | None) -> dict[str, str]:
    if hospital is None:
        raise ValueError(f"Hospital missing from CNH 2025: {reg['ccn']}")
    island = HOSPITAL_ISLAND[reg["ccn"]]
    facility = base(reg)
    facility.update({
        "island_id": island, "municipality_id": hospital["Cód. Municipio"],
        "municipality_name": hospital["Municipio"], "health_area_id": island,
        "health_zone_id": "", "health_zone_name_source": "", "facility_type": "hospital",
        "address": hospital["Dirección"], "postal_code": hospital["Código Postal"],
        "pediatrics_ap": "not_available", "pediatric_inpatient": "needs_validation",
        "source_url": f"{REGCESS_URL}|{CNH_URL}", "source_date": "2024-12-31",
        "notes": "U.20 Pediatría verificada en REGCESS y hospital con internamiento en CNH 2025. U.20 no demuestra por sí sola ingreso pediátrico, urgencia diferenciada, UCIN ni UCIP.",
    })
    return facility


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/staging/pediatric_facility_seed.csv"))
    args = parser.parse_args()
    facilities = build(args.raw_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(facilities)
    print(f"wrote {len(facilities)} facilities to {args.output}")


if __name__ == "__main__":
    main()
