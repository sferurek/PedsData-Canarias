# Resumen ejecutivo — FASE 0, siete islas

27/09/2026 · PedsData Canarias · auditoría documental con pruebas de descarga. No se ha implementado la aplicación.

## Dictamen

**NO-GO para declarar listo o publicar el MVP 0 de accesibilidad en el estado actual.** Es un bloqueo de preparación, no evidencia de inviabilidad del observatorio: faltan catálogo pediátrico geocodificado vigente en las siete islas, geometría/códigos ZBS y validación de routing. No sería honesto usar GO WITH LIMITATIONS mientras recursos y acceso aún no son robustos.

**Viabilidad técnica estimada mediante rúbrica de preparación: 56% (5/9 puntos).** No es probabilidad estadística de éxito, porcentaje de datos disponibles ni de aplicación implementada. Valora nueve dependencias solicitadas por el brief con pesos iguales: 1 = prueba esencial descargada, 0,5 = fuente relevante documentada con limitaciones/pruebas pendientes, 0 = componente técnico no ensayado. Es una valoración de esta auditoría, reproducible y deliberadamente conservadora.

|Dependencia MVP 0|Puntos|Fundamento|
|---|---:|---|
|Población infantil|1|Malla 0–14 completa en siete islas; otras edades pendientes|
|ZBS|0,5|Recuentos y directorios; geometría vigente sin certificar|
|Pediatras AP|1|SIAP 2024 siete islas descargado|
|Recursos pediátricos|0,5|Evidencia parcial de cartera; sin catálogo geocodificado exhaustivo|
|Routing|0|Motores evaluados documentalmente, sin benchmark insular|
|Renta|0,5|ADRH insular documentado, celdas sin descargar|
|Aire|0,5|Estaciones siete islas localizadas, series no auditadas|
|Hospitalización|0,5|EMH disponible provincial; insuficiente para cruces insulares|
|Actividad hospitalaria pediátrica|0,5|Memoria CHUIMI comprobada; resto desigual|

No se compensa un bloqueo crítico con una puntuación alta en otro dominio. El siguiente GO WITH LIMITATIONS exige demostrar recursos/acceso robustos en todas las islas; GO exige además el conjunto de dependencias básicas del brief. Si no se pueden localizar recursos o reutilizar denominadores, permanece NO-GO.

## Hallazgos principales y evidencia

La descarga de malla 2024 contiene 13.277 celdas y siete islas, con población 0–14 informada en todas; 0–17 está vacía. Los CSV SIAP auditados llegan a 2024 y permiten dotación AP insular. E54086B es una operación anual por ZBS documentada, pero no se validó un cubo utilizable. Fuerteventura presenta una discrepancia de recuento entre SIAP y directorio SCS.

EMH pública ISTAC ofrece provincias, no el cruce diagnóstico/edad/isla deseado. Nacimientos, mortalidad, ESC y renta aportan fuentes insulares prometedoras; deben validarse tablas y precisión. Aire tiene estaciones documentadas en siete islas, no cobertura uniforme. La localización de un servicio hospitalario no demuestra el catálogo de centros AP ni su disponibilidad horaria.

Pruebas y cifras en [VALIDATION_REPORT](VALIDATION_REPORT.md); evidencia primaria enlazada en [SOURCES](SOURCES.md). Se distingue descarga completa, comprobación documental y dato pendiente.

## Análisis comparativo y tradeoffs

Una arquitectura con disponibilidad por observación/isla permite ofrecer siete perfiles desde el inicio. Unificar todo a ZBS crearía falsa precisión; limitar todo a Canarias perdería comparaciones reales. Se recomienda conservar cada escala y disponer de vistas comparables solo donde los contratos lo permitan.

ORS es la primera opción de ensayo de routing por matrices/isócronas; OSRM sirve como comparador y Valhalla/GraphHopper como alternativas. Ninguno ha superado aquí pruebas de cobertura canaria. El acceso interinsular a UCIP/UCIN requiere modelo de traslado específico.

## Recomendación y consideraciones de implementación

Avanzar con el paquete de factibilidad del [MVP_PLAN](MVP_PLAN.md), sin iniciar el desarrollo completo. Prioridad: catálogo de recursos, códigos/geometría ZBS, routing y licencias; conservar las siete islas con estados explícitos durante cada paso. Modelo fuente→versión→observación→cobertura y arquitectura documentados. No se ha enviado ninguna solicitud institucional.

## Preguntas abiertas

Disponibilidad real E54086B; vigencia ZBS; cartera/horarios/IDs/coordenadas AP; recursos de alta complejidad y derivación; series hospitalarias comparables; completitud ambiental y precisión de encuestas. Respuestas individuales a las 22 preguntas en [DISCOVERY_QUESTIONS](DISCOVERY_QUESTIONS.md).

Entregables: [matriz insular](ISLAND_COVERAGE_MATRIX.md), [inventario](PEDIATRIC_DATA_INVENTORY.md), [matriz metodológica](PEDIATRIC_DATA_MATRIX.md), [arquitectura](ARCHITECTURE.md), [modelo](DATA_MODEL.md), [gaps](DATA_GAPS.md), [riesgos](RISKS.md), [investigación](RESEARCH_OPPORTUNITIES.md) y [siguiente prompt](NEXT_IMPLEMENTATION_PROMPT.md).
