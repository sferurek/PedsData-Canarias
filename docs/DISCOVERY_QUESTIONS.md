# Respuestas a las 22 preguntas del brief

1. **Datasets con siete islas reales:** malla 0–14 2024 y SIAP población/profesionales/recuentos 2004–2024 descargados. Nacimientos, mortalidad, ESC y renta documentan ámbitos insulares; falta auditar todas sus celdas.
2. **Diferencias por isla:** memorias/carteras y densidad de estaciones; pequeñas muestras; malla tiene la misma limitación 0–17 en las siete. Ver DATA_GAPS.
3. **SIAP a nivel ZBS:** E54086B existe como operación; ninguna isla queda certificada con cubo ZBS descargado. TIS ZBS de Gran Canaria localizado en memoria S42 es otra evidencia y otra fuente.
4. **Geometría ZBS archipelágica:** existe alternativa de investigación 2017 S29; no se ha certificado geometría oficial vigente de siete islas.
5. **Población por ZBS:** técnicamente estimable con malla 0–14 y límites válidos; hoy falta validar límites. TIS asignada no equivale a población residente intersectada.
6. **Centros con Pediatría por isla:** evidencias parciales; Valverde/Frontera confirmados documentalmente en El Hierro, hospitales candidatos en todas. Falta directorio AP exhaustivo geocodificado.
7. **Hospital pediátrico por isla:** catálogo de nueve prioritarios en HOSPITAL_COVERAGE; no se presupone cartera de Doctor Negrín ni equivalencia entre centros.
8. **Urgencias diferenciadas:** CHUIMI confirmado con cifras; resto requiere confirmación de cartera y series, no usar urgencias generales.
9. **UCIP:** evidencia Candelaria y CHUIMI; no se demuestra exhaustividad ni ausencia en otras islas.
10. **UCIN:** HUC y Candelaria documentados; completar cartera neonatal CHUIMI y otros centros, vigencia y nivel asistencial.
11. **Memorias útiles:** CHUIMI 2024 verificada y tabla TIS 2023; búsqueda del resto no acredita aún series comparables. No usar memorias de reclamaciones como actividad asistencial.
12. **Hospitalización diagnóstico/edad por isla:** EMH pública ISTAC no lo permite; publica provincias. Se requieren agregados SCS/RAE-CMBD.
13. **Perinatalidad:** nacimientos/gestación/prematuridad/múltiples y MFT por isla en colección S06; no todos los cruces multidimensionales son insulares.
14. **Mortalidad:** edad/sexo y grandes causas a nivel insular; detalle causa/edad menor resolución; IC y ventanas plurianuales.
15. **Encuesta:** ESC 2021 cubre siete islas; comparabilidad por variable con 2009/2015 y precisión de subgrupos pendiente.
16. **Aire:** estaciones S13 en todas; Echedo, Las Galanas/El Calvario/Residencia Escolar, La Grama/El Pilar/San Antonio/Las Balsas, redes de TF/GC, Casa Palacio/Tefía/El Charco, Arrecife/Ciudad Deportiva y entorno Teguise. Lista ilustrativa, no inventario cuantitativo completo.
17. **Meteo:** API AEMET e inventario documentados; cobertura variable×periodo por siete islas pendiente de prueba autenticada.
18. **Renta:** INE ADRH, serie 2015–2023 localizada, incluye islas. Preferir valor insular oficial; no promediar medianas de municipios.
19. **Routing:** ORS primera opción de prueba, OSRM comparador, Valhalla/GraphHopper alternativas. Ninguno certificado aquí para todas las islas.
20. **Small numbers:** mortalidad, diagnósticos raros, UCIP/UCIN, prematuridad en islas pequeñas, encuesta por subgrupos y tasas con pocos eventos/denominadores.
21. **Publicabilidad:** descripción insular de población/dotación AP posible con revisión; acceso siete islas publicable tras cerrar recursos/GIS/routing. Respiratorio ambiental condicionado a resolución clínica.
22. **Solicitudes:** E54086B, límites/códigos ZBS, carteras/horarios/coordenadas, derivaciones, urgencias/CMBD, precisión ESC, ambiente, espera, vacunas y farmacia; wishlist lista sin enviar.

Evidencia, periodos y limitaciones: [fuentes](SOURCES.md), [auditoría](VALIDATION_REPORT.md), [inventario](PEDIATRIC_DATA_INVENTORY.md).
