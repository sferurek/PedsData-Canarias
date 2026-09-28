# Informes territoriales pediátricos

Fecha: 28/09/2026. Estado: **READY FOR REVIEW**.

## Objetivo

`TERRITORIAL_REPORT` convierte una isla, municipio o componente territorial registrado en un informe HTML estructurado. No incorpora datasets, fuentes ni metodologías nuevas. El planner consume exclusivamente `metrics_catalog`, `sources_catalog`, las series ya publicadas y los agregados territoriales validados.

Rutas: `/informes/[geography_id]`. Se generan estáticamente Canarias, las siete islas, La Graciosa y los 88 municipios. Las rutas no registradas devuelven 404.

## Flujo determinista

1. resolver `geography_id` contra el registro territorial;
2. identificar la resolución real (`island`, `municipality`, `grid_250m` o `autonomous_community`);
3. seleccionar métricas registradas compatibles;
4. recuperar observaciones y agregados ya validados;
5. agrupar por dominio;
6. calcular cambios absolutos, relativos y participación en el total de las siete islas cuando la métrica es aditiva;
7. elegir tabla, serie o mapa según el tipo de dato;
8. renderizar únicamente si existen `source_ids`;
9. listar las fuentes efectivamente usadas.

El resumen ejecutivo utiliza reglas de código. Ask PedsData interpreta la intención, pero no calcula ni genera cifras.

## Geografía y contexto regional

Un dato insular nunca se convierte en municipal. Un dato autonómico nunca se atribuye a una isla o municipio. Espera pediátrica y hospitalización regional aparecen únicamente bajo **“Contexto regional — no atribuible al territorio analizado”**.

La Graciosa conserva `requires_interisland_transfer`: no recibe tiempo de ferry, avión, ambulancia ni un tiempo terrestre estimado. Los municipios no reciben prematuridad, mortalidad u otra métrica clínica si el catálogo no declara esa escala.

## Trazabilidad

Cada tabla, gráfico, mapa y sección enlaza mediante **“Fuentes de este resultado”** a `/trazabilidad/[metric_id]`. Cada hecho mantiene indicador, `source_ids`, periodo, geografía, método, unidad y estado. El cierre del informe enumera únicamente las fuentes usadas.

## Presentación

Los informes incluyen resumen ejecutivo, índice, dominios disponibles, contexto regional separado, dominios ausentes, limitaciones y fuentes. La vista es responsive y dispone de CSS de impresión mediante **“Exportar / imprimir informe”**. No se añadió una dependencia PDF.

## Acceso

- perfiles insulares y municipales: CTA **“Generar informe territorial”**;
- Lanzarote: enlace específico al informe de La Graciosa;
- Ask PedsData: preguntas como “Hazme un informe exhaustivo de Gran Canaria”, “Analiza Lanzarote” y “Perfil pediátrico de Telde”.

## QA

- 43 tests unitarios, incluidos planner, geografía, La Graciosa, provenance y parser;
- 19 E2E aprobados y 1 skip esperado en el fichero específico, cubriendo Gran Canaria, Lanzarote, El Hierro, Telde, La Graciosa, territorio inexistente, contexto regional, provenance, Ask, móvil y print;
- build estático: 267 páginas, incluidos 97 informes.

## Límites

Los hallazgos son descriptivos. No implican causalidad ni riesgo individual. Los dominios sin métrica válida se indican como no atribuibles o se omiten. El informe no sustituye una valoración clínica ni las fuentes oficiales.
