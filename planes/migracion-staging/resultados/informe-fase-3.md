# Informe de la fase 3: migración del legacy en staging

> **Fecha:** 2026-10-06, de 22:45 a 23:05 (hora de Colombia). **Ejecutor:** agente (Opus 5.5). **Prompt:** `prompt-fase-3.md`.
> **Ambiente:** staging (`https://api.100-60-89-139.sslip.io/api/v1`), con el BE `b31ddb6` y el FE `508b91b`.
> **Plan:** `plan-migracion-legacy-staging.md` §2, §3 y §6.
> **Referencia local:**
> - la parte A de `informe-actualizacion-fases-1-2.md`;
> - `wms_migracion` y el API en el puerto 5291, solo para leer.
>
> **Cómo se trabajó:**
> - Los datos entraron **solo por el API de importación**, con el Admin y por HTTPS, y cada carga en firme tuvo su simulación antes.
> - En staging solo hubo **SQL de solo lectura** (`BEGIN TRANSACTION READ ONLY`, por SSH con `docker exec … psql`). En local, igual sobre `wms_migracion`.
> - Los CSV no se copiaron al servidor.
>
> **Datos personales:** el informe lleva conteos, números de depósito y códigos. Las respuestas completas del API, que nombran ciudades, terceros y productos, están fuera de git, en `db_legacy/trabajo/evidencias/staging-f3/`.
> **Secretos:** la contraseña del Admin se leyó de `.admin-staging.local` sin imprimirla, y el token solo vivió en memoria. Para la revisión en pantalla, el usuario inició sesión en el navegador.

## Veredicto

**Staging queda migrado e idéntico a local, y listo para la Fase 4.**

| Criterio | Resultado |
|---|---|
| Carga de las 12 entidades | **Mismos números que local en todas.** En simulación y en firme coinciden los cinco conteos (filas, creados, asociados, omitidos y rechazados) y la lista de errores, fila por fila y con el mismo mensaje. |
| Conciliación | **133 «Ok»**, 0 «Difference» y 0 «NotMigrated». La respuesta es idéntica a la de local. |
| Tarifas T1 a T4 | **Iguales a las de local** al leerlas por el API en los dos lados. |
| `open-billing` | **128 «Opened»**, 0 «Skipped» y 0 «Failed». |
| Total del primer período | **$91.257.475,39**: $76.686.954,14 de subtotal y $14.570.521,25 de IVA. |
| Comparación con local | **Conteos idénticos.** Las únicas diferencias vienen de las operaciones de prueba de BA0042 en local (§6.2). Las **128 facturas** coinciden en número legacy, período y total. |
| Revisión en pantalla | **10 de 10 depósitos**, 10 inventarios, 3 facturas y las 9 ubicaciones correctos. |
| Correo | **0 envíos** durante la carga y **0 contactos** de terceros. |
| Respaldos | «Antes de migrar» y «staging migrado» terminaron en `Succeeded`. |

**Defectos nuevos:** ninguno. Hay **dos observaciones** que no bloquean la Fase 4:
- **O-4:** el orden de los productos en el texto de la factura cambia entre cargas (§6.3).
- **O-5:** una nota sobre los tiempos (§2.3).

---

## 1. Verificaciones previas

### 1.1 Hashes del conjunto v3

`shasum -a 256 -c sha256-csv-fase-1-v3.txt` → **12 de 12 «OK»**.

### 1.2 Estado de staging antes de cargar

Leído por el API y con SQL de solo lectura:

| Comprobación | Resultado |
|---|---|
| Login del Admin | 200 |
| Migraciones | 11; la última, `20261007030137_RemoveSampleSeedData` |
| Lotes de importación (`GET administration/legacy-import/batches`) | **0** (`totalCount` 0) |
| Depósitos | **0** |
| Ubicaciones | **0** |
| Productos | 1, «Contenedor Vacío» |
| Terceros, vehículos, ciudades y embalajes | 0 |
| Reglas de tarifa, precios y convenios | 0 |
| Facturas | 0 |
| Catálogo sembrado | 6 roles del sistema, 5 roles de negocio, 4 modalidades, 5 servicios, 10 unidades de medida e impuestos `IVA` y `RETE_FUENTE` |
| Mínimos de almacenamiento | Los 3 en $0 sin IVA |
| `ServiceTax` | Solo ALMACENAMIENTO–IVA, igual que en local antes de T3 |
| Usuarios | 1 (`admin`) |

**Id sembrados:** los que usan las peticiones de tarifas (servicios, fórmula `PERCENTAGE_OF_VALUE`, IVA, `IMP001` y el mínimo de IMP) **son los mismos** en staging y en local. La única diferencia era el mínimo de IMP, que en local ya tenía T2.

### 1.3 Respaldo «antes de migrar»

`POST administration/backups/run` → 202 → corrida `Manual` **`Succeeded`** en 0,7 s, en el destino `local-staging`.

| Archivo en `/opt/wms/backups/2026/10/` | Tamaño |
|---|---|
| **`wms_20261006_2250.dump`** | 306.798 B |
| `uploads_20261006_2250.tar.gz` | 342.517 B |

Es el punto para volver a una base sin datos migrados. **No se usó.**

## 2. Carga por entidad, comparada con local

Orden del §3.4. Para cada entidad se hizo la simulación, se comparó con la simulación de local (`evidencias/v3/carga/s2-*.json`), luego el firme, y se comparó con el firme de local (`f1-*.json`).
- **Qué se comparó:** la respuesta completa del API, salvo el `batchId`: los conteos y la lista de errores con su número de fila y su mensaje.
- **Regla:** cualquier diferencia detenía la carga. **No hubo ninguna.**

### 2.1 Resultado

| # | Entidad | Filas | Creados | Asociados | Omitidos | Rechazados | Errores por fila | ¿Igual a local? |
|---|---|---|---|---|---|---|---|---|
| 1 | Ciudades (`cities/import`) | 1.781 | 1.774 | 0 | — | 7 | 7 | **Sí** (simulación y firme) |
| 2 | Embalajes | 67 | 61 | 6 | 0 | 0 | 0 | **Sí** |
| 3 | Cuadrillas | 7 | 7 | 0 | 0 | 0 | 0 | **Sí** |
| 4 | Ubicaciones | 9 | 9 | 0 | 0 | 0 | 0 | **Sí** |
| 5 | Clientes | 1.056 | 1.053 | 3 | 0 | 0 | 0 | **Sí** |
| 6 | Agencias | 78 | 74 | 4 | 0 | 0 | 0 | **Sí** |
| 7 | Transportadoras | 273 | 262 | 9 | 0 | 2 | 2 | **Sí** |
| 8 | Vehículos | 10.594 | 10.393 | 90 | 0 | 111 | 111 | **Sí** |
| 9 | Conductores | 4.416 | 4.361 | 47 | 0 | 8 | 8 | **Sí** |
| 10 | Productos | 1.778 | 1.639 | 138 | 0 | 1 | 1 | **Sí** |
| 11 | Depósitos (filas de producto) | 133 | 133 (128 depósitos) | 0 | 0 | 0 | 0 | **Sí** |
| 12 | Levantes | 170 | 107 | 0 | 0 | 18 | 18 | **Sí** |

- **Errores por fila:** son los de local, con la misma fila y el mismo mensaje. Por eso tienen la misma causa (`informe-fase-1-repeticion.md` §4.2):

  | Entidad | Rechazos | Causa |
  |---|---|---|
  | Ciudades | 6 | Nombre repetido |
  | Ciudades | 1 | Id 0 sin nombre |
  | Transportadoras | 2 | Tipo de documento sin equivalente |
  | Vehículos | 62 | En cascada, por esas 2 transportadoras |
  | Vehículos | 49 | Placa inválida |
  | Conductores | 8 | «Cédula de Extrangería» |
  | Productos | 1 | Embalaje 69 eliminado |
  | Levantes | 18 filas (11 grupos) | Productos agotados en el legacy |

  **0 rechazos por defecto de la herramienta.**
- **Simulación frente a firme:** en las 12 entidades, la simulación dio los mismos números que su firme.
- **Lotes en staging:** quedaron **24**, una simulación y un firme por entidad.

### 2.2 Tiempos (simulación + firme, de ida y vuelta desde el Mac)

| Entidad | Tamaño del CSV | Local (s) | Staging (s) |
|---|---|---|---|
| Ciudades | 52 KB | 0,01 + 0,20 | 0,57 + 1,59 |
| Embalajes | 1 KB | 0,02 + 0,02 | 0,58 + 0,40 |
| Cuadrillas | 0,2 KB | 0,01 + 0,00 | 0,41 + 0,32 |
| Ubicaciones | 0,4 KB | 0,01 + 0,00 | ≈ 0,4 + 0,3 (ver §2.3) |
| Clientes | 58 KB | 0,53 + 0,47 | 3,07 + 2,47 |
| Agencias | 4 KB | 0,02 + 0,02 | 0,41 + 0,44 |
| Transportadoras | 17 KB | 0,06 + 0,05 | 0,65 + 0,69 |
| Vehículos | 205 KB | 1,41 + 1,21 | 7,73 + 5,95 |
| Conductores | 269 KB | 0,46 + 0,52 | 2,76 + 3,15 |
| Productos | 72 KB | 0,21 + 0,25 | 1,66 + 1,39 |
| Depósitos | 20 KB | 0,37 + 0,21 | 1,94 + 1,40 |
| Levantes | 18 KB | 0,13 + 0,09 | 1,13 + 0,98 |
| **Total de las 12** | | **6,3** | **≈ 40** |
| Conciliación | | 0,12 | 1,04 |
| Tarifas (5 peticiones) | | 0,19 | 2,54 |
| `open-billing` (128 depósitos) | | 1,41 | **6,81** |

- **Staging tarda unas 6 veces más que local.** La red explica la diferencia en los archivos pequeños (≈ 0,3 a 0,4 s por petición). En vehículos, clientes y `open-billing` pesa además la base del servidor (Lightsail de 4 GB).
- **Todo el proceso mecánico tarda menos de 1 minuto:** carga, conciliación, tarifas y apertura. Para la ventana del corte real siguen mandando la exportación y la revisión humana de cada simulación.

### 2.3 Observación O-5: tiempos de ubicaciones

El primer lanzamiento del script de carga se hizo con su salida cortada (`| head -5`). Al cerrarse la tubería, el script siguió hasta el firme de ubicaciones y se detuvo al imprimir. Por eso **no quedó el tiempo de ubicaciones**.

- **Se verificó antes de seguir:** las respuestas guardadas de simulación y firme de ciudades, embalajes, cuadrillas y ubicaciones son **idénticas** a las de local. Los lotes de staging muestran exactamente una simulación y un firme por entidad.
- **El tiempo de ubicaciones se estimó** con las horas de los lotes: ≈ 0,4 s de simulación y ≈ 0,3 s de firme.
- **Después se relanzó desde clientes** con la salida completa.
- **Impacto en los datos:** ninguno.

## 3. Conciliación

`POST administration/legacy-import/reconciliation` con `11_depositos.csv`:

| | Staging | Local |
|---|---|---|
| «Ok» | **133** | 133 |
| «Difference» | **0** | 0 |
| «NotMigrated» | **0** | 0 |
| Tiempo | 1,04 s | 0,12 s |

La respuesta, con el detalle de las 133 filas, es **idéntica** a la de local (`conciliacion-1.json`).

## 4. Tarifas T1 a T4

**Peticiones:** las mismas de la repetición, con el mismo cuerpo (`informe-fase-1-repeticion.md` §7 y `mapeo-tarifas-propuesto.md` §5):

| # | Petición | Resultado |
|---|---|---|
| T1 | `POST service/{ALMACENAMIENTO}/pricing-rules`: `PERCENTAGE_OF_VALUE`, `IMP001`, sin producto, `percentage 0.295`, `minimum 50000`, `minimumIncludesVat true`, `taxIncluded false` | 200 |
| T2 | `PUT service/{ALMACENAMIENTO}/minimum-values/{IMP}`: `amount 50000`, `includesVat true`, activo | 200 |
| T3 | `POST service/{BASCULA}/assign-tax` (IVA) | 200 |
| T3 | `POST service/{BASCULA}/prices`: `basePrice 16806.72` desde `2026-10-01T00:00:00-05:00` | 200 |
| T4 | `POST service/{GUIA_SALIDA}/prices`: `basePrice 15000` desde `2026-10-01T00:00:00-05:00` | 200 |

- **Convenios:** no se crearon (T6). Hay 0 convenios en los dos lados.
- **Comparación por el API.** Se leyeron, en staging y en local:
  - el servicio;
  - sus precios;
  - sus reglas de tarifa;
  - sus mínimos.

  Se leyó de ALMACENAMIENTO, BASCULA, GUIA_SALIDA y MONTACARGAS: 16 lecturas, todas con 200.
  - Se compararon **sin** los Id y las fechas de creación.
  - **15 de las 16 son iguales.**
  - En las reglas de ALMACENAMIENTO, los 3 parámetros de T1 vienen en otro orden dentro de la lista, pero con **las mismas claves y los mismos valores**: el API no los ordena.
  - **Las tarifas quedaron iguales.**

## 5. Apertura de la facturación

`POST administration/legacy-import/open-billing` → **128 «Opened»**, 0 «Skipped» y 0 «Failed», en 6,81 s.

| | Facturas | Período | Total con IVA |
|---|---|---|---|
| Ciclo de 15 días | 92 | 01/10/2026 a 16/10/2026 (límite 19/10) | $63.258.314,46 |
| Ciclo de 180 días | 36 | 01/10/2026 a 30/03/2027 | $27.999.160,93 |
| **Total** | **128** | Todos desde el **2026-10-01** | **$91.257.475,39** ($76.686.954,14 + $14.570.521,25 de IVA) |

- Los 128 períodos usan `PERCENTAGE_OF_VALUE`, con origen `ServiceRule`.
- **124 quedan sobre el mínimo y 4 en el piso** de $50.000: BA0558, BA0860, BA1283 y BA1448.
- Las 128 facturas están en **Borrador**.

## 6. Comparación con local

### 6.1 Conteos por entidad

SQL de solo lectura en los dos lados, a las 22:55, tras `open-billing`:

| Entidad | Local | Staging | Diferencia |
|---|---|---|---|
| Terceros | 1.389 | 1.389 | — |
| Rol `CUSTOMER` / `IMPORTER` / `CUSTOMS_AGENCY` / `TRANSPORT_COMPANY` | 1.053 / 1.053 / 77 / 266 | 1.053 / 1.053 / 77 / 266 | — |
| Configuraciones de facturación | 1.053 | 1.053 | — |
| Contactos de terceros (con correo) | 0 (0) | 0 (0) | — |
| Vehículos | 10.393 | 10.393 | — |
| Conductores | 4.361 | 4.361 | — |
| Productos | 1.640 | 1.640 | — |
| Embalajes / cuadrillas / ciudades | 61 / 7 / 1.774 | 61 / 7 / 1.774 | — |
| Ubicaciones (no disponibles) | 9 (1) | 9 (1) | — |
| Depósitos (migrados, `Confirmed`) | 128 (128, 128) | 128 (128, 128) | — |
| Productos de depósito | 133 | 133 | — |
| Movimientos de apertura: entrada / salida (`MigrationOpening`) | 133 / 69 | 133 / 69 | — |
| Levantes | 107 | 107 | — |
| `legacy_id_map` (total) | 18.284 | 18.284 | — |
| ↳ Embalajes / cuadrillas / ubicaciones | 67 / 7 / 9 | 67 / 7 / 9 | — |
| ↳ Clientes / agencias / transportadoras | 1.056 / 78 / 271 | 1.056 / 78 / 271 | — |
| ↳ Vehículos / conductores / productos | 10.483 / 4.408 / 1.777 | 10.483 / 4.408 / 1.777 | — |
| ↳ Depósitos | 128 | 128 | — |
| Períodos de almacenamiento | 128 (92 al 16/10 y 36 al 30/03) | 128 (92 al 16/10 y 36 al 30/03) | — |
| Facturas de almacenamiento | 128, $91.257.475,39 | 128, $91.257.475,39 | — |
| ↳ en Borrador / en el piso de $50.000 | 128 / 4 | 128 / 4 | — |
| Reglas de tarifa / precios / convenios | 1 / 2 / 0 | 1 / 2 / 0 | — |
| Servicios (`service_records`) | **129** | 128 | Operación de prueba (§6.2) |
| Movimientos de salida por orden de cargue | **1** | 0 | Operación de prueba |
| Facturas (todas) | **130** | 128 | Operación de prueba: báscula y guía |
| Órdenes de cargue / guías / ingresos | **1 / 1 / 1** | 0 / 0 / 0 | Operación de prueba |
| Usuarios | **6** | 1 | Local tiene las 5 cuentas `mig.*` |
| Lotes de importación | **43** | 24 | Local tiene, además, la primera pasada sin maestros (12) y la idempotencia (7) |

### 6.2 Diferencias explicadas: la operación de prueba de BA0042 en local

La parte A del informe de actualización registró en `wms_migracion` la salida de prueba de **BA0042**:
- la OC `2026OC00001`;
- el ingreso del vehículo;
- el cobro de báscula;
- el cargue de 50 unidades;
- la guía `2026S00001`;
- el repesaje y la salida.

Esa operación explica **todas** las diferencias de la tabla:

| Diferencia | Causa |
|---|---|
| +1 servicio | El de salida |
| +1 movimiento de salida | El cargue |
| +2 facturas | Báscula y guía, de contado |
| +1 OC, +1 guía y +1 ingreso | La propia operación |
| Stock de BA0042 en 398 en local y **448** en staging | Los 50 que salieron en local. El recibido (648) y lo nacionalizado (648) son iguales. |

Las cuentas `mig.*` y los lotes extra son de la preparación de local y no tocan los datos migrados.

### 6.3 Depósito por depósito

**Cómo se comparó:** por número legacy (`legacy_number`), sin comparar Id de la v2, en los dos lados.

| Nivel | Campos |
|---|---|
| **Depósito (128)** | Número v2, estado, moneda, CIF, TRM y su origen, fecha de ingreso, inicio de facturación, ubicación, identificación del cliente, carta porte, modalidad, estado de nacionalización, manifiesto con su fecha y cantidad nacionalizada |
| **Producto (133)** | Producto, embalaje, declarado, recibido, stock, reservado, disponible, ubicación, cantidad y número de levantes |
| **Período y factura (128)** | Inicio, fin, límite, estado, fórmula, tarifa, cantidad, importe, base y origen del período. Estado, subtotal, IVA, total, saldo, vencimiento, fechas, número SIIGO, huella del detalle y número de líneas de la factura |

| Resultado | Filas |
|---|---|
| Idénticas | **385 de 389** |
| BA0042, producto | 1: stock 398 en local frente a 448 en staging. Es la operación de prueba (§6.2). |
| BA0518, BA1232 y BA3029, factura | 3: **mismo período, mismo subtotal, mismo IVA y mismo total.** Solo cambia el **orden de los dos productos** en el texto del detalle («ALMACENAMIENTO DE: …») y en la descripción de la línea. |

**Las 128 facturas coinciden en número legacy, período y total. No hay diferencias de importe.**

**Observación O-4: el orden de los productos en el texto de la factura.**
- **Qué pasa:** `StorageBillingService` arma el detalle y la línea con `storage.StorageProducts` cargados con `Include` sin `OrderBy`, y EF los devuelve en el orden de su clave. El `Id` de `warehouse_storage_products` es un GUID aleatorio que cambia en cada carga.
- **Se comprobó con SQL:** en cada ambiente, el orden del texto es el de `ORDER BY wsp.id`.
- **Alcance:** 5 depósitos migrados tienen 2 productos. En 3 el orden salió distinto entre local y staging; en los otros 2 coincidió por azar.
- **Impacto:** solo cosmético. No cambia importes, cantidades ni la conciliación.
- **Sugerencia, si se quiere un orden estable:** ordenar los productos del depósito, por ejemplo por fecha de creación o por nombre. Se deja anotado, **sin ficha**, porque no es un defecto de la migración.

## 7. Revisión en pantalla (solo lectura)

`https://app.100-60-89-139.sslip.io`, con el Admin. El usuario inició sesión en el navegador y el agente **solo leyó**: no creó, editó ni aprobó nada.
- **Comprobación al terminar:** los conteos de §6.1 y la comparación depósito por depósito de §6.3, repetidos sobre staging, **no cambiaron**.

### 7.1 Ubicaciones (`/admin/locations`)

- Resumen: «Total **9** · Disponibles **8** · No disponibles **1**».
- **`Bodega 1 BA-[1][1]`** aparece **No disponible**.
- Disponibles: Bodega 2 a 5 BA, Bodega Baja BA, Cobertizo, Patio 1 BA y Patio 2 BA.
- No aparece ninguna ubicación de ejemplo.

### 7.2 Detalle de 10 depósitos migrados (Comercio Exterior)

**Lista de depósitos:** 0 en Borrador y **128 confirmados**.

**Elección:** con y sin salidas en el legacy, con 2 productos, de los dos ciclos, el de mayor importe y los 4 del piso.

| Legacy | v2 | Por qué | Nacionalización | Valor comercial | Productos: depósito → stock | Levantes | Factura |
|---|---|---|---|---|---|---|---|
| BA0042 | 2024BA00002 | Con salidas en el legacy | Nacionalizado (648) | US$ 34.248,00 | 648 → 448 | 1 | 15 días |
| BA0118 | 2024BA00006 | Ciclo de 180 días, sin salidas | Sin Nacionalizar | US$ 44.550,00 | 1.350 → 1.350 | 0 | 180 días |
| BA0154 | 2024BA00007 | Ciclo de 180 días, con salidas | Nacionalizado (1.732) | US$ 45.664,80 | 1.732 → 976 | 1 | 180 días |
| BA0518 | 2024BA00015 | 2 productos, sin salidas | Sin Nacionalizar | US$ 56.800,00 | 300 → 300 y 2.000 → 2.000 | 0 | 15 días |
| BA0558 | 2024BA00016 | **Piso**; producto «PLATANO SECO» migrado (DEF-MIG-008) | Sin Nacionalizar | US$ 2.700,00 | 300 → 300 | 0 | 15 días |
| BA0860 | 2024BA00030 | **Piso**, con salidas | Nacionalizado (200) | US$ 3.000,00 | 200 → 20 | 1 | 15 días |
| BA1196 | 2024BA00058 | 2 productos, con salidas | Nacionalizado (1.500) | US$ 62.701,00 | 500 → 200 y 2.223 → 1.223 | 2 | 15 días |
| BA1283 | 2024BA00065 | **Piso** | Sin Nacionalizar | US$ 1.350,00 | 90 → 90 | 0 | 15 días |
| BA1448 | 2024BA00102 | **Piso** | Sin Nacionalizar | US$ 2.879,00 | 104 → 104 | 0 | 15 días |
| BA2355 | 2022BA00001 | El de mayor importe ($3.483.997,59), ingreso de 2022 | Nacionalizado (730) | US$ 239.075,00 | 1.330 → 1.200 | 1 | 15 días |

**Qué muestra el detalle de los 10, y coincide con la base:**
- el cliente del depósito;
- **el importador** en «Terceros documentales» (no «Sin asignar») y la agencia de aduanas;
- el **manifiesto DIAN** con su número y fecha, y la carta porte;
- **moneda USD** y el **valor comercial**;
- la fecha de ingreso del legacy;
- los levantes, con su número, aceptación, cantidad, FOB y tasa;
- por producto: la cantidad declarada, la del depósito, el stock, lo reservado (0) y lo disponible;
- «Ingreso de camiones cerrado», con «Camiones ingresados: 0».

**BA2355** aparece «Nacionalizado» con 730 nacionalizados y 1.200 en stock. **Es correcto:** la regla vigente (ACE-1, `ImportWarehouseStorage.cs:114`) lo marca nacionalizado con al menos un levante. Es igual en local.

### 7.3 Inventario de Bodega (`/warehouse/inventory`, «Consultar stock»)

Los 10 depósitos muestran el **stock actual, reservado y disponible de la tabla anterior**, por producto, con reservado 0. Por ejemplo:
- 2024BA00002: 448 / 0 / 448;
- 2024BA00058: 200 y 1.223, total 1.423;
- 2022BA00001: 1.200.

### 7.4 Facturas de almacenamiento en Borrador

| Factura de | Período | Detalle | Línea | Subtotal | IVA | Total |
|---|---|---|---|---|---|---|
| BA0042 (2024BA00002) | 01/10/2026 – 16/10/2026 | «ALMACENAMIENTO DE: 448 UNIDAD …, 2024BA00002 …». USD 34.248,00 × TRM 3.927,64 (Manual, 10/01/2024) = $134.513.814,72 | «Tarifa base (nivel 2)» | $396.815,75 | $75.394,99 | **$472.210,74** |
| BA0558 (2024BA00016) | 01/10/2026 – 16/10/2026 | «ALMACENAMIENTO DE: 300 UNIDAD PLATANO SECO …». TRM 3.931,31 | «Almacenamiento **(mínimo aplicado)**» | $42.016,81 | $7.983,19 | **$50.000** |
| BA0118 (2024BA00006) | 01/10/2026 – 30/03/2027 | «ALMACENAMIENTO DE: 1350 UNIDAD …». TRM 3.929,79 | «Tarifa base (nivel 2)» | $516.462,83 | $98.127,94 | **$614.590,77** |

- Los tres están en **Borrador**, «Pendiente de número».
- Los importes son **los mismos del cotejo independiente de local** (`informe-fase-1-repeticion.md` §7).

### 7.5 Otros

- El menú no muestra «Estadísticas», por decisión del usuario.
- La consola del navegador tuvo **un solo error, un 404**.
  - **Causa:** el agente abrió el detalle de un depósito por URL con el Id de `warehouse_storages`, y la ruta espera el de `import_warehouse_storages`.
  - **En el log del API** es la única línea `fail:`, «El depósito de importación no existe».
  - **En la pantalla** queda «Cargando…» sin mensaje de error.
  - Navegando desde la lista, el enlace usa el Id correcto. No se registra como defecto.

## 8. Correo y avisos (D4)

| Comprobación | Resultado |
|---|---|
| **Log del API** desde las 22:45 (inicio de la carga) hasta el respaldo final, ≈ 317.000 líneas | **0** líneas de `EmailService` o `NotificationService`, ningún «Email enviado…» y ningún `warn:`. Hay un solo `fail:`, el 404 del §7.5. **No salió ningún correo, a ninguna dirección.** |
| **Notificaciones de la app** | **0 nuevas.** La única de la tabla es «Falló el respaldo», del 06/10 a las 18:58, anterior a esta fase y de la fase 2. |
| **Contactos de terceros** (`stakeholder_contacts_info`) | **0**, y 0 con correo. Igual en local. |
| **Usuarios de staging** | Solo `admin`, con el correo del usuario (`capb.dev@gmail.com`). |

**Cumple D4.** No hubo correos a otras direcciones.

## 9. Respaldo «staging migrado»

`POST administration/backups/run` al terminar, después de la revisión en pantalla → 202 → corrida `Manual` **`Succeeded`** en 0,7 s. `sizeBytes` 4.407.615, que es la suma de los dos archivos.

| Archivo en `/opt/wms/backups/2026/10/` | Tamaño |
|---|---|
| **`wms_20261006_2302.dump`** | **4.065.098 B** (≈ 3,9 MB) |
| **`uploads_20261006_2302.tar.gz`** | **342.517 B** |

- **Es el punto de restauración** de la base migrada, sin operaciones, con las tarifas y la facturación abierta. Lo usa la Fase 5 para repetir las pruebas.
- **No se restauró nada.** Los respaldos manuales no se borran por retención.

## 10. Estado que queda

| Recurso | Estado |
|---|---|
| **Staging** | BE `b31ddb6` / FE `508b91b`, 11 migraciones. **Cargado con el conjunto v3:** 128 depósitos `Confirmed` con 128 períodos y 128 facturas de almacenamiento en Borrador ($91.257.475,39), tarifas T1 a T4 y 24 lotes de importación. Sin operaciones nuevas. Un solo usuario (`admin`). |
| **Respaldos de staging** | «Antes de migrar» `wms_20261006_2250.dump`; «staging migrado» `wms_20261006_2302.dump`. |
| **Local** | `wms_migracion`, el API en el puerto 5291 y `legacy-mariadb`, sin cambios (solo se leyeron). |
| **Evidencias** (fuera de git) | En `db_legacy/trabajo/evidencias/staging-f3/`: las 24 respuestas de carga, la conciliación, las tarifas con su comparación, `open-billing` y los dos respaldos. |
| **`wmsdb`, `mysql57` y producción** | Sin tocar. |
| **Repositorios** | Sin cambios de código ni de configuración. Solo `docs/planes/migracion-staging/` sin commit. |

**Siguiente paso:** la Fase 4 (QA en staging, sesión S6). Empieza solo con la autorización del usuario.
