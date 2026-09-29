import type {Metadata} from "next";
import Link from "next/link";
import {notFound} from "next/navigation";
import {LazyAccessibilityMap} from "@/components/LazyAccessibilityMap";
import {PrintReportButton} from "@/components/PrintReportButton";
import {ResultSourcesLink} from "@/components/ResultSourcesLink";
import {SemanticChart} from "@/components/SemanticChart";
import {profiles} from "@/lib/data";
import {sourceById} from "@/lib/provenance";
import {metricById} from "@/lib/semantic";
import {buildTerritorialReport,territorialReportIds,type ExecutiveFinding,type ReportSection} from "@/lib/territorial-report";

const nf=new Intl.NumberFormat("es-ES",{maximumFractionDigits:2});
export const dynamicParams=false;
export function generateStaticParams(){return territorialReportIds().map(geography_id=>({geography_id}))}
export async function generateMetadata({params}:{params:Promise<{geography_id:string}>}):Promise<Metadata>{const {geography_id}=await params;const report=buildTerritorialReport(geography_id);return report?{title:`Informe pediátrico de ${report.territory.name}`,description:`Perfil territorial pediátrico trazable de ${report.territory.name}.`}:{}}
function valueText(value:number|string|null,unit:string){if(value===null)return "No disponible";return (typeof value==="number"?nf.format(value):value)+(unit==="estado"?"":unit.startsWith("%")?" %":" "+unit)}
function TraceLinks({section}:{section:ReportSection}){return <div className="report-trace-links">{section.metricIds.map(metricId=><ResultSourcesLink key={metricId} metricId={metricId} result={section.title} period={metricById(metricId)?.time_start+"–"+metricById(metricId)?.time_end} geography={section.facts[0]?.geography_id??section.series[0]?.geography_id}/>)}</div>}
function FindingTrace({finding,geography}:{finding:ExecutiveFinding;geography:string}){return <div className="finding-trace">{finding.metricIds.map(metricId=><ResultSourcesLink key={metricId} metricId={metricId} result="Hallazgo del informe territorial" period={finding.period} geography={geography}/>)}</div>}
function FindingList({findings,geography}:{findings:ExecutiveFinding[];geography:string}){return <ol>{findings.map(item=><li key={item.id}><p>{item.text}</p><FindingTrace finding={item} geography={geography}/></li>)}</ol>}
function Section({section,geographyId}:{section:ReportSection;geographyId:string}){
 return <section className="territorial-domain" id={section.id}><div className="report-section-heading"><div><span className="eyebrow">Dominio</span><h2>{section.title}</h2></div>{section.note&&<p>{section.note}</p>}</div>
  {section.facts.length>0&&<div className="report-facts"><table><thead><tr><th>Indicador</th><th>Resultado</th><th>Periodo</th><th>Geografía</th><th>Estado</th></tr></thead><tbody>{section.facts.map((item,index)=><tr key={item.metric_id+item.label+index}><td><Link href={`/indicadores/${item.metric_id}`}>{item.label}</Link></td><td>{valueText(item.value,item.unit)}</td><td>{item.period}</td><td>{item.geography_level}</td><td>{item.status}</td></tr>)}</tbody></table></div>}
  {section.visual==="map"&&geographyId!=="la-graciosa"&&<div className="report-visual"><LazyAccessibilityMap municipalities={profiles.municipalities.filter(item=>geographyId.length===5?item.municipality_id===geographyId:item.island_id===geographyId)} initialIsland={geographyId.length===5?(profiles.municipalities.find(item=>item.municipality_id===geographyId)?.island_id??"all"):geographyId}/><ResultSourcesLink metricId="accessibility_ap" result={section.title} period="2024" geography={geographyId}/></div>}
  {section.visual==="map"&&geographyId==="la-graciosa"&&<aside className="transfer-note"><strong>Transferencia interinsular requerida</strong><p>No se genera un mapa de tiempo terrestre ni se asigna ferry, avión o ambulancia.</p></aside>}
  {section.series.length>0&&section.metricIds.map(metricId=>{const points=section.series.filter(point=>point.metric_id===metricId),metric=metricById(metricId);if(!points.length||!metric)return null;return <div className="report-visual" key={metricId}><h3>{metric.label}</h3><SemanticChart points={points} metrics={[metric]} type="line"/><ResultSourcesLink metricId={metricId} result={`${metric.label} · ${section.title}`} period={`${metric.time_start}–${metric.time_end}`} geography={section.series[0].geography_id}/></div>})}
  <TraceLinks section={section}/>
 </section>;
}
export default async function TerritorialReportPage({params}:{params:Promise<{geography_id:string}>}){
 const {geography_id}=await params;const report=buildTerritorialReport(geography_id);if(!report)notFound();
 const sources=report.sourceIds.map(sourceById).filter(Boolean);
 return <><article className="territorial-report"><header className="report-hero"><div><Link className="back-link" href={report.territory.kind==="island"?`/islas/${report.territory.id}`:report.territory.kind==="municipality"?`/municipios/${report.territory.id}`:"/pregunta"}>← Volver al perfil</Link><span className="eyebrow">Informe territorial pediátrico</span><h1>{report.territory.name}</h1><p>Informe determinista construido exclusivamente con métricas y fuentes registradas. Geografía solicitada: <b>{report.territory.geographyLevel}</b>.</p></div><PrintReportButton/></header>
  <section className="executive-findings"><span className="eyebrow">Resumen ejecutivo</span><h2>Hallazgos calculados</h2>{report.findings.length?<FindingList findings={report.findings} geography={report.territory.id}/>:<p>No hay métricas publicables directamente atribuibles a esta geografía. El contexto regional se mantiene separado.</p>}<p className="scientific-caveat">Lectura descriptiva: no estima riesgo individual ni causalidad.</p></section>
  <nav className="report-toc" aria-label="Secciones del informe">{report.sections.map(section=><a key={section.id} href={`#${section.id}`}>{section.title}</a>)}{report.regionalContext.length>0&&<a href="#regional-context">Contexto regional</a>}</nav>
  {report.sections.map(section=><Section key={section.id} section={section} geographyId={geography_id}/>)}
  {report.regionalContext.length>0&&<section className="regional-context" id="regional-context"><span className="eyebrow">Contexto regional — no atribuible al territorio analizado</span><h2>Canarias</h2><p>Estas métricas solo están registradas a escala autonómica. Se muestran como contexto y no describen {report.territory.name}.</p>{report.regionalContext.map(section=><Section key={section.id} section={section} geographyId="canarias"/>)}</section>}
  {report.unavailableDomains.length>0&&<section className="report-unavailable"><h2>Dominios sin dato atribuible</h2><p>{report.unavailableDomains.join(" · ")}</p><p>La ausencia en este informe no equivale a ausencia clínica; indica que el catálogo no contiene una métrica válida para esta resolución.</p></section>}
  <section className="report-knowledge"><span className="eyebrow">Lectura responsable</span><h2>Qué sabemos / qué no podemos concluir</h2><div className="knowledge-grid"><div><h3>Qué sabemos</h3>{report.interpretation.known.length?<FindingList findings={report.interpretation.known} geography={report.territory.id}/>:<p>No hay conclusiones territoriales publicables con la resolución solicitada.</p>}</div><div><h3>Qué no podemos concluir</h3><ul>{report.interpretation.cannotConclude.map(item=><li key={item}>{item}</li>)}</ul><h3>Datos faltantes relevantes</h3><ul>{report.interpretation.missingData.map(item=><li key={item}>{item}</li>)}</ul></div></div></section>
  <section className="report-limitations"><h2>Limitaciones</h2><ul>{report.limitations.map(item=><li key={item}>{item}</li>)}</ul></section>
  <section className="report-sources"><span className="eyebrow">Fuentes utilizadas en este informe</span><h2>{sources.length} fuentes realmente usadas</h2><div className="source-catalog">{sources.map(source=><article key={source!.source_id}><h3><Link href={`/fuentes/${encodeURIComponent(source!.source_id)}`}>{source!.name}</Link></h3><p>{source!.organization} · {source!.available_period}</p><p>{source!.geographic_disaggregation} · versión {source!.version_used}</p><a href={source!.official_url} target="_blank" rel="noreferrer">Fuente oficial directa ↗</a></article>)}</div></section>
 </article></>;
}
