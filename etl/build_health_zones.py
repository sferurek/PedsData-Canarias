#!/usr/bin/env python3
"""Audit and export the historical 2017 ZBS fallback without claiming currency."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from pyproj import Transformer
import shapefile
from shapely.geometry import mapping, shape
from shapely.ops import transform, unary_union

from xlsx_reader import read_dicts

ZBS_URL = "https://zenodo.org/records/1256149"
AP_URL = "https://www.sanidad.gob.es/estadEstudios/estadisticas/docs/siap/2026_C_Catal_Centros_AP.xlsx"
MUNICIPAL_URL = "https://datos.canarias.es/catalogos/estadisticas/dataset/6dd8baf4-14f4-43a3-88b2-984d034c965c/resource/d31b5422-df3b-4eae-b0eb-b4acbecb8ef0/download/municipios_desde2007_generalizada_20170101.json"
BOUNDS = {
    "el-hierro": (-18.20, -17.85, 27.60, 27.90), "la-gomera": (-17.40, -17.00, 28.00, 28.25),
    "la-palma": (-18.00, -17.65, 28.45, 28.90), "tenerife": (-16.95, -16.00, 27.95, 28.65),
    "gran-canaria": (-15.85, -15.35, 27.70, 28.20), "fuerteventura": (-14.55, -13.75, 28.00, 28.80),
    "lanzarote": (-13.90, -13.40, 28.80, 29.35),
}
AREA_TO_ISLAND = {
    "EL HIERRO": "el-hierro", "LA GOMERA": "la-gomera", "LA PALMA": "la-palma",
    "TENERIFE": "tenerife", "GRAN CANARIA": "gran-canaria",
    "FUERTEVENTURA": "fuerteventura", "LANZAROTE": "lanzarote",
}
SIAP_2024_COUNTS = {"el-hierro": 2, "la-gomera": 5, "la-palma": 9, "tenerife": 40,
                    "gran-canaria": 39, "fuerteventura": 6, "lanzarote": 7}


def island_for(geometry) -> str:
    point = geometry.representative_point()
    matches = [key for key, (w, e, s, n) in BOUNDS.items() if w <= point.x <= e and s <= point.y <= n]
    if len(matches) != 1:
        raise ValueError(f"Unable to assign island at {point.wkt}")
    return matches[0]


def current_catalog(ap_path: Path, output: Path) -> list[dict[str, str]]:
    rows = read_dicts(ap_path, "Catálogo - 2026")
    zones = sorted({
        (AREA_TO_ISLAND[row["SIAP_AREASALUD_CD.NOMBRE"]], row["SIAP_ZONABASICA.NOMBRE"])
        for row in rows if row.get("SIAP_CCAA.NOMBRE") == "CANARIAS"
    })
    fieldnames = ("health_zone_id", "official_code", "name", "island_id", "health_area_id",
                  "valid_from", "valid_to", "geometry_status", "source_url", "source_date",
                  "verification_status", "routing_eligible", "notes")
    records = []
    for island, name in zones:
        records.append({
            "health_zone_id": "", "official_code": "", "name": name,
            "island_id": island, "health_area_id": island, "valid_from": "",
            "valid_to": "", "geometry_status": "not_available", "source_url": AP_URL,
            "source_date": "2025-12-31", "verification_status": "NEEDS_VALIDATION",
            "routing_eligible": "false",
            "notes": "Nomenclatura vigente en Catálogo AP 2026; código estable y polígono no publicados.",
        })
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    return records


def historical_features(shapefile_path: Path):
    transformer = Transformer.from_crs(4258, 4326, always_xy=True)
    reader = shapefile.Reader(str(shapefile_path))
    features = []
    source_geometries = []
    for item in reader.iterShapeRecords():
        source_geometry = shape(item.shape.__geo_interface__)
        if not source_geometry.is_valid:
            raise ValueError(f"Invalid source geometry {item.record['codatzbs']}; no make_valid applied")
        island = island_for(source_geometry)
        geometry = transform(transformer.transform, source_geometry)
        properties = {
            "health_zone_id": f"atlasvpm-2017:{item.record['codatzbs']}",
            "official_code": None, "source_code": int(item.record["codatzbs"]),
            "name": item.record["n_zbs"], "island_id": island, "health_area_id": island,
            "valid_from": None, "valid_to": None, "reference_year": 2017,
            "source_url": ZBS_URL, "source_date": "2017",
            "verification_status": "NEEDS_VALIDATION", "routing_eligible": False,
            "historical_reference_only": True,
            "notes": "Geometría histórica IACS/AtlasVPM; no equivale a ZBS vigente.",
        }
        features.append({"type": "Feature", "properties": properties, "geometry": mapping(geometry)})
        source_geometries.append((island, int(item.record["codatzbs"]), source_geometry))
    return features, source_geometries


def qa_report(source_geometries, municipal_path: Path, current_rows):
    project_zbs = Transformer.from_crs(4258, 32628, always_xy=True).transform
    project_land = Transformer.from_crs(4326, 32628, always_xy=True).transform
    by_island = {island: [] for island in BOUNDS}
    for island, code, geometry in source_geometries:
        by_island[island].append((code, transform(project_zbs, geometry)))
    municipal = json.loads(municipal_path.read_text())
    land = {island: [] for island in BOUNDS}
    for feature in municipal["features"]:
        geometry = shape(feature["geometry"])
        land[island_for(geometry)].append(transform(project_land, geometry))
    current_counts = {}
    for island in BOUNDS:
        current_counts[island] = sum(row["island_id"] == island for row in current_rows)
    islands = {}
    for island, items in by_island.items():
        zone_union = unary_union([geometry for _, geometry in items])
        land_union = unary_union(land[island])
        overlap_pairs = []
        for index, (left_code, left) in enumerate(items):
            for right_code, right in items[index + 1:]:
                area = left.intersection(right).area
                if area > 1.0:
                    overlap_pairs.append({"left": left_code, "right": right_code, "area_m2": round(area, 2)})
        islands[island] = {
            "historical_2017_count": len(items), "current_ap_catalog_2026_count": current_counts[island],
            "siap_2024_count": SIAP_2024_COUNTS[island], "valid_geometry_count": sum(g.is_valid for _, g in items),
            "overlap_pairs_gt_1m2": overlap_pairs,
            "land_coverage_percent": round(100 * zone_union.intersection(land_union).area / land_union.area, 5),
            "uncovered_land_m2": round(land_union.difference(zone_union).area, 2),
            "zone_outside_land_m2": round(zone_union.difference(land_union).area, 2),
        }
    codes = [code for _, code, _ in source_geometries]
    return {
        "source_crs": "EPSG:4258", "output_crs": "EPSG:4326", "area_crs": "EPSG:32628",
        "source_feature_count": len(source_geometries), "duplicate_source_code_count": len(codes) - len(set(codes)),
        "make_valid_applied": False, "land_reference": MUNICIPAL_URL,
        "land_reference_note": "Cartografía municipal generalizada; diferencias costeras pequeñas no prueban huecos ZBS.",
        "islands": islands,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shapefile", type=Path, default=Path("data/staging/zbs_2017/canarias4258.shp"))
    parser.add_argument("--municipal", type=Path, default=Path("data/raw/municipios_desde2007_generalizada_20170101.geojson"))
    parser.add_argument("--ap-catalog", type=Path, default=Path("data/raw/2026_C_Catal_Centros_AP.xlsx"))
    parser.add_argument("--output", type=Path, default=Path("data/curated/health_zones.geojson"))
    parser.add_argument("--current-output", type=Path, default=Path("data/curated/health_zones_current_catalog.csv"))
    parser.add_argument("--qa-output", type=Path, default=Path("data/curated/health_zones_qa.json"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    current_rows = current_catalog(args.ap_catalog, args.current_output)
    features, source_geometries = historical_features(args.shapefile)
    collection = {
        "type": "FeatureCollection", "name": "health_zones_historical_2017_not_for_routing",
        "metadata": {"source_crs": "EPSG:4258", "output_crs": "EPSG:4326", "reference_year": 2017,
                     "verification_status": "NEEDS_VALIDATION", "routing_eligible": False,
                     "historical_reference_only": True},
        "features": features,
    }
    args.output.write_text(json.dumps(collection, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    report = qa_report(source_geometries, args.municipal, current_rows)
    args.qa_output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(features)} historical features and {len(current_rows)} current names")


if __name__ == "__main__":
    main()
