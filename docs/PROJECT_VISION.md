# PedsData Canarias — visión y contrato de alcance

FASE 0 · versión documental 0.3 · 27/09/2026.

Observatorio exclusivamente pediátrico y perinatal de El Hierro, La Gomera, La Palma, Tenerife, Gran Canaria, Fuerteventura y Lanzarote. Cada isla permanece visible aunque una variable falte. El repositorio público es la base de fuentes, decisiones, documentación y futuras versiones; esta entrega no contiene una aplicación.

## Pregunta de investigación y contexto

¿Puede sostenerse un observatorio comparable de las siete islas con datos públicos, sin inventar resolución, edades, actualidad ni cobertura asistencial? El criterio de éxito combina cobertura territorial, denominadores fiables, recursos verificables y reproducibilidad.

El usuario exige siete unidades insulares desde MVP 0, no un piloto capitalino. La población de La Graciosa y otros territorios incluidos en las unidades estadísticas oficiales no se elimina: conservar su geografía física y adscripción original (S25). Siete perfiles no autorizan rutas terrestres a través del mar.

## Principios de producto

1. Relevancia pediátrica en toda pantalla: recién nacidos, infancia, adolescencia y perinatalidad.
2. Fuente, periodo, edad original, metodología, incertidumbre y completitud accesibles en cada indicador.
3. Canarias/provincia/isla/municipio/ZBS son niveles diferentes. No repartir valores agregados.
4. Falta de dato no es cero; falta de publicación no demuestra ausencia de servicio.
5. Datos auxiliares de adultos, renta, carreteras y ambiente sirven a preguntas pediátricas, sin módulos adultos independientes.
6. El análisis de acceso muestra dimensiones separadas; ningún score opaco ni ranking simplista.
7. Un diagnóstico atendido no equivale a incidencia poblacional y asociación ecológica no equivale a causalidad.

## Experiencia prevista, no implementada

Home de Canarias con siete islas, selector Canarias/isla, mapa pediátrico, siete perfiles insulares, perfiles ZBS y hospitales, tabla accesible y panel «Fuente y metodología». Las tarjetas de urgencias, hospitalización, prematuridad y ambiente muestran el nivel territorial real y estado de disponibilidad, incluso sin cifra.

Rutas de producto: población → recursos AP → acceso → actividad → salud → contexto ambiental/social. Se preservan todos los dominios del brief en inventario y wishlist aunque no sean publicables en el primer MVP.

## Límites de esta fase

Se han auditado catálogos, documentación y ficheros de población/SIAP. Se propone arquitectura y método. No se han construido mapas de producto, perfiles interactivos, ETL productivo ni calculado tiempos de acceso. MVP 0 es la siguiente etapa, no un entregable funcional de FASE 0.

La configuración de modelos indicada por el usuario se conserva como preferencia: Astra Medium para descubrimiento; Sol Medium para implementación y escalado según dificultad. Este repositorio no cambia configuraciones de cuenta ni afirma haberlas modificado.

Referencias: [registro](SOURCES.md), [dictamen](EXECUTIVE_SUMMARY.md), [plan](MVP_PLAN.md).
