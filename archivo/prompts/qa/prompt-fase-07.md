Eres el implementador de la **Fase 7** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad baja-media, riesgo de regresión bajo, sin migración). Las Fases 1 a 6 están completadas y con commit.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 7**, las tarjetas **CHG-41 a CHG-47** y la decisión **D-2** de §5 (resuelta: se retira «Cambiar modo de pago» del historial de báscula). Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor, `WmsApiFactory`, `OperationalData`, `WeighbridgeScenario`, `WeighbridgeFlow`), `EntryLogLock`, `EntryLogInfoUpdater`, `CarrierCompanyGuard`, `WeighbridgeOperationType`, `registration.ts` y `RegistrationSummary` del frontend, `useSubmitGuard`, `ClaimsPrincipalExtensions.GetRequiredUserId()` y las políticas de `WmsPolicyRoles`.

## Alcance
Implementa en el orden interno del plan:
- **CHG-41** Alta, detalle y edición de productos sin error 500 (`ProductProjection`).
- **CHG-42** La trazabilidad respeta la salida y no muestra etapas «Desconocido» (`TruckStageResolver`, `TruckStages`, `TraceabilitySummaryCalculator`).
- **CHG-43** Los depósitos cerrados se ven y los anulados no cuentan en el tablero (`WhereListed`).
- **CHG-44** La hora del pesaje propuesta es la hora actual (`resolveCapturedAt`, §10 · Hora del pesaje).
- **CHG-45** «Agregar otro depósito» se ofrece en el pesaje de un ingreso con depósito (`canOfferAddDeposit`).
- **CHG-46** Conductor y vehículo se guardan también en Solo báscula y en Salida (`EntryInfo` atómico dentro de la transacción).
- **CHG-47** Historial de báscula: corrección de pesos por rol (`weighing-permissions.ts`) y sin acciones muertas (D-2).

CHG-44 y CHG-45 tocan `WeightCapture.vue`: hazlos en serie. Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces.

## Migraciones y base de datos (regla 4.0.2)
Esta fase **no declara migración**. Tú gestionas la base solo con comandos `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`) y **nunca editas a mano los archivos generados** ni usas SQL manual. Si un cambio necesitara tocar el modelo, detente y repórtalo antes de generar nada. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Solo la base local de pruebas; nunca staging ni producción. **No escribas scripts de saneamiento** (`fase-07-*.sql`); deja en tu informe solo las consultas de detección (`SELECT`).

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits. Para borrar archivos usa `rm`, no `git rm`.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español. Fechas de negocio con `ColombiaTime`. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real (los números de línea ya cambiaron en seis fases), **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo. Si el comportamiento cambia, **detente y repórtalo**.
- Concurrencia: CHG-46 llama a `EntryLogInfoUpdater.ApplyAsync` dentro de la transacción y del bloqueo del ingreso de `EntryLogLock`; si el servicio falla, no se guarda nada del conductor ni del vehículo.
- **Sin retrocesos:**
  - Báscula sigue pudiendo registrar y cobrar como hoy: `isCollecting`, `RegistrationSummary` y la reanudación tras recargar no se tocan.
  - Un ciclo de varios depósitos conserva su pesaje intermedio (`MultiDeposit` del backend no cambia); «Agregar otro depósito» solo se ofrece a ingresos con depósito.
  - La hora del pesaje sigue siendo corregible por el operario dentro de la estadía del camión (`EnsureWeighingDate` no cambia).
  - En el historial, Admin y Báscula conservan editar peso y fecha; Facturación gana la corrección de pesos desde el detalle del ciclo, no desde el historial.
  - Al retirar «Cambiar modo de pago», confirma por búsqueda que no queda ningún consumidor de `PATCH weighbridge/{id}/payment-mode`; `ChangePaymentModeDialog.vue` **no se toca** (lo usan montacargas y guías).
  - La corrección de primer y segundo peso (`sequence`) ya se arregló en la Fase 6; no la repitas, solo confirma que `ModifyWeighingDialog.vue` sigue correcta.
- Actualiza también la documentación de QA que pide CHG-47 (`docs/qa/fase-03-bascula.md`, caso F3-HIS-008).

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo). Las pruebas existentes pasan sin editarlas, salvo las que una tarjeta manda reemplazar.
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. `yarn lint`: **no más de 292 errores** (la cifra de cierre de la Fase 6) y 0 en archivos nuevos. Reporta la cifra.
5. Recorre los criterios de aceptación de las siete tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega
Responde con:
1. Confirmación de que no hubo migración (resultado de `has-pending-model-changes`).
2. Los archivos creados, modificados o borrados por cambio.
3. El resultado de cada compuerta, con números.
4. Los criterios sin verificar, las consultas de detección de cada tarjeta y cualquier desviación del plan.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `feat(qa-fase-7): <resumen> (CHG-41 a CHG-47)` y un cuerpo con una línea por cambio que toque el backend (`- CHG-nn: …`). Sin commit de migración.
   - **Frontend:** `feat(qa-fase-7): <resumen> (CHG-nn, …)` con una línea por cambio. Indica qué archivos de `docs/`, `package.json` o los `components.d.ts` generados no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no avances a la Fase 8 ni marques la fase como completada.
