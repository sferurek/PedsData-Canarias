# Fase 6 — RC4

Base: main remoto `1b08252`, verificado antes de empezar. Fecha: 28/09/2026.

## Dictamen
**RC4 READY FOR REVIEW** — alcance admitido: utilización SIAP, stock regional de espera y adolescencia HBSC. No significa admisión de todos los candidatos.

## Datos
- SIAP: 1.134 observaciones, siete islas, 2007–2024; consultas, personas y frecuentación. Totales 7 × 18 por indicador; 178 ausencias conservadas.
- Espera: 90 registros regionales de 2017–2025. Pediatría/Cirugía Pediátrica en consultas; Cirugía Pediátrica en quirúrgica. Stock, no demora. Publicación insular HOLD.
- HBSC: 20 estimaciones publicadas, cuatro indicadores y cinco grupos/total. Canarias 2022, escolarizados de 11–18 años, n por ítem y ponderación; sin IC sintéticos.
- BDCAP, SIVAMIN, cribados, ESdE/ESTUDES y enriquecimiento hospitalario: HOLD documentado. Atención temprana: RESEARCH_ONLY. Sin solicitudes enviadas.

## Aplicación
Rutas /utilizacion, /adolescencia y /prevencion. Prevención explica HOLD sin cifras. Filtros de isla/año/indicador/lugar, stock por corte/lista y encuestas independientes. Research V2 permite pediatras frente a consultas o usuarios en la misma isla/año. Accesibilidad, espera y renta no se cruzan automáticamente por incompatibilidad temporal, de universo o geografía. El cuadrado asistencial mantiene dimensiones separadas.

No cambia ningún dataset de RC3 ni activa ZBS. Se conservan La Graciosa, privacidad, mapa y perfiles. Navegación móvil corregida; sin rediseño global. Footer y badge RC4; el historial clínico RC3 mantiene su etiqueta de origen.

## QA ejecutada
- 61 tests Python correctos, incluidos ocho nuevos.
- 15 tests unitarios web correctos.
- Lint y TypeScript correctos.
- Build Next 16.3.6: 102 páginas.
- E2E local y contra el preview: 23 correctos, uno omitido intencionadamente (test móvil en proyecto desktop).
- Capturas desktop/iPhone de utilización/adolescencia revisadas; sin desbordamiento horizontal de página. Tablas con desplazamiento interno.
- Esquema sql/008_phase6_utilization.sql ejecutado en PostgreSQL 15 efímero aislado, sin conexiones a las bases existentes. Esquema phase6 independiente: no presupone migración completa de los esquemas de fases anteriores.
- CSV generados con LF; git diff --check correcto.

## Reproducibilidad y rendimiento
Ejecutar `.venv/bin/python etl/build_phase6.py` y después `.venv/bin/python etl/build_phase6_web.py`. Se requiere pypdf. Entradas oficiales congeladas, versiones/checksums/licencias en phase6_sources.json; salidas curated en phase6_manifest.json. No descargas implícitas ni latest durante curación.

Payloads específicos de ruta: utilización 158.325 bytes, adolescencia 22.674 bytes sin comprimir. Home no importa históricos nuevos. La dotación reutiliza el snapshot de Fase 0 con checksum y etiqueta de población asignada.

## Incidencias resueltas y límites
- CSV CRLF producía avisos diff; normalizados los generados, fuentes preservadas.
- Navegación móvil oculta y footer RC3 residual: corregidos y verificados.
- Frecuentación tiene isPercentage=true en metadatos pero definición de razón; se conserva la razón sin multiplicar por 100.
- Espera territorial ambigua: salida exclusivamente Canarias.
- SIVAMIN no aportó export canario validable; no se usa el resumen estatal como dato regional.
- HBSC cita 2025 y NIPO 2026: ambas referencias documentadas, periodo 2022.
- Ausencia de IC/edad individual explícita; sin causalidad, rankings ni productividad individual.
- La primera ejecución E2E remota sin sesión encontró el login de Vercel. Se repitió con cookie temporal obtenida mediante el mecanismo oficial de bypass autenticado de Vercel CLI: 23 pruebas correctas. No se modificó Deployment Protection. Credenciales fuera del repositorio.

## Despliegue
- [Preview RC4](https://web-lcbrffz12-sferureks-projects.vercel.app), protegido por autenticación Vercel.
- Deployment: `dpl_FtBxVPwQE2uzMJszKTBw5UVtMUDn`.
- Commit de aplicación desplegado: `144dc84d9932b00f7f54220441fe5c1f90815dd7`. El commit posterior de documentación no altera el build.
- Vercel inspect: target preview, estado Ready. Build remoto correcto.
- [Inspector del deployment](https://vercel.com/sferureks-projects/web/FtBxVPwQE2uzMJszKTBw5UVtMUDn).
- RC3 conservada: https://web-dy4ml0fr9-sferureks-projects.vercel.app.
- No promoción a producción, cambio de dominio ni desactivación de protección. RC4 es una candidata para revisión, no release final.
