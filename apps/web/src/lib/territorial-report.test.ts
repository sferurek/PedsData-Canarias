import {describe,expect,it} from "vitest";
import {askPedsData} from "./semantic";
import {buildTerritorialReport,resolveTerritory} from "./territorial-report";

describe("territorial report planner",()=>{
 it.each(["gran-canaria","lanzarote","el-hierro"])("builds an island report for %s",id=>{const report=buildTerritorialReport(id)!;expect(report.territory.kind).toBe("island");expect(report.sections.length).toBeGreaterThan(4);expect(report.findings.length).toBeGreaterThanOrEqual(5);expect(report.sourceIds.length).toBeGreaterThan(0)});
 it("builds Telde only with municipality-compatible direct metrics",()=>{const report=buildTerritorialReport("35026")!;expect(report.territory.name).toBe("Telde");expect(report.sections.some(section=>section.id==="socioeconomic")).toBe(true);expect(report.sections.some(section=>section.id==="perinatal")).toBe(false);expect(report.regionalContext.every(section=>section.note?.includes("No se atribuye"))).toBe(true)});
 it("keeps La Graciosa as a limited component without fabricated times",()=>{const report=buildTerritorialReport("la-graciosa")!;expect(report.territory.publicationStatus).toBe("limited");expect(report.sections.flatMap(section=>section.facts).some(fact=>fact.value==="Transferencia interinsular requerida")).toBe(true);expect(report.sections.flatMap(section=>section.facts).some(fact=>typeof fact.value==="number"&&fact.metric_id==="accessibility_ap")).toBe(false)});
 it("returns null for a missing territory",()=>expect(resolveTerritory("atlantis")).toBeNull());
 it("keeps every rendered fact linked to registered sources",()=>{const report=buildTerritorialReport("gran-canaria")!;for(const fact of report.sections.flatMap(section=>section.facts)){expect(fact.source_ids.length).toBeGreaterThan(0);expect(fact.method_id).toBeTruthy();expect(fact.period).toBeTruthy();expect(fact.geography_id).toBe("gran-canaria")}});
 it("parses territorial report prompts without requiring a metric",()=>{const result=askPedsData("Hazme un informe exhaustivo de Gran Canaria");expect(result.ok).toBe(true);if(result.ok){expect(result.plan.intent).toBe("TERRITORIAL_REPORT");expect(result.report_href).toBe("/informes/gran-canaria");expect(result.source_ids.length).toBeGreaterThan(0)}});
 it("resolves a municipality by name",()=>{const result=askPedsData("Genera un perfil pediátrico de Telde");expect(result.ok).toBe(true);if(result.ok)expect(result.report_href).toBe("/informes/35026")});
 it("prioritizes a municipality when its name contains an island name",()=>{const result=askPedsData("Perfil pediátrico de Santa Cruz de Tenerife");expect(result.ok).toBe(true);if(result.ok)expect(result.report_name).toBe("Santa Cruz de Tenerife")});
 it("rejects a territorial report for an unknown place",()=>expect(askPedsData("Analiza Atlantis")).toMatchObject({ok:false,error:"GEOGRAPHY_NOT_SUPPORTED"}));
});
