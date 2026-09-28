# Seguridad de Ask PedsData

El parser usa alias y patrones cerrados. No concatena SQL, no evalúa código, no accede a archivos y no incorpora instrucciones procedentes de datasets. Todo plan se valida frente a métricas, geografías, periodos y compatibilidad.

Los resúmenes se construyen a partir del resultado numérico ya calculado. Una métrica regional no puede generar un mapa municipal. La ausencia y los estados especiales se conservan; `null` nunca se convierte en cero. La Graciosa no recibe un tiempo terrestre inventado.
