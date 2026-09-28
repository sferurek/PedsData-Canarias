# Auditoría de rendimiento

Medición local previa a RC2:

| Asset | Tamaño |
|---|---:|
| accessibility-grid.geojson | 4,6 MB |
| municipalities.geojson | 1,1 MB |
| facilities.geojson | 36 KB |
| air-stations.geojson | 24 KB |
| weather-stations.geojson | 16 KB |

Las capas nuevas añaden unos 40 KB de geometría puntual. La malla RC1 continúa siendo el cuello de botella. El mapa carga las fuentes una vez y alterna visibilidad, evitando descargas repetidas. No se introducen vector tiles en RC2 porque el incremento de Fase 4 no lo justifica; la migración de la malla a tiles queda como optimización posterior.

`next build` prerenderiza 98 páginas. Playwright valida ausencia de clipping horizontal en desktop e iPhone. La prueba visual cubre home, mapa y las siete islas.
