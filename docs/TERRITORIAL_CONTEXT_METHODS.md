# Contexto territorial y dispersión

## Fuentes y escala

Se utiliza la clasificación oficial [DEGURBA 2021 del ISTAC](https://datos.canarias.es/catalogos/estadisticas/dataset/grado-de-urbanizacion-en-canarias-2021-celdas-base-1-km-de-lado), publicada en WGS84 y basada en la metodología Eurostat adaptada a Canarias. La capa conserva su escala de 1 km. Los puntos representativos de la malla infantil ISTAC 250 m de 2024 se cruzan con sus tres clases: centros urbanos, agrupaciones urbanas y celdas rurales.

`data/curated/territorial_context.csv` incluye los 88 municipios y preserva 255.814 niños 0–14.

## Indicadores

- densidad infantil municipal = población 0–14 / superficie municipal;
- celdas infantiles pobladas;
- niños por celda infantil poblada;
- porcentaje de niños en cada clase DEGURBA.

Los porcentajes municipales son derivados, se marcan `ESTIMATED` y no alteran los datos de origen. No se construye una clasificación propia de ruralidad, un score de dispersión ni una interpolación de DEGURBA a 250 m.
