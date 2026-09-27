#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

from shapely.geometry import shape

ROOT = Path(__file__).resolve().parents[1]
ISLAND_CODES = {
    "ES703": "el-hierro", "ES706": "la-gomera", "ES707": "la-palma",
    "ES709": "tenerife", "ES705": "gran-canaria", "ES704": "fuerteventura",
    "ES708": "lanzarote",
}
ISLAND_ORDER = list(ISLAND_CODES.values())


def haversine(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, (*a, *b))
    dlon, dlat = lon2 - lon1, lat2 - lat1
    value = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371000 * 2 * math.asin(math.sqrt(value))


def nearest(point, facilities):
    return min(facilities, key=lambda item: haversine(point, item["point"]))


def component(island_id, point):
    lon, lat = point
    if island_id == "lanzarote" and lat > 29.20 and lon > -13.65:
        return "la-graciosa"
    return island_id


def load_facilities():
    grouped = {island: [] for island in ISLAND_ORDER}
    path = ROOT / "data/curated/pediatric_facilities.csv"
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["routing_eligible_pediatric_ap"] != "true":
                continue
            point = (float(row["longitude"]), float(row["latitude"]))
            grouped[row["island_id"]].append({
                "id": row["facility_id"], "name": row["name"], "point": point,
                "component": component(row["island_id"], point),
            })
    return grouped


def load_cells():
    grouped = {island: [] for island in ISLAND_ORDER}
    path = ROOT / "data/raw/child_population_grid_2024.geojson"
    with path.open(encoding="utf-8") as handle:
        features = json.load(handle)["features"]
    for feature in features:
        props = feature["properties"]
        island = ISLAND_CODES[props["isla"]]
        children = props["poblacion_00a14"]
        if children is None or children <= 0:
            continue
        point_shape = shape(feature["geometry"]).representative_point()
        point = (point_shape.x, point_shape.y)
        grouped[island].append({
            "id": props["geocode"], "children": int(children), "point": point,
            "component": component(island, point),
        })
    return grouped


def routed_row(island, case_type, cell, facility, reverse=False):
    start, end = cell["point"], facility["point"]
    if reverse:
        start, end = end, start
    return {
        "case_id": f"{island}-{case_type}", "island_id": island,
        "case_type": case_type, "origin_cell_id": cell["id"],
        "child_population_0_14": cell["children"],
        "origin_component": cell["component"],
        "origin_longitude": start[0], "origin_latitude": start[1],
        "destination_facility_id": facility["id"],
        "destination_name": facility["name"],
        "destination_component": facility["component"],
        "destination_longitude": end[0], "destination_latitude": end[1],
        "expected_status": "routed", "guard_reason": "",
    }


def build_cases():
    cells, facilities = load_cells(), load_facilities()
    output = []
    for index, island in enumerate(ISLAND_ORDER):
        island_cells, island_facilities = cells[island], facilities[island]
        facility_components = {facility["component"] for facility in island_facilities}
        routable_cells = [cell for cell in island_cells if cell["component"] in facility_components]
        candidates = lambda cell: [facility for facility in island_facilities
                                   if facility["component"] == cell["component"]]
        urban = max(routable_cells, key=lambda item: item["children"])
        distances = [(haversine(cell["point"], nearest(cell["point"], candidates(cell))["point"]), cell)
                     for cell in routable_cells]
        extreme = max(distances, key=lambda item: item[0])[1]
        sparse = [cell for cell in routable_cells if cell["children"] <= 2 and cell["id"] != extreme["id"]]
        rural = max(sparse, key=lambda cell: haversine(cell["point"], nearest(cell["point"], candidates(cell))["point"]))
        for case_type, cell in (("urban", urban), ("rural", rural), ("extreme", extreme)):
            output.append(routed_row(island, case_type, cell, nearest(cell["point"], candidates(cell))))
        output.append(routed_row(island, "reverse", extreme, nearest(extreme["point"], candidates(extreme)), True))

        if island == "lanzarote":
            graciosa = [cell for cell in island_cells if cell["component"] == "la-graciosa"]
            mainland = [facility for facility in island_facilities if facility["component"] == "lanzarote"]
            no_route_cell = max(graciosa, key=lambda item: item["children"])
            no_route_facility = nearest(no_route_cell["point"], mainland)
            expected, reason = "requires_interisland_transfer", "la_graciosa_sea_crossing"
        else:
            next_island = ISLAND_ORDER[(index + 1) % len(ISLAND_ORDER)]
            no_route_cell = urban
            no_route_facility = nearest(no_route_cell["point"], facilities[next_island])
            expected, reason = "no_route", "cross_island_topology_guard"
        row = routed_row(island, "no_route", no_route_cell, no_route_facility)
        row["expected_status"], row["guard_reason"] = expected, reason
        output.append(row)
    return output


def main():
    rows = build_cases()
    destination = ROOT / "data/curated/routing_test_cases.csv"
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} cases to {destination}")


if __name__ == "__main__":
    main()
