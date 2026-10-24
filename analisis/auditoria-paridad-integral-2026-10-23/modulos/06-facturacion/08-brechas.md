# 06-facturacion — 08 Registro de brechas

> AG-06 · 2026-10-23 · Estático. **Prefijos:** `L/` = `bodegas-legacy/`; `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`.
> Antes de registrar cada brecha se revisaron `docs/qa/resultados/defectos/INDICE.md` (153 fichas; F6, F7, F8, F9, F11), `docs/planes/migracion-staging/resultados/defectos/DEF-MIG-*.md` y `docs/contexto/estado.md` §4 y §6. Ninguna de las 14 tiene ficha. Se citan las fichas y riesgos relacionados.

## Resumen

| ID | Título | Capacidades | Criticidad |
| --- | --- | --- | --- |
| BR-06-001 | Un convenio «Programado» nunca se activa y el convenio no tiene vigencia final | CF-L018, CF-L019, CF-V060 | ALTA |
| BR-06-002 | Facturación no llega por la interfaz a tarifas base, mínimos ni tarifas de montacargas | CF-L065…068 | MEDIA |
| BR-06-003 | «Depósitos pendientes» omite depósitos sin período abierto con facturas por numerar o por refacturar | CF-L201 | MEDIA |
| BR-06-004 | Un servicio complementario sin tarifa revierte la confirmación del depósito y la renovación | CF-L202.b, CF-V060, CF-V067 | ALTA |
| BR-06-005 | La renovación cobra el stock del día en que corre el job (fin + 4), no el del inicio del período | CF-L234, CF-L202.b, CF-V067 | MEDIA |
| BR-06-006 | No existe la fecha de la factura: los informes usan la fecha de creación del borrador | CF-L202.c, CF-L204, CF-L206 | MEDIA |
| BR-06-007 | Cambiar el destinatario de una factura en Borrador no tiene pantalla | CF-L202.d, CF-L204 | MEDIA |
| BR-06-008 | El listado de facturas no filtra por depósito ni por CPI | CF-L203 | BAJA |
| BR-06-009 | «Facturación por CPI» solo busca por el número exacto del depósito | CF-L207, CF-L251 | BAJA |
| BR-06-010 | Ciclo por defecto y cambio de ciclo distintos del legacy, sin decisión | CF-L234.b, CF-V061 | BAJA |
| BR-06-011 | Endpoints de facturación sin consumidor | CF-L249, CF-V060, CF-V067 | BAJA |
| BR-06-012 | El mes del tablero y la ventana de la factura consolidada se calculan en UTC | CF-V068, CF-V06A | BAJA |
| BR-06-013 | Tipos TypeScript desalineados con los DTO de facturación | CF-L201, CF-L203, CF-L207 | BAJA |
| BR-06-014 | El resumen del depósito no muestra la tasa, el FOB ni el CIF de cada levante | CF-L201 | BAJA |

---

### BR-06-001 — Un convenio «Programado» nunca se activa y el convenio no tiene vigencia final

- **ID funcional:** CF-L018, CF-L019 (y CF-V060).
- **Descripción:** el formulario de convenio ofrece el estado «Programado» con fecha de activación (`F/features/agreements/components/AgreementForm.vue:45,64-83`) y el dominio lo guarda como `Scheduled` (`B/Wms.Domain/Entities/Agreement/Agreement.cs:36,58`). Ningún proceso lo pasa a `Active`: la búsqueda de `ScheduledActivationDate`, `AgreementStatus.Scheduled` y `Scheduled` en `B/Wms.Application`, `B/Wms.Api` (incluidos `BackgroundJobs/`) y `B/Wms.Domain` solo encuentra la creación y la edición. El resolutor solo usa convenios `Active` (`B/Wms.Application/Billing/Services/BillingResolver.cs:184`). Tampoco hay fecha de fin.
- **Esperado:** como el legacy, el convenio rige dentro de su vigencia (`L/modulos/mod_convenios/registrarconvenio.php:57`; `L/modulos/mod_bascula/consultarconveniosvehiculo.php:15-17`). Si la V2 ofrece la activación programada, debe ocurrir en la fecha.
- **Actual:** el convenio programado queda inactivo y la facturación cae a la tarifa base, al precio base o al mínimo, sin aviso.
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO` (y `PROCESOS_AUTOMATICOS`).
- **Evidencia adicional:** `docs/analisis/analisis-motor-acuerdos-facturacion-2026-09-17.md` MAF-08 (mismo hallazgo, sin ficha ni corrección). QA solo prueba el rechazo de una fecha pasada (`docs/qa/fase-01-administracion.md` F1-CNV-009).
- **Impacto:** importes de almacenamiento, báscula, montacargas y guía distintos de lo pactado, sin advertencia.
- **Criticidad:** ALTA — afecta una regla importante (la tarifa del convenio) en silencio; hay alternativa manual (crear el convenio activo) y no impide el proceso.
- **Dependencias:** decisión §2.A.3 (motor de acuerdos).
- **Acción:** completar una activación idempotente (job diario en `ColombiaTime` o activación perezosa al resolver) o retirar la opción «Programado» del formulario y del API. Confirmar con el negocio si hace falta una fecha de fin.
- **Criterio verificable:** un convenio creado «Programado» para mañana está `Active` ese día y la factura de un cargo de ese día sale «Acuerdo (nivel 1)»; o bien el formulario y `POST stakeholder/{id}/agreement` ya no aceptan `Scheduled`.

### BR-06-002 — Facturación no llega por la interfaz a tarifas base, mínimos ni tarifas de montacargas

- **ID funcional:** CF-L065, CF-L066, CF-L067, CF-L068.
- **Descripción:** el API acepta escrituras de servicios, precios, reglas base, mínimos, impuestos y tarifas de montacargas con `BillingAccess` (Admin y Facturación) (`B/Wms.Api/Controllers/v1/ServiceController.cs:36-261`; `ForkliftRateController.cs:44-85`), pero las páginas exigen `Admin` (`F/pages/admin/services/index.vue:14`, `[id].vue:102`, `create.vue:10`, `edit/[id].vue:12`; `F/pages/admin/forklift-rates/index.vue:6`) y el menú las pone en «Administración», solo Admin (`F/components/layout/AppMenu.vue:47-49,130-151`). Los convenios sí se editan desde el tercero (`F/pages/admin/stakeholders/[id].vue:132`).
- **Esperado:** `docs/qa/00-plan-maestro.md` §10 «Permisos de catálogos»: convenios **y tarifas** Admin y Facturación (decisión del 3-oct; DEF-F9-001 Verificado en el API).
- **Actual:** Facturación configura convenios, pero no la tarifa base por producto y modalidad (DEC-027), el mínimo por modalidad (DEC-020) ni el montacargas.
- **Capa / categoría:** Frontend · `SEGURIDAD` (permisos de interfaz).
- **Impacto:** Facturación depende de Admin para corregir la tarifa que genera sus facturas.
- **Criticidad:** MEDIA — función de configuración, con alternativa (Admin).
- **Dependencias:** DEC-005, DEC-031.
- **Acción:** abrir las páginas y la entrada de menú al rol Billing (lectura y escritura), o documentar que las tarifas base quedan solo para Admin.
- **Criterio verificable:** con la cuenta de Facturación, `/admin/services/{id}` permite crear una regla base y editar un mínimo, y `/admin/forklift-rates` guarda una tarifa; o hay una decisión escrita que lo restringe.

### BR-06-003 — «Depósitos pendientes» omite depósitos sin período abierto con facturas por numerar o por refacturar

- **ID funcional:** CF-L201.
- **Descripción:** la consulta solo devuelve depósitos `Confirmed` con al menos un período `Open` (`B/Wms.Application/Billing/Queries/GetPendingDeposits/GetPendingDepositsHandler.cs:21-28`). Un depósito agotado (períodos cerrados, estado `Closed`) cuya factura sigue en Borrador sin N.º SIIGO, o fue anulada y no refacturada, no aparece; «Por refacturar» solo se cuenta en las filas listadas (`:247-249`). El plan lo dejó así a propósito en el texto de F3-10 (desviación 11), sin decisión en §A.4.
- **Esperado:** el legacy muestra el depósito mientras su último período no esté facturado (`L/modulos/mod_facturacion/listardepositosfacturar.php:478-479`), haya o no saldo.
- **Actual:** esas facturas solo se encuentran en `/billing/invoices` filtrando por estado.
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO`.
- **Evidencia adicional:** riesgo R-FAC-10, caso `docs/qa/fase-06-facturacion.md` F6-REF-006 «NO EJECUTADO» (`docs/qa/resultados/F6-informe-2026-10-02.md:192`).
- **Impacto:** facturas sin numerar o sin refacturar fuera de la lista de trabajo de Facturación.
- **Criticidad:** MEDIA — escenario específico con alternativa (listado de facturas), pero puede dejar ingreso sin facturar.
- **Dependencias:** P9 (refacturar es una acción explícita).
- **Acción:** incluir en el criterio los depósitos con facturas de almacenamiento en Borrador o anuladas sin reemplazo (o agregar un filtro «con pendientes»). Confirmar con el negocio.
- **Criterio verificable:** un depósito despachado por completo con su factura anulada sin refacturar aparece en `GET billing/pending-deposits` con `periodsPendingReissue > 0`, y uno con factura en Borrador sin N.º también aparece.

### BR-06-004 — Un servicio complementario sin tarifa revierte la confirmación del depósito y la renovación

- **ID funcional:** CF-L202.b, CF-V060, CF-V067.
- **Descripción:** la línea del servicio complementario (`LinkedServiceId` de la regla) se resuelve con `billingResolver.ResolveAsync` sin captura (`B/Wms.Application/Billing/Common/Services/StorageBillingService.cs:790`); si el servicio no tiene convenio, regla ni precio base vigente, `ResolveRuleAsync` lanza `NotFoundException` (`BillingResolver.cs:66-74`). Al guardar la regla no se verifica que el complementario tenga tarifa (`B/Wms.Application/Agreements/Commands/AddAgreementService/AddAgreementServiceHandler.cs:20-60`; `B/Wms.Application/Services/Commands/CreateServicePricingRule/CreateServicePricingRuleValidator.cs:29-31`, solo formato). Efectos: la confirmación se revierte y el depósito queda en Borrador (`B/Wms.Application/ForeignTrade/Commands/ConfirmStorageDeposit/ConfirmStorageDepositHandler.cs:85-89`); el job revierte, avisa «No se pudo facturar» (`BillingJobService.cs:269-278`) y, como el período sigue vencido, vuelve a intentarlo cada 5 minutos (`StoragePeriodAutoCloseBackgroundService`, `MinInterval` en `CalculateNextWaitAsync`). Relacionado: `PERCENTAGE_OF_VALUE_PRORATED` no valida `minimumPerCargoUnit` al guardar (`B/Wms.Application/Billing/Calculators/PercentageOfValueProratedFormulaCalculator.cs:84`), aunque ese caso sí cae al mínimo.
- **Esperado:** DEC-020: la factura de almacenamiento siempre se genera; lo que falle va al mínimo o a $0 con advertencia, nunca bloquea.
- **Actual:** la falta de tarifa de un servicio secundario bloquea la confirmación (proceso esencial de Comercio Exterior) o la renovación, con avisos repetidos.
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO`.
- **Evidencia adicional:** MAF-07 y R-FAC-08 (`docs/qa/fase-06-facturacion.md` F6-ALM-014, «NO APLICA» en `F6-informe-2026-10-02.md:169` porque QA no logró crear la configuración; la causa del rechazo citada fue el parámetro `rate` de la regla, no la tarifa del complementario). El precio base puede además vencer después (`ServicePrice.ValidTo`).
- **Impacto:** depósito sin confirmar, sin factura y con etiqueta bloqueada hasta corregir la tarifa.
- **Criticidad:** ALTA — impide la confirmación en una configuración posible; no es CRÍTICA porque requiere un servicio complementario configurado sin tarifa. **Confianza MEDIA** (estático, sin reproducción).
- **Dependencias:** ninguna.
- **Acción:** capturar el fallo del complementario y emitir su línea en $0 o al mínimo con advertencia (como el cargo principal), y validar al guardar que el complementario tenga tarifa.
- **Criterio verificable:** con un convenio cuyo almacenamiento enlaza un servicio sin tarifa, la confirmación responde 200, la factura sale con la línea complementaria en $0 y la advertencia en el detalle, y el job no registra errores repetidos.

### BR-06-005 — La renovación cobra el stock del día en que corre el job (fin + 4), no el del inicio del período

- **ID funcional:** CF-L234, CF-L202.b, CF-V067.
- **Descripción:** el job renueva el día siguiente a la fecha límite (`fin + 4`) con inicio `fin + 1` (`BillingJobService.cs:160-168,225-241`) y la apertura cobra `CurrentStock` en ese momento (`StorageBillingService.cs:112-115`). Las salidas de `fin + 1` a `fin + 3`, ya dentro del período nuevo, reducen la cantidad que ese período cobra.
- **Esperado:** el legacy detalla el saldo por producto con las salidas **hasta el día de inicio** del período (`L/modulos/mod_facturacion/facturarciigo.php:119-145`, `S.fecha_salida <= fechainicio 23:59:59`). DEC-028 fija la cantidad del recálculo (stock + salidas netas desde que el período tomó su stock), no la de la apertura.
- **Actual:** con fórmulas por cantidad (`PER_UOM`, `PERCENTAGE_OF_VALUE_PRORATED`, `PER_CARGO_UNIT`) el período nuevo cobra menos que el saldo de su inicio. `PERCENTAGE_OF_VALUE` (tarifa T1 aprobada, DEC-041) no cambia.
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO` (`PROCESOS_AUTOMATICOS`).
- **Evidencia adicional:** MAF-14 (renovación atrasada con la foto actual).
- **Impacto:** subfacturación en renovaciones con despachos durante la gracia; mayor si el job estuvo detenido varios días.
- **Criticidad:** MEDIA — regla de cálculo en un escenario específico.
- **Dependencias:** DEC-028 (`StorageBillableQuantity` ya reconstruye cantidades desde movimientos).
- **Acción:** confirmar con el negocio y, si aplica, abrir el período renovado con la cantidad facturable a su fecha de inicio (stock + salidas netas desde `fin + 1`).
- **Criterio verificable:** depósito `PER_UOM` de 10 unidades, salida de 4 el día `fin + 2`; la factura del período siguiente cobra 10 (o lo que decida el negocio, por escrito).

### BR-06-006 — No existe la fecha de la factura: los informes usan la fecha de creación del borrador

- **ID funcional:** CF-L202.c, CF-L204, CF-L206.
- **Descripción:** al asignar el N.º SIIGO no se registra fecha (`B/Wms.Application/Billing/Commands/AssignInvoiceNumber/AssignInvoiceNumberHandler.cs:31-41`); la aprobación guarda `ApprovedAt` (`B/Wms.Domain/Entities/Billing/Invoice.cs:345-363`). El informe anual agrupa por `CreatedAt` (`B/Wms.Application/Reports/Queries/GetBillingAnnual/GetBillingAnnualHandler.cs:19-21`) y el de CPI muestra `InvoiceDate = CreatedAt` (`GetDepositBillingHandler.cs`, armado de `DepositBillingInvoiceDto`). El plan F5-08 lo escribe así en su regla 1, sin decisión en §A.4 (P12 solo fija el servicio por defecto).
- **Esperado:** el legacy captura la fecha de la factura emitida en SIIGO (`L/modulos/mod_facturacion/facturarciigo.php:277`; `modificarfactura.php:59`) y el informe agrupa por ella (`informefacturacion.php:92-96`).
- **Actual:** una renovación crea el borrador el día `fin + 4`; si Facturación lo numera otro día u otro mes, el informe lo cuenta en la fecha del borrador.
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO`.
- **Impacto:** el informe anual y el de CPI no cuadran con SIIGO en los cortes de mes.
- **Criticidad:** MEDIA — afecta informes, no el cobro.
- **Dependencias:** módulo 07 (páginas de informes).
- **Acción:** decidir qué fecha es la de la factura (asignación del N.º, aprobación o digitada) y usarla en los dos informes.
- **Criterio verificable:** una factura creada el 31/03 y numerada el 02/04 aparece en el mes que fije la decisión en `GET reports/billing-annual` y con esa fecha en `GET reports/deposit-billing`.

### BR-06-007 — Cambiar el destinatario de una factura en Borrador no tiene pantalla

- **ID funcional:** CF-L202.d, CF-L204.
- **Descripción:** existen `PATCH billing/invoices/{id}/recipient` (`B/Wms.Api/Controllers/v1/BillingController.cs:158-176`), el servicio (`F/features/billing/services/billing-service.ts:96-102`), el composable y el diálogo `F/features/billing/components/UpdateRecipientDialog.vue`, pero ninguna página ni componente monta el diálogo (búsqueda de `UpdateRecipientDialog` en `F/`: solo su propio archivo).
- **Esperado:** el legacy deja editar «Cliente Factura» al facturar (`L/modulos/mod_facturacion/facturarciigo.php:281-285`).
- **Actual:** la factura de almacenamiento queda a nombre del cliente del depósito sin forma de cambiarlo desde la UI.
- **Capa / categoría:** Frontend · `INTEGRACION`.
- **Impacto:** si se debe facturar a otro tercero del depósito (agencia, importador), hay que pedirlo por API.
- **Criticidad:** MEDIA — función secundaria con impacto en el documento fiscal.
- **Dependencias:** `BillingService.ValidateDepositStakeholderAsync` (`B/Wms.Application/Billing/Common/Services/BillingService.cs:122-151`).
- **Acción:** montar el diálogo en el detalle o en las acciones de la factura en Borrador, o retirar componente y endpoint con decisión.
- **Criterio verificable:** desde `/billing/invoices/{id}` en Borrador, Facturación cambia el destinatario a la agencia del depósito y el detalle lo muestra.

### BR-06-008 — El listado de facturas no filtra por depósito ni por CPI

- **ID funcional:** CF-L203.
- **Descripción:** `GetInvoicesQuery` filtra por estado, cliente, N.º, destinatario, fechas, monto y servicio (`B/Wms.Application/Billing/Queries/GetInvoices/GetInvoicesQuery.cs`), y la página por estado, N.º, destinatario y día (`F/pages/billing/invoices/index.vue:30-76`). No muestra el detalle ni las observaciones.
- **Esperado:** filtros por CPI, fecha, depósito, N.º y cliente; columnas de detalle y observaciones (`L/modulos/mod_facturacion/listarfacturas.php:60-77,216-224`).
- **Capa / categoría:** Frontend y backend · `FRONTEND`.
- **Impacto:** buscar la factura de un depósito exige pasar por el informe por CPI o por «Depósitos pendientes».
- **Criticidad:** BAJA — hay alternativas.
- **Acción:** agregar el filtro por número de depósito y documento comercial (con `all=true` para el Excel).
- **Criterio verificable:** en `/billing/invoices`, escribir `2026BA00002` o su CPI lista sus facturas.

### BR-06-009 — «Facturación por CPI» solo busca por el número exacto del depósito

- **ID funcional:** CF-L207, CF-L251.
- **Descripción:** la consulta compara el número completo (`GetDepositBillingHandler`, `WarehouseStorageNumber.ToUpper() == upper`) y la página pide el número en un campo libre (`F/pages/billing/reports/deposit-billing.vue:110-116`).
- **Esperado:** autocompletar por N.º de depósito **o CPI**, coincidencia parcial (`L/modulos/mod_facturacion/seleccionardeposito.php:9-15`; `informecpi.php:32-44`).
- **Capa / categoría:** Frontend y backend · `FRONTEND`.
- **Impacto:** quien tiene el CPI debe buscar antes el depósito en otra pantalla.
- **Criticidad:** BAJA.
- **Dependencias:** módulo 07 (página del informe).
- **Acción:** aceptar CPI y coincidencia parcial con un selector.
- **Criterio verificable:** escribir parte del CPI en «Facturación por CPI» sugiere el depósito y abre su informe.

### BR-06-010 — Ciclo por defecto y cambio de ciclo distintos del legacy, sin decisión

- **ID funcional:** CF-L234.b, CF-V061.
- **Descripción:** sin configuración, el cliente factura por mes calendario (`StorageBillingService.cs:367`; `BillingService.cs:103`); el legacy usa 15 días (`L/bodegas_schema.sql:186`; opción inicial de `L/modulos/mod_clientes/registrarcliente.php:468-469`). El legacy rehace los períodos no facturados en cada pasada (`L/cron.php:29-30`), así que un cambio de días de facturación se reflejaba; la V2 no recalcula el período abierto al guardar la configuración (`B/Wms.Application/Billing/Commands/UpsertBillingConfiguration/UpsertBillingConfigurationHandler.cs`).
- **Esperado:** documentar el comportamiento (la migración ya mapea los ciclos legacy, `LegacyBillingCycleMapper.cs:9-17`).
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO`.
- **Impacto:** solo clientes creados en la V2 sin configuración o con cambio de ciclo a mitad de período.
- **Criticidad:** BAJA.
- **Acción:** confirmar con el negocio el ciclo por defecto y si el cambio rige desde el período abierto.
- **Criterio verificable:** decisión escrita y prueba en `Wms.Tests` del comportamiento elegido.

### BR-06-011 — Endpoints de facturación sin consumidor

- **ID funcional:** CF-L249, CF-V060, CF-V067.
- **Descripción:** sin consumidor en `F/`: `GET billing/invoices/{id}/payments` (`BillingController.cs:377`), `GET billing/storage-periods/{id}` (`:535`; `getStoragePeriodById` sin uso), `POST billing/storage-periods/close` (`:554`), `GET system/dian-trm/today` (`B/Wms.Api/Controllers/v1/SystemController.cs:18`) y `GET formulatype/{code}` (`FormulaTypeController.cs:25`). `PATCH …/recipient` está en BR-06-007.
- **Esperado:** cada endpoint tiene consumidor o está documentado como API a propósito (como DF3).
- **Capa / categoría:** Backend · `CONTRATOS_API`.
- **Impacto:** superficie sin uso; el cierre manual con renovación es una operación de escritura solo disponible por API.
- **Criticidad:** BAJA.
- **Acción:** documentar el cierre manual como operación de soporte o darle pantalla; retirar o documentar los demás.
- **Criterio verificable:** lista de endpoints solo-API documentada o endpoints retirados.

### BR-06-012 — El mes del tablero y la ventana de la factura consolidada se calculan en UTC

- **ID funcional:** CF-V068, CF-V06A.
- **Descripción:** `GetMonthlyPeriod`, `GetBiweeklyPeriod` y `GetWeekPeriod` usan `DateTimeOffset.UtcNow` con desfase 0 (`B/Wms.Application/Billing/Common/Services/BillingService.cs:209-250`); el tablero toma el mes con `UtcNow` (`B/Wms.Application/Billing/Queries/GetBillingDashboard/GetBillingDashboardHandler.cs:16-17`).
- **Esperado:** fechas de negocio con `ColombiaTime` (`docs/contexto/convenciones-tecnicas.md`; AGENTS.md).
- **Actual:** un cargo después de las 19:00 del último día del mes va a la consolidada del mes siguiente y el KPI del mes cambia a esa hora.
- **Capa / categoría:** Backend · `REGLAS_NEGOCIO`.
- **Evidencia adicional:** riesgo R-FAC-11, caso F6-DSH-003 «NO EJECUTADO» (`docs/qa/resultados/F6-informe-2026-10-02.md:89`).
- **Criticidad:** BAJA — solo en el borde del día.
- **Acción:** calcular las ventanas y el mes con `ColombiaTime`.
- **Criterio verificable:** prueba en `Wms.Tests`: un cargo a las 20:00 (Colombia) del 31/10 cae en la consolidada de octubre y en el KPI de octubre.

### BR-06-013 — Tipos TypeScript desalineados con los DTO de facturación

- **ID funcional:** CF-L201, CF-L203, CF-L207.
- **Descripción:** ver `05-analisis-v2.md` §4: `IInvoiceDetailDto` hereda campos que el detalle no envía; `IInvoiceItemDto.productPriceId` no existe (es `servicePriceId`); `IInvoiceDto.customerId/customerName` no nulos; `StorageBillingPeriodStatus` acepta `"Invoiced"`; `IInvoiceHistoryEntryDto` sin `totalAmount`; nulos del informe por CPI.
- **Esperado:** tipos iguales a los DTO (nombres y nulos).
- **Capa / categoría:** Frontend · `CONTRATOS_API`.
- **Impacto:** hoy ninguno visible; riesgo de lecturas `undefined` al usar esos campos.
- **Criticidad:** BAJA.
- **Acción:** alinear los tipos.
- **Criterio verificable:** los tipos de `F/features/billing/types/*` coinciden con los DTO citados y el typecheck del frontend pasa.

### BR-06-014 — El resumen del depósito no muestra la tasa, el FOB ni el CIF de cada levante

- **ID funcional:** CF-L201.
- **Descripción:** `ReleaseDto` solo trae número, aceptación, fechas, producto, cantidad y peso (`B/Wms.Application/Billing/Queries/GetDepositSummary/ReleaseDto.cs:5-13`) y el diálogo muestra esas columnas (`F/features/billing/components/DepositSummaryDialog.vue:205-224`).
- **Esperado:** el legacy muestra por levante la tasa, el CIF US y el CIF CO, y el total CIF nacionalizado (`L/modulos/mod_facturacion/listardepositosfacturar.php:633-643`).
- **Capa / categoría:** Backend y frontend · `FRONTEND`.
- **Impacto:** Facturación no ve el valor nacionalizado al revisar el depósito.
- **Criticidad:** BAJA.
- **Dependencias:** F2-05 (FOB y tasa congelados en el levante, módulo 05); pendiente FOB/CIF (`docs/contexto/estado.md` §4 n.º 8).
- **Acción:** agregar tasa y FOB/CIF del levante al resumen.
- **Criterio verificable:** el resumen de un depósito con levante muestra su tasa y su valor en dólares y en pesos, y el total.

## Relacionados que no se registran como brecha

| Tema | Por qué no | Referencia |
| --- | --- | --- |
| Equivalencia FOB/CIF del valor migrado (base del almacenamiento) | Pendiente abierto | `docs/contexto/estado.md` §4 n.º 8; `docs/analisis/revision-fob-cif-migracion-v2-2026-10-08.md` §2 |
| `PERCENTAGE_OF_VALUE` frente a `_PRORATED` | Decisión del cliente abierta; conviven | DEC-025; `estado.md` §6 |
| Recalcular facturas emitidas conservando el N.º SIIGO (riesgo fiscal) | Decisión vigente | DEC-022; MAF-05 |
| Sin efectivo ni cambio en pagos | Decisión §10 | Módulo 02 (BR-02-017) |
| Báscula sin tarifa no cobra; «otros servicios» | Módulo 02 | BR-02-003, BR-02-004 |
| Precarga de tarifa por placa | Decisión | §2.A.3; CF-L100 (módulo 01) |
| Manual de facturación desactualizado | Se declara obsoleto en su propio aviso | `docs/manuales/manual-modulo-facturacion.md:3-6` |


---

## Decisiones posteriores (2026-10-23)

> Nota del orquestador. Después de esta auditoría, el usuario respondió las preguntas al negocio (`docs/contexto/decisiones.md`, DEC-050…054; `06-brechas-priorizadas.md` §3.1). El registro de arriba es la foto previa y no se reescribe. El estado vigente está en `06-brechas-priorizadas.md` y `04-matriz-global.csv`.

| Brecha | Estado | Decisión |
| --- | --- | --- |
| BR-06-003 | Abierta: se construye (requiere plan cerrado) | DEC-053 |
| BR-06-005 | Abierta: se construye (requiere plan cerrado) | DEC-053 |
