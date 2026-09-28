# Hospitalización pediátrica — método de publicación

Se admite el cubo oficial ISTAC `E30414A_000009`: residentes canarios dados de alta en cualquier hospital nacional, 2020–2024. El producto combina diagnóstico principal, sexo, edad y año únicamente a nivel Canarias. RC3 conserva los grupos originales `<1`, `1–4` y `5–14`; excluye `15–24` porque incluye adultos.

El diccionario versionado está en `data/reference/pediatric_diagnosis_groups.csv`. Los grupos derivan de códigos agregados publicados por EMH, no de texto libre. `J20–J22` incluye bronquiolitis pero no permite aislarla. Altas son episodios, no pacientes únicos ni incidencia. No se calculan tasas porque RC3 no ha incorporado denominadores etarios alineados por año para este cubo.
