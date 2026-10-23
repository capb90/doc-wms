Eres el implementador de la **Fase 2** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: Opus 5.5. La Fase 1 ya está completada y con commit.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 2** y las tarjetas **CHG-04 a CHG-08**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo que dejó la Fase 1 y puedes reutilizar: `Wms.IntegrationTests` (fábrica con PostgreSQL en contenedor), Vitest en el frontend y las políticas de `Wms.Domain/Security/WmsPolicyRoles.cs`.

## Alcance
Implementa en este orden, sin salirte de cada tarjeta:
- **CHG-04** Avisos por rol a Comercio Exterior (siembra del rol y destino «Weighbridge» inexistente).
- **CHG-05** Regla única de placa (normalizar, validar, única, búsqueda por igualdad), incluido `CarrierCompanyGuard`.
- **CHG-06** Descartar una operación libera el camión y bloquea su cobro.
- **CHG-07** Recepción de unidades de carga sin contar productos.
- **CHG-08** Recepción sin báscula: contrato, ingreso existente, depósito en Borrador y `GetRequiredUserId()`.

Cada cambio entrega el código descrito, las pruebas de su tarjeta y el cumplimiento de sus criterios Dado/Cuando/Entonces.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge.**
- **Migraciones y base de datos (regla 4.0.2):** tú generas, aplicas, reviertes o eliminas, siempre con comandos `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`. **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual: si la migración no sale como esperas, corrige el modelo y regénerala. Solo la base local de pruebas de `Wms.Api` en Development; nunca staging ni producción. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Esta fase genera `FixRoleSeedAndOperationalUniqueness`; después recrea la base (`database drop --force` y `database update`) y verifica que aplique sin errores. No pongas `HasDefaultValue` en columnas nuevas `NOT NULL` de tablas con `HasData`.
- **No escribas scripts de saneamiento.** Las bases son de prueba y tú las recreas con la migración nueva, así que no hay datos que depurar. Si una tarjeta pide un script, omítelo y deja en tu informe la consulta de detección (solo `SELECT`) para usarla como verificación después de recrear. Los índices únicos de esta fase se prueban en `Wms.IntegrationTests` con base limpia.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real, **detente y repórtalo**.
- Sin retrocesos: antes de restringir o cambiar un comportamiento, confirma qué pantallas lo usan y con qué roles. En especial, un vehículo inactivo sigue recibiendo ingresos (`CreateEntryLogHandler.cs:66`) y Comercio Exterior conserva el alta de vehículos y conductores en la orden de cargue.

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo).
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. Lint del frontend con `yarn lint`: no más de 296 errores y 0 en archivos nuevos. Reporta la cifra.
5. Recorre los criterios de aceptación de las cinco tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega y detención
Responde con: archivos creados o modificados por cambio, resultado de cada compuerta con números, criterios sin verificar, la migración generada (nombre y operaciones) y el resultado de recrear la base, cualquier desviación del plan y mensajes de commit. **Detente ahí**: no avances a la Fase 3 ni marques la fase como completada.
