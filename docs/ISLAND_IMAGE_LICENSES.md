# Fotografías territoriales: selección y licencias

Fecha de auditoría: 2026-09-29  
Registro estructurado: `data/visual/island_hero_images.json`

## Criterio de admisión

Solo se admitieron archivos con autoría identificada, página de origen directa y licencia **CC BY, CC BY-SA, CC0 o dominio público** verificable en Wikimedia Commons. La selección se hizo después de comparar entre dos y cuatro imágenes horizontales por territorio. No se utilizó una imagen por el mero hecho de aparecer en una búsqueda.

Se priorizaron paisajes reconocibles, encuadre adaptable a tarjetas y cabeceras, ausencia de personas identificables y evaluaciones Featured picture/Quality image. Las categorías exactas de Featured pictures no devolvieron candidatos para El Hierro ni La Graciosa; en esos dos casos se seleccionaron alternativas con autoría y licencia individual verificadas.

## Selección final

| Territorio | Obra | Autoría | Licencia | Evaluación Commons | Fuente |
|---|---|---|---|---|---|
| Gran Canaria | Roque Nublo - Barranco de Tejeda | H. Zell | CC BY 3.0 | Featured picture | [Commons](https://commons.wikimedia.org/wiki/File:Roque_Nublo_-_Barranco_de_Tejeda.JPG) |
| Tenerife | Roque Cinchado und Teide | Thomas Wolf · www.foto-tw.de | CC BY-SA 3.0 DE | Featured picture | [Commons](https://commons.wikimedia.org/wiki/File:Roque_Cinchado_und_Teide.jpg) |
| Lanzarote | Timanfaya - Lanzarote - Illas Canarias - Spain | Luis Miguel Bugallo Sánchez (Lmbuga) | CC BY-SA 3.0 | Featured picture · Quality image | [Commons](https://commons.wikimedia.org/wiki/File:Timanfaya-_Lanzarote-_Illas_Canarias-_Spain-T20.jpg) |
| Fuerteventura | View from Pico de la Zarza 07 | H. Zell | CC BY-SA 3.0 | Featured picture | [Commons](https://commons.wikimedia.org/wiki/File:View_from_Pico_de_la_Zarza_07.jpg) |
| La Palma | San Antonio volcano - Panorama 03 | Llez | CC BY-SA 3.0 | Featured picture | [Commons](https://commons.wikimedia.org/wiki/File:San_Antonio_volcano_-_Panorama_03.jpg) |
| La Gomera | Bosque Encantado, Parque nacional de Garajonay | Diego Delso | CC BY-SA 3.0 | Featured picture | [Commons](https://commons.wikimedia.org/wiki/File:Bosque_Encantado,_Parque_nacional_de_Garajonay,_La_Gomera,_Espa%C3%B1a,_2012-12-14,_DD_19.jpg) |
| El Hierro | Sabinar de El Hierro | Desde un tajinaste | CC BY 4.0 | Licencia y atribución verificadas | [Commons](https://commons.wikimedia.org/wiki/File:Sabinar_de_El_Hierro.jpg) |
| La Graciosa | Montaña Amarilla y Playa Cocina | Artsuaga | CC BY-SA 3.0 | Licencia y atribución verificadas | [Commons](https://commons.wikimedia.org/wiki/File:Monta%C3%B1a_Amarilla_y_Playa_Cocina.jpg) |

## Alternativas comparadas

- Gran Canaria: Dunas de Maspalomas frente a Roque Nublo.
- Tenerife: Teide desde la dorsal, Roque Cinchado y panorámica de las Cañadas.
- Lanzarote: Timanfaya, El Golfo, Caldera de Masián y Corazoncillo.
- Fuerteventura: Pico de la Zarza, Faro de La Entallada y Sicasumbre.
- La Palma: Llano del Jable, volcán San Antonio y Mirador El Time.
- La Gomera: Garajonay y dos vistas de Roque Agando.
- El Hierro: El Sabinar, paisaje de Isora y Roques de Salmor.
- La Graciosa: dos vistas de Montaña Amarilla y panorámica hacia Montaña Clara/Alegranza.

La elección final favorece identidad territorial, legibilidad con texto superpuesto y variedad visual entre islas.

## Tratamiento técnico

Las copias web se descargaron desde las miniaturas oficiales de Wikimedia Commons y se redimensionaron a 1600 px de ancho en JPEG. El recorte visible se hace mediante `object-fit: cover`; el archivo local no se recorta. Cada copia tiene checksum SHA-256 en el catálogo.

Las adaptaciones de obras CC BY-SA conservan la misma licencia indicada por la fuente. La atribución visible usa el formato “Foto: Autor · Licencia” y enlaza tanto al archivo original como al texto de la licencia. La página `/creditos-visuales` reúne la información completa.

## Superficies que usan las imágenes

- tarjetas de las siete islas en Home;
- cabeceras de los siete perfiles insulares;
- cabeceras de los informes territoriales insulares;
- informe territorial de La Graciosa;
- catálogo público de créditos visuales.

Las imágenes no modifican ni sustituyen métricas, fuentes de datos, metodología o trazabilidad epidemiológica.

## QA de publicación

Validaciones ejecutadas el 2026-09-29:

- ocho territorios presentes, sin duplicados;
- todos los estados de licencia en `VERIFIED`;
- URLs de los ocho archivos originales y cuatro textos de licencia: HTTP 200;
- checksum local reproducible;
- tamaño por archivo inferior a 750 KiB; conjunto local aproximado: 2,6 MiB;
- `next/image` con `sizes` responsivo;
- carga diferida en las tarjetas y prioridad solo en la cabecera territorial visible;
- 72 pruebas E2E superadas en escritorio/iPhone, 4 omisiones previstas por proyecto;
- inspección visual de Home, perfil de Gran Canaria, informe de La Graciosa y créditos;
- ausencia de desbordamiento horizontal en Home, perfiles, informes y créditos.

Comparación Lighthouse contra el commit base `fe21ec0`:

| Escenario | Base | Con imágenes |
|---|---:|---:|
| Transferencia inicial móvil | 1.653 KiB | 1.735 KiB |
| Performance móvil | 71 | 84 en repetición estable |
| LCP móvil | 4,8 s | 4,4 s |
| TBT móvil | 140 ms | 70 ms |
| Transferencia inicial escritorio | 1.710 KiB | 1.790 KiB |
| Performance escritorio | 60 | 88 |
| LCP escritorio | 1,4 s | 1,2 s |
| TBT escritorio | 640 ms | 0 ms |

Las puntuaciones de laboratorio fluctúan entre ejecuciones; el dato estable para evaluar el coste visual es un aumento aproximado de 80 KiB en la carga inicial. El resto de fotografías permanece diferido hasta aproximarse a su viewport.
