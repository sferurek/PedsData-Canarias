export function SourceMethodPanel({ compact = false }: { compact?: boolean }) {
  return <details className={`source-panel${compact ? " source-panel-compact" : ""}`}>
    <summary>Fuente y metodología</summary>
    <div className="source-grid">
      <div><strong>Fuente</strong><p>ISTAC, malla 250 m 0–14 (2024) y catálogo pediátrico público verificado.</p></div>
      <div><strong>Ruta</strong><p>OSRM 5.27.1 · OSM canary-islands-260926 · grafo congelado.</p></div>
      <div><strong>Denominador</strong><p>Población total y evaluable se muestran por separado. Cuantiles ponderados por niños.</p></div>
      <div><strong>Límite</strong><p>Acceso geográfico potencial por carretera; no representa tiempo hasta recibir atención sanitaria.</p></div>
    </div>
  </details>;
}
