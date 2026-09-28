# Open Data Deep Audit — PedsData Canarias
Fecha de comprobación: 28/09/2026. Base: main, 14a0beb. Alcance: documentación de investigación; no incorporación de datos, código, UI ni despliegue.

## Dictamen
**A. MUCHO_MAS_POR_EXPLOTAR**

Hay varias familias nuevas de alto valor y al menos dos con tablas estructuradas e información insular comprobada: actividad de Pediatría AP y listas de espera por especialidad. BDCAP, vacunación, HBSC, ESdE y cribados amplían la dimensión pediátrica regional. Esto no resuelve el límite de los datos operativos por centro, edad, diagnóstico y semana.

## Lectura de partida y deduplicación
Se contrastó la documentación de fases 0–5, inventario, SOURCES, matrices, metodología clínica, licencias, gaps y auditoría E54086B. El estado relevante figura en PHASE5_REPORT, UPDATED_DATA_MATRIX y las metodologías por dominio. Se preservan los hallazgos previos y la ZBS histórica excluida. La documentación clínica integrada se incluye como cuatro controles 57–60 en la matriz; accesibilidad, renta, DEGURBA, aire y recursos AP no se vuelven a vender como descubrimientos.

Se revisaron **60 candidatos agrupados** en [la matriz](NEW_DATA_SOURCES_MATRIX.md), incluyendo descartes, solicitudes y controles. Revisado no significa que se descargaron y validaron 60 datasets completos. D/M/C identifica inspección directa, evidencia documental o localización primaria pendiente. La cobertura y licencia desconocidas permanecen explícitas.

## Resultados que cambian la prioridad
1. **SIAP actividad:** el CSV E54086A_000005 contiene 1.728 filas y Pediatría AP por isla, lugar y año 2007–2024. Incluye las siete islas; no incluye edad individual. El catálogo también ofrece personas distintas y frecuentación. No son los tres cubos de dotación ya incorporados.
2. **Espera:** C00045A_000002 contiene 4.032 filas, Pediatría y Cirugía Pediátrica, siete categorías insulares, cortes 2017–2025. Falta cerrar la definición territorial antes de interpretarlo como espera de residentes. C00045A_000001 aporta espera quirúrgica, con ausencias explícitas.
3. **BDCAP:** documentación oficial describe morbilidad, dispensación, visitas e interconsultas con edad y CCAA. Es una muestra ponderada de historias; no un censo insular. Priorizar personas con dispensación sobre una interpretación pediátrica de DDD.
4. **Prevención y adolescencia:** SIVAMIN, cribados, HBSC y ESdE aportan indicadores distintos de ESC2021. No habilitan mapas insulares.
5. **Memorias:** Lanzarote 2023 aporta actividad hospitalaria pediátrica y AP identificable; CHUIMI ofrece recursos y actividad por especialidad adicionales a urgencias 2024. No convertir servicio en edad exacta ni hospital en isla de residencia.

Fuentes exactas y tiempos están en [Top20](TOP20_NEW_SOURCES.md) y la matriz. Las cifras de auditoría no son nuevos indicadores admitidos.

## Evidencia directa reproducible
Consultas CKAN efectuadas sobre el catálogo estadístico:
- https://datos.canarias.es/catalogos/estadisticas/api/3/action/package_search?fq=name%3A*e54086a*&rows=50 — 13 entradas, incluidos esquemas; no son 13 nuevos datasets.
- https://datos.canarias.es/catalogos/estadisticas/api/3/action/package_search?fq=name%3A*c00045a*&rows=50 — 6 entradas.
- Búsqueda textual ahogamiento: tres productos E30417A_000010–12. Solo el primero inspeccionado contiene edad.

Las URL de descarga son las del catálogo, no rutas deducidas. Los ficheros temporales no se incorporan a curated. Firmas de los bytes inspeccionados:
| Artefacto | SHA256 | Resultado |
|---|---|---|
| E54086A_000005/1.1.csv | 0918db3dab0ede536f57176f40634e5538ecf71980d3b68649ffab36e507edda | 1.728 filas; Pediatría AP y 7 islas |
| C00045A_000002/1.3.csv | 14eb84d8467658ac174de5625f0e2a85d55b460bb2531397b6e27a3b7db6648e | 4.032 filas; Pediatría y 7 islas |
| E30417A_000010/1.2.csv | 0a81ac2a8c15cd649634c66157bba192cf68cfba864245e2fef0422aae034edd | 11.880 filas; isla inscripción; edad ambigua |
| Diccionario DGT accidentes | 1df06643eff95dd7f3211fca7fad2c95f2d926930d12ca97a345c764995d0ae9 | XLSX; unidad accidente; no edad víctima |

Diccionario DGT: https://www.dgt.es/export/sites/web-DGT/.galleries/downloads/dgt-en-cifras/24h/Diccionario_Tabla_Accidentes.xlsx

Verificaciones adicionales: C00045A_000001 tiene 19.440 filas; Lanzarote PDF de 185 páginas, Pediatría p. 88 y AP p. 142; IRA Canarias: 14 páginas, edades p. 5–6, centinelas p. 8–9 y nirsevimab p. 14. No se hizo extracción validada de la tabla raster de nirsevimab: no afirmar siete áreas con dato.

## Cobertura real
| Producto inspeccionado | El Hierro | La Gomera | La Palma | Tenerife | Gran Canaria | Fuerteventura | Lanzarote |
|---|---|---|---|---|---|---|---|
| Consultas Pediatría AP 2024, cubo 000005 | Valor | Valor | Valor | Valor | Valor | Valor | Valor |
| Pendientes consulta Pediatría 12/2025, cubo 000002 | Cero publicado | Valor | Valor | Valor | Valor | Valor | Valor |
| Memoria Lanzarote 2023 Pediatría | No aplicable | No aplicable | No aplicable | No aplicable | No aplicable | No aplicable | Hospital/unidades |
| GAPGC 2021 demora agendas | Sin evidencia | Sin evidencia | Sin evidencia | Sin evidencia | Parcial | Sin evidencia | Sin evidencia |
| SIVAMIN/BDCAP/HBSC | Regional | Regional | Regional | Regional | Regional | Regional | Regional |

Regional no significa un valor asignable a cada isla. Cero publicado en espera no prueba ausencia de necesidad, ausencia de derivaciones ni inexistencia de servicio. La Graciosa no se presume separable de Lanzarote. Memorias hospitalarias siguen territorio asistencial, no residencia.

## Búsqueda por dominio y negativos importantes
Ruta de búsqueda aplicada: catálogo → organismo/operación → descargas → memorias/PDF → API/GIS cuando pertinente → histórico → equivalente nacional. No todos los pasos producen un recurso; no se inventaron endpoints al faltar descarga. Los índices y resultados parciales se califican C. Registro resumido:

| Dominio | Ruta/evidencia encontrada | Negativo y trabajo pendiente |
|---|---|---|
| Urgencias | SCS memorias CHUIMI, Lanzarote, Negrín, HUC, Candelaria; RAE-CMBD | No serie pediátrica homogénea mensual de9 hospitales. Memoria científica no asistencial |
| Hospitalización | ISTAC integrado, memoria Lanzarote, SIAE/RAE | No nuevo fichero probado edad×diagnóstico×isla residencia |
| AP | Catálogo ISTAC E54086A, API CSV, GAPGC, SIAP/BDCAP | No cubo público nuevo ZBS×mes×diagnóstico; no reabrir E54086B sin evidencia |
| Vacunas | SIVAMIN histórico/cohortes; IRA anexo nirsevimab | No cobertura vacuna×cohorte×municipio probada |
| Farmacia | BDCAP, PRAN, CIMA documentación | PRAN general no prueba uso pediátrico; CIMA no dispensación |
| Salud mental | HBSC/ESTUDES, directorioSCS, CHUIMI, ESCbase | Listas psiquiatría general no espera infantojuvenil |
| Nutrición | ALADINO, ESdE, HBSC, ECV | No representatividad ALADINO para7 islas demostrada |
| Neonatal | SICN/hipoacusia, SCS y memorias | Muestras de talón no niños únicos; no lactancia al alta7 islas |
| Transmisibles | RENAVE/CNE, SCS epidemiología/IRA | Edad y territorio publicados por separado no autorizan cruce |
| Microbiología | SiVIRA y red centinela SCS; históricoSIM | No positividad pediátrica hospital×semana7 islas abierta validada |
| Lesiones | ISTAC ahogamientos API, DGT diccionario, INTCF | DGT accidente no contiene edad; edad 4 ahogamientos requiere aclaración |
| Discapacidad/temprana | EDAD, IMSERSO/SAAD, UAT SCS | Reconocimientos ≠ prevalencia; consultas ≠ niños |
| Escolar | EducaciónNEAE, SITCAN centros, PADICAN, convenioBOC | Evaluación de enfermería prevista no equivale a resultados |
| Esperas | ISTAC C00045A API y SCS PDF | Falta semántica geográfica/edad; no demora AP actual7 islas |
| Plantillas | SIAP, SIAE, BOC | Plazas vacantes ocupadas provisionalmente ≠ plazas sin cubrir |
| Recursos hospital | CHUIMI, Lanzarote, SIAE | No catálogo vigente homogéneo enfermeríaUCIP/UCIN7 islas |
| Acceso operativo | GAPGC histórico, ODDUS, TITSA | Quejas no tiempo de atención; horarios GTFS no puntualidad |
| Determinantes | INE/ECV, SICA, SIOSE, SINAC, EGIF, cabildos/municipios | Cobertura parcial; no exposición individual ni inferencia doméstica |

Búsquedas negativas concretas: búsquedas literales CKAN de salud mental menores devolvieron un diccionario, no observaciones; una búsqueda de peso al nacer devolvió0, **no demuestra ausencia**. Búsquedas SCS La Palma 2024 encontraron consejo con AP y hospital general; El Hierro devolvió cartera y documentos de personal, sin serie de urgencia pediátrica verificada. Consultas Negrín encontraron memoria pero no acreditaron pediatría diferenciada. HUC y HUNSC devolvieron memorias de investigación, insuficientes. No se descargaron todos los anexos de todos los ayuntamientos: la auditoría es amplia y trazable, no prueba universal de inexistencia.

## Límites de esta auditoría
No se completó validación de observaciones del dashboard BDCAP/SIVAMIN, microdatos nacionales, tabla raster nirsevimab ni todos los GIS WMS/WFS. Se localizaron fuentes GIS descargables; no se declara una nueva capa sanitaria WFS vigente. No se verificaron licencias específicas de todos los PDFs. No se obtuvieron datos privados. Estos límites afectan admisión, no invalidan las oportunidades documentadas.

Entregables: [matriz](NEW_DATA_SOURCES_MATRIX.md), [Top20](TOP20_NEW_SOURCES.md), [hallazgos ocultos](HIDDEN_GEMS.md), [límites y licencias](OPEN_DATA_LIMITS.md), [solicitudes candidatas](DATA_REQUEST_CANDIDATES.md), [Fase6 propuesta](PHASE6_RECOMMENDATION.md).

## Control documental final
- 60 filas, 11 columnas, 8 puntuaciones entre 0 y 5 por candidato; 20 prioridades.
- Evidencia: 7 D, 47 M, 6 C.
- Estados: 15 NUEVO_Y_UTIL, 13 NUEVO_PERO_AGREGADO, 15 RESEARCH_ONLY, 4 REQUIERE_SCRAPING, 3 REQUIERE_SOLICITUD, 5 SIN_VALOR_INCREMENTAL, 1 NO_REUTILIZABLE, 4 YA_INTEGRADO.
- Enlaces internos comprobados; no se declara validación masiva de todos los enlaces externos ni admisión clínica.
- Solo se han añadido los siete documentos solicitados. No se ejecutó suite de aplicación porque no cambió código; no se integraron datasets ni enviaron solicitudes.
