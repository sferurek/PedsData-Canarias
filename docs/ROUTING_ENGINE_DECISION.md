# Decisión del motor de routing

## Decisión

**Gate C: GREEN.** Se selecciona OSRM 5.27.1 local con MLD y el perfil oficial de automóvil sobre el snapshot OSM Canarias `canary-islands-260926`. La combinación exacta de PBF, imagen y grafo está congelada mediante checksums y puede reconstruirse con los scripts del repositorio.

La decisión cubre accesibilidad terrestre a recursos pediátricos en las siete islas. La Graciosa permanece como componente terrestre independiente. Los traslados entre islas, incluidos UCIP/UCIN, mantienen tiempo desconocido.

## Evidencia de aceptación

- Se reutilizaron sin modificar los 35 casos de Fase 1.
- OSRM local resolvió las 28 rutas terrestres previstas: cuatro por isla.
- Los seis cruces entre componentes y La Graciosa fueron bloqueados antes de la petición; ninguno recibió cero minutos.
- Los 21 trayectos de referencia incluyen urbano, rural y extremo en cada isla.
- Frente a la mediana de OSRM/Valhalla públicos de Fase 1, 10 tiempos quedaron en GREEN y 11 en YELLOW; ninguno superó el límite RED de 35 %. La diferencia temporal mediana fue 20,1 % y la máxima 32,6 %.
- El benchmark completó 28 peticiones locales en menos de un segundo. Es una prueba funcional, no una medida de capacidad sostenida.

## Umbrales y cautelas

Se mantienen los umbrales temporales propuestos: GREEN hasta 20 %, YELLOW por encima de 20 % y hasta 35 %, RED por encima de 35 %. Para snapping se conserva GREEN hasta 50 m. El límite YELLOW es 150 m para puntos representativos de celdas y 200 m para coordenadas oficiales de centros, porque REGCESS/eGeo puede situar un centro en el edificio o parcela y no en la entrada viaria. Ninguna coordenada se desplazó para mejorar el resultado. Los 21 trayectos no tuvieron RED con estos umbrales.

Los contrastes públicos no son ground truth institucional. Antes de publicación se conservarán el caso, el motor, el grafo y la fecha, y se añadirá validación local o institucional cuando exista. El filtro de componente terrestre es obligatorio: consultar OSRM sin ese filtro podría aceptar relaciones ferry presentes en OSM.

Valhalla se mantiene como comparador independiente mediante los resultados congelados de Fase 1. No se incorpora un segundo grafo local a producción porque OSRM ya satisface los criterios y duplicarlo no cambia la trazabilidad del motor elegido.

La reutilización debe atribuir OpenStreetMap y mantener las obligaciones ODbL del extracto. El software OSRM está publicado con licencia BSD-2-Clause; ambas licencias son compatibles con este uso si se conservan atribución y avisos.
