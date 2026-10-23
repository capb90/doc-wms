Eres el implementador de la corrección de **DEF-F11-017 (CRITICAL)** y **DEF-F11-016 (MAJOR)**, los dos defectos que dejan el informe final del QA del WMS de Bodegas Asociadas en NO-GO (`docs/qa/resultados/informe-final.md`, §4 y §7). Modelo recomendado: **Opus 5.5**, porque DEF-F11-017 toca el cálculo de la factura de almacenamiento y un error ahí es dinero. Todo lo anterior está corregido y con commit. **La base local tiene el dataset del QA: no la toques.**

Implementa en este orden: **DEF-F11-017 → DEF-F11-016**. Cada uno entrega su código, sus pruebas y la actualización de su ficha.

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica, en especial §7.4 (facturación de almacenamiento) y las decisiones D10/D11 (recálculo único que actualiza facturas aprobadas o pagadas).
2. `docs/qa/plan-correccion-defectos.md`: la sección «4.0 Reglas comunes» (4.0.2 migraciones, 4.0.10 «Sin retrocesos funcionales»).
3. `docs/qa/resultados/informe-final.md` §4 y §7, y `F11-informe-S4-2026-10-06.md`.
4. Las fichas `docs/qa/resultados/defectos/DEF-F11-017.md` y `DEF-F11-016.md`, con sus evidencias (`evidencias/F11/S4-DIR-P0-F6.txt` y `S4-DIR-P0-F2.txt`).

---

## DEF-F11-017 (CRITICAL): el recálculo del período de almacenamiento cobra el stock actual

**Causa (confirmada en el código).**
- `StorageBillingService.RecalculateCoreAsync` (paso 3, «Cargos con el stock y la TRM actuales») llama a `ResolveStorageChargesAsync`.
- Esa función toma solo los productos con `CurrentStock > 0` y usa `CurrentStock` como cantidad: `groupQuantity`, `StorageChargeProduct(p.ProductId, p.CurrentStock)` y `StockAtBilling` del período.
- En la apertura es correcto, porque al confirmar el stock es igual a lo recibido. En el recálculo de un período abierto, lo despachado durante el período deja de cobrarse, y un producto agotado sale de la factura.
- Lo dispara todo recálculo: CE-7, corrección de productos, camión tardío, manifiesto o fecha de ingreso, TRM manual, reversión, anulación de pesaje o refacturación.

**Decisión (cerrada).** Al **recalcular un período abierto**, la cantidad que se cobra por producto es la **cantidad facturable del período**:

> **cantidad facturable = `CurrentStock` + salidas netas por cargue del producto desde el inicio del período**

- **Salidas netas por cargue:**
  - suma los movimientos `InventoryMovement` del producto del depósito con `MovementType = Out` y `SourceType = LoadingOrder`;
  - resta los movimientos `In` con `SourceType = LoadingOrderReversal`, porque una reversión devuelve lo cargado;
  - cuenta solo los movimientos con `CreatedAt >= PeriodStart` del período que se recalcula.
- **Todo lo demás pasa por `CurrentStock` sin sumarse de vuelta**, porque precisamente por esos cambios se recalcula: ajustes de CE-7 y de la corrección de productos, camiones tardíos, pesajes anulados, daños y devoluciones.
- **Un producto con stock actual 0 pero con salidas en el período se sigue cobrando.**
- **Invariante:** recalcular un período sin ningún cambio debe dar exactamente el mismo total que tenía. Úsalo como prueba.

**Cambios.**
1. **Cantidad del recálculo.** `ResolveStorageChargesAsync` recibe una cantidad facturable por producto opcional (por ejemplo, `IReadOnlyDictionary<Guid, decimal>? billableQuantities`).
   - **Sin el parámetro** (apertura y renovación) se comporta exactamente como hoy: usa `CurrentStock`.
   - **Con el parámetro**, filtra los productos por cantidad facturable mayor que 0 en lugar de `CurrentStock > 0`, y usa esa cantidad en `groupQuantity`, en `StorageChargeProduct` y, por lo tanto, en `StockAtBilling` del período nuevo.
   - `BaseQuantity` (lo recibido) y el CIF prorrateado por `ReceivedQuantity` (ALM-14) no cambian.
2. **Cálculo de las salidas.** `RecalculateCoreAsync` calcula la cantidad facturable de cada producto con una consulta de los movimientos desde el inicio del período abierto que recalcula. Si hay varios períodos abiertos, usa el inicio del más antiguo, que es el que reemplaza el recálculo. Comprueba ese punto en el código y anótalo.
   - La consulta y la fórmula van en una función pura, testeable aparte (por ejemplo, `StorageBillableQuantity`), con un `<summary>` que cite DEF-F11-017 y §7.4.
3. **Rama de omisión.** El mensaje «El depósito no tiene stock para facturar; la factura del período no cambió.» solo aplica si la cantidad facturable de todos los productos es 0.
4. **Fuera de alcance:**
   - la apertura, la renovación y el cierre de períodos, que ya usan bien el stock;
   - las fórmulas (`FormulaPricing`), la TRM, el mínimo y el IVA;
   - la regla D10/D11 de que la factura conserve su N.º y su aprobación;
   - el borrado y la recreación del período en el recálculo, ni lo que hizo DEF-F7-007.

**Antes de escribir código, revisa el modelo.** Verifica en el código que los cargues registran `Out` con `SourceType.LoadingOrder` y que la reversión registra `In` con `LoadingOrderReversal`.
- Si algún flujo de salida de mercancía (por ejemplo, el despacho de una orden de inspección) usa otro `SourceType`, inclúyelo en la suma y anótalo.
- **Si las salidas no se pueden reconstruir con fiabilidad desde los movimientos, detente y repórtalo** con lo que propones. No generes migración sin aprobación.

**Pruebas.**
- **Unitarias de la función pura:**
  - sin salidas → `CurrentStock`;
  - con salidas en el período → stock + salidas;
  - salidas anteriores al inicio del período → no cuentan;
  - salida y reversión → se compensan;
  - un producto agotado con salidas → se cobra.
- **Integración, con el escenario del informe** (reutiliza `BillingScenario`):
  - depósito de 40 bultos confirmado; se cargan y despachan 30 dentro del período; un CE-7 de 41 → 40 dispara el recálculo;
  - la línea cobra **40** y el total queda igual al de antes del despacho (salvo lo que cambie el propio ajuste);
  - un producto agotado sigue en la factura.
- **Invariante:** recalcular sin cambios (por ejemplo, con TRM manual igual a la vigente o el disparador más neutro que exista) → mismo total, mismas líneas y mismo N.º y aprobación.
- **F6-REC-004:** la factura aprobada conserva su N.º y su aprobación y Facturación recibe el aviso con el total anterior y el nuevo.
- **Regresión:** las pruebas existentes de `StorageBillingService`, recálculo, renovación, D10/D11 y DEF-F7-007 pasan sin editarlas. **Si alguna esperaba cobrar el stock actual tras un despacho, detente y repórtala** antes de cambiarla.

---

## DEF-F11-016 (MAJOR): corregir el motivo de un ingreso con conductor lo saca de la cola de báscula

**Causa (confirmada en el código).**
- `EntryLog.CorrectEntryReason` y `UpdateEntryLogHandler` llaman a `EntryLog.EvaluateCompletionStatus()`, que pasa el ingreso a `Completed` cuando tiene conductor y motivo.
- `GetWeighbridgeQueueHandler` filtra `Status == EntryLogStatus.Registered`, así que el camión desaparece de la cola.
- Un ingreso creado con conductor y motivo nace `Registered` y sí está en la cola. Por eso la regla depende de si Vigilancia editó el ingreso, y eso no tiene sentido operativo.
- Según el código, `EntryLogStatus.Completed` solo se escribe en esos dos puntos y solo se lee en ese filtro.

**Decisión (cerrada).** El estado `Registered`/`Completed` del ingreso **no decide si el camión está en la cola de báscula**: la cola usa las mismas condiciones de hoy, salvo ese filtro.
- `GetWeighbridgeQueueHandler` deja de filtrar por `EntryLogStatus`. Se conservan `DateTimeDeparture == null` y las demás condiciones que ya tenga, como las de CHG-06 y CHG-36.
- `EvaluateCompletionStatus` sigue marcando «datos completos» como hoy; no se toca.
- Los ingresos de la base de QA que ya quedaron `Completed` (QAK504) vuelven a la cola sin tocar datos.

**Antes de cambiar el filtro**, busca en el backend y en el frontend cualquier otro lugar que lea `EntryLogStatus` o `status: 'Completed'` de un ingreso. Busca en especial la lista de pendientes de báscula (`GetPendingEntryLogs`), Vigilancia y la trazabilidad (`TruckStageResolver` recibe `entryStatus`).
- Si alguno lo usa con el significado de «fuera de la cola» o «terminado», aplica el mismo criterio y anótalo.
- Si alguno lo usa con otro significado legítimo, no lo toques y anótalo.

**Pruebas.**
- **Integración:**
  - ingreso con conductor → en la cola;
  - Vigilancia corrige el motivo (`F2-COR-011`) → sigue en la cola, con el motivo nuevo;
  - Vigilancia edita el ingreso (`UpdateEntryLog`) → sigue en la cola;
  - registra la salida → sale de la cola.
- **Regresión:** las pruebas de la cola (CHG-06, CHG-36, `DiscardOperationTests`) pasan sin editarlas. Recuerda liberar los camiones que dejes abiertos: la cola corta en 100.

---

## Sin retrocesos (regla 4.0.10)
- **DEF-F11-017:**
  - la apertura y la renovación facturan igual que hoy;
  - un recálculo sin despachos en el período da el mismo resultado que hoy;
  - la factura recalculada conserva su N.º y su aprobación (D10/D11);
  - el reporte por CPI (DEF-F7-007) no cambia.
- **DEF-F11-016:**
  - la cola no muestra camiones que ya salieron ni operaciones descartadas o en curso que hoy no muestra;
  - el resto de Vigilancia no cambia.

## Base de datos y entorno
- **No uses la base, el API ni el frontend locales** y no los reinicies. Las pruebas de integración usan su propio PostgreSQL con Testcontainers (Docker activo).
- No se espera migración. Al terminar, `dotnet ef migrations has-pending-model-changes` no debe reportar cambios. Si algo exigiera migración, detente y repórtalo.

## Restricciones (obligatorias)
- Trabaja en `develop`. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- No copies contraseñas ni secretos. No toques producción ni `infra/`.
- Textos y comentarios en español. Respeta la estructura por features.
- Nada fuera de estas dos fichas. Las observaciones de backlog del informe final quedan fuera.
- Si el código real contradice este prompt, adapta a lo que hay sin cambiar el comportamiento pedido y anótalo. Si el comportamiento cambia, detente y repórtalo.

## Fichas
- En `DEF-F11-017.md` y `DEF-F11-016.md`:
  - cambia el **Estado** a «Corregido»;
  - agrega una fila «Corregido» al Historial con la fecha, el resumen, las pruebas y «commits: pendiente».
- En `defectos/INDICE.md`, actualiza solo esos dos estados.
- No modifiques el informe final ni los informes de sesión: el veredicto lo actualiza QA tras el re-test.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` (1605 hoy) y `Wms.IntegrationTests` (269 hoy) en verde. Reporta los totales.
3. `has-pending-model-changes` sin cambios.
4. Si tocas el frontend: `yarn test`, `yarn build` y `yarn lint` (no más de 279 errores).
5. `git status` en los dos repos: solo los archivos de este alcance, más este prompt y las fichas.

## Entrega
Responde con:
1. Los archivos creados o modificados, por ficha.
2. Lo que verificaste del modelo de movimientos (qué `SourceType` usan el cargue, la reversión y cualquier otra salida) y los usos de `EntryLogStatus` que encontraste.
3. El resultado de cada compuerta, con números. Para DEF-F11-017, incluye el total de la factura del escenario antes del despacho, después del recálculo con el código viejo y después con el nuevo.
4. Las desviaciones y cualquier prueba existente que hayas tenido que reportar.
5. Lo que QA debe re-testear en local:
   - DEF-F11-017: F6-REC-001, 002 y 004, F6-ALM-002 y 012 con despachos parciales, y F11-REG-021;
   - DEF-F11-016: F2-COR-011 con conductor y F11-REG-005 y 006.
6. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `fix(qa-f11): el recálculo de almacenamiento cobra la cantidad del período y la corrección del motivo no saca al camión de la cola (DEF-F11-017, DEF-F11-016)`, con una línea por cambio.
   - **Frontend (documentación, y código si lo hubo):** `docs(qa-f11): fichas DEF-F11-016 y DEF-F11-017 corregidas`. Este prompt puede ir en el mismo commit.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** El re-test y la actualización del veredicto del informe final los hace QA, después de que el usuario reinicie el API.
