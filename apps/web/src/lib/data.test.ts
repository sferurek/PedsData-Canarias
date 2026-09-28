import { describe, expect, it } from "vitest";
import { profiles } from "./data";

const EXPECTED_ISLANDS = ["el-hierro", "fuerteventura", "gran-canaria", "la-gomera", "la-palma", "lanzarote", "tenerife"];

describe("published profile data", () => {
  it("contains exactly the seven required islands", () => {
    expect(profiles.islands.map((item) => item.island_id).sort()).toEqual(EXPECTED_ISLANDS);
  });

  it("preserves La Graciosa as an inter-island transfer with unknown terrestrial time", () => {
    const lanzarote = profiles.islands.find((item) => item.island_id === "lanzarote");
    expect(lanzarote?.population_requires_interisland_transfer).toBe(91);
    expect(lanzarote?.pct_requires_interisland_transfer_total).toBeGreaterThan(0);
  });

  it("publishes only municipalities that satisfy the privacy rule", () => {
    expect(profiles.municipalities).toHaveLength(88);
    expect(profiles.municipalities.filter((item) => item.publication_status === "publishable")).toHaveLength(85);
    expect(profiles.municipalities.filter((item) => item.publication_status === "not_publishable").map((item) => item.municipality_name).sort()).toEqual(["Agulo", "Artenara", "Betancuria"]);
  });

  it("does not expose a health-zone dimension", () => {
    expect(JSON.stringify(profiles)).not.toMatch(/health_zone|zbs/i);
  });

  it("registers routing provenance", () => {
    expect(profiles.metadata.engine).toBe("OSRM");
    expect(profiles.metadata.engine_version).toBe("5.27.1");
    expect(profiles.metadata.osm_snapshot).toBeTruthy();
  });
  it("adds social and environmental context without scores", () => {
    expect(profiles.metadata.status).toBe("RC2");
    expect(profiles.municipalities.every((item) => item.income_mean_per_person_2023 != null)).toBe(true);
    expect(profiles.islands.every((item) => item.air_station_count > 0)).toBe(true);
    expect(JSON.stringify(profiles)).not.toMatch(/composite_score|risk_score/i);
  });

});
