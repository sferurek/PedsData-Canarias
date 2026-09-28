export function SourceMethodPanel({compact=false}:{compact?:boolean}){
 return <details className={`source-panel${compact?" source-panel-compact":""}`}><summary>Fuente y metodología</summary><div className="source-grid">
  <div><strong>Accesibilidad</strong><p>ISTAC 0–14 (2024), catálogo pediátrico verificado, OSM congelado y OSRM 5.27.1. Acceso geográfico potencial; no representa tiempo hasta recibir atención sanitaria.</p></div>
  <div><strong>Desigualdad</strong><p>INE ADRH 2023 a escala municipal. Es renta general del territorio y no equivale a pobreza infantil.</p></div>
  <div><strong>Territorio</strong><p>DEGURBA ISTAC 2021 a 1 km cruzado con población infantil 2024. Los agregados municipales son derivados y se marcan ESTIMATED.</p></div>
  <div><strong>Entorno</strong><p>Red Canaria, observaciones diarias validadas 2025 por estación. Sin interpolación. Meteorología y calima siguen pendientes de observaciones validadas reutilizables.</p></div>
 </div></details>
}
