# Ficha de defecto — DEF-MIG-003

| Campo | Valor |
|---|---|
| ID | DEF-MIG-003 |
| Título | El importador de levantes omite filas del mismo levante y producto y pierde cantidad |
| Severidad | CRITICAL |
| Prioridad sugerida | Alta |
| Módulo | Administración (migración legacy) |
| Caso(s) | FA-MIG-003, FA-MIG-007; E19 |
| Riesgo del plan (§9) | «La herramienta nunca se probó con datos reales (E19)» |
| Ambiente y commits | Local (`wms_migracion`) · FE `24d742d` · BE `f6f1828` |
| Rol / usuario | Admin |
| Estado | Verificado |

## Precondiciones y datos
- En el legacy, un levante se reparte en una fila de `producto_levante` por cada `producto_en_bodega` (cada camión del depósito).
- Un depósito con un producto que llegó en 2 camiones y un levante tiene 2 filas con el mismo número de levante, la misma aceptación y el mismo producto, cada una con su cantidad.
- La consulta del plan devuelve una fila por `producto_levante`.

## Pasos para reproducir
1. Cargar los depósitos y exportar los levantes con la consulta del plan, filtrada por id (ver DEF-MIG-002): 170 filas.
2. `POST /api/v1/administration/legacy-import/Releases` con `dryRun=true`.

CSV de ejemplo, anonimizado:
```
nro_deposito;id_producto;id_embalaje;nro_levante;fecha_levante;nro_aceptacion;fecha_aceptacion;cantidad_levante;peso_bruto;fob_dolares;tasa_cambio;fob_pesos
BA9002;555;22;372024000000001;2024-03-01;372024000000002;2024-02-28;176.16;5000;10000;3900;39000000
BA9002;555;22;372024000000001;2024-03-01;372024000000002;2024-02-28;440;5000;10000;3900;39000000
```

## Resultado esperado
- Lo nacionalizado del producto es la suma de sus filas, 616,16, igual a `nacionalizados` del CSV de depósitos.
- Además, F6-03 regla 4: «Σ levantes del producto» frente a lo ingresado.

## Resultado obtenido
- La segunda fila se cuenta como «omitida», por levante repetido (`skipped`).
- En el archivo real: **45 filas omitidas** en 15 grupos de productos vivos, **10.489 unidades** de levante perdidas.
- **14 productos vivos** quedarían con lo nacionalizado por debajo del legacy. La conciliación los marcaría como `Difference`.

## Evidencia
- Lote `s2-Releases-sim`: `created = 107`, `skipped = 45`, `errorRows = 18`.
- El análisis por grupo está en el informe de la fase 1, §5.3.

## Impacto
- Nacionalizado por debajo del real. La orden de cargue bloquearía mercancía ya nacionalizada en el legacy, y los totales de póliza (F5-06) saldrían menores.
- **Paliativo aplicado en la fase 1:** la consulta congelada (`consultas/12_levantes.sql`) agrupa por depósito, producto, embalaje y levante, con `SUM(PL.cantidad_levante)`.
- Resultado: 118 filas, 107 levantes, 0 omitidos y conciliación 133/133 `Ok`.

## Pista técnica (opcional)
- **Opción A:** corregir la consulta del plan para que agrupe, como el paliativo.
- **Opción B:** que `ReleasesImporter` (`Wms.Application/Administration/LegacyImport/Importers/ReleasesImporter.cs:95-103`) sume las filas repetidas **del mismo archivo** antes de crear el levante. La regla de «omitido» quedaría solo para los levantes ya existentes en la base, que es su propósito de idempotencia.

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado en la fase 1 de la migración (E19) | BE `f6f1828` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** `ReleasesImporter` agrupa las filas del archivo por (depósito, producto, embalaje, número de levante, número de aceptación) antes de crear (`LegacyReleaseGrouper`, nuevo) y suma la cantidad. Por decisión del usuario del 2026-10-06, el peso bruto, el FOB en dólares y en pesos, la tasa y las fechas son del levante (tabla `levante`, repetidos completos en cada fila) y se toman de la primera fila del grupo, sin sumarlos; si difieren, queda una advertencia en el lote. El reparto del FOB (`LegacyReleaseFobSplitter`) se aplica después de agrupar. «Omitido» queda solo para los levantes que ya existían en la base antes del archivo. El tope «levantado ≤ recibido» usa la cantidad agrupada, y el error de un grupo se informa en cada una de sus filas. El lote informa filas leídas (`totalRows`), levantes creados agrupados (`created`) y omitidos (`skipped`). Con el CSV real sin agrupar (170 filas) la agrupación da 118 levantes con las mismas cantidades que la consulta congelada, sin advertencias. Pruebas: `LegacyReleaseGrouperTests` (unitarias) y `LegacyReleasesImportTests` (integración: CSV sin agrupar → levantes completos y FOB sin multiplicar, segunda carga omitida, nacionalizado = suma de filas, conciliación «Ok», tope agrupado). Commits: pendiente. | BE `f6f1828` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado** en la repetición de la fase 1 (`informe-fase-1-repeticion.md`). CSV sin agrupar de 170 filas → `totalRows` 170, `created` 107, **`skipped` 0**, `errorRows` 18 (11 grupos agotados, exclusión por regla), sin advertencias. 16 grupos de varias filas (68 filas) se sumaron; el ejemplo 176,16 + 440 es BA1018 y su nacionalizado cuadra. Nacionalizado de la v2 = `nacionalizados` del CSV en 133 de 133 productos. FOB y peso por levante = legacy en 107 de 107 (sin multiplicar). Segunda carga: `created` 0, `skipped` 107. Conciliación: **133/133 Ok**. Informe de la repetición §5.3. | BE `9c5c81b` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |

## Lista de verificación para la repetición de la fase 1
- [x] El CSV de levantes es el de la consulta corregida del plan, **sin agrupar** (≈ 170 filas).
- [x] Carga en firme: `totalRows` ≈ 170, `created` ≈ 107, **`skipped` = 0** y los errores son solo de productos agotados en el legacy (≈ 11 grupos, «exclusión por regla»).
- [x] Sin advertencias de «fechas, tasa, peso o FOB distintos» (o, si aparecen, se explican).
- [x] Para cada producto vivo, Σ levantes de la v2 = `nacionalizados` del CSV de depósitos (los 14 productos que quedaban por debajo ahora cuadran; p. ej. el de 176,16 + 440 = 616,16).
- [x] El FOB de cada levante es el del legacy, no multiplicado por el número de camiones.
- [x] La segunda carga del mismo archivo da `created` = 0 y `skipped` ≈ 107.
- [x] La conciliación da **133/133 «Ok»**.
