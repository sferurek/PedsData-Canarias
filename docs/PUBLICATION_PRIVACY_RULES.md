# Reglas de privacidad y publicación

## Principio

La malla de 250 m se usa íntegra para cálculo interno. La interfaz no muestra el número exacto de niños por celda, aunque el export curado trazable lo conserve para reproducibilidad. El tooltip público muestra banda de tiempo, isla, municipio, recurso y distancia aproximada, nunca el conteo infantil de la celda.

## Municipios

Un perfil municipal es `publishable` cuando concurren:

- geometría municipal válida;
- al menos 100 niños de 0–14 años;
- al menos 5 celdas con población infantil positiva.

Si no se cumplen, el municipio permanece en el dataset con `not_publishable` y motivo explícito. En 2024 son publicables 85 de 88 unidades; Betancuria, Artenara y Agulo permanecen `not_publishable` por población inferior a 100. No se ocultan de los filtros: se muestra el estado y se evita detallar indicadores sensibles.

## Celdas y estados

No se altera ningún cálculo interno ni se imputa población. `requires_interisland_transfer`, `no_route` y `not_evaluated` nunca se convierten en cero minutos. La Graciosa usa un patrón visual propio. Las celdas con cero niños pueden conservar banda espacial, pero no aportan peso y no exponen conteos.

## Revisión

Estos umbrales son una regla conservadora de RC1, no una afirmación jurídica sobre secreto estadístico. Antes de release final deben revisarse con ISTAC/SCS y la gobernanza clínica. Cualquier cambio se versionará y obligará a regenerar el manifiesto de publicación.
