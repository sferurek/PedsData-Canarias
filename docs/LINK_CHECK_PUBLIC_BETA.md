# Comprobación de enlaces — beta pública

Fecha: 28/09/2026. Script reproducible: `scripts/check_public_links.py`.

Resultado final: **15/15 enlaces oficiales accesibles**. Códigos: 12 respuestas 200 y 3 respuestas parciales 206. INE redirige a la variante con `/` final.

La primera ejecución detectó tres 404. Se actualizaron sin cambiar datos:

- DEGURBA → catálogo oficial de celdas 250 m de 2021;
- malla ISTAC → catálogo oficial de indicadores demográficos 250 m 01/01/2024;
- OSM → página oficial Geofabrik de Canary Islands, que conserva el histórico del snapshot 26/09/2026.

Los enlaces internos críticos se validan en Playwright, incluidos sitemap, robots, aviso, licencias, citar, fuentes, indicadores, islas, municipios y resultados.
