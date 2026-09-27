export function formatNumber(value: number | null | undefined, maximumFractionDigits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "No disponible";
  return new Intl.NumberFormat("es-ES", { maximumFractionDigits }).format(value);
}

export function formatPercent(value: number | null | undefined) {
  return value === null || value === undefined ? "No disponible" : `${formatNumber(value, 1)} %`;
}

export function formatMinutes(value: number | null | undefined) {
  return value === null || value === undefined ? "No disponible" : `${formatNumber(value, 1)} min`;
}
