# Catálogo pediátrico geolocalizado

**Corte de verificación:** 27/09/2026  
**Resultado del gate A:** **YELLOW**, con una excepción sin coordenada y ausencia de destino pediátrico confirmado en La Graciosa.

## Resultado

El catálogo curado contiene **168 recursos públicos con U.20 Pediatría registrada en REGCESS**: 159 centros/consultorios de Atención Primaria y 9 hospitales. Las siete islas están presentes. REGCESS/eGeo publica coordenadas para 167 registros; 167 quedan `VERIFIED` y uno `NEEDS_VALIDATION`. Hay 158 destinos AP elegibles para routing.

| Isla | Total | AP con U.20 | Hospitales con U.20 | VERIFIED | PARTIAL | NEEDS_VALIDATION |
|---|---:|---:|---:|---:|---:|---:|
| El Hierro | 3 | 2 | 1 | 3 | 0 | 0 |
| La Gomera | 2 | 1 | 1 | 2 | 0 | 0 |
| La Palma | 5 | 4 | 1 | 5 | 0 | 0 |
| Tenerife | 89 | 87 | 2 | 88 | 0 | 1 |
| Gran Canaria | 47 | 46 | 1 | 47 | 0 | 0 |
| Fuerteventura | 8 | 7 | 1 | 8 | 0 | 0 |
| Lanzarote | 14 | 12 | 2 | 14 | 0 | 0 |
| **Canarias** | **168** | **159** | **9** | **167** | **0** | **1** |

El fichero operativo es [`data/curated/pediatric_facilities.csv`](../data/curated/pediatric_facilities.csv). `routing_eligible_pediatric_ap=true` solo aparece cuando concurren U.20, coordenada oficial y verificación completa.

## Evidencia y reglas de interpretación

1. **REGCESS** se consultó con los filtros Canarias, dependencia pública y U.20 Pediatría. La consulta devolvió 168 centros en cuatro páginas. Las fichas de detalle aportaron coordenadas REGCESS/eGeo y la oferta asistencial registrada.
2. El **Catálogo de Centros de Atención Primaria 2026**, vigente a 31/12/2025, aportó dirección, tipo, Área de Salud y nombre de ZBS para 157 de los 159 recursos AP.
3. El **Catálogo Nacional de Hospitales 2025**, vigente a 31/12/2024, aportó dirección y condición de centro con internamiento para los nueve hospitales.
4. **CartoCiudad** se utilizó como contraste secundario. Cuando discrepa o solo devuelve una aproximación, prevalece el punto oficial REGCESS/eGeo.

Los snapshots raw no se versionan. Sus URL, periodos, fechas de descarga, versión de parser y SHA-256 están en [`pediatric_facility_sources.csv`](../data/curated/pediatric_facility_sources.csv). El ETL reproducible está en `etl/`.

## Cartera hospitalaria confirmada

`U.22` confirma cuidados intermedios neonatales y `U.23` cuidados intensivos neonatales. La consulta permite confirmar UCIN registrada en:

- Complejo Hospitalario Universitario Insular Materno Infantil, Gran Canaria;
- Hospital Universitario de Canarias, Tenerife;
- Hospital Universitario Nuestra Señora de Candelaria, Tenerife.

Existe U.22 sin U.23 registrada en el Hospital General de Fuerteventura, Hospital Nuestra Señora de Guadalupe y Hospital Universitario Dr. José Molina Orosa. La ausencia de U.23 se conserva como `not_available` en esta versión del registro; no se sustituye por una inferencia clínica.

`U.68 Urgencias` por sí sola no demuestra una puerta pediátrica diferenciada. Fuentes SCS adicionales confirman urgencias, ingreso pediátrico, Neonatología, UCIN y UCIP en CHUIMI, HUC y HUNSC; confirman urgencias/ingreso en Fuerteventura y Molina Orosa, e ingreso en La Gomera y La Palma. Los demás estados se conservan como `needs_validation` o `not_available`. U.20 hospitalaria ya no se convierte automáticamente en ingreso pediátrico.

## Excepciones conservadas

- **Consultorio Local Buenavista del Norte:** REGCESS registra U.20 y coordenada; SCS confirmó apertura, consulta de Pediatría y cobertura compartida con Los Silos el 17/07/2025. Queda `VERIFIED` y entra en routing.
- **Consultorio Local de El Sauzal:** REGCESS registra U.20, pero no publica coordenada y su CCN tampoco aparece en el Catálogo AP 2026. Se mantiene `NEEDS_VALIDATION` y no entra en routing.
- **La Graciosa:** SCS confirma consultorio general y pertenencia a Teguise, pero REGCESS no muestra U.20 y la memoria 2023 no desglosa actividad pediátrica propia. No se crea un destino; conserva `requires_interisland_transfer` hacia Lanzarote.
- La denominación ZBS del catálogo AP se conserva en `health_zone_name_source`; `health_zone_id` permanece vacío hasta cerrar el gate B. No se ha fabricado ningún código.

## Limitaciones y decisión

- El registro acredita oferta autorizada, no horarios, presencia diaria, modalidad itinerante ni dotación equivalente a jornada completa.
- El catálogo no interpreta U.68 como urgencia pediátrica diferenciada ni U.37 como UCIP.
- La vigencia puede diferir entre REGCESS en vivo, AP a 31/12/2025 y hospitales a 31/12/2024; cada fila conserva fechas y fuentes.
- Las condiciones formales de reutilización siguen `NEEDS_VALIDATION` en el manifiesto y deben cerrarse antes de publicación externa.

Gate A es **YELLOW**. Hay destinos AP verificados en las siete islas, pero dos
excepciones de Tenerife y la falta de destino U20 verificado en La Graciosa
impiden declararlo completo. Urgencias Pediátricas diferenciadas y UCIP siguen
sin confirmación homogénea y no pueden mostrarse como observadas.
