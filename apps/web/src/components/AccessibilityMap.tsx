"use client";
import {useEffect,useMemo,useRef,useState} from "react";
import * as maplibregl from "maplibre-gl";
import type {Map as MapLibreMap,MapLayerMouseEvent} from "maplibre-gl";
import type {MunicipalityProfile} from "@/lib/types";
import {classificationBreaks,stepExpression,type ClassificationMethod} from "@/lib/classification";
import {metricById,timePoints,islandLabels} from "@/lib/semantic";
import {MapLegend,type ContextLayer} from "./MapLegend";
import {ResultSourcesLink} from "./ResultSourcesLink";

const BOUNDS:Record<string,[[number,number],[number,number]]>={
 "el-hierro":[[-18.2,27.6],[-17.85,27.9]],
 "la-gomera":[[-17.4,28],[-17,28.25]],
 "la-palma":[[-18,28.45],[-17.65,28.9]],
 tenerife:[[-16.95,27.95],[-16,28.65]],
 "gran-canaria":[[-15.85,27.7],[-15.35,28.2]],
 fuerteventura:[[-14.55,28],[-13.75,28.8]],
 lanzarote:[[-13.9,28.8],[-13.4,29.32]]
};
const CANARY:[[number,number],[number,number]]=[[-18.35,27.45],[-13.25,29.45]];
const BAND:Record<string,string>={
 under_5:"Menos de 5 min",
 "5_to_under_10":"5–<10 min",
 "10_to_under_15":"10–<15 min",
 "15_to_under_20":"15–<20 min",
 "20_to_under_30":"20–<30 min",
 "30_or_more":"30 min o más",
 requires_interisland_transfer:"Transferencia interinsular requerida",
 not_evaluated:"No evaluable"
};
const COLORS=["#0f4c6d","#087f9d","#12b8c4","#4fe1d2"];
const islandCenter=(id:string):[number,number]=>{const bounds=BOUNDS[id];return bounds?[(bounds[0][0]+bounds[1][0])/2,(bounds[0][1]+bounds[1][1])/2]:[-15.5,28.3]};
function islandValueLabel(layer:ContextLayer,value:number){
 const formatted=new Intl.NumberFormat("es-ES",{maximumFractionDigits:1}).format(value);
 if(layer==="pediatricians_ap")return formatted+" pediatras";
 if(layer==="assigned_children_per_pediatrician")return formatted+" niños/pediatra";
 if(layer==="pediatric_consultations")return formatted+" consultas";
 if(layer==="pediatric_frequentation")return formatted+" consultas/persona/año";
 if(layer==="child_population_assigned_0_14")return formatted+" niños";
 if(layer==="births")return formatted+" nacimientos";
 if(layer==="preterm_rate")return formatted+" %";
 return formatted;
}

type Scope="grid"|"municipality"|"island"|"station"|"facility";
type LayerMeta={
 label:string;
 metric:string;
 period:number;
 scope:Scope;
 resolution:string;
 explanation:string;
 property?:string;
 fixed?:number[];
};

const metadata:Record<ContextLayer,LayerMeta>={
 accessibility:{
  label:"Accesibilidad a Pediatría AP",
  metric:"accessibility_ap",
  period:2024,
  scope:"grid",
  resolution:"Malla territorial de 250 m",
  explanation:"El mapa representa el tiempo estimado de desplazamiento por carretera desde las celdas con población infantil hasta el recurso de Pediatría de Atención Primaria verificado más próximo. Los colores expresan bandas de tiempo y no distancia lineal."
 },
 facilities:{
  label:"Centros pediátricos AP",
  metric:"verified_pediatric_facilities",
  period:2026,
  scope:"facility",
  resolution:"Centro sanitario",
  explanation:"El mapa localiza los recursos de Pediatría de Atención Primaria verificados que se utilizan como destinos asistenciales en el análisis de accesibilidad."
 },
 child_population_assigned_0_14:{
  label:"Población infantil asignada",
  metric:"child_population_assigned_0_14",
  period:2024,
  scope:"island",
  resolution:"Isla",
  explanation:"El mapa compara la población de 0 a 14 años asignada a Atención Primaria en cada isla para el año seleccionado. La intensidad de color representa el valor insular registrado."
 },
 pediatricians_ap:{
  label:"Pediatras AP",
  metric:"pediatricians_ap",
  period:2024,
  scope:"island",
  resolution:"Isla",
  explanation:"El mapa representa el número de profesionales de Pediatría de Atención Primaria registrado en cada isla para el año seleccionado."
 },
 assigned_children_per_pediatrician:{
  label:"Población asignada por pediatra",
  metric:"assigned_children_per_pediatrician",
  period:2024,
  scope:"island",
  resolution:"Isla",
  explanation:"El mapa representa la población infantil asignada por profesional de Pediatría de Atención Primaria en cada isla. Valores mayores indican más población asignada por pediatra."
 },
 pediatric_consultations:{
  label:"Consultas de Pediatría AP",
  metric:"pediatric_consultations",
  period:2024,
  scope:"island",
  resolution:"Isla",
  explanation:"El mapa muestra el volumen anual de consultas de Pediatría de Atención Primaria por isla para el periodo seleccionado."
 },
 pediatric_frequentation:{
  label:"Frecuentación pediátrica",
  metric:"pediatric_frequentation",
  period:2024,
  scope:"island",
  resolution:"Isla",
  explanation:"El mapa representa la frecuentación pediátrica anual por isla, expresada como consultas por persona y año según la definición registrada en el catálogo."
 },
 births:{
  label:"Nacimientos",
  metric:"births",
  period:2024,
  scope:"island",
  resolution:"Isla",
  explanation:"El mapa representa el número de nacimientos registrados en cada isla para el año seleccionado."
 },
 income:{
  label:"Renta por persona",
  metric:"income_mean_per_person",
  period:2023,
  scope:"municipality",
  property:"income_mean_per_person_2023",
  resolution:"Municipio",
  explanation:"El mapa representa la renta media por persona disponible a nivel municipal. Es un indicador general del territorio y no se interpreta como medida directa de pobreza infantil."
 },
 density:{
  label:"Densidad infantil",
  metric:"child_density",
  period:2024,
  scope:"municipality",
  property:"child_density_per_km2",
  resolution:"Municipio",
  explanation:"El mapa representa la densidad estimada de población infantil por municipio, expresada como niños de 0 a 14 años por kilómetro cuadrado."
 },
 degurba:{
  label:"Urbanización DEGURBA",
  metric:"degurba",
  period:2021,
  scope:"municipality",
  property:"degurba_class",
  resolution:"Municipio",
  explanation:"El mapa clasifica cada municipio por la categoría territorial DEGURBA dominante en la población infantil: centro urbano, agrupación urbana o rural."
 },
 preterm_rate:{
  label:"Prematuridad",
  metric:"preterm_rate",
  period:2024,
  scope:"island",
  resolution:"Isla",
  fixed:[5,7,9],
  explanation:"El mapa representa la tasa de nacimientos pretérmino por isla para el año seleccionado. La comparación es territorial y no estima riesgo individual."
 },
 PM10:{
  label:"PM10",
  metric:"PM10",
  period:2025,
  scope:"station",
  property:"PM10",
  resolution:"Estación de calidad del aire",
  fixed:[10,20,40],
  explanation:"El mapa muestra los valores observados de PM10 en las estaciones disponibles. Son mediciones puntuales de estación y no una interpolación de exposición para toda la población."
 },
 "PM2.5":{
  label:"PM2,5",
  metric:"PM2.5",
  period:2025,
  scope:"station",
  property:"PM2.5",
  resolution:"Estación de calidad del aire",
  fixed:[5,10,20],
  explanation:"El mapa muestra los valores observados de PM2,5 en las estaciones disponibles. Son mediciones puntuales y no una superficie continua de exposición."
 },
 NO2:{
  label:"NO₂",
  metric:"NO2",
  period:2025,
  scope:"station",
  property:"NO2",
  resolution:"Estación de calidad del aire",
  fixed:[10,20,40],
  explanation:"El mapa muestra los valores observados de NO₂ en las estaciones disponibles. Las cifras corresponden a puntos de medida y no deben extrapolarse automáticamente a cada municipio."
 }
};

function valuesFor(layer:ContextLayer,year:number,municipalities:MunicipalityProfile[]){
 const item=metadata[layer];
 if(item.scope==="island")return timePoints.filter(point=>point.metric_id===item.metric&&point.period===String(year));
 if(item.scope==="municipality"&&item.property&&layer!=="degurba")return municipalities.map(row=>Number(row[item.property as keyof MunicipalityProfile])).filter(Number.isFinite);
 return [];
}

export function AccessibilityMap({municipalities,initialIsland="all",initialLayer="accessibility"}:{municipalities:MunicipalityProfile[];initialIsland?:string;initialLayer?:ContextLayer}){
 const container=useRef<HTMLDivElement>(null),mapRef=useRef<MapLibreMap|null>(null),valueMarkersRef=useRef<maplibregl.Marker[]>([]);
 const [island,setIsland]=useState(initialIsland),[municipality,setMunicipality]=useState("all"),[layer,setLayer]=useState<ContextLayer>(initialLayer),[year,setYear]=useState(metadata[initialLayer].period);
 const [state,setState]=useState<"loading"|"ready"|"error">("loading"),[detail,setDetail]=useState<Record<string,unknown>|null>(null),[facilities,setFacilities]=useState(true),[stations,setStations]=useState(false);
 const item=metadata[layer],definition=metricById(item.metric)!;
 const availableYears=useMemo(()=>{
  if(item.scope!=="island")return [item.period];
  const years=[...new Set(timePoints.filter(point=>point.metric_id===item.metric).map(point=>Number(point.period.slice(0,4))))].filter(Number.isFinite).sort((a,b)=>a-b);
  return years.length?years:[item.period];
 },[item.metric,item.period,item.scope]);
 const rawValues=useMemo(()=>valuesFor(layer,year,municipalities),[layer,year,municipalities]);
 const breaks=useMemo(()=>{
  const numbers=rawValues.map(value=>typeof value==="number"?value:value.value);
  return layer==="degurba"||layer==="facilities"||layer==="accessibility"?[]:classificationBreaks(numbers,(definition.classification_method??"fixed_thresholds") as ClassificationMethod,4,item.fixed??[]);
 },[definition.classification_method,item.fixed,layer,rawValues]);

 useEffect(()=>{if(!container.current||mapRef.current)return;maplibregl.setWorkerUrl("/maplibre/maplibre-gl-worker.mjs");
  const map=new maplibregl.Map({container:container.current,style:{version:8,sources:{opentopomap:{type:"raster",tiles:["https://a.tile.opentopomap.org/{z}/{x}/{y}.png","https://b.tile.opentopomap.org/{z}/{x}/{y}.png","https://c.tile.opentopomap.org/{z}/{x}/{y}.png"],tileSize:256,attribution:'© <a href="https://opentopomap.org" target="_blank" rel="noreferrer">OpenTopoMap</a> · © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap</a> contributors · SRTM'}},layers:[{id:"opentopomap-base",type:"raster",source:"opentopomap",paint:{"raster-opacity":.96,"raster-saturation":-.08,"raster-contrast":-.03,"raster-brightness-max":.98}}]},bounds:CANARY,fitBoundsOptions:{padding:28},attributionControl:false});mapRef.current=map;
  map.addControl(new maplibregl.NavigationControl({showCompass:false}),"top-right");map.addControl(new maplibregl.AttributionControl({compact:false,customAttribution:"PedsData · ISTAC · INE · Gobierno de Canarias"}));
  const init=()=>{map.addSource("municipalities",{type:"geojson",data:"/data/municipalities.geojson"});map.addLayer({id:"context-fill",type:"fill",source:"municipalities",layout:{visibility:"none"},paint:{"fill-color":"#15728e","fill-opacity":.74}});map.addLayer({id:"municipality-line",type:"line",source:"municipalities",paint:{"line-color":"#b2b8b4","line-width":.75}});
   map.addSource("islands",{type:"geojson",data:"/data/islands.geojson"});map.addLayer({id:"island-fill",type:"fill",source:"islands",layout:{visibility:"none"},paint:{"fill-color":"#20aeb9","fill-opacity":.78}});map.addLayer({id:"island-line",type:"line",source:"islands",paint:{"line-color":"#5f6f73","line-width":1.15}});
   map.addSource("accessibility",{type:"geojson",data:"/data/accessibility-grid.geojson"});map.addLayer({id:"accessibility-fill",type:"fill",source:"accessibility",paint:{"fill-color":["match",["get","band"],"under_5","#00d4c4","5_to_under_10","#2fc79f","10_to_under_15","#74cf78","15_to_under_20","#d8c94d","20_to_under_30","#f09a3d","30_or_more","#e95f4f","requires_interisland_transfer","#9b7cff","#657b86"],"fill-opacity":.74,"fill-outline-color":"rgba(255,255,255,.48)"}});
   map.addSource("facilities",{type:"geojson",data:"/data/facilities.geojson"});map.addLayer({id:"facilities",type:"circle",source:"facilities",paint:{"circle-radius":3.5,"circle-color":"#2de2e6","circle-stroke-color":"#f5fbfd","circle-stroke-width":1.5}});
   map.addSource("air",{type:"geojson",data:"/data/air-stations.geojson"});map.addLayer({id:"air-stations",type:"circle",source:"air",layout:{visibility:"none"},paint:{"circle-radius":8,"circle-color":"#7aa7ff","circle-stroke-color":"#d9ffff","circle-stroke-width":2}});

   const click=(id:string)=>(event:MapLayerMouseEvent)=>{const properties=event.features?.[0]?.properties;if(properties)setDetail({...properties,__scope:id})};for(const id of ["accessibility-fill","context-fill","island-fill","air-stations","facilities"]){map.on("click",id,click(id));map.on("mouseenter",id,()=>map.getCanvas().style.cursor="pointer");map.on("mouseleave",id,()=>map.getCanvas().style.cursor="")}
   map.once("idle",()=>setState("ready"));
  };if(map.isStyleLoaded())init();else map.once("style.load",init);map.on("error",event=>{if(!map.isStyleLoaded())setState("error");console.error(event.error)});return()=>{valueMarkersRef.current.forEach(marker=>marker.remove());valueMarkersRef.current=[];map.remove();mapRef.current=null}
 },[]);

 useEffect(()=>{const map=mapRef.current;if(!map||state!=="ready")return;valueMarkersRef.current.forEach(marker=>marker.remove());valueMarkersRef.current=[];const scope=item.scope;
  const filters:unknown[]=[];if(island!=="all")filters.push(["==",["get","island_id"],island]);if(municipality!=="all")filters.push(["==",["get","municipality_id"],municipality]);const filter=filters.length===0?null:filters.length===1?filters[0]:["all",...filters];
  map.setFilter("accessibility-fill",filter as never);map.setFilter("context-fill",filter as never);map.setFilter("island-fill",island==="all"?null:["==",["get","island_id"],island] as never);
  map.setFilter("facilities",island==="all"?null:["==",["get","island_id"],island] as never);
  const access=scope==="grid",municipal=scope==="municipality",insular=scope==="island",air=scope==="station",facility=scope==="facility";
  map.setLayoutProperty("accessibility-fill","visibility",access?"visible":"none");map.setLayoutProperty("context-fill","visibility",municipal?"visible":"none");map.setLayoutProperty("island-fill","visibility",insular?"visible":"none");
  map.setLayoutProperty("facilities","visibility",facility||facilities?"visible":"none");map.setPaintProperty("facilities","circle-radius",facility?6:3.5);
  map.setLayoutProperty("air-stations","visibility",air||stations?"visible":"none");
  if(municipal&&item.property){if(layer==="degurba")map.setPaintProperty("context-fill","fill-color",["match",["get","degurba_class"],"urban_centre","#247ea0","urban_cluster","#45b8b6","rural","#c9a662","#607581"] as never);else map.setPaintProperty("context-fill","fill-color",stepExpression(item.property,breaks,COLORS) as never)}
  if(insular){const rows=rawValues as typeof timePoints;const expression:unknown[]=["match",["get","island_id"]];rows.forEach(row=>{const index=breaks.findIndex(value=>row.value<value);expression.push(row.geography_id,COLORS[index===-1?COLORS.length-1:index])});expression.push("#607581");map.setPaintProperty("island-fill","fill-color",expression as never);
   rows.filter(row=>island==="all"||row.geography_id===island).forEach(row=>{const el=document.createElement("button");el.type="button";el.className="island-value-marker";el.textContent=islandValueLabel(layer,row.value);el.setAttribute("aria-label",(islandLabels[row.geography_id]??row.geography_id)+": "+el.textContent);el.onclick=()=>setDetail({__scope:"island-fill",island_id:row.geography_id,island_name:islandLabels[row.geography_id]??row.geography_id});const marker=new maplibregl.Marker({element:el,anchor:"center"}).setLngLat(islandCenter(row.geography_id)).addTo(map);valueMarkersRef.current.push(marker)});
  }
  if(air&&item.property){const stationFilter:unknown[]=[];if(island!=="all")stationFilter.push(["==",["get","island_id"],island]);stationFilter.push(["!=",["get",item.property],null]);map.setFilter("air-stations",["all",...stationFilter] as never);map.setPaintProperty("air-stations","circle-color",stepExpression(item.property,breaks,COLORS) as never)}
  else {map.setFilter("air-stations",island==="all"?null:["==",["get","island_id"],island] as never);map.setPaintProperty("air-stations","circle-color","#7aa7ff")}
  map.fitBounds(island==="all"?CANARY:BOUNDS[island],{padding:38,duration:400});setDetail(null);
 },[state,island,municipality,layer,year,facilities,stations,item.scope,item.property,breaks,rawValues]);

 const available=municipalities.filter(row=>island==="all"||row.island_id===island);
 const detailScope=String(detail?.__scope??"");
 const islandPoint=detailScope==="island-fill"?timePoints.find(point=>point.metric_id===item.metric&&point.period===String(year)&&point.geography_id===detail?.island_id):undefined;
 const period=item.scope==="island"?year:item.period;
 const detailValue=detailScope==="island-fill"?(islandPoint?islandPoint.value.toLocaleString("es-ES")+" "+islandPoint.unit:"Sin dato"):
  detailScope==="air-stations"?(detail?.[item.property??""]==null?"Sin observación":String(detail[item.property??""])+" µg/m³"):
  detailScope==="context-fill"?(layer==="income"?String(detail?.income_mean_per_person_2023)+" €/persona":layer==="density"?String(detail?.child_density_per_km2)+" niños/km²":String(detail?.degurba_class??"Sin dato").replace("_"," ")):
  detailScope==="facilities"?"Centro pediátrico AP verificado":
  String(detail?.nearest_facility_name??"No asignado");

 return <div className="map-shell">
  <div className="map-toolbar">
   <label>Ámbito insular<select value={island} onChange={event=>{setIsland(event.target.value);setMunicipality("all")}}><option value="all">Canarias · 7 islas</option>{Object.entries(islandLabels).filter(([id])=>!["canarias","la-graciosa"].includes(id)).map(([id,label])=><option key={id} value={id}>{label}</option>)}</select></label>
   <label>Municipio<select value={municipality} onChange={event=>setMunicipality(event.target.value)} disabled={item.scope==="island"||item.scope==="station"||item.scope==="facility"}><option value="all">Todos los municipios</option>{available.map(row=><option key={row.municipality_id} value={row.municipality_id}>{row.municipality_name}</option>)}</select></label>
   <label className="map-layer-select">Qué quieres ver<select aria-label="Qué quieres ver en el mapa" value={layer} onChange={event=>{const next=event.target.value as ContextLayer;setLayer(next);setYear(metadata[next].period)}}>
    <optgroup label="Acceso y recursos">
     <option value="accessibility">Accesibilidad a Pediatría AP</option>
     <option value="facilities">Centros pediátricos AP</option>
     <option value="child_population_assigned_0_14">Población infantil asignada</option>
    </optgroup>
    <optgroup label="Actividad asistencial">
     <option value="pediatricians_ap">Pediatras AP</option>
     <option value="assigned_children_per_pediatrician">Población asignada por pediatra</option>
     <option value="pediatric_consultations">Consultas pediátricas</option>
     <option value="pediatric_frequentation">Frecuentación pediátrica</option>
    </optgroup>
    <optgroup label="Población y territorio">
     <option value="births">Nacimientos</option>
     <option value="density">Densidad infantil</option>
     <option value="degurba">Urbanización DEGURBA</option>
     <option value="income">Renta por persona</option>
    </optgroup>
    <optgroup label="Resultados">
     <option value="preterm_rate">Prematuridad</option>
    </optgroup>
    <optgroup label="Entorno">
     <option value="PM10">PM10</option>
     <option value="PM2.5">PM2,5</option>
     <option value="NO2">NO₂</option>
    </optgroup>
   </select></label>
   {availableYears.length>1?<label>Año<select aria-label="Año de la capa" value={year} onChange={event=>setYear(Number(event.target.value))}>{availableYears.map(value=><option key={value}>{value}</option>)}</select></label>:<div className="map-year-static"><span>Año</span><strong>{availableYears[0]}</strong></div>}
  </div>
  <fieldset className="map-aux"><legend>Capas auxiliares</legend>{layer!=="facilities"&&<label><input type="checkbox" checked={facilities} onChange={event=>setFacilities(event.target.checked)}/>Centros</label>}{!["PM10","PM2.5","NO2"].includes(layer)&&<label><input type="checkbox" checked={stations} onChange={event=>setStations(event.target.checked)}/>Estaciones</label>}</fieldset>
  <div className="map-stage"><div ref={container} className="map" aria-label="Mapa temático pediátrico de Canarias"/>{state==="loading"&&<div className="map-state" role="status">Cargando capa validada…</div>}{state==="error"&&<div className="map-state" role="alert">El mapa no pudo cargarse. Los indicadores siguen disponibles en tabla.</div>}
   {detail&&<aside className="map-detail" aria-live="polite"><button onClick={()=>setDetail(null)} aria-label="Cerrar detalle">×</button><span className="eyebrow">{detailScope==="facilities"?"Centro pediátrico AP":item.label} · {period}</span><strong>{detailScope==="island-fill"?String(detail.island_name):detailScope==="air-stations"?String(detail.name):detailScope==="context-fill"?String(detail.municipality_name):detailScope==="facilities"?String(detail.name):BAND[String(detail.band)]??"Estado no disponible"}</strong><p>{detailValue}</p><small>{definition.source_ids.join(" · ")} · {definition.classification_method??"observado"}</small></aside>}
  </div>
  <MapLegend layer={layer} year={period} breaks={breaks}/>
  <div className="map-caption"><div><span className="eyebrow">Qué representa este mapa</span><p>{item.explanation}</p></div><span className="map-resolution">Resolución: <strong>{item.resolution}</strong> · Periodo: <strong>{period}</strong></span></div>
  <details className="map-text-alternative"><summary>Alternativa textual del mapa</summary><p><b>{item.label}</b> · {period} · geografía real: {definition.map_geography}. {definition.description}</p>{item.scope==="island"&&<ul>{(rawValues as typeof timePoints).map(point=><li key={point.geography_id}>{islandLabels[point.geography_id]??point.geography_id}: {point.value.toLocaleString("es-ES")} {point.unit}</li>)}</ul>}<p>Método de clasificación: {definition.classification_method??"observado"}. Fuentes: {definition.source_ids.join(" · ")}.</p></details>
  <ResultSourcesLink metricId={item.metric} period={period} geography={island==="all"?definition.map_geography??undefined:island} result={"Mapa · "+item.label}/>
 </div>;
}
