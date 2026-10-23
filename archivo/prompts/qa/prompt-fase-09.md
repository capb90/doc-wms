Eres el implementador de la **Fase 9** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad media, riesgo de regresión medio en CHG-64). Las Fases 1 a 8 están completadas y con commit. Esta fase toca facturación y jobs: la exactitud importa más que la velocidad.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 9**, las tarjetas **CHG-60 a CHG-68** y la decisión **D-1** de §5 (resuelta: «Consolidada» queda para almacenamiento y guías a crédito; báscula y montacargas siguen con factura individual; se retira «Por ciclo de báscula»). Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10 (en particular «OnDemand se retira» y «Mora»); la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor, `WmsApiFactory`, `BillingScenario`, `OverdueJobTests`, `ManualPeriodCloseTests`), `Invoice.RefreshStatus`, `OverdueSweep`, `ClientFinancialStatusRules`, `IBillingService.RefreshFinancialStatusAsync`, `VatMath`, `FormulaParameterValidator`, `PatchField<T>`, `StoragePeriodCalculator.StartAfter`, `StorageBillingNotifier`, `AuditPayloadBuilder`, `CancelledInvoiceDto` y `InvoiceCancellationPolicy`.

## Alcance
Implementa en el orden interno del plan:
- **CHG-60** El ciclo OnDemand deja de ofrecerse (§10): se quita del catálogo, del validador y del frontend; el miembro del enum se conserva para leer filas antiguas.
- **CHG-61** Quitar el límite de crédito se guarda (el PUT reemplaza todos los campos) y desbloquea al instante.
- **CHG-62** Un solo aviso de vencimiento por factura (`Invoice.DueNoticeSentAt`) y aviso de cada renovación (`NotifyPeriodRenewedAsync`).
- **CHG-63** «Consolidada» promete solo lo que hace (D-1): job de conciliación diaria de pagos y texto de la configuración.
- **CHG-64** La previsualización de fórmulas calcula igual que el cobro real (`FormulaPricing`).
- **CHG-65** El reporte por CPI conserva la factura anulada al refacturar (`DepositInvoiceLinks`).
- **CHG-66** El detalle de la factura de almacenamiento usa la cantidad facturada (`StorageDetailLines`).
- **CHG-67** Anular un depósito avisa a Bodega y a Facturación (`DepositCancellationNotices`).
- **CHG-68** Los catálogos y los roles de usuario quedan en la auditoría (`IAuditable` en 17 entidades y `Describe` en los handlers de roles).

CHG-61, CHG-62 y CHG-63 comparten `BillingJobService.cs` o `BillingConfigForm.vue`: hazlos en serie. Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces.

## Migraciones y base de datos (regla 4.0.2)
- Esta fase genera **una migración: `AddInvoiceDueNoticeSentAt`** (CHG-62: columna `invoices.due_notice_sent_at timestamptz` nula, sin valor por defecto). **CHG-68 no genera migración** (`IAuditable` es una interfaz marcadora): si `dotnet ef migrations add` arrastra otras operaciones, corrige el modelo y regénerala hasta que contenga solo esa columna.
- Tú generas, aplicas, reviertes o eliminas, siempre con `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`.
- **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual.
- Solo la base local de pruebas de `Wms.Api` en Development. Tras generar, recrea la base (`database drop --force` y `database update`) y verifica que aplique sin errores. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios.
- **No escribas scripts de saneamiento** (`fase-09-*.sql`): las bases son de prueba. Deja en tu informe solo las consultas de detección (`SELECT`) de cada tarjeta, incluida la lista de clientes con ciclo OnDemand o preferencia `PerWeighbridgeCycle`.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits. Para borrar archivos usa `rm`, no `git rm`.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español. Dinero con `decimal` y el redondeo del repositorio. Fechas de negocio con `ColombiaTime`. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real (los números de línea ya cambiaron en ocho fases), **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo. Si el comportamiento cambia, **detente y repórtalo**.
- **Sin retrocesos:**
  - CHG-60: una configuración antigua con OnDemand sigue leyéndose sin error (el miembro del enum se conserva); solo deja de ofrecerse y de aceptarse al guardar.
  - CHG-61: «sin límite nunca bloquea» (§10 · Mora); `ClientFinancialStatusRules` y el job no cambian de regla.
  - CHG-62: la frecuencia de los servicios de fondo no cambia; un aviso ya enviado no se reenvía.
  - CHG-63: la consolidación de almacenamiento y de guías a crédito **no se toca** (ya funciona); el enum conserva `PerWeighbridgeCycle`, solo sale de las opciones.
  - CHG-64: con los mismos datos, el cobro real da exactamente el mismo importe que antes de extraer `FormulaPricing`; las pruebas de facturación existentes pasan sin editarlas.
  - CHG-65 y CHG-66: `InvoicesTotal` sigue excluyendo las anuladas; `StorageInvoiceDetailFormatter` no cambia de formato.
  - CHG-67: los avisos existentes de la anulación no se tocan; las anulaciones pasadas no se re-notifican.
  - CHG-68: las bajas y altas de catálogos de la carga legacy generan filas de auditoría como ya ocurre con `ProductsImporter`; el rendimiento de la carga no puede degradarse de forma apreciable.

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo), incluida la prueba de que el job de vencimientos corrido dos veces avisa una sola vez.
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. `yarn lint`: **no más de 290 errores** (la cifra de cierre de la Fase 8) y 0 en archivos nuevos. Reporta la cifra.
5. Recorre los criterios de aceptación de las nueve tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega
Responde con:
1. La migración generada (nombre y operaciones) y el resultado de recrear la base.
2. Los archivos creados, modificados o borrados por cambio.
3. El resultado de cada compuerta, con números.
4. Los criterios sin verificar, las consultas de detección de cada tarjeta y cualquier desviación del plan.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend, commit 1:** el código de la fase, sin la migración. Asunto `feat(qa-fase-9): <resumen> (CHG-60 a CHG-68)` y un cuerpo con una línea por cambio (`- CHG-nn: …`).
   - **Backend, commit de migración:** `feat(qa-fase-9): migración AddInvoiceDueNoticeSentAt`, con una línea sobre qué cambia en la base. Lleva `Migrations/<timestamp>_AddInvoiceDueNoticeSentAt.cs`, su `.Designer.cs` y `AppDbContextModelSnapshot.cs`.
   - **Frontend:** `feat(qa-fase-9): <resumen> (CHG-nn, …)` con una línea por cambio. Indica qué archivos de `docs/`, `package.json` o los `components.d.ts` generados no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no avances a la Fase 10 ni marques la fase como completada.
