# Especificación de capas cartográficas

Solo puede existir una capa temática principal de color. Centros, estaciones y límites son auxiliares.

Cada capa declara `layer_id`, indicador, geografía real, periodo, unidad, clasificación, escala cromática, fuente, estado y transformaciones. Accesibilidad usa bandas fijas; renta y densidad son municipales; pediatras, frecuentación y prematuridad son insulares; contaminantes son puntos de estación. Una estación nunca colorea una isla completa y un dato regional nunca colorea municipios.

Clasificaciones disponibles: `fixed_thresholds`, `quantile`, `equal_interval`, `jenks` y categórica. La leyenda y la vista de trazabilidad muestran el método. La Graciosa conserva `requires_interisland_transfer` y no entra en `>=30 min`.
