# Visual QA — RC2

Fecha: 28/09/2026.

Playwright recorrió home, mapa, siete perfiles insulares y perfiles municipales en Desktop Chrome e iPhone 13. Se verificaron:

- ausencia de clipping horizontal;
- selector de capas apilado en móvil;
- leyendas específicas de acceso, renta y aire;
- cambio renta → PM10 → accesibilidad;
- siete islas y Lanzarote/La Graciosa;
- perfiles municipales publicables y restringidos;
- Source/Method y estados PARTIAL/NOT AVAILABLE.

Resultado: 14/14 E2E verdes. Las capturas se generan en `apps/web/test-results/` y no se versionan. La revisión visual manual confirma que la malla, los puntos, controles y tipografía permanecen legibles en ambos viewports.
