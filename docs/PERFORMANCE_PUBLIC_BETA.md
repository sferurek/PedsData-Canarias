# Rendimiento — beta pública

Fecha: 28/09/2026. Auditoría local sobre build de producción Next.js 16.3.6.

## Optimización

MapLibre y la malla cartográfica se cargaban en el bundle inicial. Se añadió carga diferida mediante `IntersectionObserver`, manteniendo una reserva estable de altura para evitar desplazamientos. No se modificaron datos, clasificación ni comportamiento del mapa.

| Métrica | Antes móvil | Final móvil | Final escritorio |
|---|---:|---:|---:|
| Lighthouse Performance | 37 | 97 | 100 |
| Accessibility | 93 | 100 | 100 verificado en móvil; 96 previo a las últimas correcciones |
| Best Practices | 100 | 100 | 100 |
| SEO | 100 | 100 | 100 |
| FCP | 0,9 s | 0,9 s | 0,25 s |
| LCP | 4,9 s | 2,6 s | 0,58 s |
| TBT | 2.280 ms | 10 ms | 0 ms |
| CLS | 0,327 | 0 | 0 |
| transferencia inicial | 1.640 KiB | 568 KiB | 615 KiB |

Los datos históricos permanecen segmentados por módulos y el mapa no se carga en la vista inicial hasta aproximarse a su sección. Vector tiles no son necesarios para este volumen en la beta.
