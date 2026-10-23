Eres el implementador de la **Fase 10** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad media, riesgo de regresión bajo a medio). Las Fases 1 a 9 están completadas y con commit.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 10** y las tarjetas **CHG-69 a CHG-75**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10 (en particular «Inventario de Bodega con Borradores» y «Etiqueta NACIONALIZADA con cualquier levante»); la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor, `WmsApiFactory`, `ImportExitScenario`, `AdjustmentScenario`, `BillingScenario`), `WhereListed` y `DepositSearchQueryExtensions` (CHG-43), `ReceptionDeclaredDifference` (CHG-56), `DispatchGuideSignerRules` y `DispatchGuidePdfService` (CHG-34, CHG-35), `WarehouseStorage.StatusLabel`, `ReleaseStateGuard`, `NationalizationBalance`, `ClaimsPrincipalExtensions.GetRequiredUserId()` y `useSubmitGuard`.

## Alcance
Implementa en el orden interno del plan:
- **CHG-69** Kanban por columna y cantidades separadas por unidad (`QuantityDisplay.Summary`, `ForDepositByUnit`, `LabelAmpara`).
- **CHG-70** «Validar depósito» compara con todos los camiones y se hace una sola vez (`DepositValidationMath`; guarda la plantilla).
- **CHG-71** Los filtros de órdenes de cargue buscan en los depósitos de la orden (`LoadingOrderStorageSearch`).
- **CHG-72** El responsable de la recepción es quien recibió en Bodega (`ReceptionLog.ReceivedById`).
- **CHG-73** Guía, factura y etiqueta muestran el producto, la agencia y la transportadora correctos (`CustomsAgencyResolver`, `GuideCarrierText`).
- **CHG-74** El inventario de Bodega muestra los Borradores con mercancía recibida (§10).
- **CHG-75** Las tarjetas de pendientes muestran el pesaje real.

CHG-69 y CHG-70 comparten `imports/[id]/index.vue`; CHG-72 y CHG-73 comparten `LabelGenerationService.cs` y los detalles de depósito: hazlos en serie. Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces.

## Migraciones y base de datos (regla 4.0.2)
- Esta fase genera **una migración: `AddValidationTemplateAndReceptionReceiver`** (CHG-70: `import_warehouse_storages.template_weight` y `template_quantity`, `numeric(18,4)`, nulas, sin valor por defecto; CHG-72: `reception_logs.received_by_id uuid` nula, FK a `users(id)` `ON DELETE RESTRICT` e índice). Genérala cuando CHG-70 y CHG-72 estén completos; revisa que contenga solo esas operaciones.
- Tú generas, aplicas, reviertes o eliminas, siempre con `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`.
- **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual. Si la migración no sale como esperas, corrige el modelo y regénerala.
- Solo la base local de pruebas de `Wms.Api` en Development. Tras generar, recrea la base (`database drop --force` y `database update`) y verifica que aplique sin errores. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios.
- **No escribas scripts de saneamiento ni de relleno** (`fase-10-*.sql`): las bases son de prueba y se recrean, así que no hay recepciones antiguas que rellenar; las que no tengan receptor se muestran con «—». Deja en tu informe solo las consultas de detección (`SELECT`).

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits. Para borrar archivos usa `rm`, no `git rm`.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español, con los estados traducidos. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real (los números de línea ya cambiaron en nueve fases), **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo. Si el comportamiento cambia, **detente y repórtalo**.
- **Sin retrocesos:**
  - CHG-69: los DTO de las listas cambian en el mismo cambio que el frontend; confirma por búsqueda que no queda ningún otro consumidor de los campos retirados (`stockSummary` reemplaza a `currentStock` y `unitMeasure` en el Kanban; `balances` reemplaza a las cantidades únicas en importaciones). El Kanban sigue mostrando los anulados en su columna «Anulado».
  - CHG-70: la tolerancia del 5 % no cambia; los depósitos ya validados antes quedan con plantilla nula y siguen como validados.
  - CHG-71: no cambian los filtros por número de orden, placa, depósito, fecha, producto ni transportadora.
  - CHG-72: `EntryLog.EntryAuthorizedBy` sigue siendo el responsable del ingreso en el bloque «Transporte»; los tres handlers de recepción asignan el receptor.
  - CHG-73: `DocumentProductLine` no cambia; Draft sigue imprimiendo etiqueta; la regla «NACIONALIZADA con cualquier levante» no se toca; las firmas de la guía siguen las reglas de CHG-34.
  - CHG-74: **CE no ve Borradores para cargue**: `ForeignTradeController` no activa `IncludeReceivedDrafts`; solo lo activa `WarehouseController`.
  - CHG-75: no cambian los DTO del API; solo el frontend lee los campos reales.

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo). Las pruebas existentes pasan sin editarlas, salvo las que una tarjeta manda reemplazar.
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. `yarn lint`: **no más de 290 errores** (la cifra de cierre de la Fase 9) y 0 en archivos nuevos. Reporta la cifra.
5. Recorre los criterios de aceptación de las siete tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega
Responde con:
1. La migración generada (nombre y operaciones) y el resultado de recrear la base.
2. Los archivos creados, modificados o borrados por cambio.
3. El resultado de cada compuerta, con números.
4. Los criterios sin verificar, las consultas de detección de cada tarjeta y cualquier desviación del plan.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend, commit 1:** el código de la fase, sin la migración. Asunto `feat(qa-fase-10): <resumen> (CHG-69 a CHG-75)` y un cuerpo con una línea por cambio (`- CHG-nn: …`).
   - **Backend, commit de migración:** `feat(qa-fase-10): migración AddValidationTemplateAndReceptionReceiver`, con una línea sobre qué cambia en la base. Lleva `Migrations/<timestamp>_AddValidationTemplateAndReceptionReceiver.cs`, su `.Designer.cs` y `AppDbContextModelSnapshot.cs`.
   - **Frontend:** `feat(qa-fase-10): <resumen> (CHG-nn, …)` con una línea por cambio. Indica qué archivos de `docs/`, `package.json` o los `components.d.ts` generados no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no avances a la Fase 11 ni marques la fase como completada.
