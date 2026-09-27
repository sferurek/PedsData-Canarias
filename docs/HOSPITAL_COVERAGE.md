# Cobertura por hospital — catálogo de descubrimiento

No es un directorio asistencial operativo. «Pendiente» no equivale a «no existe». Faltan IDs oficiales, coordenadas/entrada, horarios y fecha de cartera vigente para convertir candidatos en destinos de routing. No se inventan esos campos.

|Hospital / isla|Pediatría y evidencia|Urgencias diferenciadas / actividad|UCIP|UCIN / Neonatología|Memoria / acción|
|---|---|---|---|---|---|
|CHUIMI — Gran Canaria|S18/S21|Confirmadas; 2023/2024 en S18|Evidencia S21|Confirmar cartera exacta vigente; unidad neonatal documentada en fuentes SCS|Memoria 2024 útil localizada; separar centros y residencia|
|Doctor Negrín — Gran Canaria|No asumir cartera pediátrica equivalente a CHUIMI|Pendiente|Pendiente|Pendiente|Solicitar cartera y actividad pediátrica real; no usar totales adultos|
|HUC — Tenerife|S20 evidencia neonatal|Serie de urgencias pendiente|Pendiente en esta auditoría|UCIN documentada en 2025 S20|Localizar memoria comparable y límites de edad|
|Candelaria — Tenerife|S19/S21|Evidencia de cuidados pediátricos; serie urgente pendiente|Documentada, vigencia/capacidad por verificar|UCIN documentada históricamente|Actualizar memoria, cartera y derivaciones|
|Hospital General/Universitario de La Palma — La Palma|S40 evidencia histórica|Pendiente|Pendiente|Pendiente|Solicitar memoria y cartera vigentes|
|Doctor José Molina Orosa — Lanzarote|S39|No inferir pediátricas desde urgencias generales|Pendiente|Pendiente|Confirmar servicio diferenciado, serie y neonatología|
|Hospital General de Fuerteventura — Fuerteventura|S38|No inferir pediátricas desde urgencias generales|Pendiente|Pendiente|Solicitar serie y cartera específica|
|Nuestra Señora de Guadalupe — La Gomera|Cartera S22 confirma Pediatría|Pendiente|Pendiente|Pendiente|Solicitar actividad, estabilización y derivación|
|Insular Nuestra Señora de los Reyes — El Hierro|Cartera S23 confirma Pediatría|Pendiente|Pendiente|Pendiente|Solicitar actividad y cobertura horaria|

Hospital del Sur (Tenerife) y demás recursos relevantes deben añadirse al catálogo si su cartera pediátrica se verifica; esta lista prioritaria no declara exhaustividad. Recursos privados se identificarán por titularidad y condiciones de acceso, sin suponer acceso universal.

## Ejemplo de validación de actividad localizada

CHUIMI 2024 publica 45.002 urgencias pediátricas, 1.973 ingresadas y 43.029 ambulatorias: las dos categorías suman el total; 1.973 / 45.002 ×100 = 4,38% redondeado. Es actividad de hospital, no tasa de urgencias de niños residentes en Gran Canaria. Se requiere revisar definición etaria y traslado antes de comparar hospitales. [S18](SOURCES.md#s18--chuimi-memoria-2024).

## Esquema requerido para futura ficha

`id_oficial, autoridad_id, nombre, tipo, island_id, municipality_id, health_zone_id, health_area_id, lat, lon, servicios_confirmados, estado_servicio, fuente_url, source_date, last_verified_at, horario, edad_atendida, precision_coordenadas, referral_destination`.

Un campo desconocido es null y bloquea solo las operaciones que dependen de él. No bloquea que la isla figure en perfiles o matrices. [Fuentes](SOURCES.md).
