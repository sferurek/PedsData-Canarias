import Link from "next/link";
import { notFound } from "next/navigation";
import { AccessibilityMap } from "@/components/AccessibilityMap";
import { DataBadge } from "@/components/DataBadge";
import { Metric } from "@/components/Metric";
import { SourceMethodPanel } from "@/components/SourceMethodPanel";
import { islandBySlug, profiles } from "@/lib/data";
import { formatNumber, formatPercent } from "@/lib/format";
import clinical from "@/data/clinical.json";

export function generateStaticParams() { return profiles.islands.map(({ slug }) => ({ slug })); }

export default async function IslandPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const island = islandBySlug(slug);
  if (!island) notFound();
  const municipalities = profiles.municipalities.filter((item) => item.island_id === island.island_id);
  const isLanzarote = island.island_id === "lanzarote";
  const clinicalSummary = clinical.island_summary[island.island_id as keyof typeof clinical.island_summary];
  return <>
    <section className="profile-hero"><Link className="back-link" href="/">← Canarias</Link>
      <div className="profile-title"><div><span className="eyebrow">Perfil insular · acceso potencial</span><h1>{island.name}</h1></div><DataBadge status={isLanzarote ? "PARTIAL" : "VALIDATED"} /></div>
      <p>{formatNumber(island.children_0_14)} niños de 0–14 años · {island.eligible_pediatric_facilities} destinos AP elegibles · {island.pediatricians_ap_2024} pediatras AP SIAP.</p>
    </section>
    <section className="profile-metrics">
      <Metric label="Mediana" value={island.median_travel_minutes} suffix=" min" detail="Ponderada por niños" />
      <Metric label="P90" value={island.p90_travel_minutes} suffix=" min" detail="Ponderado por niños" />
      <Metric label="Población a <15 min" value={island.pct_under_15_total} suffix=" %" detail="Denominador total" />
      <Metric label="Población a ≥30 min" value={island.pct_30_or_more_total} suffix=" %" detail="Denominador total" />
      <Metric label="No evaluable" value={island.population_not_evaluated} detail="Niños" />
      <Metric label="Transferencia" value={island.population_requires_interisland_transfer} detail="Tiempo desconocido" />
    </section>
    <section className="profile-context" aria-label="Contexto territorial">
      <Metric label="Renta por persona" value={island.income_mean_per_person_2023} suffix=" €" detail="Media municipal ponderada por niños · 2023" />
      <Metric label="Densidad infantil" value={island.child_density_per_km2} suffix=" /km²" detail="0–14 · 2024" />
      <Metric label="Niños en celdas rurales" value={island.rural_children_pct} suffix=" %" detail="DEGURBA 2021" />
      <Metric label="Estaciones de aire" value={island.air_station_count} detail="Inventario 2025" />
      <Metric label="Estaciones meteo" value={island.weather_station_count} detail="Observaciones pendientes" />
    </section>
    <section className="island-clinical" aria-label="Resultados clínicos disponibles"><div><span className="eyebrow">Resultados de salud · escala insular</span><h2>Perinatalidad y mortalidad segura</h2></div><div className="clinical-kpis"><div><span>Nacimientos 2024</span><strong>{formatNumber(clinicalSummary.births_2024)}</strong><small>Residencia materna</small></div><div><span>Prematuridad 2024</span><strong>{clinicalSummary.preterm_rate_2024?.toLocaleString("es-ES")} %</strong><small>{clinicalSummary.preterm_births_2024} nacimientos</small></div><div><span>Defunciones 0–14</span><strong>{clinicalSummary.pediatric_deaths_2020_2024 ?? "Suprimido"}</strong><small>2020–2024 · {clinicalSummary.mortality_status}</small></div></div><p>Hospitalización pediátrica disponible únicamente a nivel Canarias. Urgencias comparables no disponibles para el perfil insular.</p><Link className="primary-link" href="/resultados">Ver resultados y método</Link></section>
    {isLanzarote && <aside className="transfer-note"><strong>La Graciosa</strong><p>Transferencia interinsular requerida; tiempo terrestre no estimado. 91 niños permanecen fuera del denominador evaluable.</p></aside>}
    <section className="map-section compact-map"><div className="section-heading"><div><span className="eyebrow">Mapa insular</span><h2>Accesibilidad a Pediatría AP</h2></div><p>{formatPercent(island.pct_20_or_more_total)} de la población está a 20 minutos o más.</p></div>
      <AccessibilityMap municipalities={municipalities} initialIsland={island.island_id} /><SourceMethodPanel />
    </section>
    <section className="section"><div className="section-heading"><div><span className="eyebrow">Municipios</span><h2>Perfiles con regla de publicación</h2></div><p>Los perfiles restringidos siguen visibles con su motivo.</p></div>
      <div className="municipality-list">{municipalities.map((item) => <Link key={item.municipality_id} href={`/municipios/${item.municipality_id}`}><span>{item.municipality_name}</span><small>{item.publication_status === "publishable" ? "Ver perfil" : "Datos limitados"}</small></Link>)}</div>
    </section>
  </>;
}
