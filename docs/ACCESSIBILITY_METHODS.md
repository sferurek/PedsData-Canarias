# Métodos de accesibilidad pediátrica

**Estado:** especificación preparada; cálculo bloqueado. No existe
`pediatric_accessibility_2024.csv` porque ZBS actual y routing no han superado
sus gates. Un fichero vacío aparentaría una medición real.

## Universo

- Origen: malla ISTAC 250 m, `poblacion_00a14`, 01/01/2024.
- Peso: niños observados de la celda, nunca su superficie.
- Punto: `representative_point` interior; requiere análisis de sensibilidad.
- Destino: recurso `VERIFIED`, Pediatría AP observada y apto para routing.
- Red: snapshot local con motor, perfil, fecha y checksum.

Las celdas con cero niños son observaciones válidas, pero no alteran los
agregados. Un nulo, suprimido o no evaluable nunca se transforma en cero.

## Estados y topología

Cada par origen–destino termina en `routed`, `no_route`, `not_evaluated` o
`requires_interisland_transfer`. Solo `routed` admite segundos y metros. El
preflight exige el mismo componente terrestre antes de consultar la red.

La Graciosa conserva su población bajo Lanzarote y un componente propio. La
ausencia actual de destino U20 verificado implica transferencia con tiempo
desconocido. UCIP/UCIN fuera de la isla sigue la misma regla: no se suman coche,
ferry, avión y ambulancia como si fueran una ruta terrestre.

## Agregación

Para cada isla, municipio válido y ZBS vigente se calcularán bandas `<5`,
`5–<10`, `10–<15`, `15–<20`, `20–<30`, `>=30`, además de sin ruta y no
evaluable. El denominador publicado separará población total, evaluada, sin
ruta y no evaluable.

Para una banda `b`, `%b = 100 × Σ niños de celdas routed en b / Σ niños del
ámbito`. También se publicará el porcentaje sobre población evaluada para que
la falta de ruta sea visible. Mediana y P90 son cuantiles ponderados por niños,
no por número de celdas; no incluyen estados sin tiempo.

La asignación ZBS no se ejecutará hasta disponer de límites actuales. Si una
celda cruza un límite, se conservarán pesos espaciales y análisis de
sensibilidad; no se repartirá población de forma silenciosa.

## Celdas pequeñas y publicación

Las celdas pequeñas pueden alimentar cálculos internos agregados, conservando
el valor original y la licencia. La exportación pública no mostrará ubicaciones
o combinaciones que permitan inferencias indebidas; umbral de supresión y
agrupación requieren aprobación metodológica antes de publicar. No se imputan
islas ni años faltantes.

El cálculo podrá comenzar cuando ZBS tenga versión actual utilizable y el motor
use un grafo local congelado con discrepancias y snapping aceptados. Hasta ese
momento, cualquier tiempo permanece `not_evaluated`.
