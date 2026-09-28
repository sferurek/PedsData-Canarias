# QA público de Ask PedsData

Fecha: 28/09/2026. Ask PedsData usa parser, catálogo, reglas de compatibilidad y cálculo determinista. No ejecuta SQL ni genera cifras con un LLM.

## 30 consultas verificadas

1. `Evolución de pediatras en Lanzarote`
2. `Evolución de pediatras en Tenerife`
3. `Evolución de pediatras en El Hierro`
4. `Compara consultas entre Tenerife y Gran Canaria`
5. `Compara consultas entre Lanzarote y Fuerteventura`
6. `Cómo ha cambiado la frecuentación pediátrica en El Hierro`
7. `Cómo ha cambiado la frecuentación pediátrica en La Gomera`
8. `Último valor de pediatras en La Palma`
9. `Último valor de consultas en Gran Canaria`
10. `Evolución de población infantil en Tenerife`
11. `Compara población infantil y pediatras en Lanzarote desde 2010`
12. `Compara pediatras y consultas en Tenerife desde 2010`
13. `Mapa de renta en Canarias`
14. `Mapa de renta en Fuerteventura`
15. `Mapa de accesibilidad pediátrica de Fuerteventura`
16. `Mapa de accesibilidad pediátrica de Lanzarote`
17. `Mapa de densidad infantil en Canarias`
18. `Mapa de urbanización en Canarias`
19. `Mapa de pediatras en Canarias`
20. `Mapa de frecuentación en Canarias`
21. `Mapa de prematuridad en Canarias`
22. `Mapa de PM10 en Canarias`
23. `Mapa de PM2,5 en Canarias`
24. `Mapa de NO2 en Canarias`
25. `Mapa de hospitalización pediátrica`
26. `Evolución de pediatras en Lanzarote desde 1990`
27. `Muéstrame alergias por municipio`
28. `Compara renta y hospitalización`
29. `Evolución de pediatras en La Graciosa`
30. `Evolución de consultas en Atlantis`

Los resultados válidos contienen uno o más `source_id`, periodo, geografía, unidad, método y enlace «Fuentes de este resultado». Las solicitudes imposibles devuelven uno de los estados controlados: `METRIC_NOT_FOUND`, `GEOGRAPHY_NOT_SUPPORTED`, `TIME_RANGE_NOT_AVAILABLE`, `INCOMPATIBLE_METRICS`, `NOT_MAPPABLE` o `INSUFFICIENT_DATA`.

Casos críticos aprobados: métrica regional no mapeable; periodo fuera de rango; indicador inexistente; combinación incompatible; La Graciosa sin serie inventada; territorio desconocido. Test automatizado: `src/lib/public-beta.test.ts`.
