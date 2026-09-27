export const legendItems = [
  ["under_5", "<5 min"], ["5_to_under_10", "5–<10"],
  ["10_to_under_15", "10–<15"], ["15_to_under_20", "15–<20"],
  ["20_to_under_30", "20–<30"], ["30_or_more", "≥30"],
  ["requires_interisland_transfer", "Transferencia interinsular"],
  ["not_evaluated", "No evaluable"],
] as const;

export function MapLegend() {
  return <div className="legend" aria-label="Leyenda de tiempo estimado">
    {legendItems.map(([key, label]) => <span key={key}><i className={`swatch swatch-${key}`} />{label}</span>)}
  </div>;
}
