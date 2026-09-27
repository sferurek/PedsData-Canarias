# PedsData Canarias

Observatorio Pediátrico de Canarias · **FASE 0 — Pediatric Data & Architecture Discovery** · 27/09/2026.

Cobertura obligatoria: **El Hierro, La Gomera, La Palma, Tenerife, Gran Canaria, Fuerteventura y Lanzarote**. Ninguna isla se elimina por falta de datos. Alcance exclusivamente pediátrico/perinatal; datos generales solo como auxiliares.

Esta versión contiene investigación, contratos y pruebas de fuentes. **No contiene una aplicación ni tiempos de acceso calculados.**

- [Resumen ejecutivo, viabilidad y dictamen](docs/EXECUTIVE_SUMMARY.md)
- [Visión](docs/PROJECT_VISION.md)
- [Inventario pediátrico](docs/PEDIATRIC_DATA_INVENTORY.md)
- [Matriz de variables y metodología](docs/PEDIATRIC_DATA_MATRIX.md)
- [Cobertura de las siete islas](docs/ISLAND_COVERAGE_MATRIX.md)
- [Wish list institucional](docs/PEDIATRIC_DATA_WISHLIST.md)
- [Gaps por isla](docs/DATA_GAPS.md)
- [Arquitectura](docs/ARCHITECTURE.md)
- [Modelo de datos](docs/DATA_MODEL.md)
- [Plan MVP archipelágico](docs/MVP_PLAN.md)
- [Investigación](docs/RESEARCH_OPPORTUNITIES.md)
- [Riesgos](docs/RISKS.md)
- [Hospitales](docs/HOSPITAL_COVERAGE.md)
- [22 preguntas del brief](docs/DISCOVERY_QUESTIONS.md)
- [Fuentes oficiales y primarias](docs/SOURCES.md)
- [Pruebas ejecutadas](docs/VALIDATION_REPORT.md)
- [Licencias y atribución](docs/DATA_LICENSES.md)
- [Prompt recomendado para la siguiente fase](docs/NEXT_IMPLEMENTATION_PROMPT.md)

Dictamen actual: **NO-GO para publicar MVP 0**, con **56% de preparación estimada (5/9)**; no es probabilidad de éxito. Población 0–14 y SIAP insular están comprobados; faltan recursos geocodificados vigentes, geometría ZBS y routing validado. El proyecto conserva cobertura de las siete islas.

Verificación local sin red: `python3 scripts/verify_phase0.py`. Reconsulta opcional de malla: `python3 scripts/recheck_grid.py`.

Fuente de las evidencias tabulares: Instituto Canario de Estadística (ISTAC), descarga 27/09/2026. Véanse periodos, versiones y hashes en el manifiesto. Este proyecto no implica respaldo institucional.
