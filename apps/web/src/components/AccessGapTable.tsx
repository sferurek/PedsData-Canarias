"use client";
import {useState} from "react";
import Link from "next/link";
import {formatMinutes,formatNumber,formatPercent} from "@/lib/format";
import type {IslandProfile} from "@/lib/types";
import {SourceMethodPanel} from "./SourceMethodPanel";
import {ResultSourcesLink} from "./ResultSourcesLink";
const optional=[['income','Renta'],['density','Densidad'],['rural','Ruralidad']] as const;
export function AccessGapTable({islands}:{islands:IslandProfile[]}){
 const [visible,setVisible]=useState<Record<string,boolean>>({income:true,density:true,rural:false});
 return <section className="section" id="desigualdad" aria-labelledby="access-gap-title"><div className="section-heading"><div><span className="eyebrow">Pediatric Access Gap · V2</span><h2 id="access-gap-title">Dimensiones separadas, sin puntuación única</h2></div><p>Comparación descriptiva. La renta es general y la coexistencia territorial no implica causalidad.</p></div>
 <fieldset className="column-controls"><legend>Columnas de contexto</legend>{optional.map(([key,label])=><label key={key}><input type="checkbox" checked={visible[key]} onChange={e=>setVisible({...visible,[key]:e.target.checked})}/>{label}</label>)}</fieldset>
 <div className="table-scroll"><table><thead><tr><th>Isla</th><th>Niños 0–14</th><th>Centros</th><th>Niños / centro</th><th>Mediana</th><th>P90</th><th>≥20 min</th>{visible.income&&<th>Renta / persona</th>}{visible.density&&<th>Densidad infantil</th>}{visible.rural&&<th>Niños en celdas rurales</th>}</tr></thead><tbody>{islands.map(i=><tr key={i.island_id}><th><Link href={`/islas/${i.slug}`}>{i.name}</Link></th><td>{formatNumber(i.children_0_14)}</td><td>{formatNumber(i.eligible_pediatric_facilities)}</td><td>{formatNumber(i.children_per_verified_pediatric_facility,1)}</td><td>{formatMinutes(i.median_travel_minutes)}</td><td>{formatMinutes(i.p90_travel_minutes)}</td><td>{formatPercent(i.pct_20_or_more_total)}</td>{visible.income&&<td>{formatNumber(i.income_mean_per_person_2023)} €</td>}{visible.density&&<td>{formatNumber(i.child_density_per_km2,1)}</td>}{visible.rural&&<td>{formatPercent(i.rural_children_pct)}</td>}</tr>)}</tbody></table></div><ResultSourcesLink metricId="accessibility_ap" period={2024} geography="island" result="Pediatric Access Gap"/><SourceMethodPanel compact/></section>
}
