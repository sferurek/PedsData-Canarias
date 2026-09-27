# Matriz obligatoria de cobertura insular

Corte: 27/09/2026. Cobertura del dominio pedido, no simple existencia de una fuente. Una fila amplia puede ser PARTIAL aunque una subvariable esté completa. COMPLETE solo significa completa para el contrato explícito indicado debajo, no validación clínica ni actualidad en tiempo real.

- COMPLETE: observaciones no vacías verificadas para las siete unidades y periodo definido del contrato.
- PARTIAL: una parte comprobada; faltan dimensiones, cartera, series o comprobaciones relevantes.
- NOT AVAILABLE: resolución/variable no ofrecida por la fuente evaluada, sustentado en documentación; no significa ausencia del recurso sanitario.
- NEEDS VALIDATION: evidencia insuficiente o prueba técnica no ejecutada. Una búsqueda sin resultado usa este estado.

|Variable|El Hierro|La Gomera|La Palma|Tenerife|Gran Canaria|Fuerteventura|Lanzarote|
|---|---|---|---|---|---|---|---|
|Población infantil|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Pediatras AP|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|
|Zonas de Salud|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Centros con Pediatría|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Tiempo a Pediatría|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|
|Urgencias Pediátricas|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|PARTIAL|PARTIAL|NEEDS VALIDATION|NEEDS VALIDATION|
|Hospitalización pediátrica|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|UCIP|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|PARTIAL|PARTIAL|NEEDS VALIDATION|NEEDS VALIDATION|
|UCIN|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|PARTIAL|PARTIAL|NEEDS VALIDATION|NEEDS VALIDATION|
|Mortalidad pediátrica|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Perinatalidad|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Salud mental infantil|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Calidad del aire|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|
|Meteorología|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|
|Renta/vulnerabilidad|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|PARTIAL|

## Evidencia y alcance por fila

|Fila|Contrato y evidencia|Qué falta|
|---|---|---|
|Población|S01: malla 2024 0–14 completa en siete islas; S04 catálogo edades|0–17 en malla es nulo; conciliar total malla/censo; histórico y detalle neonatal|
|Pediatras AP|E54086A_000003 v1.1, 2024, PEDIATRIA_AP y NUMERO_PROFESIONALES_AP: siete valores|ZBS, equivalentes jornada completa, sustituciones y disponibilidad actual no incluidos en COMPLETE|
|Zonas de Salud|E54086A_000002: recuentos por isla; S24–S28 directorios|Geometría actual y códigos; conflicto Fuerteventura|
|Centros con Pediatría|Hospitales candidatos de las siete islas con evidencias de distinta antigüedad; S22/S23/S37–S40|Catálogo AP exhaustivo, coordenadas, horario y vigencia|
|Tiempo a Pediatría|Derivable, motores documentados S33–S36|Ningún cálculo ni benchmark insular ejecutado|
|Urgencias|S18 CHUIMI con serie; S19 evidencia clínica histórica Tenerife|Cartera diferenciada y actividad homogénea en resto; no convertir urgencias generales en pediátricas|
|Hospitalización|S05 ofrece EMH provincial, útil como contexto compartido|Diagnóstico×edad×isla no disponible en ese producto; otras memorias por centro pendientes|
|UCIP/UCIN|S19–S21 documentan servicios en islas capitalinas|Vigencia, capacidad y cobertura exacta; en otras islas estado desconocido, no ausencia confirmada|
|Mortalidad|S07/S08 agregados insulares documentados|Desagregación neonatal, edad adolescente exacta, estabilidad y celdas suprimidas|
|Perinatalidad|S06 tablas por isla documentadas|Descarga, completitud por cruce y denominadores de prematuridad|
|Salud mental|S10–S12 resultados infantiles/encuesta|Precisión por isla/edad/sexo, 16–17 años, series comparables|
|Aire|S13 estaciones identificadas en siete islas|Serie estación×contaminante×periodo, validez y representatividad espacial|
|Meteorología|S14 API localizada|Inventario autenticado, variables y continuidad por isla no auditados|
|Renta|S16/S17 ámbito insular/municipal documentado|Descarga siete islas y supresiones por edad/umbral|

## Subcontratos que evitan ambigüedad

|Subvariable|El Hierro|La Gomera|La Palma|Tenerife|Gran Canaria|Fuerteventura|Lanzarote|
|---|---|---|---|---|---|---|---|
|Malla 2024, campo 0–14 no nulo|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|COMPLETE|
|Malla 2024, campo 0–17 informado|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|
|E54086B, observaciones ZBS descargadas|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|NEEDS VALIDATION|
|EMH pública ISTAC, diagnóstico×edad×isla|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|NOT AVAILABLE|

Las matrices no certifican que no existan otras fuentes. [Pruebas descargadas](evidence/api_audit.json), [resultados](VALIDATION_REPORT.md), [gaps](DATA_GAPS.md), [fuentes](SOURCES.md).
