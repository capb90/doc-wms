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

