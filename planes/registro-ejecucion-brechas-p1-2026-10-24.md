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

### Fase 6 — Facturación: tarifa faltante, precio futuro y renovación (§9)

- **Subagente:** Opus. Partida BE `9ba1380` / FE `8dba8a8` / docs `cc3c20b`. Una ronda, sin preguntas. Solo backend.
- **Commits (2026-10-24):** BE `7e3e150` · docs: el de esta anotación.
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1834 | 1855 |
  | Wms.IntegrationTests | 359 de 361 | 372 de 374 |

  Vitest y lint no se corrieron: la fase no toca el frontend. Con `BillAtPeriodStart` retirado del job a propósito, fallan los 3 casos de salida en la gracia: las pruebas detectan el cambio.
- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** ninguna; `has-pending-model-changes` limpio.
- **Desviaciones:**
  1. **C5 (D18, DEC-002):** cambiar solo `Service.SetPrice` no bastaba: `ServicePrice.Expire` siempre ponía `IsActive = false`. Ahora `Expire` deja activo el precio si el vencimiento es futuro, nunca alarga una vigencia y lo desactiva si el vencimiento cae antes de su inicio.
  2. La prueba va en `Wms.Tests/Domain/Services/ServiceSetPriceTests.cs` (el namespace `Domain.Service` choca con la clase).
  3. Caso 1 de la renovación: CE-7 rechaza una cantidad igual a la actual; la prueba hace 10 → 11 → 10.
  4. `StorageBillableCargoUnits.Count` devuelve el conjunto de Id de las unidades que cuentan.
  5. Caso extra 6b: tanquero despachado antes del día S, que no cuenta.
- **Visto fuera de alcance (para el usuario):**
  - Si un depósito se agota **por completo** en la gracia, `CloseDepletedProductPeriodsAsync` cierra su período antes del job: no hay renovación y lo que había el día S no se cobra. El plan solo cubre el agotamiento dentro de un grupo. Posible choque con DEC-053.
  - Un precio futuro desplazado por otro anterior queda con `ValidTo < ValidFrom` e inactivo (inocuo, pero visible en la lista de precios).

### Fase 7 — Facturación: convenios programados, índice y pendientes (§10)

- **Subagente:** Sonnet. Partida BE `7e3e150` / FE `8dba8a8` / docs `4263494`. Una ronda.
- **Commits (2026-10-24):** BE `cc832b3` · FE `682e1f7` · docs: el de esta anotación.
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1855 | 1892 |
  | Wms.IntegrationTests | 372 de 374 | 384 de 386 |
  | Vitest | 455 (92 archivos) | 468 (94 archivos) |
  | Lint | 281 errores / 413 avisos | 281 / 413; cero en archivos nuevos |

- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** `20261024155558_FixAgreementActiveStakeholderIndex` (solo el filtro del índice único pasa a `status = 'Active'`), con su `Designer` y el snapshot. `has-pending-model-changes` limpio. Aplicada a un `postgres:18.0` desechable (ya detenido).
- **Base local por defecto:** el subagente arrancó `wms-postgres-db` (estaba detenido) e intentó migrar la base configurada por defecto. Tenía 3 migraciones pendientes y `RemoveSampleSeedData` falló por claves foráneas de ubicaciones; según el subagente, la transacción se revirtió sin cambios. Probablemente es `wmsdb`, que `procesos/verificacion-local.md` §1 pide no migrar sin preguntar. El orquestador volvió a detener el contenedor. **Para revisión del usuario.**
- **Pregunta resuelta por el orquestador (alcance, no por una Dn):** el plan (§10.4, prueba 2) espera `audit_logs` de la activación programada, pero `AppDbContext.CollectAuditEntries` solo audita con un usuario en `HttpContext`, y los jobs no lo tienen (el de facturación tampoco deja `audit_logs`). Se conservó `IAuditContext.Describe` y la prueba verifica las fechas del convenio (`ActivationDate`, `ArchivingDate`, `UpdatedAt`) y el aviso a Facturación. Auditar los jobs exige cambiar `AppDbContext`, fuera de esta fase. **Queda para el usuario** decidir si se hace en otra fase.
- **Desviaciones:**
  - `Stakeholder.ActivateAgreement` ya no archiva y reactiva el convenio que ya es el activo; `Agreement.Create` toma `ActivationDate` del estado resultante.
  - La activación guarda en dos pasos (D21) con primitivas propias; `Stakeholder.ActivateDueScheduledAgreements` existe y está probada en memoria, pero el servicio no la usa.
  - El frontend envía la fecha como `yyyy-MM-ddT00:00:00-05:00` y el backend la normaliza con `ColombiaTime.StartOfDayUtc`.
  - La columna «Pendiente» reemplaza a «Por refacturar», que quedaba redundante.
  - Sin prueba manual contra la API local.
- **Visto fuera de alcance:**
  - `ForkliftService.cs:91` y `ForeignTradeService.cs:39` filtran `Agreement.Status == Active`: unos 30 s a medianoche sin ver el programado, hasta que corre el job.
  - Editar un convenio «Programado» cuya fecha ya pasó, antes del job, falla la validación de fecha del formulario (ya pasaba antes).

### Fase 8 — Reportes (§11)

- **Subagente:** Opus. Partida BE `cc832b3` / FE `682e1f7` / docs `0c7ab56`. Una ronda, sin preguntas.
- **Commits (2026-10-24):** BE `02c0b32` · FE `ae20d54` · docs: el de esta anotación.
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1892 | 1894 (6 viejas borradas con `DailyIncomingGoodsRowBuilder`, 8 nuevas) |
  | Wms.IntegrationTests | 384 de 386 | 388 de 390 |
  | Vitest | 468 (94 archivos) | 472 (95 archivos) |
  | Lint | 281 errores / 413 avisos | 281 / 413; cero en archivos nuevos |

- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** ninguna; `has-pending-model-changes` limpio.
- **Prueba manual:** contra la API local sobre un `postgres:18.0` desechable (ya detenido) con un admin de bootstrap: diario por defecto IMP, EXP correcto, XX → 400, PDF de inspección 200, diario de salidas e importaciones 200, kardex inexistente 404. PDF de muestra con 6 depósitos revisado con `pdftotext` (bloques, subtotales, «Total vehículos» y firmas).
- **Borrados:** `DailyIncomingGoodsRowBuilder.cs`, `DailyIncomingGoodsReportRowDto.cs` y sus pruebas (reemplazados por `DailyIncomingGoodsReportBuilder`).
- **Desviaciones:**
  - `buildExcelWorkbook` separado dentro de `excel-export.ts` para probar `footerLines` en una hoja.
  - La planilla de envío está en el depósito: se repite por camión en PDF y Excel, y va en el encabezado en pantalla.
  - Un depósito cuyos camiones del rango están todos anulados no sale; un primer camión anulado sigue fijando la fecha de ingreso.
  - Camiones ordenados por fecha y, si empatan, por creación. Importador solo del rol `IMPORTER`.
  - El validador conserva sus mensajes de fecha; el handler calcula el rango con `ReportDateRange`.
  - Excel del diario de salidas: los totales van en «No. Guía» y la cantidad suma todas las filas aunque mezclen unidades.
  - Pantalla del diario: tarjetas por depósito; «Exportar Excel» solo con resultados.
  - El PDF del diario de salidas imprime ahora el manifiesto DIAN bajo «Manifiesto» (nulo fuera de importación).
- **Visto fuera de alcance:**
  - El filtro `fromDate`/`toDate` de `GET foreign-trade/deposits` (`GetDepositsHandler.cs:79-88`) sigue con la fecha de creación.
  - El Excel del kardex sigue sin encabezado del depósito (resto de BR-07-005).
  - `convenciones-tecnicas.md` §3 ubica `formatColombiaDate` y `formatColombiaTime` en `shared/utils/format.ts`, pero están en `app/utils/colombia-date.ts`.

### Fase 9 — Migración legacy: año y prórroga (§12)

- **Subagente:** Sonnet. Partida BE `02c0b32` / FE `ae20d54` / docs `4e964d3`. Una ronda, sin preguntas. Backend y docs.
- **Commits (2026-10-24):** BE `f37f353` · docs: el de esta anotación (incluye F6-03 de `planes/paridad-legacy/plan-backend-paridad-legacy.md` con `prorroga`, `anio_deposito`, las consultas y O-1).
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1894 | 1915 |
  | Wms.IntegrationTests | 388 de 390 | 393 de 395 |

  Vitest y lint no aplican (sin cambios de frontend).
- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** `20261024163412_AddWarehouseStorageLegacyYear` (columna `legacy_year`; el índice pasa a `idx_warehouse_storage_legacy_number_year` con `NULLS NOT DISTINCT`), con su `Designer` y el snapshot. `has-pending-model-changes` limpio. Se aplicó con toda la cadena en el Postgres de Testcontainers de `Wms.IntegrationTests`; no en `wmsdb`.
- **Desviaciones:**
  1. **D28 sobre el texto del plan (DEC-002):** una correspondencia antigua «con el número solo» marca «ya migrado» solo si su depósito ya no existe o es del mismo año; si no, un BA0042 de 2025 se rechazaría por el de 2023 ya migrado.
  2. `CreateMigrated` recibe `legacyYear` obligatorio (1900–2200).
  3. En la conciliación, una fila sin `fecha_deposito` da error de fila (antes no se leía esa columna).
  4. El DTO de conciliación sigue mostrando el número sin el año, para no cambiar el contrato.
- **Visto fuera de alcance:**
  - `LegacyReleaseFobSplitter` reparte el FOB por (levante, aceptación) sin mirar el depósito: dos depósitos del mismo número y distinto año que compartan esos números podrían anular el FOB del segundo (improbable).
  - `OpenMigratedBilling` y su DTO muestran solo `LegacyNumber`.
  - Los CSV de `planes/migracion-staging/` no traen las columnas nuevas (fase 12, procedimiento de corte).

### Fase 10 — Respaldos: correo de fallo y destino externo (§13)

- **Subagente:** Sonnet. Partida BE `f37f353` / FE `ae20d54` / docs `3e37921`. Una ronda, sin preguntas. Backend, `deploy/` y docs; nada contra staging.
- **Commits (2026-10-24):** BE `30df3b0` · docs: el de esta anotación (incluye `procesos/despliegue-staging.md` §5).
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1915 | 1922 |
  | Wms.IntegrationTests | 393 de 395 | 398 de 400 |

  Vitest y lint no aplican. En una corrida intermedia falló además `StorageMinimumVatTests.PerCargoUnitWithOwnFloor…` y pasó en las dos siguientes: **intermitente**, a vigilar.
- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** ninguna; `has-pending-model-changes` limpio.
- **Despliegue:** `compose.staging.yaml` pasa `Backups__S3Credentials__s3-externo__AccessKeyId` y `…__SecretAccessKey` desde `BACKUP_S3_ACCESS_KEY_ID` y `BACKUP_S3_SECRET_ACCESS_KEY` (vacías por defecto). Runbook de `deploy/staging/README.md` con los pasos 1–8 y «Correo de fallo». Postman: petición «3b. Crear destino S3 (externo)» y variables `bucket` (`CAMBIAR-BUCKET`), `region` y `prefix`, sin secretos.
- **Desviaciones:** `HtmlEncode` solo sobre el texto del error y de los destinos; `MergeRecipients` separa `Notifications:AdminEmails` por coma o punto y coma; el `catch` de `StartManualAsync` avisa con `BackupKind.Manual` y destino «sin determinar».
- **Pendiente para el usuario (fase 13):** `deploy/staging/.env.staging.example` no trae `BACKUP_S3_ACCESS_KEY_ID` ni `BACKUP_S3_SECRET_ACCESS_KEY`; agregarlas vacías (el subagente no abre `.env*`).
- **Visto fuera de alcance:** el resto del runbook no se revisó; advertencias NU1903 de `Microsoft.OpenApi` 2.3.0 y `Newtonsoft.Json` 9.0.1.

### Fase 11 — Guía de salida con código QR de verificación (§14)

- **Subagente:** Opus. Partida BE `30df3b0` / FE `ae20d54` / docs `944d847`. Dos rondas (el orquestador devolvió dos desviaciones que el plan ya resolvía).
- **Commits (2026-10-24):** BE `560f558` · FE `e2e11e6` · docs: el de esta anotación (incluye `procesos/despliegue-staging.md` §6, clave del QR y proxy conocido).
- **Pruebas:**

  | Suite | Antes | Después |
  | --- | --- | --- |
  | Wms.Tests | 1922 | 1971 |
  | Wms.IntegrationTests | 398 de 400 | 405 de 407 |
  | Vitest | 472 (95 archivos) | 481 (96 archivos) |
  | Lint | 281 errores / 413 avisos | 281 / 413; cero en archivos nuevos o tocados |

- **Fallas de la línea base:** las mismas 2 de la fase 2.
- **Migración:** `20261024170332_AddGuideCodeTypeParameter` (inserta `GUIDE_CODE_TYPE = QR`, activo), con su `Designer` y el snapshot. `has-pending-model-changes` limpio. Aplicada a un `postgres:18.0` desechable (ya detenido).
- **Paquete:** `QRCoder` `[1.8.1]` (forma estricta, por D39 y §14.8). Arrastra `System.Drawing.Common` 6.0.0 como transitiva; `PngByteQRCode` no la usa.
- **Prueba manual** (API local sobre base desechable): token basura → 404 «La guía no existe o el código no es válido.»; `PATCH` del parámetro con `XYZ` → 400, con `barcode` y `QR` → 200; el limitador responde 429 desde la consulta 31. PDF en los dos modos revisado con `pdftotext`. No se pudo decodificar el QR en el equipo (sin `zbarimg`); las pruebas validan el PNG y el token.
- **Correcciones pedidas por el orquestador (resueltas por el plan):**
  1. §14.5: `UseForwardedHeaders` solo para los proxies conocidos. Nuevo `ForwardedHeadersSetup` (sección `ForwardedHeaders` con `KnownProxies` y `KnownNetworks`), llamado antes del limitador. En `compose.staging.yaml` se retiró `ASPNETCORE_FORWARDEDHEADERS_ENABLED` y se creó la red `wms` con subred fija `10.201.0.0/24`, Caddy en `10.201.0.10` y `ForwardedHeaders__KnownProxies__0` con esa IP. Con pruebas unitarias y de integración (un proxy desconocido no cambia la partición).
  2. §14.8: `QRCoder` con versión exacta `[1.8.1]`.
- **Desviaciones vigentes:**
  - `/verificar/` se abre con o sin sesión, como `/ayuda`, y no va en `PUBLIC_ROUTES` (que redirige al usuario con sesión) — D40.
  - `DispatchGuidePdfService` recibe `IConfiguration`, `IServiceScopeFactory?` y `ILogger`; el aviso a Admin va en un ámbito propio, fuera de la transacción de la emisión. Si el QR no se genera, cae a código de barras (D38).
  - No se hizo el `Select` opcional de `admin/parameters`.
- **Para la fase 13 (con aprobación):**
  - el usuario genera `GUIDE_VERIFICATION_KEY` en `.env.staging` (y, si quiere, la lista vacía en `.env.staging.example`, que el agente no abre);
  - **el primer `up -d` con la red nueva `wms` recrea los contenedores** (sin tocar volúmenes); comprobar que HTTPS no entra en loop y que la subred `10.201.0.0/24` no choca con otra red del servidor;
  - confirmar que `QRCoder` funciona en la imagen Linux;
  - escanear la guía en papel con Android e iPhone.
- **Visto fuera de alcance:** `GlobalExceptionHandler` registra cada 404 público como error (ruido en el log); el aviso «Falta la clave…» se repite en cada descarga y por depósito en el ZIP; NU1903 de `Newtonsoft.Json` 9.0.1.

