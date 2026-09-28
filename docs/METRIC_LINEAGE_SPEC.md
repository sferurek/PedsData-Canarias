# Metric lineage specification

Archivo canónico: `data/semantic/metrics_catalog.json`.

Campos obligatorios: `metric_id`, etiqueta, definición, geografía real, inicio/fin temporal, unidad, visualizaciones válidas, permiso y escala cartográfica, método de clasificación, `source_ids`, `method_id`, estado, transformaciones, redondeo, limitaciones y usos.

Una métrica derivada añade `formula.expression` y `formula.inputs[]`; cada input referencia una fuente registrada. Ejemplo: `assigned_children_per_pediatrician = child_population_assigned_0_14 / pediatricians_ap`. No se agregan edades, territorios o periodos incompatibles.

`/indicadores/[metric_id]` documenta la definición. `/trazabilidad/[metric_id]` añade el contexto del resultado concreto mediante parámetros `result`, `period` y `geography`.
