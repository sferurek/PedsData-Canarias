# Meteorología

## Auditoría

El [Sistema de Observación Meteorológica de Canarias de SITCAN](https://opendata.sitcan.es/dataset/sistema-de-observacion-meteorologica-de-canarias) publica un inventario diario de estaciones y un archivo histórico. Su API SensorThings requiere una api-key gratuita. El archivo completo observado en la auditoría supera 1,5 GB y no ofrece una distribución reciente acotada adecuada para RC2.

Se integra `weather_stations.csv` con 57 estaciones geolocalizadas y cobertura de las siete islas. `weather_observations.csv` queda vacío y su estado en provenance es `NOT_AVAILABLE_API_KEY_REQUIRED`. Temperatura aparece deshabilitada en el selector con la etiqueta “pendiente”; no se muestran valores simulados ni desactualizados.

Una fase posterior podrá ingerir temperatura, humedad, viento y precipitación tras obtener una clave y fijar una ventana temporal reproducible.
