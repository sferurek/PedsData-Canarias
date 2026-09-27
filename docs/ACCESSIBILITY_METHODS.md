# Métodos de accesibilidad pediátrica

**Estado:** pipeline ejecutado y validado en `staging`; resultados aún no publicados. Gate C está GREEN y Gate B sigue RED, por lo que se habilitan isla, municipio y malla, pero no ZBS. El export curado se reserva para la fase de cálculo/publicación autorizada.

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

Para cada isla y municipio válido se calculan bandas `<5`,
`5–<10`, `10–<15`, `15–<20`, `20–<30`, `>=30`, además de sin ruta y no
evaluable. El denominador publicado separará población total, evaluada, sin
ruta y no evaluable.

Para una banda `b`, `%b = 100 × Σ niños de celdas routed en b / Σ niños del
ámbito`. También se publicará el porcentaje sobre población evaluada para que
la falta de ruta sea visible. Mediana y P90 son cuantiles ponderados por niños,
no por número de celdas; no incluyen estados sin tiempo.

La asignación ZBS está desactivada hasta disponer de límites actuales. Si una
celda cruza un límite, se conservarán pesos espaciales y análisis de
sensibilidad; no se repartirá población de forma silenciosa.

## Celdas pequeñas y publicación

Las celdas pequeñas pueden alimentar cálculos internos agregados, conservando
el valor original y la licencia. La exportación pública no mostrará ubicaciones
o combinaciones que permitan inferencias indebidas; umbral de supresión y
agrupación requieren aprobación metodológica antes de publicar. No se imputan
islas ni años faltantes.

## Ejecución técnica de Fase 2

`etl/prepare_accessibility.py` particiona por isla/componente, usa matrices OSRM de 40 orígenes por 40 destinos y conserva el mínimo por origen. La ejecución local procesó 13.277 celdas y 158 destinos en 706 peticiones, 47,853 s y 149,03 MB de pico, sin fallos ni peticiones a servidores públicos.

Produjo 13.257 celdas `routed` y 20 celdas de La Graciosa `requires_interisland_transfer`, que suman 91 niños y mantienen tiempo/distancia nulos. Los CSV permanecen en `data/staging/`. El manifiesto versionado registra motor, checksum del grafo, lotes, runtime, memoria, fallos y checksum del resultado. El cálculo ZBS figura explícitamente como desactivado.
