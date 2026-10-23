# Informe de la fase 1: migración del legacy en local y verificación con datos reales (E19)

> **Fecha:** 2026-10-06. **Ejecutor:** agente (Opus 5.5).
> **Build:** BE `f6f1828`. FE `eb55483`: solo agrega documentos sobre `24d742d`, así que el código es el mismo.
> **Plan:** `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` §4.
> **Fuente:** `db_legacy/backupBodegas.sql` (MariaDB 10.1.38, corte del 2024-06-10).
> **Destino:** base nueva `wms_migracion` en `wms-postgres-db`. `wmsdb`, `mysql57`, staging y producción no se tocaron.
> **Datos personales:** este informe lleva conteos, números de depósito y códigos. Los clientes se citan por su id del legacy. Las evidencias con datos reales están fuera de git, en `db_legacy/trabajo/`.

## Veredicto

**No OK para pasar a la fase 2.**

- La migración en sí cumple: carga, conciliación, idempotencia, muestra de 30 y apertura de la facturación.
- Pero E19 falla en el saldo que imprime la guía de salida de los depósitos migrados con salidas en el legacy (**DEF-MIG-005**, CRITICAL: 66 de 128 depósitos).
- Además, tres defectos de la herramienta (**DEF-MIG-001** a **003**) solo se esquivaron ajustando las consultas de exportación. Deben corregirse en el plan o en el importador antes del corte real.

Ver la tabla de criterios OK y la lista de correcciones al final.

---

## 1. Tiempos (OK-8)

| Paso | Tiempo | Nota |
|---|---|---|
| Contenedor `legacy-mariadb` (MariaDB 10.11, puerto 3308, volumen `legacy-mariadb-data`) | ≈ 20 s | Imagen descargada en el momento |
| Carga de `backupBodegas.sql` (4,4 GB) | **3 min 24 s** (14:47:55 → 14:51:19) | Las 81 tablas cargaron. Fallaron 2 vistas de Colmotores por el definidor `bodegas@localhost` inexistente; se completaron creando ese usuario **bloqueado y con solo SELECT** (15 de 15 vistas). |
| `dotnet ef database update` sobre `wms_migracion` | 5 s | 10 migraciones |
| Arranque del API (puerto 5291) | ≈ 15 s | Con variables de entorno, sin tocar `appsettings` |
| Exportación de los 12 CSV | **16,4 s** | Depósitos: 14,3 s; los demás, ≤ 0,8 s cada uno |
| Simulación de las 12 entidades | 2,9 s | Primera pasada; ver §4.1 |
| Carga en firme de las 12 entidades | **3,0 s** | Detalle por entidad en §3 |
| Conciliación | 0,16 s | |
| Tarifas por el API (5 peticiones) | < 1 min | Manual |
| `open-billing` (127 depósitos) | 1,33 s | |

Para la ventana del corte real, la parte mecánica (dump, exportación, simulación, firme, conciliación y apertura) toma **menos de 10 minutos**. El tiempo lo ponen la revisión humana de la simulación y la aprobación de las tarifas.

## 2. Preparación

- **Conteos del dump:** las **81 tablas** coinciden fila a fila con las tuplas de los `INSERT` del dump (`extractos/cotejo-conteos.txt`).
- **Tablas clave:**
  - `deposito` 9.682 (AI 27.288); `ingreso` 9.895; `cliente` 1.060 (AI 1.060); `producto` 1.778;
  - `producto_en_bodega` 19.109; `producto_levante` 20.523; `producto_salida` 26.208; `levante` 12.143;
  - `vehiculo` 10.594 (AI 10.595); `persona` 10.189; `pesaje` 47.741;
  - `facturaciigo` 15.777; `detallefactura` 94.669;
  - `tarifa` 1 (AI 2); `convenio` 3 (AI 3); `servicio` 3 (AI 4).
- **Codificación:** las columnas `latin1` del legacy guardan bytes UTF-8 (con utf8mb4 se lee «CÃ©dula»), salvo tablas con latin1 genuino (`pais`, parte de `ciudad`, `producto` y `empresa_transporte`). El exportador decodifica campo por campo; ver `registro-csv-fase-1.md`. Un producto (id 7) ya venía doblemente mal codificado en el legacy y se migra tal cual.
- **`nro_deposito` no es único en el legacy:** 9.682 depósitos con 4.755 números, porque la serie se reinicia. Entre los 128 vivos sí es único.
- **Base v2:** las **10 migraciones** están en `__EFMigrationsHistory` (de `InitialParityLegacy` a `AddEntryLogServiceDiscardedAt`). Los **6 roles** están sembrados. El **login del Admin** responde 200 con el usuario creado por `Bootstrap__*`.
- **Correo:** el API usa un SMTP local de captura (Mailpit, `127.0.0.1:1025`) para que ningún aviso salga a internet (D4, §8).

## 3. Conteos legacy frente a v2 (carga en firme)

| # | Entidad | Legacy (tabla) | Filas del CSV | Creados | Asociados a un equivalente | Rechazados | En la v2 tras la carga | Tiempo en firme |
|---|---|---|---|---|---|---|---|---|
| 1 | Ciudades | `ciudad` 1.781 | 1.781 | 1.774 | 0 | 7 | 1.774 | 0,21 s |
| 2 | Embalajes | `embalaje` 69 (67 vivos) | 67 | 61 | 6 | 0 | 61 | 0,05 s |
| 3 | Cuadrillas | `cuadrilla` 7 | 7 | 7 | 0 | 0 | 7 | 0,03 s |
| 4 | Ubicaciones | `seccion` 4.032 (6 en bodegas activas que no son de Colmotores) | 6 | 6 | 0 | 0 | 26 (20 sembradas) | 0,04 s |
| 5 | Clientes | `cliente` 1.060 (1.056 sin eliminados ni 0/70) | 1.056 | 1.053 | 3 | 0 | ↓ terceros: 1.389 | 0,51 s |
| 6 | Agencias | `sia` 78 | 78 | 74 | 4 | 0 | (en terceros) | 0,05 s |
| 7 | Transportadoras | `empresa_transporte` 273 | 273 | 262 | 9 | 2 | (en terceros) | 0,07 s |
| 8 | Vehículos | `vehiculo` 10.594 | 10.594 | 10.393 | 90 | 111 | 10.393 | 1,05 s |
| 9 | Conductores | `persona` 10.189 (4.416 que conducen) | 4.416 | 4.361 | 47 | 8 | 4.361 | 0,45 s |
| 10 | Productos | `producto` 1.778 | 1.778 | 1.638 | 139 | 1 | 1.643 | 0,20 s |
| 11 | Depósitos vivos | `deposito` 9.682 (**128 vivos**, 133 productos) | 133 | 133 filas (128 depósitos) | 0 | 0 | 128 depósitos, 133 productos, 128 servicios, 202 movimientos de apertura | 0,24 s |
| 12 | Levantes | `producto_levante` 20.523 (170 de los vivos; 118 agrupados) | 118 | 107 | 0 (omitidos: 0) | 11 | 107 | 0,14 s |

- **Terceros:** 1.053 + 74 + 262 = 1.389, con 2.449 roles y 1.053 configuraciones de facturación.
- **Ciclos de facturación cargados:** `Days15` 1.025, `Days30` 24, `Days180` 3 y `Days360` 6 (de `cliente.dias_facturacion`).
- **«Asociados a un equivalente»** son registros del legacy duplicados entre sí: mismo documento normalizado, misma placa o mismo alias o nombre de producto. Se asocian a un solo registro de la v2 (F6-02, regla común); son duplicados legítimos.
- **Lotes:** 41 en `legacy_import_batches`; 18.281 correspondencias en `legacy_id_map`.

## 4. Errores por fila, clasificados

### 4.1 Primera simulación (sin maestros cargados) — FA-MIG-001 y FA-MIG-002

| Entidad | Errores | Causa | Clase |
|---|---|---|---|
| Vehículos | 8.863 | «no existe la transportadora legacy N; impórtela primero» | Dependencia: la simulación no persiste maestros (FA-MIG-002, conocido) |
| Productos | 1.778 | «no existe el embalaje legacy N» | Ídem |
| Depósitos | 133 | «no existe el cliente legacy N» | Ídem |
| Levantes | 170 | «el depósito BAN no está migrado» | Ídem |

Por eso se repitió la simulación de cada entidad dependiente justo antes de su carga en firme, ya con sus maestros. Esas segundas simulaciones dieron los mismos conteos que la carga en firme.

### 4.2 Carga en firme

| Entidad | Filas | Causa | Clase |
|---|---|---|---|
| Ciudades | 6 | «Ya existe la ciudad X (COL, depto.)»: nombre repetido en el mismo departamento con otro id | Duplicado legítimo |
| Ciudades | 1 | Fila del id 0 (comodín «N.A») sin nombre | Dato inválido del legacy |
| Transportadoras | 2 | Tipo de documento «C.I.» (id 256) y «Licencia de Conducción» (id 210), sin equivalente en la v2 | Dato inválido del legacy |
| Vehículos | 62 | Su transportadora es la 210 (59) o la 256 (3), no importadas | Exclusión por regla (en cascada) |
| Vehículos | 49 | Placas inválidas («N.A.», «SIN PLACA.», placas con punto final…) | Dato inválido del legacy |
| Conductores | 8 | Tipo «Cédula de Extrangería» (sic), sin equivalente en la v2 | Dato inválido del legacy |
| Productos | 1 | Embalaje 69 eliminado en el legacy | Exclusión por regla (en cascada) |
| Levantes | 11 | Levantes de productos ya agotados en el legacy (saldo 0, no migrados por el `HAVING ingresan − salen > 0`) | Exclusión por regla |
| **Defecto de la herramienta** | **0** | Con las consultas ajustadas. Con las del plan habría 133 rechazos (DEF-MIG-001), 2 levantes en el depósito equivocado (DEF-MIG-002) y 45 levantes perdidos (DEF-MIG-003). | — |

## 5. Hallazgos en la exportación y la carga

1. **DEF-MIG-001 (MAJOR):** la consulta de F6-03 exporta `M.nom_modalidad` («Entrada por Importación») y el importador la rechaza. Se reprodujo con 133 de 133 filas rechazadas (`def1-Deposits-sim`). Paliativo: exportar el código `IMP`.
2. **DEF-MIG-002 (CRITICAL):** la consulta de levantes filtra por `nro_deposito`, que el legacy reinicia cada año. Da 819 filas en vez de 170, y la simulación crea 109 levantes en vez de 107 (`def2-Releases-sim`). Paliativo: filtrar por `id_deposito`.
3. **DEF-MIG-003 (CRITICAL):** el importador de levantes omite como «repetido» un levante repartido en varias filas del mismo producto (una por camión).
   - 45 filas omitidas, 10.489 unidades perdidas y 14 productos vivos descuadrados (`s2-Releases-sim`).
   - Paliativo: agrupar en la consulta. Tras él, 118 filas, 107 creados, 0 omitidos y conciliación 133/133.
4. **D2:** los 128 depósitos vivos tenían otra fecha de último fin facturado: 104 entre el 2022-12-10 y el 2024-11-30, y 24 sin período. Todos quedaron en 2026-10-01 como inicio de facturación (`billing_start_date`, 128 de 128).
5. **Colmotores:** los clientes 0 y 70 están excluidos por la consulta. Las 9 bodegas `colmotores` estaban eliminadas. Ningún ingreso vivo es del importador 70.
6. **Solo hay importación:** todos los ingresos activos del dump son «Entrada por Importación». No hay depósitos vivos de exportación ni de inspección.

## 6. Idempotencia (OK-3, FA-MIG-004)

Se recargaron en firme ciudades, clientes, vehículos, depósitos y levantes:

| Entidad | Segunda carga |
|---|---|
| Ciudades | 1.774 «actualizadas» por `LegacyId` |
| Clientes | 1.056 omitidos |
| Vehículos | 10.483 omitidos y los mismos 111 errores |
| Depósitos | 133 filas con «el depósito BA… ya fue migrado» (el mensaje de F6-03; se informa como error de fila, no como omitido) |
| Levantes | 107 omitidos y los mismos 11 errores |

Los 16 conteos de la v2, de terceros a `legacy_id_map`, quedaron **idénticos** antes y después (`evidencias/carga/conteos-v2-*-idem.txt`).

## 7. Conciliación (OK-2, FA-MIG-007)

`POST administration/legacy-import/reconciliation` con `11_depositos.csv`:

- **133 Ok, 0 Difference, 0 NotMigrated**, 0 errores (0,16 s).
- Se repitió después de la operación nueva: sigue **133 Ok**. Los movimientos de la v2 (cargues y anulación) quedan explicados por `v2MovementsSinceMigration`.
- **No escribe:** depósitos, movimientos, levantes, lotes y `audit_logs` dieron los mismos conteos antes y después (128, 202, 107, 41 y 23.743).

## 8. Tarifas (D3) y apertura de la facturación (OK-5, FA-MIG-008)

- **Mapeo aprobado:** `mapeo-tarifas-propuesto.md`, con T1 a T4 y el cambio de T4 a $15.000.
  - El legacy **no calcula** el almacenamiento: el valor se digitaba.
  - No hay convenios vigentes.
  - La báscula costaba $20.000.
- **FA-MIG-008 «antes» de las tarifas:** `open-billing` sobre BA0589 da **Opened**, con el período 01/10–16/10/2026 y la factura en **$0**, cargo `MINIMUM_VALUE` y la advertencia «No existe un precio configurado…». Es la regla «la factura de almacenamiento siempre se genera»: no sale `Failed` como sugiere el caso.
- **FA-MIG-008 «después»:** **127 Opened**, 0 Skipped y 0 Failed. BA0589 no se lista porque ya tenía períodos.
  - Inicio el **2026-10-01** en los 128.
  - Fin y límite: 92 el 16/10/2026 y límite el 19/10 (`Days15`); 36 el 30/03/2027 y límite el 02/04/2027 (`Days180`). El límite es fin + 3, como en `cron.php`.
  - Importe: **$42.016,81 + $7.983,19 de IVA = $50.000** cada período. Es coherente con la tarifa mapeada: es el mínimo de T1, porque los migrados no tienen CIF (**DEF-MIG-004**, MAJOR, que se conocía al aprobar).
- **D4 (correo):**
  - **0** contactos con correo en terceros migrados: el importador no tiene columna de correo y `stakeholder_contacts_info` está vacía.
  - **0 mensajes** en el SMTP de captura durante toda la fase.
  - Las 6 notificaciones de la app fueron solo para usuarios internos (Admin y cuentas `mig.*`).
  - El log registra «No se han configurado emails de administradores…» (`NOTIFICATIONS_ADMIN_EMAILS` vacío en local).

## 9. Anexo A del QA (FA-MIG-001 a 010)

| ID | Resultado | Evidencia |
|---|---|---|
| FA-MIG-001 Simulación | **PASA** | 12 entidades en orden con `dryRun=true`; resultado por fila; nada persistido salvo el lote (`resumen-simulacion-1.txt`). |
| FA-MIG-002 Dependencias en simulación | **PASA con nota conocida** | La simulación de dependientes requiere los maestros cargados (§4.1). |
| FA-MIG-003 Carga real | **PASA** | Filas válidas guardadas aunque otras fallen. `GET legacy-import/batches/{id}` del lote de vehículos devuelve sus 111 errores. Hay 41 lotes paginados. |
| FA-MIG-004 Idempotencia | **PASA** | §6. |
| FA-MIG-005 Codificación y separadores | **PASA** | Simulación de productos con «CAFÉ FRESCO» y «CHANCLETA DE BAÑO»: (a) Windows-1252 con `,`, (b) UTF-8 con tabulador, (c) UTF-8 con BOM y `;`. Las tres asocian los 2 productos existentes por nombre (`updated = 2`), lo que prueba tildes y ñ bien leídas. El control sin tilde crea uno nuevo. Los CSV reales en UTF-8 cargaron sin mojibake. |
| FA-MIG-006 Límites | **PASA** | Archivo vacío → 400 «El archivo no tiene filas.» (también con solo el encabezado). 50.001 filas → 400 «El archivo supera 50 000 filas; divídalo.» Entidad «Inventado» → 400 «La entidad Inventado no se puede importar.» `Cities` en el endpoint común → 400. |
| FA-MIG-007 Conciliación | **PASA** | §7. |
| FA-MIG-008 Apertura de la facturación | **PASA con observación** | §8. Antes de las tarifas sale `Opened` en $0 con advertencia, no `Failed`. |
| FA-MIG-009 UI por rol | **PASA con observaciones** | §10.3. Datos coherentes por rol. Migrados en `Confirmed`. Devolver a Borrador → 409 «viene del legacy…». Corregir la fecha → 400 «El depósito no tiene camiones registrados.» La nota «saldos de guía sin salidas previas a la migración» se confirmó y es **DEF-MIG-005**. El importador se ve «Sin asignar» (**DEF-MIG-006**). |
| FA-MIG-010 Número legacy | **PASA con nota conocida** | Buscar «BA0042» en Depósitos de importación → «No se encontraron depósitos». El número legacy no se expone en ningún DTO ni en el frontend. |

## 10. E19 (datos reales)

Todas las operaciones se hicieron por el API con una cuenta por rol creada para esta base (`mig.*`; contraseñas solo en `db_legacy/trabajo/`). Los saldos son de solo lectura en Postgres; evidencias en `db_legacy/trabajo/evidencias/e19/`.

### 10.1 Saldos antes y después

| Operación | Depósito | Antes (recibido / stock / reservado / disponible / nacionalizado) | Después | Resultado |
|---|---|---|---|---|
| **Levante** (CE, `MIG-E19-LEV-0001`, 120 u) | BA0558 → `2024BA00016` | 300 / 300 / 0 / 300 / 0, «SinNacionalizar» | 300 / 300 / 0 / 300 / **120**, «Nacionalizado» | **PASA**: el stock no cambia. |
| OC por encima de lo nacionalizado (150) | BA0558 | — | 400 «… (150) supera lo nacionalizado disponible (120)…» | **PASA** |
| OC sobre un nacionalizado ya despachado en el legacy (40) | BA1451 → `2024BA00103` (nacionalizado 30, salen 30) | 70 / 40 / 0 / 40 / 30 | 400 «… (40) supera lo nacionalizado disponible (0)…» | **PASA**: la v2 descuenta lo despachado en el legacy. |
| **Orden de cargue** `2026OC00001` (100 u) | BA0558 | 300 / 300 / 0 / 300 | 300 / 300 / **100** / 200 | **PASA** |
| **Cargue** (Bodega, 100 u) | BA0558 | 300 / 300 / 100 / 200 | **200 / 0 / 200**; kardex `In:MigrationOpening 300`, `Out:LoadingOrder 100` | **PASA** |
| **Despacho**: guía `2026S00001` | BA0558 (sin salidas en el legacy) | — | Línea: recibido 300, saldo anterior 300, despachado 100, nuevo saldo 200 | **PASA** |
| **Despacho**: OC `2026OC00002` + cargue + guía `2026S00002` (50 u) | BA0042 → `2024BA00002` (recibido 648, salen 200) | 648 / 448 / 0 / 448 | Stock **398**, que es correcto (kardex 448 → 398). **La guía imprime saldo anterior 648 y nuevo saldo 598** | **FALLA: DEF-MIG-005** (66 depósitos afectados) |
| **Anulación** del depósito (F3-08) | BA0589 → `2024BA00017` | 2.000 / 2.000 / 0 / 2.000; período abierto, factura en Borrador | `Cancelled`; stock 0 (`Out:StorageCancellation 2000`); período `Closed`; factura `Cancelled` con motivo | **PASA** |
| Devolver un migrado a Borrador | BA0589 | — | 409 «El depósito 2024BA00017 viene del legacy: corrija sus cantidades con un ajuste de inventario.» | **PASA** |

### 10.2 Períodos con fecha límite

**PASA.**
- Todos los períodos son contiguos al corte D2 (inicio 2026-10-01).
- Duración por ciclo: 15 días → 16/10; 180 días → 30/03/2027.
- Límite = fin + 3, como el legacy.
- La factura conserva las fechas del período.
- Al cargar BA0558, el período conserva lo facturado ($50.000): se cobra por adelantado.
- **No se probó** el «inicio futuro → Skipped» de `open-billing`: todos los migrados empiezan el 2026-10-01, antes de hoy (2026-10-06).

### 10.3 Recorrido por rol (frontend local en el puerto 3001 contra el API de `wms_migracion`)

| Rol | Pantallas | Resultado |
|---|---|---|
| **Comercio Exterior** | Dashboard | 56 sin nacionalizar + 71 nacionalizados = 127 vivos. 66 en «abandono», esperable con ingresos de 2022 a 2024. |
| | Depósitos de importación (`2024BA00002`) | Ingreso 648, nacionalizado 648, despachado 250 (200 del legacy + 50 de la v2), existencias 398. |
| | Detalle | Manifiesto, carta porte, fechas, agencia, levante con FOB y tasa, «Ingreso de camiones cerrado» y «Camiones ingresados: 0». Moneda y valor comercial «—» (DEF-MIG-004). Importador «Sin asignar» (DEF-MIG-006). Se muestran «Editar fecha» y «Devolver para corrección», pero el API los rechaza con mensaje claro. |
| **Bodega** | Inventario | `2024BA00002`: stock 398 / 0 / 398. |
| | Movimientos | Salida de 50 con stock anterior 448 → 398; anulación de `2024BA00017` (2.000 → 0); salida de 100 en `2024BA00016` (300 → 200). |
| **Facturación** | Facturas | Pestañas Báscula 2, Guía 2 y Almacenamiento 128 (Borrador, $50.000). |
| | Inventario general (reporte) | Entran, nacionalizados, salen y saldo de los migrados coherentes con el legacy. |
| **Báscula** | Pantalla única con cola | Vacía (los dos camiones de prueba ya salieron). |
| | Por API | Inicio de salida, cobro de $20.000, tara y repesaje con tiquete `2026T00001`. |
| **Vigilancia** | Por API | Ingreso de un vehículo migrado (placa del legacy) con su conductor migrado, y salida. |

El log del API de toda la fase no tiene ningún 500: solo los 4xx esperados de las pruebas.

## 11. Muestra de 30 depósitos (OK-4)

**30 de 30 depósitos y 35 de 35 filas de producto coinciden.** Se cotejaron cliente, producto y embalaje, recibido, despachado, saldo, levantes (suma), modalidad y manifiesto (número y fecha).

- **Selección:** los 5 de E19, 5 con varios productos, 4 del ciclo de 180 días (cliente 464), 4 sin levantes ni salidas, 4 con levantes y saldo parcial, 4 de 2022–2023 y 4 al azar (semilla 19).
- **Lado legacy:** SQL de lectura sobre las **tablas base** (no sobre el CSV).
- **Lado v2:** SQL de lectura. El saldo legacy se reconstruye como stock actual − movimientos de la v2 posteriores a la migración. El script es `db_legacy/trabajo/consultas/muestra30.py`.

| Depósito legacy | Depósito v2 | Estado v2 | Productos | Recibido | Despachado legacy | Saldo legacy | Levantes | Nacionalizado | Resultado |
|---|---|---|---|---|---|---|---|---|---|
| BA0042 | 2024BA00002 | Confirmed | 1 | 648 | 200 | 448 | 1 | 648 | Coincide |
| BA0090 | 2024BA00005 | Confirmed | 1 | 3.211 | 1.211 | 2.000 | 1 | 3.211 | Coincide |
| BA0118 | 2024BA00006 | Confirmed | 1 | 1.350 | 0 | 1.350 | 0 | 0 | Coincide |
| BA0154 | 2024BA00007 | Confirmed | 1 | 1.732 | 756 | 976 | 1 | 1.732 | Coincide |
| BA0191 | 2024BA00008 | Confirmed | 1 | 1.327 | 406 | 921 | 1 | 1.327 | Coincide |
| BA0233 | 2024BA00009 | Confirmed | 1 | 3.200 | 800 | 2.400 | 1 | 3.200 | Coincide |
| BA0518 | 2024BA00015 | Confirmed | 2 | 2.300 | 0 | 2.300 | 0 | 0 | Coincide |
| BA0558 | 2024BA00016 | Confirmed | 1 | 300 | 0 | 300 | 0 | 0 | Coincide |
| BA0589 | 2024BA00017 | Cancelled | 1 | 2.000 | 0 | 2.000 | 0 | 0 | Coincide |
| BA0739 | 2024BA00026 | Confirmed | 1 | 1.470 | 0 | 1.470 | 0 | 0 | Coincide |
| BA0898 | 2024BA00031 | Confirmed | 1 | 2.700 | 0 | 2.700 | 0 | 0 | Coincide |
| BA1046 | 2023BA00001 | Confirmed | 1 | 2.994 | 2.902 | 92 | 2 | 2.994 | Coincide |
| BA1194 | 2024BA00056 | Confirmed | 1 | 1.350 | 0 | 1.350 | 0 | 0 | Coincide |
| BA1196 | 2024BA00058 | Confirmed | 2 | 2.723 | 1.300 | 1.423 | 2 | 1.500 | Coincide |
| BA1232 | 2024BA00062 | Confirmed | 2 | 517 | 492 | 25 | 2 | 517 | Coincide |
| BA1311 | 2024BA00070 | Confirmed | 1 | 55 | 0 | 55 | 0 | 0 | Coincide |
| BA1352 | 2024BA00079 | Confirmed | 2 | 3.278 | 0 | 3.278 | 0 | 0 | Coincide |
| BA1353 | 2024BA00080 | Confirmed | 1 | 3.200 | 0 | 3.200 | 0 | 0 | Coincide |
| BA1429 | 2024BA00094 | Confirmed | 1 | 2.040 | 0 | 2.040 | 0 | 0 | Coincide |
| BA1436 | 2024BA00097 | Confirmed | 1 | 2.040 | 0 | 2.040 | 0 | 0 | Coincide |
| BA1437 | 2024BA00098 | Confirmed | 1 | 5 | 2 | 3 | 1 | 2 | Coincide |
| BA1442 | 2024BA00101 | Confirmed | 1 | 1.454 | 0 | 1.454 | 0 | 0 | Coincide |
| BA1451 | 2024BA00103 | Confirmed | 1 | 70 | 30 | 40 | 1 | 30 | Coincide |
| BA1590 | 2023BA00002 | Confirmed | 1 | 733 | 122 | 611 | 1 | 733 | Coincide |
| BA1878 | 2023BA00003 | Confirmed | 1 | 1.083 | 968 | 115 | 1 | 1.083 | Coincide |
| BA2576 | 2023BA00008 | Confirmed | 1 | 2.853 | 2.322 | 531 | 2 | 2.853 | Coincide |
| BA2803 | 2023BA00011 | Confirmed | 1 | 3.200 | 0 | 3.200 | 0 | 0 | Coincide |
| BA3029 | 2023BA00012 | Confirmed | 2 | 2.669 | 2.078 | 591 | 2 | 2.669 | Coincide |
| BA3238 | 2023BA00013 | Confirmed | 1 | 1.350 | 820 | 530 | 1 | 1.350 | Coincide |
| BA4575 | 2022BA00002 | Confirmed | 1 | 450 | 0 | 450 | 0 | 0 | Coincide |

- El levante de prueba `MIG-E19-LEV-0001` se excluye del cotejo.
- **Numeración:** la v2 numera los migrados con su año de ingreso (`2022BA…` a `2024BA…`), así que no choca con la serie de 2026.

## 12. Operación nueva completa (OK-7)

Sobre **BA0558 → `2024BA00016`**: levante → OC → ingreso → báscula → cargue → guía → repesaje → salida → facturas.

1. **Levante** de 120 u (Comercio Exterior) → nacionalizado 120.
2. **OC `2026OC00001`** por 100 u (Comercio Exterior) → reserva 100. Primer consecutivo `2026OC00001`.
3. **Ingreso** (Vigilancia) del vehículo migrado con su conductor migrado.
4. **Salida en báscula** (Báscula): cobro inmediato de **$20.000** ($16.806,72 + $3.193,28 de IVA), factura `Paid`; tara de 15.000 kg con tiquete `2026T00001`.
5. **Cargue** (Bodega) de 100 u con firma y precinto → stock 300 → 200; reserva liberada.
6. **Guía `2026S00001`** (Comercio Exterior) → cobro de **$15.000** sin IVA (T4), factura `Paid`. Saldos de la guía: 300 / 100 / 200, correctos.
7. **Repesaje** de 17.500 kg → ciclo `Complete`. **Salida** (Vigilancia).
8. **Facturación:** N.º SIIGO de prueba en la factura de la guía (204). La factura de almacenamiento de BA0558 ($50.000, período 01/10–16/10/2026) se numeró y se **aprobó** (`Approved`).
9. **Conciliación posterior:** BA0558 sigue `Ok` (saldo legacy 300 + movimientos v2 −100 = stock 200).

**Resultado: PASA.** Funciona de punta a punta con saldos correctos. La misma operación sobre un depósito **con salidas en el legacy** (BA0042) también funciona y deja bien el stock, pero la guía imprime saldos errados (DEF-MIG-005, §10.1).

## 13. Criterios OK

| # | Criterio | Resultado | Motivo |
|---|---|---|---|
| OK-1 | 12 entidades en firme; cada rechazo con causa aceptada; 0 rechazos por defecto de la herramienta | **Cumple** | §3 y §4.2: 0 rechazos por defecto en la carga en firme, con los CSV congelados. Los defectos DEF-MIG-001 a 003 se registraron y se esquivaron en las consultas (§5); hay que corregirlos antes del corte real. |
| OK-2 | Conciliación sin diferencias sin explicar | **Cumple** | 133/133 Ok (§7). |
| OK-3 | Idempotencia | **Cumple** | §6. |
| OK-4 | Muestra de 30: 100 % coincide | **Cumple** | 30/30 (§11). |
| OK-5 | `open-billing`: Opened o Skipped con causa; inicio el 2026-10-01; importe coherente con la tarifa mapeada | **Cumple** | 127 Opened más 1 con período previo (FA-MIG-008), luego anulado; inicio el 2026-10-01 en los 128; $50.000 = mínimo de T1, como estaba previsto y aprobado (DEF-MIG-004). |
| OK-6 | FA-MIG-001 a 010 y E19 sin FALLA (salvo FA-MIG-002 y 010) | **No cumple** | E19 «saldos después de un despacho» falla en la guía de los migrados con salidas en el legacy (DEF-MIG-005). FA-MIG-001 a 010 sin FALLA (§9). |
| OK-7 | Operación nueva de punta a punta con saldos correctos | **Cumple** | §12. |
| OK-8 | Tiempos anotados | **Cumple** | §1. |

### Qué hay que corregir para dar el OK

| Prioridad | Defecto | Corrección | Bloquea |
|---|---|---|---|
| **1** | **DEF-MIG-005** (CRITICAL) | Guía de salida: sumar a «lo despachado antes» el movimiento `Out` `MigrationOpening` del producto migrado. | La fase 2: los operarios verían guías con saldos errados en 66 depósitos. |
| 2 | **DEF-MIG-003** (CRITICAL) | Importador de levantes, sumar las filas del mismo levante y producto, y/o la consulta del plan. | El corte real (en las fases 1 y 3 el CSV congelado ya va agrupado). |
| 3 | **DEF-MIG-002** (CRITICAL) | Consulta de levantes del plan por `id_deposito`. | Ídem. |
| 4 | **DEF-MIG-001** (MAJOR) | Consulta de depósitos del plan (código de modalidad), o el parser acepta «Entrada por …». | Ídem. |
| 5 | **DEF-MIG-004** (MAJOR) | Llevar el CIF y la moneda al CSV y a `CreateMigrated`. | El corte real: importes del almacenamiento. Para staging el usuario aceptó el mínimo. |
| 6 | **DEF-MIG-006** (MINOR) | Mostrar el importador aunque sea el cliente. | Ninguna fase; mejora visual. |

**Después de corregir DEF-MIG-005**, según el plan §4: re-ejecutar la fase 1 desde una base limpia con los mismos CSV congelados. Basta con repetir la carga, `open-billing` y el despacho de E19 sobre un depósito con salidas en el legacy. Si además se corrigen DEF-MIG-001 a 004, regenerar y volver a congelar el conjunto de CSV con las consultas corregidas del plan.

## 14. Estado del ambiente que queda

| Recurso | Estado |
|---|---|
| `legacy-mariadb` (MariaDB 10.11, `localhost:3308`, volumen `legacy-mariadb-data`, base `bodegas`) | **Arriba.** Contraseña en `db_legacy/trabajo/.mariadb.local` (modo 600). Usuario definidor `bodegas@localhost` bloqueado, solo SELECT. |
| `wms_migracion` en `wms-postgres-db` (5433) | **Arriba.** Con la migración, las tarifas, la facturación abierta y las operaciones de E19 (OC `2026OC00001`/`00002`, guías `2026S00001`/`00002`, tiquete `2026T00001`, BA0589 anulado). |
| API local contra `wms_migracion` (`http://localhost:5291`) | Arriba (PID en `db_legacy/trabajo/evidencias/api.pid`; variables en `db_legacy/trabajo/.env.migracion.local`). Se puede detener sin perder datos. |
| Frontend local (`http://localhost:3001`) | Arriba (PID en `evidencias/front.pid`). Se puede detener. |
| `migracion-mailpit` (SMTP de captura, `127.0.0.1:1025`, UI en `:8025`) | Arriba, con 0 mensajes. |
| Cuentas de prueba `mig.vigilancia`, `mig.bascula`, `mig.bodega`, `mig.comext` y `mig.facturacion` (solo en `wms_migracion`) | Contraseñas en `db_legacy/trabajo/credenciales-migracion-local.local.md`. No son las de staging (D5). |
| CSV | **Congelados** en `db_legacy/trabajo/csv/` con su SHA-256 (`registro-csv-fase-1.md`). |
| `wmsdb`, `mysql57`, staging y producción | Sin tocar. |
| Repositorios | Sin cambios de código ni de configuración. Solo `docs/planes/migracion-staging/` sin commit. |
