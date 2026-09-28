"use client";
import {useState} from "react";
import {SemanticChart} from "./SemanticChart";
import {metrics,timePoints,islandLabels,sevenIslands,type ChartType} from "@/lib/semantic";
import {DataBadge} from "./DataBadge";
import {ResultSourcesLink} from "./ResultSourcesLink";

const temporalMetrics=metrics.filter(metric=>timePoints.some(point=>point.metric_id===metric.metric_id));
const defaults={series:"pediatricians_ap",compare:"pediatric_consultations",explore:"preterm_rate"} as const;
const visuals:ChartType[]=["line","bar","small_multiples","heatmap","table"];
const visualLabels:Record<string,string>={line:"Línea",bar:"Barras",small_multiples:"Small multiples",heatmap:"Heatmap",table:"Tabla"};
const nf=new Intl.NumberFormat("es-ES",{maximumFractionDigits:2});

export function TemporalWorkbench({mode="series"}:{mode?:"series"|"compare"|"explore"}){
 const [metricId,setMetricId]=useState<string>(defaults[mode]);
 const definition=metrics.find(metric=>metric.metric_id===metricId)!;
 const regional=definition.geography_levels.includes("autonomous_community")&&!definition.geography_levels.includes("island");
 const [selected,setSelected]=useState<string[]>(mode==="series"?["lanzarote"]:["tenerife","gran-canaria"]);
 const [visual,setVisual]=useState<ChartType>(mode==="compare"?"small_multiples":"line");
 const [start,setStart]=useState(definition.time_start);
 const [end,setEnd]=useState(definition.time_end);
 const changeMetric=(id:string)=>{const next=metrics.find(metric=>metric.metric_id===id)!;setMetricId(id);setStart(next.time_start);setEnd(next.time_end);if(next.geography_levels.includes("autonomous_community")&&!next.geography_levels.includes("island"))setSelected(["canarias"])};
 const toggle=(island:string)=>setSelected(current=>current.includes(island)?current.filter(item=>item!==island):(current.length<7?[...current,island]:current));
 const points=timePoints.filter(point=>point.metric_id===metricId&&(regional?point.geography_id==="canarias":selected.includes(point.geography_id))&&Number(point.period.slice(0,4))>=start&&Number(point.period.slice(0,4))<=end);
 const validVisuals=visuals.filter(item=>definition.chart_types.includes(item)||item==="table");
 const periods=[...new Set(points.map(point=>point.period))].sort();const first=periods[0],last=periods.at(-1);
 const changes=selected.map(island=>{const a=points.find(point=>point.geography_id===island&&point.period===first),b=points.find(point=>point.geography_id===island&&point.period===last);return {island,a,b,absolute:a&&b?b.value-a.value:null,relative:a&&b&&a.value!==0?(b.value-a.value)/a.value*100:null}}).filter(item=>item.a&&item.b);
 return <div className="temporal-workbench">
  <div className="semantic-controls">
   <label>Indicador<select value={metricId} onChange={event=>changeMetric(event.target.value)}>{temporalMetrics.map(metric=><option key={metric.metric_id} value={metric.metric_id}>{metric.label}</option>)}</select></label>
   <label>Desde<input type="number" min={definition.time_start} max={end} value={start} onChange={event=>setStart(Number(event.target.value))}/></label>
   <label>Hasta<input type="number" min={start} max={definition.time_end} value={end} onChange={event=>setEnd(Number(event.target.value))}/></label>
   <label>Visualización<select value={visual} onChange={event=>setVisual(event.target.value as ChartType)}>{validVisuals.map(item=><option key={item} value={item}>{visualLabels[item]}</option>)}</select></label>
  </div>
  {!regional&&<fieldset className="island-selector"><legend>Islas · selecciona entre 1 y 7</legend>{sevenIslands.map(island=><label key={island}><input type="checkbox" checked={selected.includes(island)} onChange={()=>toggle(island)}/>{islandLabels[island]}</label>)}</fieldset>}
  {regional&&<div className="scope-note"><DataBadge status="PARTIAL"/><p>Serie regional de Canarias. No se representa por isla porque la fuente no publica esa geografía.</p></div>}
  <div className="semantic-result">
   <div className="semantic-result-head"><div><span className="eyebrow">{mode==="compare"?"Comparar territorios":mode==="explore"?"Explorar datos":"Evolución temporal"}</span><h2>{definition.label}</h2><p>{definition.description}</p></div><DataBadge status={definition.status==="DERIVED_RATE"?"DERIVED_RATE":"OBSERVED"}/></div>
   {points.length?<SemanticChart points={points} metrics={[definition]} type={visual}/>:<div className="viz-empty" role="status">No hay datos para esta selección. Ajusta territorios o periodo.</div>}
  <ResultSourcesLink metricId={metricId} period={start+"–"+end} geography={regional?"canarias":selected.join(",")} result={definition.label}/></div>
  {mode==="compare"&&changes.length>0&&<><div className="table-scroll comparison-deltas"><table><thead><tr><th>Isla</th><th>{first}</th><th>{last}</th><th>Diferencia absoluta</th><th>Diferencia relativa</th></tr></thead><tbody>{changes.map(item=><tr key={item.island}><td>{islandLabels[item.island]}</td><td>{nf.format(item.a!.value)}</td><td>{nf.format(item.b!.value)}</td><td>{nf.format(item.absolute!)}</td><td>{item.relative==null?"No calculable":nf.format(item.relative)+" %"}</td></tr>)}</tbody></table></div><ResultSourcesLink metricId={metricId} period={start+"–"+end} geography={selected.join(",")} result={"Tabla comparativa · "+definition.label}/></>}
  <details className="source-panel"><summary>Fuente y método</summary><div className="source-grid"><div><strong>Fuente</strong><p>{definition.source_id}</p></div><div><strong>Periodo</strong><p>{definition.time_start}–{definition.time_end}</p></div><div><strong>Geografía</strong><p>{definition.geography_levels.join(", ")}</p></div><div><strong>Método</strong><p>{definition.method_id} · {definition.unit}</p></div></div></details>
 </div>;
}
