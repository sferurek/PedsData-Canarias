# Informe Fase 4 — RC2

## Resultado

La Fase 4 amplía RC1 con contexto social, territorial y ambiental sin modificar el pipeline de accesibilidad. Se mantienen 13.277 celdas, 255.814 niños, 158 destinos, La Graciosa como transferencia interinsular y la exclusión de ZBS vigentes.

## Entregables

- 264 indicadores de renta para 88 municipios;
- 88 agregados territoriales con clasificación DEGURBA y densidad infantil;
- 51 estaciones de aire y 83.652 observaciones diarias validadas;
- 57 estaciones meteorológicas con observaciones pendientes;
- mapa multicapas, siete perfiles insulares V2, perfiles municipales y Access Gap V2;
- PostGIS ampliado y provenance con checksums.

## Límites decisivos

No se publica pobreza infantil, exposición individual al aire, interpolación ambiental, temperatura sin observaciones ni episodios confirmados de calima. No se introducen datos clínicos ni perfiles ZBS. La asociación entre contexto y acceso es descriptiva.

## QA

- 47 tests Python verdes;
- 11 tests unitarios web verdes;
- lint y typecheck verdes;
- build Next.js con 98 páginas estáticas;
- 14 E2E verdes en desktop/iPhone para las siete islas, capas y perfiles.

## Dictamen

**RC2 READY FOR REVIEW** condicionado a que el preview Vercel reproduzca el build y la navegación validados localmente. Sigue siendo una candidata de revisión, no una release final.

## Preview RC2

- URL: https://web-luttkl7hg-sferureks-projects.vercel.app
- Deployment: `dpl_AcDjJCm3fUnT7VwULLXUhKeL1As5`
- Commit desplegado: `c87cb8151ad1f1726f3488092362bf780a61217f`
- Target Vercel: `preview`
- Estado remoto: `READY`, build de 98 páginas y comprobaciones HTTP 200 en home y capa de aire.

RC1 conserva su deployment anterior. RC2 no se ha promovido a producción.
