Eres el implementador de la **Fase 8** del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad media por volumen: 12 cambios, riesgo de regresión bajo, sin migración). Las Fases 1 a 7 están completadas y con commit.

**Rango de esta sesión:** CHG-48 a CHG-59 (los 12 cambios), salvo que el usuario te indique un rango menor (por ejemplo «solo CHG-48 a CHG-53» o «solo CHG-54 a CHG-59»). Si te dan un rango, implementa solo ese, respeta su orden interno y entrega los mensajes de commit de ese rango.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 8** y las tarjetas **CHG-48 a CHG-59**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10; la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `Wms.IntegrationTests` (PostgreSQL en contenedor, `WmsApiFactory`, `OperationalData`, escenarios de báscula y facturación), `UniqueViolationMessages` (CHG-17), `GlobalExceptionHandler`, `PatchField<T>` y su convertidor (CHG-26), `ClaimsPrincipalExtensions.GetRequiredUserId()`, `EntryLogInfoUpdater`, `CarrierCompanyGuard`, `PlateNormalizer`, `StockChangeMovement` y `WarehouseStorage.StatusLabel`.

## Alcance
Implementa en el orden interno del plan:
- **CHG-48** Cuerpo inválido responde 400 con el campo (`InvalidRequestBodyFilter`, `RequestBodyErrorMessages`) y errores de base de datos sin texto interno (`DatabaseErrorMessages`).
- **CHG-49** Unicidad de NIT, SKU y nombre de producto con mensajes de negocio.
- **CHG-50** Administración de usuarios: contraseñas coincidentes, un rol mínimo y un Admin activo.
- **CHG-51** Login y recuperación de contraseña no revelan qué cuentas existen.
- **CHG-52** Ingreso sin fecha futura y salida no anterior al ingreso.
- **CHG-53** El API de registro y cobro aplica las reglas de la pantalla y ya no recibe efectivo ni cambio (§10).
- **CHG-54** Documento con ingreso de camiones cerrado se muestra cerrado desde la búsqueda.
- **CHG-55** Máximo 5 fotos por recepción y por cargue, solo imágenes reales (`PhotoUploadRules`).
- **CHG-56** Producto declarado y no contado cuenta como faltante y avisa a CE.
- **CHG-57** La novedad advierte (no rechaza) cuando el desglose no cuadra con el total.
- **CHG-58** Montacargas: horómetros válidos, mensajes de negocio e historial completo.
- **CHG-59** Los demás PATCH dejan de borrar o desactivar lo que no se envía.

CHG-48 y CHG-49 comparten `GlobalExceptionHandler.cs` y `UniqueViolationMessages`; CHG-55 y CHG-56 comparten los handlers de recepción: hazlos en serie. Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces.

## Migraciones y base de datos (regla 4.0.2)
Esta fase **no declara migración**: CHG-53 conserva las columnas `invoice_payments.cash_received` y `change_given` y solo deja de escribirlas y de exponerlas. Tú gestionas la base solo con comandos `dotnet ef` desde `Backend/wms-api` (`--project Wms.Infrastructure --startup-project Wms.Api`) y **nunca editas a mano los archivos generados** ni usas SQL manual. Si un cambio necesitara tocar el modelo, detente y repórtalo antes de generar nada. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Solo la base local de pruebas. **No escribas scripts de saneamiento** (`fase-08-*.sql`); deja en tu informe solo las consultas de detección (`SELECT`).

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits. Para borrar archivos usa `rm`, no `git rm`.
- No copies contraseñas ni secretos. No ejecutes ni apliques nada contra producción, Azure o staging. **Única excepción en `infra/`:** CHG-48 cambia `infra/main.tf:102` a `"Production"` solo en el repositorio; no ejecutes `terraform` ni ningún comando de despliegue.
- Mensajes y textos en español. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real (los números de línea ya cambiaron en siete fases), **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo. Si el comportamiento cambia, **detente y repórtalo**.
- **Sin retrocesos:**
  - CHG-48: no quites `SuppressModelStateInvalidFilter` (`Program.cs`); el filtro nuevo solo actúa cuando el cuerpo no se pudo leer, y los parámetros anulables sin cuerpo (`AbandonmentController`, `ForeignTradeController`, `LegacyImportController`) siguen aceptándose.
  - CHG-50: no cambies el alta de usuarios en el backend (ya exige un rol) ni la edición (`resolverEdit`).
  - CHG-51: «Usuario inactivo» solo se muestra con la contraseña correcta; la recuperación responde siempre 204.
  - CHG-53: los datos de Comercio Exterior siguen sin ser obligatorios en báscula (importador, agencia, fecha del documento, valor y manifiesto); solo se validan el valor y la moneda cuando vienen. Las columnas de efectivo y cambio se conservan en la base.
  - CHG-57: advertencia con confirmación en la pantalla, **no** rechazo; un desglose en cero o cuadrado se acepta como hoy.
  - CHG-58: no cambies las restricciones `chk_forklift_*` de la base ni el cálculo de tarifas.
  - CHG-59: solo los cinco PATCH listados en la tarjeta; los ya verificados como seguros no se tocan.

## Verificación antes de terminar
1. `dotnet build` sin errores.
2. `dotnet test` de `Wms.Tests` y de `Wms.IntegrationTests` en verde (Docker activo). Las pruebas existentes pasan sin editarlas, salvo las que una tarjeta manda reemplazar o eliminar (`CashChangeCalculatorTests` se borra entero por CHG-53).
3. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`.
4. `yarn lint`: **no más de 290 errores** (la cifra de cierre de la Fase 7) y 0 en archivos nuevos. Reporta la cifra.
5. Sondeo del CHG-48: `POST product` con el cuerpo `{"__qa":` responde 400 con «El cuerpo de la solicitud no es un JSON válido.»; anótalo en el informe.
6. Recorre los criterios de aceptación de las tarjetas de tu rango y anota cuáles quedaron verificados por prueba y cuáles solo por lectura.

## Entrega
Responde con:
1. Confirmación de que no hubo migración (resultado de `has-pending-model-changes`).
2. Los archivos creados, modificados o borrados por cambio.
3. El resultado de cada compuerta, con números.
4. Los criterios sin verificar, las consultas de detección de cada tarjeta y cualquier desviación del plan.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `feat(qa-fase-8): <resumen> (CHG-48 a CHG-59)` (o el rango que implementaste) y un cuerpo con una línea por cambio que toque el backend (`- CHG-nn: …`). Sin commit de migración. Incluye `infra/main.tf` en este commit, indicando que no se aplicó.
   - **Frontend:** `feat(qa-fase-8): <resumen> (CHG-nn, …)` con una línea por cambio. Indica qué archivos de `docs/`, `package.json` o los `components.d.ts` generados no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no avances a la Fase 9 ni marques la fase como completada.
