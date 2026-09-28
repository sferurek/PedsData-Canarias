# Actividad SIAP pediátrica
Admisión: ADMIT_WITH_LIMITATIONS. Cubos E54086A_000005,000007,000009, versión1.1; 2007–2024. CSV y SHA en manifiesto Fase6. 1.134 observaciones insulares; siete islas y18 años para cada indicador total.

Universo: servicio Pediatría AP, no cohorte inferida0–14/0–17. Consultas son contactos; personas distintas no se suman entre lugares ni años. Frecuentación general = consultas ordinarias / población asignada / año según concepto oficial almacenado en raw/phase6/frequency_definition.xml. El metadato isPercentage=true contradice la definición de cociente: se muestra como razón publicada, jamás porcentaje.

Total se usa directamente, no suma de lugares. CENTRO/DOMICILIO/TELECONSULTA conservados. Hay178 ausencias:84 en teleconsulta y5 en domicilio para consultas, otras84 y5 para personas. No implican cero. La modalidad telefónica cambia la interpretación del histórico; pandemia2020 rompe comparabilidad simple. No suavizar ni imputar discontinuidades.

Dotación usa el snapshot SIAP de la Fase0, 2007–2024, con checksum propio en payload. Ratio publicado por profesional representa población asignada, no malla de residentes. Consultas/profesional solo mismo servicio, isla y año; no FTE ni productividad individual. Consultas por niño residente y usuarios/1.000 niños quedan HOLD: población asignada no se iguala a residente y no hay edad individual compatible.

Pruebas: unicidad, cobertura7×18×3, nulos, unidades, integridad y reproducibilidad. Fuentes/condiciones: https://www.gobiernodecanarias.org/istac/aviso_legal.html. No causalidad.
