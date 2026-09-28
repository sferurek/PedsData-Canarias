import {describe,expect,it} from "vitest";
import {askPedsData,parseQuestion} from "./semantic";

describe("Ask PedsData semantic engine",()=>{
 it("builds a Lanzarote pediatrician series",()=>{
  const result=askPedsData("Muéstrame la evolución de pediatras en Lanzarote");
  expect(result.ok).toBe(true);
  if(result.ok){
   expect(result.plan.metrics).toEqual(["pediatricians_ap"]);
   expect(new Set(result.points.map(point=>point.geography_id))).toEqual(new Set(["lanzarote"]));
   expect(result.points).toHaveLength(21);
   expect(result.source_ids).toContain("ISTAC:E54086A_000001");
  }
 });
 it("compares Tenerife and Gran Canaria consultations",()=>{
  const result=askPedsData("Compara consultas de Pediatría entre Tenerife y Gran Canaria");
  expect(result.ok).toBe(true);
  if(result.ok){
   expect(result.plan.intent).toBe("COMPARE_GEOGRAPHIES");
   expect(new Set(result.points.map(point=>point.geography_id))).toEqual(new Set(["tenerife","gran-canaria"]));
  }
 });
 it("maps income at municipal resolution",()=>{
  const result=askPedsData("Haz un mapa de renta en Canarias");
  expect(result.ok).toBe(true);
  if(result.ok)expect(result.metrics[0].map_geography).toBe("municipality");
 });
 it("maps accessibility without changing grid resolution",()=>{
  const result=askPedsData("Mapa de accesibilidad pediátrica de Fuerteventura");
  expect(result.ok).toBe(true);
  if(result.ok)expect(result.metrics[0].map_geography).toBe("grid_250m");
 });
 it("rejects a regional metric map",()=>{
  const result=askPedsData("Haz un mapa de hospitalización pediátrica");
  expect(result).toMatchObject({ok:false,error:"NOT_MAPPABLE"});
 });
 it("rejects an unavailable period",()=>{
  const result=askPedsData("Evolución de pediatras en Lanzarote desde 1990");
  expect(result).toMatchObject({ok:false,error:"TIME_RANGE_NOT_AVAILABLE"});
 });
 it("rejects an unregistered metric",()=>{
  const result=askPedsData("Muéstrame alergias por municipio");
  expect(result).toMatchObject({ok:false,error:"METRIC_NOT_FOUND"});
 });
 it("rejects incompatible metrics",()=>{
  const result=askPedsData("Compara renta y hospitalización");
  expect(result).toMatchObject({ok:false,error:"INCOMPATIBLE_METRICS"});
 });
 it("keeps La Graciosa explicit without fabricating a series",()=>{
  const result=askPedsData("Evolución de pediatras en La Graciosa");
  expect(result).toMatchObject({ok:false,error:"INSUFFICIENT_DATA"});
 });
 it("returns a structured plan only",()=>{
  const result=parseQuestion("Compara población infantil y pediatras en Lanzarote desde 2010");
  expect(result).toMatchObject({intent:"COMPARE_METRICS",start_year:2010,geographies:["lanzarote"]});
 });
});
