# Matriz de admisión de datos clínicos — Fase 5

Auditoría: 28/09/2026. `ADMIT` describe un producto concreto, no todo el dominio.

| Dominio | Fuente | Edad | Geografía | Periodicidad | Definición | Comparabilidad | Estado |
|---|---|---|---|---|---|---|---|
| Hospitalización: altas, estancias y estancia media por diagnóstico | ISTAC EMH E30414A_000009 | <1, 1–4, 5–14; 15–24 excluido | Canarias, residencia | Anual 2020–2024 | Residentes canarios dados de alta en cualquier hospital nacional; diagnóstico principal | Comparable temporalmente en el cubo; no insular | ADMIT_WITH_LIMITATIONS |
| Hospitalización por isla | EMH pública | Pediátrica | Provincia/Canarias | Anual | No existe cruce edad × diagnóstico × isla | No defendible | HOLD |
| Urgencias CHUIMI | SCS, memoria 2024 | “Pediátrica”; límite no publicado | Hospital | Anual | Atendidas, ingresadas y ambulatorias | Coherencia interna; no homogénea con otros centros | ADMIT_WITH_LIMITATIONS |
| Urgencias, comparación entre hospitales | Memorias SCS heterogéneas | Variable/desconocida | Hospital | Irregular | Puertas, observación y límites etarios no armonizados | Insuficiente | HOLD |
| Nacimientos y prematuridad | ISTAC E30304A_000008 | Perinatal | Isla de residencia materna | Anual 1999–2024 | Nacimientos según maturidad del parto | Siete islas, definición estable dentro del cubo | ADMIT |
| Mortalidad pediátrica por grandes causas | ISTAC E30417A_000001 | <1, 1–4, 5–14 | Isla de residencia | Anual; publicada en ventana 2020–2024 | Causa básica, grandes grupos CIE-10 | Ventana fija y supresión local 1–4 | ADMIT_WITH_LIMITATIONS |
| ESC 2021: problemas de salud alguna vez | ISTAC C00035A_000465 | Menores de 16 | Canarias; GC; TF; grupos de islas | Plurianual | Estimación ponderada de encuesta | Sin n/error por celda en esta tabla; no desagregar grupos | ADMIT_WITH_LIMITATIONS |
| ESC 2009/2015 comparativa completa | ISTAC ESC | Edades/cuestionarios variables | Escalas variables | 2009/2015 | Requiere crosswalk pregunta a pregunta | No cerrado | RESEARCH_ONLY |
| Respiratorio × ambiente | EMH anual regional + aire diario por estación | Pediátrica | Canarias vs estación | Anual vs diario | Resoluciones incompatibles para correlación | Solo inventario de alineación | HOLD |

No se transforman provincias en islas, hospitales en residencia, 15–24 en 15–17 ni estimaciones de encuesta en prevalencia administrativa.
