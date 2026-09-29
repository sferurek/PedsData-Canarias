# Informes territoriales pediátricos

Fecha: 29/09/2026. Versión: **v0.9.0-beta.2**. Estado: **PUBLIC BETA**.

## Objetivo

`TERRITORIAL_REPORT` convierte una isla, municipio o componente territorial registrado en un informe HTML estructurado. No incorpora datasets, fuentes ni metodologías nuevas. El planner consume exclusivamente `metrics_catalog`, `sources_catalog`, las series publicadas y los agregados territoriales validados.

Rutas: `/informes/[geography_id]`. Se generan estáticamente Canarias, las siete islas, La Graciosa y los 88 municipios. Las rutas no registradas devuelven 404.

## Flujo determinista

1. resuelve `geography_id` contra el registro territorial;
2. conserva la resolución real: `island`, `municipality`, `grid_250m` o `autonomous_community`;
3. selecciona métricas registradas compatibles;
4. recupera observaciones y agregados validados;
5. agrupa por dominio;
6. calcula cambios absolutos y porcentuales, relación de niños por pediatra, participación en el total de las siete islas y comparación de accesibilidad solo cuando escala, periodo y método coinciden;
7. elige tabla, serie o mapa según el dato;
8. renderiza únicamente si existen `source_ids`;
9. lista únicamente las fuentes usadas.

Ask PedsData interpreta la intención y abre el informe. No calcula ni genera cifras.

## Resumen editorial seguro

El resumen detecta mediante reglas de código:

- aumento, descenso o estabilidad de población infantil asignada, pediatras, consultas, frecuentación, nacimientos y prematuridad;
- cambio en la relación publicada de niños por pediatra;
- concentración insular de métricas aditivas;
- diferencia descriptiva de accesibilidad frente al agregado de las siete islas.

Cada hallazgo guarda `metricIds` y periodo, y muestra **“Fuentes de este resultado”**. La redacción no atribuye causalidad, riesgo individual, calidad asistencial ni explicaciones clínicas.

El bloque **“Qué sabemos / qué no podemos concluir”** cierra el informe con entre tres y cinco conclusiones descriptivas trazables, límites de interpretación y datos faltantes relevantes.

## Geografía y contexto regional

Un dato insular nunca se convierte en municipal. Un dato autonómico nunca se atribuye a una isla o municipio. Espera pediátrica y hospitalización regional aparecen únicamente bajo **“Contexto regional — no atribuible al territorio analizado”**.

La Graciosa conserva `requires_interisland_transfer`: no recibe tiempo de ferry, avión, ambulancia ni tiempo terrestre estimado. Los municipios no reciben prematuridad, mortalidad u otra métrica clínica si el catálogo no declara esa escala.

## Trazabilidad

Cada hallazgo, tabla, gráfico, mapa y sección enlaza a `/trazabilidad/[metric_id]`. Cada hecho mantiene indicador, `source_ids`, periodo, geografía, método, unidad y estado. El cierre enumera solo las fuentes realmente usadas.

## Presentación

Los informes incluyen resumen ejecutivo, índice, dominios disponibles, contexto regional separado, lectura responsable, dominios ausentes, limitaciones y fuentes. La vista es responsive y dispone de HTML imprimible mediante **“Exportar / imprimir informe”**. No se añadió una dependencia PDF.

## Acceso

- perfiles insulares y municipales: **“Generar informe territorial”**;
- Lanzarote: enlace específico al informe de La Graciosa;
- Ask PedsData: preguntas como “Hazme un informe exhaustivo de Gran Canaria”, “Analiza Lanzarote” y “Perfil pediátrico de Telde”.

## QA

- 46 tests unitarios, incluidos planner, lenguaje editorial, comparador insular, geografía, La Graciosa, provenance y parser;
- QA E2E específico de informes: Gran Canaria, Lanzarote, El Hierro, Telde, La Graciosa, 404, contexto regional, provenance por hallazgo, Ask, móvil y print;
- la suite final de publicación se registra en el commit y deployment de beta.2.

## Límites

Los hallazgos son descriptivos. No implican causalidad, riesgo individual ni calidad asistencial. Los dominios sin métrica válida se indican como no atribuibles o se omiten. El informe no sustituye una valoración clínica ni las fuentes oficiales.
