Eres el implementador de la **Fase 6** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: **Opus 5.5** para toda la fase: cambia el cierre de la salida en báscula, Bodega, Comercio Exterior y Vigilancia, el cobro de la guía y el kárdex. Las Fases 1 a 5 están completadas y con commit. Riesgo de regresión **alto**: la exactitud y la ausencia de retrocesos importan más que la velocidad.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 6** y las tarjetas **CHG-30 a CHG-40**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos. Decisiones del §10 que aplican aquí: «Salida de importación» (ninguna mercancía de importación sale sin guía), «Guía de orden multi-cliente» (una factura por cliente dueño), «Llegada a Bodega» (obligatoria antes del segundo pesaje), «OC sobre unidad de carga», «Etiqueta con levante parcial», «Mora» y «Operarios de báscula» (un solo operario; el doble envío sí es real).
3. Lo reutilizable de fases anteriores:
   - `Wms.IntegrationTests`: PostgreSQL en contenedor, colección `Api`, `WmsApiFactory`, `OperationalData`, `WeighbridgeScenario` y `BillingScenario`. `BillingScenario.Deposit` admite `TankerPlate` para depósitos con unidad de carga.
   - `EntryLogLock` (transacción → `FOR UPDATE` del ingreso → orden de cargue → commit → avisos), `UniqueViolationMessages`, `ClaimsPrincipalExtensions.GetRequiredUserId()`, `LoadingOrder.StatusLabel`.
   - Las reglas `EntryTicketExitRules` y `AdditionalOutputOrderRules`.
   - `VatMath`, `FormulaParameterValidator` y `PatchField<T>`.
   - En el frontend: `useSubmitGuard` y `RegistrationSummary`.

## Alcance
Implementa en el orden interno del plan. Los cambios que comparten archivo van en serie.
- **CHG-30** Vigilancia no registra la salida de un camión con pesaje sin terminar. Crea `EntryLogDepartureGuard` y `DepartureBlockRules`.
- **CHG-31** Cargue y devolución a Borrador con guardas de estado en los dos sentidos: `LoadingOrder.EnsureExecutable`, `BlocksStorageCorrection`, `WarehouseStorage.MarkForCorrection` con órdenes activas y `LoadingExecutionMath.EnsureStoragesConfirmed`.
- **CHG-32** La salida en báscula valida la orden y la pone «en cargue»: `OutputInitiationRules`, `FOR UPDATE` de la orden después del bloqueo del ingreso, `BeginWeighbridgeExit` y `ReleaseWeighbridgeExit`.
- **CHG-33** Una orden de importación solo se despacha con guía vigente: `ImportGuideRules` y `LoadingOrderGuideReader`. Se aplica en el repesaje, en el cargue con la salida ya registrada, en la salida con tiquete, en las órdenes adicionales, en la guía de regularización y en Vigilancia (la regla se agrega a `EntryLogDepartureGuard`).
- **CHG-34** La guía se cobra a cada cliente dueño, con el total visible antes de crearla: `DispatchGuideBillingPlan`, `DispatchGuideSignerRules` y `GET foreign-trade/loading-orders/{id}/dispatch-guide-preview`. En el frontend, la tabla multicliente en `BillingCollectForm.vue`.
- **CHG-35** La guía conserva el levante vigente al emitirla (`dispatch_guide_lines.release_number` y `acceptance_number`) y lo imprime al reimprimir.
- **CHG-36** El segundo pesaje exige la llegada registrada en Bodega.
- **CHG-37** La tara no puede superar el peso bruto.
- **CHG-38** El ajuste CE-7 valida primero, respeta los levantes y no depende del correo.
- **CHG-39** Todo cambio de stock por Comercio Exterior deja un movimiento en el kárdex.
- **CHG-40** Levantes y etiquetas solo en el estado que corresponde.

Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces con sus valores y mensajes exactos.

## Migraciones y base de datos (regla 4.0.2)
- Esta fase genera **una migración**: `AddDispatchGuideLineReleaseSnapshot` (CHG-35). Agrega las columnas `dispatch_guide_lines.release_number` y `dispatch_guide_lines.acceptance_number`, `varchar(500)` y nulas. Genérala cuando el modelo de CHG-35 esté completo, no al final de la fase. Revisa que solo contenga esas dos `AddColumn`, sin `UpdateData` ni índices ajenos.
- Tú generas, aplicas, reviertes o eliminas, siempre con `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`.
- **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual. Si una migración no sale como esperas, corrige el modelo y regénerala.
- Solo la base local de pruebas de `Wms.Api` en Development; nunca staging ni producción. Tras generar, recrea la base (`database drop --force` y `database update`) y verifica que aplique sin errores. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios.
- **No escribas scripts de saneamiento** (`fase-06-*.sql`) ni el relleno de levantes de las guías ya emitidas: las bases son de prueba y se recrean (regla 4.0.3). Las guías nuevas guardan el levante al emitirse. Deja en tu informe solo las consultas de detección (`SELECT`) de cada tarjeta.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit (ver abajo) y el usuario hace los commits. Para borrar archivos usa `rm`, no `git rm`, porque `git rm` deja la baja preparada en el índice.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español, con los estados traducidos (Pendiente, En progreso, Cargada, Despachada, Completa, Cancelada, Revertida; Borrador, Confirmado, Cerrado, Anulado). Dinero con `decimal` y el redondeo del repositorio. Fechas de negocio con `ColombiaTime`. Respeta la estructura por features.
- Concurrencia: toda escritura de báscula sigue el orden de `EntryLogLock`. El bloqueo nuevo de la orden (CHG-32) va **después** del bloqueo del ingreso y dentro de la misma transacción. Los avisos se envían después del commit.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real, **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo. Si el comportamiento cambia, **detente y repórtalo**.
- **Sin retrocesos:**
  - Exportación: la guía se genera sin cargo y la orden se despacha como hoy.
  - Inspección: se despacha sin guía.
  - Orden de un solo cliente: se cobra igual que hoy.
  - No se tocan `OperationalDateRules`, `/billing/preview` (lo usan báscula y montacargas), `LoadingOrder.Dispatch()`, `RevertDispatchToLoaded()`, `RevertLoadingOrderCommandHandler`, `DispatchGuideBalanceService`, `WeighingTotals`, `KardexAggregator`, `CorrectReceivedQuantity` ni lo demás que las tarjetas marcan «No se toca».
  - Ningún rol pierde una función que usa. Antes de agregar una guarda o un paso obligatorio, lista qué pantallas y roles llaman al endpoint.

## Verificación antes de terminar
1. `dotnet build` sin errores y sin avisos nuevos en archivos de la fase.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde, con Docker activo. Las pruebas existentes pasan sin editarlas, salvo las que una tarjeta manda reemplazar; si editas alguna, justifícalo.
3. Una prueba de integración del flujo completo de importación: orden → salida en báscula → cargue → guía → repesaje → salida en Vigilancia. Debe cubrir el caso con guía y el caso sin guía (409 en el repesaje y en Vigilancia).
4. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
5. `yarn lint`: **no más de 292 errores** (la Fase 5 cerró en 292) y 0 en archivos nuevos. Reporta la cifra.
6. Tipos de los `.vue` tocados: `vue-tsc` instalado en el scratchpad, con un tsconfig limitado a esos archivos. Reporta solo los errores nuevos frente a HEAD.
7. Recorre los criterios de aceptación de las once tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega
Responde con:
1. La migración generada (nombre y operaciones) y el resultado de recrear la base.
2. Los archivos creados, modificados o borrados por cambio.
3. El resultado de cada compuerta, con números.
4. Los criterios sin verificar, las consultas de detección de cada tarjeta y cualquier desviación del plan. Agrega el aviso operativo para Vigilancia y Báscula sobre la nueva regla de salida, en dos o tres líneas listas para enviar.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend, commit 1:** el código de la fase, sin la migración. Asunto `feat(qa-fase-6): <resumen> (CHG-30 a CHG-40)` y un cuerpo con una línea por cambio (`- CHG-nn: …`).
   - **Backend, commit de migración:** `feat(qa-fase-6): migración AddDispatchGuideLineReleaseSnapshot`, con una línea sobre qué cambia en la base. Lleva `Migrations/<timestamp>_AddDispatchGuideLineReleaseSnapshot.cs`, su `.Designer.cs` y `AppDbContextModelSnapshot.cs`.
   - **Frontend:** `feat(qa-fase-6): <resumen> (CHG-nn, …)`, con una línea por cambio. Indica qué archivos de `docs/`, `package.json` o los `components.d.ts` generados no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no avances a la Fase 7 ni marques la fase como completada.
