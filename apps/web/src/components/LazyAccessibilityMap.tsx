"use client";
import dynamic from "next/dynamic";
import {useEffect,useRef,useState} from "react";
import type {MunicipalityProfile} from "@/lib/types";
import type {ContextLayer} from "./MapLegend";

const AccessibilityMap=dynamic(()=>import("./AccessibilityMap").then(module=>module.AccessibilityMap),{loading:()=> <div className="map-deferred" role="status">Preparando el mapa temático…</div>});

export function LazyAccessibilityMap(props:{municipalities:MunicipalityProfile[];initialIsland?:string;initialLayer?:ContextLayer}){
 const anchor=useRef<HTMLDivElement>(null);const [active,setActive]=useState(false);
 useEffect(()=>{const node=anchor.current;if(!node)return;const observer=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting)){setActive(true);observer.disconnect()}},{rootMargin:"240px"});observer.observe(node);return()=>observer.disconnect()},[]);
 return <div ref={anchor} className="lazy-map-anchor">{active?<AccessibilityMap {...props}/>:<div className="map-deferred"><strong>Mapa temático interactivo</strong><p>Se carga al llegar a esta sección para reducir el peso inicial. Las tablas y perfiles ofrecen la alternativa textual.</p><button type="button" onClick={()=>setActive(true)}>Cargar mapa</button></div>}</div>
}
