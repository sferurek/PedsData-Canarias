"use client";
import {useState} from "react";
import data from "@/data/adolescence.json";
import {SourceMethodPanel} from "./SourceMethodPanel";
export function AdolescenceExplorer(){
 const [indicator,setIndicator]=useState("breakfast_weekdays");
 const choices=Array.from(new Map(data.map(r=>[r.indicator_id,r.indicator_label])).entries());
 const selected=data.filter(r=>r.indicator_id===indicator);
 const first=selected[0];
 return <section className="clinical-module"><h2>HBSC · Canarias 2022</h2><p><b>SURVEY_ESTIMATE · REGIONAL</b>. Adolescentes escolarizados de 11–18 años. No se reparte entre islas.</p>
 <label>Indicador adolescente<select aria-label="Indicador HBSC" value={indicator} onChange={e=>setIndicator(e.target.value)}>{choices.map(([id,label])=><option key={id} value={id}>{label}</option>)}</select></label>
 <div className="table-scroll"><table><caption>{first.indicator_label} · porcentaje publicado</caption><thead><tr><th>Edad original</th><th>Estimación</th><th>N válido publicado</th><th>IC</th></tr></thead><tbody>{selected.map(r=><tr key={r.age_group_original}><td>{r.age_group_original}</td><td>{r.value?.toLocaleString("es-ES")??"No disponible"} %</td><td>{r.n_valid_published}</td><td>No publicado</td></tr>)}</tbody></table></div>
 <p>En 17–18 años solo representa a quienes siguen escolarizados. N válido varía por pregunta y puede estar redondeado por pesos; no es un denominador poblacional. No se calculan IC ignorando el muestreo por conglomerados.</p>
 <p>Autoinforme, no diagnóstico clínico. Participación condicionada por COVID. ESdE y ESTUDES permanecen en HOLD y no se mezclan con esta encuesta.</p>
 <SourceMethodPanel details={[{label:"Fuente y edición",text:"Moreno y cols., Ministerio de Sanidad. HBSC2022 Canarias; cita2025, NIPO133-26-004-4. Última actualización no publicada."},{label:"Universo, ponderación y comparación",text:first.universe+". "+first.weighting+". Una sola edición; sin tendencia entre encuestas."},{label:"Definición",text:first.indicator_label+"; tabla en página PDF "+first.source_page+"."},{label:"Versión/checksum",text:first.dataset_version+" · "+first.checksum}]} sourceLinks={[{label:"Informe oficial HBSC",url:first.source_url+"#page="+first.source_page},{label:"Condiciones de reutilización",url:first.license_url}]}/>
 </section>;
}
