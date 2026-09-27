# Estado de gates — Fase 2

Fecha de decisión: 27/09/2026.

| Gate | Estado | Evidencia |
|---|---|---|
| A — catálogo pediátrico | YELLOW | 168 recursos U20; 167 VERIFIED; 158 destinos AP elegibles; El Sauzal sin coordenada oficial y La Graciosa sin destino U20 confirmado |
| B — ZBS vigente | RED | E54086B inactiva/PLANNING con cero instancias; WMS sin polígonos y WFS deshabilitado; 105 polígonos 2017 solo históricos |
| C — routing | GREEN | OSRM 5.27.1 local, grafo/checksum congelados, 28/28 rutas, 21 referencias sin RED y guardas marítimas |
| Pipeline de accesibilidad | GREEN técnico | 13.277 celdas, 158 destinos, 706 matrices, 0 fallos; salidas solo staging |
| Base PostGIS | GREEN | PostgreSQL 18/PostGIS 3.6 y esquema de Fase 1 conservados |

## Dictamen

**GO WITH LIMITATIONS — SIN ZBS**

Routing y destinos permiten accesibilidad por malla, isla y municipio en las siete islas. Gate B no se rebaja: no se publicarán perfiles ni agregados ZBS. La Graciosa mantiene `requires_interisland_transfer` y 91 niños no evaluables por carretera a un destino U20; UCIP/UCIN interinsular conserva tiempo desconocido.
