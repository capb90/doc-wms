Eres el implementador de la **Fase 12** (la última) del plan de corrección de defectos QA del WMS de Bodegas Asociadas. Modelo recomendado: **Sonnet 5.5** (complejidad media, mecánica y extensa: unos 100 archivos en CHG-88). Las Fases 1 a 11 están completadas y con commit. Esta fase es casi toda de **frontend**; el backend solo cambia mensajes y rótulos de estado en CHG-90.

**Rango de esta sesión:** CHG-85 a CHG-90, salvo que el usuario te indique un rango menor. Se recomienda partirla así: sesión A = CHG-85 a CHG-87 (importaciones, avisos de error, navegación); sesión B = CHG-88 (formatos, el más extenso); sesión C = CHG-89 y CHG-90 (accesibilidad y textos). Si te dan un rango, implementa solo ese, respeta su orden interno y entrega los mensajes de commit de ese rango.

## Lee primero (en este orden)
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (las 10 reglas), el encabezado de la **Fase 12** y las tarjetas **CHG-85 a CHG-90**. Es el único alcance. Si el plan choca con el §10 de `docs/qa/00-plan-maestro.md`, manda el §10 (en particular «Bodega usa tableta», «el modo oscuro se mantiene» y «Catálogos sin autenticación aceptados»); la regla 4.0.10 «Sin retrocesos funcionales» manda sobre ambos.
3. Lo reutilizable de fases anteriores: `useSubmitGuard` y `submit-guard.ts` (CHG-18), `app/utils/colombia-date.ts` (con `toColombiaStartOfDayIso`, `toColombiaExcelDate`), `app/utils/role-routes.ts`, `usePermissions`, `weighing-labels` si existe, `WarehouseStorage.StatusLabel`, `LoadingOrder.StatusLabel`, `Invoice.StatusLabel` y `ReissueMessages` (si ya existen; si no, créalos según CHG-90), y las pruebas guardianas de `test/unit/guards/` si existen.

## Alcance
Implementa en el orden interno del plan:
- **CHG-85** Todos los `<LabelBase>` importados; se retira la página duplicada `receptions/create.vue` y sus componentes huérfanos (`ReceptionStepSearch.vue`, `ReceptionStepRegisterArrival.vue`), con sus exportaciones y READMEs.
- **CHG-86** Un solo dueño de los avisos de error y recuperación con el API caído (`ApiError`, `api-error-notifier`, `toast-dedupe`, `query-retry`, `useApiConnection`, `AppConnectionBanner`).
- **CHG-87** Sin callejones sin salida: inicio por rol (`resolveDeniedRedirect`), `app/error.vue` en español, `isGuid` y el middleware de ids, detalle de factura inexistente.
- **CHG-88** Un solo formato es-CO de números, montos y fechas en toda la interfaz (`formatNumber`, `formatKg`, `formatColombiaTime`, `locale="es-CO"` en los `InputNumber`, y la guardia estática).
- **CHG-89** Nombre accesible en botones y campos, y foco en el primer error (`focus-first-invalid`).
- **CHG-90** Textos visibles en español y sin términos técnicos (frontend y backend: rótulos de estado, «tercero», mensajes de facturación, auditoría con etiquetas, `weighing-labels`).

CHG-88, CHG-89 y CHG-90 comparten `history.vue`, `WeighbridgeHistoryTable.vue` y `PaymentDialog.vue`: hazlos en serie. Cada cambio entrega el código descrito, las pruebas de su tarjeta y los criterios Dado/Cuando/Entonces.

## Migraciones y base de datos (regla 4.0.2)
Esta fase **no declara migración**. Tú gestionas la base solo con comandos `dotnet ef` y **nunca editas a mano los archivos generados** ni usas SQL manual. Si un cambio necesitara tocar el modelo (por ejemplo, un rótulo de estado que exija columna), detente y repórtalo antes de generar nada. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Solo la base local de pruebas. **No escribas scripts de saneamiento**; `audit_logs.affected_table` conserva el nombre de la clase y solo cambia cómo se muestra.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits. Para borrar archivos usa `rm`, no `git rm`.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Textos en español. Respeta la estructura por features.
- No agregues funcionalidad fuera de las tarjetas. Si algo contradice el plan o el código real (los números de línea ya cambiaron en once fases), **adapta a lo que hay hoy sin cambiar el comportamiento pedido** y anótalo. Si el comportamiento cambia, **detente y repórtalo**.
- **Sin retrocesos:**
  - CHG-85: confirma por búsqueda que nada enlaza `/warehouse/receptions/create` y que la recepción directa sigue funcionando desde `/warehouse/receptions` → «Recepción Directa»; `useSearchByPlate` se conserva (lo usa `ForkliftUseDialog.vue`).
  - CHG-86: `ApiError` conserva las lecturas existentes (`message`, `description`, `response.status`, `response.data`) para que ningún componente que hoy lee el error deje de funcionar; no cambia la renovación del token ante 401 ni los `refetchInterval`; una acción del usuario nunca queda en cola para reenviarse sola (`networkMode: 'always'` en mutaciones); la sesión solo se cierra con 401 o 403 al leer el usuario actual.
  - CHG-87: el logo y `/` siguen llevando a Admin y Comercio Exterior a `/`; los demás roles van a su inicio; la búsqueda de placa de la barra superior no cambia; la ruta `[id]` con GUID válido sigue llamando al API.
  - CHG-88: **los PDF que replican el legacy conservan su formato** (`DepositPdfService`, `DispatchGuidePdfService`, `LabelGenerationService`); `excel-export.ts` no se rehace; el formato global del `DatePicker` (`dd/mm/yy`) no cambia.
  - CHG-89: no cambies los componentes de PrimeVue ni el modo oscuro; en Bodega (tableta) «Buscar» lleva texto visible porque el tooltip no aparece al tocar.
  - CHG-90: no cambies rutas, clases, claves de consulta ni nombres de variables, solo textos visibles; el término «Facturación por CPI» del menú se conserva; `LoadingOrder.StatusLabel`, `Invoice.cs:242,444` y `OverrideBillingAmountHandler.cs:26` no se tocan.
- La guardia estática de CHG-88 (`source-guards.spec.ts`) debe quedar en 0 hallazgos; no la satisfagas excluyendo archivos.

## Verificación antes de terminar
1. Si tu rango toca backend (CHG-90): `dotnet build` sin errores y `dotnet test` de `Wms.Tests` y `Wms.IntegrationTests` en verde (Docker activo); las pruebas existentes pasan sin editarlas, salvo las que una tarjeta manda reemplazar.
2. `yarn build` con código 0 y `yarn test` en verde en `Frontend/wms`. Las pruebas de zona horaria corren con `TZ` en UTC, America/Bogota y Asia/Tokyo.
3. `yarn lint`: **no más de 290 errores** (la cifra de cierre de la Fase 11) y 0 en archivos nuevos. CHG-88 toca muchos archivos: no puede subir el lint. Reporta la cifra.
4. Recorre los criterios de aceptación de las tarjetas de tu rango y anota cuáles quedaron verificados por prueba y cuáles solo por lectura. Para CHG-86 y CHG-87, deja indicado qué pasos del checkpoint (API detenido y reiniciado, inicio de los seis roles, navegador en inglés) debe ver el usuario en el navegador.

## Entrega
Responde con:
1. Confirmación de que no hubo migración (resultado de `has-pending-model-changes`) si tu rango toca backend.
2. Los archivos creados, modificados o borrados por cambio (para CHG-88, el recuento por tipo de reemplazo y la cifra de la guardia antes y después).
3. El resultado de cada compuerta, con números.
4. Los criterios sin verificar y cualquier desviación del plan.
5. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend** (solo si tu rango incluye CHG-90): `feat(qa-fase-12): <resumen> (CHG-90)` con una línea por cambio. Sin commit de migración.
   - **Frontend:** `feat(qa-fase-12): <resumen> (CHG-nn, …)` con una línea por cambio. Indica qué archivos de `docs/`, `package.json` o los `components.d.ts` generados no pertenecen al commit de código.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí**: no marques la fase como completada. Con esta fase se cierra el plan; el cierre y la fase 11 de QA los decide el usuario (§7.2).
