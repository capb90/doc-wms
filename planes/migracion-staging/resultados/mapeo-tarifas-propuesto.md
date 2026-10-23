# Mapeo de tarifas y convenios del legacy a la v2 (D3) — propuesta

> **Fase 1, checkpoint intermedio.** Fecha: 2026-10-06. Fuente: `backupBodegas.sql` (corte del dump 2024-06-10) cargado en `legacy-mariadb`.
> **Estado:** **aprobado por el usuario el 2026-10-06** («sí, aprueba T1 a T4»), con un cambio en T4: la guía de salida se cobra a **$15.000** en la v2, aunque el legacy no la cobraba. Se cargó por el API en `wms_migracion` (§5) y es el mapeo que se repite en la fase 3.
> Los clientes se citan por su id del legacy (`cliente.id_cliente`), sin nombres.

## 1. Dónde tarifaba el legacy

| Fuente | Hallazgo |
|---|---|
| `tarifa` | 1 registro activo: «Tarifa Regular», servicio 1 (Pesaje), $16.806,72 + IVA 19 % = **$20.000**, vigente de 2001 a 2050. |
| `convenio` | 3 registros: el 0 («noaplica»), el 1 del cliente 70 (Colmotores, excluido por regla, vencido en 2016) y el 2 del cliente 161 (vencido en 2014). Solo agrupaban tarifas de báscula por vehículo (`vehiculo_x_convenio`). **No hay convenios vigentes.** |
| `servicio` | 1 Pesaje, 2 Bodegaje, 3 Patios. En los recibos de los últimos 6 meses solo aparece el 1. |
| `cron.php`, `listardepositosfacturar.php`, `facturarciigo.php` | El legacy **no calcula el valor del almacenamiento**: el cron solo genera las fechas de los períodos (`cliente.dias_facturacion`, fin + 3 de plazo) y Facturación **digita el valor** (`facturarciigo.php:87-95`, campo libre en `:288-292`). La pantalla muestra el CIF y la TRM solo como referencia. Lo mismo dice RN-051 de `LEGACY_BUSINESS_RULES.md`. |
| `cliente.dias_facturacion` | 15 días: 1.025 clientes, 30: 24, 180: 3 y 360: 6. Ya se cargó como ciclo de facturación de cada cliente (`Days15`, `Days30`, `Days180`, `Days360`). Los 128 depósitos vivos son de 24 clientes: 92 depósitos con ciclo de 15 días y 36 con ciclo de 180. |
| Recibos de báscula (`recibo`/`detallerecibo`, 2023-12-10 a 2024-06-07) | Servicio 1: 4.313 cobros de $16.807 + $3.193 de IVA = $20.000, y 1.949 en $0 (repesajes). |

### 1.1 Lo que se deduce de las facturas de almacenamiento (últimos 6 meses)

Hay 2.486 facturas de almacenamiento con estado `facturada` (`facturaciigo`, facturadas entre 2023-12-11 y 2024-06-07). Se compararon con el CIF del ingreso en pesos (`ingreso.preciomercancia` × la TRM vigente el día del ingreso):

- **No hay una fórmula única:** son valores digitados.
  - El % sobre el CIF va del 0,04 % (decil 1) al 0,93 % (decil 9).
  - Los valores más repetidos son importes fijos con IVA incluido: $50.000 (263 veces), $110.075 = $92.500 + IVA (189 veces, primer período de camiones de 33 t), $102.879 (102), $154.622 (80) y $292.634 (66).
- **Primer período:** la mediana es el **0,351 % del CIF con IVA incluido**, que equivale al 0,295 % + IVA (1.577 facturas).
- **Renovaciones:** la mediana es el 0,088 % (779 facturas). El valor más repetido es **$50.000**, que en los depósitos vivos es el último valor facturado de 17 de las 55 renovaciones.
- **Depósitos vivos (128):**
  - 24 sin período facturado;
  - 49 con un solo período;
  - 55 con renovaciones.
  - Los 36 depósitos del ciclo de 180 días (clientes 464 y otro) se facturaban en torno al 0,35 % del CIF con IVA por período (≈ $560.000 a $630.000).

Extractos (fuera de git): `db_legacy/trabajo/extractos/20_facturas_almacenamiento_6m.csv` y `21_ultimo_periodo_vivos.csv`, con sus consultas en `db_legacy/trabajo/consultas/`.

### 1.2 Restricción de la v2 que condiciona el mapeo (DEF-MIG-004)

**Los depósitos migrados no tienen CIF ni moneda.**
- El CSV de depósitos (F6-03) no trae esas columnas.
- `WarehouseStorage.CreateMigrated` no las recibe.
- Ninguna pantalla ni endpoint permite fijarlas en un depósito confirmado.

**Consecuencias:**
- Cualquier fórmula sobre el CIF (`PERCENTAGE_OF_VALUE` o la prorrateada) da $0 y el período cae al mínimo.
- `PER_VEHICLE` y `PER_CARGO_UNIT` también dan 0, porque los migrados no tienen camiones ni unidades de carga.
- Solo `FIXED` y `PER_UOM` (por la cantidad en stock) producen un importe distinto del mínimo.

## 2. Propuesta (se carga por el API, con el Admin, solo después del «sí»)

| # | Qué | Endpoint | Valores |
|---|---|---|---|
| T1 | **Tarifa base de almacenamiento, importación.** Aplica a todos los clientes sin convenio. | `POST /service/{ALMACENAMIENTO}/pricing-rules` | Fórmula `PERCENTAGE_OF_VALUE`, modalidad `IMP001`, sin producto. `percentage = 0.295` (0,351 % con IVA, la mediana del primer período del legacy). `minimum = 50000` con `minimumIncludesVat = true`: $50.000 con IVA, el valor más repetido del legacy. Sin `minimumThreshold`. |
| T2 | **Mínimo de almacenamiento, importación.** Es el respaldo si la regla no se puede evaluar. | `PUT /service/{ALMACENAMIENTO}/minimum-values/{IMP}` | `amount = 50000`, `includesVat = true`, activo. |
| T3 | **Báscula.** | `POST /service/{BASCULA}/assign-tax` (IVA) y `POST /service/{BASCULA}/prices` | IVA 19 %; precio base $16.806,72 desde 2026-10-01: $20.000 con IVA, igual que la `tarifa` 1 del legacy. |
| T4 | **Guía de salida.** El legacy no la cobraba; por decisión del usuario, la v2 sí la cobra. | `POST /service/{GUIA_SALIDA}/prices` | ~~Precio base $0~~ → **precio base $15.000** desde 2026-10-01. El servicio no tiene IVA asignado: la factura es de $15.000. |
| T5 | **Ciclos de facturación por cliente.** | Ninguno: ya los cargó el importador de clientes. | `dias_facturacion` → `Days15`/`Days30`/`Days180`/`Days360`; plazo de pago de 30 días; preferencia `PerService`. |
| T6 | **Convenios por cliente.** | Ninguno. | El legacy no tiene convenios vigentes y los importes por cliente se digitaban a mano sin una regla estable (§1.1). |

### 2.1 Resultado esperado al ejecutar `open-billing` (OK-5)

- **127 depósitos «Opened»**, con el primer período desde el **2026-10-01**:
  - ciclo de 15 días: hasta el 16/10/2026;
  - ciclo de 180 días: hasta el 30/03/2027.
- **Importe de cada período:** **$50.000** ($42.016,81 + $7.983,19 de IVA). Es el mínimo de T1, porque los migrados no tienen CIF (DEF-MIG-004).
- **El depósito BA0589 (v2 `2024BA00017`)** ya tiene su período abierto en $0. Fue la prueba de FA-MIG-008 «antes de las tarifas», y `open-billing` lo omitirá («Skipped», ya tiene períodos). Se usará para la prueba de anulación de E19.
- **Facturas nuevas en la v2** (no migradas, con CIF): el primer período cobra el 0,295 % + IVA del CIF, con un piso de $50.000.

## 3. Lo que no se puede mapear

| Concepto del legacy | Motivo |
|---|---|
| **Importe real del almacenamiento por depósito** | Era digitado (`facturarciigo.php`); no hay regla que reproducir. Con DEF-MIG-004 los migrados solo pueden cobrar el mínimo, un importe fijo o un importe por cantidad. |
| **Tarifa de renovación más baja que la del primer período** (mediana del 0,088 % frente al 0,351 %) | `PERCENTAGE_OF_VALUE` cobra el mismo % en cada período, y la v2 no distingue el primer período de las renovaciones en la regla. Queda como duda de negocio para el cliente. |
| **Importes fijos por camión del primer período** ($110.075, $102.879…) | No se ven en el legacy como regla, sino como valores repetidos. `PER_VEHICLE` no sirve para los migrados, que no tienen camiones. |
| **Ciclo de 180 días con ≈ 0,35 % del CIF** (36 depósitos vivos) | Por DEF-MIG-004 cobrarán $50.000 cada 180 días, muy por debajo de los ≈ $600.000 del legacy. Es aceptable para una prueba, pero no para el corte real. |
| **Exportación e inspección** | El dump no tiene depósitos de esas modalidades (todos los ingresos activos son «Entrada por Importación»). Sus mínimos quedan en $0, como están sembrados. |
| **Montacargas** | No existe en el legacy. |
| **Servicios «Bodegaje» y «Patios»** | Están en el catálogo, pero no se cobraron en los últimos 6 meses. |
| **Convenios 1 y 2** | Uno es de Colmotores (excluido) y el otro está vencido desde 2014; además, eran de báscula. |

## 4. Alternativa (solo si el usuario la prefiere a T1–T2)

Convenios `FIXED` por cliente con el último valor de renovación de sus depósitos vivos; por ejemplo, el cliente 464 (ciclo de 180 días) con ≈ $600.000 por período. Acerca el importe de la prueba al del legacy, pero:

- es una aproximación hecha a mano;
- un `FIXED` cobra lo mismo a todos los depósitos del cliente, sin importar su tamaño;
- habría que repetirla en el corte real.

Se recomienda T1–T2 y corregir DEF-MIG-004 antes del corte real.

## 5. Carga realizada (2026-10-06, con el Admin y por el API)

| # | Petición | Resultado |
|---|---|---|
| T1 | `POST /service/a9c0d1e2-…(ALMACENAMIENTO)/pricing-rules`: `PERCENTAGE_OF_VALUE`, `IMP001`, `percentage = 0.295`, `minimum = 50000`, `minimumIncludesVat = true` | 200; regla `0ef5689b-829a-4246-a5f3-d584f29b2d25` |
| T2 | `PUT /service/a9c0d1e2-…/minimum-values/e8f9a0b1-…(IMP)`: `amount = 50000`, `includesVat = true`, activo | 200 |
| T3 | `POST /service/f8b9c0d1-…(BASCULA)/assign-tax` (IVA) y `POST …/prices`: `basePrice = 16806.72`, desde 2026-10-01 | 200 y 200; precio `fb757b0d-a6b8-4d18-b30d-21ebfc45abed` |
| T4 | `POST /service/d2f3a4b5-…(GUIA_SALIDA)/prices`: `basePrice = 15000`, desde 2026-10-01 | 200; precio `578d2be8-1001-4b66-b916-b0e46aff051d` |

**`open-billing`** (sin ids): **127 Opened**, 0 Skipped y 0 Failed, en 1,33 s.
- BA0589 (`2024BA00017`) no entra en la lista: ya tenía período desde la prueba de FA-MIG-008 «antes» y después se anuló en E19.
- Todos los períodos empiezan el **2026-10-01**: 92 terminan el 16/10/2026 (ciclo de 15 días, límite 19/10) y 36 el 30/03/2027 (ciclo de 180 días, límite 02/04/2027).
- Cada factura es de **$42.016,81 + $7.983,19 de IVA = $50.000**, con el cargo `MINIMUM_VALUE`, como se previó en §2.1 (DEF-MIG-004).

**Cobros verificados en la operación nueva:**
- báscula: $16.806,72 + $3.193,28 de IVA = **$20.000**;
- guía de salida: **$15.000** sin IVA.
