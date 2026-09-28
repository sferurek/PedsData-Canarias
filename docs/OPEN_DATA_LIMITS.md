# Límites de open data y reutilización
Fecha28/09/2026.

## Conclusión
**A. MUCHO_MAS_POR_EXPLOTAR**

No se ha alcanzado el límite práctico de información pediátrica pública. Sí se aproxima el límite de ciertos cruces muy exigentes: edad×diagnóstico×isla×semana, agendas actuales por centro, dispensación pediátrica territorial y microbiología representativa. La falta de esos cruces no elimina las oportunidades de AP, prevención y adolescencia.

## Reutilización: registro de condiciones
Los códigos siguientes se aplican individualmente a las filas de la matriz. Atribuir siempre organismo, producto, periodo, URL, versión y fecha de consulta. Esta es una evaluación operativa, no asesoría legal definitiva.

| Código | Evidencia y atribución | Restricciones | Redistribución / decisión |
|---|---|---|---|
| I | [Aviso ISTAC](https://www.gobiernodecanarias.org/istac/aviso_legal.html); atribuir ISTAC y productor | Conservar actualización/metadatos, no desnaturalizar ni reidentificar, no sugerir patrocinio; condiciones específicasAPI | Condiciones generales permiten reutilización comercial/no comercial; revisar excepción del producto y reglas API antes de publicar derivados |
| MS | [Aviso Ministerio Sanidad](https://www.sanidad.gob.es/avisoLegal/home.htm); atribuir Ministerio y sistema | Fuente/actualización, integridad del sentido, excepciones terceras; logos/diseño excluidos | Reutilización general prevista salvo indicación contraria; comprobar export y condiciones particulares |
| P | Licencia específica NO VERIFICADA para este recurso; atribuir productor enlazado | Acceso público no equivale a licencia libre; datos sensibles y terceros pueden imponer límites | En esta auditoría solo enlace/resumen. No autorizar redistribución del PDF/archivo completo hasta cerrar licencia; no implica prohibición demostrada |
| CC | Catálogo TITSA/Tenerife indica Creative Commons Attribution; versión no fijada | Atribución, conservar versión y modificaciones; verificar ficha al descargar | Redistribución condicionada a confirmar texto/versión aplicable al recurso concreto |
| CN | CNIG anuncia condiciones compatiblesCCBY4 para productos geográficos | Atribuir CNIG/IGN/productor y edición, conservar aviso de cada descarga | Confirmar licencia de la tesela canaria; no heredar automáticamente la de otro archivo |
| NC | BES/CNE indica CC BY-NC-SA4 en informe revisado | Atribución, no comercial, compartir igual; no extrapolar a todo ISCIII | Revisar compatibilidad con producto/redistribución; mantener enlace si no encaja |

INE, IMSERSO, DGT, Educación, SCS y MITECO quedan P cuando no se cerró licencia del producto, aunque puedan disponer de condiciones generales de reutilización. No se inventa una CC para ellos. La licencia de una página ISCIII no se hereda a las bases de datos que enlaza. El repositorio de PedsData tampoco relicencia contenido tercero.

## Privacidad y semántica
- No extraer nombres de listas de personal; el objetivo son agregados de dotación.
- No reutilizar filas de demanda social como expedientes pediátricos. Errores de edad y granularidad requieren revisión.
- Mortalidad, cribados de enfermedades raras y unidades pequeñas precisan supresión primaria/secundaria y control de diferenciación entre tablas.
- Encuestas: ponderación, n, IC/error y universo; no convertirlas a prevalencia administrativa.
- Dispensación, prescripción y DDD son medidas diferentes; DDD no dosis pediátrica.
- Stock de espera, demora media de resueltos y demora de agenda no son intercambiables.
- No asignar hospital a isla de residencia; no convertir CCAA a siete estimaciones.
- Año de publicación no reemplaza periodo. URI/version CSV no demuestra actualización sustantiva.

## Límites técnicos constatados
Las API ISTAC son el acceso más reproducible de esta auditoría. Dashboards nacionales requieren probar export público y registrar filtros. PDF/tablas imagen requieren extracción doble y revisión clínica. GIS requiere fecha de referencia, CRS y licencia; una ficha de catálogo no acredita cobertura. No se obtuvo un nuevo endpoint de geometría ZBS vigente.

No se declara inexistencia absoluta de fuentes por búsquedas negativas. Se conserva qué se consultó y qué falta en el informe. No se enviaron solicitudes ni se eludieron controles de acceso.
