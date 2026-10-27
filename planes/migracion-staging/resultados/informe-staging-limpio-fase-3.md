# Informe de la fase 3 del staging limpio: tarifas, convenios y apertura de la facturación en local

> **Fecha:** 2026-10-27 (hora de Colombia). **Ejecutor:** agente (Opus 5.5). **R:** 2026-10-27; corte simulado 2026-10-26 (S3).
> **Plan:** `planes/plan-cerrado-staging-limpio-legacy-2026-10-27.md` §4 (`DEC-043`). **Referencias:** `informe-staging-limpio-fase-1.md`, `convenios-propuesta-2026-10-27.md` y `mapeo-tarifas-propuesto.md`.
> **Partida:** BE `911399c` en `develop`, limpio; docs `47681d2` en `main`, limpio. Sin cambios de código.
> **Datos personales:** el informe lleva conteos, ids del legacy, números de depósito y códigos de la v2. Las salidas del API, las exportaciones de la hoja y los recálculos están fuera de git, en `db_legacy/trabajo/` (`evidencias/v4/local/` y `convenios/ensayo/`).
> **Secretos:** no se abrió ningún `.env*`. Los scripts leen la contraseña del Admin local de `db_legacy/trabajo/.admin-migracion.local` y no la imprimen; la conexión se armó en el proceso con las variables del contenedor.

## Veredicto

**Fase 3: OK (L6 a L10), con la propuesta en lugar de la hoja validada.**

- Facturación todavía no devolvió `propuesta-convenios-v1-validada.xlsx`. Como dice el §4, paso 2, **el ensayo usa la propuesta para probar el mecanismo**: se cargan como validados los 40 clientes con porcentaje calibrado, con ese porcentaje, y la báscula sin cobro según la pista (4 clientes). La tarifa base queda en T1, porque Facturación no la fijó (S4).
- **Tarifas:** T1 a T4 y las cinco de montacargas, como S4 y `DEC-041`.
- **Convenios:** 40 cargados, uno activo por cliente.
- **`open-billing`:** 128 «Opened», 0 «Skipped» y 0 «Failed». Todos los períodos empiezan el 2026-10-27 (R).
- **Recálculo:** los 128 primeros períodos coinciden al centavo con el recálculo a mano, no solo los siete del criterio.
- **Operación nueva (OK-7):** salida completa de un depósito migrado de un cliente con convenio, y un ingreso de Solo báscula en $0 de un cliente con «Báscula sin cobro».
- **Scripts:** `cargar-legacy.sh` y `cargar-tarifas-convenios.sh` corrieron de punta a punta sobre `wms_migracion` recién recreada, en el orden de staging.
- **Defectos de la herramienta:** ninguno.
- **Desviaciones:** 6 (§8).

## 1. Preparación (L10)

| Paso | Resultado | Tiempo |
| --- | --- | --- |
| Destino del `drop` | `--dry-run` y `ConnectionStrings__DefaultConnection`: `wms_migracion` en `localhost:5433` | — |
| `dotnet ef database drop --force` | Base borrada | 3,8 s |
| `dotnet ef database update` | **19 migraciones**, igual que la fase 1 | 4,4 s |
| API local | BE `911399c`, puerto 5290, con variables de entorno. Log: «Bootstrap admin 'admin' creado». El API del usuario (5281) no estaba corriendo y no se tocó | < 30 s |
| `cargar-legacy.sh` | Las 12 entidades con **los mismos conteos de la fase 1**; cada simulación igual a su firme; conciliación 133 Ok, 0 Difference, 0 NotMigrated | 13,6 s |

La recreación hace que los scripts corran como correrán en staging: base vacía → carga → `--tarifas` → `--convenios --apertura`.

## 2. Los scripts

**`db_legacy/trabajo/staging-limpio/exportar-hoja-convenios.py <hoja.xlsx> <carpeta> [--ensayo]`.** Convierte la hoja en lo que lee el script de carga:
- `convenios.csv`: `id_cliente;porcentaje;bascula_sin_cobro;origen`, solo con las filas «Validado = sí». En ellas, «% acordado» es obligatorio y debe estar entre 0 y 100;
- `tarifa-base.csv`: `T1;0.295`, o `PRORATED;<pct>` si la pestaña «Tarifa base» trae el porcentaje de Facturación (S4);
- `sha256.txt`: los hashes de los dos archivos.
- Con `--ensayo` toma la propuesta, como se describe arriba. Ese modo es solo para local.
- Lee la hoja por los nombres de columna y no imprime nombres ni documentos.

**`db_legacy/trabajo/staging-limpio/cargar-tarifas-convenios.sh <url-api> <archivo-credencial> [--tarifas] [--convenios] [--apertura] [--hoja <carpeta>] [--ambiente] [--usuario] [--etiqueta]`.** Sin pasos, corre los tres. La carpeta por defecto es `convenios/validada/`.
- **`--tarifas`:**
  - T1: la regla base de almacenamiento, con la fórmula y el porcentaje de `tarifa-base.csv`, o T1 si ese archivo no está;
  - T2: el mínimo de importación;
  - T3: el IVA y el precio de la báscula;
  - T4: el precio de la guía;
  - montacargas: `PUT forklift-rates/{tipo}`.
  Al final guarda una fotografía de lo cargado (`<etiqueta>-tarifas-resumen.json`) para comparar local con staging.
- **`--convenios`:** verifica los hashes de la hoja exportada. Por cliente:
  - busca el número de identificación en `05_clientes.csv`;
  - consulta `GET stakeholder?search=` y se queda con los terceros cuyo número normalizado es igual, con la misma normalización del importador;
  - si no sale exactamente uno, no carga y lo informa;
  - si el cliente ya tiene un convenio activo, no carga y lo informa (D21). Si ese convenio es su propio `LEG-{id}`, lo cuenta como «ya estaba»;
  - si no, crea el convenio (S7) con su servicio de almacenamiento y, si aplica, el de báscula en $0;
  - al final comprueba que el cliente quedó con un solo activo.
  Deja el detalle en `<etiqueta>-convenios.tsv`.
- **`--apertura`:** `POST administration/legacy-import/open-billing`, con el conteo de «Opened», «Skipped» y «Failed».
- **Repetible:** lo que ya está igual se informa como «ya estaba» y no se duplica. Si hay una regla base o un precio vigente distinto, el paso se detiene.
- **Seguridad:** no imprime la contraseña ni el token.
- **Salida:** 0 si todo quedó bien; 1 si falla una petición; 2 si un convenio no se cargó o la apertura trae «Failed».

Hashes de la exportación de ensayo (`convenios/ensayo/sha256.txt`): `convenios.csv` `354521970f5b5933…` y `tarifa-base.csv` `ea6764c87a63c191…`.

## 3. Tarifas (L6)

`--tarifas`: 1,20 s. Todas las peticiones dieron 200. La segunda corrida dijo «ya estaba» en T1, T3 y T4, y no duplicó nada.

| # | Lo cargado (`f3-tarifas-resumen.json`) | S4 / `DEC-041` |
| --- | --- | --- |
| T1 | `PERCENTAGE_OF_VALUE`, `IMP001`, sin producto: `percentage 0.295`, `minimum 50000`, `minimumIncludesVat true`, `taxIncluded false` | T1, porque Facturación no fijó la tarifa base |
| T2 | Mínimo IMP001: 50.000 con IVA, activo | Igual |
| T3 | IVA asignado a `BASCULA`; precio $16.806,72 desde el 2026-10-01 | Igual |
| T4 | `GUIA_SALIDA`: $15.000 desde el 2026-10-01, sin IVA | Igual |
| Montacargas | Tractomula 220.000 · Doble troque 150.000 · Sencillo 140.000 · Turbo 110.000 · Guacal o estiba 40.000 | Igual |

## 4. Convenios (L6)

`--convenios`: 1,20 s, con **40 cargados**, 0 omitidos y 0 «no cargado».

Verificación en SQL de lectura:
- 40 convenios `Active` en 40 terceros, y **ningún tercero con más de un activo** (D21);
- todos con referencia `LEG-{id_cliente}` y el nombre «Convenio calibrado legacy {id_cliente}»;
- **almacenamiento, 40 servicios:** `PERCENTAGE_OF_VALUE_PRORATED`, `IMP001`, sin producto, `taxIncluded false`, `minimum 50000` y `minimumIncludesVat true`;
- **báscula, 4 servicios:** `FIXED` con `rate 0`, sin modalidad. Son los clientes 448, 698, 925 y 972;
- el porcentaje, el nombre y la báscula de cada convenio coinciden con `convenios.csv` en **40 de 40**.

**El id 925:** la búsqueda dio exactamente un tercero, así que el convenio se cargó (S7). Ese tercero es también el del cliente 926 del legacy, que tiene el mismo documento: el importador los asoció en uno solo. Ninguno de los dos tiene depósitos vivos, y el 926 no está en la hoja. Facturación debe saberlo al validar el 925.

Solo 21 de los 40 clientes con convenio tienen depósitos vivos. Los otros 19 están en la hoja por estar entre los 29 del 80 %.

## 5. Apertura de la facturación (L7)

`--apertura`: **128 «Opened», 0 «Skipped» y 0 «Failed»**, en 2,0 s, sin mensajes.

| Inicio | Fin | Límite | Fuente | Fórmula | Depósitos |
| --- | --- | --- | --- | --- | ---: |
| 2026-10-27 | 2026-11-11 | 2026-11-13 | Convenio | `PERCENTAGE_OF_VALUE_PRORATED` | 90 |
| 2026-10-27 | 2026-11-11 | 2026-11-13 | Tarifa base | `PERCENTAGE_OF_VALUE` (T1) | 2 |
| 2026-10-27 | 2027-04-25 | 2027-04-27 | Tarifa base | `PERCENTAGE_OF_VALUE` (T1) | 36 |

- Todos los períodos están `Open`, con su factura en Borrador. Hay 128 facturas y ninguna sin período.
- Los 90 con convenio son los depósitos de los clientes con porcentaje calibrado. Los 38 de la tarifa base son de los 3 clientes vivos sin quincenas (ids 464, 1058 y 1059), como anticipó la fase 2.

## 6. Recálculo del primer período (L8)

**Fórmula:**
- con convenio: neto = máx(% × valor en pesos × saldo / recibido; 50.000 / 1,19), más el 19 % de IVA;
- T1, por lote completo: lo mismo, sin el factor saldo / recibido.
- El valor en pesos es el valor de la mercancía × la TRM del ingreso.

Se recalcularon **los 128** y coinciden **al centavo**, en subtotal, IVA y total (`evidencias/v4/local/f3-recalculo.tsv`). Los siete del criterio:

| Depósito | Legacy | Cliente | Fórmula | % | Valor en pesos | Saldo / recibido | Mínimo | Subtotal | IVA | Total V2 | ¿Igual? |
| --- | --- | ---: | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | --- |
| `2022BA00002` (con prórroga) | BA4575 | 602 | Convenio | 0,0906 | 165.137.413,50 | 450 / 450 | No | 149.614,50 | 28.426,76 | 178.041,26 | Sí |
| `2022BA00001` | BA2355 | 842 | Convenio | 0,0524 | 992.450.530,75 | 1.200 / 1.330 | No | 469.212,70 | 89.150,41 | 558.363,11 | Sí |
| `2023BA00012` (2 productos) | BA3029 | 602 | Convenio | 0,0906 | 252.246.748,16 | 591 / 2.669 | No | 50.604,91 | 9.614,93 | 60.219,84 | Sí |
| `2024BA00039` | BA1018 | 93 | Convenio | 0,3012 | 805.855.781,47 | 1 / 865 | Sí | 42.016,81 | 7.983,19 | 50.000,00 | Sí |
| `2024BA00083` | BA1387 | 752 | Convenio | 0,2450 | 646.430.292,00 | 880 / 1.200 | No | 1.161.419,76 | 220.669,75 | 1.382.089,51 | Sí |
| `2023BA00013` (ciclo de 180 días) | BA3238 | 464 | T1 | 0,295 | 181.923.480,00 | 530 / 1.350, no aplica | No | 536.674,27 | 101.968,11 | 638.642,38 | Sí |
| `2024BA00102` | BA1448 | 1059 | T1 | 0,295 | 11.154.167,28 | 104 / 104, no aplica | Sí | 42.016,81 | 7.983,19 | 50.000,00 | Sí |

**Totales del primer período,** para compararlos en la fase 4 (`evidencias/v4/local/f3-totales-primer-periodo.tsv`):

| Grupo | Clientes | Depósitos | En el mínimo | Subtotal | IVA | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Con convenio | 21 | 90 | 20 | 18.279.085,50 | 3.473.026,12 | **21.752.111,62** |
| Tarifa base (T1) | 3 | 38 | 1 | 24.526.665,47 | 4.660.066,40 | **29.186.731,87** |
| **Total** | **24** | **128** | **21** | **42.805.750,97** | **8.133.092,52** | **50.938.843,49** |

**Por cliente con convenio** (total con IVA):

| Cliente | % | Depósitos | En el mínimo | Total | | Cliente | % | Depósitos | En el mínimo | Total |
| ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 93 | 0,3012 | 1 | 1 | 50.000,00 | | 786 | 0,2992 | 1 | 0 | 379.291,47 |
| 311 | 0,1167 | 1 | 0 | 460.991,34 | | 827 | 0,3233 | 1 | 0 | 131.690,43 |
| 448 | 0,2532 | 2 | 2 | 100.000,00 | | 842 | 0,0524 | 3 | 0 | 976.056,05 |
| 526 | 0,2356 | 2 | 0 | 1.805.949,13 | | 853 | 0,2488 | 1 | 0 | 687.950,66 |
| 581 | 0,2249 | 1 | 0 | 671.903,51 | | 879 | 0,2942 | 6 | 0 | 2.811.612,67 |
| 602 | 0,0906 | 43 | 14 | 5.400.220,22 | | 891 | 0,5696 | 1 | 0 | 220.293,64 |
| 622 | 0,2588 | 4 | 0 | 833.124,71 | | 991 | 0,4133 | 3 | 0 | 1.015.302,40 |
| 698 | 0,0889 | 1 | 0 | 180.864,72 | | 992 | 0,4944 | 7 | 1 | 699.462,28 |
| 733 | 0,1315 | 2 | 2 | 100.000,00 | | 995 | 0,3036 | 1 | 0 | 313.798,93 |
| 752 | 0,2450 | 7 | 0 | 3.605.025,22 | | 1053 | 0,3222 | 1 | 0 | 1.212.154,97 |
| 773 | 2,0048 | 1 | 0 | 96.419,27 | | | | | | |

Tarifa base: el cliente 464 tiene 36 depósitos por $27.999.160,93, el mismo total del ciclo de 180 días con T1 en el v3. El 1058 suma $1.137.570,94 y el 1059, $50.000,00.

**Ojo:** estos totales son del ensayo con la propuesta. Con la hoja validada cambian los porcentajes y, quizás, la tarifa base. La comparación de la fase 4 (o de la 4b) debe hacerse contra el ensayo local con la hoja validada (§5.1, paso 1).

## 7. Operación nueva sobre un depósito migrado con convenio (L9, OK-7)

Se hizo con el Admin, porque en local no hay cuentas por rol (fase 1). Las respuestas están en `evidencias/v4/local/f3-ok7/`.

**Salida del depósito `2024BA00089`** (legacy BA1405, cliente 581, convenio al 0,2249 %). Tenía 900 recibidos, 900 en stock y ninguno nacionalizado.

| Paso | Endpoint | Resultado |
| --- | --- | --- |
| Levante | `POST foreign-trade/imports/{id}/releases` | 200. Levante de 100 unidades con CIF de USD 1.000 y TRM manual. El depósito pasa a «Nacionalizado» |
| Orden de cargue | `POST foreign-trade/loading-orders` | 201, `2026OC00001` por 100. Stock 900, reservado 100, disponible 800 |
| Ingreso del vehículo | `POST entry-logs` (Cargue importación) | 201, con un vehículo y un conductor migrados |
| Báscula | `POST weighbridge/output/initiate` | 201. Propuesta $16.806,72 + $3.193,28 = **$20.000**; `isAgreementZero` en false, porque el 581 no tiene báscula sin cobro |
| Cobro | `POST weighbridge/output/process-payment` | 200, factura `Paid` por $20.000 |
| Tara | `POST weighbridge/cycles/{id}/weighings` | 200 |
| Guía | `GET …/dispatch-guide-preview` y `POST foreign-trade/dispatch-guides` | Propuesta de **$15.000 sin IVA**; 201, guía `2026S00001`, factura `Paid` por $15.000 |
| Cargue | `POST warehouse/loading-orders/{id}/execute` | 200. Stock 800, reservado 0, disponible 800 |
| Repesaje | `POST weighbridge/cycles/{id}/weighings` (bruto) | 200. Ciclo `Complete` y OC `Dispatched` |
| Salida | `POST entry-logs/{id}/departure` | 200 |

**Comprobaciones:**
- **Línea congelada de la guía:** recibido 900 / saldo anterior 900 / sale 100 / nuevo saldo 800, con el levante y la aceptación del paso 1. El PDF de la guía se generó (255.544 bytes).
- **Saldos finales:** recibido 900 y stock 800. Son los 100 que salieron.
- **El período de almacenamiento** del depósito sigue `Open`, con su factura en Borrador de $671.903,51. La salida no toca el período abierto.

**Solo báscula de un cliente con «Báscula sin cobro»** (cliente 698, convenio con `BASCULA FIXED 0`):

| Paso | Endpoint | Resultado |
| --- | --- | --- |
| Ingreso | `POST entry-logs` (Solo báscula) | 201 |
| Inicio | `POST weighbridge/weighing-only/initiate` | 201. Propuesta $0 con **`isAgreementZero` en true** |
| Cobro | `POST weighbridge/weighing-only/process-payment` con $0 | 200, `isZeroInvoice` en true |
| Pesaje único | `POST weighbridge/cycles/{id}/weighings` | 200. Ciclo completo |
| Factura | `GET billing/invoices/{id}` | `Paid`, total 0, **sin número**, ítem «Servicio de Báscula — Sin cobro por convenio» |
| Tiquete | `GET weighbridge/{id}/ticket/pdf` | Imprime **«SIN COBRO POR CONVENIO»** y total 0,00 |
| Salida | `POST entry-logs/{id}/departure` | 200 |

**Base al cerrar:** 131 facturas (128 de almacenamiento, más la báscula y la guía de la salida, más la báscula en $0), 1 OC, 1 guía, 2 ciclos y 108 levantes.

**Log del API:** 0 líneas `crit:` y 3 `fail:`, ninguna de la carga ni de los convenios.
- 1 viene de leer la factura de la salida con `GET weighbridge/{ciclo}/invoice`, que dio 404 (§9). La factura se leyó después con `GET billing/invoices/{id}`.
- 2 dicen que falta `DispatchGuides:VerificationKey` en el API local, así que la guía se imprimió con código de barras en lugar de QR. En staging la clave está en `.env.staging` (S8).

## 8. Criterios OK y desviaciones

| # | Criterio | Resultado |
| --- | --- | --- |
| L6 | Tarifas y convenios como S4 a S7, con un solo convenio activo por cliente | **Cumple**, con la propuesta en lugar de la hoja validada (§3 y §4) |
| L7 | `open-billing` sin «Failed», con el primer período desde R | **Cumple.** 128 «Opened», todos desde el 2026-10-27 |
| L8 | Los siete recálculos coinciden al peso | **Cumple.** Los 128 coinciden al centavo |
| L9 | La operación de OK-7 funciona de punta a punta | **Cumple**, incluida la báscula en $0 por convenio |
| L10 | Los dos scripts corren de punta a punta sobre una base recién recreada | **Cumple.** `drop` → `update` → `cargar-legacy.sh` → `--tarifas` → `--convenios --apertura` |

**Desviaciones:**
1. **Sin hoja validada.** El ensayo usó la propuesta, como permite el §4, paso 2. Para esto `exportar-hoja-convenios.py --ensayo` toma el porcentaje calibrado y la pista de báscula de los 40 clientes calibrados. Con la hoja validada se repite el ensayo local (§5.1, paso 1) antes de cargar en staging.
2. **La ruta de búsqueda de terceros es `GET stakeholder?search=`, en singular.** S7 y el prompt dicen `stakeholders`, pero esa ruta no existe; es el mismo endpoint (`StakeholderController`, `[Route("[controller]")]`). Además, `search` busca por coincidencia parcial y también en el nombre y los contactos. Por eso el script cuenta solo los terceros cuyo número, normalizado como lo hace el importador, es igual al buscado.
3. **La vigencia de los precios de báscula y guía queda desde el 2026-10-01,** la misma del mapeo aprobado (`mapeo-tarifas-propuesto.md` §5). El plan no fija otra fecha, y así los precios rigen desde antes de R.
4. **OK-7 con el Admin, no por rol:** en local no hay cuentas por rol (S8 y nota de la fase 1).
5. **El orden real de OK-7 es levante → OC → ingreso → báscula → guía → cargue → repesaje → salida.** El cargue de una importación exige la guía activa antes (`ImportGuideRules`), así que la guía va antes del cargue y no después, como en el texto del §4, paso 4.
6. **Los vehículos migrados no tienen tipo,** porque el legacy no lo trae. Báscula lo pide (H1 de `DEC-057`): el ensayo lo envió en el inicio del pesaje, como lo hará el operario en la pantalla.

## 9. Fuera de alcance (avisos)

- **`GET weighbridge/{cicloId}/invoice` da 404** («modo de pago pendiente») para un ciclo de **salida** que sí tiene su factura pagada. El handler solo busca facturas por los ingresos a depósito (`WarehouseStorageEntries`), así que no ve las de salida. No afecta la operación: la factura existe y se ve en Facturación. Vale revisar si alguna pantalla usa ese endpoint para las salidas.
- **El cliente 925 del legacy comparte el tercero con el 926** (§4). Conviene que Facturación lo sepa al validar.
- **Límite de pago del período:** fin + 2 días (11/11 → 13/11). En el ensayo del 6/10 fue fin + 3 (16/10 → 19/10). No es parte de esta fase; se anota por si Facturación pregunta.

## 10. Estado que queda

- **`wms_migracion`:** con la carga del v4, las tarifas, los 40 convenios del ensayo, la apertura y la operación de OK-7. No sirve como base de partida de la 4b: el §5.1 la recrea.
- **El API del 5290 y `wms-postgres-db`:** detenidos. **`legacy-mariadb`:** arriba.
- **En `db_legacy/trabajo/`, fuera de git:**
  - `staging-limpio/cargar-tarifas-convenios.sh` y `staging-limpio/exportar-hoja-convenios.py`;
  - `convenios/ensayo/` (`convenios.csv`, `tarifa-base.csv` y `sha256.txt`);
  - en `evidencias/v4/local/`:
    - `f3carga-*` (la carga de esta fase);
    - `f3-tarifas-*`, `f3rep-tarifas-*`, `f3-convenios*` y `f3-apertura.json`;
    - `f3-periodos-bd.tsv`, `f3-recalculo.tsv` y `f3-totales-primer-periodo.tsv`;
    - `f3-ok7/` y `api-fase3.log`.

**Para la fase 4:**
- con la hoja validada, Facturación la deja en `convenios/propuesta-convenios-v1-validada.xlsx`. Se exporta con `exportar-hoja-convenios.py <hoja> convenios/validada` y se repite este ensayo con `--hoja convenios/validada`;
- en staging, el usuario corre `cargar-tarifas-convenios.sh https://api.100-60-89-139.sslip.io/api/v1 <credencial> --tarifas`. Si no hay hoja validada ni `convenios/validada/tarifa-base.csv`, la tarifa base queda en T1 (S4);
- después, en la fase 4 o en la 4b, `--convenios --apertura --hoja convenios/validada`;
- la fotografía de tarifas de staging debe ser igual a `f3-tarifas-resumen.json`.
