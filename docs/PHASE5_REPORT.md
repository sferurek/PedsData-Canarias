# Informe Fase 5 — RC3

## Resultado

La Fase 5 incorpora cinco productos clínicos auditados sin cambiar accesibilidad, ambiente, privacidad ni las siete islas de RC2. El producto conserva edad, geografía, periodo, definición de caso y comparabilidad.

## Dominios

- hospitalización pediátrica: 405 observaciones, 2020–2024, edades `<1`, `1–4`, `5–14`, nueve grupos diagnósticos, escala Canarias;
- perinatalidad: 624 observaciones, 1999–2024, Canarias y siete islas; nacimientos, prematuros y tasa derivada;
- mortalidad: 147 agregados 2020–2024 por isla/edad/gran causa, con conteos 1–4 suprimidos;
- urgencias: cuatro indicadores CHUIMI 2024, sin comparación entre hospitales;
- ESC 2021: 45 estimaciones de encuesta en la geografía publicada.

## Decisiones metodológicas

Hospitalización no se presenta por isla. El grupo 15–24 no se convierte en 15–17. Urgencias hospitalarias no se convierten en tasas insulares. Mortalidad no muestra numeradores 1–4. Los grupos insulares de ESC no se reparten. Hospitalización respiratoria anual regional y aire diario por estación quedan `INSUFFICIENT_RESOLUTION` para correlación.

## Aplicación

La ruta `/resultados` separa los datos clínicos del mapa inicial y ofrece filtros de hospitalización, tabla perinatal de siete islas, actividad urgente limitada, mortalidad multianual, encuesta y modo Research con combinaciones válidas. Los siete perfiles insulares añaden perinatalidad/mortalidad; los municipales explican la ausencia de escala clínica municipal.

## QA

- 53 tests Python verdes;
- 12 tests unitarios web verdes;
- 18 E2E verdes en desktop/iPhone;
- lint y TypeScript verdes;
- build Next.js verde con 99 páginas;
- paquete clínico específico de ruta: 419.384 bytes sin comprimir.

## Dictamen

**RC3 READY FOR REVIEW**, condicionado a verificar el preview remoto. No es una release final y no habilita comparaciones hospitalarias ni causalidad.
