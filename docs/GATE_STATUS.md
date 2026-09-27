# Estado de gates — Fase 1

Fecha de decisión: 27/09/2026.

|Gate|Estado|Evidencia|
|---|---|---|
|A — catálogo pediátrico|YELLOW|168 recursos U20 públicos, 166 VERIFIED, siete islas; 167 coordenadas oficiales|
|B — ZBS vigente|RED|105 polígonos 2017 válidos pero históricos; 106 nombres AP 2026 sin polígonos/códigos; E54086B sin instancia|
|C — routing|RED|28/28 rutas por motor y siete bloqueos; diferencia temporal mediana 43,4%, máxima 96,6%; sin grafo congelado|
|Base PostGIS|GREEN|Migraciones ejecutadas en PostgreSQL 18/PostGIS 3.6 y 23 pruebas totales|

Catálogo A es usable para QA, pero no está cerrado para publicación: quedan dos
centros de Tenerife, La Graciosa y cartera hospitalaria diferenciada. Gate B
prohíbe perfiles ZBS actuales. Gate C prohíbe publicar minutos.

## Dictamen

**NO-GO.** Dos gates críticos permanecen rojos. No se ha creado el export de
accesibilidad, el mapa ni perfiles con tiempos. Esta omisión aplica el orden
exigido y evita convertir un benchmark en indicadores reales.

Para salir de NO-GO se requieren geometrías/códigos ZBS actuales con vigencia y
un motor sobre grafo congelado, con umbrales de snapping y contraste de tiempos
aceptados. Los casos parciales del catálogo seguirán fuera de routing.
