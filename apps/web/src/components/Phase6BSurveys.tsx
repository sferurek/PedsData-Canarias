import data from "@/data/phase6b-surveys.json";
import {SourceMethodPanel} from "./SourceMethodPanel";

export function Phase6BSurveys(){
 const esde=data.find(row=>
  row.survey_id==="esde_2023"&&row.sex==="total"&&
  row.time_context==="weekday"&&row.category==="one_hour_or_more"
 )!;
 const estudes=data.find(row=>
  row.survey_id==="estudes_2023"&&row.indicator_id==="alcohol_last_30_days"
 )!;
 return <section className="clinical-module"><h2>Encuestas 2023 · universos separados</h2>
  <p><b>SURVEY_ESTIMATE · REGIONAL</b>. No forman una serie con HBSC.</p>
  <div className="clinical-kpis">
   <div><span>ESdE · pantalla ≥1 h laborables · 1–14</span><strong>{esde.value} %</strong></div>
   <div><span>ESTUDES · alcohol 30 días · 14–18</span><strong>{estudes.value} %</strong></div>
  </div>
  <p>ESdE representa población infantil en viviendas familiares mediante informante adulto. ESTUDES representa estudiantes escolarizados y presentes; N Canarias 2.488.</p>
  <SourceMethodPanel details={[
   {label:"ESdE",text:esde.age_group_original+" · "+esde.weighting},
   {label:"ESTUDES",text:estudes.age_group_original+" · "+estudes.weighting},
   {label:"Escala",text:"Solo Canarias; sin estimaciones insulares."}
  ]} sourceLinks={[
   {label:"CSV ESdE",url:esde.source_url},
   {label:"Informe ESTUDES",url:estudes.source_url}
  ]}/>
 </section>;
}
