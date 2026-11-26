# Plan cerrado — Fase 2 · F07 Tarifas y acuerdos

> **Fecha:** 26 de noviembre de 2026. **Estado:** Aprobado por el usuario el 2026-11-26 («Aprobar con §10»), con los cambios al hub de su §10, que aplica I-07 (2) (§13.4). En ejecución desde que se lanzan sus prompts (§11), después de I-06.
> **Origen:**
> - `DEC-080` y el análisis funcional `levantamiento-2026-11/fase_2-analisis-funcional-2026-11-19.md` (§2.4 a, c, e, f, g P-FAC-11 a P-FAC-14, i y j; §3.2; §3.3), con los wireframes `fase_2-mockups/facturacion.html` (P-FAC-11 a P-FAC-14) y `transversales.html` (P-TR-02, P-TR-03 y P-TR-11);
> - el plan maestro `planes/sprint-11/plan-maestro-implementacion-fase-2-2026-11-20.md` (M1 a M25, `DEC-081`), en especial M14, M15, M16, M20 y M21, §3.4 y §7.2;
> - AF dueñas (10, plan maestro §3.1): AF-108, AF-112, AF-114, AF-115, AF-116, AF-117, AF-118, AF-120, AF-123 y AF-125;
> - lo integrado de F01 (D18, D19, D41, D42; C-F01-77), F02 (D1, D2, D10 y sus ajustes D1 y D2), F04 (D2, D4; C-F04-05 a C-F04-07 y C-F04-10) y F05 (D15, D17 a D19; C-F05-22);
> - las respuestas del usuario a la ronda de preguntas de este plan (2026-11-26), en D1 a D13, y a la consulta sobre las retenciones del mismo día, en D52 a D55.
>
> **Base:** BE `fase-2` `348ab15` (con I-05) · FE `fase-2` `3531432` (con I-05) · docs `main` `6b1f2cf`. Rama: `f2/f07-tarifas-acuerdos` en BE y FE, que sale de `fase-2` cuando I-06 esté fusionada.
> **Partes:** 0 (contrato, §2) · 1 (backend, cuatro fases) · 2 (maquetación, tres fases y la revisión del usuario) · 3 (I-07 en dos fases y la carga inicial, §13 y §14). **Migraciones:** `BillingBillToAndServiceVat` (BE-1), `AgreementTariffValidity` (BE-2) y `StorageFormulasAndEntryVehicleMark` (BE-3); BE-4 no lleva.
> **Rutas:** relativas a `code_workspace/`. Prefijos: `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `FT/` = `Frontend/wms/test/`; `D/` = `docs/`; `A/` = el análisis; `PM/` = el plan maestro; `P01/` = `D/planes/sprint-11/f01-nucleo/plan-cerrado-f2-f01-nucleo-2026-11-21.md`; `P02/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-base-2026-11-21.md`; `PAJ/` = `D/planes/sprint-11/f02-base/plan-cerrado-f2-f02-ajustes-qa-2026-11-24.md`; `P04/` = `D/planes/sprint-11/f04-bodega/plan-cerrado-f2-f04-bodega-2026-11-25.md`; `P05/` = `D/planes/sprint-11/f05-comercio-exterior/plan-cerrado-f2-f05-comercio-exterior-2026-11-25.md`.

**Cómo leer este plan.** El ejecutor de cada parte lee §0, §1, §2.1 (índice) y la sección de su fase en §8 (o §13 y §14 en la parte 3). Cada fase nombra sus decisiones, sus endpoints (con la ficha de §2.2 y el esquema de §2.3 que le tocan), sus archivos (§3) y sus casos QA (§6). El resto se lee solo cuando la fase lo cita. Las líneas citadas son de la base (`348ab15` y `3531432`); el plan se escribió antes de que F06 se integre, así que cada ejecutor las confirma con `grep` antes de cambiar.

---

## 0. Instrucciones para el ejecutor

1. **Lecturas mínimas:** `D/README.md`, el `AGENTS.md` de tu repo (su sección «Eficiencia de contexto y cierres por fase» rige tu trabajo), `D/procesos/flujo-de-trabajo-agentes.md`, `PM/` §1.2, §5 y §6, y de este plan §0, §1, §2.1 y tu fase. El frontend lee además `D/contexto/convenciones-tecnicas.md` §3 («Drawer de detalle», «Tablas de listado», «Aviso junto a un dato» y «Páginas que no son listados»).
2. **Rama y git** (`PM/` §5.3): la rama sale de `fase-2` cuando I-06 esté fusionada, con lo que haya en `fase-2` en ese momento. `git fetch`; si `develop` avanzó, fusiona `develop` en `fase-2`; crea `f2/f07-tarifas-acuerdos` desde `fase-2` (o retómala si ya existe) y trabaja ahí. Al cerrar cada fase: commit con el mensaje de §12 y push de la rama. Sin `push --force`. La fusión en `fase-2` la hace I-07, en los dos repos a la vez.
3. **Antes de empezar, confirma las líneas citadas** con `grep` (el plan se escribió con F05 integrada y F06 sin integrar). Si una ruta, una firma o un comportamiento cambió (en especial lo que F06 toque del cobro de la guía, `B/Wms.Application/ForeignTrade/Common/Services/ForeignTradeService.cs:30-39`, o de la etapa Bodega del detalle de CE), detente y pregunta con todas las dudas en un solo mensaje.
4. **Una fase por turno** (`PM/` §6): cierra la fase con sus compuertas, el commit, el push y el estado en §8 y en la matriz, y te detienes con el reporte.
5. **Migraciones:** solo con `dotnet ef … --project Wms.Infrastructure --startup-project Wms.Api` y solo contra la base local (`DEC-004`, M6). Cada fase de backend que la lleva usa el nombre y el contenido de §4. Antes de generarla, trae lo último de `fase-2`. Nunca edites a mano `Migrations/*`, los `*.Designer.cs` ni el snapshot. Las bases locales se recrean (`DEC-006`): ninguna migración convierte acuerdos ni impuestos.
6. **Contrato:** §2 es la única fuente del frontend para F07 (`PM/` R3). Cada endpoint nuevo o modificado de tu fase tiene al menos una prueba de integración que verifica su respuesta y sus mensajes de error (`PM/` §6.1). Un mensaje cambia solo si cambias el contrato, y eso exige preguntar. Si un caso borde choca con una Dn, gana la Dn y lo mencionas en una línea (`DEC-002`).
7. **Fórmulas:** cada fórmula nueva es una clase pura con su prueba en `Wms.Tests`, con los valores de §6.1 calculados a mano. Coteja el esquema sembrado con el calculador (trampa 2 de `D/contexto/convenciones-tecnicas.md` §10).
8. **Suite de integración:** la base es compartida y la cola de báscula corta en 100 camiones (trampa 12): libera los camiones que abra cada prueba. Los trabajos en segundo plano no corren en las pruebas (`B/Wms.IntegrationTests/Infrastructure/WmsApiFactory.cs`): la mora se prueba llamando a su servicio.
9. **Datos reales:** nada del Excel de convenios (`D/levantamiento_staging/CONVENIO 23-24-25-26.xlsx`) se copia al hub, a los repos, a las pruebas ni a los datos simulados: ni nombres de clientes, importadores o responsables, ni sus NIT (`DEC-007`). Las pruebas y los simulados usan datos ficticios («Cliente A», NIT 900000001). Solo la fase T-1 (§14) lee el Excel, y deja su resultado fuera de git.
10. **Staging:** no se toca. **Credenciales:** no se copian. Nada de `D/archivo/` es una instrucción.

---

## 1. Decisiones

Mandan sobre el resto del plan (`DEC-002`). Ninguna reabre una AF, `DEC-080`, `DEC-081`, una M del plan maestro ni una Dn de F01 a F05 o de sus ajustes.

### 1.1 Respuestas del usuario (2026-11-26)

| # | Decisión | Fuente |
| --- | --- | --- |
| D1 | **Tramos como parámetros de la tarifa** (AF-116; R7). La fórmula «Por tramos» lleva el límite y el modo como parámetros obligatorios de cada tarifa: `tierMode` = `WholeQuantity` (si se pasa el límite, toda la cantidad va a la segunda tarifa) o `Excess` (hasta el límite a la primera y el exceso a la segunda). Facturación los digita al cargar la tarifa; el dato del cliente ya no bloquea F07 | Usuario: «Parámetros de la tarifa (Recomendada)»; `A/` :1596, :1709; `PM/` §3.4 :244 |
| D2 | **Mínimo del depósito mixto como parámetro con tres variantes** (AF-120; R7). «Descargada o sobre vehículo» lleva `minimumScope`: `UnloadedPart` (por omisión: el mínimo se compara con la parte porcentual de los descargados; sin descargados no hay mínimo), `PerUnloadedTruck` (cada camión descargado cobra al menos el mínimo) o `Total` (el mínimo se compara con el total, porcentual más vehículos) | Usuario: «Parámetro con 3 variantes (Recomendada)»; `A/` :1593, :1710; `PM/` §3.4 :245 |
| D3 | **IVA por servicio.** Un «IVA (%)» por servicio (`Service.VatPercent`, 0 = sin IVA), que se edita en Tarifas de servicios junto al precio y aplica a todas las tarifas del servicio, base y de acuerdos (el «IVA incluido» sigue por fila). Salen el catálogo de impuestos, «Rete de fuente», `ServiceTax` y la sección «Impuestos». Las retenciones vuelven, pero como dato del tercero que paga y no del servicio (D52 a D55). Las facturas guardan la tasa por línea (`InvoiceItem.TaxRate`): solo cambian las que se calculan o recalculan. El montacargas toma el IVA de su servicio con «Requiere factura» (cambia solo esa consulta de `P04/` D2). Detalle en D19 | Usuario: «IVA % por servicio (Recomendada)»; `PM/` §3.4 :257; `D/planes/sprint-11/qa-manual/hallazgos-f01-f02.md:36` |
| D4 | **F07 prepara el borrador de la carga inicial.** Después de I-07, la fase T-1 (§14) traduce la hoja 2026 del Excel de convenios a la plantilla final, fuera de git (`db_legacy/trabajo/acuerdos/`), con un informe solo en cifras de lo que no se pudo traducir. Facturación lo revisa y lo importa antes del despliegue final. Reemplaza la fase 4b pendiente de `DEC-043` (`PM/` §7.2) | Usuario: «F07 prepara un borrador (Recomendada)»; AF-114; `DEC-007` |
| D5 | **Vigencia por tarifa.** Un acuerdo por cliente; cada tarifa lleva «vigente desde» y «vigente hasta», y la siguiente tarifa del mismo ámbito cierra la anterior. Salen los estados del convenio, el trabajo de activación y los 12 endpoints de `stakeholder/{stakeholderId}/agreement…`. Detalle en D22 a D25 | Usuario: «Vigencia por tarifa (Recomendada)»; AF-114; `A/` :1613 |
| D6 | **La plantilla se arma y se lee en el API**, con la librería ClosedXML (licencia MIT, dependencia nueva aprobada por el usuario). El API genera el `.xlsx` (vacío o con lo de un cliente) y recibe el archivo en la vista previa y en la confirmación. Detalle en D37 a D41 | Usuario: «En el API» |
| D7 | **Rutas, con enlaces desde los detalles.** `/billing/configurations` (listado, conserva su ruta) y `/billing/configurations/[customerId]` (P-FAC-11, página con «Volver» y «Guardar»); `/rates/agreements` (clientes con acuerdo), `/rates/agreements/[customerId]` (P-FAC-12) y `/rates/agreements/import` (P-FAC-14); `/rates/services` (Tarifas de servicios, listado con drawer); `/admin/forklift-rates` (conserva su ruta) con el patrón. El tercero y el servicio pierden sus secciones de acuerdos y tarifas y ganan «Ver acuerdo» y «Ver tarifas» en su menú «Acciones», solo para Admin y Facturación | Usuario: «Con enlaces desde los detalles (Recomendada)»; `P02/` D1, D2; `PAJ/` D1 |
| D8 | **Cuatro fases de backend y tres de maquetación** (§8). BE-1 configuración, «Facturar a», mora e IVA; BE-2 acuerdos con vigencia; BE-3 las cuatro fórmulas, el simulador y la marca «Queda sobre el vehículo»; BE-4 plantilla e importación. FE-1 configuración de facturación y montacargas; FE-2 acuerdos con «Agregar tarifa» y simulador; FE-3 tarifas de servicios y plantilla. Después de FE-3, la revisión del usuario (§8.8); I-07 en dos fases y T-1 | Usuario: «4 de backend y 3 de maquetación (Recomendada)» |
| D9 | **Base del % en «Descargada o sobre vehículo»: el valor CPI repartido por camión.** El % se cobra sobre el valor de la mercancía descargada y la tarifa por vehículo es fija, sin mirar el valor del camión. Base de lo descargado = valor CPI del depósito en pesos × (suma de precios de los camiones descargados ÷ suma de precios de todos los camiones). Todo descargado: el CPI completo. Sin precios por camión, la parte se reparte por número de camiones; sin camiones (los migrados, M19), todo cuenta como descargado. Respeta la corrección del CPI que haga CE (AF-94). Un camión sin precio en un depósito donde otros sí tienen cuenta $0 y la factura lo advierte (D32) | Usuario: «El primero se cobra sobre el valor CIF para la mcia descargada y los 168.000 x Veh es un valor fijo que se cobra por vehículo. No tiene en cuenta el valor de cada camión», y después «CPI repartido por camión (Recomendada)»; AF-120, M16 |
| D10 | **Camión sin recepción: cuenta como descargado y la recepción recalcula.** Al facturar, un camión sin recepción cuenta como descargado. Cuando la marca cambia (recepción de Bodega o marca de CE, D11), la factura del período se recalcula con el mecanismo único (`DEC-022`), solo si el depósito cobra con esta fórmula (D34) | Usuario: «Descargado y recálculo (Recomendada)»; AF-119, AF-120 |
| D11 | **CE marca «Queda sobre el vehículo» en la etapa Bodega; la marca vive en la entrada y no mueve inventario.** La marca pasa de la recepción (`ReceptionLog.StaysOnVehicle`) a la entrada del depósito (`WarehouseStorageEntry.StaysOnVehicle`): la pone Bodega al recibir, como hoy (con la ubicación `SOBRE-VEHICULO`, `P04/` D4), y CE la cambia en la etapa Bodega del detalle del depósito, antes o después de la recepción; si CE marcó antes, la recepción la trae precargada. Cambiarla no mueve inventario (las ubicaciones siguen siendo de Bodega), queda en la auditoría y recalcula (D10) | Usuario: «Tambien agregar en el detalle del deposito en CE en la etapa de bodega la opción de marcar "Queda sobre el vehículo"», y después «En la entrada, sin mover (Recomendada)» |
| D12 | **«Por tramos» con magnitud.** La fórmula de tramos de AF-116 lleva `magnitude`: `Weight` (peso de mercancía en kg o en toneladas, AF-113) o `Vehicles` (número de camiones del depósito). Cubre las dos tarifas por volumen de la hoja 2026 y la tarifa por vehículo con tramos por cantidad (3 filas) | Usuario: «"Por tramos" con magnitud (Recomendada)» |
| D13 | **Prorrateo por saldo como parámetro de cada tarifa.** Las fórmulas nuevas llevan `prorated` (`true` por omisión, como el % prorrateado de `DEC-029` §7.5): con `true`, el valor o el peso se multiplican por saldo ÷ ingresado (la fracción del % prorrateado de hoy); con `false`, se cobran completos cada período. El límite de «Según el valor» se compara siempre con el valor CPI completo; los mínimos y las tarifas por vehículo o por unidad de carga no se prorratean | Usuario: «Parámetro por tarifa» |
| D52 | **Retenciones del tercero que paga.** La retención la practica quien paga la factura, que con AF-123 puede ser el «Facturar a» y no el cliente. Cada tercero tiene su lista de retenciones (tabla `stakeholder_withholdings`, por tercero y no por configuración), y al facturar se usan las del destinatario de la factura. Se editan en P-FAC-11: las del cliente en su página, y las de cada «Facturar a» (general o de excepción) en un modal desde su fila, aunque ese tercero no sea cliente | Usuario, 2026-11-26, a su pregunta «Es posible cargar esto en la configuracion de facturacion del cliente, y que al momento de facturar en el modal al operario de facturacion vea estos impuestos»: «Del destinatario (Recomendada)». En la hoja 2026, la columna «Observación» nombra Retefuente en 71 filas, ReteICA en 38 y ReteIVA en 16 (47 responsables), sin porcentaje |
| D53 | **Selector con las retenciones comunes, sin texto libre.** Cada retención se elige de una lista fija (`WithholdingType`): «Retención en la fuente» (`Retefuente`) y «ReteICA» (`ReteIca`), sobre el subtotal (antes de IVA), y «ReteIVA» (`ReteIva`), sobre el IVA. El tercero digita el porcentaje de cada una (mayor que 0 y hasta 100, con hasta 4 decimales: la ReteICA suele ir por mil, p. ej. 0,966 %); una retención no se repite en el mismo tercero. Sin base mínima: si no aplica a una factura, el operario la quita al facturar (D54) | Usuario, 2026-11-26: «No dejarlo libre, que se a un selector con las mas comunes que pueden utilizar.» |
| D54 | **Las retenciones restan del saldo por cobrar.** Al facturar, el operario ve las retenciones del destinatario calculadas y las puede ajustar o quitar; quedan guardadas en la factura; el total no cambia y el saldo por cobrar es total − retenciones, así que pagar el neto la deja Pagada y la mora cuenta sobre el neto. F07 deja la configuración y la regla pura del cálculo (`StorageWithholdings`: cada retención = % × su base, redondeada a 2 decimales con `AwayFromZero`); el modal «Facturar», la retención guardada en la factura y su efecto en el saldo, los pagos y la mora los construye F08 (P-FAC-04, AF-122) | Usuario, 2026-11-26: «Restan del saldo (Recomendada)» |
| D55 | **Solo en las facturas de almacenamiento.** Báscula, guía y montacargas no muestran ni restan retenciones | Usuario, 2026-11-26: «Solo almacenamiento» |

### 1.2 Configuración, «Facturar a», mora e IVA (BE-1)

| # | Decisión | Fuente |
| --- | --- | --- |
| D14 | **Ciclos sin mes calendario y con «Otro: N días»** (AF-108, AF-115, M20). `BillingCycle` suma `Custom`, y `StakeholderBillingConfiguration` suma `CycleDays` (entero, de 1 a 360, obligatorio con `Custom` y nulo con los demás). El catálogo (`B/Wms.Application/Billing/Common/Services/BillingCycleCatalog.cs:24-33`) queda: `Weekly` «Semanal (7)», `Biweekly` «Quincenal (14)», `Days15` «Quincenal (15)», `Days30` «Mensual (30)», `Days90` «Trimestral (90)», `Days180` «Semestral (180)», `Days360` «Anual (360)» y `Custom` «Otro: N días», como P-FAC-11. `Monthly` sale del catálogo como salió `OnDemand`: no se ofrece ni se acepta al guardar, y una fila que lo traiga se lee como 30 días (M20: el período abierto conserva su fin y los siguientes cuentan 30). Sin configuración, el ciclo por omisión pasa de `Monthly` a `Days30` (`B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:420`, `:567`; `BillingService.cs:103`). `StoragePeriodCalculator.ForStart` recibe la longitud en días: fin = inicio + N, límite = fin + 3, siguiente = fin + 1 (AF-115, como hoy). Ventana de la consolidada con `Custom`: semanal si N ≤ 7, quincenal si N ≤ 15 y mensual si no | AF-108, AF-115, M20; `A/` §2.4 f («Ciclos y períodos») |
| D15 | **«Facturar a» general y excepciones por importador** (AF-112, AF-123). `StakeholderBillingConfiguration.BillToStakeholderId` (tercero, nulo = el mismo cliente) y la entidad nueva `BillToException` (tabla `billing_bill_to_exceptions`: configuración, importador y «Facturar a», auditada, única por configuración e importador). La regla pura `BillToResolver` da el destinatario: la excepción del importador del depósito; si no hay, el general; sin configuración, el cliente, como hoy. El «Facturar a» y el importador deben existir y estar activos, y el importador debe tener el rol Importador | AF-112, AF-123; P-FAC-11 |
| D16 | **Destinatario y cliente en la factura de almacenamiento.** Al abrir, renovar o refacturar un período, `Invoice.CustomerId` (el destinatario) toma el resultado de `BillToResolver`, y el campo nuevo `Invoice.DepositCustomerId` guarda el cliente del depósito (nulo en báscula, guía y montacargas). El recálculo (`DEC-022`) no cambia el destinatario. El cambio de cliente con factura en Borrador (`DEC-056`, `DepositCustomerBillingChange`) actualiza los dos. Corregir el importador del depósito (C-F05-10) no toca las facturas existentes: Facturación cambia el destinatario en Borrador, como hoy. La consolidada se agrupa por cliente y «Facturar a» (`BillingService.GetOrCreateConsolidatedInvoiceAsync`, `B/Wms.Application/Billing/Common/Services/BillingService.cs:44`) | AF-112, AF-123; `DEC-056`. Resuelta sin preguntar (`DEC-002`): la consolidada de un cliente con dos «Facturar a» no puede ir a un solo destinatario |
| D17 | **«Cambiar destinatario» acepta el «Facturar a».** Los candidatos de la factura (C-F07-05) suman los «Facturar a» configurados del cliente del depósito, marcados; `UpdateInvoiceRecipientHandler.EnsureRecipientRelatedAsync` (`B/Wms.Application/Billing/Commands/UpdateInvoiceRecipient/UpdateInvoiceRecipientHandler.cs`) los acepta (C-F07-06). El resto de la regla y su mensaje no cambian | AF-112 («Facturación lo cambia en Borrador como hoy»); `DEC-057` D22 |
| D18 | **La mora y los días de pago son del cliente del depósito** (AF-112). `OverdueSweep.Apply` (`B/Wms.Application/Billing/Jobs/OverdueSweep.cs:20-25`) suma el saldo vencido por `DepositCustomerId ?? CustomerId`; el estado financiero y el bloqueo de salidas siguen la regla de hoy sobre ese cliente. La aprobación toma los días de pago de `DepositCustomerId ?? CustomerId` (`B/Wms.Application/Billing/Commands/ApproveInvoice/ApproveInvoiceHandler.cs:33-34`); F08 conserva esa regla en «Facturar» (AF-122) | AF-112, AF-122; `A/` §2.4 f («Destinatario y mora») |
| D19 | **IVA por servicio, en detalle** (D3). `Service.VatPercent` (decimal 0 a 100, dos decimales, auditado con el servicio). Semilla: `ALMACENAMIENTO` 19 (hoy su único impuesto sembrado, `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:141-145`), `BASCULA` 19 (T3 de `DEC-041`: «$16.806,72 + IVA»), `MONTACARGAS` 19 (solo se suma con «Requiere factura», `P04/` D2) y `PAPELERIA` y `GUIA_SALIDA` 0 (hoy sin impuesto; Facturación los fija en Tarifas de servicios). `BillingService.GetTotalTaxRate` (`:34`) devuelve `VatPercent`, y las consultas que incluían `ServiceTaxes` dejan de hacerlo (`git grep ServiceTaxes`: unas 15). El IVA del montacargas con «Requiere factura» es el de su servicio (`B/Wms.Application/Warehouse/Common/Services/ForkliftService.cs:156-163`); `GetForkliftTaxRatePercentAsync` (`:150-154`) no puede empezar a sumar IVA sin factura: el agente revisa sus usos con `grep` y la deja en 0 o la borra. Se borran `Tax`, `ServiceTax`, `TaxKind`, `TaxIds`, sus configuraciones, semillas, DTO y mapeadores, `GetTaxes`, `AssignServiceTax` y `RemoveServiceTax`, con sus endpoints (C-F07-11 a C-F07-13). `ServiceDto` cambia `taxes` por `vatPercent` (C-F07-08). Se edita con C-F07-09 y con el precio base (C-F07-10) | D3; `P04/` D2; `DEC-041` (T3) |

### 1.3 Acuerdos y tarifas base (BE-2)

| # | Decisión | Fuente |
| --- | --- | --- |
| D20 | **«IVA incluido» en las fórmulas nuevas.** Las cuatro fórmulas nuevas no desagregan el IVA de su resultado (`SupportsTaxIncluded = false`, como las de porcentaje y la de umbral de peso). El «IVA incluido» de la fila llega al calculador (`FormulaContext.RateIncludesVat`, que pone `FormulaPricing`) y se aplica solo a las tarifas cotizadas en pesos (por vehículo, por unidad de carga, fija, por kg o tonelada, de cada tramo): tarifa ÷ (1 + IVA). Las partes porcentuales son siempre netas y el IVA se suma después. Los mínimos siguen `minimumIncludesVat` (con IVA por omisión, `MinimumVat`, CHG-24) | Resuelta sin preguntar (`DEC-002`): `B/Wms.Domain/Billing/IFormulaCalculator.cs` («las fórmulas de porcentaje… su resultado es la base neta»); `B/Wms.Application/Billing/Calculators/MinimumVat.cs` |
| D21 | **Qué día rige una tarifa.** El período de almacenamiento cobra con las tarifas vigentes el día de su inicio, también al recalcularse (como la cantidad, `DEC-053` BR-06-005); báscula, guía y montacargas, con las vigentes el día del cobro (Colombia). `IBillingResolver.ResolveRuleAsync` recibe ese día (`B/Wms.Application/Billing/Services/BillingResolver.cs:168-189` hoy usa «ahora») | Resuelta sin preguntar (`DEC-002`): AF-114 («La anterior rige hasta esa fecha»); `DEC-053` |
| D22 | **Modelo del acuerdo** (D5). `Agreement` queda como contenedor único por cliente (índice único por `StakeholderId`), sin `Reference`, `Name`, `Status`, `ScheduledActivationDate`, `ActivationDate` ni `ArchivingDate`; se crea solo con la primera tarifa. `AgreementService` («tarifa del acuerdo») suma `ValidFrom` (fecha) y `ValidUntil` (fecha o nulo) y pierde `IsActive`. Se borran `AgreementStatus`, `AgreementEffectivity`, `AgreementActivationService`, `IAgreementActivationService`, `AgreementActivationBackgroundService` (`B/Wms.Api/BackgroundJobs/AgreementActivationBackgroundService.cs:12`) y su registro, los comandos y consultas de `B/Wms.Application/Agreements/` que el recurso nuevo no use, y los 12 endpoints de `B/Wms.Api/Controllers/v1/StakeholderController.cs:285-457` (C-F07-19 a C-F07-30) | D5 |
| D23 | **Línea de tiempo de las tarifas** (regla pura `AgreementTariffTimeline`, probada en `Wms.Tests`). **Ámbito:** servicio, producto (o todos), modalidad (o todas) y perecedero (sí, no o todos). **Rige el día d** la tarifa del ámbito con `ValidFrom ≤ d` y (`ValidUntil` nulo o `d ≤ ValidUntil`). **Alta desde F:** si el ámbito ya tiene una tarifa desde F, 409; la tarifa del ámbito con el mayor `ValidFrom < F` que siga vigente en F termina el día F − 1; si hay una posterior, la nueva termina el día antes de que esa empiece. **Retirar:** una tarifa que aún no empieza se borra y la anterior recupera el fin que tenía la borrada; una vigente termina hoy (`ValidUntil` = hoy); una terminada no se retira (409). **Editar:** fórmula, parámetros, papelería e «IVA incluido»; «vigente desde» solo si aún no empieza (se vuelve a armar la línea de tiempo); el ámbito no se edita (se retira y se agrega otra). **Estado:** `Scheduled` («Programada», empieza después de hoy), `Current` («Vigente») o `Ended` («Terminada»). Se puede dar de alta con fecha pasada (la carga inicial trae «01/01/2026»); dar de alta o editar no recalcula facturas (`DEC-043`: crear un convenio no recalcula las existentes) | D5; AF-114 |
| D24 | **Quién lee las tarifas del acuerdo.** `BillingResolver.FindActiveAgreementServiceAsync` (`:168-200`) elige con la línea de tiempo del día de D21 y luego por especificidad (`RuleSpecificity`, sin cambios). Pasan a la misma regla los que hoy miran `Agreement.Status == Active`: el precio de la guía (`B/Wms.Application/ForeignTrade/Common/Services/ForeignTradeService.cs:30-39`), el montacargas (`ForkliftService.cs:83-94`), la desactivación del servicio (`B/Wms.Application/Services/Commands/DeactivateService/DeactivateServiceHandler.cs:24-27`, que mira tarifas vigentes o programadas) y `StorageFormulaRestriction` (`B/Wms.Application/Common/Validation/StorageFormulaRestriction.cs:33-41`). La báscula en $0 por convenio (`DEC-057` H5b) sigue saliendo del resolver (`B/Wms.Application/Weighbridge/Common/Services/WeighbridgeService.cs:64-81`) | D5, D21 |
| D25 | **Recurso nuevo `rates/agreements`** (controlador `RatesAgreementsController`, `BillingAccess`): listado de clientes con acuerdo (C-F07-14), tarifas de un cliente (C-F07-15 a C-F07-18) y plantilla (C-F07-37 a C-F07-39). La papelería del contrato es un `paperwork` booleano: el backend la guarda como `LinkedServiceId` = servicio `PAPELERIA` (AF-117, BR-06-004); su importe sale del resolver de `PAPELERIA` para el cliente, como hoy | D5, D6; AF-117 |
| D26 | **Tarifas base** (`PAJ/` D2; `A/` §3.3, «Regla de precio del servicio → mismo patrón que P-FAC-13»). `ServicePricingRule` no cambia de modelo (sin vigencia; activar y desactivar como hoy) ni de endpoints (C-F07-43 a C-F07-47); su formulario es el mismo diálogo de P-FAC-13 en modo «tarifa base», sin «vigente desde». `ServicePrice` (precio con vigencia, `DEC-055`) y `ServiceMinimumValue` (mínimo por modalidad, `DEC-020`) siguen igual | `PAJ/` D2; `DEC-020`, `DEC-055` |
| D27 | **Las cuatro fórmulas nuevas son solo de Almacenamiento.** Usan datos del depósito (valor CPI, camiones, peso, unidades de carga). `StorageFormulaRestriction` suma la regla inversa a la de `PER_VEHICLE_TYPE`: en acuerdos (C-F07-16, C-F07-17) y tarifas base (C-F07-44, C-F07-45), 400 «La fórmula «{nombre}» solo aplica al servicio de Almacenamiento.». `GET FormulaType` lo informa en `serviceScope` (C-F07-31) | Resuelta sin preguntar (`DEC-002`): AF-116 («Tarifas del Excel 2026», todas de almacenamiento); `DEC-025` |
| D28 | **Permisos de Tarifas y acuerdos.** Los endpoints nuevos y modificados de configuración, acuerdos, IVA y plantilla usan `BillingAccess` (Admin, Billing; AF-127). Ninguna lectura que se retira la usa otro rol: los acuerdos se leían solo desde el detalle del tercero para Admin y Facturación (`F/features/stakeholders/components/StakeholderDetailSections.vue:59`) y los impuestos solo desde el del servicio (`F/features/services/components/ServiceProfile.vue`); I-07 lo confirma con `grep` antes de borrar (`DEC-005`). Tabla en §1.7 | AF-127; `DEC-005`; `PM/` §5.6 |

### 1.4 Fórmulas, simulador y marca «Queda sobre el vehículo» (BE-3)

| # | Decisión | Fuente |
| --- | --- | --- |
| D29 | **Las cuatro fórmulas de AF-116**, con su código y sus parámetros (esquema sembrado; todas `BillingBasis.Flat`): <br>• `UNLOADED_OR_ON_VEHICLE` «Descargada o sobre vehículo»: `percentage` (0 a 100, obligatorio), `ratePerVehicle` (≥ 0, obligatorio), `minimum` (≥ 0, opcional), `minimumScope` (`UnloadedPart` · `PerUnloadedTruck` · `Total`; por omisión `UnloadedPart`; D2), `minimumIncludesVat` y `prorated` (D13). <br>• `VALUE_THRESHOLD` «Según el valor»: `valueLimitCop` (> 0), `belowMode` (`Fixed` · `PerCargoUnit`), `belowRate` (≥ 0), `belowCargoUnitTypeCode` (obligatorio y visible solo con `PerCargoUnit`), `abovePercentage` (0 a 100) y `prorated`. <br>• `WEIGHT_RATE_MINIMUM` «Por tonelada o kilo con mínimo»: `rate` (≥ 0), `weightUnit` (`Ton` · `Kg`), `minimum` (≥ 0), `minimumIncludesVat` y `prorated`. <br>• `TIERED` «Por tramos»: `magnitude` (`Weight` · `Vehicles`; D12), `weightUnit` (`Kg` · `Ton`; visible solo con `Weight`), `limit` (> 0, en la unidad de la magnitud), `rateUpTo` (≥ 0), `rateFrom` (≥ 0), `tierMode` (`WholeQuantity` · `Excess`; D1) y `prorated` (solo con `Weight`). <br>Los enumerados llevan su rótulo en español en el esquema (`enumLabels`) y los condicionales, `visibleWhen` (§2.3). Los parámetros booleanos siguen el patrón de hoy (`String` con `uiHint: "boolean"`) | AF-116; D1, D2, D12, D13 |
| D30 | **Reglas de cálculo** (puras, en `B/Wms.Application/Billing/Calculators/`; f = saldo ÷ ingresado si `prorated`, si no 1; IVA = tasa del servicio): <br>• **Descargada o sobre vehículo:** reparto de D9 (sᵢ = precioᵢ ÷ Σ precios; sin precios, 1 ÷ n; sin camiones, un solo «camión» descargado con s = 1). Parte de cada descargado pᵢ = % × CPI × sᵢ × f; P = Σ pᵢ. Vehículos V = tarifa neta × camiones sobre el vehículo. Mínimo neto m (D2): `UnloadedPart` → máx(P, m) + V si hay descargados, si no V; `PerUnloadedTruck` → Σ máx(pᵢ, m) + V; `Total` → máx(P + V, m). <br>• **Según el valor:** si CPI ≤ límite (CPI completo, en pesos con la tasa de la semana, AF-85), la regla de abajo: `Fixed` → tarifa neta; `PerCargoUnit` → tarifa neta × unidades facturables del tipo (como `PER_CARGO_UNIT`); si CPI > límite, % × CPI × f. <br>• **Por tonelada o kilo con mínimo:** máx(tarifa neta × peso × f (÷ 1.000 si es tonelada), m). Sin peso, el mínimo. <br>• **Por tramos:** q = peso × f (en la unidad) o número de camiones; si q ≤ límite, tarifa₁ × q; si no, `WholeQuantity` → tarifa₂ × q y `Excess` → tarifa₁ × límite + tarifa₂ × (q − límite). <br>El redondeo es el de `FormulaPricing` (unitario a 2 decimales, `AwayFromZero`; IVA a 2 decimales). Sin valor CPI (`VALUE_THRESHOLD`, `UNLOADED_OR_ON_VEHICLE` con descargados), el error de hoy de las fórmulas de porcentaje, que `DEC-020` convierte en mínimo con advertencia | AF-116, AF-120; D1, D2, D9, D12, D13, D20 |
| D31 | **Contexto de la fórmula.** `FormulaContext` suma `Trucks` (lista de camiones del depósito con su precio, en la moneda del depósito, y su marca; D9, D11) y `RateIncludesVat` (D20). `StorageBillingService` llena `Trucks` con las entradas no anuladas (`WarehouseStorageEntry.MerchandiseValue`, la marca de D33); `VehicleCount` sigue siendo el número de entradas, el peso el de mercancía (`P01/` D41), y `Quantity` y `BaseQuantity` los del % prorrateado | D9, D11, D13; `P01/` D41, D42 |
| D32 | **Advertencias en el detalle de la factura** (`DEC-020`), en singular con un camión: «{n} camiones descargados sin precio: cuentan $0 en el cobro por camión.» («1 camión descargado sin precio: cuenta $0 en el cobro por camión.») (D9); «{n} camiones sin recepción se cobraron como descargados.» («1 camión sin recepción se cobró como descargado.») (D10); y la de hoy, «{n} camiones sin peso de mercancía», también para las fórmulas por peso nuevas (`P01/` D41) | `DEC-020`; D9, D10 |
| D33 | **La marca en la entrada** (D11). Migración: `WarehouseStorageEntry.StaysOnVehicle` (booleano, falso) y sale `ReceptionLog.StaysOnVehicle`. La recepción (C-F04-07, C-F07-36) escribe la marca de la entrada y sigue ubicando en `SOBRE-VEHICULO` cuando la recibe así (`P04/` D4); el detalle de la recepción (C-F04-10) la lee de la entrada. CE la cambia con C-F07-33 (`ForeignTradeAccess`), en entradas no anuladas de depósitos en Borrador o Confirmado (los estados que edita CE, `P05/` D18); no mueve inventario ni ubicaciones. La lista de Recepción la trae precargada (C-F07-35) y las entradas del depósito la muestran con `canMarkStaysOnVehicle` (C-F07-34) | D11; `P04/` D4; `P05/` D18 |
| D34 | **Recálculo por la marca** (D10). Después del commit de C-F07-33, o de una recepción que cambia la marca de la entrada, si el depósito tiene un período abierto cuyo cargo usa `UNLOADED_OR_ON_VEHICLE`, se recalcula con `StorageRecalculationTrigger.RecalculateAfterCorrectionAsync`, el mismo mecanismo de `P05/` D19 (`DEC-022`: en Borrador se recalcula; aprobada o con pagos se actualiza la misma factura y se avisa a Facturación; anulada no se toca) | D10; `DEC-022`; `P05/` D19 |
| D35 | **Simulador por fórmula** (AF-118, H-063). `GET FormulaType` (C-F07-31) trae `simulatorInputs`, la lista de datos que usa cada fórmula (`FormulaSimulatorInputs`, en código), y P-FAC-13 pide solo esos. `POST billing/formula-preview` (C-F07-32) recibe `trucks`, cambia `grossWeightKg` por `merchandiseWeightKg` (`P01/` fase 6 dejó el nombre viejo) y devuelve las advertencias de D32. La explicación dice de dónde salió el importe, como hoy | AF-118; `A/` P-FAC-13 |
| D36 | **Rótulo de `thresholdKg`** de «Por umbral de peso»: «Umbral de peso de mercancía (kg)», en la migración de BE-3 (`P01/` §8, nota de la fase 6) | `P01/` fase 6; AF-113 |

### 1.5 Plantilla e importación (BE-4)

| # | Decisión | Fuente |
| --- | --- | --- |
| D37 | **ClosedXML en `Wms.Application`** (como QuestPDF, `B/Wms.Application/Wms.Application.csproj`), con `dotnet add package ClosedXML` en su versión estable al ejecutar BE-4; el agente anota la versión en el reporte. El armado y la lectura van en clases propias (`AgreementTemplateWorkbook` y `AgreementTemplateReader`), con la validación de filas en una regla pura (`AgreementImportRules`) | D6 |
| D38 | **Formato del archivo.** Hojas: «Instrucciones» (cómo llenar, reglas y ejemplos ficticios), «Clientes», «Facturar a», «Retenciones», «Tarifas» y «Catálogos» (servicios con su IVA, modalidades, fórmulas con sus parámetros, rótulos, obligatoriedad y valores permitidos, tipos de unidad de carga y ciclos). En las hojas de datos, la fila 1 lleva el rótulo en español, la fila 2 la clave técnica (gris, protegida) y los datos empiezan en la fila 3; el lector usa la fila 2. Las columnas están en §2.2, C-F07-37. Listas desplegables para Sí/No, servicio, modalidad, fórmula, ciclo y retención. Números con coma o punto decimal; una celda con formato de porcentaje se lee como el número que muestra (0,3 % → 0,3); fechas como fecha de Excel o texto `dd/mm/aaaa` | AF-114; `A/` §2.4 f («Plantilla de acuerdos») |
| D39 | **Descarga y carga.** C-F07-37 da la plantilla vacía (con catálogos) o, con `customerId`, la de un cliente con su configuración, sus excepciones, las retenciones suyas y de sus «Facturar a», y sus tarifas vigentes y programadas. C-F07-38 (vista previa) y C-F07-39 (confirmar) reciben el mismo archivo (multipart, campo `file`): la confirmación vuelve a leer y validar todo, sin estado guardado entre las dos. Límites: `.xlsx`, hasta 5 MB y 2.000 filas de datos entre las tres hojas | D6; AF-114 («nada se guarda hasta confirmar») |
| D40 | **Qué hace cada fila.** «Clientes»: crea o actualiza la configuración (ciclo por días: 7, 14, 15, 30, 90, 180 y 360 son los del catálogo; cualquier otro N de 1 a 360 es «Otro»). «Facturar a»: crea o actualiza la excepción del importador (no borra las que no vienen; se quitan en P-FAC-11). «Retenciones»: crea o actualiza la retención del tercero (D52, D53; tampoco borra las que no vienen). «Tarifas»: por ámbito y «vigente desde», crea (`New` «Nueva», o `NewScheduled` «Nueva, programada» si empieza después de hoy), reemplaza (`Replaces` «Reemplaza desde {fecha}», con la línea de tiempo de D23), actualiza la del mismo día (`Updates` «Actualiza la del {fecha}»), o no cambia nada (`Unchanged` «Sin cambios»). Una fila con error (`Error`) no se carga y no frena las demás (AF-114). Dos filas del archivo con la misma clave: error en la segunda. Se aplican en una sola transacción, en el orden Clientes, Facturar a, Retenciones, Tarifas; volver a confirmar el mismo archivo da todo «Sin cambios» | AF-114; D23 |
| D41 | **Llaves de cada columna.** Retención por su rótulo o su valor (`Retefuente`, `ReteIca`, `ReteIva`). Terceros por NIT (sin dígito de verificación, sin puntos); un NIT que no existe es error: el tercero se crea antes en Configuración (AF-114). Servicio por código, modalidad por código o nombre, fórmula por código, tipo de unidad de carga por código. Producto por SKU o por nombre, sin distinguir mayúsculas ni tildes; un nombre que coincide con varios productos es error («use el SKU») | AF-114 |

### 1.6 Pantallas y componentes (FE)

| # | Decisión | Fuente |
| --- | --- | --- |
| D42 | **Menú y patrón.** «Tarifas y acuerdos» (Admin, Billing; `P02/` §1.5) queda con Acuerdos (`/rates/agreements`), Configuración de facturación (`/billing/configurations`), Tarifas de servicios (`/rates/services`) y Tarifas de montacargas (`/admin/forklift-rates`), en ese orden (`A/` §3.2). Las cuatro son listados con el patrón de AF-129 (`AppDataTable`, sin `AppPageHeader`): pasan a `PATTERN` en `FT/unit/guards/list-pattern-routes.ts` y `F07` sale de `PENDING_FEATURES`. `/billing/configurations/[customerId]` y `/rates/agreements/import` siguen «Páginas que no son listados» (sin tarjeta, `<h1 class="sr-only">`, acciones en una barra arriba a la derecha); `/rates/agreements/[customerId]` es un listado de tarifas, sin tarjeta de título, con el cliente en el breadcrumb. I-07 enlaza el menú | D7; AF-127, AF-129; `D/contexto/convenciones-tecnicas.md` §3 |
| D43 | **P-FAC-11.** Listado `/billing/configurations` (rediseño en su ruta, M11): Cliente ↕, NIT, Ciclo ↕, Días de pago ↕, Límite de crédito ↕, Preferencia, Facturar a, Excepciones, Retenciones (las del cliente, p. ej. «Retefuente 2,5 % · ReteICA 0,966 %»), Acciones (✎ y «Ver acuerdo»), con filtros por columna (cliente, NIT, ciclo, preferencia, Facturar a) y orden en el servidor (C-F07-01); «+ Nueva configuración» abre un modal chico con el cliente (`AppSearchSelect`) y lleva a la página. Página `/billing/configurations/[customerId]`: ciclo (con «Días del ciclo» visible solo con «Otro»), días de pago, límite de crédito y preferencia («Por servicio» o «Consolidada»; las retiradas solo se leen); «Facturar a (general)» con `AppSearchSelect` y «+» de alta rápida (C-F01-141); «Excepciones por importador» como tabla (Importador, Facturar a, Acciones ✎ 🗑) con «+ Agregar» en un modal de dos selectores. «Retenciones que practica» (D52, D53): tabla del cliente (Retención con el selector de C-F07-54, Porcentaje, Base «Subtotal» o «IVA» que da el tipo, Acciones ✎ 🗑) con «+ Agregar». Junto a cada «Facturar a» (el general y el de cada excepción) van sus retenciones en texto atenuado y la acción «Retenciones» (icono `pi pi-percentage`, tooltip), que abre un modal con la misma tabla para ese tercero y guarda al momento (C-F07-56). «Volver» y «Guardar» en la barra: «Guardar» envía C-F07-03 y las retenciones del cliente (C-F07-56); un cliente sin configuración abre el formulario vacío (C-F07-02 responde 404) | AF-108, AF-115, AF-123; P-FAC-11; D52, D53 |
| D44 | **P-FAC-12.** `/rates/agreements`: Cliente ↕, NIT ↕, Vigentes ↕, Programadas ↕, Último «vigente desde» ↕, Acciones (Ver); barra con «+ Nuevo acuerdo» (modal del cliente que lleva a su página), «Descargar plantilla» (vacía) e «Importar plantilla». `/rates/agreements/[customerId]`: una fila por tarifa con Servicio, Producto, Perecedero, Modalidad, Fórmula, Parámetros (resumen, p. ej. «0,3 % · mín. $ 257.600»), Papelería, IVA incluido, Vigencia («desde – hasta» con la etiqueta del estado) y Acciones (✎ y 🗑 «Retirar», que se ocultan en una terminada); filtros por columna en producto, perecedero, modalidad, servicio y fórmula, más una tarjeta de filtro global «Estado» (por omisión vigentes y programadas); barra con «Descargar plantilla» (del cliente), «Importar plantilla» y «+ Agregar tarifa». La columna «Importador» que nombra el texto de P-FAC-12 en `A/` §2.4 g no va: AF-125 la quitó y el wireframe no la dibuja (`DEC-002`) | AF-114, AF-118, AF-125; P-FAC-12 |
| D45 | **P-FAC-13 «Agregar tarifa»** (componente `TariffDialog`, sobre `AppCrudDialog` a dos columnas): servicio, producto (`AppSearchSelect`, «Todos» = vacío), perecedero (Todos, Sí, No), modalidad (Todas o una), fórmula (solo las de su `serviceScope`), papelería, IVA incluido y «Vigente desde» (solo en modo acuerdo); «Parámetros de {fórmula}» con solo los de la fórmula elegida, sus rótulos y sus condicionales (`visibleWhen`); el simulador (`FormulaSimulator`) con solo los datos de `simulatorInputs` y «Calcular», que muestra el resultado, el IVA, el total y las advertencias (C-F07-32). El mismo diálogo sirve en modo «tarifa base» para Tarifas de servicios (D26) | AF-118, H-063; P-FAC-13; `PAJ/` D2 |
| D46 | **P-FAC-14 «Importar plantilla»** (`/rates/agreements/import`): pasos «1 Cargar archivo», «2 Vista previa» y «3 Confirmar»; zona para soltar el archivo (como Ciudades, `PAJ/` D13) y «Descargar plantilla vacía»; la vista previa en una tabla con Hoja, Fila, Cliente (NIT), Producto, Servicio, Fórmula, Vigente desde y Resultado (etiqueta: verde nueva, azul programada o actualiza, gris sin cambios, rojo error con su mensaje), con filtro por resultado; pie con «{n} filas válidas · {m} con error (no se cargan)», «Cancelar» y «Confirmar importación»; el paso 3 muestra lo aplicado (C-F07-39) | AF-114; P-FAC-14 |
| D47 | **Tarifas de servicios** (`/rates/services`): Código ↕, Servicio ↕, IVA (%), Precio base vigente, Estado y Acciones (Ver), con filtros de código, nombre y estado (C-F07-08). Drawer `lg` (`AppDetailDrawer`) con las secciones «Precio base e IVA» (IVA del servicio y la lista de precios con su vigencia; «+ Nuevo precio» abre un modal con precio, IVA (%) precargado con el del servicio, «Precio + IVA» calculado, vigente desde y hasta, como el legacy), «Tarifas por fórmula» (las reglas con el diálogo de D45 en modo base, activar y desactivar) y «Mínimos por modalidad» (✎ en modal). El menú «Acciones» lleva «Editar IVA» (C-F07-09) | D3, D26; AF-129; `PAJ/` D2 |
| D48 | **Tarifas de montacargas** (`/admin/forklift-rates`): tabla en modo `client` con Tipo de vehículo ↕, Tarifa ↕, Actualizada y Acciones (✎ en modal, C-F07-52); al pie de la barra, en texto atenuado, «Con «Requiere factura» se suma el IVA del servicio Montacargas: {n} %». Reemplaza `F/features/forklift-rates/components/ForkliftRatesGrid.vue` | AF-129; `P04/` D2 |
| D49 | **Detalles del tercero y del servicio** (I-07, D7). El drawer del tercero pierde la sección «Acuerdos» (`F/features/stakeholders/components/StakeholderDetailSections.vue:264-311`) y el del servicio la de «Tarifas» (`F/features/services/components/ServiceRateSections.vue`); su menú «Acciones» gana «Ver acuerdo» (a `/rates/agreements/{id}`, solo si el tercero es cliente) y «Ver tarifas» (a `/rates/services?id={id}`), solo para Admin y Facturación | D7; `PAJ/` D1 |
| D50 | **La marca en las pantallas de CE y Bodega va en I-07.** La etapa Bodega del detalle del depósito (`F/features/foreign-trade/components/DepositWarehouseStage.vue:98`) cambia el texto «Queda sobre el vehículo» por un switch por entrada (visible con `canMarkStaysOnVehicle` y para Admin y CE; C-F07-33), y el modal de recepción de Bodega (P-BOD-02) trae el switch precargado (C-F07-35). Son pantallas ya integradas que llaman al API real, así que no se maquetan con datos simulados: las cambia I-07 (§13.1) | D11; `P05/` D16; `P04/` D4 |
| D51 | **Dominio y datos simulados** (M12, `P02/` D10). Lo nuevo va en `F/features/rates/` (`contracts/`, `services/*.source.ts`, `mocks/`, `components/`, `composables/`, `utils/`). La maquetación usa la sesión simulada (`NUXT_PUBLIC_MOCK_SESSION=true`, `?roles=Admin,Billing`), porque el backend lo ocupa el otro agente. Las descargas simuladas devuelven un `Blob` ficticio; la importación simulada devuelve resultados fijos que cubren los seis `outcome` | M12; `P02/` D10 |

### 1.7 Permisos por endpoint (`B/Wms.Domain/Security/WmsPolicyRoles.cs`; `PM/` §5.6, `DEC-005`)

Ninguna política nueva: `BillingAccess` (Admin, Billing), `ForeignTradeAccess` (Admin, ForeignTrade) y `WarehouseAccess` (Admin, Warehouse) ya existen.

| Endpoints | Política | Quién lo usa |
| --- | --- | --- |
| C-F07-01 a C-F07-07 | `BillingAccess` (la de hoy, `B/Wms.Api/Controllers/v1/BillingController.cs:54`) | Admin y Facturación (P-FAC-11; F08) |
| C-F07-08 | la de hoy (C-F01-37, C-F01-38) | Configuración › Servicios y Tarifas de servicios |
| C-F07-09, C-F07-10 | `BillingAccess` | Tarifas de servicios |
| C-F07-54 a C-F07-56 | `BillingAccess` | P-FAC-11 (retenciones); F08 («Facturar») |
| C-F07-14 a C-F07-18, C-F07-37 a C-F07-39 | `BillingAccess` (controlador nuevo) | Acuerdos y plantilla |
| C-F07-31 | la de hoy (`[Authorize]`, `B/Wms.Api/Controllers/v1/FormulaTypeController.cs:14`) | P-FAC-13 |
| C-F07-32 | la de hoy (`ActiveUser`, `B/Wms.Api/Controllers/v1/BillingPreviewController.cs:22`) | Simulador |
| C-F07-33, C-F07-34 | `ForeignTradeAccess` | Etapa Bodega del detalle de CE |
| C-F07-35, C-F07-36 | `WarehouseAccess` (la de hoy) | Recepción de Bodega |
| C-F07-43 a C-F07-52 | las de hoy (escrituras con `BillingAccess`) | Tarifas de servicios y de montacargas |
| C-F07-11 a C-F07-13, C-F07-19 a C-F07-30 | retirados (404) | Nadie fuera de las secciones que borra I-07 (D28) |

### 1.8 Destino de las 10 AF dueñas

| AF | Qué pide | Decisiones | Fases |
| --- | --- | --- | --- |
| AF-108 | Ciclo libre en días | D14 | BE-1, FE-1, I-07 |
| AF-112 | «Facturar a» que se precarga; mora al cliente del depósito | D15, D16, D17, D18 | BE-1, FE-1, I-07 |
| AF-114 | Carga inicial, formulario nuevo y plantilla descargable e importable | D4, D5, D6, D23, D37 a D41, D44, D46 | BE-2, BE-4, FE-2, FE-3, I-07, T-1 |
| AF-115 | Sin mes calendario; «Mensual» de 30 días; fin = inicio + N | D14 | BE-1, FE-1 |
| AF-116 | Las cuatro fórmulas nuevas | D1, D2, D9, D12, D13, D20, D27, D29, D30, D31 | BE-3, FE-2 |
| AF-117 | Tanquero y contenedor con `PER_CARGO_UNIT`; «+ báscula» en $0; caja con `PER_UOM`; papelería complementaria | D25 (papelería), D24 (báscula en $0); casos QA2-F07-035 y QA2-F07-043 | BE-2, BE-3, I-07 |
| AF-118 | Formulario de una fila por tarifa y simulador por fórmula | D35, D44, D45 | BE-3, FE-2 |
| AF-120 | Depósito mixto: por camión, % de los descargados y tarifa por vehículo | D2, D9, D10, D11, D30, D33, D34 | BE-3, I-07 |
| AF-123 | «Facturar a» por cliente e importador | D15, D16 | BE-1, FE-1 |
| AF-125 | Sin importador como dimensión de la tarifa | D23 (ámbito sin importador), D44 | BE-2, FE-2 |

Las 10 tienen decisión y fase.

### 1.9 AF de otras features que F07 usa o aplica

| AF | Dueña | Qué usa F07 |
| --- | --- | --- |
| AF-22 | F01 | `PER_UOM` por embalaje (C-F01-77, `P01/` D19): «por caja» del Excel (AF-117) |
| AF-27 | F01 | Unidades de carga que registra CE: `PER_CARGO_UNIT` y «Según el valor» por unidad de carga |
| AF-85 | F01 | Tasa de la semana de ingreso: el valor CPI en pesos (`P01/` D42) |
| AF-94 | F01 | Precio por camión (`WarehouseStorageEntry.MerchandiseValue`) y valor CPI: reparto de D9 |
| AF-113 | F01 | Peso de mercancía del depósito en las fórmulas por peso (`P01/` D41) |
| AF-119 | F04 | Marca «Queda sobre el vehículo» de la recepción (`P04/` D4), que D11 lleva a la entrada |
| AF-105 | F04 | IVA del montacargas con «Requiere factura» (`P04/` D2), que D19 toma del servicio |
| AF-75, AF-76 | F05 | Apertura tardía y recálculo al editar en Confirmado (`P05/` D17, D19): F07 no los rehace y usa el mismo mecanismo en D34 |
| AF-99, AF-129 | F02 | Filtros por columna, orden y botones con borde en las seis pantallas (D42 a D48) |
| AF-127 | F02 | Menú «Tarifas y acuerdos» para Admin y Facturación (D42) |

---

## 2. Contrato (parte 0)

Es la única fuente del frontend para lo que F07 crea, cambia o retira (`PM/` R3). Los endpoints de F01 a F05 que F07 consume sin cambios se citan por su ID; sus fichas están en su plan.

### 2.0 Convenciones

Rigen `D/planes/paridad-legacy/contrato-api-paridad.md` §0 y C-F01-00 (`P01/` §2.0): base `/api/v1`, JSON en camelCase, enums como texto, `DateOnly` como `yyyy-MM-dd` (día de Colombia), respuesta `{ data, pagination }`, `pageSize` de 1 a 50 con `all=true`, orden con `sortField` (lista blanca) y `sortOrder`, filtros por columna (texto: contiene, sin mayúsculas ni tildes; enums separados por coma), errores *ProblemDetails* con `description` y `errors[]`. Mensajes de error de C-F01-00 sin cambios («No se puede ordenar por «{campo}».», etc.). IDs: `C-F07-mm` y `QA2-F07-nnn`.

**Fichas de otras features que F07 consume sin cambios, comprobadas contra `fase-2` (`348ab15`, `3531432`):** C-F01-25 y C-F01-26 (terceros), C-F01-141 (alta rápida), C-F01-33 (tipos de unidad de carga), C-F01-69 (productos) y C-F01-77 (`GET FormulaType`: `PER_UOM` con el rótulo «Por cantidad (embalaje)» y sin `uom`, `B/Wms.Infrastructure/Persistence/SeedDataExtensions.cs:406-417`, coincide). C-F01-77 cambia en F07 (C-F07-31); C-F04-06, C-F04-07, C-F04-10 y C-F05-22 también (C-F07-34 a C-F07-36).

### 2.1 Índice

| ID | Endpoint | Cambio | Política | Consume | Fase |
| --- | --- | --- | --- | --- | --- |
| **A · Configuración de facturación y «Facturar a»** |  |  |  |  |  |
| C-F07-01 | `GET billing/configurations` | modificado: ciclo libre, «Facturar a», retenciones, orden y filtros | `BillingAccess` | P-FAC-11 (listado) | BE-1 |
| C-F07-02 | `GET billing/configurations/{stakeholderId}` | modificado: ciclo libre, «Facturar a», excepciones y retenciones | `BillingAccess` | P-FAC-11 (página); **F08** («Facturar» precarga el destinatario) | BE-1 |
| C-F07-03 | `PUT billing/configurations/{stakeholderId}` | modificado: `cycleDays`, «Facturar a» y excepciones | `BillingAccess` | P-FAC-11 | BE-1 |
| C-F07-04 | `GET billing/configurations/cycles` | modificado: sin mes calendario, con «Otro» | `BillingAccess` | P-FAC-11 | BE-1 |
| C-F07-05 | `GET billing/invoices/{id}/recipient-candidates` | modificado: suma los «Facturar a» | `BillingAccess` | **F08** («Cambiar destinatario», «Facturar») | BE-1 |
| C-F07-06 | `PATCH billing/invoices/{id}/recipient` | modificado: regla (acepta el «Facturar a») | `BillingAccess` | **F08** | BE-1 |
| C-F07-07 | `GET billing/invoices` y `GET billing/invoices/{id}` | modificado: cliente del depósito | `BillingAccess` | **F08** (P-FAC-02 Almacenamiento: «cliente» y «Facturar a») | BE-1 |
| **B · IVA del servicio** |  |  |  |  |  |
| C-F07-08 | `GET service` y `GET service/{id}` | modificado (sobre C-F01-37 y C-F01-38): `vatPercent`, sin `taxes`; la lista trae `currentPrice` | la de hoy | Tarifas de servicios; Configuración › Servicios | BE-1 |
| C-F07-09 | `PATCH service/{id}/vat` | nuevo | `BillingAccess` | Tarifas de servicios | BE-1 |
| C-F07-10 | `POST service/{id}/prices` | modificado: `vatPercent` opcional | `BillingAccess` | Tarifas de servicios | BE-1 |
| C-F07-11 | `GET administration/taxes` | retirado | — | — | BE-1 |
| C-F07-12 | `POST service/{id}/assign-tax` | retirado | — | — | BE-1 |
| C-F07-13 | `POST service/{id}/remove-tax` | retirado | — | — | BE-1 |
| **C · Acuerdos** |  |  |  |  |  |
| C-F07-14 | `GET rates/agreements` | nuevo | `BillingAccess` | Acuerdos (listado) | BE-2 |
| C-F07-15 | `GET rates/agreements/{customerId}/tariffs` | nuevo | `BillingAccess` | P-FAC-12 | BE-2 |
| C-F07-16 | `POST rates/agreements/{customerId}/tariffs` | nuevo | `BillingAccess` | P-FAC-13 | BE-2 |
| C-F07-17 | `PUT rates/agreements/{customerId}/tariffs/{tariffId}` | nuevo | `BillingAccess` | P-FAC-13 (editar) | BE-2 |
| C-F07-18 | `DELETE rates/agreements/{customerId}/tariffs/{tariffId}` | nuevo: retirar | `BillingAccess` | P-FAC-12 | BE-2 |
| C-F07-19 a C-F07-30 | `stakeholder/{stakeholderId}/agreement…` (12 endpoints) | retirados | — | — | BE-2 |
| **D · Fórmulas, simulador y marca «Queda sobre el vehículo»** |  |  |  |  |  |
| C-F07-31 | `GET FormulaType` | modificado (sobre C-F01-77): cuatro fórmulas, `simulatorInputs`, `serviceScope`, `enumLabels`, `visibleWhen` | la de hoy | P-FAC-13; Tarifas de servicios | BE-3 |
| C-F07-32 | `POST billing/formula-preview` | modificado: `trucks`, `merchandiseWeightKg`, advertencias | la de hoy (`ActiveUser`) | Simulador de P-FAC-13 | BE-3 |
| C-F07-33 | `PATCH foreign-trade/warehouse-storages/{warehouseStorageId}/entries/{entryId}/stays-on-vehicle` | nuevo | `ForeignTradeAccess` | Etapa Bodega del detalle de CE (I-07) | BE-3 |
| C-F07-34 | `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` | modificado (sobre C-F05-22): `staysOnVehicle` y `canMarkStaysOnVehicle` por entrada | `ForeignTradeAccess` | Etapa Bodega (I-07) | BE-3 |
| C-F07-35 | `GET warehouse/pending-from-weighbridge` | modificado (sobre C-F04-06): `staysOnVehicle` precargado | `WarehouseAccess` | Recepción, P-BOD-02 (I-07) | BE-3 |
| C-F07-36 | `POST warehouse/receptions` | modificado (sobre C-F04-07): regla (marca en la entrada y recálculo); forma igual | `WarehouseAccess` | Recepción | BE-3 |
| **E · Plantilla** |  |  |  |  |  |
| C-F07-37 | `GET rates/agreements/template` | nuevo | `BillingAccess` | Acuerdos, P-FAC-12, P-FAC-14 | BE-4 |
| C-F07-38 | `POST rates/agreements/import/preview` | nuevo | `BillingAccess` | P-FAC-14 | BE-4 |
| C-F07-39 | `POST rates/agreements/import` | nuevo | `BillingAccess` | P-FAC-14 | BE-4 |
| **F · De hoy, sin cambios de forma (los maqueta F07)** |  |  |  |  |  |
| C-F07-40 | `GET service/{id}/prices` | sin cambios | la de hoy | Tarifas de servicios | — |
| C-F07-41 | `PATCH service/{id}/prices/{priceId}` | sin cambios | `BillingAccess` | Tarifas de servicios | — |
| C-F07-42 | `DELETE service/{id}/prices/{priceId}` | sin cambios | `BillingAccess` | Tarifas de servicios | — |
| C-F07-43 | `GET service/{id}/pricing-rules` | sin cambios | la de hoy | Tarifas de servicios | — |
| C-F07-44 | `POST service/{id}/pricing-rules` | modificado: regla (D27) | `BillingAccess` | Tarifas de servicios | BE-2 |
| C-F07-45 | `PUT service/{id}/pricing-rules/{ruleId}` | modificado: regla (D27) | `BillingAccess` | Tarifas de servicios | BE-2 |
| C-F07-46 | `DELETE service/{id}/pricing-rules/{ruleId}` | sin cambios | `BillingAccess` | Tarifas de servicios | — |
| C-F07-47 | `PATCH service/{id}/pricing-rules/{ruleId}/activate` y `/deactivate` | sin cambios | `BillingAccess` | Tarifas de servicios | — |
| C-F07-48 | `GET service/{id}/minimum-values` | sin cambios | la de hoy | Tarifas de servicios | — |
| C-F07-49 | `PUT service/{id}/minimum-values/{minimumValueId}` | sin cambios | `BillingAccess` | Tarifas de servicios | — |
| C-F07-50 | `GET forklift-rates/vehicle-types` | sin cambios | autenticado | Tarifas de montacargas | — |
| C-F07-51 | `GET forklift-rates` | sin cambios | `BillingAccess` | Tarifas de montacargas | — |
| C-F07-52 | `PUT forklift-rates/{vehicleType}` | sin cambios | `BillingAccess` | Tarifas de montacargas | — |
| C-F07-53 | `GET administration/operation-modalities` | sin cambios | autenticado | P-FAC-11 a P-FAC-13 | — |
| **G · Retenciones del tercero que paga** |  |  |  |  |  |
| C-F07-54 | `GET billing/withholdings/types` | nuevo | `BillingAccess` | P-FAC-11 (selector); **F08** | BE-1 |
| C-F07-55 | `GET billing/withholdings/{stakeholderId}` | nuevo | `BillingAccess` | P-FAC-11; **F08** («Facturar»: retenciones del destinatario) | BE-1 |
| C-F07-56 | `PUT billing/withholdings/{stakeholderId}` | nuevo | `BillingAccess` | P-FAC-11 | BE-1 |

### 2.2 Fichas

#### Grupo A — Configuración de facturación y «Facturar a» (BE-1)

##### C-F07-01 · `GET billing/configurations` (modificado)
- **Política:** `BillingAccess`. **Qué cambia:** cada fila trae el NIT, `cycleDays`, `billingCycleLabel`, el «Facturar a», el número de excepciones y las retenciones del cliente (D52); orden y filtros de C-F01-00.
- **Filtros:** `stakeholderName` (de hoy), `stakeholderIdNumber`, `billingCycle` (enum, coma), `invoicingPreference` (enum, coma), `billToName`, `isActive` (de hoy). **Orden:** lista blanca `stakeholderName`, `stakeholderIdNumber`, `billingCycle`, `paymentTermDays`, `creditLimit`, `updatedAt`; por defecto `stakeholderName` asc. **Paginación:** la de hoy.
- **Respuesta 200:** `pagedSchema(billingConfigurationSchema)`:

```jsonc
{ "data": [{
  "id": "…", "stakeholderId": "…", "stakeholderName": "Cliente A", "stakeholderIdNumber": "900000001",
  "billingCycle": "Custom", "cycleDays": 20, "billingCycleLabel": "Otro: 20 días",
  "paymentTermDays": 30, "creditLimit": 5000000, "invoicingPreference": "PerService",
  "billTo": { "id": "…", "name": "Cliente A", "idNumber": "900000001" },
  "billToExceptionsCount": 2,
  "withholdings": [{ "type": "Retefuente", "percent": 2.5 }, { "type": "ReteIca", "percent": 0.966 }],
  "isActive": true, "createdAt": "…", "updatedAt": null
}], "pagination": { "pageIndex": 1, "pageSize": 10, "totalCount": 1, "totalPages": 1 } }
```

- **Errores:** los de C-F01-00.

##### C-F07-02 · `GET billing/configurations/{stakeholderId}` (modificado)
- **Política:** `BillingAccess`. **Qué cambia:** trae los campos de C-F07-01 y la lista `billToExceptions`; cada «Facturar a» (el general y el de cada excepción) trae sus propias `withholdings` (D52), para mostrarlas en su fila.
- **Respuesta 200:** `dataSchema(billingConfigurationDetailSchema)`: lo de C-F07-01 (con `billTo` como `billToRefSchema`) más `"billToExceptions": [{ "id": "…", "importer": { "id": "…", "name": "Importador X SAS", "idNumber": "900000010" }, "billTo": { "id": "…", "name": "Comercial Z SAS", "idNumber": "900000020", "withholdings": [{ "type": "ReteIva", "percent": 15 }] } }]`.
- **Errores:** 404 con el mensaje de hoy si el cliente no tiene configuración (la página lo toma como formulario vacío).
- **Para F08:** el «Facturar a» de un depósito sale de `BillToResolver` (D15) y ya viene en el destinatario de la factura de almacenamiento (`Invoice.CustomerId`, D16); F08 lo precarga desde la factura, no desde aquí. Las retenciones del destinatario las lee de C-F07-55 (D52, D54).

##### C-F07-03 · `PUT billing/configurations/{stakeholderId}` (modificado)
- **Política:** `BillingAccess`. **Qué cambia:** acepta `cycleDays`, `billToStakeholderId` y la lista completa `billToExceptions`, que reemplaza la guardada.

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `billingCycle` | enum | sí | Los de C-F07-04 (`Monthly` y `OnDemand` no se aceptan) |
| `cycleDays` | entero o nulo | con `Custom` | 1 a 360 con `Custom`; nulo con los demás |
| `paymentTermDays` | entero | sí | ≥ 0 |
| `invoicingPreference` | enum | sí | `PerService` o `Consolidated` (como hoy) |
| `creditLimit` | número o nulo | no | ≥ 0; nulo quita el límite |
| `billToStakeholderId` | Guid o nulo | no | Tercero activo; nulo = el mismo cliente |
| `billToExceptions` | lista | sí (puede ir vacía) | `{ importerId, billToStakeholderId }`; importador con el rol Importador, sin repetir |

- **Respuesta 200:** la de C-F07-02. **Zod:** `billingConfigurationUpsertSchema` (petición) y `billingConfigurationDetailResponseSchema` (respuesta).
- **Errores (400):** «El ciclo de facturación no es válido.» (de hoy); «Digite los días del ciclo, de 1 a 360.»; «Los días del ciclo solo aplican al ciclo «Otro».»; «Los días de plazo de pago no pueden ser negativos.» (de hoy); «El límite de crédito no puede ser negativo.» (de hoy); «La preferencia de facturación no es válida.» (de hoy); «El importador {nombre} está repetido en las excepciones.»; «El tercero {nombre} no tiene el rol Importador.»; «El tercero {nombre} está inactivo.». **404:** «No existe el tercero {id}.» (cliente, importador o «Facturar a»).

##### C-F07-04 · `GET billing/configurations/cycles` (modificado)
- **Política:** `BillingAccess`. **Respuesta 200:** `dataSchema(z.array(billingCycleOptionSchema))`, en este orden: `Weekly` «Semanal (7)» 7, `Biweekly` «Quincenal (14)» 14, `Days15` «Quincenal (15)» 15, `Days30` «Mensual (30)» 30, `Days90` «Trimestral (90)» 90, `Days180` «Semestral (180)» 180, `Days360` «Anual (360)» 360, `Custom` «Otro: N días» `null`. Sin `Monthly`. **Petición:** sin parámetros. **Errores:** ninguno propio (401 y 403 de la política). **Zod:** `billingCyclesResponseSchema`.

##### C-F07-05 · `GET billing/invoices/{id}/recipient-candidates` (modificado)
- **Política:** `BillingAccess`. **Qué cambia:** cada candidato trae `billTo` (nulo si no es un «Facturar a» configurado del cliente del depósito) y la lista suma esos «Facturar a» aunque no sean terceros del depósito.
- **Respuesta 200:** `dataSchema(z.array(invoiceRecipientCandidateSchema))`: `{ "stakeholderId", "name", "idNumber", "roles": [{ "code", "name" }], "billTo": { "scope": "General" | "Importer", "importerName": "Importador X SAS" | null } | null }`. **Errores:** los de hoy.

##### C-F07-06 · `PATCH billing/invoices/{id}/recipient` (modificado: regla)
- **Política:** `BillingAccess`. **Qué cambia:** acepta como destinatario un «Facturar a» configurado del cliente del depósito (D17). Petición, respuesta y errores, los de hoy (`B/Wms.Api/Controllers/v1/BillingController.cs:175-190`; «Solo se puede reasignar el destinatario de una factura en borrador.», «El tercero no está relacionado con la factura ni es cliente.»). **Zod:** sin cambio de forma; F08 escribe el de su diálogo sobre la petición de hoy (`UpdateInvoiceRecipientRequest`: `customerId` o `unregisteredRecipient`).

##### C-F07-07 · `GET billing/invoices` y `GET billing/invoices/{id}` (modificado)
- **Política:** `BillingAccess`. **Qué cambia:** cada factura trae `depositCustomerId` y `depositCustomerName` (el cliente del depósito en las de almacenamiento; nulos en las demás). El destinatario sigue en los campos de hoy. **Petición, filtros y errores:** los de hoy. **Respuesta 200:** la de hoy, más los dos campos (`invoiceDepositCustomerFieldsSchema`). F07 escribe solo el fragmento `invoiceDepositCustomerFieldsSchema`; F08 lo suma a sus esquemas de facturas.

#### Grupo B — IVA del servicio (BE-1)

##### C-F07-08 · `GET service` y `GET service/{id}` (modificado sobre C-F01-37 y C-F01-38)
- **Política:** la de hoy. **Qué cambia:** `vatPercent` (número, 0 a 100) en la lista y en el detalle; sale `taxes`; la lista trae `currentPrice` (el precio vigente hoy o nulo). **Petición:** filtros y orden de C-F01-37, sin cambios. **Respuesta 200:** `pagedSchema(serviceSchema)` y `dataSchema(serviceSchema)`. **Errores:** los de hoy. **Zod:** `serviceSchema` (cambia en `F/features/services/contracts/service.ts`).

##### C-F07-09 · `PATCH service/{id}/vat` (nuevo)
- **Política:** `BillingAccess`. **Petición:** `{ "vatPercent": 19 }` (número de 0 a 100, hasta 2 decimales). **Respuesta 200:** `dataSchema(serviceSchema)`. **Errores:** 400 «El IVA debe estar entre 0 y 100 %.»; 404 con el mensaje de hoy del servicio.

##### C-F07-10 · `POST service/{id}/prices` (modificado)
- **Política:** `BillingAccess`. **Qué cambia:** acepta `vatPercent` (opcional, 0 a 100): si viene, actualiza el IVA del servicio en la misma transacción. **Petición:** `servicePriceCreateSchema` (`basePrice`, `validFrom` y `validTo` de hoy, `B/Wms.Application/Services/Common/Dtos/SetServicePriceRequest.cs`, más `vatPercent`). **Respuesta:** la de hoy (`dataSchema(servicePriceSchema)`). **Errores:** los de hoy, más 400 «El IVA debe estar entre 0 y 100 %.».

##### C-F07-11 a C-F07-13 · impuestos (retirados)
`GET administration/taxes` (`B/Wms.Api/Controllers/v1/AdministrationController.cs:58`), `POST service/{id}/assign-tax` y `POST service/{id}/remove-tax` (`B/Wms.Api/Controllers/v1/ServiceController.cs:249-270`): responden 404 desde BE-1 (D19).

#### Grupo C — Acuerdos (BE-2)

##### C-F07-14 · `GET rates/agreements` (nuevo)
- **Política:** `BillingAccess`. **Qué hace:** un renglón por cliente con acuerdo (al menos una tarifa).
- **Filtros:** `customerName`, `customerIdNumber`. **Orden:** `customerName` (por defecto, asc), `customerIdNumber`, `currentCount`, `scheduledCount`, `lastValidFrom`. **Paginación:** C-F01-00.
- **Respuesta 200:** `pagedSchema(agreementListItemSchema)`: `{ "customerId", "customerName", "customerIdNumber", "currentCount": 4, "scheduledCount": 1, "lastValidFrom": "2027-01-01", "updatedAt" }`. **Zod de la petición:** `agreementListQuerySchema`.
- **Errores:** los de C-F01-00.

##### C-F07-15 · `GET rates/agreements/{customerId}/tariffs` (nuevo)
- **Política:** `BillingAccess`. **Qué hace:** las tarifas del acuerdo del cliente; un cliente sin acuerdo devuelve la lista vacía.
- **Filtros:** `serviceId`, `productName`, `appliesToPerishable` (`true`, `false` o `any` para «Todos»), `operationModalityId`, `formulaCode` (coma), `status` (`Current`, `Scheduled`, `Ended`, coma; por defecto `Current,Scheduled`). **Orden:** `serviceName` (por defecto), `productName`, `operationModalityName`, `formulaName`, `validFrom`. **Paginación:** C-F01-00 (la pantalla pide `all=true`).
- **Respuesta 200:** `pagedSchema(agreementTariffSchema)`:

```jsonc
{ "data": [{
  "id": "…", "service": { "id": "…", "code": "ALMACENAMIENTO", "name": "Almacenamiento en Bodega" },
  "product": null, "appliesToPerishable": null,
  "operationModality": { "id": "…", "code": "IMP001", "name": "Importación" },
  "formula": { "code": "UNLOADED_OR_ON_VEHICLE", "name": "Descargada o sobre vehículo" },
  "parameters": { "percentage": "0.3", "ratePerVehicle": "168000", "minimumScope": "UnloadedPart", "prorated": "true" },
  "paperwork": true, "taxIncluded": false,
  "validFrom": "2026-01-01", "validUntil": null, "status": "Current"
}], "pagination": { … } }
```

- **Errores:** 404 «No existe el cliente {id}.».

##### C-F07-16 · `POST rates/agreements/{customerId}/tariffs` (nuevo)
- **Política:** `BillingAccess`. **Qué hace:** agrega una tarifa con la línea de tiempo de D23; crea el acuerdo si el cliente no tiene.

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `serviceId` | Guid | sí | Servicio activo |
| `productId` | Guid o nulo | no | Nulo = todos |
| `appliesToPerishable` | booleano o nulo | no | Nulo = todos |
| `operationModalityId` | Guid o nulo | no | Nulo = todas |
| `formulaCode` | texto | sí | Fórmula activa permitida para el servicio (D27) |
| `parameters` | objeto texto → texto | sí | Valores con punto decimal; los valida el calculador de la fórmula |
| `paperwork` | booleano | sí | Suma la papelería (D25) |
| `taxIncluded` | booleano | sí | D20 |
| `validFrom` | fecha | sí | Cualquier día |

- **Respuesta 201:** `dataSchema(agreementTariffSchema)`.
- **Errores:** 400, los de los calculadores («Parámetro inválido: '{clave}' …», literales de hoy y de §2.2 Grupo D), «La fórmula «{nombre}» solo aplica al servicio de Almacenamiento.» (D27), «La fórmula 'Por tipo de vehículo (montacargas)' no es válida para el servicio de Almacenamiento.» (de hoy), «El tercero {nombre} no tiene el rol Cliente.»; 404 «No existe el cliente {id}.», «No existe el servicio {id}.», «No existe el producto {id}.», «No existe la modalidad {id}.», «No existe la fórmula «{código}».»; 409 «Ya hay una tarifa de {servicio} con ese producto, modalidad y perecedero desde el {dd/mm/aaaa}.».

##### C-F07-17 · `PUT rates/agreements/{customerId}/tariffs/{tariffId}` (nuevo)
- **Política:** `BillingAccess`. **Petición:** `formulaCode`, `parameters`, `paperwork`, `taxIncluded` y `validFrom` (reglas de C-F07-16; el ámbito no viaja). **Respuesta 200:** `dataSchema(agreementTariffSchema)`.
- **Errores:** los de C-F07-16 que aplican; 404 «No existe la tarifa {id} en el acuerdo del cliente.»; 409 «La vigencia de una tarifa que ya rige no se cambia: agregue una nueva desde la fecha que quiere.»; 409 «La tarifa terminó el {dd/mm/aaaa}: ya no se edita.».

##### C-F07-18 · `DELETE rates/agreements/{customerId}/tariffs/{tariffId}` (nuevo: retirar)
- **Política:** `BillingAccess`. **Petición:** sin cuerpo. **Qué hace:** D23 («Retirar»). **Respuesta 200:** `dataSchema(agreementTariffRetireResultSchema)`: `{ "result": "Deleted" | "Ended", "validUntil": "2026-11-26" | null }`.
- **Errores:** 404 como C-F07-17; 409 «La tarifa ya terminó el {dd/mm/aaaa}.».

##### C-F07-19 a C-F07-30 · `stakeholder/{stakeholderId}/agreement…` (retirados)

| ID | Endpoint de hoy (`B/Wms.Api/Controllers/v1/StakeholderController.cs:285-457`) |
| --- | --- |
| C-F07-19 | `POST stakeholder/{stakeholderId}/agreement` |
| C-F07-20 | `GET stakeholder/{stakeholderId}/agreement` |
| C-F07-21 | `GET stakeholder/{stakeholderId}/agreement/{id}` |
| C-F07-22 | `PATCH stakeholder/{stakeholderId}/agreement/{id}` |
| C-F07-23 | `POST stakeholder/{stakeholderId}/agreement/{id}/activate` |
| C-F07-24 | `POST stakeholder/{stakeholderId}/agreement/{id}/deactivate` |
| C-F07-25 | `POST stakeholder/{stakeholderId}/agreement/{agreementId}/services` |
| C-F07-26 | `GET stakeholder/{stakeholderId}/agreement/{agreementId}/services` |
| C-F07-27 | `PATCH stakeholder/{stakeholderId}/agreement/{agreementId}/services/{agreementServiceId}` |
| C-F07-28 | `DELETE stakeholder/{stakeholderId}/agreement/{agreementId}/services/{agreementServiceId}` |
| C-F07-29 | `POST stakeholder/{stakeholderId}/agreement/{agreementId}/services/{agreementServiceId}/activate` |
| C-F07-30 | `POST stakeholder/{stakeholderId}/agreement/{agreementId}/services/{agreementServiceId}/deactivate` |

Responden 404 desde BE-2. Los reemplazan C-F07-14 a C-F07-18.

#### Grupo D — Fórmulas, simulador y marca «Queda sobre el vehículo» (BE-3)

##### C-F07-31 · `GET FormulaType` (modificado sobre C-F01-77)
- **Política:** la de hoy. **Qué cambia:** las cuatro fórmulas de D29; cada fórmula trae `serviceScope` (`Any`, `StorageOnly` o `ForkliftOnly`, por D27 y `StorageFormulaRestriction`) y `simulatorInputs`; cada parámetro puede traer `enumLabels` (rótulo por valor) y `visibleWhen` (`"clave=valor"`). El rótulo de `thresholdKg` cambia (D36). `PER_UOM` sigue como en C-F01-77.
- **`simulatorInputs` por fórmula:** `PER_CARGO_UNIT` [`cargoUnitCount`]; `PER_UOM` [`quantity`]; `PERCENTAGE_OF_VALUE` [`cargoValueCop`]; `PERCENTAGE_OF_VALUE_PRORATED` [`cargoValueCop`, `quantity`, `baseQuantity`]; `PER_VEHICLE` [`vehicleCount`]; `FIXED` [] (más `cargoUnitCount` y `vehicleCount` si la tarifa usa `minimumPerCargoUnit`); `WEIGHT_THRESHOLD` [`merchandiseWeightKg`]; `PER_VEHICLE_TYPE` [`vehicleType`]; `UNLOADED_OR_ON_VEHICLE` [`cargoValueCop`, `trucks`, `quantity`, `baseQuantity`]; `VALUE_THRESHOLD` [`cargoValueCop`, `cargoUnitCount`, `quantity`, `baseQuantity`]; `WEIGHT_RATE_MINIMUM` [`merchandiseWeightKg`, `quantity`, `baseQuantity`]; `TIERED` [`merchandiseWeightKg`, `vehicleCount`, `quantity`, `baseQuantity`]. La pantalla oculta `quantity` y `baseQuantity` si `prorated` es falso, `cargoUnitCount` si `belowMode` es `Fixed`, y en `TIERED` el que no corresponde a `magnitude`.
- **Petición:** `includeInactive` (de hoy). **Respuesta 200:** `dataSchema(z.array(formulaTypeSchema))` (`formulaTypesResponseSchema`). **Errores:** ninguno nuevo. **Esquemas sembrados de las cuatro** (clave · rótulo · tipo · obligatorio · valores o condición):

| Fórmula | Parámetros |
| --- | --- |
| `UNLOADED_OR_ON_VEHICLE` «Descargada o sobre vehículo» | `percentage` · «Porcentaje sobre lo descargado (ej: 0,3 = 0,3 %)» · Decimal · sí; `ratePerVehicle` · «Tarifa por vehículo (mercancía sobre el vehículo)» · Decimal · sí; `minimum` · «Mínimo a cobrar ($)» · Decimal · no; `minimumScope` · «Cómo aplica el mínimo» · Enum · no · `UnloadedPart` «Sobre la parte porcentual del depósito» (por omisión), `PerUnloadedTruck` «Por camión descargado», `Total` «Sobre el total del depósito»; `minimumIncludesVat` (el de hoy); `prorated` · «Prorratear por saldo» · String `boolean` · no · por omisión `true` |
| `VALUE_THRESHOLD` «Según el valor» | `valueLimitCop` · «Límite del valor de la mercancía (COP)» · Decimal · sí; `belowMode` · «Hasta el límite» · Enum · sí · `Fixed` «Tarifa fija», `PerCargoUnit` «Por unidad de carga»; `belowRate` · «Tarifa hasta el límite» · Decimal · sí; `belowCargoUnitTypeCode` · «Tipo de unidad de carga» · String `lookup:cargoUnitType` · no · `visibleWhen: belowMode=PerCargoUnit` (obligatorio entonces); `abovePercentage` · «Porcentaje por encima del límite (ej: 0,2 = 0,2 %)» · Decimal · sí; `prorated` |
| `WEIGHT_RATE_MINIMUM` «Por tonelada o kilo con mínimo» | `rate` · «Tarifa por unidad de peso» · Decimal · sí; `weightUnit` · «Unidad de peso» · Enum · sí · `Ton` «Tonelada», `Kg` «Kilo»; `minimum` · «Mínimo a cobrar ($)» · Decimal · sí; `minimumIncludesVat`; `prorated` |
| `TIERED` «Por tramos» | `magnitude` · «Se cobra por» · Enum · sí · `Weight` «Peso de mercancía», `Vehicles` «Número de vehículos»; `weightUnit` · «Unidad de peso» · Enum · no · `Kg`, `Ton` · `visibleWhen: magnitude=Weight` (obligatorio entonces); `limit` · «Límite del primer tramo» · Decimal · sí; `rateUpTo` · «Tarifa hasta el límite (por unidad)» · Decimal · sí; `rateFrom` · «Tarifa desde el límite (por unidad)» · Decimal · sí; `tierMode` · «Al pasar el límite» · Enum · sí · `WholeQuantity` «Todo a la segunda tarifa», `Excess` «Solo el exceso a la segunda tarifa»; `prorated` · `visibleWhen: magnitude=Weight` |

- **Mensajes de los calculadores nuevos (400, con el patrón de hoy):** «Parámetro inválido: '{clave}' debe ser un decimal mayor o igual a 0.» (tarifas y mínimos); «… debe ser un decimal mayor que 0.» (`valueLimitCop`, `limit`); «… debe ser un decimal en el rango 0–100.» (porcentajes); «Parámetro inválido: '{clave}' debe ser uno de: {valores}.» (enums); «Parámetro inválido: 'belowCargoUnitTypeCode' es obligatorio con «Por unidad de carga».»; «Parámetro inválido: 'weightUnit' es obligatorio cuando se cobra por peso.»; `prorated` y `minimumIncludesVat`: «… debe ser true o false.».

##### C-F07-32 · `POST billing/formula-preview` (modificado)
- **Política:** la de hoy (`ActiveUser`). **Qué cambia:** `merchandiseWeightKg` reemplaza a `grossWeightKg`; entra `trucks`; la respuesta suma `warnings`.

| Campo | Tipo | Regla |
| --- | --- | --- |
| `formulaCode`, `parameters`, `taxRatePercent`, `taxIncluded`, `cargoValueCop`, `quantity`, `baseQuantity`, `cargoUnitCount`, `vehicleCount`, `vehicleType` | los de hoy | `B/Wms.Api/Controllers/v1/BillingPreviewController.cs:86-98` |
| `merchandiseWeightKg` | número o nulo | Peso de mercancía (kg) |
| `trucks` | lista o nulo | `{ price: número o nulo, staysOnVehicle: booleano }`, hasta 50 |

- **Respuesta 200:** `dataSchema(formulaPreviewResultSchema)`: `{ "amount", "taxAmount", "total", "minimumApplied", "explanation", "warnings": ["1 camión descargado sin precio: cuenta $0 en el cobro por camión."] }`.
- **Errores:** los de hoy y los de los calculadores; 400 «Máximo 50 camiones en el simulador.».

##### C-F07-33 · `PATCH foreign-trade/warehouse-storages/{warehouseStorageId}/entries/{entryId}/stays-on-vehicle` (nuevo)
- **Política:** `ForeignTradeAccess`. **Petición:** `{ "staysOnVehicle": true }`. **Qué hace:** D33 y D34 (no mueve inventario; audita; recalcula si aplica).
- **Respuesta 200:** `dataSchema(entryStaysOnVehicleResultSchema)`: `{ "entryId", "staysOnVehicle": true, "recalculated": true }`.
- **Errores:** 404 «La entrada {id} no pertenece al depósito.»; 409 «La entrada está anulada.»; 409 «El depósito {N} está {estado}: ya no se edita.» (el de `P05/` D18).

##### C-F07-34 · `GET foreign-trade/warehouse-storages/{warehouseStorageId}/entries` (modificado sobre C-F05-22)
- **Política:** `ForeignTradeAccess`. **Qué cambia:** cada entrada trae `staysOnVehicle` (la marca de la entrada, D33) y `canMarkStaysOnVehicle` (entrada no anulada y depósito en Borrador o Confirmado). `reception.staysOnVehicle` lee la misma marca. **Petición y errores:** los de C-F05-22. **Respuesta 200:** `dataSchema(z.array(depositEntryRowSchema))` con los dos campos (§2.3, «Integradas que cambian en I-07»).

##### C-F07-35 · `GET warehouse/pending-from-weighbridge` (modificado sobre C-F04-06)
- **Política:** `WarehouseAccess`. **Qué cambia:** cada fila trae `staysOnVehicle` (la marca que CE haya puesto; falso si no). **Petición y errores:** los de C-F04-06. **Respuesta 200:** la de C-F04-06 con el campo nuevo en `pendingReceptionItemSchema` (`F/features/warehouse/contracts/reception.ts:22`, §2.3).

##### C-F07-36 · `POST warehouse/receptions` (modificado sobre C-F04-07: regla)
- **Política:** `WarehouseAccess`. **Qué cambia:** `staysOnVehicle` se guarda en la entrada (D33) y, si cambia la marca que tenía, recalcula (D34). Petición, respuesta y errores, los de C-F04-07 (`receptionCreateSchema` y `receptionResultSchema`, sin cambios). Lo mismo para la recepción directa (`POST warehouse/receptions/without-weighbridge`, C-F04-08), que guarda su `staysOnVehicle` en la entrada que crea. El historial (`GET warehouse/receptions`, C-F04-09) y el detalle (`GET warehouse/receptions/{id}`, C-F04-10) leen la marca de la entrada, con la misma forma.

#### Grupo E — Plantilla (BE-4)

##### C-F07-37 · `GET rates/agreements/template` (nuevo)
- **Política:** `BillingAccess`. **Petición:** `customerId` (Guid, opcional). **Respuesta 200:** el archivo (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`), con `Content-Disposition: attachment; filename="plantilla-acuerdos.xlsx"` o `"acuerdo-{NIT}.xlsx"`. **Errores:** 404 «No existe el cliente {id}.» **Zod:** no aplica (es un archivo; la fuente devuelve un `Blob`).
- **Columnas (fila 1 rótulo · fila 2 clave):**

| Hoja | Columnas |
| --- | --- |
| Clientes | «NIT del cliente» `customerNit` · «Ciclo (días)» `cycleDays` · «Días de pago» `paymentTermDays` · «Límite de crédito» `creditLimit` · «NIT del Facturar a» `billToNit` · «Preferencia (Por servicio o Consolidada)» `invoicingPreference` |
| Facturar a | «NIT del cliente» `customerNit` · «NIT del importador» `importerNit` · «NIT del Facturar a» `billToNit` |
| Retenciones | «NIT del tercero que paga» `stakeholderNit` · «Retención (Retención en la fuente, ReteICA o ReteIVA)» `withholdingType` · «Porcentaje» `percent` |
| Tarifas | «NIT del cliente» `customerNit` · «Servicio (código)» `serviceCode` · «Producto (SKU o nombre; vacío = todos)» `product` · «Perecedero (Sí, No o vacío)» `perishable` · «Modalidad (vacío = todas)» `modality` · «Fórmula (código)» `formulaCode` · una columna por cada clave de parámetro de las fórmulas activas, con el rótulo «{rótulo} ({clave})» · «Papelería (Sí o No)» `paperwork` · «IVA incluido (Sí o No)» `taxIncluded` · «Vigente desde (dd/mm/aaaa)» `validFrom` |

##### C-F07-38 · `POST rates/agreements/import/preview` (nuevo)
- **Política:** `BillingAccess`. **Petición:** `multipart/form-data` con `file`. **Qué hace:** lee y valida sin guardar (D39 a D41).
- **Respuesta 200:** `dataSchema(agreementImportResultSchema)`:

```jsonc
{ "data": {
  "fileName": "acuerdos-2027.xlsx",
  "sheets": { "clients": 12, "billTo": 5, "withholdings": 9, "tariffs": 31 },
  "rows": [
    { "sheet": "Tariffs", "row": 3, "customerNit": "900000001", "product": null, "serviceCode": "ALMACENAMIENTO",
      "formulaName": "Porcentaje del valor de la mercancía (prorrateado por saldo)", "validFrom": "2027-01-01",
      "outcome": "NewScheduled", "message": "Nueva, programada" },
    { "sheet": "Tariffs", "row": 5, "customerNit": "900000099", "product": null, "serviceCode": "ALMACENAMIENTO",
      "formulaName": "Por tonelada o kilo con mínimo", "validFrom": "2027-01-01",
      "outcome": "Error", "message": "El NIT 900000099 no existe: créelo antes en Configuración › Terceros." },
    { "sheet": "Clients", "row": 3, "customerNit": "900000002", "product": null, "serviceCode": null,
      "formulaName": null, "validFrom": null, "outcome": "Updates", "message": "Ciclo 20 días, Facturar a general" }
  ],
  "validCount": 47, "errorCount": 1, "unchangedCount": 0, "applied": null
} }
```

- **Errores (400):** «Adjunte el archivo de la plantilla (.xlsx).»; «El archivo debe ser .xlsx.»; «El archivo supera 5 MB.»; «Falta la hoja «{hoja}».»; «La hoja «{hoja}» no tiene la columna «{clave}».»; «La plantilla tiene más de 2.000 filas: divídala en varios archivos.».
- **Mensajes por fila (`outcome: Error`):** «El NIT {nit} no existe: créelo antes en Configuración › Terceros.»; «El tercero {nit} no tiene el rol Cliente.»; «El tercero {nit} no tiene el rol Importador.»; «El servicio «{código}» no existe.»; «La fórmula «{código}» no existe.»; «El producto «{texto}» no existe.»; «El producto «{texto}» es ambiguo: use el SKU.»; «La modalidad «{texto}» no existe.»; «Perecedero debe ser Sí, No o vacío.»; «{columna} debe ser Sí o No.»; «Falta «Vigente desde».»; «La fecha «{texto}» no es válida (dd/mm/aaaa).»; «Los días del ciclo deben estar entre 1 y 360.»; «La preferencia debe ser «Por servicio» o «Consolidada».»; «Fila repetida: la fila {n} ya trae esa tarifa con la misma fecha.»; en «Retenciones», «La retención «{texto}» no existe: use Retención en la fuente, ReteICA o ReteIVA.», «Falta el porcentaje.», «El porcentaje debe ser mayor que 0 y hasta 100.» y «Fila repetida: la fila {n} ya trae esa retención para ese tercero.»; y los de los calculadores y de D27.

##### C-F07-39 · `POST rates/agreements/import` (nuevo)
- **Política:** `BillingAccess`. **Petición:** la de C-F07-38. **Qué hace:** vuelve a leer y validar y aplica las filas válidas en una transacción (D40).
- **Respuesta 200:** la de C-F07-38 con `"applied": { "clients": 12, "billTo": 5, "withholdings": 9, "tariffs": 30 }` y el `outcome` final de cada fila (`agreementImportResponseSchema`). **Errores:** los de C-F07-38; 409 si la transacción falla por una carrera («Otra persona cambió las tarifas mientras importaba: vuelva a cargar la vista previa.»), sin guardar nada.

#### Grupo G — Retenciones del tercero que paga (BE-1)

##### C-F07-54 · `GET billing/withholdings/types` (nuevo)
- **Política:** `BillingAccess`. **Petición:** sin parámetros. **Qué hace:** el selector de D53, en este orden: `Retefuente` «Retención en la fuente» (base `Subtotal`), `ReteIca` «ReteICA» (base `Subtotal`) y `ReteIva` «ReteIVA» (base `Vat`).
- **Respuesta 200:** `dataSchema(z.array(withholdingTypeOptionSchema))`: `[{ "value": "Retefuente", "label": "Retención en la fuente", "base": "Subtotal" }, …]`. **Errores:** ninguno propio (401 y 403 de la política). **Zod:** `withholdingTypesResponseSchema`.

##### C-F07-55 · `GET billing/withholdings/{stakeholderId}` (nuevo)
- **Política:** `BillingAccess`. **Petición:** sin parámetros. **Qué hace:** las retenciones que practica el tercero (D52); cualquier tercero, sea o no cliente; sin retenciones, la lista vacía.
- **Respuesta 200:** `dataSchema(z.array(withholdingSchema))`: `[{ "type": "Retefuente", "percent": 2.5 }, { "type": "ReteIva", "percent": 15 }]`. **Errores:** 404 «No existe el tercero {id}.». **Zod:** `withholdingsResponseSchema`.
- **Para F08:** «Facturar» de una factura de almacenamiento (D55) lee las del destinatario y las calcula con `StorageWithholdings` (D54): Retefuente y ReteICA = % × subtotal; ReteIVA = % × IVA; cada una a 2 decimales.

##### C-F07-56 · `PUT billing/withholdings/{stakeholderId}` (nuevo)
- **Política:** `BillingAccess`. **Qué hace:** reemplaza la lista del tercero (vacía = sin retenciones); auditada.

| Campo | Tipo | Obligatorio | Regla |
| --- | --- | --- | --- |
| `withholdings` | lista | sí (puede ir vacía) | `{ type, percent }`: `type` del selector (C-F07-54), sin repetir; `percent` mayor que 0 y hasta 100, con hasta 4 decimales |

- **Respuesta 200:** la de C-F07-55. **Zod:** `withholdingsUpdateSchema` (petición) y `withholdingsResponseSchema`.
- **Errores:** 400 «La retención «{rótulo}» está repetida.»; 400 «El porcentaje de «{rótulo}» debe ser mayor que 0 y hasta 100.»; 400 «La retención «{valor}» no existe.»; 404 «No existe el tercero {id}.».

#### Grupo F — De hoy, sin cambios de forma

Las fichas son las de hoy; F07 solo escribe sus esquemas Zod (§2.3) para maquetarlos. Rutas: `B/Wms.Api/Controllers/v1/ServiceController.cs:105-247` (C-F07-40 a C-F07-49), `B/Wms.Api/Controllers/v1/ForkliftRateController.cs:27-75` (C-F07-50 a C-F07-52) y `B/Wms.Api/Controllers/v1/AdministrationController.cs:106` (C-F07-53). Peticiones: `ServicePricingRuleRequest` (`formulaTypeId`, `productId`, `operationModalityId`, `taxIncluded`, `linkedServiceId`, `parameters[{ key, value, dataType }]`, `appliesToPerishable`), `UpdateServicePriceRequest` (`basePrice`, `validFrom`, `validTo`, opcionales), `UpdateServiceMinimumValueRequest` (`amount`, `isActive`, `includesVat`) y `UpsertForkliftRateRequest` (`amount`). C-F07-44 y C-F07-45 suman el error de D27.

### 2.3 Esquemas Zod y tipos

Zod 4 (`Frontend/wms/package.json:46`, `zod ^4.1.13`), con las ayudas de `F/shared/contracts/api.ts` (`guidSchema` = `z.guid()`, `dateTimeSchema`, `dateOnlySchema` = `z.iso.date()`, `dataSchema`, `pagedSchema`, `listQueryBaseSchema`). Los tipos se derivan con `z.infer`.

**`F/features/rates/contracts/billing-configuration.ts`** (FE-1; C-F07-01 a C-F07-04 y C-F07-54 a C-F07-56):

```ts
import { z } from "zod";
import { dataSchema, dateTimeSchema, guidSchema, listQueryBaseSchema, pagedSchema } from "~/shared/contracts/api";

export const billingCycleSchema = z.enum(["Weekly", "Biweekly", "Days15", "Days30", "Days90", "Days180", "Days360", "Custom"]);
// Solo se leen: configuraciones antiguas (D14).
export const billingCycleReadSchema = z.enum([...billingCycleSchema.options, "Monthly", "OnDemand"]);
export const invoicingPreferenceSchema = z.enum(["PerService", "Consolidated"]);
export const invoicingPreferenceReadSchema = z.enum([...invoicingPreferenceSchema.options, "PerWeighbridgeCycle"]);
export const stakeholderRefSchema = z.object({ id: guidSchema, name: z.string(), idNumber: z.string() });

// D52, D53 — Retenciones del tercero que paga.
export const withholdingTypeSchema = z.enum(["Retefuente", "ReteIca", "ReteIva"]);
export const withholdingTypeOptionSchema = z.object({
  value: withholdingTypeSchema,
  label: z.string(),
  base: z.enum(["Subtotal", "Vat"]),
});
export const withholdingSchema = z.object({
  type: withholdingTypeSchema,
  percent: z
    .number()
    .gt(0, "El porcentaje debe ser mayor que 0 y hasta 100.")
    .max(100, "El porcentaje debe ser mayor que 0 y hasta 100.")
    .refine((v) => Math.round(v * 10_000) === v * 10_000, "Hasta 4 decimales."),
});
export const withholdingsUpdateSchema = z.object({
  withholdings: z
    .array(withholdingSchema)
    .refine((list) => new Set(list.map((w) => w.type)).size === list.length, "Una retención está repetida."),
});
export const billToRefSchema = stakeholderRefSchema.extend({ withholdings: z.array(withholdingSchema) });

export const billingCycleOptionSchema = z.object({
  value: billingCycleSchema,
  label: z.string(),
  days: z.int().positive().nullable(),
});
export const billingConfigurationSchema = z.object({
  id: guidSchema,
  stakeholderId: guidSchema,
  stakeholderName: z.string(),
  stakeholderIdNumber: z.string(),
  billingCycle: billingCycleReadSchema,
  cycleDays: z.int().min(1).max(360).nullable(),
  billingCycleLabel: z.string(),
  paymentTermDays: z.int().min(0),
  creditLimit: z.number().min(0).nullable(),
  invoicingPreference: invoicingPreferenceReadSchema,
  billTo: billToRefSchema.nullable(),
  billToExceptionsCount: z.int().min(0),
  withholdings: z.array(withholdingSchema),
  isActive: z.boolean(),
  createdAt: dateTimeSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const billToExceptionSchema = z.object({
  id: guidSchema,
  importer: stakeholderRefSchema,
  billTo: billToRefSchema,
});
export const billingConfigurationDetailSchema = billingConfigurationSchema.extend({
  billToExceptions: z.array(billToExceptionSchema),
});
export const billingConfigurationListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["stakeholderName", "stakeholderIdNumber", "billingCycle", "paymentTermDays", "creditLimit", "updatedAt"]).optional(),
  stakeholderName: z.string().optional(),
  stakeholderIdNumber: z.string().optional(),
  billingCycle: z.string().optional(), // enums separados por coma (C-F01-00)
  invoicingPreference: z.string().optional(),
  billToName: z.string().optional(),
  isActive: z.boolean().optional(),
});
export const billingConfigurationUpsertSchema = z
  .object({
    billingCycle: billingCycleSchema,
    cycleDays: z.int().min(1, "Digite los días del ciclo, de 1 a 360.").max(360, "Digite los días del ciclo, de 1 a 360.").nullable(),
    paymentTermDays: z.int().min(0, "Los días de plazo de pago no pueden ser negativos."),
    invoicingPreference: invoicingPreferenceSchema,
    creditLimit: z.number().min(0, "El límite de crédito no puede ser negativo.").nullable(),
    billToStakeholderId: guidSchema.nullable(),
    billToExceptions: z.array(z.object({ importerId: guidSchema, billToStakeholderId: guidSchema })),
  })
  .refine((v) => (v.billingCycle === "Custom") === (v.cycleDays !== null), {
    path: ["cycleDays"],
    message: "Digite los días del ciclo, de 1 a 360.",
  })
  .refine((v) => new Set(v.billToExceptions.map((e) => e.importerId)).size === v.billToExceptions.length, {
    path: ["billToExceptions"],
    message: "Un importador está repetido en las excepciones.",
  });

export const billingConfigurationListResponseSchema = pagedSchema(billingConfigurationSchema);
export const billingConfigurationDetailResponseSchema = dataSchema(billingConfigurationDetailSchema);
export const billingCyclesResponseSchema = dataSchema(z.array(billingCycleOptionSchema));
export const withholdingTypesResponseSchema = dataSchema(z.array(withholdingTypeOptionSchema));
export const withholdingsResponseSchema = dataSchema(z.array(withholdingSchema));

export type BillingCycle = z.infer<typeof billingCycleSchema>;
export type BillingConfiguration = z.infer<typeof billingConfigurationSchema>;
export type BillingConfigurationDetail = z.infer<typeof billingConfigurationDetailSchema>;
export type BillingConfigurationListQuery = z.infer<typeof billingConfigurationListQuerySchema>;
export type BillingConfigurationUpsert = z.infer<typeof billingConfigurationUpsertSchema>;
export type BillingCycleOption = z.infer<typeof billingCycleOptionSchema>;
export type WithholdingType = z.infer<typeof withholdingTypeSchema>;
export type Withholding = z.infer<typeof withholdingSchema>;
export type WithholdingTypeOption = z.infer<typeof withholdingTypeOptionSchema>;
```

**`F/features/billing/contracts/billing-recipient.ts`** (se suma al archivo de hoy; FE-1 lo escribe, F08 lo usa; C-F07-05 y C-F07-07):

```ts
export const invoiceRecipientCandidateSchema = z.object({
  stakeholderId: guidSchema,
  name: z.string(),
  idNumber: z.string(),
  roles: z.array(z.object({ code: z.string(), name: z.string() })),
  billTo: z.object({ scope: z.enum(["General", "Importer"]), importerName: z.string().nullable() }).nullable(),
});
export const invoiceDepositCustomerFieldsSchema = z.object({
  depositCustomerId: guidSchema.nullable(),
  depositCustomerName: z.string().nullable(),
});
export type InvoiceRecipientCandidate = z.infer<typeof invoiceRecipientCandidateSchema>;
```

**`F/features/services/contracts/service.ts`** (cambia; FE-3; C-F07-08 a C-F07-10): `taxSchema` sale; `serviceSchema` cambia `taxes` por `vatPercent` y `currentPrice` pasa a `servicePriceSchema.nullable().optional()`:

```ts
export const vatPercentSchema = z.number().min(0, "El IVA debe estar entre 0 y 100 %.").max(100, "El IVA debe estar entre 0 y 100 %.");
export const serviceSchema = z.object({
  id: guidSchema,
  code: z.string(),
  name: z.string(),
  description: z.string().nullable(),
  isActive: z.boolean(),
  vatPercent: vatPercentSchema,
  currentPrice: servicePriceSchema.nullable().optional(),
  createdAt: dateTimeSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const serviceVatUpdateSchema = z.object({ vatPercent: vatPercentSchema });
export const servicePriceCreateSchema = z.object({
  basePrice: z.number().min(0, "El precio base debe ser mayor o igual a cero."),
  validFrom: dateTimeSchema,
  validTo: dateTimeSchema.nullable(),
  vatPercent: vatPercentSchema.nullable(),
});
export type ServicePriceCreate = z.infer<typeof servicePriceCreateSchema>;
```

**`F/features/rates/contracts/service-rates.ts`** (FE-3; C-F07-40 a C-F07-49, C-F07-53):

```ts
import { z } from "zod";
import { dataSchema, dateTimeSchema, guidSchema } from "~/shared/contracts/api";
import { servicePriceSchema } from "~/features/services/contracts/service";

export const parameterDataTypeSchema = z.enum(["Decimal", "Integer", "String", "Enum"]);
export const servicePricingRuleSchema = z.object({
  id: guidSchema,
  serviceId: guidSchema,
  formulaTypeId: guidSchema,
  formulaTypeCode: z.string(),
  formulaTypeName: z.string(),
  productId: guidSchema.nullable(),
  productName: z.string().nullable(),
  operationModalityId: guidSchema.nullable(),
  operationModalityCode: z.string().nullable(),
  operationModalityName: z.string().nullable(),
  appliesToPerishable: z.boolean().nullable(),
  isActive: z.boolean(),
  taxIncluded: z.boolean(),
  linkedServiceId: guidSchema.nullable(),
  linkedServiceName: z.string().nullable(),
  parameters: z.array(z.object({ key: z.string(), value: z.string(), dataType: parameterDataTypeSchema })),
  createdAt: dateTimeSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const servicePricingRuleInputSchema = z.object({
  formulaTypeId: guidSchema,
  productId: guidSchema.nullable(),
  operationModalityId: guidSchema.nullable(),
  taxIncluded: z.boolean(),
  linkedServiceId: guidSchema.nullable(),
  parameters: z.array(z.object({ key: z.string(), value: z.string(), dataType: parameterDataTypeSchema })),
  appliesToPerishable: z.boolean().nullable(),
});
export const servicePriceUpdateSchema = z.object({
  basePrice: z.number().min(0).nullable(),
  validFrom: dateTimeSchema.nullable(),
  validTo: dateTimeSchema.nullable(),
});
export const serviceMinimumValueSchema = z.object({
  id: guidSchema,
  operationModalityId: guidSchema,
  operationModalityCode: z.string(),
  operationModalityName: z.string(),
  amount: z.number().min(0),
  includesVat: z.boolean(),
  isActive: z.boolean(),
  updatedAt: dateTimeSchema.nullable(),
});
export const serviceMinimumValueUpdateSchema = z.object({
  amount: z.number().min(0),
  isActive: z.boolean(),
  includesVat: z.boolean(),
});
export const operationModalitySchema = z.object({
  id: guidSchema,
  code: z.string(),
  name: z.string(),
  description: z.string().nullable(),
  isActive: z.boolean(),
  createdAt: dateTimeSchema,
  updatedAt: dateTimeSchema.nullable(),
});
export const servicePricesResponseSchema = dataSchema(z.array(servicePriceSchema));
export const servicePricingRulesResponseSchema = dataSchema(z.array(servicePricingRuleSchema));
export const serviceMinimumValuesResponseSchema = dataSchema(z.array(serviceMinimumValueSchema));
export const operationModalitiesResponseSchema = dataSchema(z.array(operationModalitySchema));

export type ServicePricingRule = z.infer<typeof servicePricingRuleSchema>;
export type ServicePricingRuleInput = z.infer<typeof servicePricingRuleInputSchema>;
export type ServiceMinimumValue = z.infer<typeof serviceMinimumValueSchema>;
export type OperationModality = z.infer<typeof operationModalitySchema>;
```

**`F/features/rates/contracts/forklift-rate.ts`** (FE-1; C-F07-50 a C-F07-52):

```ts
import { z } from "zod";
import { dataSchema, dateTimeSchema } from "~/shared/contracts/api";

export const forkliftVehicleTypeSchema = z.object({ value: z.string(), label: z.string() });
export const forkliftRateSchema = z.object({
  vehicleType: z.string(),
  label: z.string(),
  amount: z.number().min(0).nullable(),
  updatedAt: dateTimeSchema.nullable(),
});
export const forkliftRateUpsertSchema = z.object({ amount: z.number().min(0, "La tarifa debe ser mayor o igual a cero.") });
export const forkliftVehicleTypesResponseSchema = dataSchema(z.array(forkliftVehicleTypeSchema));
export const forkliftRatesResponseSchema = dataSchema(z.array(forkliftRateSchema));
export type ForkliftRate = z.infer<typeof forkliftRateSchema>;
```

**`F/features/rates/contracts/formula.ts`** (FE-2; C-F07-31 y C-F07-32):

```ts
import { z } from "zod";
import { dataSchema, guidSchema } from "~/shared/contracts/api";
import { parameterDataTypeSchema } from "./service-rates";

export const simulatorInputSchema = z.enum([
  "cargoValueCop", "quantity", "baseQuantity", "merchandiseWeightKg",
  "cargoUnitCount", "vehicleCount", "vehicleType", "trucks",
]);
export const formulaParameterSchema = z.object({
  key: z.string(),
  label: z.string(),
  dataType: parameterDataTypeSchema,
  required: z.boolean(),
  enumValues: z.array(z.string()).nullable(),
  enumLabels: z.record(z.string(), z.string()).nullable(),
  uiHint: z.string().nullable(),
  defaultValue: z.string().nullable(),
  visibleWhen: z.string().regex(/^[A-Za-z]+=[A-Za-z]+$/).nullable(), // "belowMode=PerCargoUnit"
});
export const formulaTypeSchema = z.object({
  id: guidSchema,
  code: z.string(),
  name: z.string(),
  description: z.string().nullable(),
  parameterSchema: z.array(formulaParameterSchema),
  isActive: z.boolean(),
  serviceScope: z.enum(["Any", "StorageOnly", "ForkliftOnly"]),
  simulatorInputs: z.array(simulatorInputSchema),
});
export const simulatorTruckSchema = z.object({
  price: z.number().min(0).nullable(),
  staysOnVehicle: z.boolean(),
});
export const formulaPreviewRequestSchema = z.object({
  formulaCode: z.string().min(1),
  parameters: z.record(z.string(), z.string()),
  taxRatePercent: z.number().min(0).max(100).nullable(),
  taxIncluded: z.boolean(),
  cargoValueCop: z.number().min(0).nullable(),
  quantity: z.number().min(0).nullable(),
  baseQuantity: z.number().positive().nullable(),
  merchandiseWeightKg: z.number().min(0).nullable(),
  cargoUnitCount: z.int().min(0).nullable(),
  vehicleCount: z.int().min(0).nullable(),
  vehicleType: z.string().nullable(),
  trucks: z.array(simulatorTruckSchema).max(50, "Máximo 50 camiones en el simulador.").nullable(),
});
export const formulaPreviewResultSchema = z.object({
  amount: z.number(),
  taxAmount: z.number(),
  total: z.number(),
  minimumApplied: z.boolean(),
  explanation: z.string(),
  warnings: z.array(z.string()),
});
export const formulaTypesResponseSchema = dataSchema(z.array(formulaTypeSchema));
export const formulaPreviewResponseSchema = dataSchema(formulaPreviewResultSchema);

export type FormulaType = z.infer<typeof formulaTypeSchema>;
export type FormulaParameter = z.infer<typeof formulaParameterSchema>;
export type SimulatorInput = z.infer<typeof simulatorInputSchema>;
export type FormulaPreviewRequest = z.infer<typeof formulaPreviewRequestSchema>;
export type FormulaPreviewResult = z.infer<typeof formulaPreviewResultSchema>;
```

**`F/features/rates/contracts/agreement.ts`** (FE-2; C-F07-14 a C-F07-18):

```ts
import { z } from "zod";
import { dataSchema, dateOnlySchema, dateTimeSchema, guidSchema, listQueryBaseSchema, pagedSchema } from "~/shared/contracts/api";

export const agreementTariffStatusSchema = z.enum(["Current", "Scheduled", "Ended"]);
export const agreementListItemSchema = z.object({
  customerId: guidSchema,
  customerName: z.string(),
  customerIdNumber: z.string(),
  currentCount: z.int().min(0),
  scheduledCount: z.int().min(0),
  lastValidFrom: dateOnlySchema.nullable(),
  updatedAt: dateTimeSchema.nullable(),
});
export const agreementListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["customerName", "customerIdNumber", "currentCount", "scheduledCount", "lastValidFrom"]).optional(),
  customerName: z.string().optional(),
  customerIdNumber: z.string().optional(),
});
export const agreementTariffSchema = z.object({
  id: guidSchema,
  service: z.object({ id: guidSchema, code: z.string(), name: z.string() }),
  product: z.object({ id: guidSchema, name: z.string() }).nullable(),
  appliesToPerishable: z.boolean().nullable(),
  operationModality: z.object({ id: guidSchema, code: z.string(), name: z.string() }).nullable(),
  formula: z.object({ code: z.string(), name: z.string() }),
  parameters: z.record(z.string(), z.string()),
  paperwork: z.boolean(),
  taxIncluded: z.boolean(),
  validFrom: dateOnlySchema,
  validUntil: dateOnlySchema.nullable(),
  status: agreementTariffStatusSchema,
});
export const agreementTariffListQuerySchema = listQueryBaseSchema.extend({
  sortField: z.enum(["serviceName", "productName", "operationModalityName", "formulaName", "validFrom"]).optional(),
  serviceId: guidSchema.optional(),
  productName: z.string().optional(),
  appliesToPerishable: z.enum(["true", "false", "any"]).optional(),
  operationModalityId: guidSchema.optional(),
  formulaCode: z.string().optional(),
  status: z.string().optional(), // "Current,Scheduled" por omisión
});
export const agreementTariffUpdateSchema = z.object({
  formulaCode: z.string().min(1, "Elija la fórmula."),
  parameters: z.record(z.string(), z.string()),
  paperwork: z.boolean(),
  taxIncluded: z.boolean(),
  validFrom: dateOnlySchema,
});
export const agreementTariffCreateSchema = agreementTariffUpdateSchema.extend({
  serviceId: guidSchema,
  productId: guidSchema.nullable(),
  appliesToPerishable: z.boolean().nullable(),
  operationModalityId: guidSchema.nullable(),
});
export const agreementTariffRetireResultSchema = z.object({
  result: z.enum(["Deleted", "Ended"]),
  validUntil: dateOnlySchema.nullable(),
});
export const agreementListResponseSchema = pagedSchema(agreementListItemSchema);
export const agreementTariffListResponseSchema = pagedSchema(agreementTariffSchema);
export const agreementTariffResponseSchema = dataSchema(agreementTariffSchema);
export const agreementTariffRetireResponseSchema = dataSchema(agreementTariffRetireResultSchema);

export type AgreementListItem = z.infer<typeof agreementListItemSchema>;
export type AgreementTariff = z.infer<typeof agreementTariffSchema>;
export type AgreementTariffCreate = z.infer<typeof agreementTariffCreateSchema>;
export type AgreementTariffUpdate = z.infer<typeof agreementTariffUpdateSchema>;
export type AgreementTariffStatus = z.infer<typeof agreementTariffStatusSchema>;
```

Los parámetros se validan en el navegador con un esquema que arma `F/features/rates/utils/formula-parameters.ts` a partir de `formulaTypeSchema.parameterSchema` (obligatorio si `required` o si su `visibleWhen` se cumple; `Decimal` ≥ 0 con coma o punto; `Enum` dentro de `enumValues`); el API es la última palabra.

**`F/features/rates/contracts/agreement-import.ts`** (FE-3; C-F07-37 a C-F07-39; la descarga devuelve un `Blob` y no lleva esquema):

```ts
import { z } from "zod";
import { dataSchema, dateOnlySchema } from "~/shared/contracts/api";

export const importSheetSchema = z.enum(["Clients", "BillTo", "Withholdings", "Tariffs"]);
export const importOutcomeSchema = z.enum(["New", "NewScheduled", "Replaces", "Updates", "Unchanged", "Error"]);
export const agreementImportRowSchema = z.object({
  sheet: importSheetSchema,
  row: z.int().min(3),
  customerNit: z.string().nullable(),
  product: z.string().nullable(),
  serviceCode: z.string().nullable(),
  formulaName: z.string().nullable(),
  validFrom: dateOnlySchema.nullable(),
  outcome: importOutcomeSchema,
  message: z.string(),
});
export const agreementImportResultSchema = z.object({
  fileName: z.string(),
  sheets: z.object({ clients: z.int().min(0), billTo: z.int().min(0), withholdings: z.int().min(0), tariffs: z.int().min(0) }),
  rows: z.array(agreementImportRowSchema),
  validCount: z.int().min(0),
  errorCount: z.int().min(0),
  unchangedCount: z.int().min(0),
  applied: z.object({ clients: z.int().min(0), billTo: z.int().min(0), withholdings: z.int().min(0), tariffs: z.int().min(0) }).nullable(),
});
export const agreementImportResponseSchema = dataSchema(agreementImportResultSchema);
export type AgreementImportResult = z.infer<typeof agreementImportResultSchema>;
export type AgreementImportRow = z.infer<typeof agreementImportRowSchema>;
export type ImportOutcome = z.infer<typeof importOutcomeSchema>;
```

**Integradas que cambian en I-07** (C-F07-33 a C-F07-35):

```ts
// F/features/foreign-trade/contracts/deposit-entry.ts — depositEntryRowSchema (C-F05-22 → C-F07-34)
export const depositEntryRowSchema = depositEntryWithReceptionSchema.extend({
  // … campos de hoy …
  staysOnVehicle: z.boolean(),
  canMarkStaysOnVehicle: z.boolean(),
});
export const entryStaysOnVehicleInputSchema = z.object({ staysOnVehicle: z.boolean() });
export const entryStaysOnVehicleResultSchema = z.object({
  entryId: guidSchema,
  staysOnVehicle: z.boolean(),
  recalculated: z.boolean(),
});

// F/features/warehouse/contracts/reception.ts — pendingReceptionItemSchema (C-F04-06 → C-F07-35) suma:
//   staysOnVehicle: z.boolean(),
```

### 2.4 Pantallas y sus endpoints

| Pantalla | Ruta | Endpoints | Fase FE |
| --- | --- | --- | --- |
| P-FAC-11 · Configuración de facturación (listado) | `/billing/configurations` | C-F07-01, C-F07-04, C-F01-25 (modal del cliente) | FE-1 |
| P-FAC-11 · Configuración del cliente | `/billing/configurations/[customerId]` | C-F07-02, C-F07-03, C-F07-04, C-F07-54, C-F07-55, C-F07-56, C-F01-25, C-F01-26, C-F01-141 | FE-1 |
| Tarifas de montacargas | `/admin/forklift-rates` | C-F07-50, C-F07-51, C-F07-52, C-F07-08 (IVA de Montacargas) | FE-1 |
| Acuerdos (listado) | `/rates/agreements` | C-F07-14, C-F07-37, C-F01-25 | FE-2 |
| P-FAC-12 · Acuerdo del cliente | `/rates/agreements/[customerId]` | C-F07-15, C-F07-17, C-F07-18, C-F07-37, C-F01-26, C-F07-53, C-F07-08 (filtro de servicio), C-F07-31 | FE-2 |
| P-FAC-13 · Agregar tarifa (acuerdo y base) | diálogo | C-F07-16, C-F07-17, C-F07-31, C-F07-32, C-F07-08 (IVA del servicio), C-F07-53, C-F01-69, C-F01-33; en modo base C-F07-44, C-F07-45 | FE-2 |
| P-FAC-14 · Importar plantilla | `/rates/agreements/import` | C-F07-37, C-F07-38, C-F07-39 | FE-3 |
| Tarifas de servicios | `/rates/services` (drawer) | C-F07-08, C-F07-09, C-F07-10, C-F07-40 a C-F07-49, C-F07-53 | FE-3 |
| Etapa Bodega del detalle de CE (P-CE-05, integrada) | `/foreign-trade/…/[id]` | C-F07-34, C-F07-33 | I-07 |
| Recepción de Bodega (P-BOD-01, P-BOD-02, integradas) | `/warehouse/receptions` | C-F07-35, C-F07-36 | I-07 |
| Detalles de Terceros y Servicios (integrados) | `/admin/stakeholders`, `/admin/services` | — (enlaces, D49) | I-07 |
| **Para F08:** «Facturar» (con las retenciones del destinatario en las de almacenamiento, D54 y D55), «Cambiar destinatario» y Facturas › Almacenamiento | F08 | C-F07-02, C-F07-05, C-F07-06, C-F07-07, C-F07-54, C-F07-55 | — |

---

## 3. Archivos que se tocan

Líneas de la base. Cada fase confirma con `grep` antes de cambiar.

### 3.1 Backend

| Fase | Archivo (`B/`) | Qué cambia |
| --- | --- | --- |
| BE-1 | `Wms.Domain/Enums/BillingCycle.cs` | Suma `Custom`; `Monthly` queda solo para leer (comentario como `OnDemand`) |
| BE-1 | `Wms.Domain/Entities/Billing/StakeholderBillingConfiguration.cs` | `CycleDays`, `BillToStakeholderId`, colección `BillToExceptions`; `Create` y `Update` con sus reglas (D14, D15) |
| BE-1 | `Wms.Domain/Entities/Billing/BillToException.cs` (nuevo) y su configuración EF en `Wms.Infrastructure/Persistence/Configurations/Billing/` | D15 |
| BE-1 | `Wms.Domain/Entities/Billing/Invoice.cs:37`, `:212-240` | `DepositCustomerId` y su navegación; `CreateForPeriod` recibe el cliente del depósito y el destinatario (D16) |
| BE-1 | `Wms.Application/Billing/Common/Services/BillingCycleCatalog.cs:24-60` | Catálogo de D14, `LengthInDays(cycle, cycleDays)` y la ventana de `Custom` |
| BE-1 | `Wms.Application/Billing/Common/Services/StoragePeriodCalculator.cs:30-90` | `First`, `Next`, `ForStart` y `PeriodsUntil` con la longitud en días |
| BE-1 | `Wms.Application/Billing/Common/Services/StorageBillingService.cs:410-500`, `:560-570` | Ciclo por omisión `Days30`; destinatario con `BillToResolver`; `DepositCustomerId`; consolidada por cliente y destinatario |
| BE-1 | `Wms.Application/Billing/Common/Services/BillingService.cs:34-44`, `:93-103`, `:206-214` | `GetTotalTaxRate` con `VatPercent`; ciclo por omisión; consolidada por (cliente, destinatario) |
| BE-1 | `Wms.Application/Billing/Common/Services/DepositCustomerBillingChange.cs` | Cambio de cliente con `DepositCustomerId` y el destinatario de D16 |
| BE-1 | `Wms.Application/Billing/Common/Services/BillToResolver.cs` (nuevo, puro) | D15 |
| BE-1 | `Wms.Domain/Enums/WithholdingType.cs`, `Wms.Domain/Entities/Billing/StakeholderWithholding.cs` (nuevos) y su configuración EF; `Wms.Application/Billing/Common/Services/StorageWithholdings.cs` (nuevo, puro: cálculo de D54 para F08); consultas y comando de C-F07-54 a C-F07-56; endpoints en `Wms.Api/Controllers/v1/BillingController.cs` | D52 a D55 |
| BE-1 | `Wms.Application/Billing/Commands/UpsertBillingConfiguration/*` | Petición, validador (mensajes de C-F07-03) y handler (reemplaza las excepciones) |
| BE-1 | `Wms.Application/Billing/Queries/GetBillingConfiguration(s)/*`, `Common/DTOs/BillingConfigurationDto.cs` | Campos de C-F07-01 y C-F07-02; orden y filtros con `ListSorting` |
| BE-1 | `Wms.Api/Controllers/v1/BillingCyclesController.cs:24-30` | C-F07-04 |
| BE-1 | `Wms.Application/Billing/Queries/…RecipientCandidates…`, `Commands/UpdateInvoiceRecipient/UpdateInvoiceRecipientHandler.cs` | C-F07-05, C-F07-06 (D17) |
| BE-1 | `Wms.Application/Billing/Common/DTOs/InvoiceDto.cs`, `Common/Mappers/InvoiceMapper.cs` | `depositCustomerId`, `depositCustomerName` (C-F07-07) |
| BE-1 | `Wms.Application/Billing/Jobs/OverdueSweep.cs:20-25`; `Commands/ApproveInvoice/ApproveInvoiceHandler.cs:33-34` | D18 |
| BE-1 | `Wms.Domain/Entities/Service/Service.cs:17`, `:95-110`; `Wms.Infrastructure/Persistence/SeedDataExtensions.cs:30-33`, `:129-145`, `:497-505` | `VatPercent` con su semilla; salen `ServiceTaxes`, `SeedTaxes` y `SeedServiceTaxes` (D19) |
| BE-1 | Se borran: `Wms.Domain/Entities/Administration/Tax.cs`, `Entities/Service/ServiceTax.cs`, `Enums/TaxKind.cs`, `Configurations/Administration/TaxConfiguration.cs`, `Configurations/Service/ServiceTaxConfiguration.cs`, `Application/Administration/Queries/GetTaxes/*`, `Administration/Common/Mappers/TaxesMapper.cs`, el `TaxDto`, `Application/Services/Commands/AssignServiceTax/*` y `RemoveServiceTax/*`; `AppDbContext.cs:61`, `:277` | D19 |
| BE-1 | Las consultas con `.Include(s => s.ServiceTaxes)` (`git grep ServiceTaxes`: `StorageBillingService.cs:60`, `:326`; `BillingResolver.cs:85`; `ForeignTradeService.cs:67`; `ForkliftService.cs:73`, `:145`; `WeighbridgeService.cs:87`; `GetServiceByIdHandler.cs:20`; los seis handlers de cobro de báscula) | Sin el `Include`; `GetTotalTaxRate` sigue igual de firma |
| BE-1 | `Wms.Application/Warehouse/Common/Services/ForkliftService.cs:36-48`, `:142-163` | IVA de Montacargas desde su servicio (D19); `GetForkliftTaxRatePercentAsync` revisada |
| BE-1 | `Wms.Api/Controllers/v1/ServiceController.cs:105-115`, `:249-270`; `AdministrationController.cs:58-66` | C-F07-09 (nuevo), C-F07-10; retira C-F07-11 a C-F07-13 |
| BE-1 | `Wms.Application/Services/Common/Dtos/ServiceDto.cs`, `SetServicePriceRequest.cs`, `Common/Mappers/ServiceMapper.cs`, `Queries/GetAllServices/*` | `vatPercent`, `currentPrice` en la lista |
| BE-2 | `Wms.Domain/Entities/Agreement/Agreement.cs`, `AgreementService.cs` | Modelo de D22; `AgreementTariffTimeline` (nuevo, puro, en `Wms.Domain/Entities/Agreement/`) |
| BE-2 | Se borran: `Wms.Domain/Entities/Agreement/AgreementEffectivity.cs`, `Enums/AgreementStatus.cs`, `Wms.Application/Agreements/Services/*`, `Wms.Api/BackgroundJobs/AgreementActivationBackgroundService.cs` (y su registro), los comandos y consultas de `Wms.Application/Agreements/` que no use el recurso nuevo | D22 |
| BE-2 | `Wms.Application/Agreements/` (nuevo contenido): comandos y consultas de C-F07-14 a C-F07-18, DTO `AgreementTariffDto` y mapeador | D23, D25 |
| BE-2 | `Wms.Api/Controllers/v1/RatesAgreementsController.cs` (nuevo); `StakeholderController.cs:285-457` (salen los 12 endpoints) | C-F07-14 a C-F07-30 |
| BE-2 | `Wms.Application/Billing/Services/BillingResolver.cs:20-60`, `:168-200`; `IBillingResolver.cs` | Día de D21 y la línea de tiempo (D24) |
| BE-2 | `Wms.Application/ForeignTrade/Common/Services/ForeignTradeService.cs:30-39`; `Warehouse/Common/Services/ForkliftService.cs:83-94`; `Services/Commands/DeactivateService/DeactivateServiceHandler.cs:24-27`; `Common/Validation/StorageFormulaRestriction.cs:12-60` | D24, D27 |
| BE-2 | Los llamadores del resolver (`git grep ResolveAsync\|ResolveRuleAsync`): apertura y renovación del período (día de inicio), báscula, guía y montacargas (día del cobro) | D21 |
| BE-2 | `Wms.Infrastructure/Persistence/Configurations/Agreement/*` | Índices de §4 |
| BE-3 | `Wms.Domain/Billing/FormulaContext.cs` | `Trucks`, `RateIncludesVat` (D31, D20) |
| BE-3 | `Wms.Application/Billing/Calculators/` (nuevos): `UnloadedOrOnVehicleFormulaCalculator.cs`, `ValueThresholdFormulaCalculator.cs`, `WeightRateMinimumFormulaCalculator.cs`, `TieredFormulaCalculator.cs`, `TruckValueShares.cs` (reparto de D9, puro), `FormulaProration.cs` (fracción de D13, pura) | D29, D30 |
| BE-3 | `Wms.Application/Billing/Services/FormulaCalculatorRegistry.cs`, `FormulaPricing.cs` | Registro de las cuatro; `RateIncludesVat` en el contexto |
| BE-3 | `Wms.Application/Billing/Common/Services/StorageBillingService.cs` (armado del contexto), `StorageMagnitudeRules.cs`, `StorageInvoiceDetailFormatter.cs` | `Trucks` y advertencias de D32 |
| BE-3 | `Wms.Application/FormulaTypes/Common/Dtos/FormulaTypeDto.cs`, `FormulaParameterSchemaDto.cs`, `Queries/GetFormulaTypes/*`; `Wms.Domain/Entities/Billing/FormulaType.cs` (`FormulaParameterSchema`: `EnumLabels`, `VisibleWhen`); `Wms.Application/FormulaTypes/Common/FormulaSimulatorInputs.cs` (nuevo) | C-F07-31 |
| BE-3 | `Wms.Infrastructure/Persistence/SeedDataExtensions.cs:389-490` | Cuatro fórmulas sembradas y el rótulo de `thresholdKg` (D29, D36) |
| BE-3 | `Wms.Api/Controllers/v1/BillingPreviewController.cs:55-98`; `Wms.Application/Billing/Queries/PreviewFormula/*` | C-F07-32 |
| BE-3 | `Wms.Domain/Entities/Warehouse/WarehouseStorageEntry.cs`, `ReceptionLog.cs:29`, `:62` | Marca en la entrada (D33) |
| BE-3 | La recepción y la recepción directa de Bodega (`Wms.Application/Warehouse/Commands/…Reception…`), sus lecturas (C-F04-06, C-F04-09, C-F04-10) y `GET foreign-trade/warehouse-storages/{id}/entries` (C-F05-22) | C-F07-34 a C-F07-36 |
| BE-3 | `Wms.Api/Controllers/v1/ForeignTradeController.cs:418` (junto a C-F05-22); comando nuevo `SetEntryStaysOnVehicle` | C-F07-33 |
| BE-3 | `Wms.Application/Billing/Common/Services/StorageRecalculationTrigger.cs` | Disparo de D34 |
| BE-4 | `Wms.Application/Wms.Application.csproj` | ClosedXML (D37) |
| BE-4 | `Wms.Application/Agreements/Import/` (nuevo): `AgreementTemplateWorkbook.cs`, `AgreementTemplateReader.cs`, `AgreementImportRules.cs` (puro), comandos de vista previa y confirmación | C-F07-37 a C-F07-39 |
| BE-4 | `Wms.Api/Controllers/v1/RatesAgreementsController.cs` | Los tres endpoints de la plantilla |

`Wms.Application/Administration/LegacyImport/` no cambia (§7): `CustomersImporter.cs:61` sigue creando la configuración con un ciclo del catálogo (`LegacyBillingCycleMapper.cs:9-16` nunca produce `Monthly`). Si BE-1 cambia la firma de `StakeholderBillingConfiguration.Create` que usa, se ajusta la llamada y se corre la importación completa de ensayo (§7).

### 3.2 Frontend

| Fase | Archivo (`F/`, `FT/`) | Qué cambia |
| --- | --- | --- |
| FE-1 | `F/features/rates/contracts/billing-configuration.ts`, `forklift-rate.ts`; `services/billing-configuration.source.ts`, `forklift-rate.source.ts`; `mocks/` y `mocks/data/` | Nuevos |
| FE-1 | `F/features/billing/contracts/billing-recipient.ts` | Fragmentos de C-F07-05 y C-F07-07 |
| FE-1 | `F/pages/billing/configurations/index.vue` (rediseño en su ruta), `F/pages/billing/configurations/[customerId].vue` (nueva) | P-FAC-11 |
| FE-1 | `F/pages/admin/forklift-rates/index.vue` (rediseño) | Tarifas de montacargas |
| FE-1 | `F/features/rates/components/`: `BillingCycleField.vue`, `BillToExceptionDialog.vue`, `CustomerPickDialog.vue`, `ForkliftRateDialog.vue`, `WithholdingsTable.vue` (tabla editable con el selector) y `WithholdingsDialog.vue` (la del «Facturar a»); `services/withholding.source.ts` | Nuevos |
| FE-2 | `F/features/rates/contracts/agreement.ts`, `formula.ts`, `service-rates.ts` (la parte de modalidades); `services/agreement.source.ts`, `formula.source.ts`; mocks | Nuevos |
| FE-2 | `F/pages/rates/agreements/index.vue`, `F/pages/rates/agreements/[customerId].vue` | Nuevas |
| FE-2 | `F/features/rates/components/`: `TariffDialog.vue`, `FormulaParameterFields.vue`, `FormulaSimulator.vue`; `utils/formula-parameters.ts`, `tariff-summary.ts`, `tariff-status.ts` | Nuevos |
| FE-3 | `F/features/rates/contracts/agreement-import.ts`, `service-rates.ts` (resto); `services/agreement-import.source.ts`, `service-rate.source.ts`; mocks | Nuevos |
| FE-3 | `F/features/services/contracts/service.ts` | `vatPercent`, sin `taxSchema` (C-F07-08) |
| FE-3 | `F/pages/rates/services/index.vue`, `F/pages/rates/agreements/import.vue` | Nuevas |
| FE-3 | `F/features/rates/components/`: `ServicePriceDialog.vue`, `ServiceVatDialog.vue`, `ServiceMinimumDialog.vue`, `AgreementImportPreview.vue` | Nuevos |
| FE-1 a FE-3 | `FT/unit/guards/mock-sources.spec.ts` (`MAQUETACION_PAGES`: las seis páginas de la fase); `FT/unit/rates/mocks.spec.ts`; `FT/unit/rates/*.spec.ts` | Guardias y pruebas |
| I-07 | `F/features/rates/services/*.http.ts` (siete), `*.source.ts` (línea activa), `F/components/layout/menu-model.ts:171-180`, `FT/unit/guards/list-pattern-routes.ts:51-60`, `:113`, `FT/unit/guards/mock-sources.spec.ts:22`, `:30` | §13 |
| I-07 | `F/features/foreign-trade/components/DepositWarehouseStage.vue:98`, `contracts/deposit-entry.ts:76-90`; `F/features/warehouse/contracts/reception.ts`, `components/ReceptionDialog.vue` | D50 |
| I-07 | `F/features/stakeholders/components/StakeholderDetailSections.vue:18-29`, `:126-224`, `:264-311`; `F/pages/admin/stakeholders/index.vue`; `F/pages/admin/services/index.vue:14`, `:250` | D49 |
| I-07 | `F/features/audit/utils/entity-labels.ts` | Rótulos de `BillToException` y de la tarifa del acuerdo; salen los de `Tax` y `ServiceTax` |
| I-07 | Se borran (tras `grep`): §13.3 | — |

### 3.3 Docs

El plan, sus prompts, `D/planes/README.md`, la matriz y, al cerrar I-07, `D/qa/casos-qa2-f07-tarifas-acuerdos-AAAA-MM-DD.md` y los cambios al hub de §10 que el usuario apruebe.

---

## 4. Esquema y migraciones

Las genera y aplica el agente de backend con `dotnet ef`, solo en local (M6, `DEC-004`). Las bases locales se recrean (`DEC-006`): ninguna convierte datos.

| Fase | Migración | Contenido esperado, en orden |
| --- | --- | --- |
| BE-1 | `BillingBillToAndServiceVat` | 1) `stakeholder_billing_configurations`: `cycle_days` (int, nulo) y `bill_to_stakeholder_id` (uuid, nulo, FK a `stakeholders`, `Restrict`, índice). 2) Tabla `billing_bill_to_exceptions` (`id`, `billing_configuration_id` FK `Cascade`, `importer_id` FK `Restrict`, `bill_to_stakeholder_id` FK `Restrict`, `created_at`, `updated_at`), índice único (`billing_configuration_id`, `importer_id`). 3) `invoices.deposit_customer_id` (uuid, nulo, FK a `stakeholders`, `Restrict`, índice). 4) Tabla `stakeholder_withholdings` (`id`, `stakeholder_id` FK `Cascade`, `type` texto, `percent` numeric(7,4), `created_at`, `updated_at`), índice único (`stakeholder_id`, `type`). 5) `services.vat_percent` (numeric(5,2), no nulo, sin `HasDefaultValue` porque la tabla tiene `HasData`), con la semilla de D19. 6) Se borran `service_taxes` y `taxes` (con sus filas sembradas) |
| BE-2 | `AgreementTariffValidity` | 1) `agreements`: salen `reference`, `name`, `status`, `scheduled_activation_date`, `activation_date` y `archiving_date`, y el índice único filtrado de un convenio activo por cliente (`B/Wms.Infrastructure/Persistence/Configurations/Agreement/AgreementConfiguration.cs:54-57`, `status = 'Active'`); índice único `stakeholder_id`. 2) `agreement_services`: `valid_from` (date, no nulo), `valid_until` (date, nulo); sale `is_active`; índice único (`agreement_id`, `service_id`, `product_id`, `operation_modality_id`, `applies_to_perishable`, `valid_from`) con `NULLS NOT DISTINCT`, e índice (`agreement_id`, `service_id`, `valid_from`) |
| BE-3 | `StorageFormulasAndEntryVehicleMark` | 1) `formula_types`: cuatro filas sembradas (`UNLOADED_OR_ON_VEHICLE`, `VALUE_THRESHOLD`, `WEIGHT_RATE_MINIMUM`, `TIERED`, con Id fijos) y el rótulo nuevo de `thresholdKg` en `WEIGHT_THRESHOLD`; el esquema JSON suma `enumLabels` y `visibleWhen` donde aplican. 2) `warehouse_storage_entries.stays_on_vehicle` (boolean, no nulo, falso). 3) Sale `reception_logs.stays_on_vehicle` |
| BE-4 | ninguna | — |

`dotnet ef migrations has-pending-model-changes` limpio al cerrar cada fase.

---

## 5. Pruebas

| Proyecto | Prueba (nueva o ajustada) | Escenario | Fase |
| --- | --- | --- | --- |
| `Wms.Tests` | `BillingCycleCatalogTests`, `StoragePeriodCalculatorTests` (ajustadas) | Catálogo de D14; `Custom` con N; `Monthly` leído como 30; ventana de la consolidada | BE-1 |
| `Wms.Tests` | `BillToResolverTests` (nueva) | Excepción, general, sin configuración, importador nulo | BE-1 |
| `Wms.Tests` | `OverdueSweepTests` (ajustada) | Suma por `DepositCustomerId ?? CustomerId` | BE-1 |
| `Wms.Tests` | `StorageWithholdingsTests` (nueva) | Bases por tipo, redondeo, sin retenciones, IVA 0 | BE-1 |
| `Wms.Tests` | `StakeholderBillingConfigurationTests` (ajustada) | Reglas de `CycleDays` y de las excepciones | BE-1 |
| `Wms.IntegrationTests` | `BillingConfigurationTests` (ajustada), `BillToInvoiceTests`, `ServiceVatTests`, `WithholdingsTests` (nuevas) | C-F07-01 a C-F07-13 y C-F07-54 a C-F07-56; QA2-F07-001 a 014 y 051 | BE-1 |
| `Wms.Tests` | `AgreementTariffTimelineTests` (nueva) | Alta, reemplazo, posterior, retiro (programada y vigente), edición, estados, especificidad | BE-2 |
| `Wms.IntegrationTests` | `RatesAgreementsTests` (nueva); las de acuerdos de hoy se borran o se reescriben en sus *helpers* (`BillingScenario` y los que crean convenios) | C-F07-14 a C-F07-30, C-F07-44, C-F07-45; QA2-F07-015 a 023 | BE-2 |
| `Wms.Tests` | `UnloadedOrOnVehicleFormulaCalculatorTests`, `ValueThresholdFormulaCalculatorTests`, `WeightRateMinimumFormulaCalculatorTests`, `TieredFormulaCalculatorTests`, `TruckValueSharesTests` (nuevas) | Los valores de QA2-F07-025 a 031, con cero, mínimos, tramos, límite exacto y redondeo | BE-3 |
| `Wms.Tests` | `FormulaSchemaCalculatorParityTests` (nueva o ajustada) | Cada clave del esquema sembrado la lee su calculador y viceversa (trampa 2) | BE-3 |
| `Wms.IntegrationTests` | `StorageFormulasBillingTests`, `EntryStaysOnVehicleTests` (nuevas); `ReceptionTests` (ajustada) | C-F07-31 a C-F07-36; QA2-F07-024 a 035 | BE-3 |
| `Wms.Tests` | `AgreementImportRulesTests` (nueva) | Llaves, `outcome` por fila, repetidas, ciclos, fechas y números | BE-4 |
| `Wms.IntegrationTests` | `AgreementImportTests` (nueva; arma los `.xlsx` con ClosedXML en la prueba) | C-F07-37 a C-F07-39; QA2-F07-036 a 040 | BE-4 |
| Vitest | `FT/unit/rates/mocks.spec.ts` | Cada dato simulado pasa su esquema Zod | FE-1 a FE-3 |
| Vitest | `FT/unit/rates/formula-parameters.spec.ts`, `tariff-summary.spec.ts`, `tariff-status.spec.ts` | Esquema dinámico, `visibleWhen`, resumen «0,3 % · mín. $ 257.600», etiquetas de estado | FE-2 |
| Vitest | `FT/unit/rates/billing-cycle-field.spec.ts`, `withholdings-table.spec.ts`, `tariff-dialog.spec.ts`, `formula-simulator.spec.ts` | Días visibles solo con «Otro»; el selector no deja repetir una retención; solo los parámetros y los datos del simulador de la fórmula elegida | FE-1, FE-2 |
| Vitest | Guardias `list-pattern.spec.ts` y `mock-sources.spec.ts` | Rutas de F07 en `PATTERN` (I-07); `MAQUETACION_PAGES` con las páginas de la fase y vacía en I-07 | FE, I-07 |

---

## 6. Casos QA

Datos ficticios (`DEC-007`): «Cliente A» (NIT 900000001), «Comercial B» (900000002), «Comercial C» (900000003), «Importador X» (900000010), «Importador Y» (900000011). IVA de Almacenamiento 19 %. Los importes siguen `FormulaPricing` (unitario a 2 decimales y IVA a 2 decimales, `AwayFromZero`); con `BillingBasis.Flat` el unitario es el importe. «hoy» es el día de Colombia en que corre la prueba.

### 6.1 Parte 1 (API)

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F07-001 | AF-108, AF-115; D14 | — | C-F07-04 | Ocho opciones en el orden de la ficha, con `Custom` «Otro: N días» y `days: null`; sin `Monthly` | API (BE-1) |
| QA2-F07-002 | AF-108; D14 | Cliente A | C-F07-03 con `Custom` y 20; con `Custom` sin días; con `Days30` y 20; con `Monthly`; con `Custom` y 400 | 200 con `billingCycleLabel` «Otro: 20 días»; 400 «Digite los días del ciclo, de 1 a 360.»; 400 «Los días del ciclo solo aplican al ciclo «Otro».»; 400 «El ciclo de facturación no es válido.»; 400 «Digite los días del ciclo, de 1 a 360.» | API (BE-1) |
| QA2-F07-003 | AF-115; D14 | Cliente A con `Custom` 20; depósito con ingreso el 2026-12-01 | Confirmar el depósito (abre el período) | Período del 2026-12-01 al 2026-12-21, límite 2026-12-24; el siguiente empezaría el 2026-12-22 | API (BE-1) y `Wms.Tests` |
| QA2-F07-004 | M20; D14 | — | `StoragePeriodCalculator.ForStart(2026-02-01, Monthly, null)`; un cliente sin configuración abre un período el 2026-02-01 | Fin 2026-03-03 (30 días) en los dos | `Wms.Tests` y API (BE-1) |
| QA2-F07-005 | AF-112, AF-123; D15 | Cliente A; Comercial B; Comercial C; Importador X con rol Importador; Comercial B sin ese rol | C-F07-03 con «Facturar a» general B y excepción X → C; otra vez con X repetido; con excepción B → C; C-F07-02; C-F07-01 con `billToName=Comercial` y `sortField=billingCycle` | 200 y el detalle trae las dos cosas; 400 «El importador Importador X está repetido en las excepciones.»; 400 «El tercero Comercial B no tiene el rol Importador.»; la lista filtra y ordena, con `billToExceptionsCount: 1` | API (BE-1) |
| QA2-F07-006 | AF-123; D15, D16 | Configuración de 005; depósito D1 de Cliente A con importador X; D2 con importador Y; D3 de un cliente sin configuración | Confirmar los tres | Factura de D1 con destinatario C; D2 con B; D3 con su cliente; las tres con `depositCustomerId` = su cliente | API (BE-1) |
| QA2-F07-007 | AF-123; D16 | Cliente A con preferencia «Consolidada» y la configuración de 005; D1 (X) y D2 (Y) | Confirmar los dos | Dos facturas consolidadas en Borrador: una a C y otra a B | API (BE-1) |
| QA2-F07-008 | `DEC-056`; D16 | D2 con factura en Borrador; Comercial C es cliente con «Facturar a» general A | Cambiar el cliente de D2 a Comercial C | La factura pasa a `depositCustomerId` C y destinatario A, y se recalcula | API (BE-1) |
| QA2-F07-009 | AF-112; D17 | Factura de D1 en Borrador (destinatario C) | C-F07-05; C-F07-06 con B (el «Facturar a» general) | B y C aparecen con `billTo` (`General` y `Importer`); el cambio a B responde 200 | API (BE-1) |
| QA2-F07-010 | AF-112; D18 | Cliente A con 45 días de pago y sin límite de crédito; Comercial B con 10; factura de D2 (destinatario B) aprobada | Aprobar; mover el reloj hasta después del vencimiento; correr la mora | Vencimiento = aprobación + 45 días; Cliente A queda con mora (`OverdueWarning`) y Comercial B sigue `Active` | API (BE-1) |
| QA2-F07-011 | D3, D19 | Base recién migrada | C-F07-08 de los cinco servicios; C-F07-09 con 0 en Almacenamiento y una factura de período en Borrador recalculada; otra factura aprobada antes del cambio | 19, 19, 19, 0 y 0 (Almacenamiento, Báscula, Montacargas, Papelería, Guía); la línea recalculada lleva IVA 0; la aprobada conserva el 19 % de su línea | API (BE-1) |
| QA2-F07-012 | D19 | — | C-F07-10 con `vatPercent: 5`; otra vez sin `vatPercent`; C-F07-09 con 120 | El IVA del servicio queda en 5 y no cambia la segunda vez; 400 «El IVA debe estar entre 0 y 100 %.» | API (BE-1) |
| QA2-F07-013 | `P04/` D2; D19 | Montacargas con IVA 19 | Cobro del montacargas con «Requiere factura» por $100.000; sin factura; IVA del servicio en 5 y otro cobro con factura | IVA $19.000; IVA 0; IVA $5.000 | API (BE-1) |
| QA2-F07-014 | D19 | — | C-F07-11, C-F07-12 y C-F07-13 | 404 los tres | API (BE-1) |
| QA2-F07-015 | AF-114; D5, D23 | Cliente A sin acuerdo | C-F07-16: R1 Almacenamiento, todos los productos, importación, `PERCENTAGE_OF_VALUE_PRORATED` 0,3 % y mínimo 257.600, desde 2026-01-01; R2 igual desde hoy + 30; C-F07-15 | Se crea el acuerdo; R1 `Current` con `validUntil` = hoy + 29; R2 `Scheduled` sin fin; con `status=Ended` la lista sale vacía | API (BE-2) y `Wms.Tests` |
| QA2-F07-016 | D23 | Lo de 015 | C-F07-16 con el mismo ámbito y la fecha de R2; otra de producto Cebolla desde 2026-01-01 | 409 «Ya hay una tarifa de Almacenamiento en Bodega con ese producto, modalidad y perecedero desde el {fecha}.»; 201, y un depósito de Cebolla toma esa (especificidad) | API (BE-2) |
| QA2-F07-017 | D23 | Lo de 015 | C-F07-17 de R1 cambiando el porcentaje; de R1 con otra `validFrom`; de R2 con `validFrom` = hoy + 40 | 200; 409 «La vigencia de una tarifa que ya rige no se cambia: agregue una nueva desde la fecha que quiere.»; 200 y R1 termina en hoy + 39 | API (BE-2) |
| QA2-F07-018 | D23 | Lo de 017 | C-F07-18 de R2; de R1; otra vez de R1 | `Deleted` y R1 vuelve a no tener fin; `Ended` con `validUntil` = hoy; 409 «La tarifa ya terminó el {hoy}.» | API (BE-2) |
| QA2-F07-019 | D21, D23 | R1 desde 2026-01-01 a 0,3 % y R3 del mismo ámbito desde hoy a 0,4 %; un período que empezó ayer en Borrador | Recalcular la factura de ese período; abrir un período que empieza hoy | El de ayer cobra con R1 (0,3 %); el de hoy con R3 (0,4 %) | API (BE-2) |
| QA2-F07-020 | AF-117 (H5b); D24 | Cliente A con tarifa de Báscula `FIXED` 0 vigente; Guía `FIXED` 12.000 programada para mañana | Pesaje de un camión de Cliente A; cobro de la guía hoy; desactivar el servicio Báscula | Tiquete en $0 «sin cobro por convenio» (`DEC-057` H5b); la guía cobra la tarifa base de hoy (la programada aún no rige); la desactivación responde el error de hoy por tener tarifas vigentes o programadas | API (BE-2) |
| QA2-F07-021 | D25 | Clientes A y B con tarifas | C-F07-14 con `customerName=Cliente`, `sortField=currentCount&sortOrder=desc` | Cliente A con sus conteos y `lastValidFrom`; filtro y orden aplicados | API (BE-2) |
| QA2-F07-022 | D22 | — | C-F07-19 a C-F07-30; `git grep AgreementActivation` | 404 los doce; sin resultados fuera de `Migrations/` | API (BE-2) |
| QA2-F07-023 | D27 | — | C-F07-16 con Báscula y `TIERED`; C-F07-44 con Guía y `VALUE_THRESHOLD`; C-F07-16 con Almacenamiento y `PER_VEHICLE_TYPE` | 400 «La fórmula «Por tramos» solo aplica al servicio de Almacenamiento.»; 400 «La fórmula «Según el valor» solo aplica al servicio de Almacenamiento.»; 400 con el mensaje de hoy | API (BE-2) |
| QA2-F07-024 | AF-116, AF-118; D29, D35, D36 | — | C-F07-31 | Las cuatro fórmulas con los parámetros, `enumLabels` y `visibleWhen` de la ficha, `serviceScope: StorageOnly` y sus `simulatorInputs`; `thresholdKg` con «Umbral de peso de mercancía (kg)»; `PER_UOM` como C-F01-77 | API (BE-3) |
| QA2-F07-025 | AF-120; D9, D20, D30 | `UNLOADED_OR_ON_VEHICLE` 0,3 % y $168.000 por vehículo; CPI $200.000.000 | C-F07-32: (A1) camiones 60.000 y 40.000 descargados; (A2) 60.000 descargado y 40.000 sobre vehículo; (A3) como A2 con `taxIncluded: true` | A1: 600.000,00 + IVA 114.000,00 = 714.000,00. A2: 360.000 + 168.000 = 528.000,00 + 100.320,00 = 628.320,00. A3: 501.176,47 + 95.223,53 = 596.400,00 | API (BE-3) y `Wms.Tests` |
| QA2-F07-026 | AF-120; D2, D30 | CPI $20.000.000; camiones 6.000 y 2.000 descargados y 2.000 sobre vehículo; mínimo 257.600 con IVA | C-F07-32 con `minimumScope` `UnloadedPart`, `PerUnloadedTruck` y `Total`; y con un solo camión de 5.000 sobre el vehículo (`UnloadedPart`) | UnloadedPart: 384.470,59 + 73.049,41 = 457.520,00 (mínimo aplicado). PerUnloadedTruck: 600.941,18 + 114.178,82 = 715.120,00. Total: 216.470,59 + 41.129,41 = 257.600,00. Solo sobre vehículo: 168.000,00 + 31.920,00 = 199.920,00 (sin mínimo) | API (BE-3) y `Wms.Tests` |
| QA2-F07-027 | M19; D9, D13, D32 | 0,3 % y $168.000 | C-F07-32: (A5) CPI 100.000.000 sin camiones; (A6) CPI 100.000.000, un camión descargado y otro sobre vehículo, sin precios; (A7) CPI 100.000.000, 60.000 descargado, uno sin precio descargado y 40.000 sobre vehículo; (A8) como A2 con saldo 50 de 100 (`prorated` verdadero y falso) | A5: 300.000,00 + 57.000,00 = 357.000,00. A6: 318.000,00 + 60.420,00 = 378.420,00. A7: 348.000,00 + 66.120,00 = 414.120,00 con la advertencia «1 camión descargado sin precio: cuenta $0 en el cobro por camión.». A8: 348.000,00 (prorrateado) y 528.000,00 (sin prorrateo) | API (BE-3) y `Wms.Tests` |
| QA2-F07-028 | AF-116; D13, D30 | `VALUE_THRESHOLD`: límite $300.000.000, `PerCargoUnit` CONTENEDOR $276.000, 0,2 % por encima | C-F07-32: (B1) CPI 250.000.000 y 2 contenedores; (B2) CPI 300.000.000 y 2; (B3) CPI 400.000.000; (B4) CPI 400.000.000 con saldo 30 de 100; (B5) `Fixed` $300.000 con límite 128.400.000 y CPI 100.000.000; (B6) B1 con `taxIncluded: true` | B1: 552.000,00 + 104.880,00 = 656.880,00 (el resultado del wireframe P-FAC-13). B2 igual a B1 (el límite va con la regla de abajo). B3: 800.000,00 + 152.000,00 = 952.000,00. B4: 240.000,00 + 45.600,00 = 285.600,00 (se compara con el CPI completo). B5: 300.000,00 + 57.000,00 = 357.000,00. B6: 463.865,55 + 88.134,45 = 552.000,00 | API (BE-3) y `Wms.Tests` |
| QA2-F07-029 | AF-113, AF-116; D30 | `WEIGHT_RATE_MINIMUM` $4.700 por tonelada, mínimo 55.000 con IVA | C-F07-32: (C1) 30.000 kg; (C2) 8.000 kg; (C3) $15 por kilo, mínimo 0 y 20.000 kg; (C4) C1 con saldo 50 de 100; (C5) sin peso | C1: 141.000,00 + 26.790,00 = 167.790,00. C2: 46.218,49 + 8.781,51 = 55.000,00 (mínimo). C3: 300.000,00 + 57.000,00 = 357.000,00. C4: 70.500,00 + 13.395,00 = 83.895,00. C5: el mínimo, 55.000,00 en total | API (BE-3) y `Wms.Tests` |
| QA2-F07-030 | AF-116; D1, D12, D30 | `TIERED` por peso en kg, límite 10.000, $9 hasta y $10 desde | C-F07-32: (D1a) 8.000 kg; (D1b) 12.000 kg `WholeQuantity`; (D1c) 12.000 kg `Excess`; (D1d) 10.000 kg `Excess`; (D3) 12.000 kg con saldo 50 de 100 | D1a: 72.000,00 + 13.680,00 = 85.680,00. D1b: 120.000,00 + 22.800,00 = 142.800,00. D1c: 110.000,00 + 20.900,00 = 130.900,00. D1d: 90.000,00 + 17.100,00 = 107.100,00 (el límite es del primer tramo). D3: 54.000,00 + 10.260,00 = 64.260,00 | API (BE-3) y `Wms.Tests` |
| QA2-F07-031 | D12, D20, D30 | `TIERED` por vehículos, límite 2, $250.000 hasta y $178.000 desde | C-F07-32: (D2a) 2 vehículos; (D2b) 3 `WholeQuantity`; (D2c) 3 `Excess`; (D2d) D2b con `taxIncluded: true` | D2a: 500.000,00 + 95.000,00 = 595.000,00. D2b: 534.000,00 + 101.460,00 = 635.460,00. D2c: 678.000,00 + 128.820,00 = 806.820,00. D2d: 448.739,50 + 85.260,51 = 534.000,01 (el redondeo del IVA incluido, igual que `FIXED` hoy) | API (BE-3) y `Wms.Tests` |
| QA2-F07-032 | AF-85, AF-94, AF-120; D9, D31 | Depósito de Cliente A en USD con CPI 50.000 USD y tasa de la semana 4.000 (CPI $200.000.000); camiones con precio 30.000 (descargado, recibido) y 20.000 (recibido con «Queda sobre el vehículo»); tarifa del acuerdo de 025 | Confirmar el depósito | La línea de almacenamiento cobra 528.000,00 + IVA 100.320,00 (igual que A2) y el detalle no lleva advertencias | API (BE-3) |
| QA2-F07-033 | D10, D11, D33, D34 | El depósito de 032 con los dos camiones descargados (factura en Borrador por 600.000,00) | C-F07-33 sobre el segundo camión con `true`; C-F07-34; C-F07-33 sobre una entrada anulada; sobre un depósito Cerrado | 200 con `recalculated: true` y la factura queda en 528.000,00; la entrada trae `staysOnVehicle: true` y `canMarkStaysOnVehicle: true`, sin moverse de su ubicación; 409 «La entrada está anulada.»; 409 «El depósito {N} está Cerrado: ya no se edita.» | API (BE-3) |
| QA2-F07-034 | AF-119; D10, D11, D33 | Entrada pendiente marcada por CE (C-F07-33); otra entrada pendiente sin marca; el depósito cobra con `UNLOADED_OR_ON_VEHICLE` | C-F07-35; C-F07-36 de la marcada con `staysOnVehicle: true`; C-F07-36 de la otra con `false`; C-F04-10 | La marcada viene con `staysOnVehicle: true`; la recepción ubica en `SOBRE-VEHICULO` y no recalcula (la marca no cambió); la otra no recalcula; el detalle lee la marca de la entrada | API (BE-3) |
| QA2-F07-035 | AF-117; D25 | Cliente A con tarifas `PER_CARGO_UNIT` TANQUERO $240.800 con IVA incluido y papelería; `PER_UOM` $145 | C-F07-32 de `PER_CARGO_UNIT` con 1 tanquero e IVA incluido; de `PER_UOM` con 40; confirmar un depósito de un tanquero | 202.352,94 + 38.447,06 = 240.800,00; 5.800,00 + 1.102,00 = 6.902,00; la factura lleva además la línea de Papelería con el precio base de Papelería | API (BE-3) |
| QA2-F07-036 | AF-114; D38, D39 | Cliente A con configuración, una excepción y dos tarifas | C-F07-37 sin cliente; con Cliente A; con un Id que no existe | Archivo con las hojas «Instrucciones», «Clientes», «Facturar a», «Retenciones», «Tarifas» y «Catálogos» y las claves de fila 2 de la ficha; el de Cliente A trae sus filas (tarifas vigentes y programadas, y las retenciones suyas y de sus «Facturar a»); 404 «No existe el cliente {id}.» | API (BE-4) |
| QA2-F07-037 | AF-114; D40, D41 | Lo de 015 | C-F07-38 con un archivo de seis filas de Tarifas: una nueva desde hoy + 60, una igual a R1, una que reemplaza R1 desde hoy + 10, una con NIT 900000099, una sin `percentage`, y la tercera repetida | `NewScheduled`, `Unchanged`, `Replaces` («Reemplaza desde {fecha}»), `Error` «El NIT 900000099 no existe: créelo antes en Configuración › Terceros.», `Error` «Parámetro inválido: 'percentage' …», `Error` «Fila repetida: la fila 5 ya trae esa tarifa con la misma fecha.»; nada guardado (C-F07-15 igual) | API (BE-4) |
| QA2-F07-038 | AF-114; D40 | El archivo de 037 | C-F07-39; otra vez C-F07-39; C-F07-15 | `applied.tariffs: 2` y las filas con error sin cargar; la segunda vez todas `Unchanged` (las de error siguen en error); las tarifas quedan como dice la línea de tiempo | API (BE-4) |
| QA2-F07-039 | D39 | — | C-F07-38 sin archivo; con un `.csv`; con 6 MB; sin la hoja «Tarifas»; sin la columna `validFrom`; con 2.001 filas | Los seis 400 de la ficha, con su mensaje | API (BE-4) |
| QA2-F07-040 | AF-108; D40 | Cliente A y Comercial B | C-F07-39 con «Clientes»: A con 20 días y «Facturar a» B; B con 30 días; una fila con 0 días; y «Facturar a»: A, X → C | A queda `Custom` 20 con «Facturar a» B; B queda `Days30`; error «Los días del ciclo deben estar entre 1 y 360.»; la excepción X → C se crea o se actualiza | API (BE-4) |
| QA2-F07-051 | D52 a D55 | Comercial B (no es cliente) es el «Facturar a» general de Cliente A | C-F07-54; C-F07-56 de Comercial B con Retefuente 2,5, ReteICA 0,966 y ReteIVA 15; otra vez con Retefuente repetida; con ReteICA en 0; C-F07-55 de B; C-F07-02 de A; `StorageWithholdings` con subtotal 528.000,00 e IVA 100.320,00 | Tres tipos con su base; 200; 400 «La retención «Retención en la fuente» está repetida.»; 400 «El porcentaje de «ReteICA» debe ser mayor que 0 y hasta 100.»; las tres de B; A trae a B como `billTo` con sus tres retenciones; cálculo: Retefuente 13.200,00, ReteICA 5.100,48 y ReteIVA 15.048,00, en total 33.348,48 (neto a recibir de 628.320,00: 594.971,52) | API (BE-1) y `Wms.Tests` |
| QA2-F07-052 | D40, D52, D53 | Comercial B sin retenciones | C-F07-38 y C-F07-39 con «Retenciones»: B con «Retención en la fuente» 2,5; B con «ReteICA» sin porcentaje; B con «Retencion IVA»; B con «ReteIVA» 15 | La primera y la cuarta, `New`; la segunda, `Error` «Falta el porcentaje.»; la tercera, `Error` «La retención «Retencion IVA» no existe: use Retención en la fuente, ReteICA o ReteIVA.»; después de confirmar, C-F07-55 de B trae Retefuente 2,5 y ReteIVA 15 | API (BE-4) |

### 6.2 Integración I-07 (navegador)

Contra el backend local real (puerto 5281), sin la sesión simulada, con usuarios de prueba por rol (`Frontend/wms/README.md`; sus contraseñas no se copian).

| ID | Regla de origen | Precondición | Pasos | Resultado esperado | Verificación |
| --- | --- | --- | --- | --- | --- |
| QA2-F07-041 | AF-127; D42 | Usuarios Admin, Facturación y CE | Abrir el menú con cada uno | Admin y Facturación ven «Tarifas y acuerdos» con Acuerdos, Configuración de facturación, Tarifas de servicios y Tarifas de montacargas; CE no la ve; las cuatro rutas pasan la guardia `PATTERN` | Pantalla |
| QA2-F07-042 | AF-108, AF-123; D43 | Facturación | Configuración de facturación: «+ Nueva configuración» para Cliente A; «Otro» con 20 días, 30 de pago, «Facturar a» con alta rápida de un tercero nuevo, dos excepciones; «Guardar»; volver al listado y filtrar por ciclo | Guarda; el listado muestra «Otro: 20 días», el «Facturar a» y 2 excepciones; los días del ciclo solo aparecen con «Otro» | Pantalla y API |
| QA2-F07-043 | AF-114, AF-117, AF-118; D44, D45 | Facturación; Cliente A | P-FAC-12: «+ Agregar tarifa» con cada fórmula nueva (simulador con los datos de 025 A2, 028 B1, 029 C1 y 031 D2b), una de Báscula `FIXED` $0 y una de `PER_UOM`; editar una; retirar una programada y una vigente; filtrar por fórmula y por estado | El simulador da 628.320,00, 656.880,00, 167.790,00 y 635.460,00 de total; la tabla muestra resumen, papelería, IVA incluido, vigencia y estado; retirar quita la programada y termina hoy la vigente | Pantalla y API |
| QA2-F07-044 | AF-118, H-063; D45 | El diálogo abierto | Cambiar de fórmula entre las doce | Solo aparecen los parámetros de la elegida (con `visibleWhen`) y solo los datos del simulador de su `simulatorInputs`; las de Almacenamiento no salen para Báscula | Pantalla |
| QA2-F07-045 | AF-114; D46 | Facturación | «Descargar plantilla» (vacía y de Cliente A); llenarla con una fila nueva, una con NIT inexistente y una de «Clientes»; «Importar plantilla» → vista previa → «Confirmar importación» | Vista previa con «Nueva, programada», el error del NIT y la de clientes; «2 filas válidas · 1 con error (no se cargan)»; después de confirmar, P-FAC-12 muestra la nueva y la configuración cambió | Pantalla y API |
| QA2-F07-046 | D3, D26, D47 | Facturación | Tarifas de servicios: Báscula «+ Nuevo precio» con IVA 19 y $16.806,72 (precio + IVA $20.000,00); «Editar IVA» de Papelería en 19; en Almacenamiento, una tarifa base `VALUE_THRESHOLD` con el diálogo en modo base; editar un mínimo | Guarda; el listado muestra el IVA y el precio vigente; la regla aparece en «Tarifas por fórmula»; Configuración › Servicios ya no tiene sección «Impuestos» | Pantalla y API |
| QA2-F07-047 | AF-129; D48 | Facturación | Tarifas de montacargas: editar «Sencillo» a $140.000 | Se guarda; la tabla ordena y la barra muestra el IVA de Montacargas | Pantalla y API |
| QA2-F07-048 | AF-119, AF-120; D10, D11, D50 | Depósito de 032 con el segundo camión pendiente de recepción; CE | Etapa Bodega: activar «Queda sobre el vehículo» en el segundo camión; abrir la factura del período; con Bodega, abrir Recepción | El switch se guarda y la factura pasa a 528.000,00; la fila de Recepción trae el switch activo; el usuario de Bodega no ve el switch de CE | Pantalla y API |
| QA2-F07-049 | D7, D49 | Facturación y CE | Detalle del tercero Cliente A y del servicio Almacenamiento | Sin secciones de acuerdos ni de tarifas; «Ver acuerdo» y «Ver tarifas» en «Acciones» llevan a sus páginas; CE no ve esas acciones | Pantalla |
| QA2-F07-050 | AF-112; D16, D18 | Factura de almacenamiento de D2 (destinatario Comercial B) aprobada y vencida | Abrir la factura; correr la mora; tablero de Facturación | La factura muestra a Comercial B como destinatario; la mora aparece en Cliente A | Pantalla y API |
| QA2-F07-053 | D52, D53 | Facturación; Cliente A con «Facturar a» general Comercial B | P-FAC-11 de Cliente A: agregar Retefuente 2,5 % al cliente y «Guardar»; en la fila de Comercial B, «Retenciones» → ReteIVA 15 %; intentar agregar otra Retefuente al cliente | El listado muestra «Retefuente 2,5 %» en Cliente A; la fila de B muestra «ReteIVA 15 %» sin tocar la configuración de A; el selector no ofrece una retención ya agregada; la base se ve según el tipo | Pantalla y API |

---

## 7. Transición de datos

Lo que le toca de `PM/` §7.2:

| Dato | Qué se hace | Decisión |
| --- | --- | --- |
| Ciclo «mes calendario» | El importador no lo produce (`B/Wms.Application/Administration/LegacyImport/Common/LegacyBillingCycleMapper.cs:9-16` solo da 15, 30, 90, 180 y 360 días) y la opción sale del catálogo. Una fila que lo traiga se lee como 30 días; el ciclo por omisión pasa a `Days30`. En local no hay nada que convertir | M20; D14 |
| Acuerdos | La carga inicial va con la plantilla (C-F07-39), con el borrador de T-1 (§14) revisado por Facturación, en el paso 4 del despliegue final (`PM/` §7.3). Reemplaza la fase 4b pendiente de `DEC-043` | AF-114; D4 |
| IVA | La semilla de D19 deja el IVA de cada servicio; en el despliegue final, Facturación lo confirma en Tarifas de servicios junto con las tarifas base de `DEC-041` | D19 |
| Retenciones | T-1 pone en la hoja «Retenciones» del borrador las que la observación de la hoja 2026 nombra para cada «Facturar a», sin porcentaje (el Excel no lo trae); Facturación completa los porcentajes antes de importar | D4, D52, D53 |
| Impuestos y convenios de hoy | No se convierten: las bases locales se recrean (`DEC-006`) y staging se recrea en el despliegue final (M17) | M17, M18 |

**Importador del legacy:** no cambia de comportamiento. La configuración del cliente sigue naciendo con un ciclo del catálogo y sin «Facturar a» (`B/Wms.Application/Administration/LegacyImport/Importers/CustomersImporter.cs:61`). Si BE-1 cambia la firma de `StakeholderBillingConfiguration.Create`, ajusta la llamada y corre la importación completa de ensayo, como la fase 6 de F01 (`P01/` §8, nota de la fase 6): los 12 CSV de `db_legacy/trabajo/csv` en una base recreada, en la base de la rama y en la de `fase-2`, con conteos iguales (clientes y sus configuraciones incluidos); sin cambio de firma, no hace falta.

---

## 8. Fases por parte

| Fase | Parte | Contenido | Criterio de salida | Estado |
| --- | --- | --- | --- | --- |
| BE-1 | 1 | Configuración, «Facturar a», retenciones, mora e IVA (§8.1) | QA2-F07-001 a 014 y 051 en PASA; migración `BillingBillToAndServiceVat` | Pendiente |
| BE-2 | 1 | Acuerdos con vigencia por tarifa (§8.2) | QA2-F07-015 a 023 en PASA; migración `AgreementTariffValidity` | Pendiente |
| BE-3 | 1 | Fórmulas nuevas, simulador y marca «Queda sobre el vehículo» (§8.3) | QA2-F07-024 a 035 en PASA; migración `StorageFormulasAndEntryVehicleMark` | Pendiente |
| BE-4 | 1 | Plantilla e importación (§8.4) | QA2-F07-036 a 040 y 052 en PASA; sin migración | Pendiente |
| FE-1 | 2 | Configuración de facturación y tarifas de montacargas (§8.5) | Pantallas con su wireframe y captura; datos simulados con su Zod | Pendiente |
| FE-2 | 2 | Acuerdos con «Agregar tarifa» y simulador (§8.6) | Igual | Pendiente |
| FE-3 | 2 | Tarifas de servicios y plantilla (§8.7) | Igual | Pendiente |
| Revisión | — | Del usuario, con la sesión simulada (§8.8) | Visto bueno o plan de ajustes | Pendiente |
| I-07 (1) | 3 | Fuentes http, pantallas nuevas y marca en CE y Bodega (§13.1) | QA2-F07-042 a 048 y 053 en PASA | Pendiente |
| I-07 (2) | 3 | Menú, detalles, guardias, retiro de lo viejo, casos QA y fusión (§13.2) | QA2-F07-041, 049 y 050 en PASA; fusión en `fase-2` | Pendiente |
| T-1 | 3 | Borrador de la carga inicial, fuera de git (§14) | Borrador y su informe en cifras | Pendiente |

Toda fase cierra con las compuertas de `PM/` §6 (cifras antes y después), commit con el mensaje de §12 y push. BE-1 a BE-4 corren en serie en el backend y FE-1 a FE-3 en serie en el frontend, en paralelo entre los dos repos.

### 8.1 Backend, fase 1 — Configuración, «Facturar a», mora e IVA

- **Decisiones:** D3, D14 a D19, D52 a D55; D28 (permisos).
- **Endpoints:** C-F07-01 a C-F07-13 y C-F07-54 a C-F07-56 (§2.2, grupos A, B y G).
- **Archivos:** §3.1, filas BE-1.
- **Migración:** `BillingBillToAndServiceVat` (§4).
- **Pruebas:** §5, filas BE-1. **Casos:** QA2-F07-001 a 014 y 051.
- **Notas:** el destinatario se calcula al abrir, renovar y refacturar (D16), no al recalcular. `GetTotalTaxRate` conserva la firma para no tocar a sus llamadores más allá del `Include`. La revisión de `GetForkliftTaxRatePercentAsync` (D19) se informa en el reporte con sus usos. Las retenciones no tocan todavía la factura: F07 deja la configuración y `StorageWithholdings`; guardarlas en la factura y restarlas del saldo es de F08 (D54). Si cambia la firma que usa el importador del legacy, corre la importación de ensayo (§7).
- **Estado:** Pendiente.

### 8.2 Backend, fase 2 — Acuerdos con vigencia por tarifa

- **Decisiones:** D5, D21 a D27.
- **Endpoints:** C-F07-14 a C-F07-30, C-F07-44 y C-F07-45 (§2.2, grupos C y F).
- **Archivos:** §3.1, filas BE-2.
- **Migración:** `AgreementTariffValidity` (§4).
- **Pruebas:** §5, filas BE-2. Las pruebas de integración que crean convenios con los endpoints de hoy se ajustan en sus *helpers*, no prueba por prueba (`P01/` §0.5). **Casos:** QA2-F07-015 a 023.
- **Notas:** el día de D21 lo pasan los llamadores; el job de renovación y la apertura usan el día de inicio del período; los cobros de báscula, guía y montacargas, el día de Colombia del cobro. `git grep AgreementStatus` sin resultados fuera de `Migrations/` al cerrar.
- **Estado:** Pendiente.

### 8.3 Backend, fase 3 — Fórmulas nuevas, simulador y marca «Queda sobre el vehículo»

- **Decisiones:** D1, D2, D9 a D13, D20, D29 a D36.
- **Endpoints:** C-F07-31 a C-F07-36 (§2.2, grupo D).
- **Archivos:** §3.1, filas BE-3.
- **Migración:** `StorageFormulasAndEntryVehicleMark` (§4).
- **Pruebas:** §5, filas BE-3; cada calculador con los valores de QA2-F07-025 a 031 escritos en la prueba. **Casos:** QA2-F07-024 a 035.
- **Notas:** la paridad esquema-calculador (trampa 2) se prueba para las doce fórmulas. La marca sale de `ReceptionLog` en la misma migración en que entra a la entrada: la recepción y su detalle se ajustan en esta fase (C-F07-36). El recálculo de D34 usa el mismo disparo que `P05/` D19, después del commit.
- **Estado:** Pendiente.

### 8.4 Backend, fase 4 — Plantilla e importación

- **Decisiones:** D6, D37 a D41 (con la hoja «Retenciones», D52 y D53).
- **Endpoints:** C-F07-37 a C-F07-39 (§2.2, grupo E).
- **Archivos:** §3.1, filas BE-4.
- **Migración:** ninguna. **Paquete:** ClosedXML (D37); anota la versión en el reporte.
- **Pruebas:** §5, filas BE-4. **Casos:** QA2-F07-036 a 040 y 052.
- **Notas:** las pruebas arman sus `.xlsx` con ClosedXML y datos ficticios. Ninguna prueba ni ejemplo usa datos del Excel de convenios (§0.9).
- **Estado:** Pendiente.

### 8.5 Maquetación, fase 1 — Configuración de facturación y tarifas de montacargas

- **Decisiones:** D14, D15 (en pantalla), D42, D43, D48, D51, D52, D53.
- **Contratos y fuentes:** `billing-configuration.ts`, `forklift-rate.ts`, los fragmentos de `billing-recipient.ts` (§2.3); fuentes simuladas de C-F07-01 a C-F07-04, C-F07-54 a C-F07-56, C-F07-08 (solo Montacargas) y C-F07-50 a C-F07-52; C-F01-25, C-F01-26 y C-F01-141 simulados con las ayudas de `F/shared/mocks/`.
- **Pantallas:** `/billing/configurations` (listado), `/billing/configurations/[customerId]` y `/admin/forklift-rates`. Componentes compartidos: `AppDataTable`, `AppSearchSelect`, `AppCrudDialog`, `AppRowActions`. Nuevos: `BillingCycleField`, `BillToExceptionDialog`, `CustomerPickDialog`, `ForkliftRateDialog`, `WithholdingsTable`, `WithholdingsDialog`.
- **Guardias:** las tres páginas en `MAQUETACION_PAGES`; ninguna ruta nueva en el menú.
- **Pruebas:** `FT/unit/rates/mocks.spec.ts` (lo de la fase), `billing-cycle-field.spec.ts`, `withholdings-table.spec.ts`.
- **Cierre:** captura de cada pantalla con `?roles=Admin,Billing`.
- **Estado:** Pendiente.

### 8.6 Maquetación, fase 2 — Acuerdos con «Agregar tarifa» y simulador

- **Decisiones:** D9, D12, D13, D29 (en pantalla), D35, D44, D45.
- **Contratos y fuentes:** `agreement.ts`, `formula.ts` y la parte de modalidades de `service-rates.ts` (§2.3); fuentes simuladas de C-F07-14 a C-F07-18, C-F07-31, C-F07-32 (el simulado calcula con las reglas de D30 lo justo para los valores de QA2-F07-025 a 031) y C-F07-53; C-F01-33 y C-F01-69 simulados.
- **Pantallas:** `/rates/agreements` y `/rates/agreements/[customerId]`, con el diálogo P-FAC-13 en modo acuerdo. Nuevos: `TariffDialog`, `FormulaParameterFields`, `FormulaSimulator`; utilidades `formula-parameters.ts`, `tariff-summary.ts`, `tariff-status.ts`.
- **Guardias, pruebas y cierre:** como §8.5, con `formula-parameters.spec.ts`, `tariff-summary.spec.ts`, `tariff-status.spec.ts`, `tariff-dialog.spec.ts` y `formula-simulator.spec.ts`.
- **Estado:** Pendiente.

### 8.7 Maquetación, fase 3 — Tarifas de servicios y plantilla

- **Decisiones:** D3, D19 (en pantalla), D26, D38 a D40 (en pantalla), D46, D47.
- **Contratos y fuentes:** `agreement-import.ts`, el resto de `service-rates.ts` y el cambio de `F/features/services/contracts/service.ts` (§2.3); fuentes simuladas de C-F07-08 a C-F07-10, C-F07-37 a C-F07-49 (la descarga devuelve un `Blob` ficticio; la importación, resultados fijos con los seis `outcome`).
- **Pantallas:** `/rates/services` (con su drawer y el diálogo de D45 en modo base) y `/rates/agreements/import`. Nuevos: `ServicePriceDialog`, `ServiceVatDialog`, `ServiceMinimumDialog`, `AgreementImportPreview`.
- **Ojo:** Configuración › Servicios (`F/pages/admin/services/index.vue`, integrada) usa `serviceSchema`; el cambio de `taxes` por `vatPercent` no debe romperla: si la página lee `taxes`, deja ese uso para I-07 y lo anotas.
- **Guardias, pruebas y cierre:** como §8.5. Al cerrar, dile al usuario qué rutas abrir y con qué roles (§8.8).
- **Estado:** Pendiente.

### 8.8 Revisión del usuario (después de FE-3)

Con FE-1 a FE-3 cerradas y con push, el usuario revisa las pantallas en `yarn dev` con la sesión simulada (`?roles=Admin,Billing` y `?roles=Billing`) antes de I-07. Si pide ajustes, van en un plan de ajustes de la maquetación, como en F03 y F04, y se ejecutan en `f2/f07-tarifas-acuerdos` antes de I-07.

---

## 9. Riesgos

| # | Riesgo | Mitigación |
| --- | --- | --- |
| R1 | F06 se planea a la vez: su plan propuesto (`D/planes/sprint-11/f06-salidas/plan-cerrado-f2-f06-salidas-2026-11-26.md`, D4 y C-F06-06) sugiere el precio de la guía con `IForeignTradeService.GetGuidePriceAsync` y le suma si salió del convenio o del precio general, y cambia el cobro de la guía (`AppChargeForm`, `BillingCollectForm`) y la etapa Salidas del detalle de CE | F07 empieza después de I-06 y confirma las líneas (§0.3). F07 solo cambia cómo se elige la tarifa vigente dentro de `GetGuidePriceAsync` (D24), sin tocar su firma ni el origen que F06 le agregue, ni el cobro ni sus pantallas; si F06 movió la consulta, el agente se detiene y pregunta |
| R2 | El detalle de CE lo tocan F05 (integrado), F06 (etapa Salidas) y F07 (etapa Bodega, D50) | Van en serie; I-07 confirma `DepositWarehouseStage.vue` con `grep` antes de cambiar |
| R3 | Retirar el catálogo de impuestos toca unas 15 consultas y seis cobros de báscula | `GetTotalTaxRate` conserva su firma; QA2-F07-011 a 013 y la suite completa de BE-1 |
| R4 | El modelo nuevo de acuerdos rompe las pruebas que crean convenios (20 archivos de prueba los citan) | Se ajustan en sus *helpers* (§8.2); `AgreementTariffTimelineTests` cubre las reglas |
| R5 | Las fórmulas por peso cobran el peso completo si `prorated` es falso, aunque salga mercancía | `prorated` es verdadero por omisión (D13); Facturación lo verifica en el mes en paralelo (`DEC-029` §7.10) |
| R6 | Un camión sin recepción cuenta como descargado y la factura cambia al recibirlo | Advertencia en el detalle (D32) y recálculo con aviso a Facturación si ya estaba aprobada (`DEC-022`, D34) |
| R7 | La plantilla se llena a mano: fechas, porcentajes con formato y números con coma | Reglas de lectura de D38, mensajes por fila y vista previa sin guardar |
| R8 | El borrador de T-1 traduce mal un texto del Excel | Lo revisa Facturación antes de importar; el informe de T-1 lista en cifras lo no traducido; la vista previa muestra cada fila |
| R9 | El Excel de convenios con datos reales está versionado en el hub (`D/levantamiento_staging/CONVENIO 23-24-25-26.xlsx`, commit `f8f77da`), contra `DEC-007` | Fuera del alcance de F07; se le muestra al usuario al entregar el plan para que decida si sale de git |
| R10 | La consolidada por destinatario crea más facturas de las que el cliente recibía | Es lo que pide AF-123; QA2-F07-007 lo prueba |
| R11 | C-F07-07 suma campos a las facturas que F08 rediseña | F07 escribe solo el fragmento; F08 lo integra en sus esquemas |
| R12 | Las retenciones (D54) restan del saldo, pero quien las guarda en la factura y cambia el saldo, los pagos y la mora es F08: hasta F08, la configuración existe y ninguna factura las usa | El plan de F08 parte de D52 a D55 y de C-F07-54 y C-F07-55 (§2.4, «Para F08»); el prompt de su planificador debe citarlas |
| R13 | La hoja 2026 dice qué retenciones aplican pero no su porcentaje | El borrador de T-1 las deja sin porcentaje y la vista previa marca «Falta el porcentaje.»; Facturación lo completa (matriz §4) |

---

## 10. Fuera de alcance

- La operación de facturas: «Facturar» (P-FAC-04), N.º SIGO, pestañas y columnas (P-FAC-01 a P-FAC-03), pendientes, pagos y reportes (P-FAC-05 a P-FAC-10) son de F08 (M14). F07 le deja el «Facturar a» en el destinatario, `depositCustomerId` y los candidatos (C-F07-02, C-F07-05 a C-F07-07).
- El cobro de la guía, `AppChargeForm`, `BillingCollectForm`, `ChangePaymentModeDialog` y la guía de despacho (F06).
- La apertura tardía y el recálculo al editar en Confirmado (`P05/` D17, D19), que F07 usa sin rehacer.
- Las retenciones en «Facturar» (verlas, ajustarlas o quitarlas), guardarlas en la factura de almacenamiento y restarlas del saldo por cobrar, de los pagos y de la mora (F08, D54 y D55).
- Las notificaciones configurables (F09), staging, el despliegue final (`PM/` §7.3) y estimar esfuerzo.
- Sacar del hub el Excel de convenios (R9).

**Cambios al hub** (aprobados por el usuario el 2026-11-26, «Aprobar con §10»; los aplica I-07 (2) al cerrar, §13.4):

1. `D/contexto/convenciones-tecnicas.md` §6, tabla de trabajos: se quita la fila de `AgreementActivationBackgroundService` y, después de la tabla, se agrega: «`AgreementActivationBackgroundService` se retiró en F07 de la fase 2: las tarifas del acuerdo tienen vigencia propia y no hay convenios que activar (plan de F07, D22).»
2. `D/contexto/convenciones-tecnicas.md` §10, trampa 3, se reemplaza por: «3. **IVA y retenciones.** El IVA es un porcentaje del servicio (`Service.VatPercent`, 0 = sin IVA) que aplica a todas sus tarifas; cada línea de factura guarda su tasa. Las retenciones (Retefuente, ReteICA y ReteIVA) son del tercero que paga, no del servicio: se configuran en su configuración de facturación, solo aplican a las facturas de almacenamiento y restan del saldo por cobrar, nunca se suman como IVA (F07, D3, D19 y D52 a D55).»
3. `D/contexto/decisiones.md`, `DEC-025`, al final de la viñeta «No se prohíbe ninguna fórmula…»: «*Las cuatro fórmulas de AF-116 son solo de Almacenamiento porque usan datos del depósito (plan de F07, D27).*»

---

## 11. Prompts por parte

- Backend: [prompt-f2-f07-tarifas-acuerdos-backend-2026-11-26.md](prompt-f2-f07-tarifas-acuerdos-backend-2026-11-26.md)
- Maquetación: [prompt-f2-f07-tarifas-acuerdos-maquetacion-2026-11-26.md](prompt-f2-f07-tarifas-acuerdos-maquetacion-2026-11-26.md)
- Integración (I-07 y T-1): [prompt-f2-f07-tarifas-acuerdos-integracion-2026-11-26.md](prompt-f2-f07-tarifas-acuerdos-integracion-2026-11-26.md)
- Planificador: [prompt-f2-f07-tarifas-acuerdos-planificador-2026-11-26.md](prompt-f2-f07-tarifas-acuerdos-planificador-2026-11-26.md)

---

## 12. Mensajes de commit sugeridos

| Fase | Repo | Mensaje |
| --- | --- | --- |
| BE-1 | BE | `feat(billing): ciclo libre, «Facturar a» por cliente e importador, retenciones del tercero que paga, mora al cliente e IVA por servicio (DEC-080, F07)` |
| BE-2 | BE | `feat(billing): acuerdos con vigencia por tarifa en Tarifas y acuerdos (DEC-080, F07)` |
| BE-3 | BE | `feat(billing): fórmulas de AF-116, simulador por fórmula y marca «Queda sobre el vehículo» en la entrada (DEC-080, F07)` |
| BE-4 | BE | `feat(billing): plantilla de acuerdos descargable e importable (DEC-080, F07)` |
| FE-1 | FE | `feat(rates): maquetación de la configuración de facturación y las tarifas de montacargas (DEC-080, F07)` |
| FE-2 | FE | `feat(rates): maquetación de los acuerdos con «Agregar tarifa» y simulador (DEC-080, F07)` |
| FE-3 | FE | `feat(rates): maquetación de las tarifas de servicios y la importación de la plantilla (DEC-080, F07)` |
| I-07 (1) | BE y FE | `feat(rates): integración de Tarifas y acuerdos con el API, parte 1 — fuentes http y marca en CE y Bodega (DEC-080, F07)` |
| I-07 (2) | BE y FE | `feat(rates): integración de Tarifas y acuerdos, parte 2 — menú, detalles, guardias y retiro de lo viejo (DEC-080, F07)` |
| Fusión | BE y FE | `merge: I-07, F07 «Tarifas y acuerdos» en fase-2 (DEC-080, DEC-081)` |
| Docs | docs | `docs(f07): <fase> de F07 (sprint 11)` |

---

## 13. Integración I-07 (parte 3)

Un agente con los dos repos, en `f2/f07-tarifas-acuerdos`, con el backend local real y sin la sesión simulada. Dos fases y, después de la fusión, T-1 (§14).

### 13.1 I-07 (1) — Fuentes http, pantallas nuevas y marca en CE y Bodega

- **Fuentes http** (`PM/` §5.2): `F/features/rates/services/billing-configuration.http.ts` (C-F07-01 a C-F07-04), `withholding.http.ts` (C-F07-54 a C-F07-56), `forklift-rate.http.ts` (C-F07-50 a C-F07-52, C-F07-08 de Montacargas), `agreement.http.ts` (C-F07-14 a C-F07-18), `formula.http.ts` (C-F07-31, C-F07-32), `service-rate.http.ts` (C-F07-08 a C-F07-10, C-F07-40 a C-F07-49, C-F07-53) y `agreement-import.http.ts` (C-F07-37 a C-F07-39, con `FormData` y descarga de `Blob`), con `~/shared/http/contract-api`; cada `*.source.ts` cambia su línea activa. Los selectores de terceros y productos usan las fuentes ya integradas de F02.
- **Marca en CE y Bodega** (D50): `F/features/foreign-trade/contracts/deposit-entry.ts` y `F/features/warehouse/contracts/reception.ts` con los campos de §2.3; en `DepositWarehouseStage.vue` (`:98`), un `ToggleSwitch` por entrada, con `aria-label` y tooltip, visible si `canMarkStaysOnVehicle` y el usuario es Admin o CE, que llama a C-F07-33 y refresca la etapa y la factura del período; en `ReceptionDialog.vue` (P-BOD-02), el switch «Queda sobre el vehículo» precargado con la fila de C-F07-35.
- **Configuración › Servicios** (`F/pages/admin/services/index.vue`): deja de leer `taxes` si lo hacía (§8.7).
- **Casos:** QA2-F07-042 a 048 y 053 en el navegador, abriendo las rutas por URL (el menú se enlaza en I-07 (2)).
- **Cierre:** compuertas de `PM/` §6.3 sin «sin llamadas reales» en las páginas ya integradas; commit en los dos repos con el mensaje de §12 y push.

### 13.2 I-07 (2) — Menú, detalles, guardias, retiro de lo viejo y fusión

- **Menú** (`F/components/layout/menu-model.ts:171-180`): «Tarifas y acuerdos» con los cuatro ítems de D42, para Admin y Facturación.
- **Detalles** (D49): `StakeholderDetailSections.vue` pierde la sección «Acuerdos» y sus diálogos (`:18-29`, `:126-224`, `:264-311`); el drawer de Terceros gana «Ver acuerdo» en «Acciones» (solo si el tercero es cliente) y el de Servicios cambia `ServiceRateSections` (`F/pages/admin/services/index.vue:14`, `:250`) por «Ver tarifas», los dos solo para Admin y Facturación.
- **Guardias:** en `FT/unit/guards/list-pattern-routes.ts`, `/admin/forklift-rates` y `/billing/configurations` salen de `PENDING` (`:57-59`) y entran a `PATTERN` junto con `/rates/agreements` y `/rates/services`; `F07` sale de `PENDING_FEATURES` (`:113`). En `FT/unit/guards/mock-sources.spec.ts`, `MAQUETACION_PAGES` queda vacía y `INTEGRATED_SOURCES` suma las siete fuentes de §13.1.
- **Rótulos de auditoría** (`F/features/audit/utils/entity-labels.ts`): `BillToException` «Excepción de Facturar a» y la tarifa del acuerdo «Tarifa del acuerdo»; salen `Tax` y `ServiceTax`.
- **Se borra** (cada archivo después de comprobar con `grep` que nadie más lo importa, trampa 7; con `rm`):
  - `F/features/agreements/` entero (componentes, composables, servicios, tipos y utilidades de hoy);
  - `F/features/stakeholders/components/AgreementsList.vue`;
  - de `F/features/services/`: `components/ServiceRateSections.vue`, `ServiceProfile.vue`, `ServicePricingRuleFormDialog.vue`, `ServicePricesList.vue`, `ServicePricingRulesList.vue`, `ServiceMinimumValuesCard.vue`; `composables/useAssignServiceTaxes.ts`, `useRemoveServiceTaxes.ts`, `useServicePrices.ts`, `useServicePriceMutations.ts`, `useServicePricingRules.ts`, `useServicePricingRuleMutations.ts`, `useServiceMinimumValues.ts`, `useServiceMinimumValueMutations.ts`; `services/service-pricing-rule-service.ts` y los métodos de precios e impuestos de `services/service-service.ts`; `types/pricing-rule.ts`, `types/minimum-value.ts` y lo que quede sin uso de `types/service.ts`, `types/requests.ts` y `utils/service-price-status.ts`;
  - de `F/features/billing/`: `components/BillingConfigForm.vue`, `utils/billing-config-payload.ts` y los composables y tipos de configuraciones y ciclos que queden sin uso (`CustomerSelect.vue` se queda: lo usan `BillingCollectForm`, `PendingDepositsFilters` y `UpdateRecipientDialog`);
  - `F/features/forklift-rates/` entero, si `F/features/warehouse/` no lo importa;
  - el método de impuestos de `F/features/administration/services/administration-service.ts`;
  - las pruebas de todo lo anterior.
- **Casos:** QA2-F07-041, 049 y 050 en el navegador; QA2-F07-001 a 040, 051 y 052 siguen en verde en la suite.

### 13.3 Criterio de salida

- Las compuertas de `PM/` §6.3 en los dos repos.
- QA2-F07-041 a 050 y 053 en PASA en el navegador, contra el backend local real.
- Ningún import de `mocks/` de F07 fuera de las pruebas; `F/features/rates/mocks/` borrada.
- El menú enlaza las cuatro pantallas; lo viejo y sus pruebas, borrados.
- Fusión de `f2/f07-tarifas-acuerdos` en `fase-2` en los dos repos con `--no-ff`, y push.

### 13.4 Casos QA y docs

Al fusionar: los casos QA2-F07-001 a 053, con su resultado, a `D/qa/casos-qa2-f07-tarifas-acuerdos-AAAA-MM-DD.md` (formato de `D/qa/casos-qa2-f04-bodega-2026-11-25.md`); los cambios al hub de §10 que el usuario haya aprobado; el estado en §8 y §13.5, en `D/planes/README.md` y en la matriz; y al usuario, qué puede probar en local (`PM/` §5.3).

### 13.5 Estado

Pendiente.

---

## 14. Carga inicial de acuerdos (T-1, después de I-07)

D4. La corre el agente de integración después de la fusión, en un turno propio, con el backend local de `fase-2`. **Todo lo que produce queda fuera de git**, en `db_legacy/trabajo/acuerdos/` (`DEC-007`); al hub solo llegan cifras.

### 14.1 Pasos

1. **Base de ensayo:** una base local recreada, cargada con la importación completa del legacy (los 12 CSV de `db_legacy/trabajo/csv`, como la fase 6 de F01), para que existan los clientes, importadores y terceros por su NIT.
2. **Plantilla:** descarga la vacía con C-F07-37.
3. **Clientes y «Facturar a»:** por cada responsable de la hoja 2026 busca el cliente migrado (por NIT si la hoja lo trae; si no, por nombre normalizado, sin mayúsculas, tildes ni signos); la razón social en factura de cada fila da el «Facturar a»: si es la misma en todas las filas del cliente, va como general en «Clientes»; si cambia por importador, como excepciones en «Facturar a» (AF-123). El ciclo y los días de pago son los del cliente migrado. Las retenciones que nombra la observación de cada fila («aplicar Retefuente», «Retefuente y ReteICA», «sin retenciones»…) van en la hoja «Retenciones» para el «Facturar a» de esa fila (D52), sin porcentaje: el Excel no lo trae y lo completa Facturación.
4. **Tarifas:** traduce cada uno de los 58 textos con una tabla de traducción (`db_legacy/trabajo/acuerdos/traduccion-textos.csv`, texto → fórmula, parámetros, papelería, IVA incluido), por patrón: «% VR CIF + IVA … Mínima {X} TODO INCLUIDO ({Y} + 15,000)» → `PERCENTAGE_OF_VALUE_PRORATED` con mínimo Y con IVA y papelería; «por Tonelada … Mínima» → `WEIGHT_RATE_MINIMUM` en toneladas; «por Kilogramo» → `WEIGHT_RATE_MINIMUM` en kilos sin mínimo, o `TIERED` por peso si trae dos tarifas; «x VEH» → `PER_VEHICLE`; «x Tanquero» o «x Contenedor» → `PER_CARGO_UNIT`; «x CAJA» → `PER_UOM`; «+ BASCULA» → una fila más de Báscula `FIXED` 0 (`DEC-057` H5b); «MCIA DESCARGADA / SOBREVEHICULO» → `UNLOADED_OR_ON_VEHICLE`; «≤ / > {N} millones» → `VALUE_THRESHOLD`; «X vehículos … > 2 vehículos» → `TIERED` por vehículos; un valor fijo con o sin IVA incluido → `FIXED`. Un texto que no encaje no se inventa: queda fuera del borrador y entra al informe. «Vigente desde»: la fecha de la fila o, si falta, 01/01/2026.
5. **Validación:** carga el borrador con C-F07-38 en la base de ensayo y cuenta los resultados por tipo.
6. **Entrega:** `db_legacy/trabajo/acuerdos/borrador-carga-inicial-acuerdos-2026.xlsx` y su informe (fuera de git); en §14.2, solo cifras: filas de la hoja, textos traducidos y no traducidos (por motivo), clientes encontrados y no encontrados, «Facturar a» generales y excepciones, retenciones por tipo (sin porcentaje), y los resultados de la vista previa. El usuario se lo pasa a Facturación; se importa en el paso 4 del despliegue final (`PM/` §7.3).

### 14.2 Estado

Pendiente.
