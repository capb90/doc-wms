Eres el implementador de la corrección de **DEF-MIG-001 a DEF-MIG-006**, los defectos que encontró la Fase 1 del plan de migración del WMS de Bodegas Asociadas (`docs/planes/migracion-staging/plan-migracion-legacy-staging.md`). Modelo recomendado: **Opus 5.5**: toca el importador de la migración, la guía de salida y el cálculo del CIF, y los errores ahí son dinero o datos de aduana. **Tu trabajo es corregir el código y el plan de exportación, no repetir la migración.** La Fase 1 la repite otro agente con su propio prompt (`prompt-fase-1-repeticion.md`).

## Lee primero
1. `Backend/wms-api/AGENTS.md` y el documento de contexto que indica.
2. `docs/planes/migracion-staging/plan-migracion-legacy-staging.md`, en especial §3 (reglas comunes).
3. `docs/planes/migracion-staging/resultados/informe-fase-1.md` y las seis fichas de `resultados/defectos/DEF-MIG-001.md` a `DEF-MIG-006.md`.
4. `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md`:
   - F6-02 (≈ líneas 2779-2868);
   - F6-03 (≈ 2872-2980), con las consultas de exportación de depósitos (≈ 2920-2938) y levantes (≈ 2945-2953) y las reglas del CSV de depósitos;
   - F6-04 (≈ 2984-3015).
5. **Las consultas congeladas** que usó la Fase 1, como referencia: `code_workspace/db_legacy/trabajo/consultas/11_depositos.sql`, `11_depositos_original.sql`, `12_levantes.sql`, `12_levantes_original.sql` y `12_levantes_sin_agrupar.sql`. Están fuera de git y no tienen datos personales; son solo SQL. **No copies a git ningún CSV ni extracto de esa carpeta.**
6. **El código:**
   - `Wms.Application/Administration/LegacyImport/`: `LegacyDepositRowParser`, `DepositsImporter`, `ReleasesImporter`, `LegacyReleaseFobSplitter` y `DepositReconciler`;
   - `Wms.Domain/Entities/Warehouse/WarehouseStorage.cs` (`CreateMigrated`);
   - `Wms.Application/ForeignTrade/Common/Services/DispatchGuideBalanceService.cs` y `DispatchGuideBalanceCalculator.cs`;
   - `StorageBillingService` (`CalculateCargoValueCop` y el texto de la advertencia del mínimo);
   - `Frontend/wms/app/features/foreign-trade/components/DepositDetailDocumentStakeholdersSection.vue`.

Implementa en este orden: **DEF-MIG-005 → DEF-MIG-003 → DEF-MIG-002 → DEF-MIG-001 → DEF-MIG-004 → DEF-MIG-006.**

---

## DEF-MIG-005 (CRITICAL): la guía ignora las salidas del legacy en los depósitos migrados

**Causa (confirmada).** `DispatchGuideBalanceService` calcula «lo despachado antes» solo con las líneas de guías de la v2. La salida de apertura de la migración (`InventoryMovement` `Out` con `SourceType = MigrationOpening`, creada con `salen` por `DepositsImporter`) no cuenta. Resultado: la guía imprime saldo anterior 648 y nuevo saldo 598 cuando lo correcto es 448 y 398, en 66 de 128 depósitos.

**Decisión (cerrada).**
- Para un producto de depósito migrado, **lo despachado antes = la salida de apertura de la migración + las líneas de guías de la v2**, con las exclusiones de hoy: guías anuladas y órdenes canceladas o revertidas.
- La salida de apertura se lee del movimiento `Out`/`MigrationOpening` del producto. Si un producto migrado tiene más de uno, se suman.
- Para un depósito no migrado nada cambia.
- Va en el servicio, dentro del bloqueo actual (`FOR UPDATE`), en una sola consulta adicional por guía, no una por producto.
- Revisa también que la **reimpresión** y cualquier otro lugar que calcule el saldo de la guía usen la misma fuente (`DispatchGuideBalanceCalculator`), y que **no se toquen** `NationalizationBalance` ni `KardexAggregator`: el informe confirma que el nacionalizado disponible ya descuenta lo despachado en el legacy.

**Pruebas.**
- **Unitarias:** saldo con y sin apertura, y con varias guías.
- **Integración:** depósito migrado con recibido 648 y `salen` 200. Una guía de 50 debe imprimir saldo anterior **448** y nuevo **398**; una segunda guía debe partir de 398. Un depósito sin salidas en el legacy, igual que hoy.

---

## DEF-MIG-003 (CRITICAL): el importador de levantes descarta las filas repetidas del mismo levante

**Causa (confirmada).** `ReleasesImporter` (≈ líneas 95-103) marca como «repetido» (`Skipped`) una fila cuyo (número, aceptación, producto) ya existe en `deposit.Releases`, incluidos los levantes que creó **en el mismo archivo**. El legacy reparte un levante en varias filas, una por camión: se perdían 45 filas y 10.489 unidades.

**Decisión (cerrada).**
- **Opción B de la ficha:** el importador **agrupa las filas del archivo** por (depósito, producto, embalaje, número de levante, número de aceptación) **antes de crear**.
  - Suma la cantidad, el peso bruto, el FOB en dólares y el FOB en pesos.
  - Conserva la fecha de levante y de aceptación y la tasa de cambio de la primera fila. Si difieren entre filas del mismo grupo, conserva la primera y cuenta una advertencia en el lote.
  - El reparto del FOB (`LegacyReleaseFobSplitter`) se aplica **después** de agrupar.
- La regla «omitido» queda **solo** para los levantes que ya existían en la base antes de este archivo. Es su propósito de idempotencia: una segunda carga del mismo archivo sigue sin duplicar.
- La validación «levantado no supera lo recibido» se hace con la cantidad agrupada.
- El conteo del lote informa filas leídas, levantes creados (agrupados) y omitidos.

**Pruebas.**
- Unitarias de la agrupación: dos filas del mismo levante y producto → un levante con la suma; filas de levantes distintos → separados.
- Integración:
  - el CSV sin agrupar crea los levantes completos;
  - la segunda carga los omite;
  - el nacionalizado del producto es igual a la suma de las filas.

---

## DEF-MIG-002 (CRITICAL): la consulta de levantes del plan filtra por número de depósito

**Causa.** `nro_deposito` se reinicia cada año en el legacy. La consulta de F6-03 (≈ 2945-2953) trae levantes de depósitos cerrados con el mismo número.

**Cambio (solo documentación).**
- Corrige la consulta de levantes en `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` para filtrar por **`id_deposito`** de los depósitos vivos, con la misma subconsulta o condición que usa la consulta de depósitos.
- **No agrupes en la consulta:** desde DEF-MIG-003 agrupa el importador. Así el plan exporta las filas tal como están en el legacy.
- Agrega una nota sobre por qué no se filtra por número.
- Toma como base `12_levantes.sql` de la Fase 1, sin su agrupación.

---

## DEF-MIG-001 (MAJOR): la consulta de depósitos exporta el nombre de la modalidad

**Decisión (cerrada): se corrigen las dos cosas.**
1. **El parser acepta el nombre del legacy.** `LegacyDepositRowParser.ResolveModality` reconoce, sin distinguir mayúsculas ni tildes, «Entrada por Importación» → `IMP` y «Entrada por Exportación» → `EXP`, además de los códigos de la v2. Revisa en el dump, con `bodegas-legacy/bodegas_schema.sql` y la tabla `modalidad`, si hay un nombre para inspección y agrégalo si existe. El mensaje de error para un valor desconocido no cambia.
2. **El plan exporta el código.** La consulta de depósitos (≈ 2920-2938) usa un `CASE` por `id_modalidad`, como la congelada `11_depositos.sql`.

**Pruebas.** Unitarias del parser con los nombres, los códigos y un valor desconocido.

---

## DEF-MIG-004 (MAJOR): los depósitos migrados no tienen CIF ni moneda

**Causa.** El CSV de depósitos no trae el valor de la mercancía ni la moneda, y `WarehouseStorage.CreateMigrated` no los recibe. El almacenamiento por porcentaje del CIF (T1: 0,295 % con mínimo de $50.000) cae siempre al mínimo.

**Decisión (cerrada).**
1. **CSV.** Se agregan **dos columnas opcionales al final**, después de `trm_ingreso`: `valor_mercancia` y `moneda`.
   - Un CSV con las 19 columnas de hoy sigue aceptándose, sin CIF, como ahora.
   - Si `valor_mercancia` viene y `moneda` no, o la moneda no se reconoce, la fila del depósito se rechaza con un mensaje que nombre el campo.
   - Si los dos vienen vacíos, el depósito queda sin CIF, como hoy.
   - El valor es **por depósito**: en un depósito de varias filas (una por producto), las filas deben traer el mismo valor y la misma moneda. Si no, la fila se rechaza.
2. **Moneda.** Se acepta el código ISO (`USD`, `COP`, `EUR`…) o el código de país del legacy (`id_paismonedaprecio`). Revisa en el dump la tabla de países y los valores reales de `ingreso.id_paismonedaprecio` en los depósitos vivos, y mapea solo los que aparezcan. Según la ficha, `ECU` = USD; `COL` = COP. Documenta el mapeo.
3. **Dominio.** `CreateMigrated` recibe `cargoValue` y `currency`. Valida igual que el registro normal: valor mayor que 0 y moneda válida. Se mantiene la TRM manual de hoy.
   - **Moneda distinta de COP sin TRM:** el depósito queda en «TRM pendiente», con la regla que ya existe. Debe registrarse la TRM manual antes de numerar la factura.
   - **COP:** no requiere TRM.
4. **Consulta del plan.** Agrega `I.preciomercancia` y la moneda a la consulta de depósitos.
5. **Advertencia del mínimo.** Cuando la causa del mínimo es el CIF faltante, el texto de la factura dice eso, por ejemplo: «El depósito no tiene valor de la mercancía (CIF); se facturó el valor mínimo…». No debe decir «No existe un precio configurado ni acuerdo vigente». Los demás motivos del mínimo no cambian.
6. **Fuera de alcance:** completar el CIF de depósitos **ya migrados**. Las bases de prueba se recrean y la Fase 1 se repite desde cero.

**Pruebas.**
- Unitarias del parser:
  - 21 columnas;
  - 19 columnas;
  - valor sin moneda;
  - moneda desconocida;
  - valores distintos entre filas del mismo depósito.
- Integración:
  - un depósito migrado en USD con TRM → `open-billing` liquida **0,295 % × CIF en COP + IVA**, con el mínimo como piso;
  - uno en COP sin TRM → liquida;
  - uno en USD sin TRM → queda TRM pendiente;
  - uno sin CIF → mínimo con la advertencia nueva.

---

## DEF-MIG-006 (MINOR): el importador se ve «Sin asignar» cuando es el mismo cliente

**Causa.** `DepositDetailDocumentStakeholdersSection.vue` (≈ línea 61) filtra con `!s.isCustomer` y descarta al importador que también es el cliente.

**Cambio.**
- El bloque IMPORTADOR muestra al tercero con rol `IMPORTER` aunque sea el cliente. Es el caso normal del legacy: `id_cliente = id_importador`.
- El filtro `!isCustomer` se conserva solo donde su propósito sea no repetir al cliente en otra lista. Revisa por qué existe y anótalo.
- Esto afecta también a los depósitos nuevos de v2 cuyo importador sea el cliente: verifica que la regla «Obligatorio para confirmar» deje de pedir el importador en ese caso.

**Prueba.** Vitest del componente: importador que es el cliente → se muestra; importador distinto → igual que hoy.

---

## Sin retrocesos (regla 4.0.10 del plan de corrección del QA)
- **Depósitos no migrados:** la guía, el kárdex y la facturación no cambian.
- **Formato del CSV:** el importador de depósitos sigue aceptando el CSV de 19 columnas, y el de levantes el de hoy.
- **Idempotencia:** se conserva en las dos entidades.
- **Conciliación:** `DepositReconciler` sigue dando «Ok» con los CSV corregidos. Si el formato nuevo lo obliga a cambiar, cámbialo y pruébalo.
- **Pruebas existentes:** pasan sin editarlas, incluidas las de `LegacyImport`, la guía (CHG-33, CHG-35), F6-04 y DEF-F11-017. Si alguna supone el comportamiento viejo, **detente y repórtala**.

## Restricciones (obligatorias)
- Trabaja en `develop` de los dos repos. **No crees ramas, no hagas `git add`, commit, push ni merge**: entregas los mensajes de commit y el usuario hace los commits.
- **No uses la base `wms_migracion`, `wmsdb`, `legacy-mariadb`, staging ni producción** para escribir. Las pruebas de integración usan Testcontainers (Docker activo). Solo puedes leer `legacy-mariadb` para revisar modalidades y monedas reales, sin copiar datos personales a ningún archivo versionado.
- **Migraciones:** si `CreateMigrated` o algún campo nuevo cambian el modelo, genera la migración solo con `dotnet ef` y nunca edites los archivos generados. Se espera que **no** haga falta: `Currency` y `CargoValue` ya existen.
- No copies secretos ni datos reales a git. Textos y comentarios en español. Respeta la estructura por features.
- Nada fuera de las seis fichas. Si el código real contradice este prompt, adapta a lo que hay sin cambiar el comportamiento pedido y anótalo. Si el comportamiento cambia, detente y repórtalo.

## Fichas
- En `docs/planes/migracion-staging/resultados/defectos/DEF-MIG-001.md` a `006.md`:
  - **Estado** «Corregido»;
  - fila «Corregido» en el Historial con la fecha, el resumen, las pruebas y «commits: pendiente».
- Al final de cada ficha, deja la **lista de verificación para la repetición de la Fase 1**: qué debe ver el ejecutor para darla por verificada.

## Verificación antes de terminar
1. `dotnet build` sin errores ni advertencias nuevas.
2. `dotnet test` de `Wms.Tests` y `Wms.IntegrationTests` en verde (1644 y 280 antes de esta corrección). Reporta los totales.
3. `dotnet ef migrations has-pending-model-changes` sin cambios, o la migración generada y aplicada en Testcontainers.
4. En `Frontend/wms`:
   - `yarn test` en verde;
   - `yarn build` con código 0;
   - `yarn lint` con no más de 279 errores.
5. `git status` en los dos repos: solo los archivos de este alcance, más el plan de paridad, este prompt y las fichas.

## Entrega
Responde con:
1. Los archivos creados o modificados, por ficha.
2. El mapeo de monedas que encontraste en el dump (solo códigos y conteos, sin datos de terceros).
3. Las consultas corregidas del plan. Indica las líneas del plan de paridad que cambiaron.
4. El resultado de cada compuerta, con números.
5. Las desviaciones y cualquier prueba existente que hayas tenido que reportar.
6. **Los mensajes de commit**, listos para pegar, cada uno por separado:
   - **Backend:** `fix(migracion): saldo de la guía con las salidas del legacy, levantes agrupados, modalidad por nombre, CIF y moneda de los migrados (DEF-MIG-001 a 005)`, con una línea por cambio.
   - **Backend (documentación):** `docs(migracion): consultas de exportación corregidas y fichas DEF-MIG-001 a 006`. Incluye `plan-backend-paridad-legacy.md`, las fichas y este prompt.
   - **Frontend:** `fix(migracion): el importador se muestra aunque sea el cliente (DEF-MIG-006)`.
   - Todos terminan con la línea de coautoría que corresponde a tu modelo.

**Detente ahí.** La repetición de la Fase 1 la hace otro agente después de que el usuario haga los commits.
