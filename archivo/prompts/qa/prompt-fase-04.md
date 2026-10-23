Eres el implementador de la **Fase 4** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: Opus 5.5. Las Fases 1 a 3 están completadas y con commit. Esta es la fase de mayor complejidad técnica del plan: **transacciones y concurrencia en báscula**.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 4** y las tarjetas **CHG-14 a CHG-21**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor, `CreateClientForRoleAsync`, `OperationalData`), Vitest, `ClaimsPrincipalExtensions.GetRequiredUserId()`, `WmsPolicyRoles` y `CarrierCompanyGuard`.

## Alcance
Implementa en el orden interno del plan:
- **CHG-14** `ValidationBehavior` también para comandos sin respuesta (`IBaseRequest`).
- **CHG-15** El autor de cada operación sale del token; la firma del cargue es obligatoria.
- **CHG-16** El acceso se corta al desactivar, cambiar roles o cerrar sesión (sello de seguridad).
- **CHG-17** Idempotencia de báscula: `EntryLogLock`, transacciones, `IsPrimary`, índices únicos parciales y `UniqueViolationMessages`.
- **CHG-18** Guardia de envío común en el frontend y formulario de pago que conserva lo digitado.
- **CHG-19** El cobro de báscula propone al cliente de la operación.
- **CHG-20** Retomar una operación tras recargar (registro guardado, tipo real, solo lectura, aviso al recargar).
- **CHG-21** «Información General» editable en un depósito en Borrador.

CHG-19 y CHG-20 tocan `app/pages/operations/weighbridge/index.vue` en bloques distintos: hazlos en serie. Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces.

## Migraciones y base de datos (regla 4.0.2)
- Esta fase genera **`AddLoadingOrderSignatureAndWeighbridgeIdempotency`**: `loading_orders.signature_driver`, `service_record_entry_logs.is_primary` y los tres índices únicos parciales del encabezado de la fase.
- Tú generas, aplicas, reviertes o eliminas, siempre con `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`.
- **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual. Si la migración no sale como esperas, corrige el modelo y regénerala. Revisa que solo contenga las operaciones de esta fase.
- `is_primary` es `NOT NULL` en una tabla que puede tener `HasData`: no le pongas `HasDefaultValue`.
- Solo la base local de pruebas de `Wms.Api` en Development; nunca staging ni producción. Tras generar, recrea la base (`database drop --force` y `database update`) y verifica que aplique sin errores. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios.
- **No escribas scripts de saneamiento** (`fase-04-*.sql`): las bases son de prueba y se recrean. Deja en tu informe solo las consultas de detección (`SELECT`).

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge.**
- Orden de bloqueo fijo en báscula: primero el ingreso (`entry_logs … FOR UPDATE`), después la orden de cargue. Abre la transacción, bloquea, lee, guarda, confirma y solo entonces notifica.
- Los tokens emitidos antes del cambio de CHG-16 responden 401 en la primera petición y la aplicación los renueva con el refresh: es lo esperado; no cambies la vida del token.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real (por ejemplo, números de línea que ya cambiaron en fases anteriores), **adapta al código actual sin cambiar el comportamiento pedido** y anótalo; si cambia el comportamiento, **detente y repórtalo**.
- Sin retrocesos: «Cobrar» de báscula (`isCollecting`) ya está protegido y no se toca; Comercio Exterior conserva el alta de vehículos y conductores; un cobro legítimo de varios camiones o depósitos sigue funcionando con los vínculos adicionales (`IsPrimary = false`).

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo), incluidas las pruebas de concurrencia de CHG-17 (dos registros o cobros simultáneos: uno pasa y el otro responde 409).
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. Lint del frontend: tope 296 errores (hoy 295) y 0 en archivos nuevos. Mídelo con `yarn lint -f json` y reporta la cifra.
5. Mide el tiempo de un registro de báscula en la prueba de integración (antes y después de los bloqueos) para el checkpoint PRF-002.
6. Recorre los criterios de aceptación de las ocho tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega y detención
Responde con: la migración generada (nombre y operaciones) y el resultado de recrear la base, archivos creados o modificados por cambio, resultado de cada compuerta con números, criterios sin verificar, consultas de detección omitidas y cualquier desviación del plan. **Detente ahí**: no avances a la Fase 5 ni marques la fase como completada.
