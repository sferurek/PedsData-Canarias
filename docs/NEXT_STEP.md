# Siguiente paso recomendado

No iniciar UI. El siguiente encargo debe ser una fase de cierre de gates:

> Trabaja sobre `sferurek/PedsData-Canarias` desde el último commit de Fase 1.
> No cambies los estados YELLOW/RED sin nueva evidencia. Cierra primero:
>
> 1. obtener de ISTAC/SCS la geometría, código y vigencia de las ZBS actuales y
>    un crosswalk temporal con E54086B; conservar separadas en Fuerteventura las
>    4 zonas territoriales, 6 unidades funcionales y 5 polígonos de 2017;
> 2. confirmar con SCS Buenavista del Norte, El Sauzal, cobertura de La Graciosa
>    y cartera hospitalaria pediátrica diferenciada;
> 3. descargar un extracto OSM Canarias con fecha/licencia/checksum, fijar una
>    versión local de OSRM o Valhalla y repetir los 35 casos sin servidor demo;
> 4. definir y justificar umbrales de snapping y diferencia temporal usando
>    trayectos de referencia en las siete islas.
>
> Solo si B y C quedan GREEN, calcula accesibilidad AP 0–14 conforme a
> `ACCESSIBILITY_METHODS.md`, carga `accessibility_result` y genera QA insular.
> Después, y no antes, inicializa el mapa básico y siete perfiles. Mantén La
> Graciosa como componente sin conexión terrestre y UCIP/UCIN interinsular con
> tiempo desconocido. No envíes los borradores institucionales sin autorización.

Si la administración no aporta ZBS vigente, el producto puede reconsiderarse
en una decisión explícita como mapa insular/municipal sin perfiles ZBS; no debe
presentarse como cumplimiento del gate B actual.
