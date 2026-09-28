# Especificación UI clínica RC3

La ruta `/resultados` carga el paquete clínico separado del mapa inicial. Hospitalización filtra año, edad y grupo diagnóstico y mantiene la etiqueta “Canarias”. Perinatal muestra las siete islas. Urgencias identifica hospital y evita comparaciones. Mortalidad usa ventana multianual y supresión explícita. Salud infantil muestra la geografía publicada, incluidos grupos de islas.

Estados visibles: `OBSERVED`, `SURVEY_ESTIMATE`, `DERIVED_RATE`, `MULTIYEAR_AGGREGATE`, `PARTIAL`, `NOT_COMPARABLE`, `NOT_AVAILABLE`. Cada módulo expone fuente, periodo, edad, geografía, definición y limitación. Los perfiles municipales indican que los datos clínicos no están disponibles a esa escala.
