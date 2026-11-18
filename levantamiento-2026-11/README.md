# Levantamiento en staging — noviembre de 2026

Material de la visita a Bodegas Asociadas de noviembre de 2026, ya procesado, para el análisis funcional que consolida todos los hallazgos. Corte: 2026-11-11 · Backend `develop` `aa69633` · Frontend `develop` `8c7f20e`.

**Con estos archivos no hace falta volver a abrir los videos.** Si se necesita un fotograma, el comando para sacarlo está al final de `hallazgos-videos-levantamiento-2026-11-11.md`.

| Archivo | Qué tiene |
| --- | --- |
| `fase_1-consolidacion-final-hallazgos-2026-11-17.md` | **Cierre de la fase 1.** Consolidación final de hallazgos: 86 hallazgos, aclaraciones a PA-01–PA-25, observaciones de los videos, diferencias legacy/v2, 32 propuestas no aprobadas, inventario de mockups, pendientes y matriz de trazabilidad (195 filas). Solo queda abierto PA-19 (mercancía y embalaje en facturas de guías) |
| `hallazgos-videos-levantamiento-2026-11-11.md` | Lo que se ve en los dos videos, pantalla por pantalla y con tiempos: edición de pesos del tiquete, datos del depósito, amparados, levante con cálculo automático y salida global con dos tiquetes |
| `analisis-paridad-flujo-depositos-2026-11-11.md` | Paridad legacy vs v2 del flujo de depósitos en Comercio Exterior: tablas por etapa con evidencia `archivo:línea`, incluida la relación «Tickets Ingresos» – «Ingresos» (etapa 5) y las unidades de carga (etapa 6), conteo de diferencias, 12 brechas por impacto con los frentes integrados y decisiones pendientes. Anexo con la creación del depósito y la edición de un tiquete con depósito |

## Fuentes originales (fuera del repo)

Están en `/Volumes/Dock/Projects/bodegas_asociadas/documentos/Levantamiento staging/` y no se copian aquí porque tienen datos de personas reales:

| Archivo | Qué es |
| --- | --- |
| `levante_y_salida_global.MOV` | Video de 1 min 57 s: levante y salida global |
| `proceso_levante_edicion_pesos.mov` | Video de 3 min 31 s: edición de pesos, datos del depósito, amparados y levante |
| `revision_hallazgos.md` | Revisión del usuario de los hallazgos de la visita (PA-01 a PA-25 y comentarios por módulo) |
| `Comercio exterior.txt`, `bascula.txt`, `facturacion.txt` | Transcripciones de las sesiones con los operarios |
| `edicion_pesos.png`, `registro_levante_formulario.png` | Capturas de los formularios legacy de edición de pesos y de levante |
| `CONVENIO 23-24-25-26.xlsx` | Convenios y precios de Facturación |

## Notas para el análisis funcional

- Los videos se leyeron por fotogramas; el audio no se transcribió. Lo hablado sale de las transcripciones de arriba.
- Los nombres de personas, placas y empresas de los videos se omitieron a propósito (DEC-007).
- El análisis de paridad también está publicado en Claude Docs: <https://claude.ai/artifact/Lpd3pUNpFNxazFB555Lmet>, con el diagrama del flujo y la gráfica de diferencias.
- Las referencias PA-xx son los puntos de `revision_hallazgos.md`.
