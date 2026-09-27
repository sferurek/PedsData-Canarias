import { formatNumber } from "@/lib/format";

export function Metric({ label, value, suffix, detail }: {
  label: string;
  value: number | null | undefined;
  suffix?: string;
  detail?: string;
}) {
  const rendered = value === null || value === undefined ? "No disponible" : `${formatNumber(value, 1)}${suffix ?? ""}`;
  return <div className="metric">
    <span className="metric-label">{label}</span>
    <strong className="metric-value">{rendered}</strong>
    {detail && <span className="metric-detail">{detail}</span>}
  </div>;
}
