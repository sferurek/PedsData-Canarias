# QA visual — Fase 3 RC1

Fecha: 27/09/2026.

## Matriz revisada

| Vista | Desktop | iPhone | Resultado |
|---|---:|---:|---|
| Home y jerarquía de indicadores | Sí | Sí | PASS |
| Mapa completo de Canarias | Sí | Sí | PASS |
| El Hierro | Sí | Sí | PASS |
| La Gomera | Sí | Sí | PASS |
| La Palma | Sí | Sí | PASS |
| Tenerife | Sí | Sí | PASS |
| Gran Canaria | Sí | Sí | PASS |
| Fuerteventura | Sí | Sí | PASS |
| Lanzarote / La Graciosa | Sí | Sí | PASS |
| Perfil municipal restringido | Sí | Sí | PASS |

## Hallazgos y correcciones

1. MapLibre 6 no cargaba el worker bajo Next/Turbopack. Se aplicó el patrón recomendado para Next: copiar `maplibre-gl-worker.mjs` y `maplibre-gl-shared.mjs` desde la versión instalada y fijar `setWorkerUrl` al recurso same-origin.
2. La captura inicial se realizaba antes de que el GeoJSON terminase de procesarse. El estado `ready` espera ahora el evento `idle` y las pruebas esperan la transición de encuadre.
3. La vista de archipiélago mantiene las siete islas; el detalle de celdas se aprecia al filtrar por isla. Los recursos verificados se distinguen con puntos oscuros.
4. La Graciosa aparece con banda morada de transferencia interinsular, separada de `>=30`.
5. Desktop e iPhone no presentan overflow horizontal. La tabla Access Gap conserva scroll horizontal controlado en móvil.

## Accesibilidad

La navegación utiliza encabezados semánticos, etiquetas visibles en selects, foco reforzado, texto alternativo funcional en el mapa y estados de carga/error. La paleta no es el único portador de significado: la leyenda y los estados textuales acompañan el color. Queda recomendada una auditoría externa WCAG antes del release final.
