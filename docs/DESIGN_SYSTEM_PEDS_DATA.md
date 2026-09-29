# Design system de PedsData Canarias

## Principios

1. **El dato antes que el ornamento.** El color organiza, nunca sustituye una etiqueta, unidad o estado.
2. **Geografía honesta.** Una capa mantiene la resolución real de su fuente.
3. **Trazabilidad visible.** “Fuentes de este resultado” continúa junto a cada resultado.
4. **Siete islas.** Ninguna variante visual puede ocultar un territorio por ausencia de datos.
5. **Lectura accesible.** Contraste, foco, alternativa tabular y estructura semántica son parte del componente.

## Tokens

| Token | Valor | Uso |
|---|---|---|
| `--paper` | `#031522` | Fondo principal |
| `--surface` | `#082438` | Paneles |
| `--surface-raised` | `#0b3049` | Paneles elevados |
| `--ink` | `#eefbff` | Texto principal |
| `--ink-soft` | `#9fb9c8` | Texto secundario |
| `--sea` | `#2de2e6` | Acción, vínculo y dato destacado |
| `--coral` | `#ffbd69` | Énfasis cálido y foco complementario |
| `--violet` | `#a58bff` | Estados especiales y transferencia |
| `--radius` | `20px` | Paneles principales |

Las secciones claras redefinen localmente texto, superficie y borde para mantener contraste.

## Tipografía

- Titulares: Iowan Old Style/Baskerville/serif del sistema.
- Interfaz y cifras: Geist.
- Etiquetas: versales pequeñas con espaciado, siempre acompañadas por contenido legible.

## Componentes

- **Botón primario:** cian sólido, texto azul oscuro, foco dorado.
- **Botón secundario:** fondo transparente, borde cian.
- **Panel de datos:** superficie azul elevada, borde de baja opacidad y sombra contenida.
- **Mapa:** fondo oceánico, una capa de color principal y puntos auxiliares.
- **Gráfico:** cian, azul, ámbar, violeta y verde; ejes visibles sobre fondo oscuro.
- **Estado:** color más texto; nunca depende solo del color.
- **Informe:** paneles editoriales con contexto regional visualmente separado.

## Responsive

- Desktop: hero a dos columnas y mapa protagonista.
- Tablet: hero apilado; informes insulares en dos/cuatro columnas.
- Móvil: una columna, controles verticales, mapa de 440 px, menú nativo desplegable y tablas con scroll.

## Accesibilidad

Se conserva el enlace de salto, foco de 3 px, jerarquía de encabezados, nombres accesibles, alternativas textuales de mapas, tablas semánticas y reducción de movimiento. El estilo de impresión vuelve a papel blanco.
