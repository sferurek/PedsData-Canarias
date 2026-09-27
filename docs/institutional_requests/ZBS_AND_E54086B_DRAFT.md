# Borrador — solicitud de geometrías, códigos ZBS y E54086B

**No enviado.** Destinatarios propuestos: Servicio Canario de la Salud, ISTAC y SITCAN/GRAFCAN.

Para un observatorio pediátrico público y reproducible de Canarias se solicitan los siguientes datos no identificables:

1. Nomenclátor versionado de Zonas Básicas/Zonas de Salud para las siete islas: código estable, nombre, Área de Salud, fecha de alta/baja y predecesora/sucesora.
2. Geometrías oficiales vigentes e históricas en GeoPackage, GeoJSON o WFS, con CRS, licencia y fecha de referencia.
3. Correspondencia entre ZBS territorial, Equipo de Atención Primaria y unidad funcional SIAP. Se solicita aclaración expresa para Fuerteventura: cuatro territorios SCS 2026 frente a seis unidades SIAP/AP.
4. URL o extracto de E54086B por ZBS, año y siete islas, con diccionario, códigos territoriales, estados de ausencia/supresión y licencia. La API consultada el 27/09/2026 devuelve `currentlyActive=false`, `PLANNING` y cero instancias.
5. Historial de cambios desde 2017, en particular Gran Canaria, Tenerife, Fuerteventura y Lanzarote/La Graciosa.

## Finalidad y minimización

La finalidad es calcular población infantil 0–14, recursos y accesibilidad por ZBS sin inventar límites ni desagregar cifras. Solo se solicitan datos agregados y geometrías administrativas; no se solicita información clínica individual, direcciones de pacientes ni identificadores personales.

## Ausencia en open data comprobada

- IDECanarias Mapa Sanitario publica puntos asistenciales, no polígonos ZBS.
- E54086B no expone instancias en la API.
- El Catálogo AP 2026 aporta nombres, pero no códigos ni geometrías.
- El único shapefile archipelágico localizado es AtlasVPM 2017, histórico, sin licencia declarada y con particiones incompatibles con los recuentos actuales.

Se agradecería indicar también las condiciones de reutilización y cita institucional.
