import Link from "next/link";
import { notFound } from "next/navigation";
import { DataBadge } from "@/components/DataBadge";
import { Metric } from "@/components/Metric";
import { SourceMethodPanel } from "@/components/SourceMethodPanel";
import { islandName, municipalityById, profiles } from "@/lib/data";

export function generateStaticParams() { return profiles.municipalities.map(({ municipality_id }) => ({ id: municipality_id })); }

export default async function MunicipalityPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const municipality = municipalityById(id);
  if (!municipality) notFound();
  const island = profiles.islands.find((item) => item.island_id === municipality.island_id)!;
  const publishable = municipality.publication_status === "publishable";
  return <>
    <section className="profile-hero"><Link className="back-link" href={`/islas/${island.slug}`}>← {islandName(municipality.island_id)}</Link>
      <div className="profile-title"><div><span className="eyebrow">Perfil municipal</span><h1>{municipality.municipality_name}</h1></div><DataBadge status={publishable ? "VALIDATED" : "PARTIAL"} /></div>
      <p>Acceso geográfico potencial a Pediatría AP · población 0–14 · 2024.</p>
    </section>
    {publishable ? <>
      <section className="profile-metrics">
        <Metric label="Población infantil" value={municipality.children_0_14} detail="0–14" />
        <Metric label="Destinos en municipio" value={municipality.eligible_pediatric_facilities} detail="No equivale a pediatras" />
        <Metric label="Mediana" value={municipality.median_travel_minutes} suffix=" min" />
        <Metric label="P90" value={municipality.p90_travel_minutes} suffix=" min" />
        <Metric label="Población a <15 min" value={municipality.pct_under_15_total} suffix=" %" />
        <Metric label="Población a ≥30 min" value={municipality.pct_30_or_more_total} suffix=" %" />
      </section>
      <section className="section narrow"><h2>Lectura del indicador</h2><p>El destino más próximo se calcula por celda y puede estar fuera del municipio. El conteo de centros corresponde a infraestructura situada dentro del límite municipal; no infiere plantilla profesional municipal.</p><SourceMethodPanel /></section>
    </> : <section className="restricted"><DataBadge status="PARTIAL" /><h2>Perfil no publicable en RC1</h2><p>La población infantil municipal es inferior al umbral conservador de 100. Los datos permanecen en el agregado trazable, pero esta pantalla no muestra indicadores detallados.</p><Link className="primary-link" href={`/islas/${island.slug}`}>Ver perfil de {island.name}</Link></section>}
  </>;
}
