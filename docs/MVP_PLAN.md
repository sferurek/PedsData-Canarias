# Plan MVP archipelágico

FASE 0 entrega documentación y pruebas de fuente. No desarrolla aplicación. Todos los MVP conservan siete islas y estados de disponibilidad.

## Gate previo: paquete de factibilidad

1. Congelar población 0–14 2024 y SIAP 2024; conciliar totales, universo, edad, licencia y versiones.
2. Obtener catálogo pediátrico geocodificado completo y vigente en siete islas; confirmar horarios, edad y rutas de referencia.
3. Resolver ZBS: E54086B, geometría y conflicto de Fuerteventura. Si no hay polígonos fiables, mantener perfiles con estado pendiente; no afirmar que se ha cumplido MVP 0 ZBS.
4. Probar un motor de rutas en siete islas, red dirigida y componentes no conectados; conservar errores y población no evaluable.
5. Descargar renta y ambiente con cobertura trazable; hospitalización solo en su resolución real.
6. Revisión del gate: GO si todas las dependencias básicas están verificadas; GO WITH LIMITATIONS si acceso robusto siete islas y actividad desigual; NO-GO de publicación si no se cumplen dependencias críticas.

## MVP 0 — factibilidad archipelágica (siguiente fase autorizable)

Mapa completo, siete perfiles permanentes, catálogo de recursos, accesibilidad básica y provenance. Una ZBS de ensayo por isla como mínimo, sin excluir las demás del diseño ni de la cobertura prevista.

|Isla|ZBS candidata de ensayo|Motivo / condición|
|---|---|---|
|El Hierro|Frontera-Valle del Golfo|Zona especial, ruralidad y orografía; S27|
|La Gomera|San Sebastián|Enlace con hospital insular; S26|
|La Palma|Santa Cruz de La Palma|Límite descrito que cruza entidades municipales; S28|
|Tenerife|La Cuesta (candidata)|Contraste urbano/derivación; confirmar código y polígono SCS|
|Gran Canaria|Canalejas|Tabla TIS ZBS localizada S42; confirmar versión y cartera|
|Fuerteventura|Puerto del Rosario|Probar distinción ZBS/equipos; conflicto S24|
|Lanzarote|Teguise|Incluye La Graciosa según S25; imprescindible caso sin ruta terrestre|

Selección intencional para pruebas, no muestra estadísticamente representativa de todas las ZBS. Nombres candidatos no son IDs oficiales ni geometrías aprobadas.

## Criterios de aceptación MVP 0

- Home y comparación devuelven exactamente las siete unidades, incluso con fuente caída o cero filas.
- 0–14 malla y SIAP cargados con licencia, edad, periodo y checksum; no presentar sumas de malla como censo oficial sin conciliación.
- Recursos incluyen cada campo exigido y evidencia de servicio; coordenadas no verificadas no alimentan rutas.
- Un ensayo por isla con origen, destino, grafo, perfil, tiempos y revisión; no usar tiempo de otra isla.
- Geometrías ZBS con vigencia, topología y correspondencia aprobadas; conflicto documentado hasta resolver.
- Mediana/P90 y porcentajes ponderados por niños, con denominador evaluado, desconocido y sin ruta publicados.
- Tablas de hospitalización provincial conservan ese nivel y muestran limitación en los perfiles insulares.
- Auditoría de extracción de memorias: total=ingresados+ambulatorios si definición compatible; tasas se recalculan con tolerancia de redondeo.
- Sin score agregado ni causalidad; accesibilidad es modelo de desplazamiento, no disponibilidad efectiva de cita.

## MVP 1 — Canarias pediátrica

Mapa, filtros, población, AP, ratios, accesibilidad, recursos, ambiente, renta, hospitalización al nivel real y urgencias disponibles. El alcance clínico desigual se expresa por variable; no como retirada de una isla. Perfiles ZBS y hospitales se abren solo con evidencia suficiente, pero sus estados siguen visibles.

## MVP 2 — profundización

ESC, perinatalidad, mortalidad, salud mental, accidentes, historia hospitalaria y validación de edades/errores. Ninguna ampliación introduce módulos generales adultos.

## MVP 3 — investigación

Exportaciones con protección de pequeños números, scripts reproducibles, figuras/tablas, diccionario y métodos para comunicaciones/artículos. Preespecificar análisis, revisión epidemiológica y permisos de datos si cambian las fuentes.

## Secuencia y estimación

Priorizar dependencias, no prometer fecha sin respuesta institucional. Trabajo local de implementación puede comenzar por contratos, validaciones y estados; mapas de accesibilidad comparables dependen del catálogo y routing. No saltar gates para producir un dashboard aparentemente completo. [Prompt recomendado](NEXT_IMPLEMENTATION_PROMPT.md).
