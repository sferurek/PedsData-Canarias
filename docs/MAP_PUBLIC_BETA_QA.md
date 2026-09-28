# QA del mapa — beta pública

Capas auditadas: accesibilidad, renta, densidad infantil, DEGURBA, pediatras AP, frecuentación, PM10, PM2,5, NO2 y prematuridad.

Cada capa conserva geografía, periodo, unidad, clasificación, estado y `source_id`. Solo hay una capa principal de color; centros, estaciones y límites son auxiliares. Aire se representa por estación; renta y densidad por municipio; dotación, frecuentación y prematuridad por isla; accesibilidad por malla. No se colorean municipios con datos regionales ni islas a partir de una estación.

E2E valida cambio de capa, leyenda, histórico, filtro insular, retorno a accesibilidad y provenance. La inspección visual cubre mapa completo, siete islas, Lanzarote/La Graciosa, escritorio e iPhone. La Graciosa usa `requires_interisland_transfer` y no la banda `>=30`.
