import data from "@/data/phase6b-bdcap.json";
import {SourceMethodPanel} from "./SourceMethodPanel";

export function BDCAPExplorer(){
 const latest=data.at(-1)!;
 return <section className="clinical-module" id="bdcap">
  <h2>Morbilidad registrada en Atención Primaria</h2>
  <p><b>WEIGHTED_SAMPLE · REGIONAL</b>. BDCAP, población asignada de 0–14 años en Canarias.</p>
  <div className="clinical-kpis">
   <div><span>Obesidad registrada · 2024</span><strong>{Number(latest.value).toLocaleString("es-ES")} ‰</strong></div>
   <div><span>Casos ponderados</span><strong>{Number(latest.weighted_cases).toLocaleString("es-ES")}</strong></div>
  </div>
  <p>Problema activo CIAP-2 T82; no equivale a prevalencia antropométrica. El export no publica el denominador numérico.</p>
  <SourceMethodPanel details={[
   {label:"Fuente y universo",text:"BDCAP 2024 · muestra de historias clínicas de AP · Canarias · 00-14 años."},
   {label:"Ponderación",text:latest.weighting},
   {label:"Escala",text:"Solo Canarias; no se reparte entre islas."}
  ]} sourceLinks={[
   {label:"Portal BDCAP",url:latest.source_url},
   {label:"Condiciones de uso",url:latest.license_url}
  ]}/>
 </section>;
}
