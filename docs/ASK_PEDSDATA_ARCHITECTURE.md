# Arquitectura de Ask PedsData

Ask PedsData es un planificador controlado: pregunta → parser de intención → catálogo de métricas → registro geográfico → reglas de compatibilidad → plan validado → recuperación de datos → cálculo determinista → visual → resumen.

No acepta SQL, código, filesystem ni indicadores no registrados. El intérprete no calcula números. Toda respuesta correcta contiene `source_ids` y enlaza a la trazabilidad del resultado. `TERRITORIAL_REPORT` resuelve el territorio, selecciona métricas compatibles con su escala y enlaza al informe determinista; los datos autonómicos quedan en un bloque regional separado. Los errores son explícitos: `METRIC_NOT_FOUND`, `GEOGRAPHY_NOT_SUPPORTED`, `TIME_RANGE_NOT_AVAILABLE`, `INCOMPATIBLE_METRICS`, `NOT_MAPPABLE` e `INSUFFICIENT_DATA`.
