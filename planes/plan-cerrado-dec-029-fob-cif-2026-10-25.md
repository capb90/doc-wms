# Plan cerrado — Lo que se construye por DEC-029 (levante CIF, «Valor de la mercancía», valor único del levante y fórmula prorrateada por defecto)

> **Fecha:** 25 de octubre de 2026. **Estado:** Aprobado por el usuario el 2026-10-25. Ejecutado el 2026-10-25 (BE `dafd573`, FE `d838535`; la fase 3, de docs, sin commit). Prompt del ejecutor, por fase: `prompt-plan-dec-029-fob-cif-2026-10-25.md`.
> **Origen:** `DEC-029` (`contexto/decisiones.md`), respuestas del 2026-10-25 al §7 de `analisis/analisis-fob-cif-legacy-v2-2026-10-24.md`, y las 4 respuestas del usuario a las preguntas de este plan (2026-10-25).
> **Base:** BE `develop` `3cbf181` · FE `develop` `83a0af0` · docs `main` `74416e1`.
> **Alcance:** 3 fases (BE, FE, docs y verificación). Una migración de solo datos, `RenameValueFormulaLabels`. Sin cambios de permisos.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/`; `D/` = `docs/`.

---

## 0. Instrucciones para el ejecutor

1. Lee `B/AGENTS.md`, `D/contexto/convenciones-tecnicas.md`, `DEC-029` y este plan completo.
2. Trabaja en `develop`, sin ramas ni commits (`DEC-003`). Al cerrar cada fase te detienes y entregas el resumen y el mensaje de commit.
3. Las líneas citadas son de la base indicada. Antes de cambiar, confírmalas con grep. Si el código no coincide (rutas, firmas o textos), detente y pregunta, con todas las dudas en un solo mensaje.
4. **Regla de los textos:** solo cambian los textos que ve el usuario y los comentarios que digan lo contrario de `DEC-029`. Los identificadores se conservan: `FobUsd`, `FobCop`, `CargoValue`, `fobUsd`, `release-fob-usd`, `preview-cif`, rutas y nombres de columnas.

---

## 1. Decisiones

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **El valor del levante se rotula CIF.** Los textos del §2.1 y del §3.1 cambian de «FOB» a «CIF», uno a uno. El mensaje de la DIAN conserva el prefijo «No se pudo consultar la TRM de la DIAN», porque el frontend detecta la caída de la DIAN por ese prefijo (`F/app/features/foreign-trade/components/ReleaseForm.vue:53`) | `DEC-029` §7.2 |
| D2 | **La póliza no cambia de cálculo.** Ya suma el valor guardado (`FobUsd`) sin derivar nada (`B/Wms.Application/Reports/Common/PolicySummaryCalculator.cs:21-44`). Cambian sus rótulos y se corrige la premisa «el legacy rotula CIF pero suma el FOB», en `PolicySummaryCalculator.cs:9-13` y `F/app/pages/reports/policies.vue:4-5`: el valor es el CIF, como en el legacy | `DEC-029` §7.2 |
| D3 | **El valor del depósito se llama «Valor de la mercancía»** en todo lo que ve el usuario: captura, detalle, recepción manual, facturación, fórmulas y textos de factura. Desaparecen «Valor Comercial», «Valor de la carga», «valor declarado», «Umbral CIF» y «(CIF)» referidos al depósito. No hay campo nuevo | `DEC-029` §7.3 |
| D4 | **Nombres de las fórmulas, por migración.** En `SeedDataExtensions.SeedFormulaTypes`:<br>• `PERCENTAGE_OF_VALUE` pasa a «Porcentaje del valor de la mercancía (lote completo)»;<br>• `PERCENTAGE_OF_VALUE_PRORATED` conserva «Porcentaje del valor de la mercancía (prorrateado por saldo)»;<br>• `minimumThreshold`, en las dos, pasa a «Umbral del valor de la mercancía por encima del cual no se aplica el mínimo ($)».<br>Llegan a las bases con la migración de datos `RenameValueFormulaLabels`, que se genera con `dotnet ef` (precedente: `20261004212549_AddMinimumIncludesVatSetting`) | Respuesta del usuario: «Sí, con migración» |
| D5 | **Prorrateada por defecto, sin forzarla.** Al crear una regla de tarifa base o un servicio de acuerdo para ALMACENAMIENTO, el formulario preselecciona `PERCENTAGE_OF_VALUE_PRORATED` si la fórmula está vacía. Se puede cambiar a lote completo.<br>• El backend no impone ningún valor por defecto.<br>• Las reglas existentes no se tocan: T1 en staging sigue igual hasta que Facturación defina la tarifa base (`DEC-029` §7.7 y §7.10) | `DEC-029` §7.5, §7.7 y §7.10 |
| D6 | **Bloqueo del valor repetido del levante.** Al registrar o editar un producto de levante con valor mayor que 0, si otro producto del **mismo depósito** con el mismo número y aceptación ya tiene valor mayor que 0, el backend responde **409**: «El CIF del levante {número} ya se registró con «{producto}». Registre este producto sin valor.»<br>• La comparación usa recorte y mayúsculas, como `ReleaseDuplicateRules`, y excluye el registro que se edita.<br>• El formulario deshabilita el campo de valor, lo deja vacío y muestra ese producto. El aviso naranja de hoy (DF4) desaparece.<br>• El producto que tiene el valor lo puede editar o quitar | Respuesta del usuario: «409 y campo deshabilitado» |
| D7 | **Al retirar el producto con valor, el valor pasa al siguiente.** Si el levante retirado tenía valor y quedan otros productos del mismo levante (mismo depósito, número y aceptación), el valor pasa al más antiguo de ellos (`CreatedAt` y luego `Id`).<br>• Se copian tal cual los cinco campos: `FobUsd`, `ExchangeRate`, `ExchangeRateSource`, `ExchangeRateDate` y `FobCop`, sin recalcular. El `FobCop` de un migrado viene del legacy y no siempre es `FobUsd × tasa`.<br>• La descripción de auditoría del retiro dice a qué producto pasó el valor.<br>• Si no quedan otros productos, el valor se va con el retiro, como hoy | Respuesta del usuario: «Pasa al siguiente producto» |
| D8 | **Videos:** se ajustan los selectores y textos de los scripts de grabación (`F/tools/video-tutoriales/`) y los guiones (`D/videos/guiones/`), y se deja el inventario de videos y subtítulos publicados que quedan desactualizados. Regrabar y republicar es una tarea aparte | Respuesta del usuario: «Ajustar scripts; regrabar aparte» |
| D9 | **Fuera de alcance:**<br>• renombrar columnas o propiedades;<br>• la normalización de mayúsculas al agrupar en el kárdex (`KardexAggregator.cs:77-91`);<br>• corregir datos existentes con un valor repetido (solo se cuentan, §5; sin SQL, `DEC-006`);<br>• cambiar T1 y las tareas de Facturación de `DEC-029` (§7.6, §7.7, §7.9 y §7.10);<br>• desplegar en staging | `DEC-029`; `DEC-006` |

---

## 2. Fase 1 — Backend

### 2.1 Textos del levante (D1, D2)

| Archivo | Hoy | Queda |
| --- | --- | --- |
| `B/Wms.Application/Warehouse/Common/Services/WarehouseMovementsPdfService.cs:281` | `"FOB USD"` | `"CIF USD"` |
| `B/Wms.Application/ForeignTrade/Commands/RegisterImportRelease/RegisterImportReleaseCommandValidator.cs:41-42` y `B/Wms.Application/ForeignTrade/Commands/UpdateImportRelease/UpdateImportReleaseCommandValidator.cs:39-40` | «El FOB no puede ser negativo.» · «El FOB admite máximo 2 decimales.» | «El CIF no puede ser negativo.» · «El CIF admite máximo 2 decimales.» |
| `B/Wms.Domain/Entities/ForeignTrade/ImportRelease.cs:174`, `:197` y `:118` | «El FOB no puede ser negativo.» · «El levante tiene FOB sin tasa de cambio.» | «El CIF no puede ser negativo.» · «El levante tiene CIF sin tasa de cambio.» |
| `B/Wms.Application/ForeignTrade/Common/Services/ReleaseFobService.cs:82` | «No se pudo consultar la TRM de la DIAN. Digite la tasa de cambio para registrar el FOB.» | «No se pudo consultar la TRM de la DIAN. Digite la tasa de cambio para registrar el CIF.» (el prefijo no cambia) |
| `B/Wms.Application/Administration/LegacyImport/Importers/ReleasesImporter.cs:59`, `:61` | «El FOB en dólares» · «El FOB en pesos» | «El CIF en dólares (fob_dolares)» · «El CIF en pesos (fob_pesos)» |
| `B/Wms.Application/Administration/LegacyImport/Common/LegacyReleaseGrouper.cs:50` | «… peso o FOB distintos …» | «… peso o CIF distintos …» |

Comentarios y documentación de Swagger: `PolicySummaryCalculator.cs:6` y `:9-13` (D2), `PolicyReportsController.cs:13`, `:21` y `:34`, `PolicyReportDtos.cs:3`, `ImportReleaseDto.cs:14` y `ForeignTradeController.cs:1279` pasan a decir CIF.

### 2.2 Textos del valor del depósito (D3, D4)

| Archivo | Hoy | Queda |
| --- | --- | --- |
| `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:439` | «Porcentaje del valor declarado (sin prorrateo)» | «Porcentaje del valor de la mercancía (lote completo)» |
| `SeedDataExtensions.cs:444` y `:457` | «Umbral CIF por encima del cual no se aplica el mínimo ($)» | «Umbral del valor de la mercancía por encima del cual no se aplica el mínimo ($)» |
| `B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:34` | «el depósito no tiene valor de la mercancía (CIF)» | «el depósito no tiene valor de la mercancía» (sigue siendo una sola constante, que se usa como clave en `:299-300`) |
| `B/Wms.Application/Billing/Common/Services/StorageFallbackWarning.cs:34-35` | «… no tiene valor de la mercancía (CIF); …» | «… no tiene valor de la mercancía; …» |
| `B/Wms.Application/ForeignTrade/Commands/UpdateDraftDeposit/UpdateDraftDepositCommandValidator.cs:24` | «El valor comercial no puede ser negativo.» | «El valor de la mercancía no puede ser negativo.» |
| `B/Wms.Application/Warehouse/Commands/Reception/CreateReceptionWithoutWeighbridgeCommandValidator.cs:78` | «El valor de la carga debe ser mayor a cero.» | «El valor de la mercancía debe ser mayor que cero.» |
| `B/Wms.Application/Billing/Calculators/PercentageOfValueFormulaCalculator.cs:23` y `PercentageOfValueProratedFormulaCalculator.cs:29` | «El campo 'CargoValueCop' es obligatorio para la fórmula …» | «Falta el valor de la mercancía en pesos para calcular la fórmula de porcentaje.» |

- Los comentarios y la documentación de Swagger que dicen «valor comercial» o «CIF» por el valor del depósito pasan a «valor de la mercancía (FOB del ingreso)». Son los listados en el inventario: `ForeignTradeController.cs:431`, `UpdateDraftDepositCommand.cs:8`, `InitiateStorageWeighingRequest.cs:38`, `InitiateStorageWeighingCommand.cs:44`, los `*DepositDetailDto.cs` y los comentarios de `StorageBillingService`, las calculadoras, `FormulaPricing`, `WarehouseStorage:122`, `LegacyDepositRowParser` y `DepositsImporter`. Son cosméticos: si alguno no está en esa línea, se busca con grep y se sigue.
- **Migración:** después de cambiar el seed, `dotnet ef migrations add RenameValueFormulaLabels --project Wms.Infrastructure --startup-project Wms.Api`. Debe contener solo `UpdateData` de `formula_types` (`name` y `parameter_schema` de los dos ids). Si genera otra cosa, detente. Se aplica a la base local y luego `has-pending-model-changes` debe salir limpio.

### 2.3 Valor único del levante (D6)

- **Nuevo** `B/Wms.Application/ForeignTrade/Common/Services/ReleaseValueRules.cs`, una clase pura junto a `ReleaseDuplicateRules`:
  - `Check(string releaseNumber, string acceptanceNumber, decimal? fobUsd, Guid? editingId, IEnumerable<ReleaseValueCandidate> sameDeposit)`;
  - lanza `ConflictException` con el mensaje de D6 cuando `fobUsd > 0` y existe otro candidato con la misma clave (recorte y mayúsculas) y valor mayor que 0;
  - `ReleaseValueCandidate` = `(Guid Id, string ReleaseNumber, string AcceptanceNumber, decimal? FobUsd, string ProductName)`.
- **`RegisterImportReleaseCommandHandler` y `UpdateImportReleaseCommandHandler`:** cargan los levantes del depósito (ya los tienen para `ReleaseDuplicateLookup`; reusar esa consulta si trae lo necesario) y llaman `ReleaseValueRules.Check` antes de aplicar el valor.
  - En la edición, solo cuando el PATCH trae un `fobUsd` mayor que 0: si `fobUsd` no viene, se conserva el valor (CHG-59) y no se valida.
  - Un producto que ya tiene valor y lo cambia no choca consigo mismo.

### 2.4 El valor pasa al retirar (D7)

- **`B/Wms.Domain/Entities/ForeignTrade/ImportRelease.cs`:** nuevo `TakeValueFrom(ImportRelease source)`. Copia los cinco campos de D7 sin recalcular. Lanza una excepción si el destino ya tiene valor, porque D6 lo impide.
- **`B/Wms.Application/ForeignTrade/Commands/WithdrawImportRelease/WithdrawImportReleaseCommandHandler.cs`:**
  - antes de `Remove` (`:83`), si `release.FobUsd > 0`, busca en `remainingReleases` los del mismo número y aceptación (recorte y mayúsculas), ordenados por `CreatedAt` y `Id`;
  - si hay alguno, llama `heir.TakeValueFrom(release)`;
  - la descripción de auditoría agrega « El CIF pasó al producto «{nombre}».».
  - Todo ocurre en la misma transacción.

### 2.5 Pruebas de la fase 1

| Proyecto | Prueba | Escenario |
| --- | --- | --- |
| `Wms.Tests` | **Nuevo** `ForeignTrade/ReleaseValueRulesTests.cs` | Otro producto con valor → 409 con el mensaje de D6. Sin valor (null o 0) → pasa. Clave en minúsculas o con espacios → choca. Otro número → pasa. El registro que se edita no choca consigo mismo |
| `Wms.Tests` | **Nuevo** `Domain/ForeignTrade/ImportReleaseTakeValueTests.cs` | Copia los cinco campos tal cual, incluido un `FobCop` que no es `FobUsd × tasa`. Destino con valor → excepción |
| `Wms.Tests` | Ajustar `ImportReleaseFobTests.cs:44` y `ImportReleaseValidatorTests.cs:31` y `:39` | Mensajes «CIF» |
| `Wms.Tests` | Ajustar `StorageMissingCargoValueWarningTests.cs:17` | Sin «(CIF)» |
| `Wms.IntegrationTests` | Ajustar `MigratedStorageBillingTests.cs:111` | Sin «(CIF)» |
| `Wms.IntegrationTests` | **Nuevo** `ForeignTrade/ReleaseValueOnceTests.cs` | `POST` del segundo producto del mismo levante con valor → 409; sin valor → 201. `PATCH` que pone valor al segundo → 409. Retiro del primero → el segundo queda con los cinco campos y la póliza suma lo mismo que antes. Retiro sin otros productos → el valor desaparece |
| `Wms.IntegrationTests` | **Nuevo** `Billing/FormulaTypeLabelsTests.cs` | `GET` de los tipos de fórmula: los dos nombres y el umbral de D4. Ninguno contiene «CIF» ni «declarado» |

`KardexAggregationTests.cs:60-72` suma el valor de dos productos de un mismo levante. Se deja así: el agregador sigue sumando y D6 impide el caso nuevo.

**Criterio de salida de la fase 1:**
- `dotnet build Wms.sln`;
- `dotnet test Wms.Tests` y `dotnet test Wms.IntegrationTests` en verde, salvo las 2 fallas conocidas de la línea base;
- la migración generada y aplicada en local;
- `has-pending-model-changes` limpio;
- grep en `B/` (sin `Migrations/`, `bin/` ni `obj/`) de textos que ve el usuario: «FOB», «valor comercial», «valor declarado», «Umbral CIF» y «(CIF)» debe salir vacío.

**Commit sugerido (BE):** `feat(levantes,facturacion): el valor del levante se rotula CIF y se registra una sola vez; «Valor de la mercancía» en el depósito y las fórmulas (DEC-029; migración RenameValueFormulaLabels)`.

---

## 3. Fase 2 — Frontend

### 3.1 Levante y póliza (D1, D2, D6)

| Archivo | Hoy | Queda |
| --- | --- | --- |
| `F/app/features/foreign-trade/components/ReleaseForm.vue:603` | «Valor FOB» | «Valor CIF» |
| `ReleaseForm.vue:607` | «FOB del levante (USD)» | «CIF del levante (USD)» |
| `ReleaseForm.vue:622` | «Valor FOB en dólares; …» | «Valor CIF en dólares; …» |
| `ReleaseForm.vue:304` | «El FOB no puede ser negativo.» | «El CIF no puede ser negativo.» |
| `ReleaseForm.vue:319` | «… No cambia al editar el FOB.» | «… No cambia al editar el CIF.» |
| `ReleaseForm.vue:765` | `<strong>FOB:</strong>` | `<strong>CIF:</strong>` |
| `F/app/pages/foreign-trade/imports/[id]/index.vue:694`, `:701` | «FOB (USD)» · «FOB (COP)» | «CIF (USD)» · «CIF (COP)» |
| `F/app/pages/foreign-trade/releases/index.vue:90`, `:92`, `:223`, `:229` | «FOB (USD)» · «FOB (COP)» | «CIF (USD)» · «CIF (COP)» |
| `F/app/pages/reports/warehouse-movements.vue:209`, `:535` | «FOB (USD)» | «CIF (USD)» |
| `F/app/pages/reports/policies.vue:100`, `:101`, `:195`, `:198` | «FOB UAP (USD)» · «FOB no UAP (USD)» | «CIF UAP (USD)» · «CIF no UAP (USD)» |
| `policies.vue:137`, `:300` y `:309` | «FOB (USD)» · «Total FOB: …» | «CIF (USD)» · «Total CIF: …» |
| `policies.vue:149` | «Valor FOB de los levantes (USD), por mes, para UAP y no UAP.» | «Valor CIF de los levantes (USD), por mes, para UAP y no UAP.» |

- Los comentarios de `policies.vue:4-5` (D2), `reports-service.ts:212`, `AppMenu.vue:436`, `StakeholderForm.vue:199`, `stakeholder.ts:27` y `useUpdateImportRelease.ts:7` pasan a decir CIF.
- **D6 en `ReleaseForm.vue`:**
  - `existingFobRelease` (`:322-331`) se queda como está, pero ahora deshabilita el input del valor y lo deja vacío;
  - en lugar del aviso naranja (`:624-628`), muestra «El CIF de este levante ya se registró con «{producto}» ({USD}). Este producto se registra sin valor.»;
  - el formulario se puede enviar sin valor;
  - el 409 del backend se muestra bajo el campo, como los 409 de número y aceptación.

### 3.2 Valor del depósito y fórmulas (D3, D5)

| Archivo | Hoy | Queda |
| --- | --- | --- |
| `F/app/features/foreign-trade/components/DepositDetailGeneralInfoCard.vue:205`, `:273` | «Valor Comercial» | «Valor de la mercancía» |
| `DepositDetailGeneralInfoCard.vue:277` | placeholder «Valor de la carga» | «Valor de la mercancía» |
| `F/app/features/agreements/components/FormulaPreviewPanel.vue:98` | «Valor de la mercancía (CIF)» | «Valor de la mercancía» |
| `F/app/features/agreements/components/AgreementServiceFormDialog.vue:232` y `F/app/features/services/components/ServicePricingRuleFormDialog.vue:200` | «El porcentaje del valor declarado calcula …» | «El porcentaje del valor de la mercancía calcula …» |
| `F/app/features/warehouse/components/ReceptionStepManualInfo.vue:450` | «Valor de la Carga (Opcional)» | «Valor de la mercancía (opcional)» |
| `F/app/pages/billing/pending-deposits/index.vue:244` y `F/app/pages/billing/invoices/[id].vue:415` | «Valor mercancía» | «Valor de la mercancía» |

- Los comentarios con «valor comercial», «valor declarado» o «CIF» por el valor del depósito pasan a «valor de la mercancía»: `AgreementServiceFormDialog.vue:366`, `ServicePricingRuleFormDialog.vue:340`, `DepositDetailGeneralInfoCard.vue:73`, `weighbridge/types/requests.ts:120`, `import-deposit.ts:230,232`, `export-deposit.ts:48,50`, `inspection-deposit.ts:49,51` y `billing/types/invoice.ts:90`.
- **D5:**
  - en `ServicePricingRuleFormDialog.vue` (estado inicial `:318-319`, reinicio `:355-357`) y en `AgreementServiceFormDialog.vue` (`:347-349`, `:424-425`), en modo creación;
  - si el servicio es ALMACENAMIENTO y `formulaTypeId` está vacío, se preselecciona el id de la fórmula con código `PERCENTAGE_OF_VALUE_PRORATED` de la lista cargada;
  - en el acuerdo, la preselección ocurre al elegir el servicio;
  - en edición no se toca.
  - El código se toma del catálogo, no de un id fijo.

### 3.3 Scripts de video (D8)

En `F/tools/video-tutoriales/` se reemplazan los textos que buscan los scripts por los nuevos:
- `videos/7.7.mjs:40`;
- `videos/7.15.mjs:7` y `:44`;
- `videos/1.7.mjs:21`, `:34` y `:38`;
- `videos/2.2.mjs:41`;
- `videos/2.4.mjs:21`, `:22`, `:28` y `:40`;
- `videos/2.7.mjs:22`;
- `videos/2.9.mjs:31`;
- `videos/_acuerdos.mjs:33`;
- `videos/7.2.mjs:31` («Valor Comercial» → «Valor de la mercancía»);
- los comentarios de `siembra/datos.mjs:626-633`.

`pronunciacion.json` no cambia, porque «CIF» sigue existiendo.

### 3.4 Pruebas de la fase 2

| Prueba | Escenario |
| --- | --- |
| Ajustar `F/test/components/foreign-trade/DepositDetailGeneralInfoCard.spec.ts:93` | «Valor de la mercancía» |
| **Nuevo** `F/test/components/foreign-trade/ReleaseForm.spec.ts` | Con otro producto del mismo levante con valor: el campo queda deshabilitado, muestra el producto y el formulario es válido sin valor. Sin ese caso, el campo está habilitado y se rotula «CIF del levante (USD)» |
| **Nuevo** `F/test/components/services/ServicePricingRuleFormDialog.spec.ts` (o junto al spec existente del diálogo de acuerdos) | Al crear con ALMACENAMIENTO se preselecciona la prorrateada. Con otro servicio, no. En edición no cambia |

**Criterio de salida de la fase 2:**
- `yarn build`;
- `yarn test`;
- `yarn lint` sin pasar de la línea base;
- grep en `F/app` de textos que ve el usuario: «FOB», «Valor Comercial», «valor declarado», «Valor de la Carga» y «(CIF)» debe salir vacío.

**Commit sugerido (FE):** `feat(levantes,facturacion): rótulos CIF del levante y la póliza, valor único del levante, «Valor de la mercancía» y fórmula prorrateada preseleccionada en almacenamiento (DEC-029)`.

---

## 4. Fase 3 — Documentación y verificación local

- **Guiones:** en `D/videos/guiones/guiones-video-tutoriales.md` (`:1112`, `:1242`, `:1249` y los pasos y narraciones de las series 1, 2 y 7 que digan «FOB del levante», «Valor Comercial», «valor declarado», «Umbral CIF» o «el CIF» por el depósito), el texto pasa a la terminología de `DEC-029`. Se agrega una fila en `D/videos/guiones/inventario-cambios-guiones.md`.
- **Nuevo** `D/videos/videos-desactualizados-dec-029.md`: la lista de videos y subtítulos publicados que quedan desactualizados, con archivo y línea. Incluye `video-tutoriales-trabajo/salida/publicacion/subtitulos/serie-1/1-07-tarifas-base.vtt:13`, `serie-2/2-04-formulas-de-porcentaje.vtt`, `serie-7/7-07-levantes.vtt:21`, `serie-7/7-15-reportes-de-comercio-exterior.vtt:29` y los demás que salgan del grep. Lleva la nota «regrabar en una tarea aparte (D8)». No se editan los `.vtt` ni los `.srt` publicados.
- **Contexto:**
  - en `D/contexto/contexto-negocio-wms-para-ia.md`, «Levante» (`:53`, `:212`) pasa a «CIF en USD, tasa y CIF en COP», y la fila «Valor de la mercancía» quita «aún lo llaman CIF»;
  - las filas de fórmulas (`:342-343`, `:356`, `:363`) dicen «valor de la mercancía» donde dicen «CIF» del depósito;
  - el pendiente 8 de `D/contexto/estado.md` deja solo lo que queda para Facturación.
- **Verificación local** sobre la base de desarrollo migrada con `dotnet ef` (o `wms_qa_preprod`, si la de desarrollo sigue en un esquema viejo), con el API y el frontend locales:
  1. registrar un levante con dos productos: el segundo sale con el campo deshabilitado y se guarda sin valor;
  2. forzar por API el valor en el segundo → 409 con el mensaje de D6;
  3. retirar el primero → el segundo muestra el CIF con la misma tasa;
  4. la póliza y el kárdex (pantalla, Excel y PDF) dicen CIF y suman igual que antes del retiro;
  5. detalle del depósito y recepción manual: «Valor de la mercancía»;
  6. crear una regla de tarifa de almacenamiento: la prorrateada sale preseleccionada y los nombres de D4 aparecen en el select;
  7. **conteo de solo lectura:** cuántos levantes de la base local tienen valor en más de un producto. El resultado se anota en el registro, sin corregirlo (D9).
- **Registro:** este plan (estado y §6 de ejecución), `D/planes/README.md`, `DEC-029` (una línea con los commits) y `D/contexto/estado.md`.

**Commit sugerido (docs):** `docs(planes,videos,contexto): DEC-029 construido; guiones e inventario de videos desactualizados`.

---

## 5. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Hay datos con un valor repetido en dos productos de un levante, registrados en staging antes del bloqueo | D6 aplica solo a lo nuevo. Se cuentan en local (§4, paso 7). En staging, el conteo es de solo lectura y con aprobación, en el siguiente despliegue. No se corrigen con SQL (`DEC-006`) |
| Retirar el producto con valor y luego editar el heredero confunde a CE | La auditoría lo registra. El detalle del depósito muestra el CIF en el producto heredero |
| La migración `RenameValueFormulaLabels` se suma a las de la fase 13 del plan P1 | Es solo de datos y va con el script idempotente. Si la fase 13 ya se desplegó, va en el siguiente despliegue, con aprobación del usuario |
| Los videos publicados quedan con los textos viejos | Inventario de D8; se regraba en una tarea aparte |
| El frontend deja de detectar la caída de la DIAN | D1 conserva el prefijo del mensaje. La verificación del §4 incluye la TRM manual |
| Un acuerdo de almacenamiento se crea sin notar la preselección | Es una preselección visible y editable, y la vista previa de la fórmula muestra el cálculo |

---

## 6. Estado de las fases

| Fase | Estado | Commits | Notas |
| --- | --- | --- | --- |
| 1 · Backend | Hecha 2026-10-25, sin commit | — (base `3cbf181`) | Migración `20261025235406_RenameValueFormulaLabels` (solo los dos `UpdateData` de `formula_types`), aplicada en local a `wms_qa_preprod`: `wmsdb` sigue en un esquema anterior a `RemoveSampleSeedData` y no se migró (`procesos/verificacion-local.md` §1). `has-pending-model-changes` limpio. Compuertas: `dotnet build` 0 errores; `Wms.Tests` 2029/2029; `Wms.IntegrationTests` 438/440, con solo las 2 fallas de la línea base, que pasan solas; grep del §2.5 sin textos visibles (quedan comentarios con «valor de la mercancía (FOB del ingreso)», como pide el §2.2). Desviaciones: (1) nuevo `ReleaseValueLookup.cs`, la consulta de D6 compartida por alta y edición (como `ReleaseDuplicateLookup`, que no trae valor ni producto); (2) la elección del heredero de D7 es la función pura `ReleaseValueRules.FindHeir`, probada en `Wms.Tests`; (3) caso borde, gana D6: si otro producto del levante ya tiene valor (datos anteriores al bloqueo), el retiro no traspasa nada, para no repetir el CIF ni bloquear el retiro; (4) se ajustó además `PercentageOfValueFormulaCalculatorTests` (mensaje nuevo del §2.2) y los comentarios de pruebas que llamaban FOB al levante; (5) el alta del levante responde 200, no 201: la prueba comprueba éxito |
| 2 · Frontend | Hecha 2026-10-25, sin commit | BE `dafd573` (fase 1) · FE base `83a0af0` | Compuertas: `yarn build` código 0; `yarn test` 100 archivos, 504/504; `yarn lint` 281 errores y 413 avisos, igual a la línea base y sin hallazgos en los specs nuevos; grep del §3.4 en `F/app` vacío (solo quedan identificadores `fobUsd`, `fobCop`, `release-fob-usd`, `preview-cif`). Pruebas nuevas: `ReleaseForm.spec.ts` (7) y `services/ServicePricingRuleFormDialog.spec.ts` (7, incluye el diálogo de acuerdos). Desviaciones: (1) caso borde, gana D6: `existingFobRelease` compara también la aceptación, como el backend (`ReleaseValueRules`); con solo el número habría deshabilitado el campo en un levante que el API sí acepta; (2) el 409 de D6 se reconoce por su prefijo «El CIF del levante» y va bajo el campo del valor; (3) además de los comentarios listados, pasan a CIF los de `reports/types/policies.ts:3`, `import-deposit.ts:122-123` y `:292`, y el del 409 en `useUpdateImportRelease.ts`; (4) D8: también se ajustan `videos/3.3.mjs:21` y `videos/3.5.mjs:26`, que buscaban «Valor mercancía», cambiado por el §3.2; (5) `components.d.ts` lo regenera `yarn test` al montar los diálogos nuevos (`Calendar`, `InputSwitch`, `Panel`) |
| 3 · Docs y verificación | Hecha 2026-10-25, sin commit | BE `dafd573` · FE `d838535` (docs base `ea92d34`) | **Docs:** guiones con la terminología de `DEC-029` (1.7, 2.2, 2.4, 2.5, 2.7, 2.9, 3.3, 3.5, 7.2, 7.7 y 7.15) y §8 nuevo en `inventario-cambios-guiones.md`; nuevo `videos/videos-desactualizados-dec-029.md` (7 líneas de `.vtt` en 4 subtítulos y 12 videos con rótulos viejos en pantalla; `.vtt`/`.srt` sin tocar); `contexto-negocio-wms-para-ia.md` (levante CIF, fórmulas y magnitudes con «valor de la mercancía») y pendiente 8 de `estado.md` solo con lo de Facturación. **Verificación local** sobre `wms_qa_preprod` (ya migrada en la fase 1; `wmsdb` sigue en esquema viejo), API y frontend locales, depósito `2024BA00015`: (1) levante `LEV-DEC029-01` con CIF 5.000 USD en «LOMITOS…»; el segundo producto («CONSERVAS…») sale con el campo «CIF del levante (USD)» deshabilitado y el aviso de D6, y se guarda sin valor — PASA; (2) `PATCH` del segundo con `fobUsd` 1.000 → 409 «El CIF del levante LEV-DEC029-01 ya se registró con «LOMITOS DE ATUN EN AGUA». Registre este producto sin valor.»; también con la clave en minúsculas y espacios — PASA; (3) retiro de «LOMITOS…»: «CONSERVAS…» queda con los cinco campos iguales (5.000 · 3.158,43 · Dian · 2026-10-25 · 15.792.150) y la auditoría dice «El CIF pasó al producto «CONSERVAS…»» — PASA; (4) póliza 2024-03 no UAP: 451.008,79 (línea base) → 456.008,79 tras el alta → 456.008,79 tras el retiro; pantalla («Valor CIF de los levantes (USD)…», «CIF UAP/no UAP (USD)», detalle «CIF (USD)») y Excel de resumen y detalle con «CIF»; kárdex en pantalla y Excel «CIF (USD)» y PDF «CIF USD», 5.000 antes y después — PASA; (5) detalle del depósito y su edición «Valor de la mercancía»; recepción directa «Valor de la mercancía (opcional)», sin textos viejos — PASA; (6) «Crear tarifa base» de ALMACENAMIENTO: preselecciona «Porcentaje del valor de la mercancía (prorrateado por saldo)», el select trae los dos nombres de D4, el umbral y la nota usan «valor de la mercancía» y se puede cambiar a lote completo — PASA; (7) conteo de solo lectura de levantes (depósito + número + aceptación, recorte y mayúsculas) con valor en más de un producto: **0** de 129 en `wms_qa_preprod` (y 0 de 107 en `wms_migracion`, 0 de 14 en `wmsdb`); ningún levante tiene más de un producto en esas bases; nada que corregir (D9). Además (§5, riesgo de la DIAN): con la DIAN inalcanzable el formulario pide «Tasa de cambio (COP por USD) *» y muestra «No se pudo consultar la TRM de la DIAN. Digite la tasa de cambio para registrar el CIF.»; se canceló sin guardar. **Desviaciones:** (1) también se ajustaron los guiones 3.3 y 3.5 y las filas S4 y A1 de `dataset-grabacion.md`, que citaban rótulos cambiados por las fases 1 y 2 (D8); (2) la fila del inventario de guiones va en un §8 nuevo, porque ninguna tabla existente encajaba; (3) en el paso 6 la tarifa no se guardó, para no dejar una regla activa más en la facturación local (D5 y D9 no la piden); (4) datos que quedan en `wms_qa_preprod`: el levante `LEV-DEC029-01` de `2024BA00015` (CIF en «CONSERVAS…»), el ingreso y la salida de la placa `VDC029` (para abrir la recepción directa sin guardarla) y el usuario `verif.dec029`, creado con `BootstrapAdminSeeder` y desactivado al terminar; las acciones de pantalla se hicieron con la sesión QA `qa.pre.admin` abierta en el navegador. **Observaciones menores (sin corregir, fuera de la fase):** (a) la auditoría del retiro pega « El CIF pasó…» al motivo sin punto («…con el CIF El CIF pasó…») cuando el motivo no termina en punto; (b) el 409 de D6 repite el número tal como llegó en la petición (en minúsculas si así se envió). |
