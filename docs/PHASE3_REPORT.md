# Informe de Fase 3 — RC1 de accesibilidad pediátrica

Fecha: 27/09/2026. Base: `main` en `c0e6059`.

## Dictamen

**RC1 READY FOR REVIEW**

La primera versión navegable cubre las siete islas con accesibilidad geográfica potencial a Pediatría de Atención Primaria. Los datos pasaron QA antes de promoverse a `data/curated/`. Gate B permanece RED: la RC1 no incluye filtros, perfiles ni agregados ZBS.

## Revisión y promoción

La reproducción fijada de `etl/prepare_accessibility.py` confirmó el snapshot OSM, OSRM 5.27.1, el catálogo de Fase 2 y la malla ISTAC 0–14 de 2024. El QA detectó una coincidencia de snapping con 0 segundos y 0 metros en Agaete. Se clasificó como `not_evaluated`; no se inventó un mínimo ni un destino alternativo.

Resultado publicable:

- 13.277 celdas preservadas, sin duplicados;
- 13.256 `routed`;
- 20 `requires_interisland_transfer`, todas en La Graciosa;
- 1 `not_evaluated`;
- 0 `no_route` y 0 fallos de motor;
- 255.814 niños preservados;
- 158 destinos AP VERIFIED elegibles;
- 7 agregados insulares y 88 municipales;
- 85 municipios publicables y 3 restringidos por regla conservadora de small numbers.

## Producto RC1

La aplicación Next.js ofrece mapa de bandas discretas, filtros por isla y municipio, siete perfiles insulares, perfiles municipales con control de publicación, tabla descriptiva Pediatric Access Gap, separación entre centros y profesionales SIAP y panel reutilizable de fuente y método. La Graciosa usa el estado de transferencia interinsular; no recibe tiempo terrestre. No existen rutas ZBS en la aplicación.

## Verificación

- suite Python completa: ver registro final de pruebas;
- typecheck y ESLint: sin errores;
- tests de componentes: 10;
- tests de navegador: 10 en desktop e iPhone;
- build Next.js: 98 páginas estáticas;
- revisión visual: Canarias, siete mapas insulares, desktop e iPhone, leyenda, filtros y ausencia de clipping horizontal.

La RC1 sigue requiriendo revisión clínica, metodológica y visual externa antes de considerarse release final.

## Preview

La RC1 se despliega en Vercel como **preview protegido**, sin promoción a release final. El proyecto conserva Vercel Authentication; las pruebas automatizadas usan Protection Bypass temporal y no desactivan la protección.

El build remoto ejecuta `pnpm install` y `pnpm build`, genera 98 páginas estáticas y mantiene la etiqueta visible `RC1 · revisión`. La URL y el commit verificados se registran en el cierre de despliegue.
