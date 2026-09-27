# Matriz de variables, denominadores y compatibilidad

Esta matriz establece contratos metodológicos para implementación futura. Las disponibilidad se rigen por [cobertura](ISLAND_COVERAGE_MATRIX.md), [inventario](PEDIATRIC_DATA_INVENTORY.md) y [fuentes](SOURCES.md).

|Indicador|Numerador / variable|Denominador|Unidad / edad|Geografía máxima defendible|Reglas y limitaciones|
|---|---|---|---|---|---|
|Población infantil|Residentes del grupo|No aplica|personas, edad original|isla/municipio; 0–14 malla|No obtener 0–17 de 15–19 fraccionando|
|Densidad infantil|Población infantil|superficie km² validada|niños/km²|misma delimitación|Malla ocupada no equivale a superficie total insular|
|Crecimiento|P(t)−P(t−1)|P(t−1)|%|misma edad y territorio|Documentar cambio padrón/censo y límites|
|Niños por pediatra|Población residente infantil o TIS pediátrica|pediatras mismo ámbito/fecha|personas/profesional|isla verificada; ZBS pendiente|Dos indicadores distintos: residencia y asignación. No denominar carga asistencial al primero|
|Pediatras por 10.000 niños|Pediatras×10.000|población compatible|profesionales/10.000|isla|Plantilla física no equivale a FTE; cero profesionales implica ratio no definido|
|Consultas por 1.000|Consultas pediátricas×1.000|población/TIS compatible|consultas/1.000|isla; ZBS por validar|Contactos, no personas. Mantener consulta presencial/domicilio/remota original|
|Consultas por pediatra|Consultas compatibles|profesionales/FTE compatible|consultas/profesional/año|isla|No dividir actividad anual entre plantilla puntual sin aviso|
|Frecuentación|Contactos|asignados o usuarios atendidos|contactos/persona|fuente original|No confundir frecuentación general y por usuario|
|Acceso <15 min|Σ población celda con t<900s|población infantil objetivo|% y personas, 0–14 inicialmente|isla, ZBS si límites validados|Separar desconocido y sin ruta, no excluirlos silenciosamente|
|Acceso >20 min|Σ población con t>1200s|población objetivo|% y personas|igual|Publicar población evaluada y no evaluable; no asumir t desconocido >20|
|Mediana/P90 acceso|Cuantiles ponderados por población|población con ruta válida|minutos|isla|Reportar fracción excluida; si hay no alcanzables, distribución global censurada/no finita según caso|
|Ingreso desde urgencias|Episodios ingresados|urgencias pediátricas|%|hospital|Definición de ingreso/observación y edad deben coincidir|
|Hospitalización por diagnóstico|Altas por códigos/versiones|población residente si altas son por residencia|altas/10.000|provincia/Canarias EMH|Centro de atención no sustituye residencia. Reingresos no son pacientes únicos|
|Estancia media|Estancias|altas/episodios definidos|días|hospital/provincia|Mantener convención de la fuente y exclusiones|
|Prematuridad|Nacidos vivos <37 semanas|nacidos vivos con gestación conocida|%|isla residencia materna|Si tabla mide partos, producir indicador por partos; no intercambiar partos y bebés|
|Mortalidad infantil|Defunciones <1 año|nacidos vivos mismo periodo/ámbito|por 1.000 nacidos vivos|isla si categorías lo permiten|IC exacto Poisson apropiado; no dividir por población 0–14|
|Mortalidad neonatal|Muertes 0–27 días|nacidos vivos|por 1.000 nacidos vivos|según fuente|Separar neonatal precoz 0–6 y tardía 7–27 si existe|
|Mortalidad 1–4/5–14/adolescente|Muertes edad original|personas-año mismo grupo|por 100.000|isla si compatible|Agrupar años sumando numeradores/denominadores, no promediar tasas|
|Mortalidad perinatal|MFT + neonatal precoz según definición fuente|nacidos vivos + MFT compatibles|por 1.000 nacimientos|según fuente|Registrar umbral gestacional/peso para MFT|
|Salud mental y hábitos|Respuestas ponderadas|muestra elegible ponderada|%/puntuación, edades fuente|isla/gran comarca según tabla|Varianza de encuesta compleja, no IC binomial ingenuo|
|Entorno respiratorio|Concentraciones y meteo válidas|tiempo observado; cobertura|µg/m³, °C, %, mm, m/s|estación; agregación explícita|PM10 alto no prueba por sí solo calima; no trasladar estación a toda isla|
|Vulnerabilidad infantil|Indicador ADRH por edad si existe|población definida INE|%/euros|territorio original|No estimar mediana insular promediando medianas municipales|
|Accidentes|Víctimas infantiles|población residente solo con advertencia de exposición|conteo/tasa|municipio/isla ubicación|Turismo y movilidad alteran población expuesta|
|Antibióticos|Prescripciones infantiles reales|niños o personas-tiempo|recetas/1.000 niños|según fuente|DDD adulta inadecuada como dosis infantil; no inferir edades|

## Edades

Conservar perinatal, neonatal, <1, 1–4, 5–9, 10–14, 15–17, 15–19, 0–14, 0–17 y 0–19 cuando existan. Registrar límites inclusivos, unidad (días/años/semanas), universo, original label/code y versión. «Menor de 16» y «hasta 14» no son equivalentes. 15–19 incluye adultos; mostrarlo solo como grupo obligado por fuente y señalizado, sin reclasificarlo 15–17. Prohibida suma de categorías solapadas.

## Small numbers

Aplicar supresión original de la fuente siempre; nunca reconstruir celdas por resta. Propuesta de política local, pendiente revisión metodológica: ocultar conteos de 1–4 y supresión complementaria cuando permitan identificación, preservar el cero observado; marcar n<20 como inestable y estudiar ventanas fijas de 3–5 años. No es un umbral legal universal. Aplicar revisión de revelación a exportaciones y combinaciones de filtros.

IC 95% de tasas raras mediante Poisson exacto cuando sea adecuado; cero eventos conserva límite superior positivo. Para proporciones usar método compatible con diseño; encuestas requieren estratos, conglomerados y pesos. Reportar números absolutos, denominador, ventana y avisos. Las islas pequeñas nunca desaparecen por supresión.

## Cruce ambiental

Solo enlazar series clínicas y ambientales con geografía, periodo y población compatibles. Datos clínicos anuales provinciales no sostienen análisis diario insular de calima. Registrar confusión por estacionalidad, infecciones, edad, acceso y cambios de registro; preespecificar lags y análisis de sensibilidad antes de investigar.
