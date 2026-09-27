# Gaps por isla y bloqueos

Un gap es una limitación de evidencia, no ausencia sanitaria. No se oculta ninguna isla. Estado al 27/09/2026.

|Isla|Disponible comprobado|Gap específico / riesgo|Acción de cierre|
|---|---|---|---|
|El Hierro|Malla 0–14 y SIAP insular; S23 Pediatría hospital; S37 AP Valverde/Frontera; S13 Echedo|N pequeño; horarios, dedicación y derivación; geometrías; UCIP/UCIN no verificadas|SCS gerencia: cartera vigente, puntos de entrada, horarios y red de traslado; validar dos ZBS|
|La Gomera|Malla, SIAP, cartera Guadalupe; cinco ZBS; estaciones S13|Un pediatra AP en recuento SIAP 2024 no informa cobertura de agendas ni atención hospitalaria; UCIP/UCIN desconocidas|Validar itinerancia y actividad AP, cinco límites y centros; no interpretar recuento como único pediatra de toda la isla|
|La Palma|Malla, SIAP, nueve ZBS, evidencia histórica Pediatría hospital; estaciones|Actualidad de cartera y memoria clínica; cambios territoriales/poblacionales requieren periodos compatibles|Actualizar catálogo hospital/AP, memoria y límites; no extrapolar actividad de otras islas|
|Tenerife|Malla, SIAP, Candelaria UCIP/UCIN histórica y HUC UCIN 2025|Múltiples hospitales/derivaciones; riesgo de doble conteo, geografía de residencia no publicada conjuntamente|Separar HUC/Candelaria/Sur; obtener series y centros AP; mapa ZBS vigente|
|Gran Canaria|Malla, SIAP, memoria CHUIMI; TIS ZBS 2023 localizada S42|No generalizar CHUIMI a Doctor Negrín ni a residentes; tabla TIS PDF requiere QA|Cartera y actividad de cada centro; verificar extracción TIS sin asumir cobertura E54086B|
|Fuerteventura|Malla, SIAP, hospital con Pediatría documentada, estaciones|SCS web 2026 cuatro ZBS vs SIAP 2024 seis; urgencias totales no pediátricas|Pedir nomenclátor con fechas y relación ZBS/equipo; resolver diferencia antes del cruce GIS|
|Lanzarote|Malla, SIAP, siete ZBS y Pediatría Molina Orosa documentada|La Graciosa dentro de Teguise, componente físico sin acceso terrestre; cartera urgente exacta pendiente|Conservar subgeografía y traslado; actualizar centros/horarios y separar urgencias generales|

## Gaps transversales

G01 — E54086B: ficha existente, no cubo ZBS validado en ninguna isla. Solicitar publicación/URL/códigos y diccionario; no inferir disponibilidad del plan estadístico.

G02 — Geometría: alternativa histórica IACS 2017 localizada; falta corroborar cobertura, topología, licencia y equivalencia actual. Directorios textuales y número de zonas no bastan.

G03 — Catálogo: faltan coordenadas, IDs oficiales, vigencia y cartera AP exhaustiva en las siete islas. Es bloqueo de accesibilidad robusta.

G04 — Routing: no benchmark ni tiempos calculados; no convertir caminos OSM en traslados clínicos. Motor no certificado todavía.

G05 — Edades: toda malla 2024 tiene 0–17 nulo. Necesaria otra fuente para adolescentes de 15–17; no repartir 15–19.

G06 — EMH pública: diagnóstico×edad×isla no disponible en producto verificado; requerir RAE-CMBD/SCS agregado por residencia y hospital. Diferenciar provincia de isla.

G07 — Urgencias/UCIP/UCIN: memorias fragmentadas; falta una serie común y confirmación de ausencia/presencia de unidades por isla. No convertir «no localizado» en cero.

G08 — Encuesta: tablas infantiles documentadas; falta n efectivo, diseño, errores y equivalencia 2009/2015/2021. Aislar 16–17 puede no ser posible en tablas adultas.

G09 — Aire/meteo: estaciones no equivalen a representatividad insular; faltan continuidad y contaminantes/variables de cada sensor. AEMET necesita credencial propia.

G10 — Renta: ámbito siete islas documentado, faltan pruebas de descarga/celdas por tramo infantil. No estimar pobreza infantil con renta media de adultos.

G11 — Derechos: aviso ISTAC verificado; licencias específicas de geometría, directorios, ambiente y red por cerrar antes de redistribución masiva.

G12 — Actualidad: ficha actualizada en 2026 puede ofrecer datos 2024 o anteriores. UI exige ambas fechas.

## Cierre y responsable propuesto

P0: G01–G05 y G11, responsables de datos/GIS con confirmación institucional SCS/ISTAC; G06/G07 para actividad, G08 metodología, G09 ambiente, G10 datos sociales. La FASE 0 puede cerrar con incertidumbres explícitas; el gate de MVP 0 no cierra hasta las pruebas críticas. Solicitudes redactadas en [wishlist](PEDIATRIC_DATA_WISHLIST.md); ninguna enviada.
