Eres el implementador de la **Fase 11** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad media; riesgo de regresión medio en CHG-77 y CHG-84). Las Fases 1 a 10 están completadas y con commit.

**Rango de esta sesión:** CHG-76 a CHG-84 (los 9 cambios), salvo que el usuario te indique un rango menor (por ejemplo «solo CHG-76 a CHG-80» o «solo CHG-81 a CHG-84»). Si te dan un rango, implementa solo ese, respeta su orden interno y entrega los mensajes de commit de ese rango.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 11** y las tarjetas **CHG-76 a CHG-84**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10 (en particular «Reporte de ingresos diarios: solo Confirmados y Cerrados» y «Hora del pesaje»); la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor, `WmsApiFactory`, escenarios de báscula, facturación y comercio exterior), `ColombiaTime`, `PlateNormalizer`, `TruckStageResolver` y `TruckStages` (CHG-42), `WeighingTotals`, `WhereListed`, `inventory-labels.ts` y `StockChangeMovement` (CHG-39), `InvoicePdfService`, `ClaimsPrincipalExtensions`, `InvalidRequestBodyFilter` y `UniqueViolationMessages`, y las políticas de `WmsPolicyRoles`.

## Alcance
Implementa en el orden interno del plan:
- **CHG-76** Historial, tablero y reporte diario de báscula cuadran entre sí (`WeighingTotals`, `GET weighbridge/dashboard`, `DailyBillingServiceKind`).
- **CHG-77** Filtros por fecha con el día de Colombia y sin 500 (`QueryInstantParser`, model binder de `DateTimeOffset`, helpers del frontend).
- **CHG-78** Movimientos y kárdex se exportan completos y se ven sin expandir (`all=true`, hoja «Movimientos»).
- **CHG-79** El reporte de salidas diarias incluye los despachos sin guía (`OutgoingGoodsRowRules`).
- **CHG-80** Las estadísticas de facturación solo llegan al Admin (`StatisticsVisibility`).
- **CHG-81** Trazabilidad: «Hoy» de Colombia, placa sin distinguir mayúsculas y aviso en español (`TraceabilityDateRange`, `TraceabilityNotification`).
- **CHG-82** El reporte de ingresos diarios muestra placa, tiquete y neto (`DailyIncomingGoodsRowBuilder`).
- **CHG-83** Las exportaciones a Excel escriben las fechas en hora de Colombia (`toColombiaExcelDate`).
- **CHG-84** Documentos impresos con detalle, contacto real y una sola fuente de datos de la empresa (parámetros `COMPANY_*`, `CompanyInfoProvider`, ocho PDF).

CHG-77 va antes que CHG-78 y CHG-83 (los usan); CHG-83 va después de CHG-78 (mismo `warehouse-movements.vue`); CHG-84 va después de CHG-82 (mismo `DailyIncomingGoodsPdfService.cs`). Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces.

## Migraciones y base de datos (regla 4.0.2)
- Esta fase genera **una migración: `SeedCompanyParameters`** (CHG-84: seis filas nuevas en `system_parameters` con `HasData`, sin columnas nuevas). Los seis `HasData` llevan `Id` fijo, `DataType = "string"` y `IsActive = true`, con el mismo patrón del seed existente `INVENTORY_ADJUSTMENT_ADMIN_EMAIL`; sin `HasDefaultValue`. Revisa que la migración contenga solo esas seis filas.
- Tú generas, aplicas, reviertes o eliminas, siempre con `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`.
- **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual. Si la migración no sale como esperas, corrige el modelo y regénerala.
- Solo la base local de pruebas de `Wms.Api` en Development. Tras generar, recrea la base (`database drop --force` y `database update`) y verifica que aplique sin errores. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios.
- **No escribas scripts de saneamiento** (`fase-11-*.sql`): las bases son de prueba y se recrean, así que no hay parámetros `COMPANY_*` previos que borrar. Deja en tu informe solo las consultas de detección (`SELECT`).
- Si el usuario te indica un rango sin CHG-84, esta sesión **no genera migración**.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits. Para borrar archivos usa `rm`, no `git rm`.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español. Fechas de negocio con `ColombiaTime`. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real (los números de línea ya cambiaron en diez fases), **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo. Si el comportamiento cambia, **detente y repórtalo**.
- **Sin retrocesos:**
  - CHG-76: no cambies el filtro terminal del historial ni `GetPendingSecondWeightHandler`; la etiqueta «Solo Pesaje» se conserva.
  - CHG-77: no cambies los endpoints con `DateOnly`, `GetInvoicesHandler` ni `UtcDateTimeOffsetNormalizer`; con el binder, `toDate=2026-10-02` cubre ese día completo en Colombia y las peticiones con `-05:00` dejan de dar 500.
  - CHG-79: el cálculo de levantes y las secciones de Levantes y Despachos del reporte no cambian.
  - CHG-80: la página de estadísticas de Admin sigue mostrando facturación como hoy; solo CE deja de recibirla.
  - CHG-81: la ruta `/?plate=` de la barra superior y los avisos de `TraceabilityUpdated` siguen funcionando; solo cambia el título visible.
  - CHG-82: se conserva la fecha de creación del depósito como fecha del informe (§5.1 del plan).
  - CHG-84: **con los valores sembrados, el pie de cada PDF reproduce exactamente el texto actual**; compara el texto de los ocho PDF antes y después. Los datos sembrados son los del pie del legacy: `COMPANY_NAME` «Bodegas Asociadas Ltda», `COMPANY_NIT` «837.000.606-1», `COMPANY_ADDRESS` «CALLE 3 ESTE No. 2-732 BARRIO EL TEJAR», `COMPANY_PHONE` «7736748 - 7736522», `COMPANY_EMAIL` «info@bodegasasociadas.com» y `COMPANY_CITY` «IPIALES - COLOMBIA». `LoadingOrderPdfService`, `WarehouseNoveltyPdfService` y `TranslatePaymentStatus` no se tocan.

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo). Las pruebas existentes pasan sin editarlas, salvo las que una tarjeta manda reemplazar.
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`. Las pruebas de zona horaria de `colombia-date.spec.ts` corren con `TZ` en UTC, America/Bogota y Asia/Tokyo.
4. `yarn lint`: **no más de 290 errores** (la cifra de cierre de la Fase 10) y 0 en archivos nuevos. Reporta la cifra.
5. Recorre los criterios de aceptación de las tarjetas de tu rango y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega
Responde con:
1. La migración generada (nombre y operaciones) y el resultado de recrear la base, o la confirmación de que no hubo migración en tu rango.
2. Los archivos creados, modificados o borrados por cambio.
3. El resultado de cada compuerta, con números.
4. Los criterios sin verificar, las consultas de detección de cada tarjeta y cualquier desviación del plan.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend, commit 1:** el código de tu rango, sin la migración. Asunto `feat(qa-fase-11): <resumen> (CHG-76 a CHG-84)` (o tu rango) y un cuerpo con una línea por cambio (`- CHG-nn: …`).
   - **Backend, commit de migración** (solo si hubo): `feat(qa-fase-11): migración SeedCompanyParameters`, con una línea sobre qué cambia en la base. Lleva `Migrations/<timestamp>_SeedCompanyParameters.cs`, su `.Designer.cs` y `AppDbContextModelSnapshot.cs`.
   - **Frontend:** `feat(qa-fase-11): <resumen> (CHG-nn, …)` con una línea por cambio. Indica qué archivos de `docs/`, `package.json` o los `components.d.ts` generados no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no avances a la Fase 12 ni marques la fase como completada.
