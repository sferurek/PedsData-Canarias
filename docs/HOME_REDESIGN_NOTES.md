# Notas del rediseño de Home

## Arquitectura editorial

1. Hero oscuro: propuesta, principios, CTA y mapa real.
2. Banda de cinco indicadores con procedencia.
3. Informes de las siete islas sobre superficie clara.
4. Series, comparación, resultados y contexto territorial sobre fondo oscuro.
5. Ask PedsData en una pausa clara y accesible.
6. Transparencia y metodología como cierre.

## Decisiones

- El mapa usa el componente productivo; no es una ilustración ni un mock.
- Los valores del mockup de referencia no se copiaron.
- Las tarjetas de isla conservan los mismos perfiles y estados.
- Ask PedsData conserva parser, catálogo, validación y provenance.
- El mapa sigue difiriendo su carga hasta entrar en el viewport para proteger la carga inicial.
- La navegación mantiene todas las rutas públicas actuales.

## QA esperado

- Sin scroll horizontal en 390 px y desktop.
- Mapa, leyenda, filtros y procedencia visibles.
- Siete islas presentes y La Graciosa con transferencia interinsular.
- Formularios, tablas e informes legibles en ambas superficies.
- Estilos de impresión con fondo blanco.
