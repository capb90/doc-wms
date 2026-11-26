# Plan cerrado — Fase 2 · F05 Comercio Exterior

> **Fecha:** 25 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-25 («Aprobar con §10»), con los cambios al hub de su §10, que aplica I-05 (§13.4).
> **Origen:**
> - `DEC-080` y el análisis funcional `levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (§2.3 completo, §3.3, §3.5 y §3.6), con los wireframes `fase_2-mockups/comercio-exterior.html` (P-CE-01 a P-CE-07, P-CE-09, P-CE-10 y P-CE-12; P-CE-08 y P-CE-11 son de F06) y `transversales.html` (P-TR-02, P-TR-03 y P-TR-11), y los mockups del usuario MK-02 a MK-06 (`levantamiento_staging/mockups/`);
> - el plan maestro `planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (M1 a M25, `DEC-081`);
> - AF dueñas (19, plan maestro §3.1): AF-72, AF-73, AF-74, AF-75, AF-76, AF-77, AF-78, AF-80, AF-81, AF-82, AF-83, AF-87, AF-91, AF-92, AF-93, AF-96, AF-98, AF-100 y AF-102;
> - lo integrado de F01 (D1 a D47, contrato C-F01, notas de las fases 3 a 6 y de I-01), de F02 (D1 a D21 y los ajustes de su QA), de F03 (D1 a D45, contrato C-F03 y sus ajustes de UI y de QA) y de F04 (D1 a D46, contrato C-F04 y sus ajustes de UI);
> - las respuestas del usuario a la ronda de preguntas de este plan (2026-11-25), en D1 a D12.
>
> **Base:** BE `fase-2` `c2ca314` · FE `fase-2` `12f6656` · docs `main` `f8796ea`. Rama: `f2/f05-comercio-exterior` en BE y FE.
> **Partes:** 0 (contrato, §2) · 1 (backend, tres fases) · 2 (maquetación, tres fases y la revisión del usuario) · 3 (I-05, dos fases, §13). **Migraciones:** `DepositCoverageAndCpiWeights` (BE-1); BE-2 y BE-3, ninguna.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `A/` = el análisis; `PM/` = el plan maestro; `L/` = `bodegas-legacy/modulos/`; `P01/` = `D/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md`; `P02/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`; `P03/` = `D/planes/sprint-11/f03-bascula/plan-cerrado-f2-f03-bascula-2026-11-24.md`; `P04/` = `D/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md`; `MK/` = `D/levantamiento_staging/mockups/`.

**Cómo leer este plan.** El ejecutor de cada parte lee §0, §1, §2.1 (índice) y la sección de su fase en §8. Cada fase de §8 nombra sus decisiones, sus endpoints (con la ficha de §2.2 y el esquema de §2.3 que le tocan), sus archivos (§3) y sus casos QA (§6). El resto se lee solo cuando la fase lo cita. Las líneas citadas son de la base (`c2ca314` y `12f6656`).

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `D/README.md`, el `AGENTS.md` de tu repo (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo), `D/procesos/flujo-de-trabajo-agentes.md`, `PM/` §1.2, §5 y §6, y de este plan §0, §1, §2.1 y tu fase en §8. El frontend lee además `D/contexto/convenciones-tecnicas.md` §3 (drawer de detalle, tablas de listado y páginas que no son listados).
2. **Rama y git** (`PM/` §5.3): `git fetch`; si `develop` avanzó, fusiona `develop` en `fase-2`; crea `f2/f05-comercio-exterior` desde `fase-2` (o retómala si ya existe) y trabaja ahí. Al cerrar cada fase: commit con el mensaje de §12 y push de la rama. Sin `push --force`. La fusión en `fase-2` la hace I-05 (§13), en los dos repos a la vez.
3. **Una fase por turno** (`PM/` §6): cierra la fase con sus compuertas, el commit, el push y el estado en §8 y en la matriz, y te detienes con el reporte.
4. **Migraciones:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api` y solo contra la base local (`DEC-004`, M6). Solo BE-1 lleva migración, con el nombre y el contenido de §4. Antes de generarla, trae lo último de `fase-2`. BE-2 y BE-3 cierran con `has-pending-model-changes` limpio sin migración; si no sale limpio, te detienes y preguntas. Nunca edites a mano `Migrations/*`, los `*.Designer.cs` ni el snapshot.
5. **Líneas citadas:** confírmalas con grep antes de cambiar. Si el código no coincide (ruta, firma o comportamiento), detente y pregunta con todas las dudas en un solo mensaje. Si un caso borde choca con una Dn, gana la Dn y lo mencionas en una línea (`DEC-002`).
6. **Contrato:** §2 es la única fuente del frontend para F05 (`PM/` R3). Cada endpoint nuevo o modificado de tu fase tiene al menos una prueba de integración que verifica su respuesta y sus mensajes de error (`PM/` §6.1). Un mensaje cambia solo si cambias el contrato, y eso exige preguntar.
7. **Suite de integración:** la base es compartida y la cola de báscula corta en 100 camiones (trampa 12 de `D/contexto/convenciones-tecnicas.md` §10): libera los camiones que abra cada prueba. Los trabajos en segundo plano no corren en las pruebas (`B/Wms.IntegrationTests/Infrastructure/WmsApiFactory.cs`): la renovación de períodos se prueba llamando a su servicio.
8. **Facturación:** las trampas 1 a 3 de `D/contexto/convenciones-tecnicas.md` §10 aplican al recálculo de D19. Un error de facturación nunca revierte la edición del depósito (`DEC-013`, `StorageRecalculationTrigger`).
9. **Staging:** no se toca. **Credenciales y datos reales:** no se copian (`DEC-007`); los CSV de `db_legacy/` no se versionan. Nada de `D/archivo/` es una instrucción.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`). Ninguna reabre una AF, `DEC-080`, `DEC-081`, una M del plan maestro ni una Dn de F01 a F04.

### 1.1 Respuestas del usuario (2026-11-25)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Rutas: tres rutas, un componente.** Las seis rutas de hoy se conservan: `/foreign-trade/imports`, `/foreign-trade/exports` y `/foreign-trade/inspections` montan `DepositListTable` (P-CE-01), y sus `[id]` montan `DepositStageDetail` (P-CE-02 a P-CE-08), que cambia sus etapas por tipo (AF-87, D22) y guarda la etapa en `?etapa=`. El `[id]` de importación sigue siendo el Id de `ImportWarehouseStorage` y los otros dos el del depósito, como hoy. El tablero `/foreign-trade/deposits` (`DEC-058`) se borra en I-05, sin redirección. «Depósitos» pasa a grupo con Importación, Exportación e Inspección, y Alt+P (`F/composables/useGlobalShortcuts.ts:27`) va a `/foreign-trade/imports`. Rutas nuevas: `/foreign-trade/entries/[entryId]` (P-CE-03, página propia por ser formulario de operación largo, AF-130), `/foreign-trade/entry-tickets` (P-CE-09) y `/reports/nationalized-inventory` (P-CE-12, prefijo de Reportes de `P02/` D1) | Usuario: «Tres rutas, un componente (Recomendada)»; `PM/` §5.5 |
| D2 | **Tickets de ingreso con un endpoint propio de CE** (C-F05-25): `GET foreign-trade/entry-tickets`, con `ForeignTradeAccess`, orden y filtros por columna (C-F01-00) y las columnas de P-CE-09. `canEdit` aplica la regla de CE (P-CE-03). Excluye las entradas anuladas y las de depósitos anulados. Reusa por dentro los filtros de `GetHistoryEntriesQuery` (`B/Wms.Application/Weighbridge/Queries/GetHistoryEntries/GetHistoryEntriesQuery.cs:11-27`). C-F03-22 no cambia. Comparación: P-CE-09 pide mercancía con embalaje, el Id del depósito para el enlace y filtros por producto y número de depósito, que C-F03-22 no trae; su `canEdit` es la regla de Báscula (depósito en Borrador) y sus acciones son de Báscula | Usuario: «Endpoint propio de CE (Recomendada)»; AF-74 |
| D3 | **Un solo listado maestro-detalle: `GET foreign-trade/deposits` cambia de forma** (C-F05-01). Deja de ser el tablero de `DEC-058`: `modality` obligatoria, un estado, fechas de ingreso, filtros por columna y orden (C-F01-00), y una fila por depósito con lo de P-CE-01. La fila expandida lee las entradas del depósito al abrirse (C-F05-22). Se retiran `GET foreign-trade/imports`, `exports` e `inspections` (C-F05-02 a C-F05-04; eran C-F01-142 a C-F01-144), que solo usan las páginas que F05 reemplaza | Usuario: «Uno solo, el del tablero (Recomendada)»; AF-72 |
| D4 | **Fila expandida por producto, como el legacy.** Un bloque por producto (embalaje junto al nombre) con sus camiones debajo: placa, cantidad, peso, tiquete, MPreimp (el manifiesto del camión, «Manifiesto PreImp.» del legacy) y acciones (tarjeta del vehículo, tiquete). Al pie de cada bloque van entra, ampara y saldo del producto, este en rojo si no es cero, y al final los totales de cantidad y peso y «Gestionar amparados» (abre el detalle en `?etapa=amparados`). El wireframe pone «Cant. ampara» por camión, pero lo amparado es por producto (AF-77, P-CE-06) | Usuario: «Por producto, como el legacy (Recomendada)»; `L/mod_ingresos/listaringresos.php:364-507` |
| D5 | **Un endpoint por etapa para la edición.** `PUT foreign-trade/warehouse-storages/{id}/main-data` (C-F05-10) guarda todo P-CE-04 en Borrador y Confirmado, en una transacción, con un solo recálculo (D19) y la apertura tardía del período (D17). `PUT …/covered-quantities` (C-F05-11) guarda lo amparado de P-CE-06. Alta, edición, cambio de producto y baja de productos siguen con sus endpoints, abiertos a Confirmado (C-F05-12 a C-F05-15). Se retiran `PATCH …/draft`, `PATCH …/customer`, `PUT …/stakeholders`, `PATCH imports/{id}/manifest` y `POST …/return-for-correction` (C-F05-16 a C-F05-20). `PATCH warehouse-storages/{id}/entry-date` (C-F03-51) sigue para Báscula | Usuario: «Uno por etapa (Recomendada)»; AF-75, AF-76, AF-77, AF-78, AF-93 |
| D6 | **CE corrige la sección Vigilancia dentro de C-F01-90** (C-F05-23): `PUT foreign-trade/entries/{entryId}` suma `licensePlate`, `entryReasonId` y `dateTimeEntry`, con las reglas de hoy de C-F01-07 y C-F03-17 (categoría del motivo y límites de `DEC-012` y `DEC-051`). CE corrige en cualquier estado salvo Anulado, y la corrección queda en la auditoría. C-F01-07 no cambia | Usuario: «En C-F01-90 (Recomendada)»; AF-26; hueco: `EntryCorrectionAccess` es Admin, Receiving y Scale (`B/Wms.Domain/Security/WmsPolicyRoles.cs:67`) |
| D7 | **La salida exige cliente.** Confirmar una salida (C-F05-21, sobre C-F01-98), también en inspección, exige que cada depósito de sus líneas tenga cliente: si no, 409 «Asigne el cliente del depósito {N} antes de confirmar la salida.». F05 lo agrega como dueño de AF-75, y F06 lo muestra en su pantalla | Usuario: «La salida exige cliente (Recomendada)»; hueco: la inspección sale sin guía y sin cliente (`B/Wms.Application/Exits/Common/ExitGuideIssuer.cs:36-38` solo cubre la guía) |
| D8 | **Se mantiene D42 de F01.** Registrar o corregir una tasa semanal recalcula solo las facturas en Borrador (`B/Wms.Application/Billing/Common/Services/StorageRecalculationTrigger.cs:290`, `:311`), como dice `A/` §3.5. La edición en Confirmado de F05 usa `DEC-022` completo (D19). F05 no cambia código de F01 por esto | Usuario: «Se mantiene D42 (Recomendada)»; `DEC-022`, `A/` §3.5 |
| D9 | **Fecha de aceptación = fecha del levante, como el legacy.** Verificado en el legacy: al registrar y al editar, `fecha_aceptacion` se guarda con el mismo valor que `fecha_levante` (`L/mod_levantes/registrarlevante.php:326-328`; `L/mod_levantes/modificarlevante.php:88-98`), y el operario solo digita la fecha del levante (`L/mod_levantes/registrarlevante.php:617`, `L/mod_levantes/modificarlevante.php:410`). Así que C-F05-29 y C-F05-30 dejan de recibir `acceptanceDate`, el backend guarda `AcceptanceDate = ReleaseDate` al registrar y al editar, la columna sigue sin nulos y no hay migración. Los levantes migrados conservan la suya, que el legacy ya guardó igual. La etiqueta y el orden de la guía no cambian (`B/Wms.Application/ForeignTrade/Common/Services/LabelGenerationService.cs:1023-1025`; `ReleaseSnapshotSelector.cs:18`) | Usuario: «Validar si en el legacy la fecha de aceptación es la misma fecha de levante porque en el legacy el operario solo ingresa fecha de levante»; AF-82 |
| D10 | **`GET foreign-trade/releases` cambia de forma** (C-F05-32): una fila por depósito de importación, con `nationalizationStatus` (varios), `withWeightDifference`, `search` y orden (C-F01-00). Los contadores van en `GET foreign-trade/releases/summary` (C-F05-33). La fila expandida y la etapa Levantes leen los levantes del detalle del depósito (C-F05-05) | Usuario: «GET releases cambia de forma (Recomendada)»; AF-80; `B/Wms.Api/Controllers/v1/ReleasesController.cs:23` |
| D11 | **Indicador de Entradas: el precio cuenta solo sin CPI manual.** Una entrada vigente sin precio marca la etapa Entradas solo mientras el valor CPI no sea manual (`WarehouseStorage.CargoValueIsManual`, `P01/` D28). Con CPI digitado, marca solo el manifiesto que falta en los camiones con carta porte. El indicador es un color: no bloquea la confirmación | Usuario: «Solo sin CPI manual (Recomendada)»; AF-73, AF-99 (criterios aceptados) |
| D12 | **Tres fases por parte** (§8). Backend: BE-1 depósitos; BE-2 entradas, tickets, Abandono y Listas de empaque; BE-3 levantes e inventario nacionalizado. Maquetación: FE-1 contratos, fila expandible, P-CE-01 y P-CE-09; FE-2 detalle por etapas (P-CE-02 a P-CE-06, P-CE-03 y Salidas vacía); FE-3 P-CE-07, P-CE-10, P-CE-12, Abandono y Listas de empaque. Después, la revisión del usuario (§8.7) e I-05 en dos fases (§13) | Usuario: «Tres y tres (Recomendada)» |

### 1.2 Depósitos: modelo, confirmación, edición y facturación (BE-1)

| # | Decisión | Fuente |
| --- | --- | --- |
| D13 | **Cantidad amparada por producto** (AF-77): `WarehouseStorageProduct.CoveredQuantity` (decimal, nulo = sin digitar, ≥ 0, con la precisión de `DeclaredQuantity`), auditada con la entidad. **Ingresado** del producto = suma de `DeclaredQuantity` de sus líneas en las entradas no anuladas (`WarehouseStorageEntryProduct`); en un depósito sin entradas (los migrados) es su `DeclaredQuantity`. **Saldo** = amparado − ingresado; sin amparado digitado, el saldo es − ingresado. Lo amparado no cambia el stock (`DEC-010` (2), precisada por AF-77). La «Cantidad del depósito» de P-CE-06 es `DeclaredQuantity`, que hoy es la suma de los camiones (WMS-29 D21, `B/Wms.Application/ForeignTrade/Common/Services/DepositProductEditing.cs:25-33`); se corrige por camión con el modal del producto (`A/` §3.3: «Producto del depósito (10) → Modal a dos columnas, desde Amparados») | AF-77; `L/mod_ingresos/gestionarproductos.php:56-60` |
| D14 | **Pesos CPI y peso amparado** (P-CE-04, P-CE-01, P-CE-02): `WarehouseStorage.CpiNetWeight` y `CpiGrossWeight` (kg, decimal, nulos, > 0). La lectura trae además `manifestWeightSum` (suma del peso del manifiesto de las entradas no anuladas), con la que el formulario precarga los dos campos cuando están vacíos, como el legacy (`L/mod_ingresos/modificaringreso.php:422-439`). **Peso amparado** = `CpiGrossWeight`, o `manifestWeightSum` si está vacío; es el «PB.Ampara» del legacy (`L/mod_ingresos/listaringresos.php:485-491`). **Peso que entra** = peso de mercancía del depósito (`P01/` D21). El saldo de peso (amparado − entra) es informativo: no bloquea ni marca la etapa | `A/` §2.3 g (P-CE-04: «Suma de manifiestos, precargada»); legacy |
| D15 | **Confirmación sin cliente y con amparados** (C-F05-08, C-F05-09; AF-75, AF-77, AF-87). `DepositConfirmationRequirements.Evaluate` (`B/Wms.Application/ForeignTrade/Common/Services/DepositConfirmationRequirements.cs:71-133`) deja de exigir el cliente (`:75-76`). En inspección deja de exigir la fecha del documento (`:78-79`; P-CE-04: «Sí para confirmar (salvo inspección)») y exige la descripción (código `INSPECTION_DESCRIPTION`, «descripción de la inspección»). En importación y exportación suma, por producto, el código `COVERED_QUANTITY` con el texto «cantidad amparada de {producto}: {amparado} frente a {ingresado} ingresado» cuando el saldo no es cero (sin amparado digitado, «cantidad amparada de {producto}»). La inspección no tiene amparados. El resto, como hoy. Al confirmar, `ConfirmStorageDepositHandler` (`B/Wms.Application/ForeignTrade/Commands/ConfirmStorageDeposit/ConfirmStorageDepositHandler.cs:60`, `:77-80`) abre el primer período solo si hay cliente; sin cliente no abre nada | AF-75, AF-77, AF-87; `A/` §2.3 f |
| D16 | **Etapas por tipo** (AF-87): importación con Entradas, Datos principales, Bodega, Amparados, Levantes y Salidas; exportación sin Levantes; inspección sin Levantes ni Amparados. Código de las etapas: `Entries`, `MainData`, `Warehouse`, `Coverage`, `Releases`, `Exits` | AF-87 |
| D17 | **Apertura tardía del período** (AF-75). Cuando C-F05-10 asigna el cliente a un depósito **Confirmado** que nunca tuvo período de almacenamiento, abre en la misma transacción el primer período desde la fecha de ingreso con su factura, igual que la confirmación (`StoragePeriodCalculator.FirstStart(storage.EntryDate, ColombiaTime.Today)` y `IStorageBillingService.OpenPeriodWithInvoiceAsync`). Después de guardar, avisa a Facturación las advertencias del cobro, como la confirmación (`StorageBillingNotifier.NotifyBillingWarningsAsync`). Los períodos siguientes los abre la renovación de hoy, que alcanza un período vencido por pasada (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:154-260`). En Borrador, el cliente solo se guarda. Si el depósito ya tiene período, el cambio de cliente sigue `DEC-056` con `DepositCustomerBillingChange`, como hoy (`B/Wms.Application/ForeignTrade/Commands/AssignDepositCustomer/AssignDepositCustomerHandler.cs:71`, `:93-99`) | AF-75; `DEC-012`, `DEC-020`, `DEC-056` |
| D18 | **Edición en Borrador y Confirmado** (AF-76, AF-78): C-F05-10 a C-F05-15 aceptan Borrador y Confirmado; en Cerrado o Anulado responden 409 «El depósito {N} está {estado}: ya no se edita.». `WarehouseStorage.UpdateDraftInfo` (`B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:477-506`) y `EnsureProductsAreEditable` (`:565-571`) pasan a la regla nueva. Productos: una cantidad no queda por debajo de lo levantado más lo despachado en guías vigentes y un producto con levante o salida no se quita, con los mensajes de `B/Wms.Domain/Services/EntryCorrectionRules.cs:52-56`. La fecha de ingreso conserva los límites de `DEC-012` y `DEC-051`, y el número del depósito no se edita | AF-76, AF-78; `A/` §2.3 f |
| D19 | **Recálculo de la factura del período** (AF-76, AF-78; `DEC-022`). Un guardado de C-F05-10 a C-F05-15 que cambia algo que afecta el cobro (valor CPI, moneda, cliente, agencia, cantidades de productos o fecha de ingreso) recalcula una sola vez, después del commit, con `StorageRecalculationTrigger.RecalculateAfterCorrectionAsync` (`:43`), que actualiza la factura en cualquier estado salvo Anulada (`B/Wms.Application/Billing/Common/Services/IStorageBillingService.cs:54-63`): en Borrador o Pendiente se recalcula; aprobada, enviada o con pagos, se actualiza la misma factura, conserva el N.º SIIGO y se avisa a Facturación con el total anterior y el nuevo. La fecha de ingreso va por `HandleEntryDateChangedAsync` (`:180`), que mueve el período o avisa. Qué campos cuentan lo decide `DraftCorrectionBillingRules.ChangedBillingFields`, como hoy. Amparado, pesos CPI, documento, manifiesto DIAN, importador, exportador y observaciones no recalculan | AF-76; `DEC-022`; D8 |
| D20 | **Se retira «Devolver a Borrador»** (AF-93): `POST …/return-for-correction` (C-F05-20), `ReturnStorageForCorrectionCommand` y su handler, y `WarehouseStorage.MarkForCorrection` (`:350-376`), con sus pruebas. El retiro de «Cerrar ingreso de camiones» ya lo hizo F01 (C-F01-82); F05 borra lo que quede en el frontend (`F/features/foreign-trade/composables/useCloseTruckEntries.ts` y su diálogo) | AF-93, AF-95 |
| D21 | **Salida con cliente** (D7): en `ConfirmExitCommand` (`B/Wms.Application/Exits/Commands/ConfirmExitCommand.cs:73-80`, junto a la regla BR-05-004), antes de mover stock, cada depósito de las líneas debe tener `ServiceRecord.CustomerId`; si no, 409 «Asigne el cliente del depósito {N} antes de confirmar la salida.», con el primero que falte. Aplica a los cuatro tipos y a las tres modalidades. Es una regla pura (`ExitCustomerRules`) con su prueba | D7 |
| D22 | **Indicador de etapas** (AF-73, criterios de `A/` §2.3 f aceptados en AF-99; D11). Regla pura `DepositStageRules` (`B/Wms.Application/ForeignTrade/Common/Services/`) que devuelve `pendingStages` y `warehouseLevel`; la usan el listado (C-F05-01) y el detalle (C-F05-05 a C-F05-07). **Entradas:** una entrada vigente con carta porte sin número o peso de manifiesto, o una entrada vigente sin precio mientras el CPI no sea manual. **Datos principales:** falta un requisito de confirmación de esta etapa (`DOCUMENT_DATE`, `IMPORTER`, `CUSTOMS_AGENCY`, `DIAN_MANIFEST`, `EXPORTER`, `CURRENCY`, `CARGO_VALUE`, `INSPECTION_DESCRIPTION`); el cliente no cuenta (AF-75). **Bodega:** una entrada vigente con la recepción pendiente; `warehouseLevel` es el peor nivel de sus relojes (`None`, `Yellow`, `Red`; C-F04-05). **Amparados:** un producto con saldo distinto de cero (incluye el camión tardío, AF-84). **Levantes:** un producto con diferencia de peso (D23). **Salidas:** nunca en F05; F06 llena la regla. Solo se evalúan las etapas del tipo (D16). En Cerrado y Anulado no se marca ninguna | AF-73, AF-84 |
| D23 | **Nacionalización por mercancía** (MK-04, MK-06): **peso de ingreso** del producto = suma de `NetWeight` de sus líneas en las entradas vigentes; si ninguna lo tiene y el depósito tiene un solo producto, el peso de mercancía del depósito; si no, nulo. **Nacionalizado** = suma de cantidad y peso de sus levantes. **Estado:** `NotNationalized` (nada levantado), `Partial` y `Nationalized` (levantado ≥ ingresado); el del depósito es `Nationalized` si todos sus productos lo están, `NotNationalized` si ninguno tiene levante y `Partial` en otro caso. **Diferencia de peso** (regla de MK-04, `MK/levantes/levante_detalle_deposito/Main.dc.html`): saldo de peso = peso de ingreso − peso nacionalizado; hay diferencia si (saldo de cantidad ≤ 0 y saldo de peso ≠ 0) o saldo de peso < 0; sin peso de ingreso, no hay diferencia. La etiqueta pasa a «NACIONALIZADO» con el primer levante, como hoy (PA-15) | AF-80, AF-83; MK-04 |
| D24 | **Importador del legacy** (`PM/` §7.2, M19): `DepositsImporter` (`B/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs:271-275`) fija `CoveredQuantity` = lo ingresado de cada producto migrado (`WarehouseStorageProduct.CreateMigrated`, `B/Wms.Domain/Entities/Warehouse/WarehouseStorageProduct.cs:81-103`). Los pesos CPI quedan nulos: el CSV de depósitos no los trae (`LegacyDepositRowParser.cs`). Los migrados no tienen entradas, así que su ingresado es su `DeclaredQuantity` (D13) y Amparados no queda pendiente | M19; `PM/` §7.2 |

### 1.3 Entradas, edición del ingreso, tickets y listados con el patrón (BE-2)

| # | Decisión | Fuente |
| --- | --- | --- |
| D25 | **Entradas del depósito** (C-F05-22, sobre C-F04-05 y C-F01-85): cada entrada suma `entryLogId`, `dateTimeEntry` (la hora de Vigilancia), `driverName`, `quantity` (suma de lo declarado) y `canEdit` (regla de CE: depósito no anulado y entrada no anulada). Lo usan la etapa Entradas (P-CE-02), la fila expandida (D4) y la etapa Bodega (P-CE-05) | P-CE-02; AF-96 |
| D26 | **Edición del ingreso por CE** (C-F05-23, sobre C-F01-90): además de D6, suma `currency` (COP o USD; nula = no cambia), porque P-CE-03 edita la moneda del depósito junto al precio (AF-94: «una por depósito»). Cambiar la moneda recalcula (D19). Lo demás, como C-F01-90 | P-CE-03; AF-94 |
| D27 | **Elección del depósito al cambiar el documento en P-CE-03** (C-F05-24): `GET weighbridge/storage/document-candidates` (C-F03-52) pasa de `WeighbridgeController` (política de clase `ScaleAccess`, `B/Wms.Api/Controllers/v1/WeighbridgeController.cs:65`) a `EntryCorrectionController` con `EntryEditAccess` (Admin, Scale, ForeignTrade). La ruta y la respuesta no cambian. Báscula conserva el acceso (`DEC-005`) | AF-26 («cambiar el documento repite la elección del depósito», `DEC-057` D1) |
| D28 | **Tickets de ingreso** (D2): orden por defecto `dateTimeEntry desc`; lista blanca `dateTimeEntry`, `vehiclePlate`, `driverName`, `ticketNumber`, `warehouseStorageNumber`; filtros `dateTimeEntryFrom`, `dateTimeEntryTo`, `vehiclePlate`, `driverName`, `ticketNumber`, `product` (nombre o descripción) y `warehouseStorageNumber` (texto, contiene). Solo entradas de almacenamiento (importación, exportación e inspección); salidas y solo pesaje quedan en el historial de báscula (AF-74) | AF-74; P-CE-09 |
| D29 | **Abandono y Listas de empaque con el patrón** (`P02/` D3, AF-99, AF-129): `GET foreign-trade/abandonment` (C-F05-26), `GET foreign-trade/packing-lists` (C-F05-27) y `GET foreign-trade/packing-list-items` (C-F05-28) suman orden y filtros por columna (C-F01-00), conservando sus filtros de hoy. Las páginas pasan a `AppDataTable` en modo servidor; Listas de empaque pone sus pestañas «Archivos» y «Artículos» en el slot `toolbar` de cada tabla y «Cargar lista de empaque» como `createLabel` | `P02/` D3; AF-129 |

### 1.4 Levantes e inventario nacionalizado (BE-3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D30 | **Levante en la fila editable** (AF-80, AF-82, AF-83, AF-86). Registrar (C-F05-29) y editar (C-F05-30) quedan como hoy, un producto por petición, sin `acceptanceDate` (D9). **Tasa editable al editar:** `ReleaseFobService.ApplyOnEditAsync` (`B/Wms.Application/ForeignTrade/Common/Services/ReleaseFobService.cs:34-56`) cambia la tasa guardada si la petición trae otra, recalcula el valor en pesos y fija el origen con la regla de `P01/` D43 (`Weekly` si es la de la semana del levante; si no, `Manual`). **Cálculo de la cantidad (front):** con un producto, cantidad = peso digitado × Σ cantidad ingresada ÷ Σ peso del manifiesto de las entradas no anuladas, redondeada a 2 decimales; con varios, se precarga lo pendiente del producto elegido y «Levante total del saldo» precarga la cantidad y el peso pendientes, sin peso documental; la cantidad queda editable y no supera lo pendiente (el backend sigue validando con `NationalizationBalance`). **Valor en pesos** = valor en aduanas × tasa, calculado al digitar. Tras guardar, la fila editable vuelve a ofrecerse con el nuevo saldo (H-040). Tasa precargada con C-F01-13 y prefijos con C-F01-08 | AF-80, AF-82, AF-83, AF-86; `A/` §2.3 f |
| D31 | **Rótulo «Valor en aduanas»** (AF-81): cambia el texto, no el dato ni su cálculo; `FobUsd` y `FobCop` conservan su nombre. Backend: «Digite la tasa de cambio para registrar el valor en aduanas.» (`ReleaseFobService.cs:67`); «El valor en aduanas no puede ser negativo.» y «El valor en aduanas admite máximo 2 decimales.» (`RegisterImportReleaseCommandValidator.cs:41-42`, `UpdateImportReleaseCommandValidator.cs:39-40`); «El valor en aduanas del levante {N} ya se registró con «{producto}». …» (`ReleaseValueRules.cs:42`); « El valor en aduanas pasó al producto «{producto}».» (`WithdrawImportReleaseCommandHandler.cs:93`); el PDF de movimientos, «Valor en aduanas (USD)» (`B/Wms.Application/Warehouse/Common/Services/WarehouseMovementsPdfService.cs:282`). Frontend: la etapa Levantes, Levantes (vista 2), Movimientos por depósito (`F/pages/reports/warehouse-movements.vue:210`, `:535`) y Póliza (`F/pages/reports/policies.vue:4-5`, `:100-101`, `:137`, `:180`, `:203`, `:206`, `:308`, `:317`: «Valor en aduanas UAP (USD)», «Valor en aduanas no UAP (USD)», «Total valor en aduanas»). El valor en pesos se rotula «Valor en aduanas (COP)» | AF-81, AF-82 |
| D32 | **Levantes, vista 2** (C-F05-32, C-F05-33; D10, D23): una fila por depósito de importación confirmado o cerrado con su documento comercial, manifiesto DIAN, importador, mercancía (nombres con embalaje), ingreso (cantidad y peso), nacionalizado (cantidad, peso y %), saldo, estado y número de levantes. `search` busca en número de depósito, documento, importador, mercancía y número de levante. Contadores por estado y el de «Con diferencia de peso» | AF-80; MK-05 |
| D33 | **Inventario de mercancía nacionalizada** (C-F05-34, C-F05-35; AF-91): mercancías de importación con al menos un levante cuya fecha cae en el rango (por defecto, el mes en curso; obligatorio, de hasta 366 días). Agrupado por depósito (número, documento comercial, agencia, importador y cliente); por mercancía, embalaje, fecha de ingreso, manifiesto DIAN, ingreso, existencia (stock actual) y nacionalizados (total levantado, como el legacy, `L/mod_inventario/reportenacionalizados.php:64-77`), y debajo los levantes del rango (número, aceptación, fecha, cantidad, peso y valor en aduanas). PDF con las firmas «Jefe de Bodega» y «Recibí conforme» (`:393-398`); Excel en el navegador con `useExcelExport`. Política `ForeignTradeAccess` (AF-128: «Reportes, los suyos») | AF-91 |

### 1.5 Pantallas, componentes y transversales (FE)

| # | Decisión | Fuente |
| --- | --- | --- |
| D34 | **`AppDataTable` con fila expandible** (riesgo R4 de `PM/`; la guardia del patrón exige `AppDataTable`). Cambio aditivo en `F/components/app/AppDataTable.vue:33-75`: prop `expandable` (boolean), `v-model:expandedRows` y slot `expansion` (`{ row }`), con el botón de expandir en la primera columna (`aria-label` «Expandir» o «Contraer»). Sin la prop, la tabla se ve como hoy. Con prueba y en la galería `/dev/components`. Los demás compartidos se usan sin cambios (`P03/` D38) | `PM/` R4; P-CE-01, P-CE-10 |
| D35 | **Componentes de CE nuevos** (`F/features/foreign-trade/components/`): `DepositListTable` (P-CE-01, para los tres tipos), `DepositListExpansion` (D4), `DepositStageDetail` (página del detalle), `DepositDetailHeader` (encabezado de P-CE-02 con el menú «Acciones»), `DepositStageStepper` (etapas con el indicador), `DepositGeneralInfo` (información general, balances y progreso), `DepositEntriesStage`, `DepositMainDataStage`, `DepositWarehouseStage`, `DepositCoverageStage`, `DepositReleasesStage` (P-CE-07, también compacta en P-CE-10), `ReleaseEditableRow`, `DepositExitsStage` (vacía), `EntryEditForm` (P-CE-03) y `NationalizedInventoryReport` (en `F/features/reports/components/`). `DepositProductDialog` se rehace a dos columnas, sin unidad de medida (`A/` §3.3) | `PM/` §5.5 |
| D36 | **Fuentes intercambiables** (M12, `PM/` §5.2): contratos en `F/features/foreign-trade/contracts/` (`deposit.ts`, `deposit-entry.ts` ampliado, `deposit-edit.ts`, `entry-ticket.ts`, `release.ts`, `abandonment.ts`, `packing-list.ts`, `deposit-misc.ts`) y `F/features/reports/contracts/nationalized-inventory.ts`; fuentes `deposit`, `deposit-edit`, `entry-ticket`, `release`, `abandonment` y `packing-list` en `F/features/foreign-trade/services/*.source.ts`, y `nationalized-inventory` en `F/features/reports/services/`. Lo integrado de F01, F03 y F04 que usan las pantallas (terceros con su alta rápida, productos con su alta, embalajes, tipos de unidad de carga, motivos, conductores con su alta, tipos de documento, prefijos, tasa de una fecha, entrada para editar y la del tiquete) se simula con la fachada `F/features/foreign-trade/services/catalog.source.ts`, como `P03/` D40 y `P04/` D41. I-05 la borra | M12; `P03/` D40 |
| D37 | **Reloj de Bodega en la etapa Bodega** (`P04/` D37, D40): cada recepción pendiente muestra `WarehouseClockTag`, y el color del paso Bodega del stepper es `warehouseLevel` (D22) | `P04/` D37 |
| D38 | **Etapa Salidas vacía hasta F06** (`PM/` §2.2): el stepper la muestra en importación, exportación e inspección; su contenido dice «Las salidas de este depósito llegan con la próxima actualización.» y no llama a ningún endpoint. No se marca pendiente | `PM/` §2.2 |
| D39 | **Acciones del detalle** (P-CE-02; `DEC-005`, lo que hoy hace la página): el menú «Acciones» del encabezado lleva Confirmar (con los requisitos de C-F05-08), Imprimir etiqueta del depósito, Imprimir tarjeta por vehículo, Descargar PDF del depósito, Planilla de envío (diálogo con `PATCH …/shipping-form-number`, que también admite Cerrado), Registrar prórroga (importación) y Anular (al final, `danger`). Sin «Devolver a Borrador» ni «Cerrar ingreso de camiones». El encabezado muestra el estado de nacionalización (importación), el estado del depósito, las impresiones de la etiqueta y el aviso del estado financiero del cliente, como hoy | P-CE-02; AF-93, AF-95 |
| D40 | **Acciones de la etapa Entradas** (`DEC-005`): por fila, con `AppRowActions` (más de tres, al menú ⋮): «Editar» (P-CE-03, si `canEdit`), «Ver pesaje» (`/operations/weighbridge/cycles/{cycleId}`; se conserva el enlace de `P03/` D7), «Tarjeta del vehículo», «Tiquete» (C-F03-35), «Repartir en unidades» (si la entrada tiene unidades de carga) y «Agregar de la lista de empaque» (importación, en Borrador y Confirmado) | P-CE-02; `P03/` D7 |
| D41 | **Etapa Bodega** (P-CE-05): recepciones por entrada (C-F05-22: estado, contado, ubicación y cuadrilla de la recepción, con el reloj), inventario por producto (stock, reservado, disponible y ubicaciones, del detalle) y los botones «Ajustar cantidad (CE-7)», «Movimientos» (abre `/reports/warehouse-movements?deposito={N}`, el reporte Movimientos por depósito, que F05 enseña a leer ese parámetro) y «Ver novedades» (`/warehouse/novelties?deposito={N}`, como hoy) | P-CE-05 |
| D42 | **Navegación del detalle:** la etapa va en `?etapa=entradas|datos|bodega|amparados|levantes|salidas`; sin ella abre Entradas. Migas: Comercio Exterior › Depósitos › {Importación|Exportación|Inspección} › {número}. «Volver» regresa a la lista de su tipo. P-CE-03 lleva `?volver=` con la ruta de origen (el detalle con su etapa o Tickets de ingreso) | P-CE-02, P-CE-03 |
| D43 | **Menú** (`P02/` §1.5): CE queda Dashboard · Depósitos ▸ Importación, Exportación, Inspección · Tickets de ingreso · Levantes · Abandono y prórrogas · Listas de empaque · Órdenes de cargue y Guías de salida (hasta F06, AF-97). Reportes suma «Inventario nacionalizado» (`/reports/nationalized-inventory`, Admin y ForeignTrade). El dashboard de CE (`F/pages/foreign-trade/index.vue:22`, `:29`, `:86`, `:94`) enlaza «Sin nacionalizar» y «Nacionalizados» a `/foreign-trade/releases?estado=…` y los accesos de importación y exportación a sus listas | `P02/` §1.5; AF-97 |
| D44 | **Guardias:** `FT/unit/guards/list-pattern-routes.ts` pasa a `PATTERN` `/foreign-trade/imports`, `/exports`, `/inspections`, `/entry-tickets`, `/releases`, `/abandonment` y `/packing-lists`; quita las cuatro filas de F05 de `PENDING` (`:44-48`) y F05 de `PENDING_FEATURES` (`:109`); suma `/reports/nationalized-inventory` a `OUTSIDE` («Reporte»). `FT/unit/guards/mock-sources.spec.ts`: la maquetación lista sus páginas en `MAQUETACION_PAGES` (`:18`) e I-05 la vacía y suma las fuentes a `INTEGRATED_SOURCES` | `P02/` D14, D15 |
| D45 | **Unidad de medida: F05 es su último uso** (`P02/` D19, `P03/` D42, `P04/` D46). Verificado con grep en la base: solo `F/features/foreign-trade/components/DepositProductDialog.vue:11`, `:69` usa `useUnitMeasures`, y `ReleaseForm.vue` lee `unitMeasure`. I-05 borra `F/features/administration/composables/useUnitMeasures.ts`, `F/features/administration/types/unit-measure.ts` y los cuatro métodos de `F/features/administration/services/administration-service.ts:105-133`, después de comprobar con grep que nadie más los importa | M21; `P02/` D19 |
| D46 | **Lo que se borra en I-05** (§13.3), después de comprobar con grep quién importa cada archivo (trampa 7): el tablero (`F/pages/foreign-trade/deposits/index.vue`, `DepositKanbanColumn`, `DepositFiltersPanel`, `useDepositFiltersQuery`, `types/deposit-kanban.ts` en lo que nadie más use), las páginas viejas de lista y detalle (reemplazadas en su ruta), `ReleaseForm.vue`, `ValidationForm.vue` (su diálogo nunca se abre: `F/pages/foreign-trade/imports/[id]/index.vue:259` solo lo cierra), `useReturnStorageForCorrection`, `useCloseTruckEntries`, `useUpdateDraftDeposit`, `useAssignDepositCustomer` y `AssignDepositCustomerDialog`, `useDepositStakeholders` (escritura), `useUpdateManifestInfo`, `useImportDeposits`, `useExportDeposits`, `useInspectionDeposits`, `useFullTextSearchImports`, `useReleases`, las tarjetas del detalle viejo que nadie más use, sus métodos de `foreign-trade-service.ts`, sus pruebas y lo de D45. No se borra lo que usan las pantallas de F06 (órdenes de cargue y guías: `ExitWithEntryTicketDialog`, `DispatchGuideForm`, `LoadingOrderForm` y sus composables) | `PM/` §5.4 |

### 1.6 Destino de las 19 AF dueñas

| AF | Decisión | Fase | AF | Decisión | Fase |
| --- | --- | --- | --- | --- | --- |
| AF-72 | D1, D3, D4 | BE-1, FE-1 | AF-87 | D16, D22 | BE-1, FE-2 |
| AF-73 | D11, D22, D37 | BE-1, FE-2 | AF-91 | D33 | BE-3, FE-3 |
| AF-74 | D2, D28 | BE-2, FE-1 | AF-92 | D35, D36 (selectores con «+» en P-CE-03, P-CE-04 y P-CE-06) | FE-2 |
| AF-75 | D7, D15, D17, D21 | BE-1, FE-2 | AF-93 | D5, D20, D39 | BE-1, FE-2 |
| AF-76 | D5, D18, D19 | BE-1, FE-2 | AF-96 | D25, D38, D40 | BE-2, FE-2 |
| AF-77 | D13, D15, D22 | BE-1, FE-2 | AF-98 | D35 (`DepositGeneralInfo` sin subpartida) | FE-2 |
| AF-78 | D18, D19 | BE-1, FE-2 | AF-100 | D35 (`DepositMainDataStage` en bloques, cada dato del documento en su campo) | FE-2 |
| AF-80 | D10, D30, D32 | BE-3, FE-3 | AF-102 | D35 (`EntryEditForm`: switch «Unidad de carga») | FE-2 |
| AF-81 | D31 | BE-3, FE-3 | AF-83 | D23, D30 | BE-3, FE-3 |
| AF-82 | D9, D30, D31 | BE-3, FE-3 | | | |

Las 19 tienen decisión y fase (§6 las cubre con casos).

### 1.7 AF de otras features que F05 muestra o aplica

| AF | Feature dueña | Qué muestra o aplica F05 | Pantalla |
| --- | --- | --- | --- |
| AF-26 | F01 | Edición del ingreso por CE en cualquier estado salvo lo levantado o despachado (C-F01-90, ampliado en C-F05-23) | P-CE-03 |
| AF-27 | F01 | Agregar y quitar unidades de carga mientras ningún producto tenga levante o salida | P-CE-03 |
| AF-41 | F01 | Diferencia manifiesto/mercancía en Entradas | P-CE-02 |
| AF-84 | F01 | Camión tardío en Confirmado: Amparados en rojo y aviso («Camión tardío en depósito confirmado», `P01/` D45) | P-CE-01, P-CE-02, P-CE-06 |
| AF-85, AF-86 | F01 | Tasa semanal precargada por la fecha del levante, editable (C-F01-13) | P-CE-07, P-CE-10 |
| AF-79 | F01 | Prefijos precargados en N.º de levante, N.º de aceptación y manifiesto DIAN (C-F01-08) | P-CE-04, P-CE-07 |
| AF-94 | F01 | Precio por camión (P-CE-03) y valor CPI precargado con la suma (P-CE-04) | P-CE-03, P-CE-04 |
| AF-95 | F01 | Sin «Cerrar ingreso de camiones» | P-CE-02 |
| AF-101 | F01 | Transportadora por entrada; Datos principales las lista en solo lectura | P-CE-03, P-CE-04 |
| AF-12, AF-17 | F01 | Manifiesto solo con carta porte; inspección con descripción y documento opcional | P-CE-01, P-CE-03, P-CE-04 |
| AF-57 | F04 | Color del reloj de recepción (`WarehouseClockTag`) | P-CE-05 |
| AF-54 | F02 | «+» de alta rápida: terceros, transportadora, conductor y producto | P-CE-03, P-CE-04, P-CE-06 |
| AF-99, AF-129, AF-130 | F02 | Filtros por columna, orden, botones con borde, patrón de listado, detalle en página propia para formularios largos | P-CE-01, P-CE-09, P-CE-10, Abandono, Listas de empaque |
| AF-127, AF-128 | F02 | Menú de P-TR-01 y roles | Menú |
| AF-131, AF-134 | F02 | Etiquetas encima; selectores paginados con búsqueda | Todas |

### 1.8 Permisos (`B/Wms.Domain/Security/WmsPolicyRoles.cs`; `PM/` §5.6, `DEC-005`)

| Endpoint | Política | Cambio |
| --- | --- | --- |
| C-F05-01, C-F05-05 a C-F05-15, C-F05-22, C-F05-23, C-F05-25 a C-F05-33 | `ForeignTradeAccess` (Admin, ForeignTrade) | Ninguno: la de hoy de sus controladores |
| C-F05-24 (`weighbridge/storage/document-candidates`) | `EntryEditAccess` (Admin, Scale, ForeignTrade) | Suma ForeignTrade; Scale conserva el acceso. Pasa a `EntryCorrectionController` |
| C-F05-21 (`exits/{id}/confirm`) | la de hoy (`ForeignTradeAccess`) | Ninguno |
| C-F05-34, C-F05-35 (`reports/nationalized-inventory`) | `ForeignTradeAccess` | Nuevo endpoint; los demás roles no lo tenían |
| C-F05-36 (`warehouse/movements-report/pdf`) | la de hoy (`InventoryReportAccess`) | Ninguno |

Ningún rol pierde una función: los endpoints que se retiran (C-F05-02 a C-F05-04, C-F05-16 a C-F05-20) solo los llaman pantallas de CE que F05 reemplaza (grep en la base: `F/features/foreign-trade/services/foreign-trade-service.ts:150`, `:162-166`, `:320`, `:332-336`, `:402-406`, `:810`, `:839-853`, `:931`; `F/features/foreign-trade/services/deposit-service.ts:17`).

---

## 2. Contrato (parte 0)

Es la única fuente del frontend para lo que F05 crea, cambia o retira (`PM/` R3). La maquetación lo simula (M12) e I-05 lo llama de verdad.

### 2.0 Convenciones

- Rige `P01/` §2.0: base `/api/v1`, JSON en camelCase, enums como texto, fechas ISO 8601 con zona y `DateOnly` como `yyyy-MM-dd` en día de Colombia, `{ data, pagination }`, `pageSize` de 1 a 50 con `all=true`, errores *ProblemDetails* con `description` y `errors[]`, motivos de 10 a 500 caracteres. Orden y filtros por columna: **C-F01-00**, con sus mensajes («No se puede ordenar por «{campo}».», «El orden debe ser asc o desc.», «La fecha inicial no puede ser posterior a la final.», «El valor «{valor}» no es válido para {campo}.»).
- **Identificadores:** `C-F05-mm` para cada endpoint y `QA2-F05-nnn` para cada caso (`PM/` §5.1).
- **Verificado contra el código de `fase-2`:** las fichas de F01, F03 y F04 que F05 consume (C-F01-08, C-F01-13, C-F01-25, C-F01-29, C-F01-33, C-F01-69, C-F01-71, C-F01-141, C-F01-145, C-F03-13, C-F03-35, C-F03-44, C-F03-51, C-F04-05, C-F04-30) coinciden con sus controladores y DTO (`SettingsController.cs:24`, `:56`; `StakeholderController.cs:69`; `EntryCorrectionController.cs:29-30`; `ForeignTradeController.cs:538`; `DepositStorageEntryDto.cs`). Diferencias anotadas, gana lo integrado: (1) `DepositStorageEntryDto` no trae conductor, hora de Vigilancia ni cantidad, que la etapa Entradas necesita (los suma C-F05-22); (2) `ImportReleaseDto` conserva `acceptanceDate` (D9: ahora igual a la fecha del levante); (3) el detalle de exportación e inspección son DTO propios (`ExportDepositDetailDto.cs`, `InspectionDepositDetailDto.cs`), con los campos de C-F01-86 que les aplican.
- **Lo que el esquema no declara se descarta** (Zod): los esquemas del detalle (§2.3) declaran solo lo que usan las pantallas de F05; el DTO puede traer más.

### 2.1 Índice

**Grupo A — Depósitos** (backend, fase BE-1).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F05-01 | `GET foreign-trade/deposits` | modificado: deja de ser el tablero de `DEC-058`; listado maestro-detalle por tipo (D3) | `ForeignTradeAccess` | P-CE-01 |
| C-F05-02 | `GET foreign-trade/imports` | retirado (era C-F01-142; D3) | — | — |
| C-F05-03 | `GET foreign-trade/exports` | retirado (era C-F01-143; D3) | — | — |
| C-F05-04 | `GET foreign-trade/inspections` | retirado (era C-F01-144; D3) | — | — |
| C-F05-05 | `GET foreign-trade/imports/{id}` | modificado (sobre C-F01-86): etapas, amparados, pesos CPI, nacionalización por producto | `ForeignTradeAccess` | P-CE-02 a P-CE-07, P-CE-10 |
| C-F05-06 | `GET foreign-trade/exports/{id}` | modificado (sobre C-F01-87): lo mismo, sin nacionalización | `ForeignTradeAccess` | P-CE-02 a P-CE-06 |
| C-F05-07 | `GET foreign-trade/inspections/{id}` | modificado (sobre C-F01-88): lo mismo, sin amparados ni nacionalización | `ForeignTradeAccess` | P-CE-02 a P-CE-05 |
| C-F05-08 | `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` | modificado (sobre C-F01-83): sin cliente, con amparados (D15) | `ForeignTradeAccess` | P-CE-02 |
| C-F05-09 | `POST foreign-trade/warehouse-storages/{id}/confirm` | modificado (sobre C-F01-84): igual; abre el período solo con cliente | `ForeignTradeAccess` | P-CE-02 |
| C-F05-10 | `PUT foreign-trade/warehouse-storages/{id}/main-data` | nuevo (D5) | `ForeignTradeAccess` | P-CE-04 |
| C-F05-11 | `PUT foreign-trade/warehouse-storages/{id}/covered-quantities` | nuevo (D5, D13) | `ForeignTradeAccess` | P-CE-06 |
| C-F05-12 | `POST foreign-trade/deposits/{id}/products` | modificado: Borrador y Confirmado (D18) | `ForeignTradeAccess` | P-CE-06 |
| C-F05-13 | `PUT foreign-trade/deposits/{id}/products/{storageProductId}` | modificado: Borrador y Confirmado, con piso (D18) | `ForeignTradeAccess` | P-CE-06 |
| C-F05-14 | `DELETE foreign-trade/deposits/{id}/products/{storageProductId}` | modificado: Borrador y Confirmado (D18) | `ForeignTradeAccess` | P-CE-06 |
| C-F05-15 | `PUT foreign-trade/deposits/{id}/products/{storageProductId}/catalog-product` | modificado: Borrador y Confirmado (D18) | `ForeignTradeAccess` | P-CE-06 |
| C-F05-16 | `PATCH foreign-trade/warehouse-storages/{id}/draft` | retirado (D5) | — | — |
| C-F05-17 | `PATCH foreign-trade/warehouse-storages/{id}/customer` | retirado (D5) | — | — |
| C-F05-18 | `PUT foreign-trade/warehouse-storages/{id}/stakeholders` | retirado (era C-F01-89; D5) | — | — |
| C-F05-19 | `PATCH foreign-trade/imports/{id}/manifest` | retirado (D5) | — | — |
| C-F05-20 | `POST foreign-trade/warehouse-storages/{id}/return-for-correction` | retirado (AF-93, D20) | — | — |
| C-F05-21 | `POST exits/{id}/confirm` | modificado (sobre C-F01-98): cada depósito con cliente (D7, D21) | `ForeignTradeAccess` | F06 (P-CE-11) |

**Grupo B — Entradas, tickets y listados con el patrón** (backend, fase BE-2).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F05-22 | `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` | modificado (sobre C-F04-05): hora de Vigilancia, conductor, cantidad y `canEdit` (D25) | `ForeignTradeAccess` | P-CE-01 (expandida), P-CE-02, P-CE-05 |
| C-F05-23 | `PUT foreign-trade/entries/{entryId}` | modificado (sobre C-F01-90): Vigilancia y moneda (D6, D26) | `ForeignTradeAccess` | P-CE-03 |
| C-F05-24 | `GET weighbridge/storage/document-candidates` | modificado (sobre C-F03-52): política `EntryEditAccess` (D27) | `EntryEditAccess` | P-CE-03 (y P-BAS-02) |
| C-F05-25 | `GET foreign-trade/entry-tickets` | nuevo (D2, D28) | `ForeignTradeAccess` | P-CE-09 |
| C-F05-26 | `GET foreign-trade/abandonment` | modificado: orden y filtros (D29) | `ForeignTradeAccess` | Abandono y prórrogas |
| C-F05-27 | `GET foreign-trade/packing-lists` | modificado: orden y filtros (D29) | `ForeignTradeAccess` | Listas de empaque › Archivos |
| C-F05-28 | `GET foreign-trade/packing-list-items` | modificado: orden y filtros (D29) | `ForeignTradeAccess` | Listas de empaque › Artículos; «Agregar de la lista de empaque» |

**Grupo C — Levantes e inventario nacionalizado** (backend, fase BE-3).

| ID | Endpoint | Cambio | Política | Pantalla |
| --- | --- | --- | --- | --- |
| C-F05-29 | `POST foreign-trade/imports/{id}/releases` | modificado: sin fecha de aceptación (D9) y rótulo (D31) | `ForeignTradeAccess` | P-CE-07, P-CE-10 |
| C-F05-30 | `PATCH foreign-trade/imports/{id}/releases/{releaseId}` | modificado: tasa editable (D30), sin fecha de aceptación (D9), rótulo | `ForeignTradeAccess` | P-CE-07, P-CE-10 |
| C-F05-31 | `POST foreign-trade/imports/{id}/releases/{releaseId}/withdraw` | modificado: rótulo del mensaje (D31) | `ForeignTradeAccess` | P-CE-07, P-CE-10 |
| C-F05-32 | `GET foreign-trade/releases` | modificado: una fila por depósito (D10, D32) | `ForeignTradeAccess` | P-CE-10 |
| C-F05-33 | `GET foreign-trade/releases/summary` | nuevo (D10, D32) | `ForeignTradeAccess` | P-CE-10 |
| C-F05-34 | `GET reports/nationalized-inventory` | nuevo (D33) | `ForeignTradeAccess` | P-CE-12 |
| C-F05-35 | `GET reports/nationalized-inventory/pdf` | nuevo (D33) | `ForeignTradeAccess` | P-CE-12 |
| C-F05-36 | `GET warehouse/movements-report/pdf` | modificado (sobre C-F01-161): rótulo «Valor en aduanas (USD)» (D31) | `InventoryReportAccess` | Reportes › Movimientos por depósito |

**Grupo D — De hoy, sin cambios, que consumen las pantallas de F05** (ningún contrato anterior les dio ID; la maquetación los simula, `PM/` §5.2).

| ID | Endpoint | Política | Pantalla |
| --- | --- | --- | --- |
| C-F05-40 | `GET foreign-trade/{imports\|exports\|inspections}/{id}/label` y `…/{id}/entries/{entryId}/label` (`?action=print\|download`) | `ForeignTradeAccess` | P-CE-01 (expandida), P-CE-02 |
| C-F05-41 | `GET foreign-trade/{imports\|exports\|inspections}/{id}/pdf` | `ForeignTradeAccess` | P-CE-02 |
| C-F05-42 | `GET foreign-trade/warehouse-storages/{id}/label-prints` | `ForeignTradeAccess` | P-CE-02 |
| C-F05-43 | `POST foreign-trade/imports/{id}/extension` | `ForeignTradeAccess` | P-CE-02, Abandono |
| C-F05-44 | `POST foreign-trade/warehouse-storages/{id}/cancel` | `ForeignTradeAccess` | P-CE-02 |
| C-F05-45 | `GET foreign-trade/validate-client/{stakeholderId}` | `ForeignTradeAccess` | P-CE-02 |
| C-F05-46 | `PATCH foreign-trade/warehouse-storages/{id}/shipping-form-number` | `ForeignTradeAccess` | P-CE-02 (D39) |
| C-F05-47 | `PUT foreign-trade/warehouse-storages/{id}/entries/{entryId}/cargo-unit-breakdown` | `ForeignTradeAccess` | P-CE-02 (D40) |
| C-F05-48 | `POST warehouse/inventory/adjustments` | `ForeignTradeAccess` | P-CE-05 |
| C-F05-49 | `GET foreign-trade/abandonment/summary` | `ForeignTradeAccess` | Abandono |
| C-F05-50 | `GET` y `POST foreign-trade/packing-list-suppliers`, `POST foreign-trade/packing-lists/import`, `GET` y `DELETE foreign-trade/packing-lists/{id}`, `POST foreign-trade/deposits/{id}/entries/{entryId}/packing-list-items` | `ForeignTradeAccess` | Listas de empaque; P-CE-02 (D40) |

Los números C-F05-37 a C-F05-39 no se usan.

**Consumidos de F01, F03 y F04 sin cambios** (sus fichas y esquemas están en su plan): C-F01-02 (motivos), C-F01-08 (prefijos), C-F01-13 (tasa de una fecha), C-F01-15 y C-F01-17 (conductores y su alta), C-F01-25, C-F01-26 y C-F01-141 (terceros y alta rápida), C-F01-29 y C-F01-30 (embalajes y su alta), C-F01-33 (tipos de unidad de carga), C-F01-69 y C-F01-71 (productos y su alta), C-F01-145 (unidades de carga del depósito), C-F03-13 (la entrada para editar), C-F03-35 (tiquete), C-F03-44 (tipos de documento), C-F04-30 (novedades, por enlace).

**Para F06:** la etapa Salidas (P-CE-08) y «Nueva salida» no llaman a ningún endpoint en F05 (D38). C-F05-21 queda listo para P-CE-11; `GET exits` (C-F04-03) y `GET exits/{id}` (C-F04-04) los consume F06.

### 2.2 Fichas

#### Grupo A — Depósitos

##### C-F05-01 · `GET foreign-trade/deposits` (modificado)
- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/ForeignTradeController.cs:53`, `:62-69`). Orden y filtros (C-F01-00).
- **Qué cambia:** deja de servir al tablero de `DEC-058` (`GetDepositsQuery`, `B/Wms.Application/ForeignTrade/Queries/GetDeposits/GetDepositsQuery.cs:12-30`; salen `DepositType`, `Search` y la paginación por columna) y devuelve una fila por depósito con lo de P-CE-01 (D3).
- **Petición (consulta):** paginación; `modality` (`Import` \| `Export` \| `Inspection`, obligatorio); `status` (`Draft` \| `Confirmed` \| `Closed` \| `Cancelled`, uno; sin él, todos); `entryDateFrom`, `entryDateTo`; `warehouseStorageNumber`, `document` (tipo o número; en inspección también la descripción), `ticketNumber`, `product` (nombre o descripción) (texto, contiene).
- **Orden:** lista blanca `entryDate`, `warehouseStorageNumber`, `document`, `ticketNumber`, `product`; por defecto `entryDate desc`.
- **Respuesta 200:** `pagedSchema(depositListRowSchema)`:

```jsonc
{ "data": [ {
  "warehouseStorageId": "guid", "importDepositId": "guid",      // importDepositId nulo salvo en importación
  "warehouseStorageNumber": "2026BA00003", "modality": "Import", "status": "Draft",
  "entryDate": "2026-11-02T09:40:00-05:00",
  "vehiclePlates": ["IAA111", "TLM442"], "ticketNumbers": ["2026T00298", "2026T00299"],
  "documentTypeName": "Carta porte", "documentNumber": "EC0001", "inspectionDescription": null,
  "customerName": "Cliente A", "importerName": "Importador A", "exporterName": null,
  "merchandise": [ { "productName": "Cebolla", "packaging": "Sacos" } ],
  "weights": { "gross": 44820, "merchandise": 32980, "tare": 11840, "manifest": 44980 },
  "dianManifestNumber": "1165750", "cargoValue": 20629.20, "currency": "USD",
  "products": [ { "warehouseStorageProductId": "guid", "productName": "Cebolla", "packaging": "Sacos",
                  "enteredQuantity": 760, "coveredQuantity": 850, "quantityBalance": 90 } ],
  "coverage": { "enteredQuantity": 760, "coveredQuantity": 850, "quantityBalance": 90,
                "enteredWeight": 32980, "coveredWeight": 44980, "weightBalance": 12000 },
  "nationalizationStatus": "NotNationalized",                    // nulo salvo en importación
  "pendingStages": ["MainData", "Warehouse", "Coverage"], "warehouseLevel": "Yellow"
} ], "pagination": { … } }
```

- **Reglas:** pesos = sumas de las entradas no anuladas (indicador, mercancía, tara y manifiesto); `coverage` según D13 y D14 (en inspección, `products[].coveredQuantity` y `coverage.covered*` nulos); `pendingStages` y `warehouseLevel` con `DepositStageRules` (D22); `nationalizationStatus` según D23.
- **Errores:** 400 «Indique el tipo de depósito.»; los de C-F01-00.
- **Zod:** `depositListQuerySchema`, `depositListRowSchema` (`F/features/foreign-trade/contracts/deposit.ts`).
- **Notas:** el Excel de «Exportar» lo arma la página con `all=true` y los filtros activos.

##### C-F05-02, C-F05-03 y C-F05-04 · `GET foreign-trade/imports`, `exports` e `inspections` (retirados)
- **Política de hoy:** `ForeignTradeAccess` (`ForeignTradeController.cs:83-86`, `:711-714`, `:811-814`). **Lo reemplaza:** C-F05-01 con `modality`. Solo los llaman `F/features/foreign-trade/services/foreign-trade-service.ts:162-166`, `:332-336`, `:402-406`, desde las páginas que F05 reemplaza. Petición, respuesta, errores y Zod: no aplica; 404 desde BE-1. Se borran sus consultas (`GetImportDepositsQuery`, `GetExportDepositsQuery`, `GetInspectionDepositsQuery`) si nadie más las usa (grep).

##### C-F05-05, C-F05-06 y C-F05-07 · `GET foreign-trade/{imports|exports|inspections}/{id}` (modificados)
- **Política:** `ForeignTradeAccess` (`ForeignTradeController.cs:101-105`, `:681-685`, `:829-833`). **Petición:** el Id en la ruta (importación: `ImportWarehouseStorage`; las otras: el depósito), como hoy.
- **Qué cambia** (sobre C-F01-86 a C-F01-88), con los mismos nombres en los tres DTO:
  - `pendingStages`, `warehouseLevel` (D22) y `stages` (las etapas del tipo, en orden: D16);
  - `cpiNetWeight`, `cpiGrossWeight`, `manifestWeightSum` y `coverage` (D13, D14), como C-F05-01;
  - `documentTypeId` (para el formulario de Datos principales) y `customerId` (ya existe en importación; se suma a las otras dos);
  - cada producto de `products[]` suma `enteredQuantity`, `coveredQuantity`, `quantityBalance` (nulos en inspección), `releasedQuantity`, `releasedWeight`, `dispatchedQuantity` (guías vigentes), `entryWeight`, `nationalizationStatus` y `hasWeightDifference` (D23; nulos fuera de importación) y `locations` (códigos de sus ubicaciones con mercancía, `WarehouseStorageProductPlacement`);
  - importación suma `nationalizationStatus` del depósito (D23).
- **Respuesta 200:** `dataSchema(depositDetailSchema)` (§2.3; declara solo lo que usan las pantallas).
- **Errores:** los de hoy (404 «El depósito de importación no existe.» y sus pares).
- **Zod:** `depositDetailSchema`, `depositDetailProductSchema`, `importReleaseSchema` (`F/features/foreign-trade/contracts/deposit.ts`, `release.ts`).

##### C-F05-08 · `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` (modificado)
- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/DepositCompletionController.cs:23`, `:33`). **Petición:** el Id del depósito en la ruta.
- **Qué cambia** (sobre C-F01-83, D15): sale `CUSTOMER`; en inspección sale `DOCUMENT_DATE` y entra `INSPECTION_DESCRIPTION`; en importación y exportación entra `COVERED_QUANTITY` por producto con saldo distinto de cero.
- **Respuesta 200:** `dataSchema(confirmationRequirementsSchema)`: `{ warehouseStorageId, warehouseStorageNumber, canConfirm, missing: [{ code, message }] }` (`B/Wms.Application/ForeignTrade/Common/DTOs/ConfirmationRequirementsDto.cs:7-13`).
- **Errores:** 404 «El depósito no existe.» (el de hoy).
- **Zod:** `confirmationRequirementsSchema` (`deposit.ts`).

##### C-F05-09 · `POST foreign-trade/warehouse-storages/{id}/confirm` (modificado)
- **Política:** `ForeignTradeAccess` (`ForeignTradeController.cs:417-421`). **Petición:** el Id en la ruta, sin cuerpo.
- **Qué cambia** (sobre C-F01-84): los requisitos de C-F05-08; sin cliente confirma y no abre período (D15).
- **Respuesta 200:** `dataSchema(depositStatusResultSchema)` = `{ warehouseStorageId, status: "Confirmed" }`.
- **Errores:** 400 «No se puede confirmar el depósito {N}. Falta: {lista separada por «; »}.» (`DepositConfirmationRequirements.cs:136-138`); 400 «Solo se puede confirmar un depósito en estado Borrador. Estado actual: {estado}.»; 404 «El depósito no existe.».
- **Zod:** `depositStatusResultSchema`.

##### C-F05-10 · `PUT foreign-trade/warehouse-storages/{id}/main-data` (nuevo)
- **Política:** `ForeignTradeAccess` (en `ForeignTradeController`).
- **Qué hace:** guarda P-CE-04 en Borrador y Confirmado (D5, D18), en una transacción; después del commit, un solo recálculo (D19) y, si llega el cliente a un Confirmado sin período, la apertura del primer período (D17). Toda la petición se aplica o nada.
- **Petición:** `depositMainDataSchema`:

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `entryDate` | fecha y hora | Sí | Si cambia: límites de `DEC-012` y `DEC-051` (los de `WarehouseStorage.CorrectEntryDate`, `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs:255-287`) y `entryDateReason` |
| `entryDateReason` | string \| null | Si cambia `entryDate` | 10 a 500 |
| `documentTypeId`, `documentNumber` | guid \| null, string \| null | En importación y exportación | Hasta 50. Corrige el documento del depósito y de sus entradas; no traslada entradas (eso es P-CE-03, `P01/` nota de la fase 4) |
| `documentDate` | `yyyy-MM-dd` \| null | No (lo pide la confirmación, salvo inspección) | No futura |
| `dianManifestNumber`, `dianManifestDate` | string \| null, `yyyy-MM-dd` \| null | No (importación; se ignora en las otras) | Hasta 50; fecha no futura |
| `customerId` | guid \| null | No (AF-75) | Tercero con rol `CUSTOMER`. Con período abierto, no se puede dejar vacío. Con factura, `DEC-056` |
| `importerId`, `customsAgencyId` | guid \| null | No (importación) | Rol `IMPORTER` y `CUSTOMS_AGENCY` |
| `exporterId` | guid \| null | No (exportación) | Rol `EXPORTER` |
| `cpiNetWeight`, `cpiGrossWeight` | decimal \| null | No | > 0 (D14) |
| `cargoValue` | decimal \| null | No (lo pide la confirmación) | > 0; si cambia, queda manual (`P01/` D28) |
| `currency` | `"COP"` \| `"USD"` \| null | Con `cargoValue` | — |
| `inspectionDescription` | string \| null | En inspección | 10 a 500 (`P01/` D23) |
| `observations` | string \| null | No | Hasta 1.000 |

- **Respuesta 200:** `dataSchema(depositEditResultSchema)`:

```jsonc
{ "data": { "warehouseStorageId": "guid", "status": "Confirmed",
            "billingRecalculated": true,     // D19
            "billingPeriodOpened": false,    // D17
            "warnings": [] } }               // advertencias del cobro (DEC-020), como la confirmación
```

- **Errores:**

| Status | Mensaje |
| --- | --- |
| 404 | «El depósito no existe.» |
| 409 | «El depósito {N} está {estado}: ya no se edita.» |
| 409 | «El depósito {N} ya factura a {cliente}: cámbielo por otro cliente, no lo deje vacío.» |
| 409 | los de `DEC-056` de hoy (`DepositCustomerBillingChange`) |
| 400 | «La fecha del documento no puede ser futura.» · «La fecha del manifiesto DIAN no puede ser futura.» |
| 400 | «Indique el motivo del cambio de la fecha de ingreso (de 10 a 500 caracteres).» y los de hoy de la fecha de ingreso (`DEC-051`) |
| 400 | «El tercero {nombre} no tiene el rol {rol}.» |
| 400 | «El valor CPI debe ser mayor que cero.» · «Indique la moneda del valor CPI.» · «La moneda debe ser COP o USD.» |
| 400 | «El peso neto CPI debe ser mayor que cero.» · «El peso bruto CPI debe ser mayor que cero.» |
| 400 | «La descripción de la inspección debe tener entre 10 y 500 caracteres.» |
| 400 | «Indique el tipo y el número del documento comercial.» (importación y exportación) |

- **Zod:** `depositMainDataSchema`, `depositEditResultSchema` (`F/features/foreign-trade/contracts/deposit-edit.ts`).
- **Notas:** el formulario precarga los pesos CPI con `manifestWeightSum` y el valor CPI con `truckValueSum` cuando están vacíos (AF-94, D14). La transportadora no viaja: va por entrada (AF-101).

##### C-F05-11 · `PUT foreign-trade/warehouse-storages/{id}/covered-quantities` (nuevo)
- **Política:** `ForeignTradeAccess`.
- **Qué hace:** guarda la cantidad amparada de los productos del depósito (D13), en Borrador y Confirmado (D18). No mueve stock ni recalcula (D19).
- **Petición:** `coveredQuantitiesSchema` = `{ items: [{ warehouseStorageProductId: guid, coveredQuantity: number ≥ 0 | null }] }` (1 o más; los productos que no vienen no cambian).
- **Respuesta 200:** `dataSchema(coveredQuantitiesResultSchema)` = `{ warehouseStorageId, products: [{ warehouseStorageProductId, enteredQuantity, coveredQuantity, quantityBalance }], pendingStages }`.
- **Errores:** 404 «El depósito no existe.»; 404 «El producto no pertenece al depósito.»; 409 «El depósito {N} está {estado}: ya no se edita.»; 409 «Un depósito de inspección no tiene amparados.»; 400 «La cantidad amparada no puede ser negativa.»
- **Zod:** `coveredQuantitiesSchema`, `coveredQuantitiesResultSchema` (`deposit-edit.ts`).

##### C-F05-12 a C-F05-15 · productos del depósito (modificados)
- **Rutas:** `POST foreign-trade/deposits/{id}/products` (`ForeignTradeController.cs:593-597`), `PUT …/products/{storageProductId}` (`:621-625`), `DELETE …/products/{storageProductId}` (`:651-655`) y `PUT …/products/{storageProductId}/catalog-product` (`DepositCompletionController.cs:53`).
- **Política:** `ForeignTradeAccess` en las cuatro, la de hoy.
- **Qué cambia:** aceptan Borrador y Confirmado (D18; `DepositProductEditing.LoadEditableStorageAsync`, `B/Wms.Application/ForeignTrade/Common/Services/DepositProductEditing.cs:145-161`); con el depósito confirmado, recalculan (D19). C-F05-13 no deja una cantidad por debajo de lo levantado más lo despachado; C-F05-14 y C-F05-15 no aceptan un producto con levante o salida.
- **Petición:** la de hoy: `AddDepositProductRequest` (`ForeignTradeController.cs:1004-1011`), `UpdateDepositProductRequest` (`:1014-1019`), `RemoveDepositProductRequest` (`:1022`) y `ChangeDepositLineProductRequest` (`B/Wms.Api/Controllers/v1/Requests/DepositCompletionRequests.cs:6`).
- **Respuesta:** la de hoy (C-F05-12 a C-F05-14: 200 sin datos o el producto; C-F05-15: `ChangeDepositLineProductResultDto`); la pantalla vuelve a leer el detalle.
- **Errores:** los de hoy, más 409 «El depósito {N} está {estado}: ya no se edita.»; 409 «{producto}: la cantidad no puede quedar en {q}; ya tiene {l} levantado y {d} despachado.»; 409 «{producto} ya tiene levantes o salidas: no se puede quitar.» (`EntryCorrectionRules.cs:52-56`). Sale «Solo se pueden editar los productos de un depósito en Borrador.» (`WarehouseStorage.cs:567-569`).
- **Zod:** `depositProductCreateSchema`, `depositProductUpdateSchema`, `depositProductRemoveSchema`, `depositLineProductChangeSchema` (`deposit-edit.ts`).

##### C-F05-16 a C-F05-20 · edición en Borrador y «Devolver a Borrador» (retirados)
- `PATCH foreign-trade/warehouse-storages/{id}/draft` (`ForeignTradeController.cs:437-441`), `PATCH …/customer` (`:346-350`), `PUT …/stakeholders` (`:389-393`, C-F01-89), `PATCH foreign-trade/imports/{id}/manifest` (`:239-243`) y `POST …/return-for-correction` (`:490-494`). **Política de hoy:** `ForeignTradeAccess`. **Los reemplazan:** C-F05-10 (los cuatro primeros) y nada (el último, AF-93). Petición, respuesta, errores y Zod: no aplica; 404 desde BE-1. Se borran sus comandos, handlers, validadores y pruebas (`UpdateDraftDeposit`, `AssignDepositCustomer`, `UpdateDepositStakeholders`, `UpdateManifestInfo`, `ReturnStorageForCorrection`); sus reglas de facturación pasan a C-F05-10. `GET …/stakeholders` (`:369-373`) se conserva sin cambios.

##### C-F05-21 · `POST exits/{id}/confirm` (modificado)
- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/ExitsController.cs:69-70`). **Petición:** la de C-F01-98. **Respuesta 200:** la de C-F01-98.
- **Qué cambia:** antes de mover stock, cada depósito de las líneas debe tener cliente (D21).
- **Errores nuevos:** 409 «Asigne el cliente del depósito {N} antes de confirmar la salida.». Los de C-F01-98 siguen.
- **Zod:** los de C-F01-98 (`F/features/exits/contracts/exit.ts`). **Notas:** la pantalla es de F06 (P-CE-11).

#### Grupo B — Entradas, tickets y listados con el patrón

##### C-F05-22 · `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` (modificado)
- **Política:** `ForeignTradeAccess` (`ForeignTradeController.cs:538-541`). **Petición:** el Id del depósito en la ruta.
- **Qué cambia** (sobre C-F04-05; D25): cada entrada suma `entryLogId`, `dateTimeEntry` (hora de Vigilancia), `driverName` (nulo sin conductor), `quantity` (suma de lo declarado) y `canEdit`.
- **Respuesta 200:** `dataSchema(z.array(depositEntryRowSchema))`.
- **Errores:** los de hoy. **Zod:** `depositEntryRowSchema` (`F/features/foreign-trade/contracts/deposit-entry.ts`; extiende `depositEntryWithReceptionSchema` de F04).
- **Notas:** el DTO es el mismo de C-F03-13 (`DepositStorageEntryDto`); Báscula no declara los campos nuevos y su pantalla no cambia (Zod descarta lo que no declara).

##### C-F05-23 · `PUT foreign-trade/entries/{entryId}` (modificado)
- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/EntryCorrectionController.cs:84-85`).
- **Qué cambia** (sobre C-F01-90; D6, D26): suma los datos de Vigilancia y la moneda del depósito.
- **Petición:** `entryCorrectionCeSchema` de C-F01-90 con estos campos nuevos:

| Campo nuevo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `licensePlate` | string \| null | No (nulo = no cambia) | Como C-F01-07; mayúsculas sin espacios |
| `entryReasonId` | guid \| null | No | Motivo activo; si el camión ya tiene un ciclo guardado, de la misma categoría (C-F01-07) |
| `dateTimeEntry` | fecha y hora \| null | No | Límites de hoy de C-F01-07 (`DEC-012`, `DEC-051`); no futura |
| `currency` | `"COP"` \| `"USD"` \| null | No | Moneda del depósito (AF-94); recalcula (D19) |

- **Respuesta 200:** `dataSchema(depositEntrySchema)` (la de hoy).
- **Errores:** los de C-F01-90, más los de hoy de C-F01-07 para esos campos: 409 «El camión {placa} ya tiene un registro de {categoría actual}: para cambiarlo a {categoría nueva}, anule el pesaje y regístrelo de nuevo.» y los límites de fecha. CE no recibe el 409 «… la corrección la hace Comercio Exterior.» (`EntryCorrectionRules.cs:49-50`), que es de Báscula.
- **Zod:** `entryCorrectionCeSchema` ampliado (`deposit-entry.ts`).
- **Notas:** la auditoría guarda los cambios de Vigilancia en el ingreso (`EntryLog`) y los demás en la entrada, como hoy; el aviso de «Modificación de peso» sigue la regla de `P01/` D30.

##### C-F05-24 · `GET weighbridge/storage/document-candidates` (modificado)
- **Política:** `EntryEditAccess` (Admin, Scale, ForeignTrade); antes `ScaleAccess` por la clase de `WeighbridgeController` (`:65`). Pasa a `EntryCorrectionController` (D27). **Petición:** la de C-F03-52. **Respuesta 200:** la de C-F03-52. **Errores:** los de C-F03-52. Sin cambios en ninguno.
- **Zod:** el de C-F03-52 (`F/features/weighbridge/contracts/registration.ts`). **Notas:** P-CE-03 lo llama al cambiar el documento, para elegir el depósito (`DEC-057` D1).

##### C-F05-25 · `GET foreign-trade/entry-tickets` (nuevo)
- **Política:** `ForeignTradeAccess`. Orden y filtros (C-F01-00).
- **Petición (consulta):** paginación; `dateTimeEntryFrom`, `dateTimeEntryTo`; `vehiclePlate`, `driverName`, `ticketNumber`, `product`, `warehouseStorageNumber` (texto, contiene); `modality` (enum, varios: `Import`, `Export`, `Inspection`).
- **Orden:** lista blanca `dateTimeEntry`, `vehiclePlate`, `driverName`, `ticketNumber`, `warehouseStorageNumber`; por defecto `dateTimeEntry desc`.
- **Respuesta 200:** `pagedSchema(entryTicketRowSchema)`:

```jsonc
{ "data": [ { "warehouseStorageEntryId": "guid", "entryLogId": "guid", "weighbridgeCycleId": "guid",
  "dateTimeEntry": "2026-11-02T09:40:00-05:00", "vehiclePlate": "IAA111", "driverName": "Conductor 1",
  "ticketNumber": "2026T00298", "merchandise": [ { "productName": "Cebolla", "packaging": "Sacos", "quantity": 720 } ],
  "grossWeight": 44820, "merchandiseWeight": 32980, "tareWeight": 11840, "quantity": 720, "manifestWeight": 33000,
  "modality": "Import", "warehouseStorageId": "guid", "importDepositId": "guid",
  "warehouseStorageNumber": "2026BA00003", "warehouseStorageStatus": "Confirmed", "canEdit": true } ],
  "pagination": { … } }
```

- **Reglas:** solo entradas de almacenamiento no anuladas de depósitos no anulados (D28); `canEdit` = regla de CE (siempre `true` con esas condiciones; queda en el contrato por si cambia la regla).
- **Errores:** los de C-F01-00. **Zod:** `entryTicketListQuerySchema`, `entryTicketRowSchema` (`F/features/foreign-trade/contracts/entry-ticket.ts`).

##### C-F05-26 · `GET foreign-trade/abandonment` (modificado)
- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/AbandonmentController.cs:20`, `:53`). Orden y filtros (C-F01-00).
- **Petición (consulta):** los filtros de hoy (`status`, `hasExtension`, `warehouseStorageNumber`, `cargoManifestNumber`, `importerId`, `customsAgencyId`; `B/Wms.Application/ForeignTrade/Queries/GetAbandonmentList/GetAbandonmentListQuery.cs:15-20`), con `warehouseStorageNumber` y `cargoManifestNumber` como «contiene», más `importerName`, `customsAgencyName` y `customerName` (texto) y `entryDateFrom`, `entryDateTo`.
- **Orden:** lista blanca `warehouseStorageNumber`, `entryDate`, `daysRemaining`, `status`, `importerName`; por defecto `daysRemaining asc` (el de hoy, `B/Wms.Application/ForeignTrade/Common/Services/AbandonmentReader.cs:81`).
- **Respuesta 200:** `pagedSchema(abandonmentItemSchema)` (`AbandonmentItemDto`, sin cambios). **Errores:** los de C-F01-00. **Zod:** `abandonmentListQuerySchema`, `abandonmentItemSchema` (`F/features/foreign-trade/contracts/abandonment.ts`).

##### C-F05-27 · `GET foreign-trade/packing-lists` (modificado)
- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/PackingListsController.cs:27`, `:101`). Orden y filtros (C-F01-00).
- **Petición (consulta):** los de hoy (`importerId`, `supplierId`) más `fileName`, `importerName` y `supplierName` (texto) y `createdAtFrom`, `createdAtTo`.
- **Orden:** lista blanca `createdAt`, `fileName`, `importerName`, `supplierName`; por defecto `createdAt desc` (el de hoy, `GetPackingListsQuery.cs:34`).
- **Respuesta 200:** `pagedSchema(packingListFileSchema)` (`PackingListFileDto`, sin cambios). **Errores:** los de C-F01-00. **Zod:** `packingListQuerySchema`, `packingListFileSchema` (`F/features/foreign-trade/contracts/packing-list.ts`).

##### C-F05-28 · `GET foreign-trade/packing-list-items` (modificado)
- **Política:** `ForeignTradeAccess` (`PackingListsController.cs:134`). Orden y filtros (C-F01-00).
- **Petición (consulta):** los de hoy (`importerId` obligatorio, `status`, `search`) más `code`, `description` y `warehouseStorageNumber` (texto).
- **Orden:** lista blanca `code`, `description`, `quantity`, `netWeightKg`; por defecto `code asc` (el de hoy, `GetPackingListItemsQuery.cs:49`).
- **Respuesta 200:** `pagedSchema(packingListItemSchema)` (`PackingListItemDto`, sin cambios). **Errores:** los de hoy («Indique el importador.» del validador) y los de C-F01-00. **Zod:** `packingListItemQuerySchema`, `packingListItemSchema`.
- **Nota para BE-2:** confirma con grep los nombres de las columnas de `PackingListFileDto` y `PackingListItemDto`; si alguno de la lista blanca no existe, usa el nombre del DTO y lo anota en §8.2 (`DEC-002`).

#### Grupo C — Levantes e inventario nacionalizado

##### C-F05-29 · `POST foreign-trade/imports/{id}/releases` (modificado)
- **Política:** `ForeignTradeAccess` (`ForeignTradeController.cs:170-174`). **Petición:** `RegisterImportReleaseRequest` (`:974-985`) sin `acceptanceDate` (D9); si llega, se ignora.
- **Qué cambia:** `AcceptanceDate` = `ReleaseDate`; los mensajes dicen «valor en aduanas» (D31).
- **Respuesta 200:** la de hoy (el detalle de importación, C-F05-05).
- **Errores:** los de hoy, con el rótulo: «Digite la tasa de cambio para registrar el valor en aduanas.»; «El valor en aduanas no puede ser negativo.»; «El valor en aduanas admite máximo 2 decimales.»; «El valor en aduanas del levante {N} ya se registró con «{producto}». …» (`DEC-029` §7.8). Sale «La fecha de aceptación es requerida.» (`RegisterImportReleaseCommandValidator.cs:29-31`).
- **Zod:** `releaseRegisterSchema`, `depositDetailSchema` (`F/features/foreign-trade/contracts/release.ts`).

##### C-F05-30 · `PATCH foreign-trade/imports/{id}/releases/{releaseId}` (modificado)
- **Política:** `ForeignTradeAccess` (`:203-207`). **Petición:** `UpdateImportReleaseRequest` (`:991-1001`) sin `acceptanceDate`.
- **Qué cambia:** `AcceptanceDate` = `ReleaseDate`; con `manualExchangeRate` distinto de la tasa guardada, la cambia y recalcula el valor en pesos (D30); rótulo (D31).
- **Respuesta 200:** la de hoy (el detalle de importación, C-F05-05). **Errores:** los de hoy, con el rótulo de C-F05-29; sale «La fecha de aceptación es requerida.» (`UpdateImportReleaseCommandValidator.cs`). **Zod:** `releaseUpdateSchema`, `depositDetailSchema`.

##### C-F05-31 · `POST foreign-trade/imports/{id}/releases/{releaseId}/withdraw` (modificado)
- **Política:** `ForeignTradeAccess` (`B/Wms.Api/Controllers/v1/ImportReleaseActionsController.cs:18`, `:32`). **Petición:** `{ reason }`, la de hoy. **Respuesta 200:** la de hoy. **Errores:** los de hoy. El texto de la nota del producto heredero dice « El valor en aduanas pasó al producto «{producto}».» (`WithdrawImportReleaseCommandHandler.cs:93`). **Zod:** `releaseWithdrawSchema` (`{ reason }`), `releaseWithdrawResultSchema` (la respuesta de hoy, `F/features/foreign-trade/types/import-deposit.ts`).

##### C-F05-32 · `GET foreign-trade/releases` (modificado)
- **Política:** `ForeignTradeAccess` (`ReleasesController.cs:17`, `:23`). Orden y filtros (C-F01-00).
- **Qué cambia:** de una fila por levante a una por depósito de importación confirmado o cerrado (D10, D32). Salen `releaseNumber`, `importerId`, `customsAgencyId`, `fromDate` y `toDate` (`GetReleasesQuery.cs`).
- **Petición (consulta):** paginación; `search` (número de depósito, documento, importador, mercancía o número de levante); `nationalizationStatus` (enum, varios: `NotNationalized`, `Partial`, `Nationalized`); `withWeightDifference` (bool); `entryDateFrom`, `entryDateTo`.
- **Orden:** lista blanca `entryDate`, `warehouseStorageNumber`, `nationalizedPercent`; por defecto `entryDate desc`.
- **Respuesta 200:** `pagedSchema(releaseDepositRowSchema)`:

```jsonc
{ "data": [ { "importDepositId": "guid", "warehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00003",
  "entryDate": "2026-11-02T09:40:00-05:00", "documentTypeName": "Carta porte", "documentNumber": "EC0001",
  "dianManifestNumber": "1165750", "importerName": "Importador A",
  "merchandise": [ { "productName": "Cebolla", "packaging": "Sacos" } ],
  "enteredQuantity": 760, "enteredWeight": 44820, "nationalizedQuantity": 300, "nationalizedWeight": 17700,
  "nationalizedPercent": 39.47, "balanceQuantity": 460, "balanceWeight": 27120,
  "nationalizationStatus": "Partial", "hasWeightDifference": false, "releaseCount": 2 } ],
  "pagination": { … } }
```

- **Errores:** los de C-F01-00. **Zod:** `releaseDepositQuerySchema`, `releaseDepositRowSchema` (`release.ts`).

##### C-F05-33 · `GET foreign-trade/releases/summary` (nuevo)
- **Política:** `ForeignTradeAccess`. **Petición (consulta):** `search`, `entryDateFrom`, `entryDateTo` (los de C-F05-32 sin el estado).
- **Respuesta 200:** `dataSchema(releaseSummarySchema)` = `{ total, notNationalized, partial, nationalized, withWeightDifference }` (enteros).
- **Errores:** 400 «La fecha inicial no puede ser posterior a la final.». **Zod:** `releaseSummarySchema`.

##### C-F05-34 · `GET reports/nationalized-inventory` (nuevo)
- **Política:** `ForeignTradeAccess` (controlador nuevo `NationalizedInventoryReportController`, ruta `reports`).
- **Petición (consulta):** `releaseDateFrom`, `releaseDateTo` (`yyyy-MM-dd`, obligatorios, rango de hasta 366 días).
- **Respuesta 200:** `dataSchema(nationalizedInventorySchema)`:

```jsonc
{ "data": { "releaseDateFrom": "2026-11-01", "releaseDateTo": "2026-11-30",
  "deposits": [ { "warehouseStorageNumber": "2026BA00003", "documentTypeName": "Carta porte", "documentNumber": "EC0001",
    "customsAgencyName": "Agencia A", "importerName": "Importador A", "customerName": "Cliente A",
    "products": [ { "productName": "Cebolla", "packaging": "Sacos", "entryDate": "2026-11-02T09:40:00-05:00",
      "dianManifestNumber": "1165750", "enteredQuantity": 760, "currentStock": 460, "nationalizedQuantity": 300,
      "releases": [ { "releaseNumber": "37202600011", "acceptanceNumber": "48202600022", "releaseDate": "2026-11-05",
                      "quantity": 300, "weight": 17700, "customsValueUsd": 8000.00 } ] } ] } ],
  "totals": { "enteredQuantity": 760, "currentStock": 460, "nationalizedQuantity": 300 } } }
```

- **Errores:** 400 «Indique el rango de fechas de los levantes.»; 400 «La fecha inicial no puede ser posterior a la final.»; 400 «El rango no puede pasar de 366 días.»
- **Zod:** `nationalizedInventoryQuerySchema`, `nationalizedInventorySchema` (`F/features/reports/contracts/nationalized-inventory.ts`).

##### C-F05-35 · `GET reports/nationalized-inventory/pdf` (nuevo)
- **Política:** `ForeignTradeAccess`. **Petición:** la de C-F05-34. **Respuesta 200:** `application/pdf` («inventario-nacionalizado-{desde}-{hasta}.pdf»), con el formato del legacy y las firmas «Jefe de Bodega» y «Recibí conforme» (QuestPDF). **Errores:** los de C-F05-34. **Zod:** no aplica (archivo); la consulta usa `nationalizedInventoryQuerySchema`.

##### C-F05-36 · `GET warehouse/movements-report/pdf` (modificado)
- **Política:** `InventoryReportAccess` (`B/Wms.Api/Controllers/v1/WarehouseMovementsReportController.cs:63-64`). **Petición:** la de C-F01-161. **Respuesta 200:** el PDF de hoy. **Errores:** los de C-F01-161. **Qué cambia:** la columna «CIF USD» del PDF dice «Valor en aduanas (USD)» (D31; `WarehouseMovementsPdfService.cs:282`). **Zod:** no aplica (archivo).

#### Grupo D — De hoy, sin cambios

Petición, respuesta y errores son los de hoy; ninguno cambia. La maquetación los simula con estos esquemas (`F/features/foreign-trade/contracts/deposit-misc.ts`, salvo C-F05-48 y C-F05-50).

| ID | Petición | Respuesta 200 | Errores de hoy | Zod |
| --- | --- | --- | --- | --- |
| C-F05-40 | Ids en la ruta; `action` | PDF | 404 del depósito o del camión; 409 del camión anulado | no aplica (archivo) |
| C-F05-41 | Id en la ruta | PDF | 404 del depósito | no aplica (archivo) |
| C-F05-42 | Id en la ruta | `{ warehouseStorageId, printCount, downloadCount, lastPrintedAt, lastPrintedByName, items[] }` (`F/features/foreign-trade/types/label-prints.ts:8-24`) | 404 | `labelPrintsSchema` |
| C-F05-43 | `{ notes? }` | el resultado de la prórroga (`IStorageExtensionResultDto`, `F/features/foreign-trade/types/import-deposit.ts:308-…`) | 404; 409 de la segunda prórroga | `extensionRequestSchema`, `extensionResultSchema` |
| C-F05-44 | `{ reason }` (10 a 500) | `{ warehouseStorageId, status, removedOrderItems, cancelledOrders[], closedPeriods, cancelledInvoices[], invoicesToReview[] }` (`F/features/foreign-trade/types/deposit-kanban.ts:153-167`) | 400 cerrado o ya anulado; 400 motivo | `cancelDepositSchema`, `cancelDepositResultSchema` |
| C-F05-45 | Id del tercero en la ruta | `{ stakeholderId, stakeholderName, financialStatus: "Active"\|"OverdueWarning"\|"Blocked", overdueAmount, canProceed, blockReason? }` | 404 | `clientFinancialStatusSchema` |
| C-F05-46 | `{ shippingFormNumber }` (hasta 100, nulo para quitarla) | `{ warehouseStorageId, shippingFormNumber }` | 400 anulado; 400 largo | `shippingFormNumberSchema`, `shippingFormNumberResultSchema` |
| C-F05-47 | `{ units: [{ warehouseStorageCargoUnitId, products: [{ warehouseStorageProductId, declaredQuantity }] }], reason }` | la de hoy | 404 del camión; 400 del reparto | `cargoUnitBreakdownSchema` |
| C-F05-48 | `{ warehouseStorageProductId, newReceivedQuantity, observations?, warehouseStorageCargoUnitId? }` | la de hoy | los de hoy | `inventoryAdjustmentSchema` (`F/features/warehouse/contracts/inventory.ts`, que ya lo tiene o lo suma) |
| C-F05-49 | — | `{ inAlert, abandoned }` | — | `abandonmentSummarySchema` (`abandonment.ts`) |
| C-F05-50 | los de hoy | los de hoy (`F/features/foreign-trade/types/packing-list.ts`) | los de hoy | `packing-list.ts` (esquemas con los campos de los tipos de hoy) |


### 2.3 Esquemas Zod y tipos

Zod 4 (`Frontend/wms/package.json`: `"zod": "^4.1.13"`), con las ayudas de `F/shared/contracts/api.ts` (`guidSchema` = `z.guid()`, `dateTimeSchema` = `z.iso.datetime({ offset: true })`, `dateOnlySchema` = `z.iso.date()`, `dataSchema`, `pagedSchema`, `listQueryBaseSchema`, `reasonSchema`). Los tipos se derivan con `z.infer`. FE-1 escribe todos los archivos; los de los grupos que no maqueta en FE-1 quedan listos para FE-2 y FE-3.

**`F/features/foreign-trade/contracts/deposit.ts`** (FE-1; C-F05-01, C-F05-05 a C-F05-09):

```ts
import { z } from "zod";
import { dataSchema, dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema, pagedSchema } from "~/shared/contracts/api";
import { clockLevelSchema } from "~/features/warehouse/contracts/clock";
import { importReleaseSchema } from "./release";

export const depositModalitySchema = z.enum(["Import", "Export", "Inspection"]);
export const depositStatusSchema = z.enum(["Draft", "Confirmed", "Closed", "Cancelled"]);
export const depositStageSchema = z.enum(["Entries", "MainData", "Warehouse", "Coverage", "Releases", "Exits"]);
export const nationalizationStatusSchema = z.enum(["NotNationalized", "Partial", "Nationalized"]);
export const currencySchema = z.enum(["COP", "USD"]);

export const merchandiseNameSchema = z.object({ productName: z.string(), packaging: z.string().nullable() });
export const depositWeightsSchema = z.object({
  gross: z.number().nullable(), merchandise: z.number().nullable(), tare: z.number().nullable(), manifest: z.number().nullable(),
});
export const depositCoverageSchema = z.object({
  enteredQuantity: z.number(),
  coveredQuantity: z.number().nullable(),      // nulo en inspección
  quantityBalance: z.number().nullable(),
  enteredWeight: z.number().nullable(),
  coveredWeight: z.number().nullable(),        // D14: peso bruto CPI o suma de manifiestos
  weightBalance: z.number().nullable(),
});
export const depositListProductSchema = z.object({
  warehouseStorageProductId: guidSchema,
  productName: z.string(),
  packaging: z.string().nullable(),
  enteredQuantity: z.number(),
  coveredQuantity: z.number().nullable(),
  quantityBalance: z.number().nullable(),
});

// C-F05-01
export const depositListQuerySchema = listQueryBaseSchema.extend({
  modality: depositModalitySchema,
  status: depositStatusSchema.optional(),
  entryDateFrom: dateOnlySchema.optional(),
  entryDateTo: dateOnlySchema.optional(),
  warehouseStorageNumber: z.string().optional(),
  document: z.string().optional(),
  ticketNumber: z.string().optional(),
  product: z.string().optional(),
});
export const depositListRowSchema = z.object({
  warehouseStorageId: guidSchema,
  importDepositId: guidSchema.nullable(),
  warehouseStorageNumber: z.string(),
  modality: depositModalitySchema,
  status: depositStatusSchema,
  entryDate: dateTimeSchema.nullable(),
  vehiclePlates: z.array(z.string()),
  ticketNumbers: z.array(z.string()),
  documentTypeName: z.string().nullable(),
  documentNumber: z.string().nullable(),
  inspectionDescription: z.string().nullable(),
  customerName: z.string().nullable(),
  importerName: z.string().nullable(),
  exporterName: z.string().nullable(),
  merchandise: z.array(merchandiseNameSchema),
  weights: depositWeightsSchema,
  dianManifestNumber: z.string().nullable(),
  cargoValue: z.number().nullable(),
  currency: z.string().nullable(),
  products: z.array(depositListProductSchema),
  coverage: depositCoverageSchema,
  nationalizationStatus: nationalizationStatusSchema.nullable(),
  pendingStages: z.array(depositStageSchema),
  warehouseLevel: clockLevelSchema,
});
export const depositListResponseSchema = pagedSchema(depositListRowSchema);

// C-F05-05 a C-F05-07 — solo lo que usan las pantallas de F05; el DTO trae más.
export const depositServiceStakeholderSchema = z.object({
  stakeholderId: guidSchema,
  stakeholderName: z.string(),
  idNumber: z.string().nullable(),
  idType: z.string().nullable(),
  roleCode: z.string(),
  roleName: z.string(),
  isCustomer: z.boolean(),
});
export const depositDetailProductSchema = z.object({
  id: guidSchema,
  productId: guidSchema,
  productName: z.string().nullable(),
  productDescription: z.string().nullable(),
  packagingTypeId: guidSchema.nullable(),
  packagingTypeName: z.string().nullable(),
  declaredQuantity: z.number().nullable(),
  currentStock: z.number(),
  reservedStock: z.number(),
  availableStock: z.number(),
  canDelete: z.boolean(),
  blockReason: z.string().nullable(),
  enteredQuantity: z.number(),
  coveredQuantity: z.number().nullable(),
  quantityBalance: z.number().nullable(),
  releasedQuantity: z.number(),
  releasedWeight: z.number(),
  dispatchedQuantity: z.number(),
  entryWeight: z.number().nullable(),
  nationalizationStatus: nationalizationStatusSchema.nullable(),
  hasWeightDifference: z.boolean().nullable(),
  locations: z.array(z.string()),
  entries: z.array(z.object({
    warehouseStorageEntryId: guidSchema, vehiclePlate: z.string().nullable(), declaredQuantity: z.number().nullable(),
  })).nullable(),
});
export const depositDetailSchema = z.object({
  warehouseStorageId: guidSchema,
  id: guidSchema,                                   // importación: Id de ImportWarehouseStorage; las otras: el del depósito
  warehouseStorageNumber: z.string(),
  warehouseStorageStatus: z.string(),               // "Draft" | "Confirmed" | "Closed" | "Cancelled" (texto de hoy)
  manifestNumber: z.string().nullable().optional(), // manifiesto DIAN (importación)
  manifestDate: dateTimeSchema.nullable().optional(),
  customerId: guidSchema.nullable(),
  customerName: z.string().nullable(),
  documentTypeId: guidSchema.nullable(),
  primaryDocumentTypeName: z.string().nullable(),
  cargoManifestNumber: z.string().nullable(),       // número del documento comercial (trampa 9)
  documentDate: dateTimeSchema.nullable(),
  entryDate: dateTimeSchema.nullable(),
  currency: z.string().nullable(),
  cargoValue: z.number().nullable(),
  cargoValueIsManual: z.boolean(),
  truckValueSum: z.number().nullable(),
  carriers: z.array(z.string()),
  merchandiseWeight: z.number().nullable(),
  shippingFormNumber: z.string().nullable(),
  observations: z.string().nullable(),
  cancelledAt: dateTimeSchema.nullable(),
  cancellationReason: z.string().nullable(),
  crewName: z.string().nullable(),
  inspectionDescription: z.string().nullable().optional(),
  extensionRegisteredAt: dateTimeSchema.nullable().optional(),
  serviceStakeholders: z.array(depositServiceStakeholderSchema),
  products: z.array(depositDetailProductSchema),
  releases: z.array(importReleaseSchema).optional(), // solo importación
  cpiNetWeight: z.number().nullable(),
  cpiGrossWeight: z.number().nullable(),
  manifestWeightSum: z.number().nullable(),
  coverage: depositCoverageSchema,
  stages: z.array(depositStageSchema),
  pendingStages: z.array(depositStageSchema),
  warehouseLevel: clockLevelSchema,
  nationalizationStatus: nationalizationStatusSchema.nullable().optional(),
});
export const depositDetailResponseSchema = dataSchema(depositDetailSchema);

// C-F05-08 y C-F05-09
export const missingRequirementSchema = z.object({ code: z.string(), message: z.string() });
export const confirmationRequirementsSchema = z.object({
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  canConfirm: z.boolean(),
  missing: z.array(missingRequirementSchema),
});
export const depositStatusResultSchema = z.object({ warehouseStorageId: guidSchema, status: z.string() });

export type DepositModality = z.infer<typeof depositModalitySchema>;
export type DepositStage = z.infer<typeof depositStageSchema>;
export type DepositListQuery = z.infer<typeof depositListQuerySchema>;
export type DepositListRow = z.infer<typeof depositListRowSchema>;
export type DepositDetail = z.infer<typeof depositDetailSchema>;
export type DepositDetailProduct = z.infer<typeof depositDetailProductSchema>;
export type ConfirmationRequirements = z.infer<typeof confirmationRequirementsSchema>;
```

**`F/features/foreign-trade/contracts/deposit-entry.ts`** (FE-1 amplía el archivo de hoy; C-F05-22, C-F05-23):

```ts
// Se suma al final del archivo de hoy (depositEntrySchema, entryCorrectionCeSchema y los de F04 no cambian de nombre).
export const depositEntryRowSchema = depositEntryWithReceptionSchema.extend({
  entryLogId: guidSchema,
  dateTimeEntry: dateTimeSchema.nullable(),
  driverName: z.string().nullable(),
  quantity: z.number(),
  canEdit: z.boolean(),
});
export const depositEntriesResponseSchema = dataSchema(z.array(depositEntryRowSchema));

// C-F05-23 — entryCorrectionCeSchema de hoy suma Vigilancia y moneda (se edita en su lugar):
//   licensePlate: z.string().trim().min(1).max(15).nullable(),
//   entryReasonId: guidSchema.nullable(),
//   dateTimeEntry: dateTimeSchema.nullable(),
//   currency: z.enum(["COP", "USD"]).nullable(),
export type DepositEntryRow = z.infer<typeof depositEntryRowSchema>;
```

**`F/features/foreign-trade/contracts/deposit-edit.ts`** (FE-1; C-F05-10 a C-F05-15):

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, reasonSchema } from "~/shared/contracts/api";
import { currencySchema, depositStageSchema } from "./deposit";

export const depositMainDataSchema = z.object({
  entryDate: dateTimeSchema,
  entryDateReason: reasonSchema.nullable(),
  documentTypeId: guidSchema.nullable(),
  documentNumber: z.string().trim().max(50).nullable(),
  documentDate: dateOnlySchema.nullable(),
  dianManifestNumber: z.string().trim().max(50).nullable(),
  dianManifestDate: dateOnlySchema.nullable(),
  customerId: guidSchema.nullable(),
  importerId: guidSchema.nullable(),
  customsAgencyId: guidSchema.nullable(),
  exporterId: guidSchema.nullable(),
  cpiNetWeight: z.number().positive().nullable(),
  cpiGrossWeight: z.number().positive().nullable(),
  cargoValue: z.number().positive().nullable(),
  currency: currencySchema.nullable(),
  inspectionDescription: z.string().trim().min(10).max(500).nullable(),
  observations: z.string().trim().max(1000).nullable(),
});
export const depositEditResultSchema = z.object({
  warehouseStorageId: guidSchema,
  status: z.string(),
  billingRecalculated: z.boolean(),
  billingPeriodOpened: z.boolean(),
  warnings: z.array(z.string()),
});

export const coveredQuantitiesSchema = z.object({
  items: z.array(z.object({
    warehouseStorageProductId: guidSchema,
    coveredQuantity: z.number().min(0).nullable(),
  })).min(1),
});
export const coveredQuantitiesResultSchema = z.object({
  warehouseStorageId: guidSchema,
  products: z.array(z.object({
    warehouseStorageProductId: guidSchema,
    enteredQuantity: z.number(),
    coveredQuantity: z.number().nullable(),
    quantityBalance: z.number().nullable(),
  })),
  pendingStages: z.array(depositStageSchema),
});

// C-F05-12 a C-F05-15: las peticiones de hoy (ForeignTradeController.cs:1004-1022; DepositCompletionRequests.cs:6).
export const depositProductCreateSchema = z.object({
  warehouseStorageEntryId: guidSchema,
  productId: guidSchema,
  productDescription: z.string().trim().max(500).nullable(),
  packagingTypeId: guidSchema.nullable(),
  declaredQuantity: z.number().positive(),
  warehouseStorageCargoUnitId: guidSchema.nullable(),
  reason: reasonSchema,
});
export const depositProductUpdateSchema = z.object({
  productDescription: z.string().trim().max(500).nullable(),
  packagingTypeId: guidSchema.nullable(),
  entries: z.array(z.object({ warehouseStorageEntryId: guidSchema, declaredQuantity: z.number().min(0) })).nullable(),
  units: z.array(z.object({ warehouseStorageCargoUnitId: guidSchema, declaredQuantity: z.number().min(0) })).nullable(),
  reason: reasonSchema,
});
export const depositProductRemoveSchema = z.object({ reason: reasonSchema });
export const depositLineProductChangeSchema = z.object({ productId: guidSchema, reason: reasonSchema });

export type DepositMainData = z.infer<typeof depositMainDataSchema>;
export type DepositEditResult = z.infer<typeof depositEditResultSchema>;
export type CoveredQuantities = z.infer<typeof coveredQuantitiesSchema>;
```

**`F/features/foreign-trade/contracts/entry-ticket.ts`** (FE-1; C-F05-25):

```ts
import { z } from "zod";
import { dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema, pagedSchema } from "~/shared/contracts/api";
import { depositModalitySchema } from "./deposit";

export const entryTicketListQuerySchema = listQueryBaseSchema.extend({
  dateTimeEntryFrom: dateOnlySchema.optional(),
  dateTimeEntryTo: dateOnlySchema.optional(),
  vehiclePlate: z.string().optional(),
  driverName: z.string().optional(),
  ticketNumber: z.string().optional(),
  product: z.string().optional(),
  warehouseStorageNumber: z.string().optional(),
  modality: z.array(depositModalitySchema).optional(),   // se envía separado por comas (C-F01-00)
});
export const entryTicketRowSchema = z.object({
  warehouseStorageEntryId: guidSchema,
  entryLogId: guidSchema,
  weighbridgeCycleId: guidSchema.nullable(),
  dateTimeEntry: dateTimeSchema.nullable(),
  vehiclePlate: z.string().nullable(),
  driverName: z.string().nullable(),
  ticketNumber: z.string().nullable(),
  merchandise: z.array(z.object({ productName: z.string(), packaging: z.string().nullable(), quantity: z.number().nullable() })),
  grossWeight: z.number().nullable(),
  merchandiseWeight: z.number().nullable(),
  tareWeight: z.number().nullable(),
  quantity: z.number(),
  manifestWeight: z.number().nullable(),
  modality: depositModalitySchema,
  warehouseStorageId: guidSchema,
  importDepositId: guidSchema.nullable(),
  warehouseStorageNumber: z.string(),
  warehouseStorageStatus: z.string(),
  canEdit: z.boolean(),
});
export const entryTicketListResponseSchema = pagedSchema(entryTicketRowSchema);
export type EntryTicketRow = z.infer<typeof entryTicketRowSchema>;
```

**`F/features/foreign-trade/contracts/release.ts`** (FE-1; C-F05-29 a C-F05-33):

```ts
import { z } from "zod";
import { dataSchema, dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema, pagedSchema, reasonSchema } from "~/shared/contracts/api";

export const exchangeRateSourceSchema = z.enum(["Weekly", "WeeklyFallback", "Manual"]);
export const importReleaseSchema = z.object({          // ImportReleaseDto (B/…/DTOs/ImportReleaseDto.cs:5-21)
  id: guidSchema,
  warehouseStorageProductId: guidSchema,
  releaseNumber: z.string(),
  releaseDate: dateTimeSchema,
  acceptanceNumber: z.string(),
  acceptanceDate: dateTimeSchema,                      // D9: igual a releaseDate
  releasedQuantity: z.number(),
  releasedWeight: z.number(),
  observations: z.string().nullable(),
  fobUsd: z.number().nullable(),                       // «Valor en aduanas (USD)» (AF-81)
  exchangeRate: z.number().nullable(),
  exchangeRateSource: exchangeRateSourceSchema.nullable(),
  exchangeRateDate: dateOnlySchema.nullable(),
  fobCop: z.number().nullable(),                       // «Valor en aduanas (COP)»
  createdAt: dateTimeSchema,
});

const releaseBodyBase = z.object({
  releaseNumber: z.string().trim().min(1).max(100),
  releaseDate: dateTimeSchema,
  acceptanceNumber: z.string().trim().min(1).max(100),
  releasedQuantity: z.number().positive(),
  releasedWeight: z.number().positive(),
  observations: z.string().trim().max(500).nullable(),
  fobUsd: z.number().min(0).nullable(),
  manualExchangeRate: z.number().positive().nullable(),
});
export const releaseRegisterSchema = releaseBodyBase.extend({ warehouseStorageProductId: guidSchema });   // C-F05-29
export const releaseUpdateSchema = releaseBodyBase.extend({ warehouseStorageProductId: guidSchema.nullable() }); // C-F05-30
export const releaseWithdrawSchema = z.object({ reason: reasonSchema });                                    // C-F05-31

// C-F05-32 y C-F05-33
export const releaseDepositQuerySchema = listQueryBaseSchema.extend({
  search: z.string().optional(),
  nationalizationStatus: z.array(z.enum(["NotNationalized", "Partial", "Nationalized"])).optional(),
  withWeightDifference: z.boolean().optional(),
  entryDateFrom: dateOnlySchema.optional(),
  entryDateTo: dateOnlySchema.optional(),
});
export const releaseDepositRowSchema = z.object({
  importDepositId: guidSchema,
  warehouseStorageId: guidSchema,
  warehouseStorageNumber: z.string(),
  entryDate: dateTimeSchema.nullable(),
  documentTypeName: z.string().nullable(),
  documentNumber: z.string().nullable(),
  dianManifestNumber: z.string().nullable(),
  importerName: z.string().nullable(),
  merchandise: z.array(z.object({ productName: z.string(), packaging: z.string().nullable() })),
  enteredQuantity: z.number(),
  enteredWeight: z.number().nullable(),
  nationalizedQuantity: z.number(),
  nationalizedWeight: z.number(),
  nationalizedPercent: z.number(),
  balanceQuantity: z.number(),
  balanceWeight: z.number().nullable(),
  nationalizationStatus: z.enum(["NotNationalized", "Partial", "Nationalized"]),
  hasWeightDifference: z.boolean(),
  releaseCount: z.int(),
});
export const releaseDepositListResponseSchema = pagedSchema(releaseDepositRowSchema);
export const releaseSummarySchema = z.object({
  total: z.int(), notNationalized: z.int(), partial: z.int(), nationalized: z.int(), withWeightDifference: z.int(),
});
export const releaseSummaryResponseSchema = dataSchema(releaseSummarySchema);

export type ImportRelease = z.infer<typeof importReleaseSchema>;
export type ReleaseRegister = z.infer<typeof releaseRegisterSchema>;
export type ReleaseDepositRow = z.infer<typeof releaseDepositRowSchema>;
export type ReleaseSummary = z.infer<typeof releaseSummarySchema>;
```

`releaseWithdrawResultSchema` copia los campos de la respuesta de hoy del retiro (`F/features/foreign-trade/types/import-deposit.ts`).

**`F/features/foreign-trade/contracts/abandonment.ts`** y **`packing-list.ts`** (FE-1 los crea; FE-3 los usa; C-F05-26 a C-F05-28, C-F05-49, C-F05-50):

```ts
// abandonment.ts
export const abandonmentStatusSchema = z.enum(["EnPlazo", "EnAlerta", "EnAbandono"]); // AbandonmentStatus (B/Wms.Application/ForeignTrade/Common/Services/AbandonmentCalculator.cs:4)
export const abandonmentListQuerySchema = listQueryBaseSchema.extend({
  status: z.array(abandonmentStatusSchema).optional(),
  hasExtension: z.boolean().optional(),
  warehouseStorageNumber: z.string().optional(),
  cargoManifestNumber: z.string().optional(),
  importerName: z.string().optional(),
  customsAgencyName: z.string().optional(),
  customerName: z.string().optional(),
  entryDateFrom: dateOnlySchema.optional(),
  entryDateTo: dateOnlySchema.optional(),
});
export const abandonmentItemSchema = z.object({   // AbandonmentItemDto (B/…/DTOs/AbandonmentItemDto.cs:7-31)
  importWarehouseStorageId: guidSchema, warehouseStorageId: guidSchema, warehouseStorageNumber: z.string(),
  cargoManifestNumber: z.string().nullable(), entryDate: dateTimeSchema, daysElapsed: z.int(), deadlineDays: z.int(),
  daysRemaining: z.int(), status: z.string(), hasExtension: z.boolean(), extensionRegisteredAt: dateTimeSchema.nullable(),
  importerName: z.string().nullable(), customsAgencyName: z.string().nullable(), customerName: z.string().nullable(),
  pendingToNationalize: z.number(), currentStock: z.number(),
  importerId: guidSchema.nullable(), customsAgencyId: guidSchema.nullable(),
});
export const abandonmentSummarySchema = z.object({ inAlert: z.int(), abandoned: z.int() });

// packing-list.ts
export const packingListQuerySchema = listQueryBaseSchema.extend({
  importerId: guidSchema.optional(), supplierId: guidSchema.optional(),
  fileName: z.string().optional(), importerName: z.string().optional(), supplierName: z.string().optional(),
  createdAtFrom: dateOnlySchema.optional(), createdAtTo: dateOnlySchema.optional(),
});
export const packingListFileSchema = z.object({   // PackingListFileDto (B/…/PackingLists/Common/PackingListDtos.cs:9-20)
  id: guidSchema, fileName: z.string(), supplierName: z.string(), importerName: z.string(), itemCount: z.int(),
  activeItems: z.int(), associatedItems: z.int(), createdByName: z.string(), createdAt: dateTimeSchema,
});
export const packingListItemQuerySchema = listQueryBaseSchema.extend({
  importerId: guidSchema, status: z.string().optional(), search: z.string().optional(),
  code: z.string().optional(), description: z.string().optional(), warehouseStorageNumber: z.string().optional(),
});
export const packingListItemSchema = z.object({   // PackingListItemDto (PackingListDtos.cs:29-…)
  id: guidSchema, packingListFileId: guidSchema, fileName: z.string(), supplierName: z.string(), code: z.string(),
  description: z.string(), packages: z.number(), unitsPerPackage: z.number(), quantity: z.number(), netWeightKg: z.number(),
  productId: guidSchema, productName: z.string(), productSku: z.string(), status: z.string(),
  warehouseStorageEntryId: guidSchema.nullable(), warehouseStorageNumber: z.string().nullable(), vehiclePlate: z.string().nullable(),
});
// Los de C-F05-50 (proveedores, importación de la lista, detalle, borrado, asociación) se escriben con los campos de
// F/features/foreign-trade/types/packing-list.ts, sin cambiarlos.
```

**`F/features/foreign-trade/contracts/deposit-misc.ts`** (FE-1; grupo D):

```ts
import { z } from "zod";
import { dateTimeSchema, guidSchema, reasonSchema } from "~/shared/contracts/api";

export const labelPrintsSchema = z.object({
  warehouseStorageId: guidSchema, printCount: z.int(), downloadCount: z.int(),
  lastPrintedAt: dateTimeSchema.nullable(), lastPrintedByName: z.string().nullable(),
  items: z.array(z.object({ action: z.string(), printedByName: z.string(), createdAt: dateTimeSchema, vehiclePlate: z.string().nullable().optional() })),
});
export const extensionRequestSchema = z.object({ notes: z.string().trim().max(500).nullable().optional() });
export const cancelDepositSchema = z.object({ reason: reasonSchema });
export const cancelDepositResultSchema = z.object({
  warehouseStorageId: guidSchema, status: z.string(), removedOrderItems: z.int(), cancelledOrders: z.array(z.string()),
  closedPeriods: z.int(),
  cancelledInvoices: z.array(z.object({ invoiceId: guidSchema, invoiceNumber: z.string().nullable() })),
  invoicesToReview: z.array(z.object({ invoiceId: guidSchema, invoiceNumber: z.string().nullable(), status: z.string(), total: z.number() })),
});
export const clientFinancialStatusSchema = z.object({
  stakeholderId: guidSchema, stakeholderName: z.string(), financialStatus: z.enum(["Active", "OverdueWarning", "Blocked"]),
  overdueAmount: z.number(), canProceed: z.boolean(), blockReason: z.string().nullable().optional(),
});
export const shippingFormNumberSchema = z.object({ shippingFormNumber: z.string().trim().max(100).nullable() });
export const shippingFormNumberResultSchema = z.object({ warehouseStorageId: guidSchema, shippingFormNumber: z.string().nullable() });
export const cargoUnitBreakdownSchema = z.object({
  units: z.array(z.object({
    warehouseStorageCargoUnitId: guidSchema,
    products: z.array(z.object({ warehouseStorageProductId: guidSchema, declaredQuantity: z.number().min(0) })),
  })),
  reason: reasonSchema,
});
// extensionResultSchema: los campos de IStorageExtensionResultDto (F/features/foreign-trade/types/import-deposit.ts).
```

**`F/features/reports/contracts/nationalized-inventory.ts`** (FE-1; C-F05-34, C-F05-35):

```ts
import { z } from "zod";
import { dataSchema, dateOnlySchema, dateTimeSchema } from "~/shared/contracts/api";

export const nationalizedInventoryQuerySchema = z.object({ releaseDateFrom: dateOnlySchema, releaseDateTo: dateOnlySchema });
export const nationalizedReleaseSchema = z.object({
  releaseNumber: z.string(), acceptanceNumber: z.string(), releaseDate: dateOnlySchema,
  quantity: z.number(), weight: z.number(), customsValueUsd: z.number().nullable(),
});
export const nationalizedProductSchema = z.object({
  productName: z.string(), packaging: z.string().nullable(), entryDate: dateTimeSchema.nullable(),
  dianManifestNumber: z.string().nullable(), enteredQuantity: z.number(), currentStock: z.number(),
  nationalizedQuantity: z.number(), releases: z.array(nationalizedReleaseSchema),
});
export const nationalizedDepositSchema = z.object({
  warehouseStorageNumber: z.string(), documentTypeName: z.string().nullable(), documentNumber: z.string().nullable(),
  customsAgencyName: z.string().nullable(), importerName: z.string().nullable(), customerName: z.string().nullable(),
  products: z.array(nationalizedProductSchema),
});
export const nationalizedInventorySchema = z.object({
  releaseDateFrom: dateOnlySchema, releaseDateTo: dateOnlySchema,
  deposits: z.array(nationalizedDepositSchema),
  totals: z.object({ enteredQuantity: z.number(), currentStock: z.number(), nationalizedQuantity: z.number() }),
});
export const nationalizedInventoryResponseSchema = dataSchema(nationalizedInventorySchema);
export type NationalizedInventory = z.infer<typeof nationalizedInventorySchema>;
```

### 2.4 Pantallas y sus endpoints

| Pantalla | Ruta | Endpoints |
| --- | --- | --- |
| P-CE-01 Depósitos › Importación, Exportación, Inspección | `/foreign-trade/imports`, `/exports`, `/inspections` | C-F05-01; expandida: C-F05-22; acciones: C-F05-40 (tarjeta del vehículo), C-F03-35 (tiquete) |
| P-CE-02 Detalle: encabezado, etapas, información general y Entradas | `/foreign-trade/{imports\|exports\|inspections}/[id]` | C-F05-05 a C-F05-07, C-F05-08, C-F05-09, C-F05-22, C-F05-40 a C-F05-47, C-F05-50 (asociar artículos), C-F05-28 (artículos del importador), C-F01-145 (unidades), C-F03-35 |
| P-CE-03 Edición del ingreso | `/foreign-trade/entries/[entryId]` | C-F03-13, C-F05-23, C-F05-24; catálogos C-F01-02, C-F01-15, C-F01-17, C-F01-25, C-F01-141, C-F01-69, C-F01-71, C-F01-29, C-F01-30, C-F01-33, C-F03-44 |
| P-CE-04 Datos principales | etapa `datos` del detalle | C-F05-05 a C-F05-07 (lectura), C-F05-10; C-F01-25, C-F01-141, C-F03-44, C-F01-08 (prefijo del manifiesto DIAN) |
| P-CE-05 Bodega | etapa `bodega` | C-F05-22 (recepción y reloj), C-F05-05 a C-F05-07 (inventario), C-F05-48; enlaces a Movimientos por depósito y a Novedades (C-F04-30) |
| P-CE-06 Amparados | etapa `amparados` | C-F05-05, C-F05-06 (lectura), C-F05-11, C-F05-12 a C-F05-15; C-F01-69, C-F01-71, C-F01-29, C-F01-30 |
| P-CE-07 Levantes (vista 1) | etapa `levantes` (importación) | C-F05-05, C-F05-29, C-F05-30, C-F05-31, C-F01-13, C-F01-08 |
| P-CE-08 Salidas | etapa `salidas` | ninguno en F05 (D38); F06 |
| P-CE-09 Tickets de ingreso | `/foreign-trade/entry-tickets` | C-F05-25; «Editar» lleva a P-CE-03 |
| P-CE-10 Levantes (vista 2) | `/foreign-trade/releases` | C-F05-32, C-F05-33; expandida: C-F05-05, C-F05-29, C-F05-30, C-F05-31, C-F01-13, C-F01-08 |
| P-CE-12 Inventario nacionalizado | `/reports/nationalized-inventory` | C-F05-34, C-F05-35 |
| Abandono y prórrogas | `/foreign-trade/abandonment` | C-F05-26, C-F05-49, C-F05-43 |
| Listas de empaque | `/foreign-trade/packing-lists` | C-F05-27, C-F05-28, C-F05-50 |
| Movimientos por depósito y Póliza (solo rótulos, D31) | `/reports/warehouse-movements`, `/reports/policies` | C-F05-36 (PDF); las lecturas de hoy sin cambios |


---

## 3. Archivos que se tocan

### 3.1 Pantallas y componentes

| Pantalla | Página | Componentes (nuevos en negrita) | Compartidos |
| --- | --- | --- | --- |
| P-CE-01 | `F/pages/foreign-trade/{imports,exports,inspections}/index.vue` (se reemplazan en su ruta) | **`DepositListTable`**, **`DepositListExpansion`** | `AppDataTable` (D34), `AppRowActions` |
| P-CE-02 a P-CE-08 | `F/pages/foreign-trade/{imports,exports,inspections}/[id]/index.vue` (se reemplazan en su ruta) | **`DepositStageDetail`**, **`DepositDetailHeader`**, **`DepositStageStepper`**, **`DepositGeneralInfo`**, **`DepositEntriesStage`**, **`DepositMainDataStage`**, **`DepositWarehouseStage`**, **`DepositCoverageStage`**, **`DepositReleasesStage`**, **`ReleaseEditableRow`**, **`DepositExitsStage`**; `DepositProductDialog` (dos columnas), `DepositConfirmationRequirements`, `FinancialStatusAlert`, `LabelPrintsBadge`, `RegisterExtensionDialog`, `CargoUnitBreakdownDialog`, `AssociatePackingListItemsDialog`, `WithdrawReleaseDialog` (de hoy) | `AppSearchSelect` (con «+»), `AppRowActions`, `ReasonDialog`, `CorrectionResultDialog`, `WarehouseClockTag` (F04), `StakeholderQuickDialog` (F03), `AdjustInventoryDialog` (de hoy) |
| P-CE-03 | **`F/pages/foreign-trade/entries/[entryId].vue`** | **`EntryEditForm`** | `AppSearchSelect`, `StakeholderQuickDialog`, `DriverQuickDialog` (F03) |
| P-CE-09 | **`F/pages/foreign-trade/entry-tickets.vue`** | — | `AppDataTable` |
| P-CE-10 | `F/pages/foreign-trade/releases/index.vue` (se reemplaza en su ruta) | `DepositReleasesStage` (compacta), `ReleaseEditableRow` | `AppDataTable` (D34) |
| P-CE-12 | **`F/pages/reports/nationalized-inventory.vue`** | **`NationalizedInventoryReport`** (`F/features/reports/components/`) | convención «Páginas que no son listados» |
| Abandono y prórrogas | `F/pages/foreign-trade/abandonment/index.vue` (al patrón) | `AbandonmentSummaryAlert`, `RegisterExtensionDialog` (de hoy) | `AppDataTable` |
| Listas de empaque | `F/pages/foreign-trade/packing-lists/index.vue` (al patrón) | `PackingListUploadDialog`, `PackingListItemsDialog` (de hoy) | `AppDataTable` |
| Rótulos (D31) | `F/pages/reports/warehouse-movements.vue`, `F/pages/reports/policies.vue` | — | — |

### 3.2 Backend

| Archivo | Cambio | Fase |
| --- | --- | --- |
| `B/Wms.Domain/Entities/Warehouse/WarehouseStorageProduct.cs` | `CoveredQuantity` y `SetCoveredQuantity` (D13) | BE-1 |
| `B/Wms.Domain/Entities/Warehouse/WarehouseStorage.cs` | `CpiNetWeight`, `CpiGrossWeight`, `UpdateMainData` (Borrador y Confirmado) en lugar de `UpdateDraftInfo` (`:477-506`); `EnsureProductsAreEditable` (`:565-571`) con la regla de D18; borra `MarkForCorrection` (`:350-376`) | BE-1 |
| `B/Wms.Infrastructure/Persistence/Configurations/Warehouse/WarehouseStorage*Configuration.cs` | Columnas nuevas (§4) | BE-1 |
| `B/Wms.Application/ForeignTrade/Common/Services/DepositConfirmationRequirements.cs` | D15 (`:75-79`, nuevo `COVERED_QUANTITY` e `INSPECTION_DESCRIPTION`); el snapshot suma productos con ingresado y amparado | BE-1 |
| `B/Wms.Application/ForeignTrade/Common/Services/DepositStageRules.cs`, `DepositCoverage.cs`, `NationalizationRules.cs` (nuevos, puros) | D13, D14, D22, D23 | BE-1 |
| `B/Wms.Application/ForeignTrade/Queries/GetDeposits/` | C-F05-01 (reescrito) | BE-1 |
| `B/Wms.Application/ForeignTrade/Queries/GetImportDeposits/`, `GetExportDeposits/`, `GetInspectionDeposits/` | Se borran (C-F05-02 a C-F05-04), si nadie más los usa | BE-1 |
| `B/Wms.Application/ForeignTrade/Common/DTOs/ImportDepositDetailDto.cs`, `ExportDepositDetailDto.cs`, `InspectionDepositDetailDto.cs`, `DepositStorageProductDto.cs`, `DepositDetailProductsBuilder.cs` | C-F05-05 a C-F05-07 | BE-1 |
| `B/Wms.Application/ForeignTrade/Commands/ConfirmStorageDeposit/ConfirmStorageDepositHandler.cs` | D15 (`:60`, `:77-80`) | BE-1 |
| `B/Wms.Application/ForeignTrade/Commands/UpdateDepositMainData/` (nuevo) | C-F05-10, con D17 y D19; reusa `DepositCustomerBillingChange`, `DraftCorrectionBillingRules`, `CorrectEntryDate` y las reglas de terceros de `UpdateDepositStakeholdersHandler` | BE-1 |
| `B/Wms.Application/ForeignTrade/Commands/UpdateCoveredQuantities/` (nuevo) | C-F05-11 | BE-1 |
| `B/Wms.Application/ForeignTrade/Common/Services/DepositProductEditing.cs` y los comandos `AddDepositProduct`, `UpdateDepositProduct`, `RemoveDepositProduct`, `ChangeDepositLineProduct` | D18 (piso con `EntryCorrectionRules`) | BE-1 |
| `B/Wms.Application/ForeignTrade/Commands/UpdateDraftDeposit/`, `AssignDepositCustomer/`, `UpdateDepositStakeholders/`, `UpdateManifestInfo/`, `ReturnStorageForCorrection/` | Se borran (C-F05-16 a C-F05-20) | BE-1 |
| `B/Wms.Application/Exits/Commands/ConfirmExitCommand.cs`, `B/Wms.Application/Exits/Common/ExitCustomerRules.cs` (nuevo) | D21 | BE-1 |
| `B/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs` | D24 (`:271-275`) | BE-1 |
| `B/Wms.Api/Controllers/v1/ForeignTradeController.cs` | C-F05-01, C-F05-10, C-F05-11; borra las acciones retiradas | BE-1 |
| `B/Wms.Application/ForeignTrade/Common/DTOs/DepositStorageEntryDto.cs` y su consulta | C-F05-22 | BE-2 |
| `B/Wms.Application/Weighbridge/Commands/Storage/CorrectEntry/`, `B/Wms.Application/Weighbridge/Common/Services/EntryCorrectionService.cs` | C-F05-23 (reusa las reglas de `CorrectEntryLogCommandHandler`) | BE-2 |
| `B/Wms.Api/Controllers/v1/EntryCorrectionController.cs`, `WeighbridgeController.cs` | C-F05-24 (mueve la acción) | BE-2 |
| `B/Wms.Application/ForeignTrade/Queries/GetEntryTickets/` (nuevo) | C-F05-25 | BE-2 |
| `B/Wms.Application/ForeignTrade/Queries/GetAbandonmentList/`, `PackingLists/Queries/GetPackingLists/`, `GetPackingListItems/` | C-F05-26 a C-F05-28 | BE-2 |
| `B/Wms.Application/ForeignTrade/Commands/RegisterImportRelease/`, `UpdateImportRelease/`, `WithdrawImportRelease/`, `Common/Services/ReleaseFobService.cs`, `ReleaseValueRules.cs` | C-F05-29 a C-F05-31 (D9, D30, D31) | BE-3 |
| `B/Wms.Application/ForeignTrade/Queries/GetReleases/` | C-F05-32, C-F05-33 | BE-3 |
| `B/Wms.Application/Reports/NationalizedInventory/` (nuevo), `B/Wms.Api/Controllers/v1/NationalizedInventoryReportController.cs` (nuevo) | C-F05-34, C-F05-35 | BE-3 |
| `B/Wms.Application/Warehouse/Common/Services/WarehouseMovementsPdfService.cs` | C-F05-36 (`:282`) | BE-3 |

### 3.3 Frontend

| Archivo | Cambio | Fase |
| --- | --- | --- |
| `F/components/app/AppDataTable.vue`, `FT/unit/components/AppDataTable.spec.ts`, `F/pages/dev/components.vue` | D34 | FE-1 |
| `F/features/foreign-trade/contracts/*.ts`, `F/features/reports/contracts/nationalized-inventory.ts` | §2.3 | FE-1 |
| `F/features/foreign-trade/services/{deposit,deposit-edit,entry-ticket,release,abandonment,packing-list,catalog}.source.ts`, `F/features/reports/services/nationalized-inventory.source.ts`, `F/features/*/mocks/` | D36 | FE-1 (las que usa), FE-2 y FE-3 (las suyas) |
| `FT/unit/foreign-trade/mocks.spec.ts`, `FT/unit/reports/mocks.spec.ts` | Datos simulados contra sus esquemas | FE-1 a FE-3 |
| `FT/unit/guards/mock-sources.spec.ts` | `MAQUETACION_PAGES` con las páginas de F05 | FE-1 a FE-3 |
| Las páginas y componentes de §3.1 | Pantallas | FE-1 a FE-3 |
| `F/features/foreign-trade/utils/release-quantity.ts` y `deposit-stages.ts` (nuevos, puros) | Cálculo de la cantidad del levante (D30) y textos y colores de las etapas (D22) | FE-2, FE-3 |

### 3.4 Docs

El plan (estado de cada fase en §8), la matriz (`D/planes/sprint-11/seguimiento-implementacion-fase-2-2026-11-21.md`), los prompts y, en I-05, `D/qa/casos-qa2-f05-comercio-exterior-AAAA-MM-DD.md` y el estado del hub (§13.4).

---

## 4. Esquema y migraciones

| Fase | Migración | Contenido esperado |
| --- | --- | --- |
| BE-1 | `DepositCoverageAndCpiWeights` | `warehouse_storage_products.covered_quantity` (numérica, nula, con la precisión de `declared_quantity`); `warehouse_storages.cpi_net_weight` y `cpi_gross_weight` (numéricas, nulas, con la precisión de los pesos de hoy). Sin índices, sin semillas, sin datos |
| BE-2 | ninguna | — |
| BE-3 | ninguna | D9 conserva `import_releases.acceptance_date` sin nulos |

La genera y aplica el agente con `dotnet ef` en local (`DEC-004`, M6); `has-pending-model-changes` limpio al cerrar cada fase.

---

## 5. Pruebas

| Proyecto | Prueba (nueva o ajustada) | Escenario |
| --- | --- | --- |
| `Wms.Tests` | `DepositStageRulesTests` (nueva) | Cada etapa por tipo (D16); Entradas con y sin CPI manual (D11); Bodega con el peor nivel; Amparados con camión tardío; Cerrado y Anulado sin etapas |
| `Wms.Tests` | `DepositCoverageTests`, `NationalizationRulesTests` (nuevas) | Ingresado con entradas anuladas y sin entradas (migrado); peso amparado con y sin CPI; los estados de nacionalización y la regla de diferencia de peso de MK-04 |
| `Wms.Tests` | `DepositConfirmationRequirementsTests` (ajustada) | Sin cliente; amparado distinto; inspección sin fecha del documento y con descripción |
| `Wms.Tests` | `ExitCustomerRulesTests` (nueva) | Depósito sin cliente en cada tipo de salida |
| `Wms.Tests` | `ReleaseFobServiceTests` (ajustada) | Tasa cambiada al editar y su origen |
| `Wms.IntegrationTests` | `DepositListEndpointTests`, `DepositDetailStagesTests`, `DepositMainDataTests`, `CoveredQuantitiesTests`, `DepositProductsConfirmedTests`, `LateCustomerBillingTests` (nuevas) | C-F05-01, C-F05-05 a C-F05-15, con D17 y D19 (factura en Borrador y aprobada) |
| `Wms.IntegrationTests` | `RetiredDepositEndpointsTests` (nueva) | C-F05-02 a C-F05-04 y C-F05-16 a C-F05-20 en 404 |
| `Wms.IntegrationTests` | `ConfirmExitTests` (ajustada) | C-F05-21 |
| `Wms.IntegrationTests` | `DepositsImporterTests` (ajustada) | D24 |
| `Wms.IntegrationTests` | `DepositEntriesReadTests`, `EntryCorrectionCeTests` (ajustadas), `EntryTicketsEndpointTests` (nueva), `AbandonmentListTests`, `PackingListsListTests` (ajustadas) | C-F05-22 a C-F05-28 |
| `Wms.IntegrationTests` | `ImportReleaseTests` (ajustada), `ReleaseDepositsEndpointTests`, `NationalizedInventoryReportTests` (nuevas) | C-F05-29 a C-F05-36 |
| Vitest | `AppDataTable.spec.ts` (ajustada) | Fila expandible (D34) |
| Vitest | `FT/unit/foreign-trade/mocks.spec.ts`, `FT/unit/reports/mocks.spec.ts` | Cada dato simulado pasa su esquema (`P02/` D16) |
| Vitest | `release-quantity.spec.ts`, `deposit-stages.spec.ts` (nuevas) | D30 (un producto, varios, levante total) y D22 |
| Vitest | Componentes: `DepositListTable`, `DepositStageStepper`, `DepositCoverageStage`, `ReleaseEditableRow`, `EntryEditForm` | Lo que pinta cada uno con datos simulados |
| Vitest | Guardias (`list-pattern`, `mock-sources`, `source-guards`) | En verde en cada fase |

---

## 6. Casos QA

### 6.1 Parte 1 (API)

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F05-001 | AF-72; D3 | Depósitos de los tres tipos en varios estados | C-F05-01 con `modality=Import&status=Draft`; sin `modality`; con `sortField=foo` | Solo importaciones en Borrador, `entryDate desc`, con los campos de la ficha; 400 «Indique el tipo de depósito.»; 400 «No se puede ordenar por «foo».» | API (BE-1) |
| QA2-F05-002 | AF-99; D3 | Lo de 001 | C-F05-01 con `warehouseStorageNumber`, `document`, `ticketNumber`, `product` y `entryDateFrom/To`; `sortField=warehouseStorageNumber` | Filtra (contiene, sin tildes ni mayúsculas) y ordena | API (BE-1) |
| QA2-F05-003 | AF-73, AF-87; D16, D22 | Importación en Borrador sin manifiesto DIAN, con una entrada sin recepción (umbrales 30/60, primer peso hace 40 min) y amparado distinto; exportación e inspección | C-F05-01 y C-F05-05 a C-F05-07 | Importación: `pendingStages` con `MainData`, `Warehouse` y `Coverage`, `warehouseLevel: Yellow`, `stages` con seis; exportación con cinco; inspección con cuatro y sin `Coverage` | API (BE-1) |
| QA2-F05-004 | AF-75; D15 | Importación completa sin cliente, amparado = ingresado | C-F05-08; C-F05-09 | `canConfirm: true` sin `CUSTOMER`; 200 Confirmado; sin período ni factura de almacenamiento | API (BE-1) |
| QA2-F05-005 | AF-77, AF-87; D15 | Importación con amparado distinto; inspección sin fecha del documento ni descripción | C-F05-09 en cada una | 400 con «cantidad amparada de {producto}: …»; inspección: 400 con «descripción de la inspección» y sin «fecha del documento» | API (BE-1) |
| QA2-F05-006 | AF-75; D17 | El depósito de 004 (confirmado sin cliente), ingreso hace 20 días | C-F05-10 con `customerId` | 200 con `billingPeriodOpened: true`; primer período desde el día de ingreso con su factura en Borrador; aviso de advertencias a Facturación si las hay | API (BE-1) |
| QA2-F05-007 | AF-76; D19; `DEC-022` | Importación confirmada con cliente y factura del período en Borrador; otra con la factura aprobada con N.º SIIGO | C-F05-10 cambia el valor CPI en cada una | Borrador: total recalculado. Aprobada: la misma factura, con el N.º SIIGO, total nuevo y aviso a Facturación con el total anterior y el nuevo | API (BE-1) |
| QA2-F05-008 | AF-76; D18 | Depósitos cerrado y anulado | C-F05-10 y C-F05-11 | 409 «El depósito {N} está Cerrado: ya no se edita.» (y Anulado) | API (BE-1) |
| QA2-F05-009 | AF-78; D18, D19 | Importación confirmada con un levante de 100 sobre 300 | C-F05-13 a 80; C-F05-14 del producto; C-F05-12 de otro producto | 409 «…: la cantidad no puede quedar en 80; ya tiene 100 levantado y 0 despachado.»; 409 «… ya tiene levantes o salidas: no se puede quitar.»; 200 y factura recalculada | API (BE-1) |
| QA2-F05-010 | AF-77; D13 | Importación con dos productos | C-F05-11 con amparado igual al ingresado; con −1 | 200, `quantityBalance: 0`, sin `Coverage`; stock sin cambios; 400 «La cantidad amparada no puede ser negativa.» | API (BE-1) |
| QA2-F05-011 | AF-84; D22 | Importación confirmada con amparado = ingresado | Báscula registra un camión tardío con el mismo documento | C-F05-05 con `Coverage` pendiente y saldo distinto de cero; aviso «Camión tardío en depósito confirmado» | API (BE-1) |
| QA2-F05-012 | AF-93; D5, D20 | — | C-F05-02 a C-F05-04, C-F05-16 a C-F05-20 | 404 en cada uno | API (BE-1) |
| QA2-F05-013 | AF-75; D7, D21 | Inspección confirmada sin cliente con stock; salida `Deposit` en Borrador sobre ella | C-F05-21 | 409 «Asigne el cliente del depósito {N} antes de confirmar la salida.»; con cliente, 200 | API (BE-1) |
| QA2-F05-014 | D14; AF-100 | Importación con dos entradas con manifiesto | C-F05-05; C-F05-10 con `cpiGrossWeight`; C-F05-10 con fecha del documento futura | `manifestWeightSum` = suma y `coverage.coveredWeight` = esa suma; después = el CPI; 400 «La fecha del documento no puede ser futura.» | API (BE-1) |
| QA2-F05-015 | AF-92; D18 | Confirmado | C-F05-10 con un importador sin el rol `IMPORTER`; con `entryDate` fuera de la estadía del primer camión | 400 «El tercero {nombre} no tiene el rol Importador.»; 400 de `DEC-051` | API (BE-1) |
| QA2-F05-016 | M19; D24 | CSV de ensayo de la suite | Importación de depósitos | Cada producto migrado con `coveredQuantity` = lo ingresado; C-F05-05 de un migrado sin `Coverage` | API (BE-1) |
| QA2-F05-017 | AF-96; D25 | Depósito con dos entradas, una anulada | C-F05-22 | Las dos, con `dateTimeEntry`, `driverName`, `quantity`; la anulada con `canEdit: false` y `reception: null` | API (BE-2) |
| QA2-F05-018 | AF-26; D6 | Importación confirmada; camión con ciclo de ingreso | C-F05-23 con placa, motivo de la misma categoría y fecha dentro de la estadía; con un motivo de otra categoría | 200 y auditoría en el ingreso; 409 de la categoría | API (BE-2) |
| QA2-F05-019 | AF-94; D26 | Importación confirmada con factura en Borrador, moneda COP | C-F05-23 con `currency: USD` y precio | La moneda del depósito pasa a USD, el CPI automático se recalcula y la factura también | API (BE-2) |
| QA2-F05-020 | AF-26; D27 | Usuarios de CE, Báscula y Bodega | C-F05-24 con cada uno | 200, 200 y 403 | API (BE-2) |
| QA2-F05-021 | AF-74; D2, D28 | Entradas de los tres tipos, una anulada, un depósito anulado | C-F05-25 con `product`, `warehouseStorageNumber`, `vehiclePlate`; con un usuario de Báscula | Filtra; sin la anulada ni las del depósito anulado; `dateTimeEntry desc`; Báscula 403 | API (BE-2) |
| QA2-F05-022 | AF-99; D28 | Lo de 021 | C-F05-25 con `sortField=warehouseStorageNumber&sortOrder=asc`; con `modality=Import,Export` | Ordena; filtra por modalidad | API (BE-2) |
| QA2-F05-023 | AF-99, AF-129; D29 | Varios depósitos en abandono | C-F05-26 con `importerName`, `status=EnAlerta`, `sortField=entryDate` | Filtra y ordena; sin parámetros, `daysRemaining asc` como hoy | API (BE-2) |
| QA2-F05-024 | D29 | Varias listas de empaque | C-F05-27 con `supplierName` y orden por `fileName` | Filtra y ordena | API (BE-2) |
| QA2-F05-025 | D29 | Artículos de un importador | C-F05-28 con `code`, `description` y orden por `quantity desc`; sin `importerId` | Filtra y ordena; 400 de hoy | API (BE-2) |
| QA2-F05-026 | `DEC-005` | Usuario de Báscula | C-F05-22 y C-F05-23 | 403 (siguen en `ForeignTradeAccess`); C-F03-13 y C-F03-14 siguen para Báscula | API (BE-2) |
| QA2-F05-027 | AF-82; D9 | Importación confirmada | C-F05-29 sin `acceptanceDate`; con `acceptanceDate` distinta | 200; `acceptanceDate` = `releaseDate` en los dos | API (BE-3) |
| QA2-F05-028 | AF-86; D30 | Levante con tasa 4.020 (semanal) | C-F05-30 con tasa 4.050 | Tasa 4.050, `exchangeRateSource: Manual`, `fobCop` recalculado | API (BE-3) |
| QA2-F05-029 | AF-81; D31 | Levante con valor en aduanas en otro producto | C-F05-29 con valor en el segundo producto; con −1; retiro del primero | Mensajes con «valor en aduanas»; la nota del heredero con «El valor en aduanas pasó al producto» | API (BE-3) |
| QA2-F05-030 | AF-80; D10, D32 | Importaciones sin levante, parcial, nacionalizada y una con diferencia de peso | C-F05-32 con `nationalizationStatus=Partial`; con `withWeightDifference=true`; con `search` por número de levante | Una fila por depósito con los campos de la ficha; filtra | API (BE-3) |
| QA2-F05-031 | D32 | Lo de 030 | C-F05-33 | Los contadores de cada estado y el de diferencia de peso | API (BE-3) |
| QA2-F05-032 | AF-91; D33 | Levantes en noviembre y en octubre | C-F05-34 con noviembre; sin fechas; con 400 días | Solo las mercancías con levante en noviembre, con sus levantes de noviembre y el total nacionalizado; 400 y 400 | API (BE-3) |
| QA2-F05-033 | AF-91; D33 | Lo de 032 | C-F05-35 | 200 `application/pdf` con las firmas | API (BE-3) |
| QA2-F05-034 | AF-81; D31 | Depósito con levante | C-F05-36 | El PDF trae la columna «Valor en aduanas (USD)» | API (BE-3) |
| QA2-F05-035 | AF-83 | Producto con 300 pendientes | C-F05-29 con 301 | El error de hoy de `NationalizationBalance` | API (BE-3) |
| QA2-F05-036 | `PM/` §7.2, M19 | Base local recreada; los 12 CSV de ensayo | Importación completa (§7) | Conteos iguales a los de la fase 6 de F01; todos los productos migrados con amparado = ingresado | API (BE-3) |

### 6.2 Integración I-05 (navegador)

Contra el backend local real de `f2/f05-comercio-exterior` y sin la sesión simulada, con usuarios de prueba por rol (sus contraseñas no se copian).

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F05-041 | AF-127; D43 | Usuarios CE, Bodega y Admin | Abrir el menú | CE y Admin ven Depósitos ▸ Importación, Exportación, Inspección, Tickets de ingreso, Levantes, Abandono, Listas de empaque y Reportes › Inventario nacionalizado; Bodega no ve CE; sin «Depósitos» suelto ni tablero | Pantalla (I-05 (1)) |
| QA2-F05-042 | AF-72, AF-99; D3, D4 | Importaciones en varios estados | Abrir Importación; cambiar estado y fechas; filtrar por columna; ordenar; expandir; «Exportar» | Borrador por defecto; filtros y orden; expandida por producto con sus camiones y entra, ampara y saldo (rojo si no cuadra); «Ver depósito» solo en la fila principal; la fila no abre nada al clic; Excel | Pantalla (I-05 (1)) |
| QA2-F05-043 | AF-87; D1 | Exportación e inspección | Abrir sus listas | Misma tabla, sin columnas de levantes; inspección muestra la descripción cuando no hay documento | Pantalla (I-05 (1)) |
| QA2-F05-044 | AF-73, AF-87, AF-93, AF-95, AF-98; D39 | Importación en Borrador con etapas pendientes | Abrir el detalle; recorrer el stepper; abrir «Acciones» | Seis etapas con el indicador por color; información general sin subpartida; acciones sin «Devolver a Borrador» ni «Cerrar ingreso»; `?etapa=` conserva la etapa al recargar | Pantalla (I-05 (1)) |
| QA2-F05-045 | AF-26, AF-27, AF-102, AF-94; D6 | Importación confirmada | Entradas › «Editar»; cambiar placa, peso del indicador, precio y moneda; switch «Unidad de carga» y agregar una unidad; «Guardar» | Vuelve a Entradas con los datos nuevos; el CPI (no manual) refleja el precio; con un levante registrado, el switch queda bloqueado con su mensaje | Pantalla (I-05 (1)) |
| QA2-F05-046 | AF-76, AF-92, AF-100; D5 | Importación confirmada con factura | Datos principales: cambiar valor CPI, agencia con «+» de alta rápida y fecha del documento; «Guardar» | Bloques separados; se guarda; la factura del período cambia (Facturación) | Pantalla (I-05 (1)) |
| QA2-F05-047 | AF-75; D17 | Importación confirmada sin cliente | Datos principales: asignar cliente; «Guardar» | Facturación ve la factura del primer período desde la fecha de ingreso | Pantalla (I-05 (1)) |
| QA2-F05-048 | AF-57; D37, D41 | Entrada sin recibir con primer peso hace 40 min (umbrales 30/60) | Etapa Bodega | Recepción pendiente con `WarehouseClockTag` amarillo; paso Bodega en amarillo; «Ajustar cantidad (CE-7)», «Movimientos» y «Ver novedades» funcionan | Pantalla (I-05 (1)) |
| QA2-F05-049 | AF-77, AF-78; D13 | Importación en Borrador | Amparados: digitar distinto; intentar confirmar; corregir; agregar producto con «+»; confirmar | Saldo en rojo y el requisito al confirmar; al cuadrar, confirma; el producto nuevo aparece con su embalaje | Pantalla (I-05 (1)) |
| QA2-F05-050 | AF-84 | Importación confirmada que cuadra | Báscula registra un camión tardío | En el listado y el detalle, Amparados en rojo; aviso a CE | Pantalla (I-05 (1)) |
| QA2-F05-051 | AF-80, AF-82, AF-83, AF-86, AF-79; D30 | Importación confirmada con un producto; tasa de la semana registrada; prefijos | Levantes › «Nuevo levante»: N.º con prefijo, fecha, peso (calcula la cantidad), valor en aduanas (calcula pesos); «Guardar»; editar la tasa; retirar | Fila guardada y otra fila ofrecida con el saldo; tasa precargada y editable; sin fecha de aceptación; tarjetas de ingreso, nacionalizado, saldo y levantes | Pantalla (I-05 (2)) |
| QA2-F05-052 | AF-83; D30 | Importación con dos productos | Nuevo levante del segundo; «Levante total del saldo» | Precarga lo pendiente; la cantidad queda editable y no pasa de lo pendiente | Pantalla (I-05 (2)) |
| QA2-F05-053 | `PM/` §2.2; D38 | Cualquier depósito | Etapa Salidas | Vacía, con el aviso; no se marca | Pantalla (I-05 (2)) |
| QA2-F05-054 | AF-74; D2 | Entradas de varios depósitos | Tickets de ingreso: filtrar; enlace al depósito; «Editar» y «Guardar» | Filtra; el enlace abre el detalle; «Editar» abre P-CE-03 y vuelve a Tickets | Pantalla (I-05 (2)) |
| QA2-F05-055 | AF-80, AF-81; D10, D32 | Lo de 030 | Levantes (vista 2): contadores, filtro por estado, «Con diferencia de peso», expandir y «Agregar levante» | Filas por depósito; la expandida es la tabla agrupada compacta y registra | Pantalla (I-05 (2)) |
| QA2-F05-056 | AF-91; D33 | Levantes en el mes | Reportes › Inventario nacionalizado: rango, «Consultar», «Descargar PDF», «Exportar Excel» | Agrupado por depósito con el detalle de cada levante; PDF con firmas; Excel | Pantalla (I-05 (2)) |
| QA2-F05-057 | AF-99, AF-129; D29 | Depósitos en abandono | Abandono: filtros por columna, orden, «Registrar prórroga» | Patrón de listado; la prórroga queda | Pantalla (I-05 (2)) |
| QA2-F05-058 | D29, D40 | Lista de empaque de un importador | Listas de empaque: pestañas, filtros, «Cargar»; en Entradas, «Agregar de la lista de empaque» | Patrón; los artículos quedan asociados al camión | Pantalla (I-05 (2)) |
| QA2-F05-059 | AF-81; D31 | Levantes con valor | Reportes › Movimientos por depósito (pantalla y PDF) y Póliza | «Valor en aduanas» en lugar de «CIF» | Pantalla (I-05 (2)) |
| QA2-F05-060 | `DEC-005` | Usuarios de Báscula y Facturación | Báscula edita una entrada en Borrador y elige otro depósito; Facturación abre Movimientos por depósito | Siguen funcionando (C-F05-24; C-F05-36) | Pantalla (I-05 (2)) |

---

## 7. Transición de datos

Lo que le toca a F05 de `PM/` §7.2. Las bases locales se recrean; staging se recrea en el despliegue final (M17, M25); nada se convierte.

| Dato | Qué se hace | Fase | Decisión |
| --- | --- | --- | --- |
| Cantidad amparada de lo confirmado o cerrado | El importador fija amparado = ingresado en cada producto migrado (todos los migrados están vivos y confirmados) | BE-1 | M19; D24 |
| Pesos CPI | Quedan nulos: el CSV no los trae; la pantalla precarga la suma de manifiestos, que en los migrados es nula | BE-1 | D14 |
| Fecha de aceptación | Sin cambio: los migrados conservan la del CSV | — | D9 |

**Importación completa de ensayo** (QA2-F05-036, como la fase 6 de F01): antes de cerrar BE-3, el ejecutor corre la importación completa en una base local recreada por Testcontainers con los 12 CSV de `db_legacy/trabajo/csv` (no versionados), en la base `c2ca314` y en la rama, y compara los conteos con los de la fase 6 de F01 (`P01/` §8: productos 1.643, depósitos migrados 128 con 133 líneas, saldo 136.499, ingresado 203.255, levantes 107 con 107.026,37 levantados, terceros 1.390, vehículos 10.393, conductores 4.361, ciudades 1.774). Después de F05 los conteos son iguales y las 133 líneas tienen amparado = ingresado. Si un conteo cambia, se detiene y pregunta. Los CSV no se copian a git (`DEC-007`).

---

## 8. Fases por parte

Una a la vez por repo; el backend y la maquetación corren en paralelo (M10). Cada fase cierra con las compuertas de `PM/` §6, commit y push.

| Fase | Parte | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| BE-1 | 1 | Depósitos: modelo, listado, detalle, confirmación, edición, apertura tardía, recálculo, retiros, salida con cliente, importador | QA2-F05-001 a 016 en PASA | Hecha el 2026-11-25 (`bb0d735`) |
| BE-2 | 1 | Entradas, edición del ingreso por CE, candidatos, Tickets, Abandono y Listas de empaque | QA2-F05-017 a 026 en PASA | Hecha el 2026-11-25 (`aac6de8`) |
| BE-3 | 1 | Levantes, rótulo, vista 2, inventario nacionalizado, importación de ensayo | QA2-F05-027 a 036 en PASA | Hecha el 2026-11-25 (`d94f831`) |
| FE-1 | 2 | Contratos, fuentes simuladas, `AppDataTable` expandible, P-CE-01 (tres rutas) y P-CE-09 | P-CE-01 y P-CE-09 con su lista del wireframe y captura | Hecha el 2026-11-25 (FE `8881589`) |
| FE-2 | 2 | Detalle por etapas: P-CE-02 a P-CE-06, P-CE-03 y Salidas vacía | P-CE-02 a P-CE-06 con su lista y captura | Hecha el 2026-11-25 (FE `45defb9`) |
| FE-3 | 2 | P-CE-07, P-CE-10, P-CE-12, Abandono, Listas de empaque y rótulos | Su lista y captura | Hecha el 2026-11-25 (FE `fe18386`) |
| Revisión | — | El usuario revisa la maquetación (§8.7) | Su visto bueno o un plan de ajustes ejecutado | Pendiente: parte 2 cerrada, a la espera de la revisión del usuario |
| I-05 (1) | 3 | Fuentes http, menú, borrado y casos de depósitos (§13) | QA2-F05-041 a 050 en PASA | Pendiente |
| I-05 (2) | 3 | Levantes, tickets, reportes y listados; casos a `D/qa/`; fusión | QA2-F05-051 a 060 en PASA; fusión en `fase-2` | Pendiente |

### 8.1 Backend, fase 1 — Depósitos

- **Decisiones:** D3, D5, D7, D13 a D24.
- **Endpoints:** C-F05-01 a C-F05-21 (fichas del grupo A; esquemas de `deposit.ts` y `deposit-edit.ts` para comparar nombres).
- **Archivos:** §3.2, filas de BE-1. Migración `DepositCoverageAndCpiWeights` (§4).
- **Orden sugerido:** modelo y migración → reglas puras (`DepositCoverage`, `DepositStageRules`, `NationalizationRules`, `ExitCustomerRules`) con sus pruebas → requisitos y confirmación → detalle → listado → C-F05-10 y C-F05-11 (con D17 y D19) → productos → retiros → salida con cliente → importador.
- **Casos:** QA2-F05-001 a 016.
- **Notas para FE e I-05:** si un nombre de campo del DTO difiere de la ficha, gana la ficha; si no se puede, se anota aquí con el porqué y se avisa (el frontend usa la ficha).
- **Notas para FE e I-05** (BE-1, 2026-11-25; los nombres de los DTO coinciden con las fichas y los esquemas de §2.3):
  - **C-F05-01:** `status` acepta también varios valores separados por coma (C-F01-00). `modality` inválida responde 400 «El valor «{valor}» no es válido para modality.». El orden por `ticketNumber` y `product` usa el menor tiquete vigente y el menor nombre de producto del depósito.
  - **C-F05-05 a C-F05-07:** `stages`, `pendingStages` y `warehouseLevel` como texto; `warehouseLevel` en `None|Yellow|Red`. La etapa Bodega y `warehouseLevel` cuentan las entradas vigentes con la recepción pendiente **y con primer peso**, como la lista de pendientes de Bodega (`PendingReceptionFilters`); un camión sin primer peso no marca Bodega.
  - **C-F05-10:** (1) la fecha de ingreso se compara al minuto: si la petición trae la misma fecha leída sin segundos, no cuenta como cambio ni pide motivo. (2) Se conserva la regla de hoy BAS-01 (F1-04): un documento con su fecha no repite el de otro depósito abierto → 409 «Ya existe un depósito abierto con el documento {N} y fecha {dd/MM/yyyy}: {depósito}.». (3) Errores que la ficha no lista: 404 «El tercero no existe.», 404 «El tipo de documento principal no existe.», 400 «El número del documento admite hasta 50 caracteres.», 400 «El número del manifiesto DIAN admite hasta 50 caracteres.», 400 «Las observaciones admiten hasta 1.000 caracteres.» y 400 «El depósito no tiene camiones registrados.» (fecha de ingreso de un depósito sin entradas). (4) `customerId` nulo en un depósito sin período abierto deja el depósito sin cliente. (5) `warnings` solo trae algo cuando se abrió el período (D17). (6) Antes, el manifiesto DIAN se editaba también en Cerrado (`PATCH imports/{id}/manifest`); con D18, Cerrado responde 409.
  - **C-F05-11:** sin `items` responde 400 «Indique al menos un producto.».
  - **C-F05-12 a C-F05-15:** las respuestas son las de hoy (C-F05-12 responde 201 con el Id del producto). El 409 de levantes o salidas va antes de los bloqueos de hoy (`DepositProductDependencies`); C-F05-15 usa el mismo texto «… ya tiene levantes o salidas: no se puede quitar.».
  - **Retiros:** C-F05-02 a C-F05-04, C-F05-16, C-F05-17, C-F05-19 y C-F05-20 responden 404; `PUT …/stakeholders` (C-F05-18) responde **405**, porque su ruta sigue viva para `GET …/stakeholders`, que se conserva (como C-F04-11 en F04).
  - **Ayudas de prueba:** las pruebas que confirman depósitos digitan antes lo amparado igual a lo ingresado (`BillingScenario.EnsureCoveredQuantitiesAsync`), como la pantalla de Amparados.
- **Estado:** hecha el 2026-11-25 (BE `bb0d735`, rama `f2/f05-comercio-exterior` desde `fase-2` `c2ca314`). QA2-F05-001 a 016 en PASA por API (pruebas `DepositListEndpointTests`, `DepositDetailStagesTests`, `DepositMainDataTests`, `LateCustomerBillingTests`, `DraftCorrectionRecalculationTests` (QA2-F05-007, reescrita sobre C-F05-10 en Confirmado), `DepositProductsConfirmedTests`, `RetiredDepositEndpointsTests`, `ExitCustomerRequiredTests` y `LegacyDepositsCoverageTests`). `dotnet build Wms.sln` sin errores; `Wms.Tests` 2272 → 2315 y `Wms.IntegrationTests` 825 → 846, todas en verde. Migración `DepositCoverageAndCpiWeights` (las tres columnas de §4, sin índices ni datos) generada y aplicada en local; `has-pending-model-changes` limpio. Se borraron las pruebas del tablero (`DepositKanbanSearchTests`) y del manifiesto en anulado (`ManifestCancelledDepositTests`, cubierto por QA2-F05-008), y `ManifestStateGuard` con su prueba (ya sin uso).

### 8.2 Backend, fase 2 — Entradas, tickets y listados

- **Decisiones:** D2, D6, D25 a D29.
- **Endpoints:** C-F05-22 a C-F05-28.
- **Archivos:** §3.2, filas de BE-2. Sin migración.
- **Casos:** QA2-F05-017 a 026.
- **Notas para FE e I-05** (BE-2, 2026-11-25; los nombres coinciden con las fichas y los esquemas de §2.3):
  - **C-F05-22:** `canEdit` es `true` también en Cerrado (regla de D25: depósito no anulado y entrada no anulada). Los campos nuevos viajan también en C-F03-13 y en la respuesta de C-F05-23 (mismo DTO); Zod de Báscula los descarta.
  - **C-F05-23:** (1) `dateTimeEntry` se compara al minuto: si llega en el mismo minuto que la de hoy, no cuenta como cambio. (2) El motivo de la corrección sigue opcional para CE, como C-F01-90. (3) Las reglas de Vigilancia son las de C-F01-07, extraídas a `EntryLogCorrector` (las usan las dos correcciones, sin cambio de comportamiento en C-F01-07): además del 409 de la categoría, 409 «La placa {placa} ya tiene un ingreso abierto.», 404 «El motivo de ingreso no existe.», los 400 de la placa y los de la fecha («… no puede ser futura.», «… posterior a la salida registrada (…).», «… posterior al primer pesaje del ingreso (…).»). (4) `currency` fuera de COP o USD: 400 «La moneda debe ser COP o USD.». (5) Los cambios de Vigilancia marcan el ingreso como corregido y quedan en la auditoría de `entry_logs`, con la descripción de la corrección de la entrada (incluye el motivo).
  - **C-F05-24:** la acción pasó a `EntryCorrectionController`; ruta, petición y respuesta sin cambios. Bodega recibe 403.
  - **C-F05-25:** `merchandise[].quantity` es lo declarado en el camión; `grossWeight` es el indicador y `tareWeight` la tara real o calculada, como C-F05-22.
  - **C-F05-26:** `status` ahora acepta varios valores separados por coma; uno inválido responde 400 «El valor «{valor}» no es válido para status.». Los filtros de texto se aplican en memoria (los días se calculan en hora de Colombia), sin tildes ni mayúsculas. Sin `sortField` ni `sortOrder` queda el orden de hoy (días faltantes y número del depósito).
  - **C-F05-27 y C-F05-28:** las columnas de la lista blanca existen en `PackingListFileDto` y `PackingListItemDto`; `quantity` es calculada y se ordena por bultos × unidades por bulto. El 400 sin importador es el de hoy, «Seleccione el importador.» (la ficha lo citaba como «Indique el importador.»; gana el de hoy, que la ficha manda conservar). El filtro `status` de los artículos sigue siendo de un valor, como hoy.
- **Estado:** hecha el 2026-11-25 (BE `aac6de8`, rama `f2/f05-comercio-exterior`). QA2-F05-017 a 026 en PASA por API (`EntryCorrectionTests` (los casos `F05_*`: 017, 018, 019 y 026), `EntryTicketsEndpointTests` (020 a 022), `AbandonmentListTests` (023) y `PackingListsListTests` (024 y 025)). `dotnet build Wms.sln` sin errores; `Wms.Tests` 2315 → 2326 y `Wms.IntegrationTests` 846 → 858, todas en verde. Sin migración; `has-pending-model-changes` limpio.

### 8.3 Backend, fase 3 — Levantes e inventario nacionalizado

- **Decisiones:** D9, D10, D23 (lecturas), D30 a D33.
- **Endpoints:** C-F05-29 a C-F05-36.
- **Archivos:** §3.2, filas de BE-3. Sin migración.
- **Transición:** la importación completa de ensayo de §7.
- **Casos:** QA2-F05-027 a 036.
- **Notas para FE e I-05** (BE-3, 2026-11-25; los nombres coinciden con las fichas y los esquemas de §2.3):
  - **C-F05-29 y C-F05-30:** `acceptanceDate` ya no está en la petición; si llega, se ignora. La respuesta la sigue trayendo, igual a `releaseDate` (D9).
  - **C-F05-30:** una `manualExchangeRate` positiva y distinta de la guardada reemplaza la tasa aunque el PATCH no traiga `fobUsd` (si el levante tiene valor en aduanas); `exchangeRateDate` pasa a hoy y el origen sigue `P01/` D43 (`Weekly` si es la de la semana del levante; si no, `Manual`). Con la misma tasa o sin ella, se conserva la guardada. Regla pura `ReleaseRateRules`.
  - **D31 en el backend:** además de los mensajes de la ficha, los de la entidad dicen «valor en aduanas» («El valor en aduanas no puede ser negativo.» y «El producto del levante {N} ya tiene valor en aduanas; no puede recibir el de otro producto.»). El texto de importación del legacy (`fob_dolares`) no cambia.
  - **C-F05-32:** (1) `nationalizationStatus` acepta uno o varios valores separados por coma, como `status` en C-F05-01; uno inválido responde 400 «El valor «{valor}» no es válido para nationalizationStatus.». (2) `search` admite hasta 100 caracteres (400 «La búsqueda admite hasta 100 caracteres.»); busca en número de depósito, número del documento (`CargoManifestNumber`), importador, nombre o descripción del producto y número de levante, sin tildes ni mayúsculas. (3) Estado, diferencia de peso, orden y paginación se calculan en memoria sobre los depósitos que pasan la búsqueda y las fechas, con `ReleaseDepositRules` (estado y diferencia de peso de `NationalizationRules`, como el detalle). (4) `enteredWeight` es la suma del peso de ingreso de los productos cuando todos lo tienen; si no, el peso de mercancía del depósito (nulo en los migrados, que no tienen entradas). (5) `releaseCount` cuenta número y aceptación distintos (un levante con varios productos cuenta una vez). (6) `entryDate` es la fecha de ingreso del depósito o, sin ella, su creación. (7) Los parámetros viejos (`releaseNumber`, `warehouseStorageNumber`, `importerId`, `customsAgencyId`, `fromDate`, `toDate`) ya no filtran. `ReleaseListItemDto` se borró.
  - **C-F05-33:** los mismos filtros de C-F05-32 sin el estado; `total` cuenta los depósitos que pasan la búsqueda y las fechas.
  - **C-F05-34:** el rango cuenta los dos extremos (un año bisiesto completo, 366 días, se acepta). Los depósitos salen por número ascendente; los anulados no salen. La fecha de ingreso de cada mercancía es la del depósito; `customerName` es el cliente del depósito. Bodega, Báscula, Vigilancia y Facturación reciben 403.
  - **C-F05-35:** carta horizontal; título «INFORME DE MERCANCÍAS NACIONALIZADAS EXISTENTES EN DEPÓSITO», levantes del rango debajo de cada mercancía, totales, las firmas y «Página N de M». El archivo es `inventario-nacionalizado-{desde}-{hasta}.pdf`.
  - **Importación de ensayo (§7, QA2-F05-036):** en la base `c2ca314` y en la rama, conteos iguales a los de la fase 6 de F01 (productos 1.643; 128 depósitos migrados con 133 líneas; saldo 136.499; ingresado 203.255; 107 levantes con 107.026,37 levantados; terceros 1.390; vehículos 10.393; conductores 4.361; ciudades 1.774), y en la rama las 133 líneas con amparado = ingresado. Sobre esos datos, C-F05-32, C-F05-33 y C-F05-34 responden en menos de 80 ms: 128 depósitos de importación, 58 sin nacionalizar, 9 parciales, 61 nacionalizados y ninguno con diferencia de peso (los migrados no tienen peso de ingreso).
- **Estado:** hecha el 2026-11-25 (BE `d94f831`, rama `f2/f05-comercio-exterior`). QA2-F05-027 a 036 en PASA por API (`ImportReleaseTests` (027, 028, 029 y 035; la parte de 029 del segundo producto con valor y del heredero, en `ReleaseValueOnceTests`), `ReleaseDepositsEndpointTests` (030 y 031), `NationalizedInventoryReportTests` (032 a 034; el texto de las firmas y de la columna «Valor en aduanas (USD)» lo prueba `NationalizedInventoryRangeTests` en `Wms.Tests`, porque el PDF guarda el texto comprimido) y la importación de ensayo (036)). `dotnet build Wms.sln` sin errores; `Wms.Tests` 2326 → 2344 y `Wms.IntegrationTests` 858 → 872, todas en verde. Sin migración; `has-pending-model-changes` limpio. **Parte 1 cerrada.**

### 8.4 Maquetación, fase 1 — Contratos, fuentes, fila expandible, depósitos por tipo y tickets

- **Decisiones:** D1, D3, D4, D28 (columnas), D34, D36, D44 (`MAQUETACION_PAGES`).
- **Contratos:** todos los de §2.3 (FE-2 y FE-3 los usan). Fuentes simuladas: `deposit`, `entry-ticket` y la fachada `catalog`; datos ficticios con los ejemplos de los wireframes y sin personas reales; los de FE-2 y FE-3 pueden ir en su fase.
- **Pantallas:** P-CE-01 en sus tres rutas (`/foreign-trade/imports`, `/exports`, `/inspections`, que reemplazan a las de hoy en la rama) y P-CE-09 (`/foreign-trade/entry-tickets`). Sin enlazar nada nuevo en el menú (M4). «Ver depósito» lleva al `[id]` de su tipo, que en FE-1 todavía es el de hoy.
- **Lista del wireframe P-CE-01:** filtro de estado (uno, Borrador por defecto) y fechas en la tarjeta de filtros; columnas Fecha, N.º de depósito con placas, Doc. comercial, Tiquetes, Terceros (cliente e importador; exportador en exportación), Mercancía (embalaje), Pesos (bruto, mercancía, tara, manifiesto), Estado (con «n etapas pendientes»), Acciones («Ver depósito»); filtros por columna en número, documento, tiquete y mercancía; orden; expandida de D4; «Exportar».
- **Lista del wireframe P-CE-09:** columnas de la etapa Entradas más el N.º de depósito como enlace; filtros por columna (fecha, placa, conductor, tiquete, mercancía, depósito); «Editar».
- **Casos:** la lista de cada pantalla con su captura en `D/planes/sprint-11/f05-comercio-exterior/evidencias/fe1-*`.
- **Estado:** hecha el 2026-11-25 (FE `8881589`, rama `f2/f05-comercio-exterior`, con push).
  - **Cifras:** `yarn build` con código 0; `yarn test` 709 → 734 pruebas (141 → 143 archivos), todas en verde, guardias incluidas; `yarn lint` 190 → 184 errores (las tres listas viejas se reemplazaron), ninguno en archivos nuevos. `yarn test` sale con código 1 por un rechazo no manejado de `FT/components/weighbridge/WeighbridgeQueuePage.spec.ts` que ya estaba en la base (2 en la base, 1 ahora); no es de F05.
  - **P-CE-01** (`/foreign-trade/imports`, `/exports`, `/inspections`, `DepositListTable` y `DepositListExpansion`): tarjeta de filtros con el estado (uno, Borrador por defecto) y las fechas de ingreso; columnas Fecha, N.º de depósito con placas, Doc. comercial (en inspección, «Documento», con la descripción si no hay documento), Tiquetes, Terceros (cliente con importador; exportador en exportación), Mercancía con embalaje, Pesos (bruto, mercancía, tara, manifiesto), Estado (con la nacionalización en importación y «n etapas pendientes», con las etapas en el tooltip) y «Ver depósito» (solo icono, solo en la fila principal); filtros por columna en número, documento, tiquete y mercancía; orden en Fecha, número, documento, tiquete y mercancía; «Exportar» en la barra (P-TR-02: el wireframe lo pone en la tarjeta de filtros, gana el patrón). Fila expandida de D4: manifiesto DIAN y valor; un bloque por producto con placa, cantidad, peso, tiquete, MPreimp y «Tarjeta del vehículo» y «Tiquete»; entra, ampara y saldo por producto (en rojo si no es cero); totales de cantidad y peso y «Gestionar amparados» (`?etapa=amparados`). Inspección sin amparados ni «Gestionar amparados». Capturas `fe1-01` a `fe1-05`.
  - **P-CE-09** (`/foreign-trade/entry-tickets`): columnas de la etapa Entradas más el depósito como enlace (con su tipo debajo); filtros por columna en fecha (rango), placa, conductor, tiquete, mercancía y depósito; «Editar» (si `canEdit`) a `/foreign-trade/entries/{warehouseStorageEntryId}?volver=/foreign-trade/entry-tickets`. Capturas `fe1-06` y `fe1-07`.
  - **D34:** `AppDataTable` suma `expandable`, `v-model:expandedRows` (las abiertas por `dataKey`) y el slot `expansion`; el botón «Expandir»/«Contraer» va en la primera columna con tooltip y `aria-expanded`. Prueba en `FT/unit/components/AppDataTable.spec.ts` y ejemplo en la galería (`fe1-08`).
  - **Notas para FE-2 y FE-3:** (1) la respuesta de hoy del retiro de un levante es el detalle del depósito (`foreign-trade-service.ts:210`), así que `releaseWithdrawResultSchema` es `depositDetailSchema` y vive en `deposit.ts` (`release.ts` no puede importarlo: ciclo); `nationalizationStatusSchema` vive en `release.ts` y `deposit.ts` lo reexporta. (2) `entryCorrectionScaleSchema` (`F/features/weighbridge/contracts/entry-edit.ts`) omite los cuatro campos nuevos de C-F05-23, así la corrección de Báscula no cambia. (3) El mundo simulado está en `F/features/foreign-trade/mocks/world.ts` (14 depósitos de `mocks/data/deposit.ts`, numeración `2026BA000nn`; las entradas con `minutesAgo` se fechan al cargar la página); FE-2 le suma el detalle. (4) La fachada `catalog.source.ts` solo tiene el tiquete (C-F03-35); FE-2 suma lo demás de D36. (5) Textos de tipo, estado, etapas y nacionalización en `F/features/foreign-trade/utils/deposit-display.ts`, con `depositDetailPath`; consultas y claves (`['foreign-trade', …]`) en `composables/deposit.queries.ts`. (6) «Ver depósito» y el enlace de Tickets abren el `[id]` de hoy, que con los Id simulados no carga datos hasta FE-2; «Editar» lleva a P-CE-03, que crea FE-2.
  - **Nota para I-05:** las cuatro páginas están en `MAQUETACION_PAGES`; las fuentes nuevas son `deposit`, `entry-ticket` y `catalog` (esta se borra).

### 8.5 Maquetación, fase 2 — Detalle por etapas

- **Decisiones:** D1 (detalle), D11, D13, D14, D16, D22 (pintado), D35, D37 a D42.
- **Pantallas:** P-CE-02 a P-CE-06 (en `[id]` de los tres tipos, con `DepositStageDetail`), P-CE-03 (`/foreign-trade/entries/[entryId]`) y Salidas vacía. Fuentes simuladas `deposit` (detalle), `deposit-edit` y las de la fachada.
- **Listas del wireframe:** P-CE-02 (encabezado con número, tipo, estado de nacionalización y del depósito, «Volver» y «Acciones»; stepper con seis etapas e indicador; información general sin subpartida; progreso; Entradas con sus columnas y acciones); P-CE-03 (secciones 1 a 5, switch «Unidad de carga», unidades, fecha del manifiesto, precio y moneda; «Guardar» y «Volver» en el encabezado); P-CE-04 (bloques Ingreso, Documento comercial, Manifiesto DIAN, Terceros y Pesos y valor CPI; «+»; transportadoras en solo lectura; un «Guardar»); P-CE-05 (recepciones con reloj, inventario, botones); P-CE-06 (columnas de la tabla, saldo en rojo, «+ Agregar producto», quitar, «Guardar»).
- **Casos:** capturas en `evidencias/fe2-*`.
- **Estado:** hecha el 2026-11-25 (FE `45defb9`, rama `f2/f05-comercio-exterior`, con push).
  - **Cifras:** `yarn build` con código 0; `yarn test` 734 → 774 pruebas (143 → 148 archivos), todas en verde, guardias incluidas; `yarn lint` 184 → 171 errores (299 → 295 avisos; los tres detalles viejos se reemplazaron), ninguno en archivos nuevos ni tocados. `yarn test` sigue saliendo con código 1 por el rechazo no manejado de `FT/components/weighbridge/WeighbridgeQueuePage.spec.ts` que ya estaba en la base (1 antes, 1 ahora); no es de F05. Sin llamadas reales: las cuatro páginas nuevas o reescritas en `MAQUETACION_PAGES`, el grep de cierre sin `useApi`, servicios `*-service`, fuentes de `INTEGRATED_SOURCES` ni componentes de hoy que llamen al API, y ninguna petición al API en el navegador. Ninguna ruta nueva en el menú. Revisado en el navegador con la sesión simulada (`?roles=Admin,ForeignTrade` y `?roles=ForeignTrade`).
  - **P-CE-02** (`DepositStageDetail` en `/foreign-trade/{imports,exports,inspections}/[id]`): encabezado con número, tipo, nacionalización (importación), estado, impresiones de la etiqueta, prórroga, planilla y el aviso del estado financiero del cliente; «Volver» (a la lista del tipo) y «Acciones» con Confirmar (diálogo con los requisitos de C-F05-08 y «Ir a {etapa}»), etiqueta, tarjeta por vehículo, PDF, planilla de envío, prórroga (importación confirmada) y Anular al final; stepper con las etapas del tipo (seis, cinco o cuatro) y su indicador; etapa en `?etapa=` y migas Comercio Exterior › Depósitos › {tipo} › {número}; información general sin subpartida, balance de cantidades (sin amparado en inspección), balance de pesos y progreso. Entradas con las columnas del wireframe, la marca «Datos pendientes» de D11, totales y las seis acciones de D40 en el menú ⋮. Capturas `fe2-01` a `fe2-05` y `fe2-16`.
  - **P-CE-03** (`/foreign-trade/entries/[entryId]`, `EntryEditForm`): «Volver» y «Guardar» en el encabezado; 1. Vigilancia y 2. Camión y conductor resumidas con «Editar»; 3. Registro de operación (modalidad sin cambio, documento con la elección del depósito de C-F05-24, manifiesto, mercancía con «+»); 4. Pesaje; 5. Comercio Exterior (switch «Unidad de carga» con sus unidades, fecha del manifiesto, precio y moneda del depósito); motivo obligatorio. Capturas `fe2-12` y `fe2-13`.
  - **P-CE-04** (Datos principales): bloques Ingreso (con motivo si cambia la fecha), Documento comercial (descripción en inspección), Manifiesto DIAN (importación, con prefijo), Terceros con «+» (cliente opcional; importador y agencia, o exportador), transportadoras en solo lectura, Pesos y valor CPI precargados (D14, AF-94) y Observaciones; un «Guardar» con el aviso de período abierto o factura recalculada. Capturas `fe2-06`, `fe2-07`, `fe2-14` y `fe2-15`.
  - **P-CE-05** (Bodega): recepciones con estado, `WarehouseClockTag`, contado, ubicación y cuadrilla; inventario por producto; «Ajustar cantidad (CE-7)», «Movimientos» (`/reports/warehouse-movements?deposito=`, que el reporte ahora consulta al llegar) y «Ver novedades». Captura `fe2-08`.
  - **P-CE-06** (Amparados): columnas del wireframe con lo amparado editable, saldo en rojo, «Agregar producto» y «Corregir» con `DepositProductDialog` a dos columnas sin unidad de medida, «Quitar» con motivo (deshabilitado con levante), «Guardar», y el aviso del camión tardío en un confirmado (AF-84). Capturas `fe2-09` a `fe2-11`.
  - **Salidas** vacía (D38) en los tres tipos, sin llamar a nada. Levantes queda en solo lectura (`DepositReleasesStage`); FE-3 la completa.
  - **Gana la Dn (`DEC-002`):** el saldo es amparado − ingresado (D13): el wireframe pone −90 y la pantalla +90. D36 manda sobre §3.1: los diálogos de hoy que llaman al API (`RegisterExtensionDialog`, `CargoUnitBreakdownDialog`, `AssociatePackingListItemsDialog`, `LabelPrintsBadge`, `AdjustInventoryDialog`, `DepositConfirmationRequirements`) no se importan; la maquetación usa equivalentes sobre la fuente activa (`EntryCargoUnitDialog`, `EntryPackingListDialog`, `DepositAdjustDialog` y los diálogos de `DepositStageDetail`), y `FinancialStatusAlert` se reusa porque no llama al API.
  - **Notas para FE-3 e I-05:** (1) contratos sumados en `deposit-misc.ts`: `depositCargoUnitSchema` (C-F01-145) e `inventoryAdjustmentSchema` (C-F05-48), con la forma de hoy; `contracts/catalog.ts` reexporta los esquemas de F01 y F03 de la fachada. (2) Fuentes nuevas: `deposit-edit` y `packing-list` (solo artículos y asociación; FE-3 suma los archivos); `deposit` y `catalog` crecen. (3) «Contado», «Ubicación» y «Cuadrilla» de P-CE-05 salen del contrato sin cambiarlo: lo declarado del camión recibido, las `locations` de sus productos y el `crewName` del depósito (C-F05-22 no los trae por recepción). (4) Las migas leen el número que el detalle recuerda (`rememberDepositNumber`) y una navegación `force` las repinta al cargar. (5) La columna derecha pasa debajo de la etapa con menos de 1600 px para que la tabla de Entradas quepa. (6) I-05 decide si conserva los diálogos de la maquetación o vuelve a los de hoy (D46 no borra `RegisterExtensionDialog` ni `AdjustInventoryDialog`). (7) `DepositProductsTable` y los componentes del detalle viejo quedan sin uso hasta que I-05 los borre (D46).

### 8.6 Maquetación, fase 3 — Levantes, reportes y listados

- **Decisiones:** D10, D23, D29 a D33, D43 (solo el enlace del dashboard dentro de la rama, sin menú).
- **Pantallas:** P-CE-07 (etapa Levantes), P-CE-10 (`/foreign-trade/releases`, reemplaza a la de hoy en la rama), P-CE-12 (`/reports/nationalized-inventory`, sin tarjeta de título, `h1` oculto y acciones en la fila de la tarjeta de filtros), Abandono y Listas de empaque al patrón, y los rótulos de D31 en Movimientos por depósito y Póliza.
- **Listas del wireframe:** P-CE-07 (encabezado con «Exportar» y «Nuevo levante», cuatro tarjetas, alerta de diferencia de peso, tabla agrupada por mercancía con su fila editable y nacionalizado y saldo); P-CE-10 (búsqueda, contadores, «Con diferencia de peso», columnas, expandida con «Agregar levante»); P-CE-12 (rango, «Consultar», «Descargar PDF», «Exportar Excel», agrupado por depósito, firmas).
- **Casos:** capturas en `evidencias/fe3-*`.
- **Estado:** hecha el 2026-11-25 (FE `fe18386`, rama `f2/f05-comercio-exterior`, con push). Parte 2 cerrada.
  - **Cifras:** `yarn build` con código 0; `yarn test` 774 → 814 pruebas (148 → 152 archivos), todas en verde, guardias incluidas; `yarn lint` 171 → 171 errores (295 → 295 avisos), ninguno en archivos nuevos ni tocados. `yarn test` sigue saliendo con código 1 por el rechazo no manejado de `FT/components/weighbridge/WeighbridgeQueuePage.spec.ts` que ya estaba en la base (1 antes, 1 ahora); no es de F05. Sin llamadas reales: las cuatro páginas reescritas o nuevas en `MAQUETACION_PAGES` y ninguna petición al API en el navegador. Ninguna ruta nueva en el menú. Revisado en el navegador con la sesión simulada (`?roles=Admin,ForeignTrade` y `?roles=ForeignTrade`).
  - **P-CE-07** (etapa Levantes, `DepositReleasesStage` y `ReleaseEditableRow`): «Exportar» (Excel de los levantes del depósito) y «Nuevo levante» (lleva el foco a la primera fila con saldo); cuatro tarjetas (ingreso, nacionalizado con % y barra, saldo en bodega, levantes con mercancías y completas); alerta de diferencia de peso con la regla de D23 (MK-04); tabla agrupada por mercancía con el ingreso, los levantes (N.º, aceptación, fecha, tasa, valor en aduanas USD y COP, cantidad, peso) con «Ver levante» (drawer), «Editar» (la fila pasa a editable con la tasa guardada) y «Retirar» (motivo), la fila editable con el saldo y lo nacionalizado y el saldo del producto (en rojo con «x kg nacionalizados por encima del ingreso»). Fila editable de D30: prefijos precargados (C-F01-08), fecha de hoy y nunca futura, tasa de la semana precargada y editable (C-F01-13 por la fachada), valor en pesos al digitar, cantidad desde el peso con un producto, «Levante total del saldo», tope en lo pendiente, Enter guarda y Esc cancela; al guardar vuelve a ofrecerse con el nuevo saldo (H-040). Sin fecha de aceptación (D9). Capturas `fe3-01` a `fe3-04`.
  - **P-CE-10** (`/foreign-trade/releases`, reemplaza la de hoy en la rama): búsqueda (depósito, documento, importador, mercancía o N.º de levante), pestañas Todos, Sin nacionalizar, Parcial y Nacionalizados con sus contadores (C-F05-33) y «Con diferencia de peso» en la barra; columnas fecha de ingreso (rango), depósito (enlace al detalle en `?etapa=levantes`), documento comercial con manifiesto, importador, mercancía con embalaje, ingreso, nacionalizado (con % y barra), saldo y estado con el número de levantes; orden por fecha, depósito y %; «Exportar»; fila expandida con la vista compacta de la etapa («Agregar levante» y «Ver detalle del depósito»). `?estado=sin-nacionalizar|parcial|nacionalizados` abre la pestaña. Capturas `fe3-05`, `fe3-06` y `fe3-08`.
  - **P-CE-12** (`/reports/nationalized-inventory`, `NationalizedInventoryReport`): sin tarjeta de título, `h1` oculto; «Levantes desde» y «Hasta» (por defecto el mes en curso, hasta 366 días), «Consultar», y «Descargar PDF» y «Exportar Excel» a la derecha en la fila de la tarjeta de filtros, con la regla del reporte al pie; agrupado por depósito (documento, agencia, importador y cliente), por mercancía (embalaje, ingreso, manifiesto DIAN, ingreso, existencia y nacionalizados) con sus levantes del rango, totales y las firmas «Jefe de Bodega» y «Recibí conforme». Captura `fe3-07`.
  - **Abandono y prórrogas** (al patrón, C-F05-26, C-F05-49, C-F05-43): resumen de alerta y abandono arriba de la tabla con «Ver en alerta» y «Ver en abandono»; filtros por columna en depósito, carta porte, fecha de ingreso (rango), estado, prórroga, importador, agencia y cliente; orden por depósito, fecha, días que faltan, estado e importador (por defecto días que faltan); «Exportar»; «Registrar prórroga» por fila. `?estado=` como hoy (sin parámetro, «En alerta»). «Días» y «Plazo» van en una columna («46 / 30 días») y «Por nacionalizar» y «Existencias» en otra, para que la tabla quepa con sus acciones. Capturas `fe3-09` y `fe3-10`.
  - **Listas de empaque** (al patrón, C-F05-27, C-F05-28, C-F05-50): pestañas «Archivos» y «Artículos» en la barra de cada tabla y «Cargar lista de empaque» como acción de la barra; Archivos con filtros y orden en archivo, proveedor, importador y fecha, «Ver artículos» (drawer `PackingListFileDrawer`, con «Eliminar» en su menú) y «Eliminar» (confirmación); Artículos con el importador obligatorio en la barra (selector con búsqueda) y filtros en código, descripción, depósito y estado; «Exportar» en las dos. La carga (`PackingListImportDialog`) simula y luego importa el CSV, que la fuente simulada lee de verdad con los textos del backend. Capturas `fe3-11` a `fe3-14`.
  - **Rótulos de D31:** «Valor en aduanas (USD)» en Movimientos por depósito (tabla y Excel) y en Póliza («Valor en aduanas UAP (USD)», «Valor en aduanas no UAP (USD)», «Total valor en aduanas»). Esas páginas ya llaman al API real, así que no tienen captura en la maquetación. El tablero de CE enlaza «Sin nacionalizar» y «Nacionalizados» a `/foreign-trade/releases?estado=…` (D43).
  - **Nota de BE-2 aplicada:** el 400 sin importador de C-F05-28 es el de hoy, «Seleccione el importador.» (§8.2); la fuente simulada lo usa.
  - **Notas para I-05:** (1) fuentes nuevas: `release`, `abandonment` y `F/features/reports/services/nationalized-inventory.source.ts`; `packing-list` suma archivos, detalle, borrado, proveedores y carga; la fachada `catalog` suma `exchangeRateForDate` (C-F01-13). (2) Páginas en `MAQUETACION_PAGES`: `releases/index.vue`, `abandonment/index.vue`, `packing-lists/index.vue` y `reports/nationalized-inventory.vue`. (3) Componentes nuevos además de los de D35: `ReleaseDepositExpansion` (la fila expandida de P-CE-10 lee el detalle), `PackingListFileDrawer` y `PackingListImportDialog` (equivalente sobre la fuente activa de `PackingListUploadDialog`, que llama al API; I-05 decide con cuál se queda, como los diálogos de FE-2). `PackingListItemsDialog`, `AbandonmentSummaryAlert` y `RegisterExtensionDialog` no se usan en estas páginas. (4) El mundo simulado suma los depósitos 2026BA00015 a 2026BA00017 (levantes con diferencia de peso, sin levantes y nacionalizado), los levantes con número, aceptación, fecha, valor en aduanas y tasa, y las tasas semanales ficticias de `mocks/data/catalog.ts`. (5) Consultas en `composables/release.queries.ts`, `abandonment.queries.ts`, `packing-list.queries.ts` y `F/features/reports/composables/nationalized-inventory.queries.ts`; cálculos de D30 en `utils/release-quantity.ts`.

### 8.7 Revisión del usuario (después de FE-3)

Con FE-1 a FE-3 cerradas y con push, el usuario revisa las pantallas en `yarn dev` con la sesión simulada (`NUXT_PUBLIC_MOCK_SESSION=true`; `?roles=Admin,ForeignTrade` y `?roles=ForeignTrade`) antes de I-05. Si pide ajustes, van en un plan de ajustes de la maquetación, como el de F03 y F04, y se ejecutan en `f2/f05-comercio-exterior` antes de I-05. El agente de maquetación, al cerrar FE-3, le dice qué rutas abrir y con qué roles: las tres listas de depósitos, un detalle de cada tipo con cada etapa, `/foreign-trade/entries/{id}`, `/foreign-trade/entry-tickets`, `/foreign-trade/releases`, `/reports/nationalized-inventory`, `/foreign-trade/abandonment` y `/foreign-trade/packing-lists`.

- **Ajustes durante la revisión** (2026-11-25): (1) ancho del contenido: se quitó el ancho fijo de 1504 px de `.layout-content` (FE `0ee7de6`) y el usuario pidió deshacerlo; queda como estaba (FE `1af6707`).

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | La edición en Confirmado recalcula facturas ya enviadas y sorprende a Facturación | `DEC-022` ya lo prevé (misma factura, N.º SIIGO y aviso con los dos totales); un guardado, un recálculo (D5, D19); QA2-F05-007 |
| R2 | La apertura tardía (D17) de un depósito con ingreso de hace meses tarda varios días en ponerse al día, porque la renovación abre un período por pasada | Es el comportamiento de hoy del trabajo y del cobro de los migrados; Facturación ve la primera factura al asignar el cliente. Si hiciera falta abrirlos todos de una vez, se decide aparte |
| R3 | `GET foreign-trade/deposits` cambia de forma y el tablero deja de funcionar dentro de la rama antes de I-05 | Es lo esperado (`PM/` §5.4): el tablero se borra en I-05; nada se despliega hasta el final (M25) |
| R4 | El cambio de `AppDataTable` (D34) afecta a las 26 páginas que lo usan | Aditivo, apagado por defecto, con prueba; las guardias y la suite completa al cerrar FE-1 |
| R5 | Los tres DTO del detalle divergen al sumarles campos | Un solo constructor de los bloques nuevos (`DepositDetailBlocksDto.cs`, que ya existe) y un solo esquema en el frontend |
| R6 | D42 (tasa, solo Borrador) y D19 (edición, todos los estados) se comportan distinto con una factura aprobada | Decidido por el usuario (D8); se anota en la nota de la integración para Facturación |
| R7 | El detalle de hoy tiene funciones que el wireframe no dibuja (planilla de envío, reparto en unidades, listas de empaque, prórroga, etiquetas) | D39 y D40 las ubican; QA2-F05-044 y 058 las recorren (`DEC-005`) |
| R8 | El contrato de las entradas del depósito (C-F05-22) lo comparte Báscula (C-F03-13) | Campos aditivos; Báscula no los declara (Zod los descarta); C-F03-13 no cambia |
| R9 | F06 necesita la etapa Salidas y el cliente obligatorio | D38 deja el lugar; C-F05-21 queda en el contrato; F06 los consume |
| R10 | Videos, manuales y casos QA de la campaña de CE quedan desactualizados | Lista en el despliegue final (`PM/` R13) |

---

## 10. Fuera de alcance

- Las salidas: P-CE-08 con datos, P-CE-11, «Nueva salida», el retiro de «Órdenes de cargue» y «Guías de salida» y sus páginas (F06, AF-97). F05 deja la etapa vacía (D38) y C-F05-21.
- La facturación por CPI y sus reportes (F07 y F08); el acceso de Facturación a Póliza (F08, AF-111).
- Abrir de una vez todos los períodos vencidos de una apertura tardía (R2).
- Retirar `GET foreign-trade/warehouse-storages/{id}/stakeholders`, `imports/{id}/validation-info` e `imports/{id}/validate` del backend (quedan sin uso en el frontend; se pueden retirar aparte).
- Los avisos configurables (F09), staging y el despliegue final (`PM/` §7.3), y estimar esfuerzo.

**Cambios al hub** (aprobados por el usuario el 2026-11-25, «Aprobar con §10»; los aplica I-05 al cerrar, §13.4):

1. `D/contexto/convenciones-tecnicas.md` §3, «Tablas de listado», al final de la viñeta «Filtros»: «**Fila expandible** (F05, D34): un maestro-detalle usa `AppDataTable` con `expandable`, `v-model:expandedRows` y el slot `expansion`; las acciones van solo en la fila principal (AF-99).»
2. `D/contexto/decisiones.md`, `DEC-029`, después de «*El rótulo «CIF», reemplazado por `DEC-080` (AF-81).*»: «*Construido en F05 de la fase 2 («Valor en aduanas» en pantallas, impresos y mensajes, D31).*»

---

## 11. Prompts por parte

- Backend: [prompt-f2-f05-comercio-exterior-backend-2026-11-25.md](prompt-f2-f05-comercio-exterior-backend-2026-11-25.md)
- Maquetación: [prompt-f2-f05-comercio-exterior-maquetacion-2026-11-25.md](prompt-f2-f05-comercio-exterior-maquetacion-2026-11-25.md)
- Integración (I-05): [prompt-f2-f05-comercio-exterior-integracion-2026-11-25.md](prompt-f2-f05-comercio-exterior-integracion-2026-11-25.md)
- Planificador: [prompt-f2-f05-comercio-exterior-planificador-2026-11-25.md](prompt-f2-f05-comercio-exterior-planificador-2026-11-25.md)

---

## 12. Mensajes de commit sugeridos

```text
BE-1: feat(foreign-trade): depósitos por tipo, amparados, edición en Confirmado y apertura tardía (DEC-080, F05)
BE-2: feat(foreign-trade): entradas del depósito, edición por CE, tickets de ingreso y listados con orden (DEC-080, F05)
BE-3: feat(foreign-trade): levantes por depósito, valor en aduanas e inventario nacionalizado (DEC-080, F05)
FE-1: feat(foreign-trade): contratos, fila expandible, depósitos por tipo y tickets con datos simulados (DEC-080, F05)
FE-2: feat(foreign-trade): detalle del depósito por etapas y edición del ingreso con datos simulados (DEC-080, F05)
FE-3: feat(foreign-trade): levantes, inventario nacionalizado, abandono y listas de empaque con datos simulados (DEC-080, F05)
I-05 (1): feat(foreign-trade): integración de depósitos, detalle y edición (DEC-080, F05)
I-05 (2): feat(foreign-trade): integración de levantes, tickets, reportes y listados (DEC-080, F05)
Fusión: merge: I-05, F05 «Comercio Exterior» en fase-2 (DEC-080, DEC-081)
docs: docs(f05): <fase> de F05 (sprint 11)
```

Cada commit termina con la línea de coautoría que indique la sesión.

---

## 13. Integración I-05 (parte 3)

Ocupa los dos repos, en `f2/f05-comercio-exterior`, después de BE-3, FE-3 y la revisión del usuario (§8.7). Dos fases, una por turno.

### 13.1 Fuentes http

Cada `*.source.ts` de D36 pasa a su `*.http.ts` (con `contractApi()` y su esquema), y sus fuentes pasan a `INTEGRATED_SOURCES`. La fachada `catalog.source.ts` se borra y sus usos pasan a las fuentes integradas de F01, F03 y F04. `mocks/` de `foreign-trade` y `reports` se borra (`PM/` §6.3). I-05 (1) hace `deposit`, `deposit-edit` y `entry-ticket`; I-05 (2), `release`, `abandonment`, `packing-list` y `nationalized-inventory`.

### 13.2 Menú, rutas, enlaces y guardias

- Menú de D43 (`F/components/layout/menu-model.ts:83-114` y Reportes `:136-157`); Alt+P y Alt+I (`F/composables/useGlobalShortcuts.ts:24`, `:27`); enlaces del dashboard (`F/pages/foreign-trade/index.vue`) y las migas de los detalles (D42).
- Guardias de D44; `MAQUETACION_PAGES` vacía.

### 13.3 Se borra

Lo de D46 y D45, con `rm`, después de comprobar con grep quién importa cada archivo (trampa 7), con sus pruebas. Lo que use F06 se queda.

### 13.4 Casos QA y docs

QA2-F05-041 a 060 en el navegador (§6.2); los 001 a 036 siguen en verde en la suite. Al cerrar I-05 (2): copia de los casos a `D/qa/casos-qa2-f05-comercio-exterior-AAAA-MM-DD.md` con el formato de `D/qa/casos-qa2-f04-bodega-2026-11-25.md`; los dos cambios al hub de §10 (aprobados el 2026-11-25); `D/contexto/estado.md` (hito de I-05), `D/planes/README.md` y la matriz; y el aviso al usuario de qué puede probar en local (M25).

### 13.5 Criterio de salida

Compuertas de `PM/` §6.3 en los dos repos; QA2-F05-041 a 060 en PASA; ningún import de `mocks/` fuera de las pruebas; menú enlazado; lo viejo borrado; fusión de `f2/f05-comercio-exterior` en `fase-2` en los dos repos con `--no-ff`, y push.

### 13.6 Estado

Pendiente.
