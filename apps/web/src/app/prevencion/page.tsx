import {SourceMethodPanel} from "@/components/SourceMethodPanel";
import data from "@/data/phase6b-screening.json";

export const metadata={title:"Prevención pediátrica"};

export default function Page(){
 const value=(id:string)=>data.find(row=>row.indicator_id===id)!;
 const participation=value("participation");
 const invalid=value("first_invalid_sample");
 const traceability=value("traceability");
 return <><section className="clinical-hero">
  <span className="eyebrow">Prevención · escala regional</span>
  <h1>Procesos preventivos<br/><em>con denominador.</em></h1>
  <p>Indicadores regionales publicados sin convertir proceso en prevalencia.</p>
 </section><div className="clinical-shell"><section className="clinical-module">
  <h2>Cribado metabólico neonatal · Canarias 2024</h2>
  <p><b>OBSERVED · REGIONAL</b>. Calidad y oportunidad del programa de prueba de talón.</p>
  <div className="clinical-kpis">
   <div><span>Participación</span><strong>{participation.value} %</strong></div>
   <div><span>Primeras muestras no válidas</span><strong>{invalid.value} %</strong></div>
   <div><span>Trazabilidad</span><strong>{traceability.value} %</strong></div>
  </div>
  <p>{participation.numerator}/{participation.denominator} recién nacidos. Son indicadores de proceso, no prevalencia de enfermedad.</p>
  <h2>Vacunación y cribado auditivo</h2>
  <p>HOLD · SIVAMIN no ofrece aún un export reproducible de Canarias. El informe auditivo 2024 no publica una fila de Canarias; ausencia no significa cero.</p>
  <SourceMethodPanel details={[
   {label:"Fuente",text:"SICN, evaluación 2024, tablas 2–3."},
   {label:"Geografía",text:"Canarias; no se reparte entre islas."},
   {label:"Método",text:"Participación 11.536/11.671; tiempos como percentiles publicados."}
  ]} sourceLinks={[
   {label:"Informe SICN 2024",url:participation.source_url},
   {label:"Condiciones de uso",url:participation.license_url}
  ]}/>
 </section></div></>;
}
