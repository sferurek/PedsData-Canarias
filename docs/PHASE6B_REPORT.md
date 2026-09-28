# Phase 6B — cierre RC4 y rescate de HOLD

Fecha: 28/09/2026. Base RC4: 3987e36.

La rama phase6-rc4 ya coincidía linealmente con main local. Antes del fast-forward y push se verificaron 61 tests Python, 15 tests web y build Next de 102 páginas.

## Dictámenes

| Dataset | Dictamen | Resultado |
|---|---|---|
| BDCAP | ADMIT_WITH_LIMITATIONS | 14 años; obesidad registrada 00–14; Canarias |
| SIVAMIN | HOLD | sin export autonómico reproducible |
| Cribado metabólico | ADMIT_WITH_LIMITATIONS | 12 indicadores de proceso; Canarias 2024 |
| Cribado auditivo | HOLD | informe 2024 sin fila Canarias |
| ESdE | ADMIT_WITH_LIMITATIONS | 18 estimaciones de pantallas; 1–14 |
| ESTUDES | ADMIT_WITH_LIMITATIONS | 9 estimaciones; escolarizados 14–18 |
| Espera insular | HOLD | TERRITORIO no define residencia/atención |
| Hospitalario adicional | HOLD | sin normalización incremental suficiente |

Los admitidos conservan escala regional, edad original, estado muestral/proceso y provenance. La UI solo amplía rutas existentes: BDCAP en Resultados, cribado metabólico en Prevención y ESdE/ESTUDES en Adolescencia.

## GitHub y Vercel

Main remoto quedó en 3987e36 y phase6-rc4 se conserva. El webhook de main lanzó un intento con target Production que falló antes de publicar: estado ERROR, sin alias y sin promoción. El preview RC4 sigue disponible y no se modificó.

RC4.1 se desplegó únicamente como preview desde la rama `phase6b-hold-resolution`:

- URL: https://web-qhvea596s-sferureks-projects.vercel.app
- deployment: `dpl_5reUFap1aviVpsiWmrY6Qn5WMyNb`
- target: `preview`
- estado: `Ready`
- commit desplegado: `9b7850e`

La verificación remota autenticada confirmó Home, Resultados/BDCAP, Prevención/cribado metabólico y Adolescencia/ESdE/ESTUDES. La aplicación conserva las etiquetas visibles `RC4.1 · preview`. No se cambió ni promocionó producción.

## QA final

- 66 tests Python superados.
- 16 tests web unitarios superados.
- lint y typecheck superados.
- build Next.js superado: 102 páginas.
- 23 pruebas Playwright superadas y 1 omitida por diseño según viewport.
- QA E2E ejecutado en escritorio e iPhone.
- Build Vercel superado y rutas nuevas verificadas sobre el preview protegido.

## Conclusión

**CERCA_DEL_LIMITE.** Los últimos bloques abiertos reproducibles ya están integrados. Las mejoras pediátricas con mayor valor territorial y clínico requieren aclaración o solicitud institucional; persisten oportunidades puntuales en memorias y futuras ediciones.
