# Ficha de defecto — DEF-MIG-005

| Campo | Valor |
|---|---|
| ID | DEF-MIG-005 |
| Título | La guía de salida de un depósito migrado ignora lo despachado en el legacy e imprime saldos errados |
| Severidad | CRITICAL |
| Prioridad sugerida | Alta |
| Módulo | Comercio Exterior (guía de salida) / migración legacy |
| Caso(s) | E19 «saldos después de un despacho»; FA-MIG-009 (nota «saldos de guía sin salidas previas a la migración») |
| Riesgo del plan (§9) | «La herramienta nunca se probó con datos reales (E19)» |
| Ambiente y commits | Local (`wms_migracion`) · FE `24d742d` · BE `f6f1828` |
| Rol / usuario | `mig.comext` (Comercio Exterior) |
| Estado | Verificado |

## Precondiciones y datos
- Depósito migrado BA0042 (v2 `2024BA00002`), un producto.
- Recibido 648, despachado en el legacy 200 (movimiento `Out` `MigrationOpening`), saldo 448, nacionalizado 648.
- **66 de los 128 depósitos migrados** (69 filas de producto) tienen salidas en el legacy.

## Pasos para reproducir
1. Comercio Exterior crea la orden de cargue `2026OC00002` por 50 unidades de BA0042.
2. Vigilancia registra el ingreso; Báscula hace la salida (cobro y tara); Bodega ejecuta el cargue de 50.
3. Comercio Exterior emite la guía: `POST /api/v1/foreign-trade/dispatch-guides` → `2026S00002`.
4. Revisar la línea de la guía (`dispatch_guide_lines`) y el PDF.

## Resultado esperado
Plan cerrado de la Ola 1, WMS-19: «Saldo anterior = cantidad del depósito − lo despachado antes». Para un migrado, lo despachado antes incluye lo despachado en el legacy:

| Saldo anterior | Despachado | Nuevo saldo |
|---|---|---|
| 448 | 50 | 398 |

## Resultado obtenido
| Recibido | Saldo anterior | Despachado | Nuevo saldo |
|---|---|---|---|
| 648 | **648** | 50 | **598** |

El PDF de la guía imprime 648 y 598. El stock del sistema sí queda bien: 448 → 398, y el kardex de Bodega muestra la salida con 448 → 398.

## Evidencia
- `db_legacy/trabajo/evidencias/e19/despacho-BA0042/`: `guia.json`, `guia.pdf`, `antes.txt` y `despues.txt` (fuera de git).
- Consulta de lectura:
  `select received_quantity, previous_balance, dispatched_quantity, new_balance from dispatch_guide_lines where dispatch_guide_id = '8580f5fe-…'` → `648 | 648 | 50 | 598`.
- Control: en BA0558, sin salidas en el legacy, la guía `2026S00001` imprime bien 300 → 200.

## Impacto
- La guía es el documento que acompaña la mercancía y se entrega al conductor.
- En 66 depósitos migrados, cada guía hasta agotar el saldo imprime un saldo mayor que el real, por la cantidad despachada en el legacy.
- Los operarios de staging lo verían en la primera salida de un depósito migrado con historia.

## Pista técnica (opcional)
- `Wms.Application/ForeignTrade/Common/Services/DispatchGuideBalanceService.cs:40-48` solo suma las líneas de guías de la v2.
- `DispatchGuideBalanceCalculator.cs:31` calcula `received − previouslyDispatched`.
- Para los migrados, sumar a lo despachado el movimiento `Out` con `SourceType = MigrationOpening` del producto. La migración ya lo crea con `salen`, en `DepositsImporter.cs`.

## Historial
| Fecha | Evento | Build | Por |
|---|---|---|---|
| 2026-10-06 | Detectado en la fase 1 de la migración (E19) | BE `f6f1828` | Agente ejecutor (Opus 5.5) |
| 2026-10-06 | **Corregido.** `DispatchGuideBalanceService.FreezeLinesAsync` suma a «lo despachado antes» la salida de apertura de la migración (`InventoryMovement` `Out` con `SourceType = MigrationOpening`) de cada producto, con una sola consulta adicional por guía y dentro del bloqueo `FOR UPDATE`; varias aperturas del mismo producto se suman (`DispatchGuideBalanceCalculator.MergeDispatched`). Siguen las exclusiones de hoy (guías anuladas, órdenes canceladas o revertidas). Un depósito no migrado no tiene ese movimiento y no cambia. La reimpresión lee la línea congelada (`DispatchGuidePdfService`), sin cálculo propio, y es el único lugar que imprime estos saldos; `NationalizationBalance` y `KardexAggregator` no se tocaron. Pruebas: `DispatchGuideMigratedBalanceTests` (unitarias: sin apertura, con apertura, apertura más guías y otro producto) y `MigratedGuideBalanceTests` (integración: migrado con recibido 648 y salen 200 → guía de 50 con 448 → 398 y la siguiente parte de 398; migrado sin salidas → 300 → 200, igual que antes). Commits: pendiente. | BE `f6f1828` + cambios sin commit | Agente implementador (Opus 5.5) |
| 2026-10-06 | **Verificado** en la repetición de la fase 1 (`informe-fase-1-repeticion.md`). BA0042 (recibido 648, salen 200): guía `2026S00001` de 50 → línea y PDF **648 / 448 / 50 / 398**; segunda guía `2026S00002` de 30 → **648 / 398 / 30 / 368**. Otro migrado con salidas, BA1196 (recibido 2.223, salen 1.000): guía `2026S00003` de 150 → 2.223 / 1.223 / 150 / 1.073. Sin salidas, BA0558: guía `2026S00004` de 100 → 300 / 300 / 100 / 200. La reimpresión es idéntica byte a byte en las 4. Kárdex de BA0042: 648 → 448 (apertura) → 398 → 368. Informe de la repetición §8. | BE `9c5c81b` · FE `4799cc4` | Agente ejecutor (Opus 5.5) |

## Lista de verificación para la repetición de la fase 1
- [x] En BA0042 (recibido 648, salen 200): OC, cargue y guía de 50 → la línea de `dispatch_guide_lines` y el PDF imprimen **recibido 648, saldo anterior 448, despachado 50, nuevo saldo 398**.
- [x] Una segunda guía sobre BA0042 parte de **398**.
- [x] Repetir en otro depósito con salidas en el legacy: saldo anterior = recibido − `salen` − guías anteriores de la v2.
- [x] En un depósito sin salidas en el legacy (p. ej. BA0558), la guía imprime lo mismo que en la primera ejecución (300 → 200).
- [x] La reimpresión de la guía (`GET foreign-trade/dispatch-guides/{id}/pdf`) imprime los mismos saldos.
- [x] El stock y el kárdex de Bodega no cambian respecto de la primera ejecución (448 → 398 en el movimiento).
- [x] **Staging, F11-S6 (2026-10-07, BE `b31ddb6` / FE `508b91b`):** BA0042, OC 2026OC00002 por 50 → guía 2026S00002 con 648 / 448 / 50 / 398, stock 398 y kárdex `In/MigrationOpening 648`, `Out/MigrationOpening 200`, `Out/LoadingOrder 50`. BA0558, levante de 100 y OC 2026OC00003 → guía 2026S00003 con 300 / 300 / 100 / 200. Evidencia: `docs/qa/resultados/evidencias/F11/S6-A-E2E-REG-operaciones.txt` §B.2.
