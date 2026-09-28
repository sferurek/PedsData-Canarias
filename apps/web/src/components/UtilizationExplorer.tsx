"use client";
import {useState} from "react";
import data from "@/data/utilization.json";
import {profiles} from "@/lib/data";
import {SourceMethodPanel} from "./SourceMethodPanel";
const labels:Record<string,string>={consultations:"Consultas",distinct_persons:"Personas distintas",frequentation:"Frecuentación general"};
export const formatUtilization=(v:number|null|undefined)=>v==null?"No disponible":new Intl.NumberFormat("es-ES",{maximumFractionDigits:2}).format(v);
export function UtilizationExplorer(){
 const [island,setIsland]=useState("el-hierro"),[year,setYear]=useState(2024),[metric,setMetric]=useState("consultations"),[place,setPlace]=useState("_T");
 const [waiting,setWaiting]=useState("outpatient:PEDIATRIA"),[cut,setCut]=useState("2025-12-31"),[research,setResearch]=useState("consultations");
 const selectedPlace=metric==="frequentation"?"_T":place;
 const selected=data.activity.find(r=>r.island===island&&r.year===year&&r.metric===metric&&r.place===selectedPlace);
 const staff=data.staff.find(r=>r.island===island&&r.year===year);
 const trend=data.activity.filter(r=>r.island===island&&r.metric===metric&&r.place===selectedPlace).sort((a,b)=>a.year-b.year);
 const max=Math.max(...trend.map(r=>r.value??0),1);
 const [kind,specialty]=waiting.split(":");
 const waits=data.waiting.filter(r=>r.kind===kind&&r.specialty===specialty&&r.band==="_T").sort((a,b)=>a.date.localeCompare(b.date));
 const stock=waits.find(r=>r.date===cut);
 const ap=data.activity.find(r=>r.island===island&&r.year===year&&r.metric==="consultations"&&r.place==="_T")?.value;
 const ratio=ap!=null&&staff?.pediatricians?ap/staff.pediatricians:null;
 const profile=profiles.islands.find(r=>r.island_id===island);
 return <>
 <section className="clinical-module" id="ap"><h2>Pediatría AP</h2><p>Servicio Pediatría · OBSERVED / NOT_AVAILABLE · 2007–2024. No equivale a una cohorte de edad individual.</p>
 <div className="clinical-filters">
 <label>Isla<select aria-label="Isla SIAP" value={island} onChange={e=>setIsland(e.target.value)}>{data.islands.map(i=><option key={i.id} value={i.id}>{i.name}</option>)}</select></label>
 <label>Año<select aria-label="Año SIAP" value={year} onChange={e=>setYear(Number(e.target.value))}>{Array.from({length:18},(_,i)=>2024-i).map(y=><option key={y}>{y}</option>)}</select></label>
 <label>Indicador<select aria-label="Indicador SIAP" value={metric} onChange={e=>setMetric(e.target.value)}>{Object.entries(labels).map(([k,v])=><option key={k} value={k}>{v}</option>)}</select></label>
 <label>Lugar<select aria-label="Lugar de consulta" value={selectedPlace} disabled={metric==="frequentation"} onChange={e=>setPlace(e.target.value)}>{[["_T","Total publicado"],["CENTRO","Centro"],["DOMICILIO","Domicilio"],["TELECONSULTA","Teleconsulta"]].map(([k,v])=><option key={k} value={k}>{v}</option>)}</select></label></div>
 <div className="clinical-kpis"><div><span>{labels[metric]}</span><strong data-testid="siap-value">{formatUtilization(selected?.value)}</strong><small>{metric==="frequentation"?"Consultas / persona asignada / año":metric==="consultations"?"Contactos":"Personas; no sumar lugares"}</small></div><div><span>Pediatras AP · {year}</span><strong>{formatUtilization(staff?.pediatricians)}</strong><small>Profesionales, no centros ni FTE</small></div><div><span>Población asignada / pediatra</span><strong>{formatUtilization(staff?.assigned_per_professional)}</strong><small>Ratio original SIAP; no residentes de la malla</small></div></div>
 <p>Teleconsulta sin dato no significa cero. El total es el publicado; no se suman lugares. Cambios de modalidad y pandemia limitan la comparación temporal.</p>
 <div className="phase6-trend" aria-label="Tendencia anual SIAP">{trend.map(r=><div key={r.year}><span>{r.year}</span><div className="phase6-track"><i style={{width:r.value==null?"0":`${r.value/max*100}%`}}/></div><span>{formatUtilization(r.value)}</span></div>)}</div>
 <SourceMethodPanel details={[{label:"Universo y denominador",text:"Servicio Pediatría AP. Frecuentación = consultas ordinarias / población asignada / año. No es porcentaje ni consultas por niño residente."},{label:"Periodo, frecuencia y versión",text:"2007–2024, anual; E54086A_000005/000007/000009 versión1.1. Usuarios distintos no se suman entre lugares."},{label:"Checksum del indicador",text:data.sources[metric as keyof typeof data.sources].checksum}]} sourceLinks={[{label:"CSV oficial del indicador",url:data.sources[metric as keyof typeof data.sources].source_url},{label:"Dotación SIAP; snapshot conservado",url:data.staff_source.url},{label:"Condiciones ISTAC",url:data.sources.consultations.license_url}]}/>
 </section>
 <section className="clinical-module" id="espera"><h2>Listas de espera</h2><p><b>Canarias · ADMINISTRATIVE_STOCK</b>. Personas pendientes en una fecha. No es demora, incidencia ni tiempo individual.</p>
 <div className="clinical-filters"><label>Lista<select aria-label="Lista pediátrica" value={waiting} onChange={e=>setWaiting(e.target.value)}><option value="outpatient:PEDIATRIA">Consultas externas · Pediatría</option><option value="outpatient:CIRUGIA_PEDIATRICA">Consultas externas · Cirugía Pediátrica</option><option value="surgical:CIRUGIA_PEDIATRICA">Quirúrgica · Cirugía Pediátrica</option></select></label><label>Fecha de corte<select aria-label="Corte de espera" value={cut} onChange={e=>setCut(e.target.value)}>{[...waits].reverse().map(r=><option key={r.date}>{r.date}</option>)}</select></label></div>
 <p className="phase6-value" data-testid="waiting-value">{formatUtilization(stock?.value)} <small>personas pendientes · {stock?.status??"MISSING"}</small></p>
 <p>Publicación insular en HOLD: pendiente de confirmar residencia frente a territorio de atención. Cero publicado no implica ausencia de necesidad. No sumar cortes ni listas.</p>
 <div className="table-scroll"><table><caption>Evolución del stock regional</caption><thead><tr><th>Fecha</th><th>Pendientes</th><th>Estado</th></tr></thead><tbody>{waits.map(r=><tr key={r.date}><td>{r.date}</td><td>{formatUtilization(r.value)}</td><td>{r.status}</td></tr>)}</tbody></table></div>
 <SourceMethodPanel details={[{label:"Definición y geografía",text:"Stock de especialidad pediátrica en centros SCS. Solo Canarias; especialidad no acredita edad0–17."},{label:"Método y privacidad",text:"Cortes semestrales2017–2025. Total de banda; sin demora calculada. Conteos1–4 y bandas relacionadas suprimidos si aparecen."}]} sourceLinks={[{label:"CSV consultas externas",url:data.sources.outpatient.source_url},{label:"CSV espera quirúrgica",url:data.sources.surgical.source_url}]}/>
 </section>
 <section className="clinical-module" id="research"><h2>Research · Cuadrado asistencial</h2><p>Oferta, acceso, utilización y presión pendiente se mantienen separados. Sin puntuación total ni causalidad.</p>
 <div className="phase6-square"><article><h3>Oferta · {year}</h3><p>{formatUtilization(staff?.pediatricians)} pediatras AP</p><p>{profile?.eligible_pediatric_facilities} destinos verificados · catálogo2026</p></article><article><h3>Acceso · población2024</h3><p>{formatUtilization(profile?.median_travel_minutes)} min de mediana potencial</p><p>Red congelada2026; no tiempo hasta atención. Comparación simultánea con SIAP no habilitada.</p></article><article><h3>Utilización · {year}</h3><p>{formatUtilization(ap)} consultas</p><p>{formatUtilization(ratio)} consultas/profesional · DERIVED_RATE, no productividad individual.</p></article><article><h3>Presión pendiente</h3><p>Solo stock regional. No atribuible a esta isla.</p></article></div>
 <label>Comparación compatible<select aria-label="Comparación Research V2" value={research} onChange={e=>setResearch(e.target.value)}><option value="consultations">Pediatras y consultas · misma isla/año</option><option value="distinct_persons">Pediatras y personas distintas · misma isla/año</option><option disabled>Accesibilidad: periodos y universo no alineados</option><option disabled>Espera: geografía insular en HOLD</option><option disabled>Renta2023: alineación de universo pendiente</option></select></label>
 <div className="table-scroll"><table><caption>Comparación descriptiva {year} · sin ranking</caption><thead><tr><th>Isla</th><th>Pediatras</th><th>{labels[research]}</th></tr></thead><tbody>{data.islands.map(i=><tr key={i.id}><th>{i.name}</th><td>{formatUtilization(data.staff.find(r=>r.island===i.id&&r.year===year)?.pediatricians)}</td><td>{formatUtilization(data.activity.find(r=>r.island===i.id&&r.year===year&&r.metric===research&&r.place==="_T")?.value)}</td></tr>)}</tbody></table></div>
 </section></>;
}
