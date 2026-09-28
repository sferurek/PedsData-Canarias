# Auditoría de accesibilidad — beta pública

Fecha: 28/09/2026. Alcance: Home, mapa, series, comparación, Ask PedsData, fuentes, indicadores, perfiles, resultados y páginas legales; escritorio e iPhone.

## Cambios aplicados

- enlace «Saltar al contenido principal» y un único landmark `main`;
- foco visible para enlaces, botones, selectores y `summary`;
- navegación móvil operable por teclado;
- etiquetas de controles y estados `aria-live`, `role=status` y `role=alert`;
- contraste de acentos corregido, incluido el bloque clínico oscuro;
- objetivos táctiles de enlaces de fuentes y perfiles ampliados;
- leyendas que combinan color y texto;
- alternativa textual del mapa con indicador, periodo, geografía, método y fuentes;
- tablas desplazables sin ocultar la primera columna;
- respeto a `prefers-reduced-motion`;
- 404, loading y error con lenguaje útil y acción de reintento.

## Evidencia

Lighthouse móvil final: accesibilidad **100/100**. La suite Playwright valida teclado, landmarks, alternativa del mapa, navegación móvil y ausencia de clipping en iPhone y escritorio. El mapa sigue siendo una experiencia visual compleja; para lectores de pantalla se priorizan tablas, perfiles y la alternativa textual.
