# Informe de implementación — Fase 1

Fecha: 27/09/2026. Repositorio: `sferurek/PedsData-Canarias`.

## Resumen ejecutivo

Se ejecutó P0 en orden: catálogo, ZBS, PostGIS y routing. No se inició la
interfaz. El resultado es **NO-GO**: ZBS vigente y tiempos de routing no tienen
validación suficiente. Accesibilidad y mapa siguen bloqueados, sin datos mock.

Quedan artefactos reproducibles: 168 recursos públicos U20, 105 polígonos
históricos auditados, esquema PostGIS probado y 35 casos de routing en siete
islas con dos motores.

## A — Catálogo pediátrico

REGCESS, Catálogo AP 2026 y CNH 2025 sustentan 168 filas: 166 `VERIFIED`, una
`PARTIAL` y una `NEEDS_VALIDATION`; 167 tienen coordenada oficial. Seis islas
tienen todas sus filas verificadas. Tenerife conserva Buenavista del Norte y El
Sauzal. La Graciosa no tiene destino U20 verificado en su componente.

El catálogo no convierte U68 en Urgencias Pediátricas ni U37 en UCIP. U23
confirma UCIN solo donde está registrada; la falta del código no se interpreta
como ausencia clínica. Gate A: **YELLOW**.

## B — Zonas Básicas de Salud

E54086B figura inactiva, en planificación y sin instancia pública. El WMS del
Mapa Sanitario ofrece puntos, no polígonos ZBS. La única capa localizada es
IACS/AtlasVPM 2017: 105 geometrías válidas, sin duplicados ni solapes mayores de
1 m², pero histórica y sin licencia explícita; queda excluida de routing.

Fuerteventura conserva 4 zonas territoriales 2026, 6 unidades funcionales
AP/SIAP y 5 polígonos 2017. También persisten diferencias en Tenerife, Gran
Canaria y Lanzarote. Gate B: **RED**.

## C — PostGIS

Las migraciones crean fuentes/versiones, siete islas, municipios, áreas, ZBS,
malla infantil, recursos, snapshots y resultados. Las restricciones impiden
routing con recursos no verificados, minutos cero para no-ruta, transferencias
interinsulares con tiempo y valores numéricos para estados no observados.

Se ejecutaron completas en PostgreSQL 18 + PostGIS 3.6. La vista de cobertura
parte de `island` y usa `LEFT JOIN`. Soporte de base: **GREEN**.

## D — Routing

Cada isla aporta urbano, rural, extremo, inverso y no-ruta. OSRM y Valhalla
resolvieron 28/28 rutas terrestres cada uno; los cruces marinos se bloquearon
antes de la petición. ORS quedó no evaluado porque requiere clave.

La diferencia temporal absoluta entre motores tiene mediana 43,4% y máximo
96,6%; snapping OSRM máximo 169,2 m. Los servidores demo no congelan el grafo.
Gate C: **RED**. No se ha elegido motor de producción.

## E–F — Accesibilidad e interfaz

No ejecutadas por regla de gate. `ACCESSIBILITY_METHODS.md` deja fórmulas,
denominadores, cuantiles ponderados y estados preparados. No existe export de
accesibilidad ni aplicación Next.js inicializada. Los directorios web y shared
solo contienen una nota de bloqueo.

## Validación

- 23 pruebas Python pasan: siete islas, null distinto de cero, catálogo,
  geometría histórica, Fuerteventura, routing y La Graciosa.
- Se ejecutaron las cinco migraciones y tres bloques SQL de invariantes en una
  base efímera PostgreSQL 18/PostGIS 3.6.
- Los 28 casos terrestres por motor retornaron HTTP 200; 14 estados marinos se
  resolvieron por preflight sin consulta.
- Hospitalización provincial no se transformó en insular y 0–14 no se convirtió
  en 0–17.

Commits principales: `25e803c` catálogo, `d246d08` ZBS, `4554f50` PostGIS y
`a7d74ce` routing. Los borradores institucionales no se han enviado.

## Entregables y decisión

Se entregan catálogo CSV y documento, capa histórica etiquetada y catálogo ZBS
actual sin geometría inventada, esquema SQL, casos/resultados/manifiesto de
routing, método de accesibilidad, matriz insular, estados de gate, borradores y
siguiente paso.

Faltan tres hechos para continuar: fuente oficial de ZBS vigente, cierre de los
recursos parciales y red local congelada con tiempos contrastados. Con B y C en
rojo, el dictamen obligatorio es **NO-GO**. Las siete islas permanecen visibles
en todos los contratos y ninguna ausencia se codifica como cero.
