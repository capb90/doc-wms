# Informe de la repetición de la fase 1: migración con las consultas corregidas y verificación de DEF-MIG-001 a 006

> **Fecha:** 2026-10-06. **Ejecutor:** agente (Opus 5.5).
> **Build:**
> - BE `9c5c81b`: corrección de DEF-MIG-001 a 005, sobre `f6f1828`.
> - FE `4799cc4`: corrección de DEF-MIG-006, sobre `eb55483`.
>
> **Plan:** `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` §4. **Primera ejecución:** `informe-fase-1.md` (No OK).
> **Fuente:** `legacy-mariadb` (MariaDB 10.11, puerto 3308, base `bodegas`). Es el mismo `backupBodegas.sql` del 2024-06-10, cargado en la primera ejecución; no se recargó.
> **Destino:** `wms_migracion` en `wms-postgres-db`, borrada y recreada con `dotnet ef`. `wmsdb`, `mysql57`, staging y producción no se tocaron.
> **Datos personales:** el informe lleva conteos, números de depósito y códigos. Las evidencias con datos reales están fuera de git, en `db_legacy/trabajo/evidencias/v2/`.

## Veredicto

**OK para pasar a la Fase 2.**

- **Criterios:** los ocho del §4 se cumplen (tabla en §12).
- **Defectos corregidos:** DEF-MIG-001 a 006 quedan **verificados**, con las consultas del plan **tal como están** y sin paliativos.
- **Defecto nuevo:**
  - **DEF-MIG-007 (MAJOR):** la guía de salida de los migrados imprime el manifiesto DIAN en blanco.
  - Ningún criterio OK lo cubre y no afecta saldos, stock ni facturación.
  - **No bloquea el despliegue (fase 2).** Conviene corregirlo antes de la fase 4: los operarios y QA verán guías de migrados sin manifiesto.

---

## 1. Tiempos (OK-8)

| Paso | Tiempo | Nota |
|---|---|---|
| Detener el API viejo y comprobar el destino del `drop` | — | Dos comprobaciones: la variable `ConnectionStrings__DefaultConnection` y `dotnet ef database drop --dry-run` decían `wms_migracion` en `localhost:5433`. |
| `dotnet ef database drop` | 2 s | `DROP DATABASE wms_migracion WITH (FORCE)`; `wmsdb` sigue en el servidor. |
| `dotnet ef database update` | 2 s | 10 migraciones. |
| Arranque del API (puerto 5291) | < 1 min (no se cronometró) | Con `.env.migracion.local`, sin tocar `appsettings`. |
| Exportación de los 12 CSV | **16,8 s** | Depósitos 14,3 s; el resto, ≤ 0,9 s cada uno. |
| Simulación de las 12 entidades (primera pasada) | 2,4 s | |
| Carga en firme de las 12 entidades | **2,6 s** | Cada una precedida de su simulación con los maestros ya cargados. |
| Idempotencia (5 entidades) | 0,3 s | |
| Conciliación | 0,12 s | |
| Tarifas T1 a T4 por el API (5 peticiones) | 0,2 s | |
| `open-billing` (128 depósitos) | **1,45 s** | |
| Salida completa por el API, del levante o la OC a la salida de Vigilancia | 0,2 a 2,2 s de respuesta del API por camión (10 a 15 llamadas) | 4 camiones. |

La parte mecánica del corte (exportación, simulación, firme, conciliación, tarifas y apertura) **no llega a 30 s** sin contar la carga del dump (3 min 24 s en la primera ejecución). Igual que antes, el tiempo lo ponen la revisión humana de la simulación y la aprobación.

## 2. Base limpia

- **Migraciones:** 10 en `__EFMigrationsHistory`, de `20261001193201_InitialParityLegacy` a `20261006034830_AddEntryLogServiceDiscardedAt`.
- **Roles:** los 6 sembrados (Administrador, Comercio exterior, Facturación y los tres operarios).
- **Admin:** login con 200, con el usuario de `Bootstrap__*`.
- **Cuentas por rol:** `mig.vigilancia`, `mig.bascula`, `mig.bodega`, `mig.comext` y `mig.facturacion` se recrearon por el API (`POST user`) con las contraseñas de `db_legacy/trabajo/credenciales-migracion-local.local.md`. Después se cambió la contraseña por `auth/change-password`, para quitar el cambio obligatorio del frontend.
- **Correo:** el API usa Mailpit (`127.0.0.1:1025`).

## 3. CSV v2 y conteos

- **Origen de las consultas:** se extrajeron **sin editar** del plan de paridad (`consultas/v2/extraer_del_plan.py` → `consultas/v2/*.sql`). El registro completo está en `registro-csv-fase-1.md`, «Conjunto v2».
- **Maestros:** los 10 CSV son **idénticos byte a byte** a los del v1.
- **Depósitos:**
  - 133 filas de 128 depósitos, con **21 columnas**;
  - las 19 primeras coinciden celda por celda con el v1;
  - `modalidad = IMP` en las 133;
  - `valor_mercancia` con valor y `moneda = ECU` en las 133;
  - `trm_ingreso` en las 133.
- **Levantes:** **170 filas** sin agrupar, todas de depósitos vivos. Son las mismas filas de la prueba sin agrupar de la primera ejecución.
- **D2:** los 128 depósitos tenían otra fecha de último fin facturado: 104 entre el 2022-12-10 y el 2024-11-30, y 24 sin período. Todos quedan en 2026-09-30, y `billing_start_date` = 2026-10-01 en los 128.

| # | Entidad | Filas | Creados | Asociados a un equivalente | Rechazados | Primera ejecución (creados / asociados / rechazados) |
|---|---|---|---|---|---|---|
| 1 | Ciudades | 1.781 | 1.774 | 0 | 7 | 1.774 / 0 / 7 |
| 2 | Embalajes | 67 | 61 | 6 | 0 | 61 / 6 / 0 |
| 3 | Cuadrillas | 7 | 7 | 0 | 0 | 7 / 0 / 0 |
| 4 | Ubicaciones | 6 | 6 | 0 | 0 | 6 / 0 / 0 |
| 5 | Clientes | 1.056 | 1.053 | 3 | 0 | 1.053 / 3 / 0 |
| 6 | Agencias | 78 | 74 | 4 | 0 | 74 / 4 / 0 |
| 7 | Transportadoras | 273 | 262 | 9 | 2 | 262 / 9 / 2 |
| 8 | Vehículos | 10.594 | 10.393 | 90 | 111 | 10.393 / 90 / 111 |
| 9 | Conductores | 4.416 | 4.361 | 47 | 8 | 4.361 / 47 / 8 |
| 10 | Productos | 1.778 | 1.638 | 139 | 1 | 1.638 / 139 / 1 |
| 11 | Depósitos (filas de producto) | 133 | 133 (128 depósitos) | 0 | 0 | 133 / 0 / 0, con la consulta ajustada |
| 12 | Levantes | **170** | **107** | 0 (omitidos: 0) | 18 filas (11 grupos) | 118 filas agrupadas: 107 / 0 / 11 |

**En la v2 tras la carga:**
- 1.389 terceros, con 2.449 roles y 1.053 configuraciones de facturación;
- 10.393 vehículos y 4.361 conductores;
- 1.643 productos, 61 embalajes, 7 cuadrillas y 26 ubicaciones (20 sembradas);
- 1.774 ciudades;
- 128 depósitos, 133 productos, 128 servicios, 202 movimientos de apertura y 107 levantes;
- 18.281 correspondencias.

Son los mismos números de la primera ejecución.

## 4. Errores por fila, comparados con la primera ejecución

### 4.1 Primera simulación, sin maestros (FA-MIG-002, nota conocida)
Igual que en la primera ejecución:
- vehículos: 8.863 «no existe la transportadora legacy N»;
- productos: 1.778 «no existe el embalaje legacy N»;
- depósitos: 133 «no existe el cliente legacy N»;
- levantes: 170 «el depósito BAN no está migrado».

Las simulaciones previas al firme, con los maestros ya cargados, dieron los mismos conteos que el firme.

### 4.2 Carga en firme

| Entidad | Filas | Causa | Clase | Primera ejecución |
|---|---|---|---|---|
| Ciudades | 6 | Nombre repetido en el mismo departamento con otro id | Duplicado legítimo | 6 |
| Ciudades | 1 | Id 0 («N.A»), sin nombre | Dato inválido del legacy | 1 |
| Transportadoras | 2 | Tipo de documento «C.I.» y «Licencia de Conducción» | Dato inválido del legacy | 2 |
| Vehículos | 62 | Su transportadora es una de esas 2, no importadas | Exclusión por regla (en cascada) | 62 |
| Vehículos | 49 | Placa inválida («N.A.», «SIN PLACA.», punto final…) | Dato inválido del legacy | 49 |
| Conductores | 8 | «Cédula de Extrangería» (sic) | Dato inválido del legacy | 8 |
| Productos | 1 | Embalaje 69 eliminado en el legacy | Exclusión por regla (en cascada) | 1 |
| Levantes | 18 filas = 11 grupos | «el producto legacy N con embalaje N no está en el depósito BAN»: levantes de productos agotados en el legacy, que la consulta de depósitos no exporta (`HAVING ingresan − salen > 0`) | Exclusión por regla | 11 filas (CSV agrupado) |
| **Defecto de la herramienta** | **0** | Con las consultas del plan **sin cambios** | — | 0, pero solo con paliativos. Con las consultas del plan habría habido 133 + 2 + 45 (DEF-MIG-001 a 003). |

## 5. Verificación de DEF-MIG-001 a 003 e idempotencia (OK-1, OK-3)

### 5.1 DEF-MIG-001: modalidad
- La consulta del plan exporta `IMP` en las 133 filas. Simulación y firme: 133 creados, **0 rechazos por modalidad**.
- **Prueba opcional:** el mismo CSV con «Entrada por Importación» en la columna y números `SIM…`, en simulación → 133 creados, 0 errores (`carga/def1-Deposits-nombre-legacy-sim.json`). No persistió nada: siguen 128 depósitos.

### 5.2 DEF-MIG-002: levantes por id de depósito
- La consulta trae **170 filas** (no 819), todas de depósitos del CSV de depósitos.
- **Firme:** 107 levantes (no 109).
- Ningún error por número de depósito repetido. Los 18 errores son de los 11 grupos agotados (§4.2).

### 5.3 DEF-MIG-003: agrupación en el importador
- **Firme:** `totalRows` 170, `created` 107, **`skipped` 0**, `errorRows` 18, sin advertencias de «fechas, tasa, peso o FOB distintos».
- **Agrupación:** 16 grupos de varias filas (68 filas) se sumaron. El ejemplo de la ficha (176,16 + 440 en el mismo levante) es BA1018, y su nacionalizado cuadra con el legacy.
- **Nacionalizado de la v2 = `nacionalizados` del CSV** en **133 de 133** productos, con el recibido y el saldo también iguales. Antes del arreglo había 14 productos por debajo.
- **FOB y peso bruto** por par número–aceptación iguales al legacy en **107 de 107**: no se multiplican por camión.

### 5.4 Idempotencia (OK-3, FA-MIG-004)

| Entidad | Segunda carga en firme | Primera ejecución |
|---|---|---|
| Ciudades | 1.774 «actualizadas» por `LegacyId`, 7 errores | Igual |
| Clientes | 1.056 omitidos | Igual |
| Vehículos | 10.483 omitidos, 111 errores | Igual |
| Depósitos | 133 «el depósito BA… ya fue migrado» | Igual |
| Levantes | `created` 0, **`skipped` 107**, los mismos 18 errores | 107 omitidos (CSV agrupado) |

Los 16 conteos de la v2, de terceros a `legacy_id_map`, quedaron **idénticos** antes y después (`carga/conteos-v2-antes-idem.txt` y `conteos-v2-despues-idem.txt`).

## 6. Conciliación (OK-2, FA-MIG-007)

- **Tras la carga, con el CSV de 21 columnas:** **133 Ok, 0 Difference, 0 NotMigrated**, 0 errores. No escribe: los 18 conteos y `audit_logs` quedaron iguales antes y después.
- **Después de las operaciones de §7 y §9:** 131 Ok y 2 Difference, ambas **explicadas**. Son BA0558 y la fila de 2.223 de BA1196: en las dos se registró **un levante nuevo en la v2** (`MIG-R1-…`). El reconciliador exige que lo nacionalizado sea igual al legacy («Lo nacionalizado debe ser igual», `DepositReconciler.cs:43`) y no descuenta los levantes nuevos, como sí hace con los movimientos de stock. El stock de las dos sí cuadra con `v2MovementsSinceMigration`. BA0042 sigue Ok (448 − 80 = 368).
- **Corrección a la primera ejecución:** su informe (§7) dice que la conciliación repetida «después de la operación nueva» seguía en 133 Ok. Según las horas de las evidencias, esa conciliación (`conciliacion-2.json`, 15:15) se corrió **antes** del levante de E19 (15:17), así que no lo cubría.
- **Observación O-2:** la conciliación sirve para el día del corte, antes de operar. Si se usa después, un levante nuevo aparece como `Difference`. Sugerencia para el plan: decirlo en F6-04, o que el reconciliador informe los levantes de la v2 como informa los movimientos.

## 7. Facturación con CIF (OK-5, FA-MIG-008, DEF-MIG-004)

**Tarifas**, cargadas por el API con el Admin, igual que en la primera ejecución (mapeo aprobado, sin nueva aprobación):

| # | Petición | Resultado |
|---|---|---|
| T1 | `POST service/{ALMACENAMIENTO}/pricing-rules`: `PERCENTAGE_OF_VALUE`, `IMP001`, `percentage 0.295`, `minimum 50000`, `minimumIncludesVat true` | 200 |
| T2 | `PUT service/{ALMACENAMIENTO}/minimum-values/{IMP}`: 50.000 con IVA, activo | 200 |
| T3 | `POST service/{BASCULA}/assign-tax` (IVA) y `POST …/prices`: 16.806,72 desde el 2026-10-01 | 200 y 200 |
| T4 | `POST service/{GUIA_SALIDA}/prices`: 15.000 desde el 2026-10-01 | 200 |

**`open-billing`:** **128 Opened**, 0 Skipped y 0 Failed. En la primera ejecución fueron 127, porque BA0589 ya tenía período por la prueba «antes de las tarifas», que esta vez no se repitió.

**Períodos:**
- Todos empiezan el **2026-10-01**.
- 92 del ciclo de 15 días terminan el 16/10/2026, con límite el 19/10.
- 36 del ciclo de 180 días terminan el 30/03/2027, con límite el 02/04/2027.
- Los 128 con `formula_code = PERCENTAGE_OF_VALUE`: **ninguno en `MINIMUM_VALUE`**. En la primera ejecución, los 128 estaban en el mínimo.

**Importes:**

| | Facturas | Total con IVA |
|---|---|---|
| Ciclo de 15 días | 92 | $63.258.314,46 |
| Ciclo de 180 días | 36 | $27.999.160,93 |
| **Total del primer período** | **128** | **$91.257.475,39** ($76.686.954,14 + $14.570.521,25 de IVA) |

- **124 sobre el mínimo y 4 en el piso** de $50.000 ($42.016,81 + $7.983,19).
- **Por qué hay 4 en el piso:** BA0558, BA0860, BA1283 y BA1448 tienen un CIF bajo (USD 1.350 a 3.000), y su 0,295 % + IVA da entre $18.146 y $39.760.
- **Rango:** de $50.000 a $3.483.997,59 (BA2355).
- **Ciclo de 180 días:** queda en ≈ 0,35 % del CIF con IVA por período, del orden de lo que facturaba el legacy (≈ $560.000 a $630.000; ver el mapeo de tarifas §1.1).
- **El total del primer período, $91.257.475,39, es la referencia que la fase 3 debe reproducir en staging.**

**Cotejo independiente:** se recalcularon los 128 con CIF × TRM × 0,295 % + IVA del 19 % y piso de $50.000, redondeando a centavos. **Coinciden 128 de 128.** Diez de ellos:

| Depósito | v2 | CIF | TRM de ingreso | CIF en COP | 0,295 % (subtotal) | IVA | Total | Ciclo |
|---|---|---|---|---|---|---|---|---|
| BA0008 | 2024BA00001 | USD 41.600,00 | 3.822,05 | 158.997.280,00 | 469.041,98 | 89.117,98 | 558.159,96 | 15 días |
| BA0042 | 2024BA00002 | USD 34.248,00 | 3.927,64 | 134.513.814,72 | 396.815,75 | 75.394,99 | 472.210,74 | 15 días |
| BA0118 | 2024BA00006 | USD 44.550,00 | 3.929,79 | 175.072.144,50 | 516.462,83 | 98.127,94 | 614.590,77 | 180 días |
| BA1046 | 2023BA00001 | USD 56.204,00 | 4.424,02 | 248.647.620,08 | 733.510,48 | 139.366,99 | 872.877,47 | 15 días |
| BA1196 | 2024BA00058 | USD 62.701,00 | 3.900,38 | 244.557.726,38 | 721.445,29 | 137.074,61 | 858.519,90 | 15 días |
| BA4575 | 2022BA00002 | USD 34.425,00 | 4.797,02 | 165.137.413,50 | 487.155,37 | 92.559,52 | 579.714,89 | 15 días |
| BA0558 | 2024BA00016 | USD 2.700,00 | 3.931,31 | 10.614.537,00 | 31.312,88 → **piso** 42.016,81 | 7.983,19 | **50.000,00** | 15 días |
| BA0860 | 2024BA00030 | USD 3.000,00 | 3.775,37 | 11.326.110,00 | 33.412,02 → **piso** 42.016,81 | 7.983,19 | **50.000,00** | 15 días |
| BA1283 | 2024BA00065 | USD 1.350,00 | 3.828,98 | 5.169.123,00 | 15.248,91 → **piso** 42.016,81 | 7.983,19 | **50.000,00** | 15 días |
| BA1448 | 2024BA00102 | USD 2.879,00 | 3.874,32 | 11.154.167,28 | 32.904,79 → **piso** 42.016,81 | 7.983,19 | **50.000,00** | 15 días |

**Otras comprobaciones:**
- **Moneda y TRM:** los 128 migrados quedan en **USD** (de `ECU`), con el CIF y la TRM del CSV (`trm_source = Manual`, que viene del CSV).
- **TRM pendiente con moneda extranjera:** **0**. Ninguna factura dice «TRM PENDIENTE».
- **Advertencia por CIF faltante:** no aplica, porque los 128 traen CIF. **0** facturas dicen «No existe un precio configurado…», el texto que la primera ejecución tenía en los 128. El texto nuevo, «El depósito no tiene valor de la mercancía (CIF)…», está cubierto por `StorageMissingCargoValueWarningTests` y `MigratedStorageBillingTests` y no se pudo observar con este dump.
- **En la pantalla:** el detalle de `2024BA00002` muestra «Moneda USD · Valor Comercial US$ 34.248,00». En la primera ejecución salía «—».
- **Correo (D4):** **0 mensajes** en Mailpit en toda la repetición. **0** contactos de terceros (`stakeholder_contacts_info` vacía). Las 8 notificaciones de la app fueron para el Admin (4 «Cargue completado») y `mig.comext` (4 «Guía de salida requerida»). El log registra «No se han configurado emails de administradores…», como antes.

## 8. Verificación de DEF-MIG-005 (saldos de la guía) y E19

Cuatro salidas completas por el API, una cuenta por rol: OC → ingreso (Vigilancia) → inicio de salida, cobro y tara (Báscula) → cargue (Bodega) → guía (Comercio Exterior) → repesaje (Báscula) → salida (Vigilancia). Los saldos se leyeron con SQL de solo lectura. Evidencias en `evidencias/v2/e19/<caso>/`.

| Caso | Depósito | Antes (recibido / stock / reservado / disponible / nacionalizado) | Guía | Línea de la guía y PDF (recibido / saldo anterior / sale / nuevo saldo) | Kárdex | Resultado |
|---|---|---|---|---|---|---|
| BA0042, primera guía | BA0042 → `2024BA00002` (salen 200 en el legacy) | 648 / 448 / 0 / 448 / 648 | `2026S00001`, 50 u | **648 / 448 / 50 / 398** (antes 648 / 648 / 50 / 598) | 648 → 448 (apertura) → 398 | **PASA** |
| BA0042, segunda guía | ídem | 648 / 398 / 0 / 398 / 648 | `2026S00002`, 30 u | **648 / 398 / 30 / 368** | 398 → 368 | **PASA** |
| Otro migrado con salidas | BA1196 → `2024BA00058`, producto de 2.223 (salen 1.000, nacionalizado 1.000) | 2.223 / 1.223 / 0 / 1.223 / 1.000 | `2026S00003`, 150 u | **2.223 / 1.223 / 150 / 1.073** | 2.223 → 1.223 → 1.073 | **PASA** |
| Migrado sin salidas | BA0558 → `2024BA00016` | 300 / 300 / 0 / 300 / 0 | `2026S00004`, 100 u | **300 / 300 / 100 / 200**, igual que en la primera ejecución | 300 → 200 | **PASA** |

**Más comprobaciones de E19:**
- La reimpresión (`GET dispatch-guides/{id}/pdf`) da **el mismo PDF byte a byte** en las 4 guías.
- La OC reserva y el cargue descuenta y libera la reserva, en los 4 casos.
- Ciclos `Complete`, órdenes `Dispatched` y las 4 salidas de Vigilancia registradas.
- **Cobros por salida:**
  - báscula $20.000 ($16.806,72 + IVA), factura `Paid`;
  - guía $15.000 sin IVA (T4), factura `Paid`.

**Hallazgo nuevo: DEF-MIG-007 (MAJOR).**
- La columna «Manifiesto» de la guía sale **vacía** en las 4 guías. El PDF toma el manifiesto de los camiones (`EntryLogs.Manifests`, `DispatchGuidePdfService.cs:491`), y los migrados no tienen camiones.
- El manifiesto sí está en el depósito: el detalle lo muestra y la muestra de 30 lo coteja bien.
- Ya pasaba en la primera ejecución, pero no se detectó.

**De la primera ejecución, sin cambios en el código que tocan** (no se repitieron):
- la anulación de un migrado (F3-08);
- la devolución a Borrador (409);
- la OC por encima de lo nacionalizado (400).

## 9. Operación nueva completa sobre un migrado con salidas en el legacy (OK-7)

Sobre **BA1196 → `2024BA00058`**, producto de 2.223 u. En el legacy: nacionalizado 1.000 y salen 1.000.

1. **Levante** `MIG-R1-BA1196-op` de 200 u, con FOB USD 5.000 y tasa manual (Comercio Exterior) → nacionalizado 1.000 → **1.200**; el stock no cambia (1.223).
2. **OC `2026OC00003`** por 150 u (Comercio Exterior) → reservado 150, disponible 1.073. El tope «nacionalizado − despachado − reservado» = 1.200 − 1.000 − 0 = 200 la permite.
3. **Ingreso** (Vigilancia) de un vehículo migrado con un conductor migrado.
4. **Báscula:** inicio de salida con la OC, cobro inmediato de $20.000 y tara de 15.000 kg.
5. **Cargue** (Bodega) de 150 u, con firma y precinto → stock 1.223 → **1.073**; reserva liberada.
6. **Guía `2026S00003`** (Comercio Exterior) → 2.223 / **1.223** / 150 / **1.073**; cobro de $15.000.
7. **Repesaje** (bruto 18.750 kg) → ciclo `Complete`, OC `Dispatched`. **Salida** (Vigilancia).
8. **Facturación** (`mig.facturacion`):
   - N.º SIIGO de prueba en la factura de la guía (`Paid`).
   - La factura de almacenamiento de BA1196 ($858.519,90, período 01/10–16/10/2026) se numeró y se **aprobó** (`Approved`).
   - El período conserva lo facturado tras el despacho: se cobra por adelantado.

**Resultado: PASA.** Saldos correctos de punta a punta en un migrado con salidas en el legacy, que era el caso que fallaba en la primera ejecución. La conciliación posterior marca esa fila como `Difference` por el levante nuevo (§6, explicado). La guía sale sin manifiesto (DEF-MIG-007).

## 10. Recorrido por rol en la pantalla (FA-MIG-009) y DEF-MIG-006

Frontend local (`http://localhost:3001`, Nuxt dev con el FE `4799cc4`) contra el API de `wms_migracion`, una cuenta por rol:

| Rol | Pantalla | Resultado |
|---|---|---|
| **Comercio Exterior** | Dashboard | 57 sin nacionalizar + 71 nacionalizados = 128 vivos; «67 en abandono», esperable con ingresos de 2022 a 2024. |
| | Detalle de `2024BA00002` | Manifiesto DIAN y fecha; carta porte; **Moneda USD, Valor Comercial US$ 34.248,00**; fecha de ingreso 10/01/2024; «Ingreso de camiones cerrado», «Camiones ingresados: 0»; levante con FOB y tasa; stock 368. **Terceros documentales: el bloque IMPORTADOR muestra el tercero** (razón social y NIT, el mismo del cliente) y no «Sin asignar». La agencia de aduanas aparece igual que antes. → **DEF-MIG-006 verificado.** |
| **Bodega** | Inventario | `2024BA00002`: 368 / 0 / 368. |
| | Movimientos | Las 4 salidas con stock anterior y nuevo (448 → 398, 398 → 368, 1.223 → 1.073 y 300 → 200) y las aperturas «Ingreso legacy» y «Despachado en el legacy». |
| **Facturación** | Facturas | Pestañas Báscula 4, Montacargas 0, Guía de salida 4 y **Almacenamiento 128**, con importes por CIF (p. ej. $183.610,80, $818.984,57, $1.627.743,78) en Borrador. Dashboard: «Borradores 127» (128 menos la aprobada de BA1196). |
| **Báscula** | Pantalla única con cola | Vacía: los 4 camiones de prueba ya salieron. |
| **Vigilancia** | Ingreso | «Camiones en planta: 0». |

El log del API de la repetición no tiene ningún 500. Su único `fail:` es un «Refresh token inválido o expirado» (401) del navegador al cambiar de cuenta.

## 11. Muestra de 30 depósitos (OK-4)

- **Selección:** los **mismos 30 depósitos** de la primera ejecución, que suman 35 filas de producto.
- **Script:** `db_legacy/trabajo/consultas/v2/muestra30.py`, una adaptación de la de la primera ejecución.
- **Campos cotejados:** cliente, producto y embalaje, recibido, despachado, saldo, levantes, modalidad y manifiesto, más **CIF, moneda y TRM de ingreso**.
- **Cómo se cotejó:** solo lectura en los dos lados. En el legacy, sobre las tablas base; en la v2, el saldo legacy se reconstruye restando los movimientos de la v2 posteriores a la migración. Los levantes `MIG-*` de esta repetición se excluyen.
- **Resultado: 30 de 30 depósitos y 35 de 35 filas coinciden en todos los campos.**

| Depósito legacy | Depósito v2 | Productos | Recibido | Despachado legacy | Saldo legacy | Levantes | Nacionalizado | CIF (legacy = v2) | Moneda legacy → v2 | Resultado |
|---|---|---|---|---|---|---|---|---|---|---|
| BA0042 | 2024BA00002 | 1 | 648 | 200 | 448 | 1 | 648 | 34.248,00 | ECU → USD | Coincide |
| BA0090 | 2024BA00005 | 1 | 3.211 | 1.211 | 2.000 | 1 | 3.211 | 69.669,50 | ECU → USD | Coincide |
| BA0118 | 2024BA00006 | 1 | 1.350 | 0 | 1.350 | 0 | 0 | 44.550,00 | ECU → USD | Coincide |
| BA0154 | 2024BA00007 | 1 | 1.732 | 756 | 976 | 1 | 1.732 | 45.664,80 | ECU → USD | Coincide |
| BA0191 | 2024BA00008 | 1 | 1.327 | 406 | 921 | 1 | 1.327 | 23.620,60 | ECU → USD | Coincide |
| BA0233 | 2024BA00009 | 1 | 3.200 | 800 | 2.400 | 1 | 3.200 | 49.600,00 | ECU → USD | Coincide |
| BA0518 | 2024BA00015 | 2 | 2.300 | 0 | 2.300 | 0 | 0 | 56.800,00 | ECU → USD | Coincide |
| BA0558 | 2024BA00016 | 1 | 300 | 0 | 300 | 0 | 0 | 2.700,00 | ECU → USD | Coincide |
| BA0589 | 2024BA00017 | 1 | 2.000 | 0 | 2.000 | 0 | 0 | 49.000,00 | ECU → USD | Coincide |
| BA0739 | 2024BA00026 | 1 | 1.470 | 0 | 1.470 | 0 | 0 | 18.375,00 | ECU → USD | Coincide |
| BA0898 | 2024BA00031 | 1 | 2.700 | 0 | 2.700 | 0 | 0 | 45.900,00 | ECU → USD | Coincide |
| BA1046 | 2023BA00001 | 1 | 2.994 | 2.902 | 92 | 2 | 2.994 | 56.204,00 | ECU → USD | Coincide |
| BA1194 | 2024BA00056 | 1 | 1.350 | 0 | 1.350 | 0 | 0 | 35.100,00 | ECU → USD | Coincide |
| BA1196 | 2024BA00058 | 2 | 2.723 | 1.300 | 1.423 | 2 | 1.500 | 62.701,00 | ECU → USD | Coincide |
| BA1232 | 2024BA00062 | 2 | 517 | 492 | 25 | 2 | 517 | 5.300,00 | ECU → USD | Coincide |
| BA1311 | 2024BA00070 | 1 | 55 | 0 | 55 | 0 | 0 | 44.005,50 | ECU → USD | Coincide |
| BA1352 | 2024BA00079 | 2 | 3.278 | 0 | 3.278 | 0 | 0 | 74.355,00 | ECU → USD | Coincide |
| BA1353 | 2024BA00080 | 1 | 3.200 | 0 | 3.200 | 0 | 0 | 76.160,00 | ECU → USD | Coincide |
| BA1429 | 2024BA00094 | 1 | 2.040 | 0 | 2.040 | 0 | 0 | 85.680,00 | ECU → USD | Coincide |
| BA1436 | 2024BA00097 | 1 | 2.040 | 0 | 2.040 | 0 | 0 | 86.700,00 | ECU → USD | Coincide |
| BA1437 | 2024BA00098 | 1 | 5 | 2 | 3 | 1 | 2 | 11.998,51 | ECU → USD | Coincide |
| BA1442 | 2024BA00101 | 1 | 1.454 | 0 | 1.454 | 0 | 0 | 63.249,00 | ECU → USD | Coincide |
| BA1451 | 2024BA00103 | 1 | 70 | 30 | 40 | 1 | 30 | 41.563,73 | ECU → USD | Coincide |
| BA1590 | 2023BA00002 | 1 | 733 | 122 | 611 | 1 | 733 | 38.011,20 | ECU → USD | Coincide |
| BA1878 | 2023BA00003 | 1 | 1.083 | 968 | 115 | 1 | 1.083 | 29.807,00 | ECU → USD | Coincide |
| BA2576 | 2023BA00008 | 1 | 2.853 | 2.322 | 531 | 2 | 2.853 | 50.400,00 | ECU → USD | Coincide |
| BA2803 | 2023BA00011 | 1 | 3.200 | 0 | 3.200 | 0 | 0 | 83.200,00 | ECU → USD | Coincide |
| BA3029 | 2023BA00012 | 2 | 2.669 | 2.078 | 591 | 2 | 2.669 | 61.864,00 | ECU → USD | Coincide |
| BA3238 | 2023BA00013 | 1 | 1.350 | 820 | 530 | 1 | 1.350 | 45.600,00 | ECU → USD | Coincide |
| BA4575 | 2022BA00002 | 1 | 450 | 0 | 450 | 0 | 0 | 34.425,00 | ECU → USD | Coincide |

- Las columnas «Productos», «Recibido», «Despachado», «Saldo», «Levantes» y «Nacionalizado» suman los productos de cada depósito, como en la primera ejecución. El detalle por fila está en `evidencias/v2/muestra30/cotejo.json`.
- La TRM de ingreso de la v2 es igual a la `tasa_cambio` vigente en la fecha de ingreso del legacy en las 35 filas.
- **Numeración:** igual que en la primera ejecución (`2022BA…` a `2024BA…`).
- **FA-MIG-005 (codificación y separadores) y FA-MIG-006 (límites):** no se repitieron, porque no cambiaron; se citan con la evidencia de la primera ejecución (`informe-fase-1.md` §9, `evidencias/carga/fa005-*` y `fa006-*`).
- **Los CSV reales se leyeron sin mojibake,** como en la primera ejecución: los maestros son idénticos byte a byte a los del v1.

## 12. Criterios OK

| # | Criterio | Resultado | Motivo |
|---|---|---|---|
| OK-1 | 12 entidades en firme; cada rechazo con causa aceptada; 0 rechazos por defecto de la herramienta | **Cumple** | §3 y §4.2: 0 rechazos por defecto, ahora **con las consultas del plan sin cambios**. |
| OK-2 | Conciliación sin diferencias sin explicar | **Cumple** | 133/133 Ok tras la carga. Después de operar, 2 `Difference` explicadas por levantes nuevos de la v2 (§6). |
| OK-3 | Idempotencia | **Cumple** | §5.4: los levantes se omiten (`skipped` 107) y los conteos no cambian. |
| OK-4 | Muestra de 30: 100 % coincide | **Cumple** | 30/30, también en CIF, moneda y TRM (§11). |
| OK-5 | `open-billing`: Opened o Skipped con causa; inicio el 2026-10-01; importe coherente con la tarifa | **Cumple** | 128 Opened desde el 2026-10-01; T1 sobre el CIF en los 128 (124 sobre el mínimo, 4 en el piso), cotejo de 128/128 (§7). |
| OK-6 | FA-MIG-001 a 010 y E19 sin FALLA, salvo las notas conocidas de FA-MIG-002 y 010 | **Cumple** | FA-MIG-001, 003, 004, 007, 008 y 009: §4 a §10. FA-MIG-005 y 006: evidencia de la primera ejecución. FA-MIG-002 y 010: sin cambios respecto de sus notas conocidas. E19: saldos de la guía correctos en migrados con y sin salidas (§8); períodos con fecha límite (§7); recorrido por rol (§10). DEF-MIG-007 es un defecto del PDF, no de los saldos. |
| OK-7 | Operación nueva de punta a punta con saldos correctos | **Cumple** | §9, sobre un migrado con salidas en el legacy. |
| OK-8 | Tiempos anotados | **Cumple** | §1. |

### Defectos y observaciones

| Tipo | ID | Estado | Bloquea |
|---|---|---|---|
| Defecto | DEF-MIG-001 a 006 | **Verificados** (fila «Verificado» en cada ficha) | — |
| Defecto | **DEF-MIG-007** (MAJOR): manifiesto en blanco en la guía de los migrados | **Corregido y verificado** (2026-10-06, sin commit): las 4 guías reimpresas en `wms_migracion` imprimen el manifiesto del depósito; ver la ficha. | No bloquea la fase 2. **Conviene corregirlo antes de la fase 4/5.** Para re-verificarlo basta una guía sobre un migrado; no hace falta repetir la carga. |
| Observación | O-1 | El `ORDER BY` de la consulta de levantes no es total. Una reexportación trae las mismas filas en otro orden y cambia el hash; no cambia la carga (registro de CSV, «Conjunto v2»). **Corregida** (2026-10-06, sin commit): el plan ordena los levantes también por `PL.id_productolevante` y los depósitos por `X.id_deposito`; mismas 170 y 133 filas, orden estable entre ejecuciones. | No. La fase 3 carga el archivo congelado. |
| Observación | O-2 | La conciliación marca `Difference` cuando hay levantes nuevos en la v2 (§6). | No. Es una herramienta del día del corte. |
| Observación | O-3 | El inicio de salida de báscula responde `totalAmount = 19.999,9968` (16.806,72 × 1,19 sin redondear). La factura sale bien, en $20.000,00. **Corregida** (2026-10-06, sin commit): el IVA del total propuesto (ingreso, salida y solo báscula) se redondea a 2 decimales como la vista previa del cobro; propone $20.000,00. | No. Se informa por si el frontend muestra el valor sin redondear. |

## 13. Estado del ambiente que queda

| Recurso | Estado |
|---|---|
| `legacy-mariadb` (`localhost:3308`, base `bodegas`) | **Arriba**, sin cambios. Contraseña en `db_legacy/trabajo/.mariadb.local`. |
| `wms_migracion` en `wms-postgres-db` (5433) | **Arriba**, recreada. Tiene la carga v2, las tarifas T1 a T4, la facturación abierta (128 períodos) y las operaciones de la repetición: levantes `MIG-R1-*`, OC `2026OC00001` a `00004`, guías `2026S00001` a `00004`, factura de almacenamiento de BA1196 aprobada. |
| API local (`http://localhost:5291`) | Arriba, con el BE `9c5c81b` (PID en `evidencias/api.pid`; log en `evidencias/api.log`; el log de la primera ejecución está en `evidencias/v1/api-v1.log`). Se puede detener sin perder datos. |
| Frontend local (`http://localhost:3001`) | Arriba, Nuxt dev con el FE `4799cc4` (PID en `evidencias/front.pid`). Se puede detener. |
| `migracion-mailpit` (`127.0.0.1:1025`, UI en `:8025`) | **Arriba**, con 0 mensajes. |
| Cuentas `mig.*` (solo en `wms_migracion`) | Recreadas con las mismas contraseñas, en `db_legacy/trabajo/credenciales-migracion-local.local.md`. |
| CSV | **Conjunto v2 congelado** en `db_legacy/trabajo/csv/`, con `sha256-csv-fase-1-v2.txt`. El v1 está en `csv/v1/`. Consultas en `consultas/v2/`. |
| `wmsdb`, `mysql57`, staging y producción | Sin tocar. |
| Repositorios | Sin cambios de código ni de configuración. Solo `docs/planes/migracion-staging/` sin commit. |
