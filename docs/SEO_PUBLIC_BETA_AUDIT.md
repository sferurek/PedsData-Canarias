# Auditoría SEO — beta pública

Fecha: 28/09/2026. Versión objetivo: `v0.9.0-beta.1`.

## Resultado

- `title` con plantilla y descripción pública específica.
- `metadataBase`, OpenGraph, Twitter card, icono y OG image 1200×630.
- idioma `es`, viewport y `theme-color` declarados.
- canonical explícito en Home, Aviso, Licencias y Cómo citar.
- `sitemap.xml`, `robots.txt` y `manifest.webmanifest` generados por Next.js.
- jerarquía con un único `main`, un `h1` por ruta principal y encabezados descriptivos.
- rutas legibles: `/evolucion`, `/comparar`, `/pregunta`, `/fuentes`, `/indicadores/[metric_id]`, `/aviso`, `/licencias`, `/citar`.

Lighthouse final: SEO **100/100** en móvil y escritorio. El sitemap incluye páginas públicas, 7 perfiles insulares, 88 municipales, 20 indicadores y 15 fuentes. La URL canónica de producción es `https://pedsdata.pedscore.app`.
