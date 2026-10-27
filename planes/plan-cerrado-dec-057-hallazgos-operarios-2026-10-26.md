# Plan cerrado — Hallazgos de los operarios (DEC-057)

> **Fecha:** 26 de octubre de 2026. **Estado:** Aprobado por el usuario el 2026-10-26. Ejecutado el 2026-10-26 (§8): las 6 fases commiteadas; la corrección posterior de la tarjeta de pesos de CE, sin commit. Prompt del ejecutor, por fase: `prompt-plan-dec-057-hallazgos-operarios-2026-10-26.md`.
> **Origen:**
> - `DEC-057` (`contexto/decisiones.md`) y `analisis/hallazgos-operarios-2026-10-26.md`;
> - las respuestas del usuario a las preguntas de este plan (2026-10-26), registradas en D3, D11, D18 y D19.
>
> **Base:** BE `develop` `dafd573` · FE `develop` `d838535` · docs `main` `a68c511`.
> **Alcance:**
> - 6 fases: 3 de backend, 2 de frontend, y docs con QA local;
> - una migración, `AddLabelPrintEntry`;
> - sin cambios de permisos de roles; se agrega un endpoint con política existente.
>
> **Orden:** se ejecuta antes de la fase 13 del plan de brechas P1, que despliega todo junto (`DEC-057`).
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`.

---

## 0. Instrucciones para el ejecutor

1. Lee `B/AGENTS.md`, `D/contexto/convenciones-tecnicas.md`, `DEC-057`, `D/analisis/hallazgos-operarios-2026-10-26.md` y este plan completo.
2. Trabaja en `develop` (BE y FE) y `main` (docs), sin ramas ni commits (`DEC-003`). Al cerrar cada fase te detienes con el resumen y el mensaje de commit.
3. Las líneas citadas son de la base. Confírmalas con grep antes de cambiar. Si el código no coincide (ruta, firma o comportamiento), detente y pregunta, con todas las dudas en un solo mensaje. Si el texto choca con una Dn en un caso borde, gana la Dn (`DEC-002`).
4. Migraciones solo con `dotnet ef`, solo la del plan y solo contra la base local. `has-pending-model-changes` limpio al cerrar cada fase de backend.
5. Las pruebas de integración que hoy registran ingresos sin manifiesto, asocian camiones por número repetido o confirman importaciones sin manifiesto DIAN se ajustan en la misma fase que cambia la regla. Hay que tocar sus *helpers* (`OperationalData`, `WeighbridgeScenario`, `BillingScenario.ConfirmDepositAsync` y los `ConfirmDepositAsync` locales) y no cada prueba suelta, salvo las que prueban justo esa regla.

---

## 1. Decisiones

### 1.1 Carta porte (H7)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Nada se asocia solo.** El comando de ingreso a depósito (`InitiateStorageWeighingCommand` y `RegisterStorageEntryCommand`, con sus requests) recibe `TargetWarehouseStorageId` (`Guid?`).<br>• **Nulo:** siempre se crea un depósito nuevo.<br>• **Con valor:** el camión se asocia a ese depósito, después de validar que siga abierto (servicio de entrada no descartado, ingreso de camiones sin cerrar, estado Borrador o Confirmado) y que tenga el mismo número normalizado y el mismo tipo de documento. Si no, 409 «El depósito {N} ya no está abierto para el documento {número}. Vuelva a buscar el documento.»<br>• `StorageDocumentMatcher.Select` y el 409 de ambigüedad dejan de usarse en el ingreso.<br>• Se conservan, al asociar: el 409 de modalidad distinta y el 409 de camión ya activo en el depósito (`InitiateStorageWeighingHandler.cs:320-350`) | `DEC-057` H7; reemplaza la decisión P1 de `D/planes/paridad-legacy/plan-backend-paridad-legacy.md` |
| D2 | **Fecha del documento al asociar.** Manda la del depósito elegido.<br>• Si el depósito no tiene fecha y la petición trae una, se escribe, como hoy (`:338-339`).<br>• Si el depósito ya tiene fecha, la de la petición se ignora; el formulario la muestra en solo lectura | `DEC-057` H7 |
| D3 | **Depósitos cerrados.**<br>• Los que tienen el mismo número y tipo (ingreso de camiones cerrado, agotados o migrados) se muestran como información, con «Cerrado por {nombre} el {fecha}» o «Migrado», y no se pueden elegir.<br>• El bloqueo de `EnsureTruckEntriesNotClosedAsync` (`StorageDocumentLookup.cs:99-117`) deja de aplicarse al crear un depósito nuevo: el operario puede crearlo | Respuesta del usuario: «Los muestra y deja crear» |
| D4 | **Nueva consulta de candidatos.** `GET weighbridge/storage/document-candidates?number=&primaryDocumentTypeId=`, con la misma política que `service-records/by-document` (`WeighbridgeController.cs:760-771`). Devuelve la lista de `StorageDocumentCandidateDto`, ordenada con los abiertos primero y por creación:<br>• datos del depósito: `WarehouseStorageId`, número, estado, `IsOpen`, `ClosedAt`, `ClosedByName`, `IsMigrated`, modalidad (código y nombre) y `DocumentDate`;<br>• terceros: `CustomerName`, `ImporterName` o `ExporterName` y `CustomsAgencyName`;<br>• `CarrierNames`, sin repetir: las transportadoras de los vehículos de los camiones no anulados, y el tercero `TRANSPORT_COMPANY` si no hay;<br>• `Plates`: las de los camiones no anulados;<br>• `TruckCount`;<br>• `ServiceRecord` y `WarehouseStorage`, solo en los abiertos y con los mismos DTO de hoy (`ServiceRecordDetailDto` y `WarehouseStorageDto`), para que el formulario precargue como hoy. El mapeo se extrae de `GetServiceRecordByDocumentHandler` y `GetWarehouseStorageByDocumentHandler` a una sola clase.<br>La búsqueda usa la clave de `StorageDocumentLookup` (`:24-35`), sin filtro de fecha | `DEC-057` H7 |
| D5 | **Depósito adicional.** El backend rechaza un depósito adicional cuyo número y tipo ya tengan un depósito **abierto**: 409 «El documento {número} ya tiene un depósito abierto ({N}). Un depósito adicional necesita un documento propio.» Hoy solo lo valida el frontend (`F/pages/operations/weighbridge/index.vue:972-985`) | Guarda contra el mismo riesgo de H7 |
| D6 | **Endpoints existentes.** `service-records/by-document` y `warehouse-storage/by-document` se conservan sin cambios para otros usos, pero el formulario de ingreso deja de usarlos.<br>**Sin cambios:** el 409 de fecha repetida de `UpdateDraftDepositHandler.cs:69-86`, `GET weighbridge/lookup` (BR-02-018) y la recepción de Bodega sin báscula | Alcance |

### 1.2 Manifiestos (H2 y manifiesto DIAN)

| # | Decisión | Fuente |
| --- | --- | --- |
| D7 | **Manifiesto obligatorio en Báscula.** En `InitiateStorageWeighingValidator` (`:98-107`) y `RegisterStorageEntryValidator` (`:55-59`):<br>• `ManifestNumber` es obligatorio: «El número de manifiesto del camión es obligatorio.», con el tope de 100 que ya tiene;<br>• `ManifestWeight` es obligatorio y mayor que 0: «El peso del manifiesto del camión es obligatorio.»<br>Aplica a importación, exportación e inspección, también al depósito adicional (mismo comando). Solo báscula, Salida y la recepción de Bodega sin báscula no cambian. El aviso de camión tardío sin manifiesto (`InitiateStorageWeighingHandler.cs:740-748`) se conserva, porque CE sigue pudiendo editar | `DEC-057` H2; reemplaza P2 / BAS-01 |
| D8 | **Manifiesto DIAN al confirmar la importación.**<br>• `DepositConfirmationRequirements` agrega el código `DIAN_MANIFEST`, con el mensaje «número del manifiesto DIAN», solo para importación, cuando `ImportWarehouseStorage.ManifestNumber` está vacío.<br>• El snapshot agrega `DianManifestNumber`, que `DepositConfirmationSnapshotReader` lee de `ImportWarehouseStorage`.<br>• Solo se exige el número; la fecha no.<br>• Un depósito migrado que vuelve a Borrador también lo necesita al reconfirmar | `DEC-057`; legacy `registraringreso.php:288-296` |

### 1.3 Pesos del legacy (H3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D9 | **Se calcula al leer, sin migración.** Nueva clase pura `B/Wms.Application/Weighbridge/Common/Services/ManifestDeducedWeights.cs`.<br>Entradas:<br>• el primer pesaje del ciclo (tipo y peso);<br>• la suma de `ManifestWeight` de los camiones del grupo (un camión o el pesaje compartido de varios depósitos);<br>• el `ManifestWeight` de cada camión;<br>• si el ciclo se completó con un solo pesaje;<br>• el `PhysicalNetWeight` real.<br>Salidas: `Indicator`, `ManifestWeight`, `DeducedTare`, `DeducedCargo`, `EffectiveNet` y `NetSource` (`Weighings`, `Manifest` o `None`). `PhysicalNetWeight` no se toca: sigue siendo solo el neto real por diferencia de pesajes | `DEC-057` H3 |
| D10 | **Reglas, como el legacy** (`registrarentradabascula.php:643-649`; varios documentos, `registrarentradavariascp.php:713-721`):<br>• hay deducción solo si el primer pesaje es **Bruto** y hay peso de manifiesto;<br>• `DeducedCargo` = peso del manifiesto del camión;<br>• `DeducedTare` = indicador − suma de los manifiestos del grupo;<br>• si la suma del manifiesto supera al indicador, no hay tara deducida y se muestra «El manifiesto supera el peso del indicador»;<br>• con primer pesaje Tara, no hay deducción | `DEC-057` H3 |
| D11 | **Neto efectivo:**<br>• con segundo pesaje, `EffectiveNet` = el neto real (`NetSource = Weighings`);<br>• con el ciclo completo de un solo pesaje (perecederos, inspección o «Requiere segundo pesaje» apagado), `EffectiveNet` = `DeducedCargo` (`NetSource = Manifest`): vale como el peso de la mercancía del ingreso, como en el legacy;<br>• sin manifiesto, `None` | Respuesta del usuario: «igual que el legacy» |
| D12 | **Dónde se usa el neto efectivo** (con `NetSource = Manifest` se rotula «según manifiesto» y no se hacen las comparaciones contra el manifiesto, que serían consigo mismo):<br>• tiquete de báscula: agrega «T. VEHÍCULO» y «P. MANIFIESTO», e imprime «PESO MERCANCÍA» con el neto efectivo y «(según manifiesto)» cuando corresponde (`WeighbridgeTicketPdfService.cs:341-413`);<br>• detalle del ciclo: DTO y página, sin la comparación ±2 % cuando la fuente es Manifest (`cycles/[id].vue:528-562`);<br>• detalle del depósito en CE: `PhysicalWeightStatus` agrega el valor `CalculatedFromManifest` cuando algún camión tiene neto Manifest y ninguno queda en `None`; las tarjetas muestran «Calculado según manifiesto»;<br>• validación del depósito: la diferencia del 5 % no se evalúa en los camiones con fuente Manifest (`DepositValidationMath.cs:23-44`);<br>• diario de ingresos: `NetWeightKg` (`DailyIncomingGoodsReportBuilder.cs:134-135`);<br>• historial de báscula y sus totales: `WeighingTotals` (CHG-76, `:37-49`) usa el neto efectivo, de modo que un solo pesaje con manifiesto reporta la mercancía deducida como neto y la tara deducida como tara.<br>Los demás consumidores de `PhysicalNetWeight` (tablero, estadísticas, recepción, facturación por umbral) **no cambian** | `DEC-057` H3 |
| D13 | **Pantalla de pesaje:** en el primer pesaje de un ingreso a depósito con tipo Bruto, `WeightCapture.vue` muestra siempre los cuatro campos:<br>• P. indicador: el peso que digita el operario;<br>• P. manifiesto: el del registro, en solo lectura, sumado si el pesaje es compartido;<br>• T. vehículo y P. mercancía: calculados mientras digita.<br>Con segundo pesaje, la pantalla de salida sigue mostrando «Neto (bruto − tara)» (`WeightCapture.vue:327-338`). El detalle del ciclo y el historial muestran los cuatro valores con su fuente | `DEC-057` H3 («siempre en pantalla») |

### 1.4 Tiquete en $0 por convenio (H5b)

| # | Decisión | Fuente |
| --- | --- | --- |
| D14 | **Cuándo sale en $0.** Solo si `BillingResolver` resuelve el servicio de báscula desde un **convenio** (`Source = Agreement`) con monto 0.<br>• `WeighbridgeService.GetWeighingPriceAsync` (`:56-79`) pasa a devolver el monto y si viene de un convenio en cero (`WeighbridgePriceQuote`).<br>• Una tarifa base o un precio general en 0 se siguen rechazando como hoy, y la falta de tarifa sigue siendo «No se encontró tarifa…» (BR-02-003 sigue abierta) | `DEC-057` H5b |
| D15 | **Cómo se cobra.** En los tres flujos de báscula (ingreso a depósito, Solo báscula y Salida) y en sus dos modos (Inmediato y Por facturar), un precio de convenio en cero produce el cobro en $0 con el mismo mecanismo del depósito adicional (`ProcessStoragePaymentHandler.cs:289-379`):<br>• factura `IsZeroValue`, sin número, pagada con un pago de $0 «ZERO-INVOICE»;<br>• el ítem se describe «Servicio de Báscula — Sin cobro por convenio».<br>El modo Por facturar no aplica a un cobro en cero. Las 9 validaciones de precio y total mayor que 0 (tabla del §3.2) aceptan el cero solo en este caso. El operario no puede poner 0 si el precio es mayor que 0. Sin migración: la marca va en la descripción del ítem | `DEC-057` H5b; `DEC-024` |
| D16 | **Tiquete y pantalla.**<br>• El tiquete imprime «SIN COBRO POR CONVENIO» bajo «VALOR TOTAL $» (`WeighbridgeTicketPdfService.cs:446-454`). La leyenda no fiscal no cambia.<br>• En pantalla, `BillingCollectForm.vue` entra en modo `zeroValue` con el texto «Sin cobro por convenio» cuando la vista previa trae total 0 y un `agreementServiceId` | `DEC-057` H5b |

### 1.5 Tarjeta (H10, H12, H13, H14, H15)

| # | Decisión | Fuente |
| --- | --- | --- |
| D17 | **Tarjeta del depósito** (`LabelGenerationService.cs`, en sus tres copias: importación `:91-251`, exportación `:317-450` e inspección `:523-652`):<br>• **H10:** se quita la fila «Transportadora» (`:140-145`, `:366-371`, `:574-579`). Se borran `FormatCarrierCompanies` (`:773-783`), `CarrierCompanyText` y su prueba si quedan sin uso.<br>• **H13:** la línea del documento pasa a ser «{tipo}: {número} ({fecha})», con el tipo tomado de `PrimaryDocumentType.Name` («Documento» si es nulo) y la fecha de `ColombiaTime.DateOf(sr.DocumentDate)` en `yyyy-MM-dd`, o «N/A» si no hay. Las consultas incluyen `PrimaryDocumentType` (patrón de `GetWarehouseStorageMovementsHandler.cs:41`). El bloque «Documentos:» de exportación e inspección se conserva.<br>• **H15:** la tabla queda Ampara · Saldo · Mercancía. La mercancía es el texto de `DocumentProductLine` más « ({embalaje})» si hay embalaje, como el legacy. Sigue habiendo una fila por producto, y la consolidación del Ampara por unidad (CHG-69, `LabelAmpara`) no cambia | `DEC-057` H10, H13, H15 |
| D18 | **H14:** `DocumentProductLine.For` (`:9-23`) no repite la descripción cuando, comparada con `CatalogNameNormalizer.ForComparison`, es igual al nombre o el nombre ya la contiene. Vale para todos sus usos. El PDF del depósito y la guía ya pasan un solo texto y no cambian | `DEC-057` H14 |
| D19 | **Tarjeta por vehículo** (H12), como el legacy (`adhesivovehiculo.php`), en importación, exportación e inspección:<br>• encabezado igual al de la tarjeta del depósito: logo, número con código de barras, importador o exportador, intermediario y fecha de ingreso del depósito;<br>• «Placa: {placa del camión}» y sus unidades de carga;<br>• la línea del documento de D17;<br>• «Manifiesto No. {manifiesto del camión}»;<br>• la tabla «Cant. ingresa · Mercancía», una fila por producto de ese camión (`WarehouseStorageEntryProduct.DeclaredQuantity` con `QuantityDisplay.Quantity`), con el texto de D17;<br>• la franja de estado de la tarjeta del depósito.<br>Sin Ampara ni Saldo.<br>• Endpoints: `GET foreign-trade/imports/{id}/entries/{entryId}/label?action=` y sus equivalentes en exports e inspections, con la política de las tarjetas actuales.<br>• Un camión anulado (`VoidedAt`) o de otro depósito → 400 o 404.<br>• Los depósitos migrados no tienen camiones y no ofrecen esta tarjeta | Respuesta del usuario: «Como el legacy» |
| D20 | **Registro de impresiones:** `WarehouseStorageLabelPrint` agrega `WarehouseStorageEntryId` (`Guid?`, FK opcional), con la migración **`AddLabelPrintEntry`**. `RecordPrintAsync` lo recibe en la tarjeta por vehículo. `GET warehouse-storages/{id}/label-prints` devuelve la placa cuando lo hay | Respuesta del usuario: «Sí, con su camión» |

### 1.6 Destinatario de la factura (BR-06-007)

| # | Decisión | Fuente |
| --- | --- | --- |
| D21 | **Candidatos:** `GET billing/invoices/{id}/recipient-candidates`, con la política `BillingAccess`, devuelve los terceros de los depósitos de la factura: cliente, importador o exportador, agencia y transportadoras, con su rol. Los depósitos se ubican por los ítems de la factura (`InvoiceItem.StorageBillingPeriodId` y `DispatchGuideId`) | `DEC-057`; brecha BR-06-007 |
| D22 | **Validación** en `UpdateInvoiceRecipientHandler` (solo en Borrador, como hoy): el tercero elegido debe ser uno de los candidatos o tener el rol Cliente. Si no: 400 «El tercero no está relacionado con la factura ni es cliente.» Se reutiliza `BillingService.ValidateDepositStakeholderAsync` (`:122-151`), que hoy no se llama. El destinatario no registrado sigue igual | `DEC-057` |
| D23 | **Pantalla.** En `F/pages/billing/invoices/[id].vue`, bloque «Destinatario» (`:312-351`), se agrega el botón «Cambiar destinatario», solo con la factura en Borrador, que monta `UpdateRecipientDialog.vue`.<br>• En modo registrado, el diálogo muestra primero los candidatos y además permite buscar cualquier cliente (`CustomerSelect`).<br>• Al guardar se llama `refetchInvoice()` | `DEC-057` |

### 1.7 Fuera de alcance

| # | Decisión | Fuente |
| --- | --- | --- |
| D24 | **Fuera de alcance:**<br>• los hallazgos sin cambio de código (H1, H4, H5a y H6), que van en la nota de capacitación (§7);<br>• crear un cliente rápido desde Báscula o CE;<br>• editar el cobro de un tiquete guardado (`DEC-050`);<br>• BR-02-003 (cobro no tarifado);<br>• filtrar los camiones anulados en las placas de la tarjeta del depósito;<br>• desplegar en staging (fase 13) | `DEC-057` |

---

## 2. Fase 1 — Backend: carta porte y manifiestos (D1–D8)

- **`StorageDocumentLookup`:** nuevo `GetCandidatesAsync(number, typeId)`, que arma los candidatos de D4. Se extrae el mapeo de los dos handlers `by-document` a `StorageDocumentCandidateMapper`.
- **Nueva consulta:** `GetStorageDocumentCandidatesQuery`, con su handler y su endpoint (D4).
- **`InitiateStorageWeighingCommand` y su request, `RegisterStorageEntryCommand` y su request, `WeighbridgeController`** (`:190-298`): agregan `TargetWarehouseStorageId`, que se pasa en orden en `ToInitiateCommand`.
- **`InitiateStorageWeighingHandler`:**
  - reemplaza `MatchOpenAsync` (`:272-279`) por la carga del depósito elegido con las validaciones de D1, o por la creación de uno nuevo;
  - quita `EnsureTruckEntriesNotClosedAsync` del camino de creación (D3);
  - aplica D2 a la fecha;
  - en `HandleAdditionalDepositAsync` (`:908`) agrega la guarda de D5.
- **Validadores:** D7.
- **`DepositConfirmationRequirements`, el snapshot y el reader:** D8.
- **`StorageDocumentMatcher`:**
  - `Select` y `AmbiguousMessage` siguen solo si otros usos los necesitan (los handlers `by-document`);
  - `SelectClosed` y `ClosedMessage` quedan para `by-document`;
  - lo que quede sin uso se borra.

**Pruebas de la fase 1:**

| Proyecto | Prueba | Escenario |
| --- | --- | --- |
| `Wms.Tests` | Ajustar `Weighbridge/StorageDocumentMatcherTests.cs` | Según lo que quede del matcher |
| `Wms.Tests` | Ajustar `InitiateStorageWeighingValidatorTests.cs` (`:60`, `:71`, `:79`, `:133`, `:201`) y `RegisterStorageEntryValidatorTests.cs` (`:89`, `:98`) | Manifiesto obligatorio |
| `Wms.Tests` | Ajustar `DepositConfirmationRequirementsTests.cs` | `DIAN_MANIFEST` en importación; exportación e inspección no lo piden |
| `Wms.IntegrationTests` | **Nuevo** `Weighbridge/DocumentCandidatesTests.cs` | Dos depósitos abiertos con la misma carta porte y clientes distintos: los dos salen con su cliente, transportadora y placas. Un cerrado y un migrado salen con `IsOpen = false` |
| `Wms.IntegrationTests` | **Nuevo** `Weighbridge/ExplicitDepositChoiceTests.cs` | Sin `TargetWarehouseStorageId` y con un depósito abierto del mismo número → se crea otro depósito (el escenario H7 ya no mezcla). Con el target → se asocia. Target cerrado entre la búsqueda y el guardado → 409. Número igual al de un depósito cerrado sin fecha → se crea (D3). Depósito adicional con número de un abierto → 409 (D5) |
| `Wms.IntegrationTests` | Ajustar `ClosedDocumentLookupTests.cs`, `GetImportDepositDetailHandlerTests.cs:117`, `DailyIncomingGoodsTests.cs:124` y los *helpers* | Mandar `targetWarehouseStorageId` en el segundo camión; mandar el manifiesto; poner el manifiesto DIAN antes de confirmar |

**Criterio de salida:** `dotnet build`; `Wms.Tests` y `Wms.IntegrationTests` en verde, salvo las 2 fallas de la línea base; `has-pending-model-changes` limpio.
**Commit sugerido (BE):** `feat(bascula,comercio-exterior): el operario elige el depósito de la carta porte; manifiesto obligatorio en báscula y manifiesto DIAN al confirmar la importación (DEC-057)`.

---

## 3. Fase 2 — Backend: pesos del legacy y tiquete en $0 (D9–D16)

### 3.1 Pesos

- **Nuevo:** `ManifestDeducedWeights` (D9–D11).
- **Consumidores de D12:**
  - el tiquete: `WeighbridgeTicketPdfService`;
  - el detalle del ciclo: `WeighbridgeCycleDetailDto`, `GetWeighbridgeCycleHandler.cs:153` y `GetOpenCycleByPlateHandler.cs:164`;
  - el detalle del depósito en CE, en importación (`:156-165`), exportación (`:91-100`) e inspección (`:108-117`), con el valor nuevo `CalculatedFromManifest` en el enum de `PhysicalWeightStatus`;
  - la validación: `DepositValidationMath` y sus dos handlers;
  - el diario de ingresos: `GetDailyIncomingGoodsReportHandler.cs:97`;
  - el historial y sus totales: `WeighingTotals`, `GetWeighbridgeHistoryHandler`, `GetWeighbridgeHistoryTotalsHandler` y `GetCustomsAgencyEntryDetailHandler`.
- El neto real (`CycleNetWeights`, `SharedNetSplit` y `CycleNetWeightUpdater`) **no cambia**.

### 3.2 Tiquete en $0

`WeighbridgeService.GetWeighingPriceAsync` pasa a devolver `WeighbridgePriceQuote` (D14). Los 9 handlers y los 5 validadores que exigen mayor que 0 aceptan el cero solo cuando `IsAgreementZero`, y generan la factura en cero de D15:

| Handler | Rechazos de hoy |
| --- | --- |
| `InitiateStorageWeighingHandler` | `:697-706` |
| `InitiateWeighingOnlyHandler` | `:152-158` |
| `InitiateOutputWeighingHandler` | `:180-186` |
| `ProcessStoragePaymentHandler` | `:166-183` (además, el número de factura del operario pasa a null en el cobro en cero) |
| `StartStoragePendingBillingHandler` | `:102-114` |
| `ProcessWeighingOnlyPaymentHandler` | `:98-112` |
| `StartWeighingOnlyPendingBillingHandler` | `:79-91` |
| `ProcessOutputPaymentHandler` | `:101-115` |
| `StartOutputPendingBillingHandler` | `:78-90` |

- **Validadores:** `ProcessWeighingOnlyPaymentValidator`, `StartWeighingOnlyPendingBillingValidator`, `StartStoragePendingBillingValidator`, `ProcessOutputPaymentValidator` y `StartOutputPendingBillingValidator` pasan de mayor que 0 a mayor o igual que 0. El handler decide.
- **La creación de la factura en cero** se extrae a un servicio compartido con el depósito adicional (`:289-379`), con la descripción como parámetro.
- **Tiquete:** D16.

**Pruebas de la fase 2:**

| Proyecto | Prueba | Escenario |
| --- | --- | --- |
| `Wms.Tests` | **Nuevo** `Weighbridge/ManifestDeducedWeightsTests.cs` | 21.380 de bruto y 13.700 de manifiesto → tara 7.680, mercancía 13.700, fuente Manifest con un solo pesaje. Con segundo pesaje → fuente Weighings y el neto real. Primer pesaje Tara → sin deducción. Manifiesto mayor que el indicador → sin tara. Pesaje compartido: la tara es el indicador menos la suma de los manifiestos y la mercancía va por camión |
| `Wms.Tests` | Ajustar `WeighingTotalsTests.cs` (`:39-81`), `CycleNetWeightsTests.cs` (sigue: el neto real queda null con un solo pesaje) y `DepositValidationMath` | — |
| `Wms.IntegrationTests` | **Nuevo** `Weighbridge/SingleWeighingManifestNetTests.cs` | Inspección de un solo pesaje con manifiesto: el detalle del depósito sale «Calculado según manifiesto» con el neto igual al manifiesto, y el diario y el detalle del ciclo lo muestran |
| `Wms.IntegrationTests` | **Nuevo** `Weighbridge/AgreementZeroWeighbridgeTests.cs` | Convenio de báscula `FIXED` con tarifa 0: ingreso, Solo báscula y Salida cobran en $0, con factura no fiscal pagada y el ítem «Sin cobro por convenio». Precio general en 0 sin convenio → 400 como hoy. Monto 0 digitado con precio mayor que 0 → 400 |
| `Wms.Tests` | `DocumentLegendsTests` | Sigue en verde |

**Criterio de salida:** el mismo de la fase 1.
**Commit sugerido (BE):** `feat(bascula): pesos del legacy con la tara y la mercancía según el manifiesto, y tiquete en $0 por convenio (DEC-057)`.

---

## 4. Fase 3 — Backend: tarjeta y destinatario de la factura (D17–D23)

- **Tarjeta del depósito (D17, D18):**
  - en `LabelGenerationService` se quitan las transportadoras, va la línea del documento con su tipo y fecha, y la tabla queda de 3 columnas con el embalaje en el texto;
  - las consultas incluyen `PrimaryDocumentType` (en importación también, que hoy no la incluye);
  - `DocumentProductLine.For` aplica D18.
- **Tarjeta por vehículo (D19):**
  - nuevo método en `ILabelGenerationService`;
  - tres endpoints en `ForeignTradeController`, junto a `:278`, `:738` y `:853`;
  - la consulta del camión con sus productos (`EntryProducts` → `WarehouseStorageProduct` → producto, unidad y embalaje), su `EntryLog` y su vehículo, sus `CargoUnits` y el `ServiceRecord` con su tipo de documento.
- **D20:**
  - la entidad y su configuración;
  - la migración `dotnet ef migrations add AddLabelPrintEntry`, que debe traer solo la columna, su índice y su FK;
  - `RecordPrintAsync` y la consulta `label-prints`;
  - además, `DepositStorageEntryDto` agrega `VoidedAt`, para que el frontend oculte la tarjeta del camión anulado (`GetWarehouseStorageEntriesHandler.cs:15-44`).
- **D21–D22:** la consulta de candidatos con su endpoint, y la validación en `UpdateInvoiceRecipientHandler`.

**Pruebas de la fase 3:**

| Proyecto | Prueba | Escenario |
| --- | --- | --- |
| `Wms.Tests` | Ajustar `DocumentProductLineTests.cs` | **Nuevo:** «Cebolla fresca» + «CEBOLLA  FRESCA» → «CEBOLLA FRESCA». «Cebolla fresca» + «fresca» → «CEBOLLA FRESCA». «Arroz» + «blanco» → «ARROZ BLANCO», como hoy |
| `Wms.Tests` | **Nuevo** `ForeignTrade/LabelDocumentLineTests.cs` (función pura de la línea del documento, extraída) | Tipo y fecha. Sin fecha → «N/A». Sin tipo → «Documento» |
| `Wms.Tests` | `LabelAmparaTests` sin cambios; `CarrierCompanyFormatTests` se borra si se borra `CarrierCompanyText` | — |
| `Wms.IntegrationTests` | **Nuevo** `ForeignTrade/VehicleLabelTests.cs` | La tarjeta por vehículo de importación, exportación e inspección responde un PDF, y el registro de impresiones guarda el camión. Camión anulado → 400. Camión de otro depósito → 404 |
| `Wms.IntegrationTests` | **Nuevo** `Billing/InvoiceRecipientCandidatesTests.cs` | Los candidatos traen al cliente, la agencia y la transportadora del depósito. Cambiar a la agencia en Borrador → 200. Un tercero ajeno y sin rol Cliente → 400. Factura aprobada → 400, como hoy |

**Criterio de salida:** el de la fase 1, con la migración aplicada en local.
**Commit sugerido (BE):** `feat(tarjeta,facturacion): tarjeta como el legacy (documento con su fecha, sin transportadora ni unidad, mercancía sin duplicar), tarjeta por vehículo y cambio de destinatario de la factura (DEC-057; migración AddLabelPrintEntry)`.

---

## 5. Fase 4 — Frontend: Báscula (D1–D7 y D13–D16)

- **`F/features/weighbridge/components/StorageServiceForm.vue`:**
  - la búsqueda (`:543-554`) llama a la consulta de candidatos;
  - el campo de fecha deja de ser el mecanismo para elegir el depósito;
  - **`DocumentMatchBanner.vue` pasa a ser un selector:**
    - una tarjeta por candidato abierto, con número, estado, cliente, importador o exportador, agencia, transportadoras, fecha del documento, placas y número de camiones;
    - los cerrados, en gris, con «Cerrado por… el…» o «Migrado», sin poder elegirlos;
    - la opción «Es otro documento: crear depósito nuevo»;
    - sin preselección: si hay abiertos, «Guardar» queda bloqueado hasta elegir;
  - al elegir uno, se precarga como hoy (`:263-314` y `:1213-1222`) y se envía `targetWarehouseStorageId`; con «crear nuevo», el formulario queda editable;
  - el número y el peso del manifiesto pierden «(opcional)», cuentan en `missingCount` (`:597-610`) y se validan (`:653-658`);
  - el comentario de cabecera (`:5-8`) se actualiza.
- **`F/pages/operations/weighbridge/index.vue`:**
  - `handleSearchCargoManifest` (`:937-1016`) y `handleStorageConflict` (`:718-733`) se simplifican: ya no hay 409 de ambigüedad ni de cerrado al guardar;
  - el depósito adicional se rechaza en el frontend si hay un candidato abierto (D5).
- **`F/features/weighbridge/services/weighbridge-service.ts`:** `getStorageDocumentCandidates` y su tipo.
- **`WeightCapture.vue`:** los cuatro campos de D13 en el primer pesaje Bruto de un ingreso a depósito, con el aviso de D10 cuando el manifiesto supera al indicador.
- **`cycles/[id].vue` y `history.vue`:** el neto efectivo y su fuente; sin «Diferencia» cuando la fuente es Manifest.
- **`BillingCollectForm.vue`:** modo `zeroValue` cuando la vista previa trae total 0 y `agreementServiceId` (D16). `index.vue` envía el cobro en cero.

**Pruebas de la fase 4:**
- **Nuevo:** `FT/components/weighbridge/DocumentMatchBanner.spec.ts`. Dos abiertos y un cerrado: el cerrado no se puede elegir. Sin elección, guardar queda bloqueado. «Crear nuevo» desbloquea.
- **Ajustar:** `FT/components/weighbridge/WeightCapture.spec.ts`, con los cuatro campos y el cálculo de 21.380 y 13.700 → 7.680. Y `FT/components/billing/BillingCollectForm.spec.ts`, con el cero por convenio.

**Criterio de salida:** `yarn build`; `yarn test`; `yarn lint` sin pasar la línea base y sin errores en archivos nuevos.
**Commit sugerido (FE):** `feat(bascula): selector de depósito por carta porte, manifiesto obligatorio, pesos del legacy y cobro en $0 por convenio (DEC-057)`.

---

## 6. Fase 5 — Frontend: Comercio Exterior y Facturación (D8 y D17–D23)

- **D8:**
  - `DepositConfirmationRequirements.vue`: `SECTION_BY_CODE` agrega `DIAN_MANIFEST` → `deposit-section-manifest`;
  - `DepositDetailManifestInfo.vue` recibe ese anchor;
  - el tipo `ConfirmationRequirementCode` (`deposit-kanban.ts:58-77`);
  - `useUpdateManifestInfo.ts` también invalida `['foreign-trade','confirmation-requirements', id]`.
- **D19:**
  - `DepositExpandedEntriesTable.vue` agrega, en la columna de acciones (`:145-168`), «Tarjeta del camión», con `aria-label`, oculta en los camiones anulados;
  - usa `useDepositLabelPrint` con las tres funciones nuevas de `foreign-trade-service.ts`;
  - el tipo `IDepositStorageEntryDto` se corrige para reflejar el DTO real y suma `voidedAt`.
- **D20:** el historial de impresiones muestra la placa cuando la hay.
- **D23:** el botón y el diálogo de destinatario, con los candidatos.

**Pruebas de la fase 5:**
- **Nuevo:** `FT/components/foreign-trade/DepositExpandedEntriesTable.spec.ts`. El botón aparece en los camiones vigentes y no en los anulados.
- **Nuevo:** `FT/components/billing/UpdateRecipientDialog.spec.ts`. Lista los candidatos y envía `customerId`.
- **Ajustar:** `DepositDetailManifestInfo.spec.ts`.

**Criterio de salida:** el de la fase 4.
**Commit sugerido (FE):** `feat(comercio-exterior,facturacion): manifiesto DIAN para confirmar, tarjeta por camión y cambio de destinatario de la factura (DEC-057)`.

---

## 7. Fase 6 — Documentación, nota de capacitación y QA local

- **Nota de capacitación:** `D/manuales/nota-operarios-hallazgos-2026-10-26.md`, ya redactada con este plan. Se revisa contra lo construido y se ajusta si cambió algo.
- **QA:**
  - `D/qa/fase-05-comercio-exterior.md`: F5-ETI-001 y F5-ETI-003 sin transportadoras, con el tipo y la fecha del documento y la tabla de 3 columnas; casos nuevos para la tarjeta por camión y el manifiesto DIAN;
  - `D/qa/fase-07-transversal.md:67`, F7-PDF-002;
  - `D/qa/fase-03-bascula.md`: casos del selector de carta porte, el manifiesto obligatorio, los cuatro pesos y el cobro en cero.
- **Verificación local** sobre `wms_qa_preprod`, con la API y el frontend locales:
  1. el escenario H7, con dos clientes y la misma carta porte: el operario elige, y «crear nuevo» deja dos depósitos separados;
  2. un depósito cerrado con el mismo número no bloquea;
  3. el manifiesto obligatorio en Báscula;
  4. el manifiesto DIAN exigido al confirmar;
  5. un solo pesaje de inspección con 21.380 y 13.700: tara 7.680 y mercancía 13.700 en pantalla, tiquete y detalle;
  6. un convenio de báscula en $0: tiquete y factura en cero;
  7. la tarjeta del depósito y la del camión, con `pdftotext -layout`;
  8. el cambio de destinatario a la agencia.
- **Registro:**
  - este plan, con su §8 de estado;
  - `D/planes/README.md`;
  - `DEC-057`, con una línea de commits;
  - `D/contexto/estado.md` (8b);
  - el §16.4 del plan P1: la migración `AddLabelPrintEntry` se suma a las 7 y quedan **8**; los commits nuevos y los casos de QA en staging de este plan;
  - `D/videos/videos-desactualizados-dec-029.md`, o un archivo hermano para DEC-057, con los videos de Báscula y CE que cambian.

**Commit sugerido (docs):** `docs(planes,qa,manuales): DEC-057 construido; nota para operarios y casos QA`.

---

## 8. Estado de las fases

| Fase | Estado | Commits | Notas |
| --- | --- | --- | --- |
| 1 · BE carta porte y manifiestos | Hecha y commiteada (2026-10-26) | BE `c2239cd` | Base BE `dafd573`. `Wms.Tests` 2029 → 2044; `Wms.IntegrationTests` 438/440 → 449/451 (solo las 2 fallas conocidas, que pasan solas); `has-pending-model-changes` limpio, sin migración. Endpoint `GET weighbridge/storage/document-candidates`. **Notas:** (1) `TargetWarehouseStorageId` va como `Guid?` (D1); un Id inexistente responde 404 «El depósito elegido no existe.». (2) «Abierto» para elegir y para la guarda de D5 excluye los migrados (D3); `GetOpenCandidatesAsync` y `MatchOpenAsync` siguen iguales para `by-document` (D6). (3) Se borraron `EnsureTruckEntriesNotClosedAsync` y `ClosedMessage` (sin uso tras D3) con sus 2 pruebas; `Select`, `AmbiguousMessage`, `SelectClosed` y `FindClosedAsync` quedan para `by-document`. (4) `ToInitiateCommand` está en `RegisterStorageEntryHandler`, no en el controlador. (5) Además de los *helpers*, 13 pruebas que registraban ingresos inline recibieron el manifiesto; `SharedWeighingMultiDepositTests.CompletingTheMissingManifest_SplitsTheNet` borra el manifiesto en la base para simular un depósito anterior a D7; `EntryDateReportsTests` espera el manifiesto DIAN del helper en el kárdex; `StorageLinkedServiceFallbackTests` digita el manifiesto DIAN antes de su confirmación local |
| 2 · BE pesos y tiquete en $0 | Hecha y commiteada (2026-10-26) | BE `543fe7f` | Base BE `c2239cd`. `Wms.Tests` 2044 → 2070; `Wms.IntegrationTests` 449/451 → 456/458 (solo las 2 fallas conocidas, que pasan solas); `has-pending-model-changes` limpio, sin migración. **Notas:** (1) El grupo de D9 son los camiones no anulados del ciclo (en el primer pesaje el camión lleva la mercancía de todos sus depósitos); si a alguno le falta el manifiesto no hay tara deducida, pero sí mercancía. (2) `PhysicalWeightStatus` es un `string`, no un enum: se agregó el valor `CalculatedFromManifest` (`DepositPhysicalWeight`); en perecederos gana sobre `NotApplicable` cuando todos los camiones tienen neto. (3) Validación (D12): el peso registrado suma el neto efectivo y la tolerancia del 5 % se mide solo contra lo pesado; sin camiones pesados no se evalúa. (4) Historial (D12): sin manifiesto en todos los camiones, un solo pesaje sigue con CHG-76 (no se pierde el neto de Solo báscula); `WeighbridgeHistoryDto` agrega `ManifestWeightKg` y `NetWeightSource`, el detalle del ciclo `IndicatorWeight`, `DeducedTareWeight`, `DeducedCargoWeight`, `ManifestExceedsIndicator`, `EffectiveNetWeight` y `NetWeightSource`, y el diario `NetWeightSource`. (5) Tiquete: «T. VEHÍCULO» solo sin segundo pesaje (con él, la tara es el pesaje de salida); «(según manifiesto)» va en la línea de «Kilogramos». (6) $0 (D15): con convenio en cero el monto debe ser 0 (400 «El convenio del cliente fija la báscula sin cobro: el total a pagar debe ser 0.»); en «Por facturar» el ciclo se crea Inmediato con la factura en cero pagada; el pago de $0 va en Efectivo como el del depósito adicional. Los inicios devuelven `IsAgreementZero` y los «Por facturar» `IsZeroInvoice`, para el frontend. Servicio compartido `WeighbridgeZeroInvoice`. (7) `BillingScenario.Deposit` agrega `ManifestWeight` (por defecto 12.000) y `ModalityFreeServiceChargeTests` lee `.Amount` |
| 3 · BE tarjeta y destinatario | Hecha y commiteada (2026-10-26) | BE `a8d06dd` | Base BE `543fe7f`. `Wms.Tests` 2070 → 2076 (se borraron las 6 de `CarrierCompanyFormatTests`); `Wms.IntegrationTests` 456/458 → 466/468 (solo las 2 fallas conocidas, que pasan solas). Migración `20261026183022_AddLabelPrintEntry` (columna `warehouse_storage_entry_id`, índice `idx_label_print_entry` y FK con `SET NULL`), aplicada en local solo a `wms_qa_preprod` (`wmsdb` sigue en su esquema viejo); `has-pending-model-changes` limpio. Endpoints: `GET foreign-trade/{imports,exports,inspections}/{id}/entries/{entryId}/label?action=` y `GET billing/invoices/{id}/recipient-candidates`. **Notas:** (1) `CarrierCompanyText` y `CarrierCompanyFormatTests` se borraron (sin uso tras H10); la exportación ya no carga los camiones. (2) Funciones puras nuevas: `LabelDocumentLine` (D17) y `DocumentProductLine.GoodsWithPackaging` (H15). (3) Tarjeta por vehículo: «Cant. ingresa» es `DeclaredQuantity` del camión; con unidades de carga ese valor es nulo y se imprime la suma de sus unidades de carga (`VehicleLabelQuantity`, caso borde de D19 resuelto con DEC-057: «solo la mercancía y cantidades que ingresó ese camión»). Camión anulado → 400 «No se puede imprimir la tarjeta de un camión anulado.»; de otro depósito o inexistente → 404 «El camión no pertenece al depósito.». (4) `label-prints`: cada ítem agrega `vehiclePlate` (nula en la tarjeta del depósito); los conteos suman las dos tarjetas. `DepositStorageEntryDto` agrega `voidedAt`. (5) D21: un candidato por tercero, con todos sus roles (`roles[{code,name}]`), del cliente a la transportadora; las transportadoras salen del pivote `ServiceRecordEntryLogs`, igual que la validación. D22: `BillingService.IsDepositStakeholderAsync` (extraída de `ValidateDepositStakeholderAsync`, que la usa). El `PATCH …/recipient` sigue respondiendo 204, no 200. (6) `BillingScenario.Deposit` agrega `CarrierCompanyId` (opcional) para la prueba de candidatos |
| 4 · FE Báscula | Hecha y commiteada (2026-10-26) | FE `0948d62` | Base FE `d838535` (BE `a8d06dd`). `yarn test` 504 → 523 (100 → 102 archivos); `yarn lint` 281 → 280 errores (413 avisos, igual), ninguno en archivos nuevos; `yarn build` OK. **Notas:** (1) `DocumentMatchBanner` pasa a selector con estado `found` (candidatos y `selection`: el Id o `NEW_DEPOSIT`); la regla de bloqueo es pura (`documentMatchBlocksSave`). Solo con cerrados o migrados no hay que elegir: se crea uno nuevo (D3). (2) Si la consulta de candidatos falla, Guardar queda bloqueado hasta «Reintentar» (D1: sin saber si hay abiertos no se crea un depósito a ciegas); antes no bloqueaba. (3) El 409 «…Vuelva a buscar el documento.» repite la búsqueda; los demás 409 (modalidad, camión repetido, D5) quedan en el aviso global. D5 se rechaza en el frontend con el mismo texto del backend. (4) D2: con el depósito elegido con fecha, la fecha se muestra en solo lectura y viaja `null`. (5) D16: `BillingCollectForm` entra en cero solo con la nueva prop `allowAgreementZero` (la pasa Báscula en los tres flujos) y con destinatario «Tercero registrado», que es el cliente con el que cotiza el backend; Guías y Montacargas no cambian (D15 es solo báscula). Emite `zeroByAgreement` y el resumen del paso dice «Sin cobro por convenio · factura en $0»; si un «Por facturar» responde `isZeroInvoice`, igual. (6) D13: `WeightCapture` recibe `isStorageEntry` y `manifestWeight` (suma de los manifiestos del ciclo, `groupManifestSum`); regla espejo en `utils/manifest-deduced-weights.ts`. El detalle del ciclo muestra los cuatro pesos, el neto efectivo con su fuente y la «Diferencia» solo con neto pesado; el historial agrega la columna «Manifiesto (kg)» y «según manifiesto» bajo el neto (el Excel no cambia). (7) Se borraron `getServiceRecordByDocument` y `getWarehouseStorageByDocument` del servicio FE (sin uso; los endpoints siguen, D6) |
| 5 · FE CE y Facturación | Hecha y commiteada (2026-10-26) | FE `18f79f1` | Base FE `0948d62` (BE `a8d06dd`). `yarn test` 523 → 531 (102 → 104 archivos); `yarn lint` 280 errores y 413 avisos, igual, ninguno en archivos nuevos; `yarn build` OK. **Notas:** (1) D8: `useUpdateManifestInfo` invalida los requisitos con el `warehouseStorageId` de la respuesta y no con el `id` de la mutación, que es el de la importación (`ImportWarehouseStorage`): con ese Id la invalidación no tocaba nada. (2) D19: `DepositExpandedEntriesTable` recibe `vehicleLabelKind` (`import`, `export` o `inspection`) y `labelDepositId`; solo los tres detalles los pasan, y solo si el depósito no está Anulado (como su tarjeta). Las listas expandidas no ofrecen la tarjeta. Tras imprimir se refresca el conteo de `label-prints`. (3) `IDepositStorageEntryDto` se corrigió al DTO real: sin `declaredQuantity` ni `unitMeasure` a nivel de camión (el backend nunca los envió y la columna «Cantidad» mostraba «— —»), con `entryProducts` obligatorio y `voidedAt`. La columna ahora suma lo declarado de los productos del camión por unidad. (4) D20: el historial de la etiqueta agrega la columna «Tarjeta» («Depósito» o «Camión {placa}»). (5) D23: el diálogo pide los candidatos solo abierto (`useInvoiceRecipientCandidates`); en «Cliente registrado» los muestra con sus roles y debajo «O busque otro cliente» (`CustomerSelect`), y el 400 de D22 sale en el aviso del diálogo. La validación sin elección dice «Debe seleccionar el destinatario». **Fuera de alcance:** las tablas de camiones no marcan el camión anulado (solo se oculta su tarjeta) |
| 6 · Docs y QA local | Hecha y commiteada (2026-10-26) | docs `b338cdd` y `20c045b`; FE `41a17e1` (tarjeta de pesos de CE) | Base BE `a8d06dd`, FE `18f79f1`, docs `22d74a3`. Línea base sin cambios: `Wms.Tests` 2076; `Wms.IntegrationTests` 466/468 (las 2 fallas conocidas); `yarn test` 531 (104 archivos); `yarn lint` 280 errores y 413 avisos; `yarn build` OK. Sin cambios de código ni migraciones. **Docs:** casos QA en `qa/fase-03-bascula.md` (F3-REG-020, 021 y 025 a 029; F3-COB-015 y 016; F3-PES-017 y 018; F3-MUL-006; F3-HIS-009; F3-CIC-005; y se ajustaron REG-001, 012 y 013, COB-008, TIQ-002, MCA-001 y 005 a 008, y MUL-005), `qa/fase-05-comercio-exterior.md` (§4, F5-CNF-001, 002 y 017, F5-ETI-001, 003, 008 y 009, F5-IMP-001), `qa/fase-07-transversal.md` (F7-PDF-002) y `qa/fase-06-facturacion.md` (F6-INV-021); nota para operarios revisada; `videos/videos-desactualizados-dec-057.md` nuevo; registro en `DEC-057`, `planes/README.md`, `contexto/estado.md` y §16.4 del plan P1 (8 migraciones). Verificación local: §8.1. **Desviación:** F6-INV-021 se agregó en `qa/fase-06-facturacion.md`, que el §7 no lista, para que D21–D23 tengan caso QA. **Corrección de frontend (a pedido del usuario, sin commit):** D12 quedó sin construir en la tarjeta «Pesos del Depósito» de CE, que ninguna fase de frontend tenía en su lista: con un solo pesaje según manifiesto mostraba el neto con «Pendiente» y «Pendiente de cierre del ciclo». `DepositDetailWeightsCard.vue` reconoce ahora `CalculatedFromManifest` («Calculado según manifiesto», resaltado y sin «Diferencia»), y los tipos `physicalWeightStatus` de importación, exportación e inspección lo incluyen; 3 pruebas nuevas en `DepositDetailWeightsCard.spec.ts`. FE: `yarn test` 531 → 534; `yarn lint` 280 errores y 413 avisos, igual, sin problemas en los archivos tocados; `yarn build` OK. **Descartado:** en la verificación, los cuatro pesos de `WeightCapture.vue` parecían calcularse solo al salir del campo, pero era un efecto del navegador automatizado, que inserta el texto sin `keypress`: con teclas reales (`keydown` + `keypress`, reproducido en Vitest) se calculan mientras se digita, porque `InputNumber` avisa al formulario en cada tecla (`formField.onInput`) |

### 8.1 Verificación local (fase 6, 2026-10-26)

**Entorno:** `wms-postgres-db` (5433) con `wms_qa_preprod`, que ya tenía `AddLabelPrintEntry`; API local (`dotnet run`, Development, puerto 5281) con la cadena cambiada solo de base, SMTP a `migracion-mailpit` y un admin de arranque nuevo, `qa.d57.boot`, con la clave solo en el scratchpad; frontend `yarn dev` (3000); navegador integrado con la sesión de `qa.pre.admin` de la ronda de preproducción. Los pasos 1, 3, 5, 6 y 8 se hicieron en pantalla; los demás, y las comprobaciones de datos, por la API, con lecturas SQL de solo lectura. Datos nuevos con el prefijo `QA-D57`: placas `QD5701`–`QD5710`, el tercero `QA-D57 Cliente Convenio Cero SAS` (convenio `QA-D57-CONV-CERO`, BASCULA `FIXED` 0) y los depósitos `2026BA00041`–`2026BA00046` y `2026INSP00003`. Los camiones `QD5701`–`QD5707` y `QD5709`–`QD5710` quedan con el ingreso abierto en la cola de `wms_qa_preprod`. Al terminar se detuvieron la API, el frontend, mailpit y Postgres.

| Paso | Resultado | Evidencia |
| --- | --- | --- |
| 1. H7: dos clientes, misma carta porte | PASA | `QA-D57-CP-001`: QD5701 crea `2026BA00041` (Cliente Uno). En pantalla, QD5702 ve la tarjeta de `2026BA00041` (cliente, importador, agencia, transportadora, fecha y placa) y «Guardar» deshabilitado; con «Es otro documento: crear depósito nuevo» y Cliente Dos crea `2026BA00042`. QD5703, con `targetWarehouseStorageId`, entra a `2026BA00041`. Los candidatos devuelven los dos depósitos abiertos, cada uno con su cliente, placas y camiones (2 y 1) |
| 2. Depósito cerrado con el mismo número | PASA | `QA-D57-CP-002`: `2026BA00043` con el ingreso de camiones cerrado sale `isOpen=false` con «Cerrado por …»; en pantalla, en gris con candado y sin poder elegirlo. Elegirlo por la API → 409 «El depósito 2026BA00043 ya no está abierto para el documento QA-D57-CP-002. Vuelva a buscar el documento.»; sin elegir → crea `2026BA00044`. El migrado `QA-PRE-CP-M6` (`2025BA00004`, `isMigrated`) no bloquea: crea `2026BA00045` |
| 3. Manifiesto obligatorio | PASA | En pantalla, sin manifiesto: «Registro · Faltan 2 datos» y, al guardar, «El número de manifiesto del camión es obligatorio.» y «El peso del manifiesto del camión es obligatorio.». Por API, 400 con los dos mensajes; con peso 0, 400. Solo báscula (QD5710) se inició sin manifiesto |
| 4. Manifiesto DIAN al confirmar | PASA | `2026BA00041` completo: requisitos solo `DIAN_MANIFEST` «número del manifiesto DIAN»; confirmar → 400 «No se puede confirmar el depósito 2026BA00041. Falta: número del manifiesto DIAN.». Con el número, sin fecha, confirma. En pantalla, `2026BA00042` lista «número del manifiesto DIAN». La inspección `2026INSP00003` confirmó sin pedirlo |
| 5. Un solo pesaje con 21.380 y 13.700 | PASA, tras la corrección de la tarjeta de CE | `2026INSP00003`, tiquete `2026T00058`. En pantalla: P. indicador 21.380 · P. manifiesto 13.700 · T. vehículo 7.680 · P. mercancía 13.700 (con el navegador automatizado aparecieron al salir del campo; con teclas reales se calculan mientras se digita, ver la fila de la fase 6). Tiquete (`pdftotext`): «P. MANIFIESTO 13.700 Kg», «T. VEHÍCULO 7.680 Kg», «PESO MERCANCÍA: 13.700», «Kilogramos (según manifiesto)». Detalle del ciclo: los cuatro pesos y «Peso neto 13.700 kg · según manifiesto», sin «Diferencia». API de CE: `CalculatedFromManifest` con neto 13.700; la tarjeta de CE decía «Pendiente» y se corrigió (fila de la fase 6; verificado con Vitest, no en pantalla). Diario de ingresos (INSP): QD5708 con manifiesto y neto 13.700, fuente `Manifest` |
| 6. Convenio de báscula en $0 | PASA | `2026BA00046` (QD5709): el registro devuelve total 0 e `isAgreementZero`. En pantalla, «Sin cobro por convenio.» sin total ni modo de pago, y el resumen dice «Sin cobro por convenio · factura en $0». Factura: sin número, `IsZeroValue`, total 0, Pagada, pago 0 «ZERO-INVOICE», ítem «Servicio de Báscula — Sin cobro por convenio». Tiquete: «VALOR TOTAL $: 0,00» y «SIN COBRO POR CONVENIO». Solo báscula (QD5710): 10.000 → 400 «El convenio del cliente fija la báscula sin cobro: el total a pagar debe ser 0.»; «Por facturar» con 0 → factura en cero pagada y el ciclo Inmediato |
| 7. Tarjeta del depósito y del camión | PASA | `2026BA00041` (`pdftotext -layout`): sin «Transportadora»; «Carta Porte: QA-D57-CP-001 (2026-10-25)»; Ampara · Saldo · Mercancía «1.000 · 1.000 · CEBOLLA FRESCA (SACOS)» (producto con la descripción igual al nombre, sin repetir). Tarjeta de QD5701: «Placa: QD5701», «Manifiesto No. MAN-QD5701», «Cant. ingresa 730 · CEBOLLA FRESCA (SACOS)», franja «MERCANCIA SIN NACIONALIZAR». Inspección: tarjeta del depósito con el bloque «Documentos:» y tarjeta de QD5708. Camión de otro depósito → 404 «El camión no pertenece al depósito.». `label-prints`: 2 registros, uno con `vehiclePlate` QD5701 |
| 8. Destinatario a la agencia | PASA | Factura de almacenamiento de `2026BA00041` en Borrador: candidatos Cliente Uno (Cliente, Importador), Agencia SIA (Agencia de aduanas) y Transportes (Empresa de transporte). En pantalla, «Cambiar destinatario» → la agencia → Guardar: el encabezado y el bloque pasan a «QA-PRE Agencia SIA SAS». Un tercero ajeno y sin rol Cliente → 400 «El tercero no está relacionado con la factura ni es cliente.» |

**Revisión del código (2026-10-26):** corregido con `plan-cerrado-correccion-dec-057-2026-10-26.md` (fase 1: BE `7189676`, FE `543502d`): C1, «Guardar» ya no sale mientras se busca la carta porte ni con una clave sin buscar (D1); C2, los camiones anulados no cuentan en el estado del peso de CE (D12); C3, la tolerancia del 5 % se mide sobre lo pesado, descontada la parte según manifiesto (D12); C4, el P. manifiesto del primer pesaje excluye los camiones anulados (D13). **Quedan anotados, sin corregir (C5):** la búsqueda repetida tras el 409 borra las cantidades digitadas, y `lastDocumentSearch` es de toda la página; el duplicado de la mercancía se detecta por texto parcial; no hay candidatos de destinatario en las facturas de báscula y montacargas; la tarjeta por vehículo de exportación no valida la modalidad; hay varias consultas por candidato; falta accesibilidad en las tarjetas del selector; la cotización del inicio puede salir con otro cliente.

---

## 9. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| El selector agrega un clic al operario cuando el documento ya existe (`DEC-010`, báscula rápida) | Es un solo clic y solo cuando hay depósitos con ese número. A cambio, se evita mezclar mercancía de dos clientes |
| Exigir el manifiesto frena un camión que llega sin él | Lo pidieron los operarios (`DEC-057`). Solo báscula y Salida no lo piden |
| Un depósito migrado que vuelve a Borrador no tiene manifiesto DIAN | La mayoría lo trae del legacy (`DepositsImporter.cs:264-265`). Si falta, CE lo digita antes de reconfirmar |
| El neto según manifiesto se confunde con un neto pesado | Se rotula «según manifiesto» en todas partes y no se compara contra el manifiesto |
| Con unidades mixtas, la tarjeta no dice la unidad del Ampara | Riesgo aceptado en `DEC-057` |
| Muchas pruebas de integración registran ingresos sin manifiesto o confirman sin manifiesto DIAN | Se ajustan los *helpers* en la misma fase (§0.5) |
| La migración `AddLabelPrintEntry` se suma a las 7 de la fase 13 | Es una columna opcional; el §16.4 del plan P1 se actualiza en la fase 6 |
