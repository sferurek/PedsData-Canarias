import catalogRaw from "@/data/metrics-catalog.json";
import compatibilityRaw from "@/data/metric-compatibility.json";
import seriesRaw from "@/data/metric-time-series.json";
import profilesRaw from "@/data/profiles.json";

export type ChartType="line"|"bar"|"small_multiples"|"heatmap"|"slope"|"scatter"|"map"|"table";
export type Intent="TIME_SERIES"|"COMPARE_GEOGRAPHIES"|"MAP_METRIC"|"COMPARE_METRICS"|"LATEST_VALUE"|"TREND_SUMMARY"|"TERRITORIAL_REPORT";
export type QueryError="METRIC_NOT_FOUND"|"GEOGRAPHY_NOT_SUPPORTED"|"TIME_RANGE_NOT_AVAILABLE"|"INCOMPATIBLE_METRICS"|"NOT_MAPPABLE"|"INSUFFICIENT_DATA";
export type MetricDefinition={metric_id:string;label:string;description:string;geography_levels:string[];time_start:number;time_end:number;unit:string;chart_types:string[];map_allowed:boolean;map_geography:string|null;classification_method:string|null;color_scale:string|null;compatible_metrics:string[];source_id:string;source_ids:string[];method_id:string;status:string;formula:{expression:string;inputs:{metric:string;source_id:string}[];transformations:string[];rounding:string}|null;transformations:string[];rounding:string;limitations:string[];visualizations:string[];lineage_version:string};
export type TimePoint={metric_id:string;geography_level:string;geography_id:string;period:string;value:number;unit:string;status:string;source_id:string;method_id:string;dimension?:string};
export type QueryPlan={intent:Intent;metrics:string[];geographies:string[];start_year?:number;end_year?:number;visual:ChartType};
export type QueryResult={ok:true;plan:QueryPlan;points:TimePoint[];summary:string;metrics:MetricDefinition[];source_ids:string[];report_href?:string;report_name?:string}|{ok:false;error:QueryError;message:string;plan?:Partial<QueryPlan>};

export const metrics=(catalogRaw as {metrics:MetricDefinition[]}).metrics;
export const timePoints=(seriesRaw as {points:TimePoint[]}).points;
const validPairs=(compatibilityRaw as {valid_pairs:string[][]}).valid_pairs.map(pair=>pair.slice().sort().join("|"));
export const islandLabels:Record<string,string>={"el-hierro":"El Hierro","la-gomera":"La Gomera","la-palma":"La Palma",tenerife:"Tenerife","gran-canaria":"Gran Canaria",fuerteventura:"Fuerteventura",lanzarote:"Lanzarote",canarias:"Canarias","la-graciosa":"La Graciosa"};
export const sevenIslands=Object.keys(islandLabels).filter(id=>id!=="canarias"&&id!=="la-graciosa");

const metricAliases:Record<string,string[]>={
 pediatricians_ap:["pediatras","pediatra","profesionales de pediatria"],
 pediatric_consultations:["consultas","consultas de pediatria","actividad pediatrica"],
 pediatric_distinct_users:["personas distintas","usuarios distintos","personas atendidas"],
 pediatric_frequentation:["frecuentacion","frecuentación"],
 child_population_assigned_0_14:["poblacion infantil","población infantil","poblacion asignada","niños"],
 assigned_children_per_pediatrician:["niños por pediatra","ninos por pediatra","poblacion por pediatra"],
 consultations_per_pediatrician:["consultas por pediatra"],
 births:["nacimientos"],preterm_rate:["prematuridad","tasa de prematuridad"],
 pediatric_outpatient_waiting_stock:["lista de espera","stock de espera","pendientes"],
 pediatric_hospital_discharges_selected:["hospitalizacion","hospitalización","altas pediatricas","altas pediátricas"],
 income_mean_per_person:["renta","renta media"],child_density:["densidad infantil"],degurba:["urbanizacion","urbanización","degurba"],
 PM10:["pm10"],"PM2.5":["pm2.5","pm2,5"],NO2:["no2","no₂"],accessibility_ap:["accesibilidad","tiempo a pediatria","tiempo a pediatría"],
};
const baseGeoAliases:Record<string,string[]>={"el-hierro":["el hierro"],"la-gomera":["la gomera"],"la-palma":["la palma"],tenerife:["tenerife"],"gran-canaria":["gran canaria"],fuerteventura:["fuerteventura"],lanzarote:["lanzarote"],canarias:["canarias"],"la-graciosa":["la graciosa"]};
const profileData=profilesRaw as {municipalities:{municipality_id:string;municipality_name:string}[]};
const municipalityIds=new Set(profileData.municipalities.map(item=>item.municipality_id));
const geoAliases:Record<string,string[]>={...baseGeoAliases,...Object.fromEntries(profileData.municipalities.map(item=>[item.municipality_id,[item.municipality_name,item.municipality_id]]))};
function normalized(value:string){return value.toLocaleLowerCase("es").normalize("NFD").replace(/[\u0300-\u036f]/g,"")}
function mentions(haystack:string,needle:string){return haystack.includes(normalized(needle))}
export function metricById(id:string){return metrics.find(metric=>metric.metric_id===id)}
export function parseQuestion(question:string):QueryPlan|QueryResult{
 const text=normalized(question);
 const foundMetrics=Object.entries(metricAliases).filter(([,aliases])=>aliases.some(alias=>mentions(text,alias))).sort((a,b)=>Math.max(...b[1].map(x=>x.length))-Math.max(...a[1].map(x=>x.length))).map(([id])=>id);
 const uniqueMetrics=[...new Set(foundMetrics)];
 const geographies=Object.entries(geoAliases).filter(([,aliases])=>aliases.some(alias=>mentions(text,alias))).map(([id])=>id);
 const asksReport=["informe","analiza","perfil pediatrico","perfil territorial"].some(term=>mentions(text,term))||(text.includes("compara")&&uniqueMetrics.length===0);
 if(asksReport){
  const specific=geographies.find(id=>municipalityIds.has(id))??geographies.find(id=>id!=="canarias")??geographies[0];
  if(!specific)return {ok:false,error:"GEOGRAPHY_NOT_SUPPORTED",message:"No encuentro un territorio registrado para generar el informe."};
  return {intent:"TERRITORIAL_REPORT",metrics:[],geographies:[specific],visual:"table"};
 }
 if(!uniqueMetrics.length)return {ok:false,error:"METRIC_NOT_FOUND",message:"No encuentro un indicador registrado en esa pregunta."};
 const years=[...text.matchAll(/\b(19\d{2}|20\d{2})\b/g)].map(match=>Number(match[1]));
 let intent:Intent="TIME_SERIES";
 if(text.includes("mapa"))intent="MAP_METRIC";
 else if(uniqueMetrics.length>1)intent="COMPARE_METRICS";
 else if(text.includes("compara")||text.includes("comparar"))intent="COMPARE_GEOGRAPHIES";
 else if(text.includes("ultimo")||text.includes("actual")||text.includes("valor mas reciente"))intent="LATEST_VALUE";
 else if(text.includes("como ha cambiado")||text.includes("tendencia")||text.includes("evolucion"))intent="TREND_SUMMARY";
 const visual:ChartType=intent==="MAP_METRIC"?"map":intent==="COMPARE_GEOGRAPHIES"?"small_multiples":intent==="COMPARE_METRICS"?"line":intent==="LATEST_VALUE"?"bar":"line";
 return {intent,metrics:uniqueMetrics.slice(0,2),geographies:geographies.length?geographies:["canarias"],start_year:years[0],end_year:years[1],visual};
}
function compatible(a:string,b:string){return validPairs.includes([a,b].sort().join("|"))}
function latestPeriod(points:TimePoint[]){return points.map(p=>p.period).sort().at(-1)}
function labelGeo(id:string){return islandLabels[id]??id}
function formatValue(value:number,unit:string){return new Intl.NumberFormat("es-ES",{maximumFractionDigits:2}).format(value)+(unit==="%"?" %":" "+unit)}
export function executePlan(plan:QueryPlan):QueryResult{
 if(plan.intent==="TERRITORIAL_REPORT"){
  const geographyId=plan.geographies[0];
  const municipality=profileData.municipalities.find(item=>item.municipality_id===geographyId);
  const level=municipality?"municipality":geographyId==="la-graciosa"?"grid_250m":geographyId==="canarias"?"autonomous_community":"island";
  const directIds=level==="municipality"?["child_population_grid_0_14","verified_pediatric_facilities","accessibility_ap","income_mean_per_person","child_density","degurba"]:level==="grid_250m"?["accessibility_ap"]:level==="island"?["child_population_grid_0_14","verified_pediatric_facilities","accessibility_ap",...metrics.filter(metric=>metric.geography_levels.includes("island")).map(metric=>metric.metric_id)]:[];
  const reportMetrics=[...new Set([...directIds,"pediatric_outpatient_waiting_stock","pediatric_hospital_discharges_selected"])].map(metricById).filter(Boolean) as MetricDefinition[];
  if(!reportMetrics.length)return {ok:false,error:"INSUFFICIENT_DATA",message:"El catálogo no contiene métricas válidas para este territorio.",plan};
  const source_ids=[...new Set(reportMetrics.flatMap(metric=>metric.source_ids))];
  const reportName=municipality?.municipality_name??islandLabels[geographyId]??geographyId;
  return {ok:true,plan,points:[],metrics:reportMetrics,source_ids,summary:"Informe territorial de "+reportName+" preparado con "+reportMetrics.length+" métricas registradas. El contexto regional se presenta por separado.",report_href:"/informes/"+encodeURIComponent(geographyId),report_name:reportName};
 }
 const defs=plan.metrics.map(metricById);
 if(defs.some(item=>!item))return {ok:false,error:"METRIC_NOT_FOUND",message:"El indicador solicitado no está registrado.",plan};
 const registered=defs as MetricDefinition[];
 const source_ids=[...new Set(registered.flatMap(metric=>metric.source_ids))];
 if(plan.metrics.length>1&&!compatible(plan.metrics[0],plan.metrics[1]))return {ok:false,error:"INCOMPATIBLE_METRICS",message:"Estos indicadores no comparten una comparación registrada y segura.",plan};
 if(plan.geographies.includes("la-graciosa"))return {ok:false,error:"INSUFFICIENT_DATA",message:"La Graciosa se conserva como componente territorial, pero no dispone de una serie insular separada.",plan};
 if(plan.intent==="MAP_METRIC"){
  const target=registered[0];
  if(!target.map_allowed)return {ok:false,error:"NOT_MAPPABLE",message:target.label+" solo está disponible a nivel "+target.geography_levels.join(", ")+" y no puede representarse en una geografía más fina.",plan};
  const year=plan.end_year??target.time_end;
  if(year<target.time_start||year>target.time_end)return {ok:false,error:"TIME_RANGE_NOT_AVAILABLE",message:target.label+" está disponible entre "+target.time_start+" y "+target.time_end+".",plan};
  return {ok:true,plan:{...plan,start_year:year,end_year:year},points:[],metrics:registered,source_ids,summary:"Mapa de "+target.label.toLocaleLowerCase("es")+" · "+year+". La capa conserva la geografía "+target.map_geography+"."};
 }
 for(const def of registered){
  if((plan.start_year&&(plan.start_year<def.time_start||plan.start_year>def.time_end))||(plan.end_year&&(plan.end_year<def.time_start||plan.end_year>def.time_end)))return {ok:false,error:"TIME_RANGE_NOT_AVAILABLE",message:def.label+" está disponible entre "+def.time_start+" y "+def.time_end+".",plan};
 }
 const requestedGeos=plan.geographies.includes("canarias")&&registered.every(m=>m.geography_levels.includes("island"))?sevenIslands:plan.geographies;
 const points=timePoints.filter(p=>plan.metrics.includes(p.metric_id)&&requestedGeos.includes(p.geography_id)&&(!plan.start_year||Number(p.period.slice(0,4))>=plan.start_year)&&(!plan.end_year||Number(p.period.slice(0,4))<=plan.end_year));
 if(!points.length)return {ok:false,error:"GEOGRAPHY_NOT_SUPPORTED",message:"No hay observaciones para esa combinación de indicador, geografía y periodo.",plan};
 if(plan.intent==="LATEST_VALUE"){
  const latest=latestPeriod(points);const selected=points.filter(p=>p.period===latest);
  return {ok:true,plan,points:selected,metrics:registered,source_ids,summary:"Último periodo disponible: "+latest+". "+selected.map(p=>labelGeo(p.geography_id)+": "+formatValue(p.value,p.unit)).join("; ")+"."};
 }
 const periods=points.map(p=>p.period).sort();const first=periods[0],last=periods.at(-1)!;
 const firstPoints=points.filter(p=>p.period===first),lastPoints=points.filter(p=>p.period===last);
 let summary="Serie observada entre "+first+" y "+last+"; "+new Set(points.map(p=>p.geography_id)).size+" territorios y "+points.length+" observaciones.";
 if(plan.intent==="TREND_SUMMARY"&&firstPoints.length===1&&lastPoints.length===1){
  const change=lastPoints[0].value-firstPoints[0].value;
  summary=labelGeo(lastPoints[0].geography_id)+" cambió "+formatValue(change,lastPoints[0].unit)+" entre "+first+" y "+last+". Es una diferencia descriptiva.";
 }
 return {ok:true,plan,points,metrics:registered,source_ids,summary};
}
export function askPedsData(question:string):QueryResult{
 const parsed=parseQuestion(question);
 return "ok" in parsed&&parsed.ok===false?parsed:executePlan(parsed as QueryPlan);
}

