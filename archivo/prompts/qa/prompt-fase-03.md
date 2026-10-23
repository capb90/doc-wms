Eres el implementador de la **Fase 3** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: Opus 5.5. Las Fases 1 y 2 están completadas y con commit. Esta fase toca **dinero**: la exactitud importa más que la velocidad.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 3** y las tarjetas **CHG-09 a CHG-13**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor), Vitest y `ClaimsPrincipalExtensions.GetRequiredUserId()`.

## Paso previo: migración pendiente de la Fase 2
La Fase 2 cambió el modelo (rol ForeignTrade, `idx_vehicle_plate` único, `idx_entry_vehicle_open_unique`) pero su migración no se generó. Antes de tocar código de esta fase, comprueba con `dotnet ef migrations list` y `dotnet ef migrations has-pending-model-changes`; si falta, genera `FixRoleSeedAndOperationalUniqueness` con `dotnet ef migrations add`, revisa que solo contenga esas operaciones, recrea la base (`database drop --force` y `database update`) y repórtalo por separado para que el usuario la incluya en el commit de la Fase 2.

## Alcance
Implementa en este orden (el orden interno del plan es obligatorio porque CHG-12 y CHG-13 tocan `Invoice.cs` y `BillingJobService.cs` y CHG-13 parte del código que deja CHG-12):
- **CHG-09** Una tarifa solo aplica a su modalidad y producto (`RuleSpecificity`, `BillingResolver`).
- **CHG-10** El cierre manual abre el período siguiente desde el fin del cerrado (`StoragePeriodCalculator.StartAfter`).
- **CHG-11** El override fija el total de la línea con IVA incluido y rotulado; crea `VatMath` en el dominio, que reutiliza la Fase 5.
- **CHG-12** Solo vencen las facturas emitidas; el vencimiento se fija al aprobar.
- **CHG-13** Mora en una sola corrida y pagos parciales que vencen (`Invoice.RefreshStatus`, `OverdueSweep`, `ClientFinancialStatusRules`).

Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces con sus valores numéricos exactos (comprueba los importes de los ejemplos, p. ej. 501.865,34 y 196.350).

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge.**
- **Migraciones y base de datos (regla 4.0.2):** tú generas, aplicas, reviertes o eliminas, siempre con comandos `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`. **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual: si la migración no sale como esperas, corrige el modelo y regénerala. Solo la base local de pruebas de `Wms.Api` en Development; nunca staging ni producción. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Esta fase no declara migración; si un cambio la necesita, detente y repórtalo antes de generarla.
- **No escribas scripts de saneamiento.** Las bases son de prueba y se recrean (regla 4.0.3 actualizada). Si una tarjeta pide un script, omítelo y deja en tu informe la consulta de detección (solo `SELECT`).
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español. Fechas de negocio con `ColombiaTime`. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas ni cambies fórmulas de tarifas no mencionadas. Si algo contradice el plan o el código real, **detente y repórtalo**.
- Sin retrocesos: las facturas de contado, las guías a crédito y las consolidadas siguen funcionando como hoy; solo cambia lo que dice cada tarjeta. Para cada servicio que resuelve sin modalidad (BASCULA, MONTACARGAS, GUIA_SALIDA), confirma con una prueba que su cobro no cambia.
- La aritmética de dinero usa `decimal` y el redondeo que ya usa el repositorio; no introduzcas `double`.

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo). Todas las pruebas de facturación existentes deben seguir pasando sin editarlas, salvo las que la tarjeta indica reemplazar.
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. Lint del frontend con `yarn lint`: no más de 296 errores y 0 en archivos nuevos. Reporta la cifra.
5. Recorre los criterios de aceptación de las cinco tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega y detención
Responde con: el resultado del paso previo (migración de la Fase 2), archivos creados o modificados por cambio, resultado de cada compuerta con números, criterios sin verificar, cualquier desviación del plan y las consultas de detección omitidas. **Detente ahí**: no avances a la Fase 4 ni marques la fase como completada.
