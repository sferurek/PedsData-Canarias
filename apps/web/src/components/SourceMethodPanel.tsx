export function SourceMethodPanel({compact=false}:{compact?:boolean}){
 return <details className={`source-panel${compact?" source-panel-compact":""}`}><summary>Fuente y metodología</summary><div className="source-grid">
  <div><strong>Accesibilidad</strong><p>ISTAC 0–14 (2024), catálogo pediátrico, OSM congelado y OSRM 5.27.1. Acceso geográfico potencial; no representa tiempo hasta recibir atención sanitaria.</p></div>
  <div><strong>Territorio y entorno</strong><p>INE ADRH 2023, DEGURBA 2021 y Red Canaria 2025. Aire por estación sin interpolación.</p></div>
  <div><strong>Hospitalización</strong><p>ISTAC EMH 2020–2024. Edad × diagnóstico solo para Canarias; altas son episodios de residentes, no incidencia ni pacientes únicos.</p></div>
  <div><strong>Perinatal y mortalidad</strong><p>ISTAC 2024 por residencia materna; mortalidad de residentes en ventana 2020–2024 con conteos 1–4 suprimidos.</p></div>
  <div><strong>Urgencias</strong><p>Memoria CHUIMI 2024, actividad del hospital. No comparable con otros centros ni atribuible a residentes insulares.</p></div>
  <div><strong>Encuesta infantil</strong><p>ESC 2021, menores de 16. SURVEY_ESTIMATE en la geografía publicada; no prevalencia administrativa.</p></div>
 </div></details>
}
