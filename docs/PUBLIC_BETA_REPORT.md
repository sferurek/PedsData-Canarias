# Informe de beta pública

Fecha: 28/09/2026. Versión candidata: `v0.9.0-beta.1`.

## Alcance

Consolida Phase 6B y Phase 8 y endurece el producto existente. No se añadieron datasets, dominios clínicos ni funciones de producto. Se preparó una beta pública con identidad independiente, SEO, accesibilidad, páginas legales, licencia, citación, errores, rendimiento, QA de mapa/Ask/provenance y configuración Vercel reproducible.

## Evidencia

- datos: 79 pruebas Python;
- web: 32 unitarias, lint y typecheck;
- build: 170 páginas;
- E2E: 40 aprobadas y 2 skips esperados de viewport;
- Ask PedsData: 30 consultas válidas y errores controlados;
- fuentes: 15/15 URLs oficiales accesibles después de corregir tres enlaces obsoletos;
- Lighthouse móvil final: Performance 97, Accessibility 100, Best Practices 100, SEO 100;
- Lighthouse escritorio: Performance 100, Best Practices 100, SEO 100; accesibilidad 96 antes de las dos correcciones finales confirmadas en móvil.

## Límites visibles

ZBS permanece fuera por falta de geometría oficial vigente. La Graciosa no recibe un tiempo terrestre ficticio. Los análisis territoriales son ecológicos y descriptivos. El producto no sustituye fuentes oficiales ni atención clínica.

## Dictamen

**PUBLIC_BETA_READY**. La suite final, el preview Vercel y el smoke público permanecen verdes. Producción: `https://web-sferureks-projects.vercel.app`; deployment inicial del merge: `56068b372511318bfaed1b3d823ea040b29780c7`. Vercel Authentication protege únicamente previews.
