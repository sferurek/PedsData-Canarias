import Link from "next/link";
import { formatMinutes, formatNumber, formatPercent } from "@/lib/format";
import type { IslandProfile } from "@/lib/types";
import { SourceMethodPanel } from "./SourceMethodPanel";

export function AccessGapTable({ islands }: { islands: IslandProfile[] }) {
  return <section className="section" aria-labelledby="access-gap-title">
    <div className="section-heading">
      <div><span className="eyebrow">Pediatric Access Gap</span><h2 id="access-gap-title">Dimensiones de acceso, sin puntuación única</h2></div>
      <p>Comparación descriptiva. El orden territorial no implica una clasificación.</p>
    </div>
    <div className="table-scroll"><table>
      <thead><tr><th>Isla</th><th>Niños 0–14</th><th>Centros</th><th>Niños / centro</th><th>Mediana</th><th>P90</th><th>≥20 min</th></tr></thead>
      <tbody>{islands.map((island) => <tr key={island.island_id}>
        <th><Link href={`/islas/${island.slug}`}>{island.name}</Link></th>
        <td>{formatNumber(island.children_0_14)}</td>
        <td>{formatNumber(island.eligible_pediatric_facilities)}</td>
        <td>{formatNumber(island.children_per_verified_pediatric_facility, 1)}</td>
        <td>{formatMinutes(island.median_travel_minutes)}</td>
        <td>{formatMinutes(island.p90_travel_minutes)}</td>
        <td>{formatPercent(island.pct_20_or_more_total)}</td>
      </tr>)}</tbody>
    </table></div>
    <SourceMethodPanel compact />
  </section>;
}
