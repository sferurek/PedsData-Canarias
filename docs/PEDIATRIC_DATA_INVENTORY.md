# Inventario pediátrico de fuentes

Consulta 27/09/2026. «Documentado» no equivale a «descargado y validado». Todas las fuentes Sxx enlazan al [registro](SOURCES.md). Licencias no comprobadas quedan pendientes, no se heredan de un portal a otro. La última edición localizada no es una promesa de exhaustividad.

|ID / prioridad|Proveedor/producto|Variables y edades|Geografía real|Periodo / periodicidad|Formato y acceso comprobados|Licencia / estado|
|---|---|---|---|---|---|---|
|POP-GRID / P0|S01 ISTAC malla 250 m|poblacion_00a14; 00a17 nulo|celdas, isla, municipio; siete islas|01/01/2024 provisional; anual|GeoJSON WFS descargado; CSV/GPKG/GML/KML y ODS diccionario catalogados|Aviso ISTAC; descarga validada estructuralmente|
|POP-AGE / P0|S04 E30243A_000001 v1.5|sexo/edades originales|Canarias/islas/municipios|anual; máximos del cubo pendientes|Catálogo JSON consultado, distribuciones CSV/TSV/JSON/XLSX|Aviso ISTAC; pendiente observaciones|
|AP-STAFF / P0|S02 E54086A_000003 v1.1|pediatras y ratio publicado|siete islas/Canarias|2004–2024; anual|CSV completo descargado|Aviso ISTAC; recuento 2024 siete islas confirmado|
|AP-TIS / P0|S02 E54086A_000001 v1.1|TIS, sexo, 0–4, 5–9, 10–14, 15–19, resto|siete islas/Canarias|2004–2024; anual|CSV completo descargado|Aviso ISTAC; distinguir asignación/residencia|
|AP-ZCOUNT / P0|S02 E54086A_000002 v1.1|número ZBS, centros y consultorios generales|siete islas/Canarias|2004–2024; anual|CSV completo descargado|Aviso ISTAC; no geometría ni cartera pediátrica|
|AP-ACT / P0|S02 colección E54086A_000001|consultas, pacientes, frecuentación por profesional/edad|islas; cruces separados|actividad desde 2007 según colección; anual|visualizador documentado; ficheros actividad pendientes|Aviso ISTAC; no mezclar tablas como si todas las dimensiones coexistieran|
|AP-SMALL / P0|S03 E54086B|personal, actividad y centros por ZBS anunciados|ZBS, cobertura efectiva desconocida|anual; última ficha 28/05/2026, no periodo de datos|HTML/API operación; descarga de observaciones no localizada|No declarar disponible a nivel ZBS|
|ZBS-GEO / P0|S24–S29 SCS / IACS|límites, códigos y versiones|siete islas requeridas; directorios parciales revisados|directorios variables; alternativa 2017|HTML textual; ZIP histórico localizado|Licencia geometría histórica pendiente; actualidad/topología pendientes|
|FACILITY / P0|S18–S23/S37–S40 SCS|Pediatría, neonatología, unidades y cartera|centro/hospital; residencia paciente distinta|documentos heterogéneos|HTML/PDF; no base geocodificada consolidada|Reutilización por producto pendiente; no republicar PDFs completos|
|EMERGENCY / P1|S18 memorias SCS|urgencias pediátricas, ingresadas, ambulatorias|hospital CHUIMI verificado|2023/2024; anual en memoria|HTML/PDF|Serie utilizable localizada; equivalencia resto pendiente|
|HOSP / P1|S05 EMH ISTAC/INE|altas, estancias, edad, sexo, diagnóstico; comprobar cruces|provincia/Canarias; residencia vs hospital|2020–2024 y ediciones anteriores; anual|índice/visualizador; formato de descarga pendiente|No dato insular verificable en EMH pública|
|PERINATAL / P1|S06 E30304A|nacidos, gestación, prematuridad, edad materna, múltiples, MFT, tipo parto|isla residencia madre; algunos municipios|1999–2024; anual|colección HTML; cubos pendientes|Aviso ISTAC; revisar denominador y desconocidos|
|MORT / P1|S07 E30306A / S08 E30417A|defunciones edad/sexo y grandes causas|isla residencia; detalles solo Canarias|1999–2024; anual|colecciones y metodología PDF|Aviso ISTAC; small numbers y defectos históricos S09|
|SURVEY / P1|S10/S11 ESC, S12 índice|menores 16; salud mental 4–15, CVRS 8–15, hábitos, lactancia, uso|isla y grandes comarcas GC/TF según tabla|2009/2015/2021; plurianual, 2021 localizado|HTML/PDF; microdatos/tablas localizar individualmente|Aviso ISTAC para sus tablas; comparabilidad y diseño pendientes|
|AIR / P0|S13 Gobierno; MITECO complemento|PM10, PM2.5, NO2, O3, SO2 deseados|estación, no isla homogénea|horario deseado; vigencia de cada serie pendiente|listado HTML validado; descarga de observaciones pendiente|Condiciones de cada red pendientes|
|WEATHER / P1|S14/S15 AEMET; SensorThings candidato|temperatura, humedad, lluvia, viento, extremos|estación, siete islas por validar|horario/diario según producto|REST JSON documentado con API key; no prueba autenticada|Condiciones AEMET a registrar antes de redistribuir|
|SOCIAL / P0|S16/S17 INE ADRH|renta persona/hogar; umbrales por edad donde proceda|islas, municipios, distritos, secciones|2015–2023; anual|web/metodología; descarga de tabla pendiente|Condiciones INE pendientes de incorporar a manifiesto|
|INJURY / P2|S30 DGT, ISTAC complemento|víctimas, gravedad, edad, municipio deseados|ubicación accidente; residencia no equivalente|2024 localizado; anual|ficheros y diccionario catalogados, no descargados|Validar licencia, geografía y edad conjunta|
|PHARMA / P2|S31 BDCAP; SCS solicitud|prescripción/antibióticos por edad|CCAA documentada; isla no acreditada|anual|portal; extracción infantil no verificada|No módulo visible hasta desglose real|
|ROAD / P0|S33–S36 routing + OSM / SITCAN candidato|red, sentidos, accesos y velocidades|componentes físicos por isla|snapshot versionado, no frecuencia garantizada|motores documentados; red no descargada|Registrar ODbL/atribución de OSM y licencia propia del motor|

## Prioridad y cobertura

P0 son dependencias del MVP de acceso; P1 amplía resultados de salud; P2 investigación condicionada. P0 no significa disponibilidad confirmada. Ninguna fuente de actividad hospitalaria representa automáticamente a residentes de su isla: hay derivaciones y doble insularidad.

No se ha enviado ninguna solicitud institucional. Los candidatos SITCAN/GRAFCAN, MITECO y SensorThings requieren URL exacta, metadatos de servicio, licencia y ensayo antes de promoción a fuente validada.
