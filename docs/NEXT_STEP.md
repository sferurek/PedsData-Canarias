# Siguiente paso recomendado

El próximo encargo puede iniciar **Fase 3 — cálculo publicable y mapa de accesibilidad pediátrica sin ZBS** sobre el último commit de Fase 2.

> Reproduce `etl/prepare_accessibility.py` con el snapshot y motor fijados. Revisa los 13.277 resultados, denominadores, celdas pequeñas, cuantiles y agregados insulares/municipales; después promueve un export curado con provenance completo. Construye el mapa básico y los siete perfiles insulares, más perfiles municipales cuando la geografía sea válida.
>
> Mantén Gate B RED: no publiques filtros, perfiles, ratios ni actividad ZBS y no uses los polígonos de 2017 como actuales. Muestra “Pendiente de geometría oficial vigente”. Mantén La Graciosa como componente separado con transferencia interinsular y tiempo desconocido. No asignes tiempo terrestre a UCIP/UCIN fuera de isla.
>
> La UI debe mostrar población evaluada, no evaluable y sin ruta; fuente, periodo, motor, grafo y limitaciones. No conviertas los CSV de staging en cifras públicas sin revisión metodológica. No envíes los borradores institucionales sin autorización explícita.
