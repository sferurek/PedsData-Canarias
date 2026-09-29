"use client";
import {useEffect,useMemo,useRef,useState} from "react";
import * as maplibregl from "maplibre-gl";
import type {Map as MapLibreMap,MapLayerMouseEvent} from "maplibre-gl";
import type {MunicipalityProfile} from "@/lib/types";
import {classificationBreaks,stepExpression,type ClassificationMethod} from "@/lib/classification";
import {metricById,timePoints,islandLabels} from "@/lib/semantic";
import {MapLegend,type ContextLayer} from "./MapLegend";
import {ResultSourcesLink} from "./ResultSourcesLink";

const BOUNDS:Record<string,[[number,number],[number,number]]>={"el-hierro":[[-18.2,27.6],[-17.85,27.9]],"la-gomera":[[-17.4,28],[-17,28.25]],"la-palma":[[-18,28.45],[-17.65,28.9]],tenerife:[[-16.95,27.95],[-16,28.65]],"gran-canaria":[[-15.85,27.7],[-15.35,28.2]],fuerteventura:[[-14.55,28],[-13.75,28.8]],lanzarote:[[-13.9,28.8],[-13.4,29.32]]};
const CANARY:[[number,number],[number,number]]=[[-18.35,27.45],[-13.25,29.45]];
const BAND:Record<string,string>={under_5:"Menos de 5 min","5_to_under_10":"5–<10 min","10_to_under_15":"10–<15 min","15_to_under_20":"15–<20 min","20_to_under_30":"20–<30 min","30_or_more":"30 min o más",requires_interisland_transfer:"Transferencia interinsular requerida",not_evaluated:"No evaluable"};
const COLORS=["#163f5b","#15728e","#20aeb9","#62e0d5"];
const metadata:Record<ContextLayer,{label:string;metric:string;period:number;scope:"grid"|"municipality"|"island"|"station";property?:string;fixed?:number[]}>={
 accessibility:{label:"Accesibilidad pediátrica",metric:"accessibility_ap",period:2024,scope:"grid"},
 income:{label:"Renta por persona",metric:"income_mean_per_person",period:2023,scope:"municipality",property:"income_mean_per_person_2023"},
 density:{label:"Densidad infantil",metric:"child_density",period:2024,scope:"municipality",property:"child_density_per_km2"},
 degurba:{label:"Urbanización DEGURBA",metric:"degurba",period:2021,scope:"municipality",property:"degurba_class"},
 pediatricians_ap:{label:"Pediatras AP",metric:"pediatricians_ap",period:2024,scope:"island"},
 pediatric_frequentation:{label:"Frecuentación pediátrica",metric:"pediatric_frequentation",period:2024,scope:"island"},
 preterm_rate:{label:"Prematuridad",metric:"preterm_rate",period:2024,scope:"island",fixed:[5,7,9]},
 PM10:{label:"PM10",metric:"PM10",period:2025,scope:"station",property:"PM10",fixed:[10,20,40]},
 "PM2.5":{label:"PM2,5",metric:"PM2.5",period:2025,scope:"station",property:"PM2.5",fixed:[5,10,20]},
 NO2:{label:"NO₂",metric:"NO2",period:2025,scope:"station",property:"NO2",fixed:[10,20,40]}
};
function valuesFor(layer:ContextLayer,year:number,municipalities:MunicipalityProfile[]){
 const item=metadata[layer];
 if(item.scope==="island")return timePoints.filter(point=>point.metric_id===item.metric&&point.period===String(year));
 if(item.scope==="municipality"&&item.property&&layer!=="degurba")return municipalities.map(row=>Number(row[item.property as keyof MunicipalityProfile])).filter(Number.isFinite);
 return [];
}

export function AccessibilityMap({municipalities,initialIsland="all",initialLayer="accessibility"}:{municipalities:MunicipalityProfile[];initialIsland?:string;initialLayer?:ContextLayer}){
 const container=useRef<HTMLDivElement>(null),mapRef=useRef<MapLibreMap|null>(null);
 const [island,setIsland]=useState(initialIsland),[municipality,setMunicipality]=useState("all"),[layer,setLayer]=useState<ContextLayer>(initialLayer),[year,setYear]=useState(metadata[initialLayer].period);
 const [state,setState]=useState<"loading"|"ready"|"error">("loading"),[detail,setDetail]=useState<Record<string,unknown>|null>(null),[facilities,setFacilities]=useState(true),[stations,setStations]=useState(true),[boundaries,setBoundaries]=useState(true);
 const item=metadata[layer],definition=metricById(item.metric)!;
 const availableYears=useMemo(()=>item.scope==="island"?[...new Set(timePoints.filter(point=>point.metric_id===item.metric).map(point=>Number(point.period.slice(0,4))))].sort((a,b)=>a-b):[item.period],[item.metric,item.period,item.scope]);
 const rawValues=useMemo(()=>valuesFor(layer,year,municipalities),[layer,year,municipalities]);
 const breaks=useMemo(()=>{
  const numbers=rawValues.map(value=>typeof value==="number"?value:value.value);
  return layer==="degurba"?[]:classificationBreaks(numbers,(definition.classification_method??"fixed_thresholds") as ClassificationMethod,4,item.fixed??[]);
 },[definition.classification_method,item.fixed,layer,rawValues]);

 useEffect(()=>{if(!container.current||mapRef.current)return;maplibregl.setWorkerUrl("/maplibre/maplibre-gl-worker.mjs");
  const map=new maplibregl.Map({container:container.current,style:{version:8,sources:{},layers:[{id:"background",type:"background",paint:{"background-color":"#031b2c"}}]},bounds:CANARY,fitBoundsOptions:{padding:28},attributionControl:false});mapRef.current=map;
  map.addControl(new maplibregl.NavigationControl({showCompass:false}),"top-right");map.addControl(new maplibregl.AttributionControl({customAttribution:"ISTAC · INE · Gobierno de Canarias · OSM"}));
  const init=()=>{map.addSource("municipalities",{type:"geojson",data:"/data/municipalities.geojson"});map.addLayer({id:"context-fill",type:"fill",source:"municipalities",layout:{visibility:"none"},paint:{"fill-color":"#15728e","fill-opacity":.84}});map.addLayer({id:"municipality-line",type:"line",source:"municipalities",paint:{"line-color":"#55a5b0","line-width":.7}});
   map.addSource("islands",{type:"geojson",data:"/data/islands.geojson"});map.addLayer({id:"island-fill",type:"fill",source:"islands",layout:{visibility:"none"},paint:{"fill-color":"#20aeb9","fill-opacity":.84}});map.addLayer({id:"island-line",type:"line",source:"islands",paint:{"line-color":"#9cebf0","line-width":1.2}});
   map.addSource("accessibility",{type:"geojson",data:"/data/accessibility-grid.geojson"});map.addLayer({id:"accessibility-fill",type:"fill",source:"accessibility",paint:{"fill-color":["match",["get","band"],"under_5","#17d8c4","5_to_under_10","#4fc9a7","10_to_under_15","#8fd690","15_to_under_20","#e0d572","20_to_under_30","#f1a85a","30_or_more","#ef765e","requires_interisland_transfer","#a98bff","#657b86"],"fill-opacity":.88,"fill-outline-color":"rgba(255,255,255,.3)"}});
   map.addSource("facilities",{type:"geojson",data:"/data/facilities.geojson"});map.addLayer({id:"facilities",type:"circle",source:"facilities",paint:{"circle-radius":3.5,"circle-color":"#2de2e6","circle-stroke-color":"#031522","circle-stroke-width":1.5}});
   map.addSource("air",{type:"geojson",data:"/data/air-stations.geojson"});map.addLayer({id:"air-stations",type:"circle",source:"air",layout:{visibility:"none"},paint:{"circle-radius":8,"circle-color":"#7aa7ff","circle-stroke-color":"#d9ffff","circle-stroke-width":2}});
   const click=(id:string)=>(event:MapLayerMouseEvent)=>{const properties=event.features?.[0]?.properties;if(properties)setDetail({...properties,__scope:id})};for(const id of ["accessibility-fill","context-fill","island-fill","air-stations"]){map.on("click",id,click(id));map.on("mouseenter",id,()=>map.getCanvas().style.cursor="pointer");map.on("mouseleave",id,()=>map.getCanvas().style.cursor="")}
   map.once("idle",()=>setState("ready"));
  };if(map.isStyleLoaded())init();else map.once("style.load",init);map.on("error",event=>{if(!map.isStyleLoaded())setState("error");console.error(event.error)});return()=>{map.remove();mapRef.current=null}
 },[]);

 useEffect(()=>{const map=mapRef.current;if(!map||state!=="ready")return;const scope=item.scope;
  const filters:unknown[]=[];if(island!=="all")filters.push(["==",["get","island_id"],island]);if(municipality!=="all")filters.push(["==",["get","municipality_id"],municipality]);const filter=filters.length===0?null:filters.length===1?filters[0]:["all",...filters];
  map.setFilter("accessibility-fill",filter as never);map.setFilter("context-fill",filter as never);map.setFilter("island-fill",island==="all"?null:["==",["get","island_id"],island] as never);
  map.setFilter("facilities",island==="all"?null:["==",["get","island_id"],island] as never);
  const access=scope==="grid",municipal=scope==="municipality",insular=scope==="island",air=scope==="station";
  map.setLayoutProperty("accessibility-fill","visibility",access?"visible":"none");map.setLayoutProperty("context-fill","visibility",municipal?"visible":"none");map.setLayoutProperty("island-fill","visibility",insular?"visible":"none");
  map.setLayoutProperty("facilities","visibility",facilities?"visible":"none");map.setLayoutProperty("air-stations","visibility",air&&stations?"visible":"none");map.setLayoutProperty("municipality-line","visibility",boundaries?"visible":"none");map.setLayoutProperty("island-line","visibility",boundaries?"visible":"none");
  if(municipal&&item.property){if(layer==="degurba")map.setPaintProperty("context-fill","fill-color",["match",["get","degurba_class"],"urban_centre","#247ea0","urban_cluster","#45b8b6","rural","#c9a662","#607581"] as never);else map.setPaintProperty("context-fill","fill-color",stepExpression(item.property,breaks,COLORS) as never)}
  if(insular){const rows=rawValues as typeof timePoints;const expression:unknown[]=["match",["get","island_id"]];rows.forEach(row=>{const index=breaks.findIndex(value=>row.value<value);expression.push(row.geography_id,COLORS[index===-1?COLORS.length-1:index])});expression.push("#607581");map.setPaintProperty("island-fill","fill-color",expression as never)}
  if(air&&item.property){const stationFilter:unknown[]=[];if(island!=="all")stationFilter.push(["==",["get","island_id"],island]);stationFilter.push(["!=",["get",item.property],null]);map.setFilter("air-stations",["all",...stationFilter] as never);map.setPaintProperty("air-stations","circle-color",stepExpression(item.property,breaks,COLORS) as never)}
  map.fitBounds(island==="all"?CANARY:BOUNDS[island],{padding:38,duration:400});setDetail(null);
 },[state,island,municipality,layer,year,facilities,stations,boundaries,item.scope,item.property,breaks,rawValues]);
 const available=municipalities.filter(row=>island==="all"||row.island_id===island);
 const detailScope=String(detail?.__scope??"");
 const islandPoint=detailScope==="island-fill"?timePoints.find(point=>point.metric_id===item.metric&&point.period===String(year)&&point.geography_id===detail?.island_id):undefined;
 const period=item.scope==="island"?year:item.period;
 return <div className="map-shell"><div className="map-toolbar">
  <label>Ámbito insular<select value={island} onChange={event=>{setIsland(event.target.value);setMunicipality("all")}}><option value="all">Canarias · 7 islas</option>{Object.entries(islandLabels).filter(([id])=>!["canarias","la-graciosa"].includes(id)).map(([id,label])=><option key={id} value={id}>{label}</option>)}</select></label>
  <label>Municipio<select value={municipality} onChange={event=>setMunicipality(event.target.value)} disabled={item.scope==="island"}><option value="all">Todos los municipios</option>{available.map(row=><option key={row.municipality_id} value={row.municipality_id}>{row.municipality_name}</option>)}</select></label>
  <label>Capa principal<select aria-label="Capa principal" value={layer} onChange={event=>{const next=event.target.value as ContextLayer;setLayer(next);setYear(metadata[next].period)}}><option value="accessibility">Accesibilidad</option><option value="income">Renta</option><option value="density">Densidad infantil</option><option value="degurba">Urbanización</option><option value="pediatricians_ap">Pediatras AP</option><option value="pediatric_frequentation">Frecuentación</option><option value="PM10">PM10</option><option value="PM2.5">PM2,5</option><option value="NO2">NO₂</option><option value="preterm_rate">Prematuridad</option></select></label>
  <label>Año<select aria-label="Año de la capa" value={year} onChange={event=>setYear(Number(event.target.value))} disabled={availableYears.length===1}>{availableYears.map(value=><option key={value}>{value}</option>)}</select></label>
  <span className="layer-label">{item.label} · {definition.map_geography}</span>
 </div><fieldset className="map-aux"><legend>Capas auxiliares</legend><label><input type="checkbox" checked={facilities} onChange={event=>setFacilities(event.target.checked)}/>Centros</label><label><input type="checkbox" checked={stations} onChange={event=>setStations(event.target.checked)}/>Estaciones</label><label><input type="checkbox" checked={boundaries} onChange={event=>setBoundaries(event.target.checked)}/>Límites</label></fieldset>
 <div className="map-stage"><div ref={container} className="map" aria-label="Mapa temático pediátrico de Canarias"/>{state==="loading"&&<div className="map-state" role="status">Cargando capa validada…</div>}{state==="error"&&<div className="map-state" role="alert">El mapa no pudo cargarse. Los indicadores siguen disponibles en tabla.</div>}
 {detail&&<aside className="map-detail" aria-live="polite"><button onClick={()=>setDetail(null)} aria-label="Cerrar detalle">×</button><span className="eyebrow">{item.label} · {period}</span><strong>{detailScope==="island-fill"?String(detail.island_name):detailScope==="air-stations"?String(detail.name):detailScope==="context-fill"?String(detail.municipality_name):BAND[String(detail.band)]??"Estado no disponible"}</strong><p>{detailScope==="island-fill"?(islandPoint?islandPoint.value.toLocaleString("es-ES")+" "+islandPoint.unit:"Sin dato"):detailScope==="air-stations"?(detail[item.property??""]==null?"Sin observación":String(detail[item.property??""])+" µg/m³"):detailScope==="context-fill"?(layer==="income"?String(detail.income_mean_per_person_2023)+" €/persona":layer==="density"?String(detail.child_density_per_km2)+" niños/km²":String(detail.degurba_class).replace("_"," ")):String(detail.nearest_facility_name??"No asignado")}</p><small>{definition.source_ids.join(" · ")} · {definition.classification_method}</small></aside>}</div>
 <MapLegend layer={layer} year={period} breaks={breaks}/><details className="map-text-alternative"><summary>Alternativa textual del mapa</summary><p><b>{item.label}</b> · {period} · geografía real: {definition.map_geography}. {definition.description}</p>{item.scope==="island"&&<ul>{(rawValues as typeof timePoints).map(point=><li key={point.geography_id}>{islandLabels[point.geography_id]??point.geography_id}: {point.value.toLocaleString("es-ES")} {point.unit}</li>)}</ul>}<p>Método de clasificación: {definition.classification_method}. Fuentes: {definition.source_ids.join(" · ")}.</p></details><ResultSourcesLink metricId={item.metric} period={period} geography={island==="all"?definition.map_geography??undefined:island} result={"Mapa · "+item.label}/></div>;
}
