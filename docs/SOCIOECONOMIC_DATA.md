# Datos socioeconómicos

## Fuente integrada

Se integra el **Atlas de Distribución de Renta de los Hogares (ADRH) 2023** del INE mediante las tablas oficiales [Las Palmas 31151](https://www.ine.es/jaxiT3/Tabla.htm?t=31151) y [Santa Cruz de Tenerife 31187](https://www.ine.es/jaxiT3/Tabla.htm?t=31187). La descarga se realizó desde la API Tempus del INE el 28/09/2026.

`data/curated/socioeconomic_indicators.csv` contiene 264 filas: tres medidas para cada uno de los 88 municipios.

- renta neta media por persona;
- renta neta media por hogar;
- mediana de renta por unidad de consumo.

La geografía es municipal y el periodo es 2023. No se desagrega por edad y no se interpreta como renta o pobreza infantil. RC2 no crea quintiles ni un índice compuesto. En el perfil insular la renta por persona es una media municipal ponderada por población 0–14 para describir el contexto de residencia infantil; no es una estimación individual.

## QA

Los 88 identificadores municipales se emparejan con la geometría oficial usada por RC1. Las unidades y el año son obligatorios. Los valores nulos nunca se convierten en cero.
