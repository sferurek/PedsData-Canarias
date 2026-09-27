import { AccessGapTable } from "@/components/AccessGapTable";
import { AccessibilityMap } from "@/components/AccessibilityMap";
import { DataBadge } from "@/components/DataBadge";
import { IslandCards } from "@/components/IslandCards";
import { Metric } from "@/components/Metric";
import { SourceMethodPanel } from "@/components/SourceMethodPanel";
import { profiles } from "@/lib/data";

export default function Home() {
  const { summary, islands, municipalities, metadata } = profiles;
  return <>
    <section className="hero">
      <div className="hero-copy"><div className="hero-badges"><DataBadge status="VALIDATED" /><span>7 islas · 2024</span></div>
        <h1>Accesibilidad pediátrica<br /><em>basada en datos públicos.</em></h1>
        <p>Tiempo estimado por carretera desde la población infantil al recurso de Pediatría de Atención Primaria verificado más próximo.</p>
        <a className="primary-link" href="#mapa">Explorar el mapa <span aria-hidden="true">↓</span></a>
      </div>
      <div className="hero-note"><span className="note-number">01</span><div><strong>Acceso geográfico potencial</strong><p>No representa tiempo hasta recibir atención sanitaria.</p></div></div>
    </section>

    <section className="summary-strip" aria-label="Indicadores de Canarias">
      <Metric label="Población infantil" value={summary.children_0_14} detail="0–14 · ISTAC 2024" />
      <Metric label="Destinos pediátricos AP" value={summary.eligible_pediatric_facilities} detail="Centros verificados" />
      <Metric label="Mediana de acceso" value={summary.median_travel_minutes} suffix=" min" detail="Ponderada por niños" />
      <Metric label="Población a <15 min" value={summary.pct_under_15_total} suffix=" %" detail="Sobre población total" />
      <Metric label="Población a ≥30 min" value={summary.pct_30_or_more_total} suffix=" %" detail="Sobre población total" />
    </section>

    <section className="map-section" id="mapa" aria-labelledby="map-title">
      <div className="section-heading"><div><span className="eyebrow">Mapa principal</span><h2 id="map-title">La distancia asistencial cambia con el territorio</h2></div>
        <p>Bandas discretas para evitar falsa precisión. Los puntos oscuros son destinos AP verificados.</p></div>
      <AccessibilityMap municipalities={municipalities} />
      <SourceMethodPanel />
    </section>

    <section className="section" id="islas" aria-labelledby="islands-title">
      <div className="section-heading"><div><span className="eyebrow">Siete perfiles</span><h2 id="islands-title">Un archipiélago, siete contextos</h2></div><p>Ninguna isla desaparece por disponibilidad desigual.</p></div>
      <IslandCards islands={islands} />
    </section>

    <AccessGapTable islands={islands} />

    <section className="section split-section" id="metodologia">
      <div><span className="eyebrow">Dotación · SIAP 2024</span><h2>{summary.pediatricians_ap_2024} pediatras AP</h2><p>La dotación profesional se muestra separada de los {summary.eligible_pediatric_facilities} centros. Profesionales y edificios no son conceptos intercambiables.</p></div>
      <div className="method-callout"><DataBadge status="PENDING OFFICIAL GEOMETRY" /><h3>Perfiles ZBS no publicados</h3><p>Los perfiles por Zona Básica de Salud no se publican actualmente porque no existe una geometría oficial vigente reutilizable validada para las siete islas.</p></div>
    </section>

    <div className="data-ribbon"><span>{metadata.source_period} · población</span><span>2026 · catálogo</span><span>{metadata.osm_snapshot} · red</span><span>{metadata.status} · revisión</span></div>
  </>;
}
