# Informe de Fase 2

**Fecha:** 27/09/2026  
**Base:** `main` en `874e459`  
**Dictamen:** **GO WITH LIMITATIONS — SIN ZBS**

## Resultado ejecutivo

Gate C pasa de RED a GREEN: el proyecto dispone de OSRM 5.27.1 local, extracto OSM fechado, imagen fijada por digest, grafo con checksum y barrera de componentes terrestres. Los 35 casos de Fase 1 se repitieron sin cambiar la muestra; las 28 rutas terrestres resolvieron y los siete casos bloqueados no llegaron al motor. Los 21 trayectos urbano/rural/extremo no tuvieron diferencias RED frente al contraste disponible.

Gate A sigue YELLOW justificado. Buenavista queda verificado y elegible; El Sauzal confirma Pediatría pero carece de coordenada oficial; La Graciosa no tiene destino U20 confirmado. La asignación automática de ingreso pediátrico a todo hospital U20 fue eliminada y la cartera diferenciada se actualizó solo con fuentes SCS.

Gate B sigue RED. E54086B está inactiva, en planificación y sin instancias. El servicio geográfico sanitario no publica polígonos ZBS ni habilita WFS. Las 105 geometrías de 2017 permanecen históricas y no routeables. Por ello se adopta formalmente isla/municipio/malla/recurso y se excluyen perfiles ZBS.

## Routing reproducible

- Snapshot: `canary-islands-260926`, datos OSM hasta 26/09/2026, SHA-256 `2c5f0f3c7b42fc68f6d1bf64679642edb86f546fe510e6f081a07a4d398379f9`.
- Motor: OSRM 5.27.1, MLD, `car.lua`, imagen GHCR fijada por digest.
- Grafo: 26 archivos, 116.750.248 bytes, checksum `f0b0700b3224c76f6b62682102cbf2002936164d1de7bb28d8820af81578a37e`.
- QA: 28/28 rutas terrestres; 10 referencias GREEN y 11 YELLOW en tiempo; ninguna RED.
- La Graciosa y cualquier cruce marítimo se bloquean antes de OSRM. UCIP/UCIN interinsular no recibe minutos terrestres ficticios.

## Preparación de accesibilidad

El pipeline de matrices se ejecutó como validación técnica, sin publicar export curado: 13.277 celdas, 158 destinos, lotes 40×40, 706 peticiones locales, 47,853 segundos, 149,03 MB y cero fallos. Conservó 13.257 celdas `routed` y 20 de La Graciosa como `requires_interisland_transfer`; estas últimas representan 91 niños y tiempo/distancia nulos.

Los agregados de staging cubren siete islas y municipios, ponderan por niños y no por celdas, y excluyen ZBS. Los resultados se mantienen en `data/staging/`; el manifiesto reproducible sí se versiona.

## Alcance y siguiente decisión

No se construyó UI. La siguiente fase puede autorizar el export curado, revisión estadística de agregados, mapa y perfiles insulares/municipales. Los perfiles ZBS continúan prohibidos hasta disponer de fuente oficial vigente. Los borradores institucionales están listos y no se enviaron.
