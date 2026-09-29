import type {Metadata} from "next";
import Link from "next/link";
import {AccessGapTable} from "@/components/AccessGapTable";
import {AskPedsData} from "@/components/AskPedsData";
import {LazyAccessibilityMap} from "@/components/LazyAccessibilityMap";
import {DataBadge} from "@/components/DataBadge";
import {IslandCards} from "@/components/IslandCards";
import {Metric} from "@/components/Metric";
import {ResultSourcesLink} from "@/components/ResultSourcesLink";
import {SourceMethodPanel} from "@/components/SourceMethodPanel";
import {profiles} from "@/lib/data";

export const metadata:Metadata={alternates:{canonical:"/"}};

export default function Home(){
 const {summary,islands,municipalities,metadata}=profiles;
 const airStations=islands.reduce((n,i)=>n+i.air_station_count,0);
 return <>
  <section className="home-hero" id="mapa" aria-labelledby="home-title">
   <div className="hero-atmosphere" aria-hidden="true"/>
   <div className="home-hero-grid">
    <div className="home-hero-copy">
     <div className="hero-badges"><DataBadge status="VALIDATED"/><span>7 islas · beta pública</span></div>
     <span className="hero-kicker">Datos para una infancia más saludable</span>
     <h1 id="home-title">Entender la salud<br/><em>infantil de las islas.</em></h1>
     <p>Mapas, series temporales e informes territoriales construidos con datos públicos trazables para comprender mejor la salud infantil en Canarias.</p>
     <div className="hero-actions"><a className="button-primary" href="#mapa-interactivo">Explorar los datos <span aria-hidden="true">→</span></a><Link className="button-secondary" href="/informes/canarias">Ver informe de Canarias</Link></div>
     <ul className="hero-principles" aria-label="Principios del observatorio"><li><b>Datos públicos</b><span>y trazables</span></li><li><b>Rigor científico</b><span>y sanitario</span></li><li><b>Siete islas</b><span>siempre visibles</span></li></ul>
    </div>
    <div className="hero-map-frame" id="mapa-interactivo">
     <div className="hero-map-heading"><strong>Mapa pediátrico de Canarias · Tiempo de acceso por carretera a la atención pediátrica</strong></div>
     <LazyAccessibilityMap municipalities={municipalities}/>
    </div>
   </div>
   <nav className="home-quick-links" aria-label="Accesos principales"><a href="#mapa-interactivo">Explorar mapa</a><Link href="/evolucion">Ver evolución</Link><Link href="/comparar">Comparar islas</Link><Link href="/pregunta">Preguntar a PedsData</Link><Link href="/fuentes">Ver fuentes</Link></nav>
  </section>

  <section className="summary-strip home-stat-band" aria-label="Indicadores de Canarias">
   <Metric metricId="child_population_grid_0_14" label="Población infantil" value={summary.children_0_14} detail="0–14 · ISTAC 2024"/>
   <Metric metricId="verified_pediatric_facilities" label="Destinos pediátricos AP" value={summary.eligible_pediatric_facilities} detail="Centros verificados"/>
   <Metric metricId="accessibility_ap" label="Mediana de acceso" value={summary.median_travel_minutes} suffix=" min" detail="Ponderada por niños"/>
   <Metric metricId="income_mean_per_person" label="Municipios con renta" value={88} detail="INE ADRH 2023"/>
   <Metric metricId="PM10" label="Estaciones de aire" value={airStations} detail="51 inventariadas · 49 en mapa"/>
  </section>

  <section className="home-light-section">
   <div className="section" id="islas" aria-labelledby="islands-title">
    <div className="section-heading"><div><span className="eyebrow">Territorio, contexto, realidad</span><h2 id="islands-title">Informes territoriales</h2></div><div><p>La situación pediátrica de cada isla, con indicadores, tendencias y límites explícitos.</p><Link className="button-outline" href="/informes/canarias">Ver informe del archipiélago →</Link></div></div>
    <IslandCards islands={islands}/>
   </div>
  </section>

  <section className="home-observatory-section">
   <div className="section-heading home-dark-heading"><div><span className="eyebrow">Indicadores que cuentan historias</span><h2>Una visión amplia del bienestar pediátrico</h2></div><p>Explora la evolución, compara territorios y revisa resultados sin perder la escala real de cada fuente.</p></div>
   <div className="observatory-cards">
    <Link href="/evolucion"><span>01 · Series</span><h3>Evolución temporal</h3><p>Veinte años de población, dotación, utilización y resultados disponibles.</p><b>Explorar series →</b></Link>
    <Link href="/comparar"><span>02 · Territorios</span><h3>Comparar islas</h3><p>Dos a siete islas con la misma definición, periodo y unidad.</p><b>Abrir comparador →</b></Link>
    <Link href="/resultados"><span>03 · Salud</span><h3>Resultados pediátricos</h3><p>Hospitalización, perinatalidad, mortalidad y encuesta con comparabilidad explícita.</p><b>Ver resultados →</b></Link>
   </div>
   <div className="section context-board" id="entorno" aria-labelledby="context-title"><div className="section-heading"><div><span className="eyebrow">Contexto territorial infantil</span><h2 id="context-title">Medido, derivado y pendiente</h2></div><p>Cada dominio conserva fecha, geografía y estado de validación.</p></div><div className="context-grid"><article><DataBadge status="COMPLETE"/><h3>Renta municipal</h3><strong>88 municipios</strong><p>Renta general del territorio; no se presenta como pobreza infantil.</p><ResultSourcesLink metricId="income_mean_per_person" period={2023} geography="municipality" result="Cobertura municipal de renta"/></article><article><DataBadge status="ESTIMATED"/><h3>Densidad y DEGURBA</h3><strong>255.814 niños</strong><p>Malla infantil 2024 sobre clasificación oficial 2021, sin score de ruralidad.</p><ResultSourcesLink metricId="child_density" period={2024} geography="municipality" result="Contexto territorial infantil"/></article><article><DataBadge status="PARTIAL"/><h3>Calidad del aire</h3><strong>{airStations} estaciones</strong><p>Valores de estación 2025; dos ubicaciones no entran en el mapa.</p><ResultSourcesLink metricId="PM10" period={2025} geography="station" result="Estaciones de calidad del aire"/></article><article><DataBadge status="NOT AVAILABLE"/><h3>Meteorología y calima</h3><strong>Observaciones pendientes</strong><p>El inventario no se publica como indicador hasta disponer de observaciones trazables.</p></article></div></div>
   <AccessGapTable islands={islands}/>
  </section>

  <section className="home-ask-section">
   <div className="home-ask-intro"><span className="eyebrow">Tu pregunta, nuestros datos</span><h2>Pregunta a PedsData</h2><p>Escribe una pregunta en lenguaje natural. El catálogo determina qué puede responderse y cada cifra conserva su fuente.</p></div>
   <div className="home-ask-app"><AskPedsData/></div>
  </section>

  <section className="home-transparency">
   <div><span className="eyebrow">Transparencia que genera confianza</span><h2>Datos abiertos.<br/><em>Impacto real.</em></h2><p>Fuentes oficiales, metodología documentada y trazabilidad completa. Cada número puede seguirse hasta su origen.</p><div className="hero-actions"><Link className="button-primary" href="/fuentes">Conocer las fuentes →</Link><Link className="button-secondary" href="/explorar">Explorar datos</Link></div></div>
   <div className="transparency-grid"><article><span>01</span><h3>Fuentes oficiales</h3><p>Dataset, versión, periodo y enlace directo.</p></article><article><span>02</span><h3>Método reproducible</h3><p>Fórmulas, transformaciones y límites visibles.</p></article><article><span>03</span><h3>Geografía real</h3><p>Sin atribuir datos regionales a una isla o municipio.</p></article><article><span>04</span><h3>Trazabilidad</h3><p>Every number must be traceable.</p></article></div>
  </section>

  <section className="section split-section" id="metodologia"><div><span className="eyebrow">Dotación · SIAP 2024</span><h2>{summary.pediatricians_ap_2024} pediatras AP</h2><p>Profesionales y edificios se mantienen separados. Las capas de contexto no modifican el cálculo de accesibilidad.</p><ResultSourcesLink metricId="pediatricians_ap" period={2024} geography="island" result="Dotación de Pediatría AP"/></div><div className="method-callout"><DataBadge status="PENDING OFFICIAL GEOMETRY"/><h3>Perfiles ZBS no publicados</h3><p>No se publican perfiles por Zona Básica de Salud mientras no exista una geometría oficial vigente y reutilizable para las siete islas.</p></div></section>
  <SourceMethodPanel/>
  <section className="scientific-disclaimer" aria-label="Limitación científica"><strong>Lectura científica</strong><p>Los análisis territoriales describen asociaciones ecológicas y accesibilidad potencial. No estiman riesgo individual ni causalidad salvo que se indique expresamente.</p></section>
  <div className="data-ribbon"><span>{metadata.source_period} · población</span><span>{metadata.income_period} · renta</span><span>{metadata.air_period} · aire validado</span><span>Beta pública · trazabilidad activa</span></div>
 </>;
}
