# Registro de riesgos y mitigaciones

|ID|Riesgo|Impacto / prioridad|Control y prueba de cierre|
|---|---|---|---|
|R01|Desaparición de islas por joins o filtros|Crítico P0|Dimensión canónica + prueba siete IDs en salidas incluso vacías|
|R02|Confundir ficha E54086B con datos disponibles|Alto P0|Exigir URL descargable, filas ZBS y diccionario por siete islas|
|R03|ZBS antiguas/códigos incompatibles|Crítico P0|Versionar y conciliar SCS; caso Fuerteventura seis vs cuatro abierto|
|R04|Cartera o coordenadas incorrectas|Crítico P0|Validación por servicio, entrada física y fecha; excluir de routing destinos no confirmados|
|R05|Ruta por mar o acceso teórico presentado como clínico|Crítico P0|Componentes físicos, ferris desactivados para conducción, traslado separado|
|R06|TIS vs población residente / profesionales vs FTE|Alto P0|Indicadores separados con universos y fechas explícitos|
|R07|Malla 0–14 convertida a 0–17|Alto P0|Bloquear transformaciones sin edad simple o categorías sumables|
|R08|EMH provincial atribuida a islas|Crítico P0|geography_role/level obligatorio; prohibición de desagregar sin fuente|
|R09|Reidentificación/small numbers|Alto P1|Supresión fuente + revisión local/complementaria, ventanas fijas e IC; no reconstrucción por filtros|
|R10|Estación ambiental tomada como exposición insular|Alto P1|Cobertura espacial, contaminantes, calidad y sensibilidad explícitas|
|R11|Sesgo de encuesta y cruces sin potencia|Alto P1|Diseño, errores y grupos originales; no IC ingenuo|
|R12|Memorias PDF y cambios de definiciones|Alto P1|Extracción revisada visualmente, doble control de totales y diccionario por año|
|R13|Licencias heterogéneas y credenciales en Git|Alto P0|Manifiesto por fuente; secretos fuera de repositorio, no PDFs masivos sin revisión|
|R14|URLs/títulos obsoletos y falsa actualidad|Medio P0|Consultar periodos del fichero; ejemplo SIAP 2024 aunque título termina 2023|
|R15|Falta de mantenimiento/recursos de routing|Medio P1|Benchmark, snapshots y presupuestos antes de desplegar|
|R16|Causalidad/ecological fallacy/estigma|Alto P1|Lenguaje descriptivo, dimensiones separadas, límites de interpretación|
|R17|Cambio AEMET de claves|Medio P0 antes de integrar|Revisar S15 y usar credencial vigente; no claves de ejemplos de documentación|
|R18|Datos institucionales no obtenidos|Alto P0|Solicitudes concretas; publicar estado pendiente; no sustituir con cifras generadas|

No se conocen impedimentos globales de reutilización de ISTAC para esta auditoría; otras licencias no están aprobadas por analogía. Dictamen de preparación en [resumen](EXECUTIVE_SUMMARY.md). Referencias S01–S42 en [registro](SOURCES.md).
