# Registro de los CSV de la fase 1

> **Conjunto vigente: el «Conjunto v4»** (al final), para el reinicio de staging de `DEC-043` (`planes/plan-cerrado-staging-limpio-legacy-2026-10-27.md`). Es el v3 con `11_depositos.csv` y `12_levantes.csv` regenerados con las consultas actuales (prórroga y año del depósito) y el corte en R − 1 = 2026-10-26.
>
> El «Conjunto v3» fue el de la fase 3 del plan de migración (2026-10-06): los 11 CSV del conjunto v2 sin cambios más el CSV de ubicaciones regenerado con la consulta corregida por DEF-MIG-008 (`informe-actualizacion-fases-1-2.md`). Los conjuntos v1, v2 y v3 quedan como histórico: **no se cargan en el reinicio.**

## Conjunto v1 (primera ejecución, reemplazado)

> **Fecha:** 2026-10-06. **Fuente:** `db_legacy/backupBodegas.sql` (MariaDB 10.1.38, «Dump completed on 2024-06-10»), cargado en el contenedor `legacy-mariadb` (MariaDB 10.11, puerto 3308).
> **Ubicación (fuera de git):** `code_workspace/db_legacy/trabajo/csv/`. Las consultas usadas están en `db_legacy/trabajo/consultas/`.
> **Formato:**
> - separador `;`, comillas dobles cuando hace falta, fin de línea LF y una fila de encabezado (`headerRows = 1`);
> - codificación **UTF-8 sin BOM**; los archivos marcados `us-ascii` no tienen caracteres fuera de ASCII y son UTF-8 válido;
> - `NULL` de MySQL → campo vacío.
> **Exportador:** `consultas/exportar.py`. Lanza la consulta con el cliente en `latin1` y decodifica **cada campo**: primero como UTF-8 y, si no es válido, como Windows-1252. Motivo: las columnas `latin1` del legacy guardan casi siempre bytes UTF-8 (leerlas como utf8mb4 da «CÃ©dula»), pero algunas tablas tienen latin1 genuino (`pais`, parte de `ciudad`, `producto` y `empresa_transporte`).
> **Reproducibilidad:** se reexportó todo el conjunto y los 12 hashes salieron idénticos (`evidencias/reexportacion.txt`).
> Los archivos del v1 están ahora en `csv/v1/`.

| # | Archivo | Entidad (endpoint) | Consulta | Filas de datos | Bytes | Codificación | SHA-256 |
|---|---|---|---|---|---|---|---|
| 1 | `01_ciudades.csv` | Ciudades (`administration/cities/import`) | `01_ciudades.sql` (nueva: el plan no trae consulta de ciudades) | 1.781 | 52.017 | UTF-8 (491 campos venían en latin1 genuino) | `58d57bb292c611d024fee7fa3b1d9bbc13e16a633f0ce44bcc00d8723bc693b8` |
| 2 | `02_embalajes.csv` | `PackagingTypes` | `02_embalajes.sql` (F6-02, sin cambios) | 67 | 761 | ASCII | `c44e848041dc8ad6266f084a43e1bb277ec4653cc9c55e3afa8ce1f427d3e29e` |
| 3 | `03_cuadrillas.csv` | `Crews` | `03_cuadrillas.sql` (F6-02, sin cambios) | 7 | 199 | ASCII | `5d2277833441797dd12848a7190b3d6bb9ca23d4078eff6345b55eecdcc7502f` |
| 4 | `04_ubicaciones.csv` | `Locations` | `04_ubicaciones.sql` (F6-02, sin cambios) | 6 | 213 | ASCII | `bfaac07bb890f04dca30e072c78e7ef4ed4eb5a4d88efa945dc10bdeee05e8e0` |
| 5 | `05_clientes.csv` | `Customers` | `05_clientes.sql` (F6-02, sin cambios; excluye los clientes 0 y 70) | 1.056 | 57.999 | UTF-8 | `7bcd278b047ed4269d46fde4acebe08bd06942439cef07df226c933cbb1d2a28` |
| 6 | `06_agencias.csv` | `CustomsAgencies` | `06_agencias.sql` (F6-02, sin cambios) | 78 | 3.910 | UTF-8 | `6b3bf4e6446f1163a20532c0b71a9f0982902555a3d3b15e3cdbd71410597577` |
| 7 | `07_transportadoras.csv` | `TransportCompanies` | `07_transportadoras.sql` (F6-02, sin cambios) | 273 | 16.565 | UTF-8 (14 campos en latin1 genuino) | `56611d3b68eadf3915671379ba25cc1b8361c9f86fd617d73426c822ce8d3143` |
| 8 | `08_vehiculos.csv` | `Vehicles` | `08_vehiculos.sql` (F6-02, sin cambios) | 10.594 | 205.392 | ASCII | `42df39558b5aecff1d97998d3a3bac9149c8f0e1e1fe144710ccca15b04f6ee3` |
| 9 | `09_conductores.csv` | `Drivers` | `09_conductores.sql` (F6-02, sin cambios) | 4.416 | 268.663 | UTF-8 (4 campos en latin1 genuino) | `d27fd28acff625ba1280f566eaa6d4a5a8ee05d592c6ac887cc67b7ccdc3377d` |
| 10 | `10_productos.csv` | `Products` | `10_productos.sql` (F6-02, sin cambios) | 1.778 (1.785 líneas: hay descripciones con saltos de línea entre comillas) | 71.507 | UTF-8 (64 campos en latin1 genuino) | `0124b8b54d0140705527f0ba76a643a57d7af426fb6835ace6ad83fc67c6c404` |
| 11 | `11_depositos.csv` | `Deposits` (y conciliación) | `11_depositos.sql` (**ajustada**) + `aplicar_d2.py` | 133 (128 depósitos) | 17.796 | ASCII | `f8651fe8bb237a39ac47414c87184e18edc0477802054da5095bc5faa11ed84e` |
| 12 | `12_levantes.csv` | `Releases` | `12_levantes.sql` (**ajustada**) | 118 | 12.467 | ASCII | `dfbec8858b9327345257b31dddbb2fde2822191a6fcf61569441f5099287014f` |

### Diferencias de las consultas ajustadas (v1)

**`11_depositos.sql`**, frente a F6-03 del plan (la original está en `11_depositos_original.sql`):
1. `saldo = ingresan − salen`, con una consulta externa sobre la del plan (el plan la deja en `NULL`).
2. `trm_ingreso` = `tasa_cambio.valor` vigente en `DATE(ingreso.fechahora_ingreso)`, como en `kardex.php:227`:
   - solo registros no eliminados y con valor > 0;
   - si hay varios, primero el de `ECU` y luego el más reciente.

   Los 128 depósitos tienen TRM.
3. `modalidad` sale como el código de la v2 (`IMP` o `EXP`) y no como `M.nom_modalidad`, porque el nombre del legacy «Entrada por Importación» no lo reconoce el importador (**DEF-MIG-001**).
4. **Ajuste D2** (`aplicar_d2.py`, sobre el CSV): `ultimo_fin_facturado = 2026-09-30` en los 128 depósitos vivos.
   - Los 128 tenían otra fecha: 104 con último fin facturado entre el **2022-12-10** y el **2024-11-30**, y 24 sin período facturado.
   - El CSV sin el ajuste se conserva en `extractos/11_depositos_sin_d2.csv`.

**`12_levantes.sql`**, frente a F6-03 del plan (la original está en `12_levantes_original.sql`):
1. Filtra por `D.id_deposito` de los depósitos vivos (ids de `_ids_vivos.sql`) y no por `D.nro_deposito`. El legacy reinicia la serie, y el filtro por número trae 819 filas en vez de 170 (**DEF-MIG-002**).
2. Una fila por levante y producto, con `SUM(PL.cantidad_levante)` agrupado por depósito, producto, embalaje y levante. Sin agrupar, el importador omite como repetidas las filas de un mismo levante repartido en varios camiones (**DEF-MIG-003**).

El resultado son 170 filas → 118.

### Archivos de trabajo que no forman parte del conjunto (v1)
Todos están en `db_legacy/trabajo/extractos/`:
- `11_depositos_original.csv`, `11_depositos_sin_d2.csv` y `11_depositos_modalidad_legacy.csv` (prueba de DEF-MIG-001);
- `12_levantes_original.csv` y `12_levantes_sin_agrupar.csv` (pruebas de DEF-MIG-002 y DEF-MIG-003);
- `20_facturas_almacenamiento_6m.csv` y `21_ultimo_periodo_vivos.csv` (análisis de tarifas D3);
- `fa-mig/` (archivos sintéticos de FA-MIG-005 y FA-MIG-006).

## Conjunto v2 (repetición de la fase 1, reemplazado por el v3)

> **Fecha:** 2026-10-06. Misma fuente (`legacy-mariadb`, base `bodegas`, dump del 2024-06-10).
> **Ubicación (fuera de git):** `db_legacy/trabajo/csv/`. Hashes en `csv/sha256-csv-fase-1-v2.txt`. El v1 se movió, sin borrarlo, a `csv/v1/` con su `sha256-csv-fase-1.txt`.
> **Consultas:** `db_legacy/trabajo/consultas/v2/`, extraídas **sin editar** de `docs/planes/paridad-legacy/plan-backend-paridad-legacy.md` (F6-02 y F6-03) por `consultas/v2/extraer_del_plan.py`. Ciudades usa la misma consulta del v1 (`01_ciudades.sql`): el plan no trae consulta de ciudades.
> **Exportador y formato:** los mismos del v1 (`consultas/exportar.py`, `;`, UTF-8 sin BOM, LF y encabezado). Ajuste D2 con `consultas/aplicar_d2.py`. El CSV de depósitos sin el ajuste está en `extractos/v2/11_depositos_sin_d2.csv`.
> **Antes de cargar en la fase 3:** `cd db_legacy/trabajo/csv && shasum -a 256 -c sha256-csv-fase-1-v2.txt`.

| # | Archivo | Entidad (endpoint) | Consulta (`consultas/v2/`) | Filas de datos | Bytes | Codificación | SHA-256 | Frente al v1 |
|---|---|---|---|---|---|---|---|---|
| 1 | `01_ciudades.csv` | Ciudades (`administration/cities/import`) | `01_ciudades.sql` | 1.781 | 52.017 | UTF-8 | `58d57bb292c611d024fee7fa3b1d9bbc13e16a633f0ce44bcc00d8723bc693b8` | Idéntico |
| 2 | `02_embalajes.csv` | `PackagingTypes` | `02_embalajes.sql` (F6-02) | 67 | 761 | ASCII | `c44e848041dc8ad6266f084a43e1bb277ec4653cc9c55e3afa8ce1f427d3e29e` | Idéntico |
| 3 | `03_cuadrillas.csv` | `Crews` | `03_cuadrillas.sql` (F6-02) | 7 | 199 | ASCII | `5d2277833441797dd12848a7190b3d6bb9ca23d4078eff6345b55eecdcc7502f` | Idéntico |
| 4 | `04_ubicaciones.csv` | `Locations` | `04_ubicaciones.sql` (F6-02) | 6 | 213 | ASCII | `bfaac07bb890f04dca30e072c78e7ef4ed4eb5a4d88efa945dc10bdeee05e8e0` | Idéntico |
| 5 | `05_clientes.csv` | `Customers` | `05_clientes.sql` (F6-02) | 1.056 | 57.999 | UTF-8 | `7bcd278b047ed4269d46fde4acebe08bd06942439cef07df226c933cbb1d2a28` | Idéntico |
| 6 | `06_agencias.csv` | `CustomsAgencies` | `06_agencias.sql` (F6-02) | 78 | 3.910 | UTF-8 | `6b3bf4e6446f1163a20532c0b71a9f0982902555a3d3b15e3cdbd71410597577` | Idéntico |
| 7 | `07_transportadoras.csv` | `TransportCompanies` | `07_transportadoras.sql` (F6-02) | 273 | 16.565 | UTF-8 | `56611d3b68eadf3915671379ba25cc1b8361c9f86fd617d73426c822ce8d3143` | Idéntico |
| 8 | `08_vehiculos.csv` | `Vehicles` | `08_vehiculos.sql` (F6-02) | 10.594 | 205.392 | ASCII | `42df39558b5aecff1d97998d3a3bac9149c8f0e1e1fe144710ccca15b04f6ee3` | Idéntico |
| 9 | `09_conductores.csv` | `Drivers` | `09_conductores.sql` (F6-02) | 4.416 | 268.663 | UTF-8 | `d27fd28acff625ba1280f566eaa6d4a5a8ee05d592c6ac887cc67b7ccdc3377d` | Idéntico |
| 10 | `10_productos.csv` | `Products` | `10_productos.sql` (F6-02) | 1.778 | 71.507 | UTF-8 | `0124b8b54d0140705527f0ba76a643a57d7af426fb6835ace6ad83fc67c6c404` | Idéntico |
| 11 | `11_depositos.csv` | `Deposits` (y conciliación) | `11_depositos.sql` (F6-03 corregida) + `aplicar_d2.py` | 133 (128 depósitos) | 19.540 | ASCII | `8c0844bb541e482b8748a1f59bfc5f1ba330314eb88232ffbc503b81b50d37ab` | 21 columnas. Las 19 primeras son iguales al v1, celda por celda. Agrega `valor_mercancia` (133 con valor) y `moneda` (`ECU` en las 133). |
| 12 | `12_levantes.csv` | `Releases` | `12_levantes.sql` (F6-03 corregida) | 170 | 17.899 | ASCII | `6cb11d9c944c50b96e3669faf3a57206624b64fb21eae9474864f88858a38b26` | Sin agrupar: 170 filas. Son las mismas filas de `extractos/12_levantes_sin_agrupar.csv` de la primera ejecución, en otro orden. El importador las agrupa en 118 (DEF-MIG-003). |

**Ajuste D2:**
- Los 128 depósitos vivos quedaron con `ultimo_fin_facturado = 2026-09-30`.
- Todos tenían otra fecha:
  - 104 con último fin facturado entre el **2022-12-10** y el **2024-11-30**;
  - 24 sin período facturado.

Es el mismo resultado del v1.

**Reproducibilidad:** se reexportó el conjunto.
- 11 de 12 hashes salieron idénticos.
- `12_levantes.csv` trae las mismas 170 filas en otro orden. El `ORDER BY` de la consulta de levantes del plan (`nro_deposito, nro_levante, nro_aceptacion, id_producto`) no desempata las filas del mismo levante y producto, una por camión.
- No afecta la carga, porque el importador agrupa esas filas y suma la cantidad.
- Sí hace que una reexportación no reproduzca el hash. Por eso la fase 3 debe cargar **el archivo congelado**, no uno reexportado.
- Para el plan se sugiere agregar `PL.id_productolevante` al final del `ORDER BY` (observación O-1 del informe de la repetición).

**Archivos de trabajo de la repetición** (`db_legacy/trabajo/extractos/v2/`, fuera del conjunto):
- `11_depositos_sin_d2.csv`;
- `11_depositos_modalidad_legacy_sim.csv`: prueba opcional de DEF-MIG-001, con «Entrada por Importación» y números de depósito con el prefijo `SIM`, solo en simulación.

## Conjunto v3 (recarga tras DEF-MIG-008, congelado para la fase 3)

> **Fecha:** 2026-10-06. Misma fuente (`legacy-mariadb`, base `bodegas`, dump del 2024-06-10).
> **Qué cambia:** solo `04_ubicaciones.csv`, exportado con la consulta corregida de F6-02 (`docs/planes/paridad-legacy/plan-backend-paridad-legacy.md`). Los otros 11 son **los mismos archivos** del v2: no se reexportaron, y su SHA-256 se verificó contra `sha256-csv-fase-1-v2.txt` (12 de 12 «OK» antes de reemplazar el de ubicaciones).
> **Ubicación (fuera de git):** `db_legacy/trabajo/csv/`. Hashes en `csv/sha256-csv-fase-1-v3.txt`. El CSV de ubicaciones del v2 se movió, sin borrarlo, a `csv/v2-reemplazados/04_ubicaciones.csv`.
> **Consultas:** `db_legacy/trabajo/consultas/v3/`, extraídas sin editar del plan con `extraer_del_plan.py`. Frente a `consultas/v2/`:
> - `04_ubicaciones.sql` es la consulta nueva (DEF-MIG-008);
> - `11_depositos.sql` y `12_levantes.sql` solo agregan un desempate al `ORDER BY` (`X.id_deposito` y `PL.id_productolevante`, observación O-1). Esos dos CSV **no** se reexportaron: se carga el archivo congelado del v2;
> - las demás son iguales.
> **Antes de cargar en la fase 3:** `cd db_legacy/trabajo/csv && shasum -a 256 -c sha256-csv-fase-1-v3.txt`.

| # | Archivo | Entidad (endpoint) | Consulta (`consultas/v3/`) | Filas de datos | Bytes | Codificación | SHA-256 | Frente al v2 |
|---|---|---|---|---|---|---|---|---|
| 1 | `01_ciudades.csv` | Ciudades (`administration/cities/import`) | `01_ciudades.sql` (v2) | 1.781 | 52.017 | UTF-8 | `58d57bb292c611d024fee7fa3b1d9bbc13e16a633f0ce44bcc00d8723bc693b8` | Idéntico |
| 2 | `02_embalajes.csv` | `PackagingTypes` | `02_embalajes.sql` | 67 | 761 | ASCII | `c44e848041dc8ad6266f084a43e1bb277ec4653cc9c55e3afa8ce1f427d3e29e` | Idéntico |
| 3 | `03_cuadrillas.csv` | `Crews` | `03_cuadrillas.sql` | 7 | 199 | ASCII | `5d2277833441797dd12848a7190b3d6bb9ca23d4078eff6345b55eecdcc7502f` | Idéntico |
| 4 | `04_ubicaciones.csv` | `Locations` | `04_ubicaciones.sql` (**F6-02 corregida, DEF-MIG-008**) | **9** | 351 | ASCII | `58e984c260aaf7aaa0ddbc28c1cf43aa2199799659f2b41f5681e5637206367d` | **Nuevo.** 7 columnas (agrega `ocupacion` e `id_bodega`). 6 filas de sección (4027 a 4032; la 4027, de Bodega 1 BA, `deshabilitado`; las demás `libre` o `Libre`) y 3 de bodega sin sección (Cobertizo, Patio 1 BA y Patio 2 BA, bodegas 18 a 20, con `id_seccion` vacío). |
| 5 | `05_clientes.csv` | `Customers` | `05_clientes.sql` | 1.056 | 57.999 | UTF-8 | `7bcd278b047ed4269d46fde4acebe08bd06942439cef07df226c933cbb1d2a28` | Idéntico |
| 6 | `06_agencias.csv` | `CustomsAgencies` | `06_agencias.sql` | 78 | 3.910 | UTF-8 | `6b3bf4e6446f1163a20532c0b71a9f0982902555a3d3b15e3cdbd71410597577` | Idéntico |
| 7 | `07_transportadoras.csv` | `TransportCompanies` | `07_transportadoras.sql` | 273 | 16.565 | UTF-8 | `56611d3b68eadf3915671379ba25cc1b8361c9f86fd617d73426c822ce8d3143` | Idéntico |
| 8 | `08_vehiculos.csv` | `Vehicles` | `08_vehiculos.sql` | 10.594 | 205.392 | ASCII | `42df39558b5aecff1d97998d3a3bac9149c8f0e1e1fe144710ccca15b04f6ee3` | Idéntico |
| 9 | `09_conductores.csv` | `Drivers` | `09_conductores.sql` | 4.416 | 268.663 | UTF-8 | `d27fd28acff625ba1280f566eaa6d4a5a8ee05d592c6ac887cc67b7ccdc3377d` | Idéntico |
| 10 | `10_productos.csv` | `Products` | `10_productos.sql` | 1.778 | 71.507 | UTF-8 | `0124b8b54d0140705527f0ba76a643a57d7af426fb6835ace6ad83fc67c6c404` | Idéntico |
| 11 | `11_depositos.csv` | `Deposits` (y conciliación) | archivo del v2 (`consultas/v2/11_depositos.sql` + `aplicar_d2.py`) | 133 (128 depósitos) | 19.540 | ASCII | `8c0844bb541e482b8748a1f59bfc5f1ba330314eb88232ffbc503b81b50d37ab` | Idéntico |
| 12 | `12_levantes.csv` | `Releases` | archivo del v2 (`consultas/v2/12_levantes.sql`) | 170 | 17.899 | ASCII | `6cb11d9c944c50b96e3669faf3a57206624b64fb21eae9474864f88858a38b26` | Idéntico |

**Reproducibilidad del CSV nuevo:** se exportó dos veces y dio el mismo hash: el `ORDER BY B.id_bodega, S.id_seccion` es total.

## Conjunto v4 (staging limpio, `DEC-043`, vigente)

> **Fecha:** 2026-10-27. **R:** 2026-10-27; corte simulado 2026-10-26 (S3). Misma fuente (`legacy-mariadb`, base `bodegas`, dump del 2024-06-10).
> **Qué cambia (S2):** `11_depositos.csv` y `12_levantes.csv`, exportados con las consultas actuales de F6-03 del plan P1 (`planes/paridad-legacy/plan-backend-paridad-legacy.md`). Los otros 10 son **los mismos archivos** del v3: no se reexportaron, y su SHA-256 se verificó contra `sha256-csv-fase-1-v3.txt` (12 de 12 «OK» antes de reemplazar los dos).
> **Ubicación (fuera de git):** `db_legacy/trabajo/csv/`. Hashes en `csv/sha256-csv-v4.txt`. Los dos CSV del v3 se movieron, sin borrarlos, a `csv/v3-reemplazados/`. El CSV de depósitos sin el corte está en `extractos/v4/11_depositos_sin_d2.csv`.
> **Consultas:** `db_legacy/trabajo/consultas/v4/`, extraídas sin editar del plan con `extraer_del_plan.py` (copiado sin cambios de `consultas/v3/`). Frente a `consultas/v3/`, las 9 de maestros son idénticas; `11_depositos.sql` agrega `D.prorroga` y `12_levantes.sql` agrega `YEAR(D.fecha_deposito) AS anio_deposito`.
> **Corte:** `consultas/aplicar_d2.py`, que ahora recibe la fecha: `aplicar_d2.py entrada.csv salida.csv 2026-10-26`.
> **Antes de cargar en staging (fase 4):** `cd db_legacy/trabajo/csv && shasum -a 256 -c sha256-csv-v4.txt`. `staging-limpio/cargar-legacy.sh` lo hace antes de cargar.

| # | Archivo | Entidad (endpoint) | Consulta (`consultas/v4/`) | Filas de datos | Bytes | Codificación | SHA-256 | Frente al v3 |
|---|---|---|---|---|---|---|---|---|
| 1 | `01_ciudades.csv` | Ciudades (`administration/cities/import`) | `01_ciudades.sql` (v2) | 1.781 | 52.017 | UTF-8 | `58d57bb292c611d024fee7fa3b1d9bbc13e16a633f0ce44bcc00d8723bc693b8` | Idéntico |
| 2 | `02_embalajes.csv` | `PackagingTypes` | `02_embalajes.sql` | 67 | 761 | ASCII | `c44e848041dc8ad6266f084a43e1bb277ec4653cc9c55e3afa8ce1f427d3e29e` | Idéntico |
| 3 | `03_cuadrillas.csv` | `Crews` | `03_cuadrillas.sql` | 7 | 199 | ASCII | `5d2277833441797dd12848a7190b3d6bb9ca23d4078eff6345b55eecdcc7502f` | Idéntico |
| 4 | `04_ubicaciones.csv` | `Locations` | `04_ubicaciones.sql` | 9 | 351 | ASCII | `58e984c260aaf7aaa0ddbc28c1cf43aa2199799659f2b41f5681e5637206367d` | Idéntico |
| 5 | `05_clientes.csv` | `Customers` | `05_clientes.sql` | 1.056 | 57.999 | UTF-8 | `7bcd278b047ed4269d46fde4acebe08bd06942439cef07df226c933cbb1d2a28` | Idéntico |
| 6 | `06_agencias.csv` | `CustomsAgencies` | `06_agencias.sql` | 78 | 3.910 | UTF-8 | `6b3bf4e6446f1163a20532c0b71a9f0982902555a3d3b15e3cdbd71410597577` | Idéntico |
| 7 | `07_transportadoras.csv` | `TransportCompanies` | `07_transportadoras.sql` | 273 | 16.565 | UTF-8 | `56611d3b68eadf3915671379ba25cc1b8361c9f86fd617d73426c822ce8d3143` | Idéntico |
| 8 | `08_vehiculos.csv` | `Vehicles` | `08_vehiculos.sql` | 10.594 | 205.392 | ASCII | `42df39558b5aecff1d97998d3a3bac9149c8f0e1e1fe144710ccca15b04f6ee3` | Idéntico |
| 9 | `09_conductores.csv` | `Drivers` | `09_conductores.sql` | 4.416 | 268.663 | UTF-8 | `d27fd28acff625ba1280f566eaa6d4a5a8ee05d592c6ac887cc67b7ccdc3377d` | Idéntico |
| 10 | `10_productos.csv` | `Products` | `10_productos.sql` | 1.778 | 71.507 | UTF-8 | `0124b8b54d0140705527f0ba76a643a57d7af426fb6835ace6ad83fc67c6c404` | Idéntico |
| 11 | `11_depositos.csv` | `Deposits` (y conciliación) | `11_depositos.sql` (**F6-03 actual**, con `prorroga`) + `aplicar_d2.py` con `2026-10-26` | 133 (128 depósitos) | 19.815 | ASCII | `e7c0a2db97b9dda42fbc0f27fcbcda0cb8b9236c8856826b70a9ffa15524d6cb` | **Nuevo.** 22 columnas. Las 21 del v3 son iguales celda por celda y en el mismo orden, salvo `ultimo_fin_facturado` (2026-09-30 → 2026-10-26). `prorroga`: `1` en 1 fila (BA4575, 2022) y `0` en 132. Los 128 depósitos son `IMP` |
| 12 | `12_levantes.csv` | `Releases` | `12_levantes.sql` (**F6-03 actual**, con `anio_deposito`) | 170 | 18.763 | ASCII | `95e7c6e35ce6841362608cf9cf7473cd602b6b4d13f9893b90728a309dae3dc5` | **Nuevo.** 13 columnas. Las mismas 170 filas del v3 en sus 12 columnas, ahora en el orden total de O-1, más `anio_deposito` (2024: 148, 2023: 19, 2022: 3) |

**Corte:**
- los 128 depósitos vivos quedaron con `ultimo_fin_facturado = 2026-10-26`;
- originalmente, 104 tenían un último fin facturado entre el **2022-12-10** y el **2024-11-30**, y 24 no tenían período facturado. Es lo mismo que en el v1 a v3.

**Reproducibilidad:** los dos CSV nuevos se exportaron dos veces y dieron el mismo hash. Con los desempates de O-1, el `ORDER BY` es total.

**Números repetidos:** entre los 128 vivos no hay números repetidos, aunque 127 de esos números existen en otros años del legacy. Con `anio_deposito`, cada levante va al depósito de su año.
