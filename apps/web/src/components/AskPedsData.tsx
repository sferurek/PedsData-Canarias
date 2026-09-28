"use client";
import {FormEvent,useState} from "react";
import {askPedsData,type QueryResult,type ChartType} from "@/lib/semantic";
import {sourceById} from "@/lib/provenance";
import {profiles} from "@/lib/data";
import {SemanticChart} from "./SemanticChart";
import {AccessibilityMap} from "./AccessibilityMap";
import {ResultSourcesLink} from "./ResultSourcesLink";
import type {ContextLayer} from "./MapLegend";

const examples=["Evolución de pediatras en Lanzarote","Compara consultas entre Tenerife y Gran Canaria","Mapa de renta en Canarias","Mapa de accesibilidad pediátrica de Fuerteventura","Cómo ha cambiado la frecuentación pediátrica en El Hierro"];
const mapLayers:Record<string,ContextLayer>={income_mean_per_person:"income",accessibility_ap:"accessibility",child_density:"density",degurba:"degurba",pediatricians_ap:"pediatricians_ap",pediatric_frequentation:"pediatric_frequentation",preterm_rate:"preterm_rate",PM10:"PM10","PM2.5":"PM2.5",NO2:"NO2"};

export function AskPedsData(){
 const [question,setQuestion]=useState(examples[0]),[result,setResult]=useState<QueryResult|null>(null),[pending,setPending]=useState(false);
 const submit=(event?:FormEvent)=>{event?.preventDefault();setPending(true);queueMicrotask(()=>{setResult(askPedsData(question));setPending(false)})};
 const handleExample=(value:string)=>{setQuestion(value);setPending(true);queueMicrotask(()=>{setResult(askPedsData(value));setPending(false)})};
 return <div className="ask-shell"><form onSubmit={submit}><label htmlFor="ask-input">Pregunta a PedsData</label><div><input id="ask-input" value={question} onChange={event=>setQuestion(event.target.value)} placeholder="Evolución, comparación o mapa…" autoComplete="off"/><button disabled={pending||!question.trim()}>{pending?"Validando…":"Consultar"}</button></div><p>Consulta controlada: interpreta intención, valida catálogo y calcula con datos registrados. No ejecuta SQL ni genera cifras.</p></form><div className="ask-examples" aria-label="Preguntas de ejemplo">{examples.map(example=><button key={example} onClick={()=>handleExample(example)}>{example}</button>)}</div>
 {result&&!result.ok&&<section className="ask-error" role="alert"><b>{result.error}</b><p>{result.message}</p><span>Prueba una sugerencia registrada o cambia indicador, territorio o periodo.</span></section>}
 {result?.ok&&<section className="ask-result" aria-live="polite"><div className="semantic-result-head"><div><span className="eyebrow">{result.plan.intent}</span><h2>{result.metrics.map(metric=>metric.label).join(" × ")}</h2><p>{result.summary}</p></div><code>{result.plan.visual}</code></div>
  {result.plan.visual==="map"?<AccessibilityMap key={result.metrics[0].metric_id+String(result.plan.end_year)} municipalities={profiles.municipalities} initialIsland={result.plan.geographies.length===1&&result.plan.geographies[0]!=="canarias"?result.plan.geographies[0]:"all"} initialLayer={mapLayers[result.metrics[0].metric_id]}/>:<SemanticChart points={result.points} metrics={result.metrics} type={result.plan.visual as ChartType}/>}
  <div className="ask-provenance"><strong>Fuentes registradas</strong>{result.source_ids.map(id=>{const source=sourceById(id);return <span key={id}>{source?.organization??id} · {source?.version_used??"versión registrada"}</span>})}</div>
  <ResultSourcesLink metricId={result.metrics[0].metric_id} period={result.plan.start_year&&result.plan.end_year?result.plan.start_year+"–"+result.plan.end_year:result.plan.end_year} geography={result.plan.geographies.join(",")} result={result.summary}/>
 </section>}</div>;
}
