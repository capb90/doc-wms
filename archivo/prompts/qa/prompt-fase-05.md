Eres el implementador de la **Fase 5** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: Sonnet 5.5 para la fase, con **Opus 5.5 para CHG-24, CHG-25 y CHG-26** (reglas de IVA, mínimos y tarifas). Las Fases 1 a 4 están completadas y con commit. Esta fase toca **dinero**: la exactitud importa más que la velocidad.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 5** y las tarjetas **CHG-22 a CHG-29**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor, `BillingScenario`), `VatMath` (`Wms.Domain/Billing`), `Invoice.RefreshStatus`, `ClaimsPrincipalExtensions.GetRequiredUserId()`, el guardia de envío (`useSubmitGuard`) y `UniqueViolationMessages`.

## Alcance
Implementa en el orden interno del plan (los pares que comparten archivo van en serie):
- **CHG-22** Pagos solo en facturas emitidas; no se anula una factura con dinero.
- **CHG-23** N.º SIIGO en facturas de contado ya pagadas.
- **CHG-24** El mínimo de almacenamiento dice si incluye IVA (parámetro `minimumIncludesVat`, `service_minimum_values.includes_vat`).
- **CHG-25** El piso por unidad de carga no se cuenta como magnitud doble.
- **CHG-26** Reglas para perecederos configurables y PATCH del servicio de convenio sin borrar campos (`PatchField<T>`).
- **CHG-27** Parámetros del convenio validados con los rangos de la tarifa base.
- **CHG-28** Se retira la creación manual de facturas (pantalla y API).
- **CHG-29** El comprobante del pago se sube como archivo (`POST billing/payments/vouchers`) y se puede consultar.

Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces con sus valores exactos.

## Migraciones y base de datos (regla 4.0.2)
- Esta fase genera **dos migraciones, en este orden**: `AddMinimumIncludesVatSetting` (CHG-24 y CHG-25: `service_minimum_values.includes_vat` y el `UpdateData` del esquema de parámetros de las fórmulas) y `AddPerishableToRuleUniqueIndexes` (CHG-26: recrea `idx_agreement_service_unique_active` e `idx_service_pricing_rule_unique_active` con `applies_to_perishable`). Genera cada una cuando su modelo esté completo, no al final de la fase.
- Tú generas, aplicas, reviertes o eliminas, siempre con `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`): `migrations add`, `database update`, `database drop --force`, `migrations remove`.
- **Nunca edites a mano los archivos generados** (`Wms.Infrastructure/Migrations/*`, incluidos `*.Designer.cs` y el snapshot) ni modifiques la base con SQL manual. Si una migración no sale como esperas, corrige el modelo y regénerala; revisa que solo contenga las operaciones de su cambio.
- `includes_vat` es una columna `NOT NULL` nueva en una tabla que puede tener `HasData`: no le pongas `HasDefaultValue` en el modelo (falla del 1-oct-2026).
- Solo la base local de pruebas de `Wms.Api` en Development; nunca staging ni producción. Tras generar, recrea la base (`database drop --force` y `database update`) y verifica que aplique sin errores. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios.
- **No escribas scripts de saneamiento** (`fase-05-*.sql`): las bases son de prueba. Deja en tu informe solo las consultas de detección (`SELECT`).

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge.** Entregas los mensajes de commit (ver abajo); el usuario hace los commits.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Mensajes y textos en español. Dinero con `decimal` y el redondeo del repositorio. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real, **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo; si el comportamiento cambia, **detente y repórtalo**.
- Sin retrocesos: las facturas de contado, las guías a crédito y las consolidadas siguen como hoy; las reglas sin el parámetro `minimumIncludesVat` se leen como IVA incluido, de modo que **ningún total existente cambia** al desplegar; los PATCH ya verificados como seguros no se tocan. Al retirar `POST billing/invoices`, confirma que no queda ningún consumidor (báscula, guías y almacenamiento usan `Invoice.CreateFor*`, que no se toca).

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo). Las pruebas de facturación existentes pasan sin editarlas, salvo las que una tarjeta manda reemplazar.
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. `yarn lint`: no más de 296 errores y 0 en archivos nuevos. Reporta la cifra.
5. Recorre los criterios de aceptación de las ocho tarjetas y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega
Responde con:
1. Las dos migraciones generadas (nombre y operaciones) y el resultado de recrear la base.
2. Archivos creados o modificados por cambio.
3. Resultado de cada compuerta, con números.
4. Criterios sin verificar, consultas de detección omitidas y cualquier desviación del plan.
5. **Los mensajes de commit**, listos para pegar, con este formato y por separado:
   - **Backend, commit 1:** el código de la fase, sin migraciones. Asunto `feat(qa-fase-5): <resumen> (CHG-22 a CHG-29)` y cuerpo con una línea por cambio (`- CHG-nn: …`).
   - **Backend, commits de migración:** uno por migración, en el orden de generación (`feat(qa-fase-5): migración AddMinimumIncludesVatSetting`, etc.), con una línea sobre qué cambia en la base. Indica qué archivos (`Migrations/<timestamp>_<Nombre>.cs`, `.Designer.cs` y el snapshot) pertenecen a cada commit; si el snapshot no se puede separar, indícalo y propone un solo commit de migraciones.
   - **Frontend:** `feat(qa-fase-5): <resumen> (CHG-nn, …)` con una línea por cambio. Indica qué archivos de `docs/` o `package.json` no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no avances a la Fase 6 ni marques la fase como completada.
