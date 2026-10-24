# Registro de ejecución — Plan de brechas P1 (fases 2 a 12, orquestador)

> **Plan:** `planes/plan-cerrado-brechas-paridad-p1-2026-10-23.md`. **Prompt de fase:** `planes/prompt-plan-brechas-paridad-p1-2026-10-23.md`. **Prompt del orquestador:** `planes/prompt-orquestador-brechas-paridad-p1-2026-10-24.md`.
> **Inicio:** 2026-10-24. El orquestador lanza un subagente por fase, en secuencia, y hace el commit de cada fase con la autorización del usuario del 2026-10-24 (excepción a `DEC-003`, solo para el orquestador). Sin push, sin staging.

## Arranque

| Repo | Rama | HEAD al iniciar | Estado |
| --- | --- | --- | --- |
| `Backend/wms-api` | `develop` | `267bef6` | limpio |
| `Frontend/wms` | `develop` | `7963a4f` | limpio |
| `docs` | `main` | `0872063` | sin rastrear: `planes/prompt-orquestador-brechas-paridad-p1-2026-10-24.md` |

- **Rama del repo `docs`:** el hub solo tiene la rama `main` (local y `origin/main`); nunca tuvo `develop`. `DEC-003` y el `README.md` del hub hablan de `develop` en los **dos** repos de código. El orquestador interpreta que, en `docs`, la rama de trabajo es `main` y continúa allí, sin crear ramas. Si el usuario quería otra cosa, los commits de `docs` de esta ejecución están solo en local y se pueden revisar antes del push.
- **Docker:** disponible (servidor 29.1.3), así que `Wms.IntegrationTests` corre completo.
- **Fase 1:** el usuario ya hizo los commits (BE `267bef6`, FE `7963a4f`). El orquestador solo actualizó el §17 del plan y `planes/README.md`.

## Fases

### Fase 2 — Concurrencia y guardas de la orden (§5)

- **Subagente:** Opus. Partida BE `267bef6` / FE `7963a4f` / docs `b6f725a`. Dos rondas (una por la pregunta 1).
- **Commits (2026-10-24):** BE `a7bd8ef` · FE `9c64ca5` · docs: el de esta anotación.
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1763 | 1769 |
  | Wms.IntegrationTests | 320 de 322 | 329 de 331 |
  | Vitest | 412 (87 archivos) | 423 (88 archivos) |
  | Lint | 281 errores / 413 avisos | 281 / 413; cero en archivos nuevos |

- **Fallas de la línea base (no bloquean):** `InitiateCustomerIdTests.Queue_PendingService_ReturnsCustomerId` y `DiscardOperationTests.Discard_ReleasesTruckToNotStarted`. Pasan solas; el subagente lo atribuye al tope de 100 camiones de la cola de báscula al correr la suite completa.
- **Migración:** ninguna; `has-pending-model-changes` limpio.
- **Preguntas resueltas:**
  1. `WarehouseStorageCancellationService` también cancela órdenes (llamador no previsto por el §5.2). Resuelta con **D6** (DEC-002): la anulación del depósito responde 409 «Anule primero la guía {n} de la orden {OC}.» si la orden tiene guía vigente, sin anular la guía. Con prueba de integración.
  2. Las guías de importación y de exportación toman el consecutivo `S` antes de bloquear los productos (contra el orden global de D5). El §5.1 no pide reordenarlo, la de exportación está fuera de alcance y hoy no hay ciclo: sin cambio. **Queda para el usuario** decidir si se ajustan las dos en otra fase.
- **Desviaciones:** `activeDispatchGuideNumber` solo en `features/warehouse/types/loading-order.ts` (`ILoadingOrder`, que comparten CE y Bodega); el tipo de `foreign-trade` no tiene el detalle. Sin prueba manual contra la API local: la base de Development (`wmsdb`) está en un esquema viejo y su contenedor detenido; los endpoints se probaron por HTTP en `Wms.IntegrationTests`.
- **Visto fuera de alcance:**
  - `CreateLoadingOrderCommandHandler`: el mismo producto desde dos unidades de carga en una orden responde 404 «Uno o más productos de depósito no existen».
  - `LoadingOrderReservationService.RemoveAsync` no deja retirar un ítem que salió en una guía ya anulada (no filtra `CancelledAt`).
  - `GetLoadingOrderDetailHandler`: falta un paréntesis en la condición de `reserveForThisOrder`.

### Fase 3 — Guía con aviso y marca «sin salidas» (§6)

- **Subagente:** Opus. Partida BE `a7bd8ef` / FE `9c64ca5` / docs `2f987ce`. Una ronda, sin preguntas.
- **Commits (2026-10-24):** BE `272b785` · FE `b1b27fa` · docs: el de esta anotación.
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1769 | 1788 |
  | Wms.IntegrationTests | 329 de 331 | 340 de 342 |
  | Vitest | 423 (88 archivos) | 440 (90 archivos) |
  | Lint | 281 errores / 413 avisos | 281 / 413; cero en archivos nuevos |

- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** `20261024144232_AddStakeholderExitBlock` (4 columnas en `stakeholders`: `exits_blocked` con valor por defecto `false`, motivo, fecha y autor sin FK), con su `Designer` y el snapshot. `has-pending-model-changes` limpio. Se aplicó a un Postgres 18 desechable (`wms-fase3-mig`, ya detenido), porque la base de Development `wmsdb` está detenida y en un esquema viejo. **Pendiente para el usuario:** aplicarla a la base local que use.
- **Permisos:** política nueva `ExitBlockAccess` (Admin, ForeignTrade, Billing) solo para `PATCH stakeholder/{id}/exit-block`; no quita funciones a ningún rol (DEC-005). Pruebas de 403 para Receiving, Scale y Warehouse.
- **Desviaciones:**
  - `activeDispatchGuideDiffersFromLoad` solo en `ILoadingOrder` de warehouse, como en la fase 2.
  - El composable invalida también `['stakeholder', id]` para refrescar el detalle.
  - La prueba de integración usa guía de 10 y cargue de 8 (el depósito sembrado es de 10), en vez de 100 y 80.
  - Espacio de nombres `Wms.Tests.Domain.Stakeholders` en la carpeta `Domain/Stakeholder/` (el singular chocaba con la entidad, CS0118).
  - `UnblockExits(userId)` conserva la firma, pero el autor del desbloqueo queda en `audit_logs`.
  - Sin prueba manual contra la API local, por lo mismo de la fase 2; los endpoints se probaron por HTTP en `Wms.IntegrationTests`.
- **Visto fuera de alcance:** `WarehouseMapper.MapToDto` no ignora `ActiveDispatchGuideNumber` ni `ActiveDispatchGuideDiffersFromLoad` (solo avisos RMG de Mapperly). La guía automática de exportación no valida la marca, conforme a D9.

### Fase 4 — Báscula: corrección por pesaje y «Solo báscula» (§7)

- **Subagente:** Sonnet. Partida BE `272b785` / FE `b1b27fa` / docs `900884f`. Una ronda.
- **Commits (2026-10-24):** BE `157503b` · FE `8e4deb2` · docs: el de esta anotación.
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1788 | 1807 |
  | Wms.IntegrationTests | 340 de 342 | 350 de 352 |
  | Vitest | 440 | 445 |
  | Lint | 281 errores / 413 avisos | 281 / 413; cero en archivos nuevos |

- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** ninguna; `has-pending-model-changes` limpio.
- **Cambios de comportamiento a tener presentes:**
  - `ModifyFirstWeight` ya no guarda el propio peso como neto: con un solo pesaje el neto queda nulo (D11).
  - **Tiquete de un depósito facturado a consumidor final:** con la cadena del §7.2 (factura → no registrado → cliente del servicio → «CONSUMIDOR FINAL»), que D12 respalda («el tiquete muestra al destinatario no registrado»), ahora imprime «Consumidor Final» en lugar del cliente del depósito (CHG-84). El subagente pidió confirmarlo; el orquestador lo dio por resuelto por el plan. **Para revisión del usuario.**
- **Desviaciones:** el filtro del historial citado en `WeighbridgeHistoryFilters.cs:41-48` es el de nombre; el de `CustomerId` ya miraba `wc.Invoice`. Se extendió el de nombre. Sin prueba manual contra la API local (no hay base de Development); verificado con pruebas de integración y `pdftotext` del tiquete.
- **Visto fuera de alcance:** BR-02-007 (los handlers de corrección no rechazan ciclos anulados); la fase 5 amplía `CycleNetWeights`.

### Fase 5 — Báscula: un pesaje para varios documentos (§8)

- **Subagente:** Opus. Partida BE `157503b` / FE `8e4deb2` / docs `d393a7d`. Una ronda, sin preguntas.
- **Commits (2026-10-24):** BE `9ba1380` · FE `8dba8a8` · docs: el de esta anotación.
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1807 | 1834 |
  | Wms.IntegrationTests | 350 de 352 | 359 de 361 |
  | Vitest | 445 (90 archivos) | 455 (92 archivos) |
  | Lint | 281 errores | 281; cero en archivos nuevos |

- **Fallas de la línea base:** las mismas 2 de la fase 2 («Sequence contains no matching element»; pasan aisladas).
- **Migración:** ninguna; `has-pending-model-changes` limpio.
- **Verificación del PDF** (`pdftotext`): camión con manifiestos 20.000 y 10.000 y neto 27.000 → `2026T00001` con 18.000 y `2026T00002` con 9.000, los dos con «Pesaje compartido por 2 depósitos · neto del camión 27.000 kg».
- **Desviaciones:**
  - Texto nuevo del 409 obsoleto de `RecordWeighingHandler` (el plan no lo daba): «Este ciclo es de un solo pesaje y ya quedó cerrado con el primero.».
  - `CompleteCycleHandler` abre su propia transacción si no hay una abierta (el endpoint directo `POST weighbridge/cycles/{id}/complete` no la abría y el consecutivo del tiquete la exige).
  - Agregados: el paso de tiquete lista todos los números y el botón dice «Imprimir tiquetes»; `IsSharedWeighing` también en `GetOpenCycleByPlate`; pruebas de componente de `WeightCapture` y `DepositDetailWeightsCard`.
  - Sin prueba manual contra la API local (no hay base de Development en marcha).
- **Visto fuera de alcance:**
  - Advertencia de EF: `FormulaType.ParameterSchema` sin value comparer.
  - En el detalle de CE, un depósito adicional no lista su ciclo en `weighbridgeCycles` (el ciclo cuelga del ServiceRecord ancla): puede faltar «Ver ciclo».
  - Al imprimir varios tiquetes seguidos, el navegador puede bloquear las ventanas emergentes después de la primera; la descarga de cada PDF sí sale.

