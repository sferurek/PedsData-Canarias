import rawProfiles from "@/data/profiles.json";
import {metricById,timePoints,type MetricDefinition,type TimePoint} from "./semantic";
import type {ProfilesData,IslandProfile,MunicipalityProfile} from "./types";

const profiles=rawProfiles as ProfilesData;

export type TerritoryKind="island"|"municipality"|"archipelago"|"territorial_component";
export type ReportTerritory={id:string;name:string;kind:TerritoryKind;geographyLevel:string;islandId?:string;publicationStatus:"publishable"|"limited"};
export type ReportFact={metric_id:string;label:string;value:number|string|null;unit:string;period:string;geography_level:string;geography_id:string;status:string;source_ids:string[];method_id:string};
export type ReportSection={id:string;title:string;metricIds:string[];facts:ReportFact[];series:TimePoint[];visual:"line"|"table"|"map";note?:string};
export type ExecutiveFinding={id:string;text:string;metricIds:string[];period:string};
export type ReportInterpretation={known:ExecutiveFinding[];cannotConclude:string[];missingData:string[]};
export type TerritorialReport={territory:ReportTerritory;sections:ReportSection[];regionalContext:ReportSection[];findings:ExecutiveFinding[];interpretation:ReportInterpretation;unavailableDomains:string[];sourceIds:string[];limitations:string[]};

const DOMAIN_METRICS:{id:string;title:string;metrics:string[]}[]=[
 {id:"demography",title:"Demografía infantil",metrics:["child_population_grid_0_14","child_population_assigned_0_14"]},
 {id:"resources",title:"Recursos pediátricos",metrics:["verified_pediatric_facilities","pediatricians_ap"]},
 {id:"access",title:"Accesibilidad",metrics:["accessibility_ap"]},
 {id:"utilization",title:"Utilización de Pediatría AP",metrics:["pediatric_consultations","pediatric_distinct_users","pediatric_frequentation"]},
 {id:"capacity",title:"Oferta y presión asistencial",metrics:["assigned_children_per_pediatrician","consultations_per_pediatrician"]},
 {id:"socioeconomic",title:"Contexto socioeconómico",metrics:["income_mean_per_person"]},
 {id:"urbanization",title:"Urbanización y ruralidad",metrics:["child_density","degurba"]},
 {id:"environment",title:"Entorno ambiental",metrics:["PM10","PM2.5","NO2"]},
 {id:"perinatal",title:"Perinatalidad",metrics:["births","preterm_rate"]},
 {id:"mortality",title:"Mortalidad",metrics:[]},
 {id:"health",title:"Resultados de salud",metrics:[]},
 {id:"adolescence",title:"Adolescencia",metrics:[]},
 {id:"prevention",title:"Prevención",metrics:[]},
 {id:"hospital",title:"Actividad hospitalaria",metrics:["pediatric_hospital_discharges_selected"]},
];
const REGIONAL_METRICS=["pediatric_outpatient_waiting_stock","pediatric_hospital_discharges_selected"];
const additiveMetrics=new Set(["child_population_assigned_0_14","pediatricians_ap","pediatric_consultations","pediatric_distinct_users","births"]);
const nf=new Intl.NumberFormat("es-ES",{maximumFractionDigits:2});

export function resolveTerritory(id:string):ReportTerritory|null{
 if(id==="canarias")return {id,name:"Canarias",kind:"archipelago",geographyLevel:"autonomous_community",publicationStatus:"publishable"};
 if(id==="la-graciosa")return {id,name:"La Graciosa",kind:"territorial_component",geographyLevel:"grid_250m",islandId:"lanzarote",publicationStatus:"limited"};
 const island=profiles.islands.find(item=>item.island_id===id||item.slug===id);
 if(island)return {id:island.island_id,name:island.name,kind:"island",geographyLevel:"island",islandId:island.island_id,publicationStatus:"publishable"};
 const municipality=profiles.municipalities.find(item=>item.municipality_id===id||item.slug===id);
 if(municipality)return {id:municipality.municipality_id,name:municipality.municipality_name,kind:"municipality",geographyLevel:"municipality",islandId:municipality.island_id,publicationStatus:municipality.publication_status==="publishable"?"publishable":"limited"};
 return null;
}
export function territorialReportIds(){return ["canarias","la-graciosa",...profiles.islands.map(item=>item.island_id),...profiles.municipalities.map(item=>item.municipality_id)]}
function def(id:string){const item=metricById(id);if(!item)throw new Error("Metric not registered: "+id);return item}
function fact(metricId:string,label:string,value:number|string|null,unit:string,period:string,territory:ReportTerritory,status?:string):ReportFact{
 const metric=def(metricId);if(!metric.source_ids.length)throw new Error("No source_id = no render: "+metricId);
 return {metric_id:metricId,label,value,unit,period,geography_level:territory.geographyLevel,geography_id:territory.id,status:status??metric.status,source_ids:metric.source_ids,method_id:metric.method_id};
}
function islandFacts(profile:IslandProfile,territory:ReportTerritory){return [
 fact("child_population_grid_0_14","Población infantil 0–14",profile.children_0_14,"niños","2024",territory),
 fact("verified_pediatric_facilities","Recursos AP verificados",profile.eligible_pediatric_facilities,"recursos","2026",territory),
 fact("accessibility_ap","Mediana de acceso potencial",profile.median_travel_minutes,"min","2024",territory),
 fact("accessibility_ap","P90 de acceso potencial",profile.p90_travel_minutes,"min","2024",territory),
 fact("accessibility_ap","Población a menos de 15 min",profile.pct_under_15_total,"% población total","2024",territory),
 fact("accessibility_ap","Población a 30 min o más",profile.pct_30_or_more_total,"% población total","2024",territory),
 ...(profile.population_requires_interisland_transfer?[fact("accessibility_ap","Población con transferencia interinsular",profile.population_requires_interisland_transfer,"niños","2024",territory,"requires_interisland_transfer")]:[]),
 ];}
function municipalityFacts(profile:MunicipalityProfile,territory:ReportTerritory){
 if(profile.publication_status!=="publishable")return [];
 return [
  fact("child_population_grid_0_14","Población infantil 0–14",profile.children_0_14??null,"niños","2024",territory),
  fact("verified_pediatric_facilities","Recursos AP verificados",profile.eligible_pediatric_facilities??null,"recursos","2026",territory),
  fact("accessibility_ap","Mediana de acceso potencial",profile.median_travel_minutes??null,"min","2024",territory),
  fact("accessibility_ap","P90 de acceso potencial",profile.p90_travel_minutes??null,"min","2024",territory),
  fact("accessibility_ap","Población a menos de 15 min",profile.pct_under_15_total??null,"% población total","2024",territory),
  fact("accessibility_ap","Población a 30 min o más",profile.pct_30_or_more_total??null,"% población total","2024",territory),
  fact("income_mean_per_person","Renta media por persona",profile.income_mean_per_person_2023??null,"€","2023",territory),
  fact("child_density","Densidad infantil",profile.child_density_per_km2??null,"niños/km²","2024",territory),
 ];
}
function currentFacts(territory:ReportTerritory){
 if(territory.kind==="island")return islandFacts(profiles.islands.find(item=>item.island_id===territory.id)!,territory);
 if(territory.kind==="municipality")return municipalityFacts(profiles.municipalities.find(item=>item.municipality_id===territory.id)!,territory);
 if(territory.kind==="archipelago")return [fact("child_population_grid_0_14","Población infantil 0–14",profiles.summary.children_0_14,"niños","2024",territory),fact("verified_pediatric_facilities","Recursos AP verificados",profiles.summary.eligible_pediatric_facilities,"recursos","2026",territory)];
 if(territory.kind==="territorial_component")return [fact("accessibility_ap","Estado de acceso terrestre","Transferencia interinsular requerida","estado","2024",territory,"requires_interisland_transfer")];
 return [];
}
function exactSeries(territory:ReportTerritory){
 if(territory.kind!=="island")return [];
 return timePoints.filter(point=>point.geography_id===territory.id&&metricById(point.metric_id)?.geography_levels.includes("island"));
}
function regionalSeries(){return timePoints.filter(point=>point.geography_id==="canarias"&&REGIONAL_METRICS.includes(point.metric_id));}
function toSections(territory:ReportTerritory,facts:ReportFact[],series:TimePoint[]){
 const sections:ReportSection[]=[];
 for(const domain of DOMAIN_METRICS){
  if(domain.id==="hospital")continue;
  const domainFacts=facts.filter(item=>domain.metrics.includes(item.metric_id));
  const domainSeries=series.filter(item=>domain.metrics.includes(item.metric_id));
  if(!domainFacts.length&&!domainSeries.length)continue;
  sections.push({id:domain.id,title:domain.title,metricIds:[...new Set([...domainFacts.map(item=>item.metric_id),...domainSeries.map(item=>item.metric_id)])],facts:domainFacts,series:domainSeries,visual:domain.id==="access"?"map":domainSeries.length?"line":"table"});
 }
 return sections;
}
function regionalSections(){
 const points=regionalSeries();return REGIONAL_METRICS.flatMap(metricId=>{const metricPoints=points.filter(point=>point.metric_id===metricId);if(!metricPoints.length)return [];const metric=def(metricId);return [{id:"regional-"+metricId,title:metric.label,metricIds:[metricId],facts:[],series:metricPoints,visual:"line" as const,note:"Dato de Canarias. No se atribuye al territorio analizado."}]});
}
function displayUnit(unit:string){return ({professionals:"pediatras",consultations:"consultas",persons:"personas asignadas","assigned_persons/professional":"niños por pediatra",births:"nacimientos",percent:"%",consultations_per_assigned_person_year:"consultas por persona asignada y año",consultations_per_professional:"consultas por pediatra",persons_per_professional:"niños por pediatra"} as Record<string,string>)[unit]??unit}
function format(value:number,unit:string){const label=displayUnit(unit);return nf.format(value)+(label==="%"||label.startsWith("%")?" %":" "+label)}
function seriesFor(series:TimePoint[],metricId:string){return series.filter(point=>point.metric_id===metricId).slice().sort((a,b)=>a.period.localeCompare(b.period))}
function relativeChange(first:number,last:number){return first===0?null:(last-first)/Math.abs(first)*100}
function trendVerb(change:number){return change>0?"aumentó":change<0?"descendió":"se mantuvo"}
function changeText(first:TimePoint,last:TimePoint){const change=last.value-first.value,pct=relativeChange(first.value,last.value);return `${trendVerb(change)} de ${format(first.value,first.unit)} a ${format(last.value,last.unit)}${pct===null?"":` (${change>=0?"+":""}${nf.format(pct)} %)`}`}
function finding(id:string,text:string,metricIds:string[],period:string):ExecutiveFinding{return {id,text,metricIds:[...new Set(metricIds)],period}}
function buildFindings(territory:ReportTerritory,facts:ReportFact[],series:TimePoint[]){
 const findings:ExecutiveFinding[]=[];
 if(territory.kind==="island"){
  const population=seriesFor(series,"child_population_assigned_0_14"),pediatricians=seriesFor(series,"pediatricians_ap"),ratio=seriesFor(series,"assigned_children_per_pediatrician");
  const periods=[population[0]?.period,pediatricians[0]?.period,ratio[0]?.period].filter(Boolean) as string[];
  const ends=[population.at(-1)?.period,pediatricians.at(-1)?.period,ratio.at(-1)?.period].filter(Boolean) as string[];
  const start=periods.sort().at(-1),end=ends.sort()[0];
  const at=(points:TimePoint[],period:string|undefined)=>points.find(point=>point.period===period);
  const p0=at(population,start),p1=at(population,end),d0=at(pediatricians,start),d1=at(pediatricians,end),r0=at(ratio,start),r1=at(ratio,end);
  if(start&&end&&p0&&p1&&d0&&d1&&r0&&r1)findings.push(finding("workforce-balance",`Entre ${start} y ${end}, la población infantil asignada ${changeText(p0,p1)}, mientras que la dotación de pediatras ${changeText(d0,d1)}. La relación pasó de ${format(r0.value,r0.unit)} a ${format(r1.value,r1.unit)}. Es una descripción de dotación y población asignada, no de calidad asistencial.`,["child_population_assigned_0_14","pediatricians_ap","assigned_children_per_pediatrician"],`${start}–${end}`));
 }
 const priority=["pediatric_consultations","pediatric_frequentation","births","preterm_rate"];
 for(const metricId of priority){
  const points=seriesFor(series,metricId);if(points.length<2)continue;const first=points[0],last=points.at(-1)!,metric=def(metricId);
  findings.push(finding(`trend-${metricId}`,`Entre ${first.period} y ${last.period}, ${metric.label.toLocaleLowerCase("es")} ${changeText(first,last)}.`,[metricId],`${first.period}–${last.period}`));
 }
 if(territory.kind==="island"){
  const profile=profiles.islands.find(item=>item.island_id===territory.id)!;
  const medianDelta=(profile.median_travel_minutes??0)-profiles.summary.median_travel_minutes;
  if(profile.median_travel_minutes!==null)findings.push(finding("access-comparison",`En 2024, la mediana de acceso geográfico potencial fue ${nf.format(profile.median_travel_minutes)} min, frente a ${nf.format(profiles.summary.median_travel_minutes)} min en el conjunto de las siete islas (${medianDelta>=0?"+":""}${nf.format(medianDelta)} min). El ${nf.format(profile.pct_under_15_total)} % de la población infantil quedó a menos de 15 min, frente al ${nf.format(profiles.summary.pct_under_15_total)} % del conjunto.`,["accessibility_ap"],"2024"));
  const latestByMetric=new Map<string,TimePoint>();for(const point of timePoints.filter(item=>item.period&&item.geography_level==="island"))if(!latestByMetric.get(point.metric_id)||point.period>latestByMetric.get(point.metric_id)!.period)latestByMetric.set(point.metric_id,point);
  for(const metricId of ["child_population_assigned_0_14","pediatricians_ap"]){const period=latestByMetric.get(metricId)?.period;if(!period||!additiveMetrics.has(metricId))continue;const all=timePoints.filter(item=>item.metric_id===metricId&&item.period===period);const own=all.find(item=>item.geography_id===territory.id);const total=all.reduce((sum,item)=>sum+item.value,0);if(own&&total>0)findings.push(finding(`share-${metricId}`,`${territory.name} concentra ${nf.format(own.value/total*100)} % del total de las siete islas para ${def(metricId).label.toLocaleLowerCase("es")} en ${period}.`,[metricId],period));}
 }else{
  for(const item of facts){if(item.value!==null&&findings.length<5)findings.push(finding(`fact-${item.metric_id}-${item.label}`,`${item.label}: ${typeof item.value==="number"?format(item.value,item.unit):item.value} (${item.period}).`,[item.metric_id],item.period))}
 }
 return findings.slice(0,10);
}
export function buildTerritorialReport(geographyId:string):TerritorialReport|null{
 const territory=resolveTerritory(geographyId);if(!territory)return null;
 const facts=currentFacts(territory),series=exactSeries(territory),sections=toSections(territory,facts,series),regionalContext=territory.kind==="archipelago"?[]:regionalSections();
 const usedMetrics=[...new Set([...sections.flatMap(item=>item.metricIds),...regionalContext.flatMap(item=>item.metricIds)])];
 const sourceIds=[...new Set(usedMetrics.flatMap(metricId=>def(metricId).source_ids))];
 const availableDomainIds=new Set(sections.map(item=>item.id));
 const unavailableDomains=DOMAIN_METRICS.filter(domain=>!availableDomainIds.has(domain.id)&&domain.id!=="hospital").map(domain=>domain.title);
 const limitations=["Informe descriptivo construido solo con métricas y fuentes registradas.","Los análisis territoriales describen asociaciones ecológicas y accesibilidad potencial; no estiman riesgo individual ni causalidad.","Los datos regionales aparecen separados y no se atribuyen al territorio.",...(territory.publicationStatus==="limited"?["El detalle territorial está limitado por las reglas de publicación o por ausencia de una serie propia."]:[])];
 const findings=buildFindings(territory,facts,series);
 const interpretation:ReportInterpretation={known:findings.slice(0,5),cannotConclude:["No permite atribuir causas a las diferencias observadas ni estimar riesgo individual.","No mide calidad asistencial, tiempo hasta recibir atención ni resultados clínicos individuales.","Las comparaciones describen periodos, universos y geografías registrados; no prueban que un indicador explique otro."],missingData:[...unavailableDomains.slice(0,5),"Geometría oficial vigente de Zonas Básicas de Salud para las siete islas"]};
 return {territory,sections,regionalContext,findings,interpretation,unavailableDomains,sourceIds,limitations};
}
export function metricsForTerritorialReport(geographyId:string):MetricDefinition[]{const report=buildTerritorialReport(geographyId);if(!report)return [];return [...new Set([...report.sections,...report.regionalContext].flatMap(item=>item.metricIds))].map(def)}
