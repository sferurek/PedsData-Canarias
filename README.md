# PedsData Canarias

**PedsData Canarias — Public Beta** es un observatorio independiente de salud infantil en Canarias basado en datos públicos, metodología reproducible y trazabilidad explícita.

Cubre siempre **El Hierro, La Gomera, La Palma, Tenerife, Gran Canaria, Fuerteventura y Lanzarote**. La aplicación permite explorar accesibilidad pediátrica, evolución temporal, comparación territorial, contexto social y ambiental, resultados sanitarios y utilización asistencial respetando la escala real de cada fuente.

## Principios

- Pediatría y salud perinatal como único foco visible.
- Ninguna isla desaparece por disponibilidad desigual.
- Ningún dato se convierte de regional a insular o municipal.
- `null`, `no_route`, `not_available` y `requires_interisland_transfer` no equivalen a cero.
- Cada número visible enlaza su fuente, periodo, geografía, versión, método y limitaciones.
- Los análisis territoriales son descriptivos; no estiman riesgo individual ni causalidad.

## Ejecutar la aplicación

Requisitos: Node.js 24 y pnpm 11.

```bash
cd apps/web
pnpm install --frozen-lockfile
pnpm dev
```

Validación:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests
cd apps/web
pnpm test
pnpm lint
pnpm typecheck
pnpm build
pnpm test:e2e
```

## Reproducibilidad y fuentes

- [Arquitectura de trazabilidad](docs/DATA_PROVENANCE_ARCHITECTURE.md)
- [Métodos de accesibilidad](docs/ACCESSIBILITY_PUBLICATION_METHODS.md)
- [Catálogo semántico](docs/SEMANTIC_METRICS_CATALOG.md)
- [Catálogo público de fuentes](https://web-sferureks-projects.vercel.app/fuentes)
- [Checklist de beta pública](docs/PUBLIC_BETA_CHECKLIST.md)

Los datasets de terceros conservan sus propias licencias y atribuciones. La aplicación enlaza la fuente oficial exacta desde cada indicador y resultado.

## Límites conocidos

No se publican perfiles por Zona Básica de Salud porque no existe una geometría oficial vigente reutilizable validada para las siete islas. La Graciosa permanece como componente terrestre separado y su acceso figura como transferencia interinsular requerida, sin tiempo clínico inventado. Los datos hospitalarios, encuestas y estaciones ambientales mantienen sus universos y geografías originales.

## Citación

PedsData Canarias. *Observatorio independiente de salud infantil en Canarias*. Versión 0.9.0-beta.2. Consultado el [fecha] en https://web-sferureks-projects.vercel.app. Código: https://github.com/sferurek/PedsData-Canarias.

No existe DOI asignado en esta versión.

## Licencia

El código propio se distribuye bajo licencia [MIT](LICENSE). Esta licencia no cubre ni sustituye las licencias de datos de terceros. Véanse [licencias y atribuciones](docs/DATA_LICENSES.md).
