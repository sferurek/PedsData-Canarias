# Especificación UI — RC1

## 1. UX Brief

**Persona:** profesional clínico, gestor sanitario, investigador o ciudadano que necesita comparar acceso pediátrico sin interpretar un dashboard técnico. **Trabajo:** entender en menos de cinco segundos qué se mide, explorar las siete islas y comprobar fuente, periodo y límites de cada cifra.

Pantallas: home con mapa y Access Gap; siete perfiles insulares; 85 perfiles municipales publicables y tres estados municipales restringidos. Éxito observable: las siete islas aparecen, La Graciosa no recibe minutos, ningún nulo se muestra como cero, y cualquier indicador abre su método.

Restricciones: datos 0–14 de 2024, catálogo verificado 2026, OSRM/OSM congelados, Gate B RED, sin ZBS, sin tiempo clínico ni inferencias causales.

## 2. UX States Matrix

| State | Trigger | UI Response | Recovery/Next Action |
|---|---|---|---|
| Loading | MapLibre o GeoJSON cargando | Altura reservada, skeleton y texto “Cargando mapa validado” | Carga automática |
| Empty | Filtro sin geometrías | Mensaje local y botón “Ver Canarias” | Restablecer filtro |
| Error recuperable | Fallo de mapa/basemap | Mantener indicadores y ofrecer reintento | Botón “Reintentar mapa” |
| Error fatal | Dataset agregado ausente | Página de error con enlace al inicio y estado de datos | Volver al inicio |
| Success | Datos y mapa listos | Mapa por bandas, KPIs y perfiles | Explorar isla/municipio |
| Disabled/Pending | Municipio no publicable | Indicadores sensibles ocultos y motivo visible | Consultar perfil insular |
| Partial/Degraded | La Graciosa, ZBS o centro parcial | Patrón/aviso específico, tiempo nulo | Abrir metodología |

## 3. Visual Direction

Estructura central: un “atlas clínico” con mapa ancho y panel lateral compacto. Fondo `#f4f6f1`, superficies blancas, texto `#102a36`, acento sanitario `#08766b`, bordes `#dbe4df`, radios de 16–24 px y sombras muy suaves. Las seis bandas usan una escala categórica verde–ocre; transferencia usa violeta tramado y no evaluable gris. Tipografía Geist, títulos 40/48 px en escritorio y 32/38 px móvil. Movimiento limitado a transiciones de estado de 150 ms; se respeta `prefers-reduced-motion`.

## 4. Component Contracts

- `AccessibilityMap`: recibe GeoJSON, filtro territorial y callback de selección. Debe reservar altura, exponer fallback y ser navegable junto a filtros HTML.
- `MapLegend`: muestra exactamente seis bandas y estados sin tiempo; nunca gradiente continuo.
- `ScopeFilters`: Canarias, siete islas y municipio; sin ZBS; etiquetas asociadas y foco visible.
- `Metric`: acepta `number | null`; `null` produce “No disponible”, nunca `0`.
- `IslandProfile` / `MunicipalityProfile`: indicadores, denominadores, limitaciones y provenance. Municipio `not_publishable` oculta métricas sensibles.
- `AccessGapTable`: dimensiones paralelas sin score, ranking ni etiquetas valorativas.
- `SourceMethodPanel`: panel desplegable nativo con fuente, periodo, motor, denominador y limitaciones.
- `DataBadge`: variantes `VALIDATED`, `PARTIAL`, `PENDING OFFICIAL GEOMETRY` con texto además de color.

## 5. File Plan

Crear `apps/web` como aplicación Next.js App Router, componentes en `src/components`, contratos en `src/lib`, rutas home/isla/municipio y datos públicos sanitizados en `public/data`. Crear un generador Python para que GeoJSON y JSON web deriven de curated. No modificar geometrías ZBS ni construir rutas ZBS.

## 6. Implementation

Server Components cargan perfiles JSON en build; el mapa es el único límite cliente. Los perfiles usan rutas estáticas. El mapa recibe celdas sin conteo infantil exacto, solo banda, territorio, destino y distancia aproximada. Los datos SIAP aparecen como dotación separada del conteo de centros.

## 7. Verification

Typecheck, lint, unit/component tests, build de producción y Playwright en móvil/escritorio. La inspección visual cubre archipiélago, siete islas, La Graciosa, leyenda, tooltips, clipping, foco y contraste.

## 8. PR Summary

### What
- RC1 navegable de accesibilidad pediátrica para siete islas, perfiles y Access Gap.

### Why
- Convertir exports validados en una experiencia revisable sin introducir ZBS ni falsa precisión.

### UX States Covered
- Loading: skeleton de mapa.
- Empty: restablecimiento de ámbito.
- Error: fallback local y página de error.
- Success: mapa, perfiles y metodología.

### Accessibility
- Semántica nativa, foco visible, controles etiquetados, color acompañado de texto y tablas responsivas.

### Verification
- `pnpm typecheck`, `pnpm lint`, `pnpm test`, `pnpm build`, Playwright móvil/escritorio.

### Risks / Follow-Ups
- Dependencia de tiles externos en preview; revisión clínica y de privacidad pendiente antes de release final.
