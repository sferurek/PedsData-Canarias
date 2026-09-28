#!/usr/bin/env python3
"""Curate Phase 6B admissions from frozen primary sources."""
import csv
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PARSER = "phase6b-v1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_fields(key, sources):
    source = sources[key]
    return {
        "source_id": key,
        "source_url": source["source_url"],
        "dataset_version": source["dataset_version"],
        "checksum": source["checksum"],
        "retrieved_at": source["retrieved_at"],
        "license_url": source["license_url"],
        "parser_version": PARSER,
    }


def read_semicolon(path, encoding="utf-8-sig"):
    with path.open(encoding=encoding, newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def bdcap(sources):
    output = []
    source = source_fields("bdcap_obesity", sources)
    rows = read_semicolon(ROOT / sources["bdcap_obesity"]["path"], "latin-1")
    for row in rows:
        rate = float(row["Personas con problemas de salud por mil asignadas"].replace(",", "."))
        cases = float(row["Casos"].replace(",", "."))
        output.append(source | {
            "indicator_id": "obesity_active_problem_registered",
            "indicator_label": "Obesidad registrada como problema activo",
            "reference_period": row["Año"],
            "geography_level": "autonomous_community",
            "geography_id": "canarias",
            "age_group_original": "00-14 años",
            "universe": "Población asignada a Atención Primaria incluida en la muestra BDCAP",
            "value": rate,
            "unit": "persons_per_1000_assigned",
            "weighted_cases": cases,
            "denominator": "",
            "denominator_definition": "Población asignada de 0-14 años; el export no publica su valor numérico",
            "weighting": "Estimación BDCAP ponderada por CCAA, sexo, edad quinquenal y país de nacimiento",
            "value_status": "WEIGHTED_SAMPLE",
            "comparability_status": "ADMIT_WITH_LIMITATIONS",
            "method_id": "bdcap_registered_morbidity_v1",
        })
    if [int(row["reference_period"]) for row in output] != list(range(2011, 2025)):
        raise ValueError("Unexpected BDCAP year coverage")
    return output


def estudes(sources):
    source = source_fields("estudes", sources)
    reader = PdfReader(ROOT / sources["estudes"]["path"])
    text = "\n".join((reader.pages[i].extract_text() or "") for i in range(2, 12))
    expected = ["2.488", "14 a 18 años", "ponderación", "51,3%", "16,5%", "15,9%", "23,5%"]
    for token in expected:
        if token not in text:
            raise ValueError("ESTUDES transcription drift: " + token)
    values = [
        ("alcohol_lifetime", "Alcohol, alguna vez", 73.2, "lifetime", 8),
        ("alcohol_last_12_months", "Alcohol, últimos 12 meses", 70.4, "last_12_months", 8),
        ("alcohol_last_30_days", "Alcohol, últimos 30 días", 51.3, "last_30_days", 8),
        ("tobacco_lifetime", "Tabaco, alguna vez", 28.8, "lifetime", 8),
        ("tobacco_last_30_days", "Tabaco, últimos 30 días", 16.5, "last_30_days", 8),
        ("cannabis_lifetime", "Cannabis, alguna vez", 26.1, "lifetime", 8),
        ("cannabis_last_12_months", "Cannabis, últimos 12 meses", 21.1, "last_12_months", 8),
        ("cannabis_last_30_days", "Cannabis, últimos 30 días", 15.9, "last_30_days", 8),
        ("binge_drinking_last_30_days", "Consumo en atracón, últimos 30 días", 23.5, "last_30_days", 11),
    ]
    output = []
    for indicator, label, value, period, page in values:
        row = source.copy()
        row.update({
            "survey_id": "estudes_2023",
            "indicator_id": indicator,
            "indicator_label": label,
            "reference_period": "2023",
            "geography_level": "autonomous_community",
            "geography_id": "canarias",
            "age_group_original": "14-18 años",
            "sex": "total",
            "time_context": period,
            "category": "yes",
            "value": value,
            "unit": "percent",
            "universe": "Estudiantes de 14-18 años en enseñanzas secundarias incluidas",
            "sample_size": 2488,
            "weighting": "Ponderada por CCAA, titularidad y estudios; error Canarias ±2,0%",
            "value_status": "SURVEY_ESTIMATE",
            "comparability_status": "ADMIT_WITH_LIMITATIONS",
            "method_id": "estudes2023_canarias_report_v1",
            "source_page": page,
        })
        output.append(row)
    return output


def esde(sources):
    source = source_fields("esde_screen_time", sources)
    output = []
    rows = read_semicolon(ROOT / sources["esde_screen_time"]["path"])
    sex_codes = {"AMBOS SEXOS": "total", "Hombres": "male", "Mujeres": "female"}
    period_codes = {"De lunes a viernes": "weekday", "En fin de semana": "weekend"}
    category_codes = {
        "Nada o casi nada": "none_or_almost_none",
        "Menos de una hora": "under_one_hour",
        "Una hora o más": "one_hour_or_more",
    }
    for row in rows:
        if row["COMUNIDAD AUTÓNOMA"] != "Canarias" or row["TIEMPO DIARIO"] == "Total":
            continue
        output.append(source | {
            "survey_id": "esde_2023",
            "indicator_id": "leisure_screen_time",
            "indicator_label": "Tiempo libre diario frente a una pantalla",
            "reference_period": "2023",
            "geography_level": "autonomous_community",
            "geography_id": "canarias",
            "age_group_original": "1-14 años",
            "sex": sex_codes[row["SEXO"]],
            "time_context": period_codes[row["TIEMPO SEMANA"]],
            "category": category_codes[row["TIEMPO DIARIO"]],
            "value": float(row["Total"].replace(",", ".")),
            "unit": "percent",
            "universe": "Población de 1 a 14 años residente en viviendas familiares",
            "sample_size": "",
            "weighting": "Estimación ESdE; N y error de celda no publicados en tabla 72840",
            "value_status": "SURVEY_ESTIMATE",
            "comparability_status": "ADMIT_WITH_LIMITATIONS",
            "method_id": "esde2023_table72840_v1",
        })
    if len(output) != 18:
        raise ValueError("Unexpected ESdE Canarias rows")
    return output


def metabolic_screening(sources):
    source = source_fields("metabolic_screening", sources)
    reader = PdfReader(ROOT / sources["metabolic_screening"]["path"])
    table2 = reader.pages[20].extract_text() or ""
    table3 = reader.pages[28].extract_text() or ""
    expected2 = r"CANARIAS\s+11671\s+11536\s+11536\s+98,8\s+48\s+48\s+72\s+1,3\s+99,8"
    if not re.search(expected2, table2):
        raise ValueError("SICN table 2 transcription drift")
    if not re.search(r"CANARIAS\s+2\s+4\s+6", table3):
        raise ValueError("SICN table 3 transcription drift")
    values = [
        ("newborns_in_ccaa", "Recién nacidos registrados en la CCAA", 11671, "newborns", "", ""),
        ("newborns_sampled", "Recién nacidos con toma de muestra", 11536, "newborns", 11536, 11671),
        ("newborns_analyzed", "Recién nacidos analizados", 11536, "newborns", 11536, 11671),
        ("participation", "Participación en el cribado", 98.8, "percent", 11536, 11671),
        ("sample_collection_p50", "Tiempo nacimiento-toma de muestra P50", 48, "hours", "", ""),
        ("sample_collection_p95", "Tiempo nacimiento-toma de muestra P95", 48, "hours", "", ""),
        ("sample_collection_p99", "Tiempo nacimiento-toma de muestra P99", 72, "hours", "", ""),
        ("first_invalid_sample", "Primeras muestras no válidas", 1.3, "percent", "", 11536),
        ("traceability", "Trazabilidad del proceso", 99.8, "percent", "", 11536),
        ("sample_transport_p50", "Tiempo toma-recepción en laboratorio P50", 2, "days", "", ""),
        ("sample_transport_p95", "Tiempo toma-recepción en laboratorio P95", 4, "days", "", ""),
        ("sample_transport_p99", "Tiempo toma-recepción en laboratorio P99", 6, "days", "", ""),
    ]
    output = []
    for indicator, label, value, unit, numerator, denominator in values:
        output.append(source | {
            "indicator_id": indicator,
            "indicator_label": label,
            "reference_period": "2024",
            "geography_level": "autonomous_community",
            "geography_id": "canarias",
            "age_group_original": "Recién nacidos incluidos en el programa durante 2024",
            "universe": "Programa de cribado neonatal en prueba de talón",
            "value": value,
            "unit": unit,
            "numerator": numerator,
            "denominator": denominator,
            "value_status": "OBSERVED",
            "comparability_status": "ADMIT_WITH_LIMITATIONS",
            "method_id": "sicn_process_indicator_v1",
            "source_page": 21 if not indicator.startswith("sample_transport") else 29,
        })
    return output


def write(name, rows):
    path = ROOT / "data/curated" / name
    fieldnames = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path


def main():
    sources = json.loads((ROOT / "data/manifests/phase6b_sources.json").read_text())
    for source in sources.values():
        if sha(ROOT / source["path"]) != source["checksum"]:
            raise ValueError("Frozen Phase 6B source checksum mismatch")
    datasets = {
        "bdcap_pediatric_indicators.csv": bdcap(sources),
        "neonatal_screening_indicators.csv": metabolic_screening(sources),
        "adolescent_survey_indicators_phase6b.csv": esde(sources) + estudes(sources),
    }
    paths = [write(name, rows) for name, rows in datasets.items()]
    admission = {
        "bdcap_morbidity": "ADMIT_WITH_LIMITATIONS",
        "sivamin": "HOLD",
        "metabolic_screening": "ADMIT_WITH_LIMITATIONS",
        "hearing_screening": "HOLD",
        "esde": "ADMIT_WITH_LIMITATIONS",
        "estudes": "ADMIT_WITH_LIMITATIONS",
        "waiting_island": "HOLD",
        "hospital_enrichment": "HOLD",
    }
    outputs = {}
    for path in paths:
        outputs[str(path.relative_to(ROOT))] = {
            "sha256": sha(path),
            "rows": len(datasets[path.name]),
        }
    manifest = {
        "parser_version": PARSER,
        "sources": sources,
        "admission": admission,
        "outputs": outputs,
    }
    manifest_path = ROOT / "data/manifests/phase6b_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({name: len(rows) for name, rows in datasets.items()}))


if __name__ == "__main__":
    main()
