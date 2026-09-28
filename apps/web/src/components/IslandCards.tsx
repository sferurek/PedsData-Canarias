import Link from "next/link";
import { formatMinutes, formatNumber, formatPercent } from "@/lib/format";
import type { IslandProfile } from "@/lib/types";
import { DataBadge } from "./DataBadge";
import { ResultSourcesLink } from "./ResultSourcesLink";

export function IslandCards({ islands }: { islands: IslandProfile[] }) {
  return <div className="island-grid">{islands.map((island) => <article className="island-card" key={island.island_id}>
    <div className="island-card-top"><span className="island-index">{String(islands.indexOf(island) + 1).padStart(2, "0")}</span><DataBadge status={island.island_id === "lanzarote" ? "PARTIAL" : "VALIDATED"} /></div>
    <h3>{island.name}</h3>
    <div className="island-stat"><strong>{formatNumber(island.children_0_14)}</strong><span>niños 0–14</span></div>
    <dl><div><dt>Mediana</dt><dd>{formatMinutes(island.median_travel_minutes)}</dd></div><div><dt>&lt;15 min</dt><dd>{formatPercent(island.pct_under_15_total)}</dd></div></dl>
    <ResultSourcesLink metricId="accessibility_ap" period={2024} geography={island.island_id} result={`Perfil resumido · `} />
    <Link className="text-link" href={`/islas/${island.slug}`}>Abrir perfil <span aria-hidden="true">→</span></Link>
  </article>)}</div>;
}
