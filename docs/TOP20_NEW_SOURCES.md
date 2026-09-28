# Top20 — oportunidades nuevas
Auditoría28/09/2026. Identificadores enlazan a la [matriz con URL primaria, fechas y licencia](NEW_DATA_SOURCES_MATRIX.md). Orden de prioridad editorial, no suma de scores. Estimación en jornadas de una persona para adquisición/QA/admisión, sin UI ni espera institucional; no compromiso. Ninguna fila está integrada por esta auditoría. Frecuencia anual salvo indicación.

| Prioridad / ID | Aporte/variable | Edad y geografía | Periodo/formato/frecuencia | Esfuerzo | Límite y recomendación |
|---|---|---|---|---|---|
| 1 ·01 SIAP actividad | Consultas, usuarios, frecuentación | Pediatría servicio;7 islas | 2007–24 CSV/API anual | 2–4d | Primera integración candidata; validar cada cubo y denominador, no reutilizar edad de otro cubo |
| 2 ·02 Espera consultas | Pendientes Pediatría/Cirugía Pediátrica | Especialidad;7categorías insulares | 2017–25 CSV semestral | 2–4d | Cerrar isla asistencial vs residencia; no denominar demora a un stock |
| 3 ·03 Espera quirúrgica | Pendientes por tramo | Cirugía Pediátrica;islas con ausencias | Desde 2003 CSV cortes | 2–4d | Mantener missing y cambios; no transformar especialidad en0–17 |
| 4 ·05 BDCAP | Morbilidad/dispensación/utilización | Quinquenios;Canarias | 2024 documentación/exportExcel anual | 4–7d | Probar export pediátrico; usar muestra ponderada; no isla |
| 5 ·06 SIVAMIN | Coberturas por vacuna/cohorte | Cohortes;Canarias | Variable/resumenU07/2026 dashboard/PDF anual | 3–5d | Distinguir provisional/definitivo, denominadores y cambios calendario |
| 6 ·11 HBSC | Bienestar/hábitos adolescente | Escolarizados 11–18;Canarias | 2022 PDF cuatrienal | 3–5d | Nueva ventana adolescente; error/n/diseño antes de series |
| 7 ·14 ESdE | Salud/uso/pantallas infantil | Edadvariable;CCAA | 2023 tablas/microdatos por edición | 4–6d | Edad1–14 para pantallas; no duplicar ESC ni encadenar cuestionarios |
| 8 ·15 Cribado metabólico | Cobertura/oportunidad programa | Neonatos;CCAA | 2024 PDF anual | 2–4d | Programas/paneles distintos; enfermedades raras suprimidas |
| 9 ·16 Cribado auditivo | Proceso preventivo neonatal | Neonatos;CCAA | 2024 PDF anual | 2–4d | No prevalencia de hipoacusia; verificar pérdidas seguimiento |
| 10 ·17 Memoria Lanzarote | Actividad AP y servicio hospital | Servicio;Lanzarote/hospital | 2022–23 PDF anual | 3–5d | Mantener escalas, camas/altas/estancias; ingreso urgente no visita en Urgencias |
| 11 ·18 CHUIMI especialidades | UCIP/Neonatología/cirugía | Servicio;hospital | 2023–24 HTML/PDF anual | 2–4d | Incremental sobre ED existente; hospital≠residencia GC |
| 12 ·07 IRA+nirsevimab | Vigilancia por edad y prevenciónVRS | 0–4/5–14;regional/áreas según tabla | Semana1/2025 PDF semanal | 4–7d | Auditar red; extracción visual anexo; dosis≠cobertura |
| 13 ·12 ESTUDES | Adicciones adolescente | Escolarizados 14–18;Canarias | 2023 PDF bienal | 2–4d | No extrapolar a no escolarizados; no mapas insulares |
| 14 ·20 Red UAT | Recursos atención temprana | 0–6;7 islas declaradas | Acumulado2020–25 HTML eventual | 3–5d | Verificar vigencia/ubicación uno a uno; no tasas con acumulados |
| 15 ·28 NEAE | Necesidades de apoyo educativo | Etapas;CCAA/provincia | Curso 2023–24 tablas anual | 3–5d | Contexto educativo, no diagnóstico ni prevalencia clínica |
| 16 ·19 GAPGC demora | Acceso operativo complementa routing | Pediatría;GC | 2017–21 HTML anual histórico | 2–3d | No actualidad; agenda no espera experimentada por cada paciente |
| 17 ·04 SCS espera hospital | Contraste hospitalario del stock | Especialidad;hospital | Diciembre2025 PDF semestral | 2–3d | Solapa02/03; integrar solo valor adicional hospital/demora |
| 18 ·42 Centros educativos | Contextualizar acceso y entorno escolar | Etapa;recurso puntual | U2023 GeoJSON irregular | 2–4d | Validar7 islas, estado y licencia; no alumnado inferido |
| 19 ·44 SICA ruido | Contexto de ruido alrededor de población infantil | Auxiliar;áreas/ejes parciales | Fase 2022 GPKG/PDF quinquenal | 4–7d | Cobertura incompleta; ruido modelado no medición individual |
| 20 ·48 Meteo Tenerife | Observaciones reales sin bloqueo por clave AEMET | Auxiliar;estaciónTenerife | 2025–26 CSV/JSON semanal | 2–4d | Mejora parcial, mantener otras 6 islas con estado faltante |

BDCAP aporta varias dimensiones pero cuenta como una familia. Las dos listas de espera cuentan como productos distintos con medidas distintas; su admisión conjunta debe evitar duplicación. ALADINO, RENAVE, SiVIRA, EDAD, SINAC y SIOSE quedan en segunda ola por granularidad, validación pendiente o menor prioridad inmediata.

Todos los periodos son de referencia; fecha de publicación desconocida permanece desconocida. Un informe actualizado2026 sobre2024 no se rotulará como observación2026. Las licencias P del Top20 bloquean redistribuir documentos completos hasta revisar condiciones; permiten mantener la recomendación y el enlace.
