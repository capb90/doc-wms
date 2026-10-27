# Informe de la fase 1 del staging limpio: conjunto v4 y carga local con la herramienta actual

> **Fecha:** 2026-10-27 (hora de Colombia). **Ejecutor:** agente (Opus 5.5). **R:** 2026-10-27; corte simulado 2026-10-26 (S3).
> **Plan:** `planes/plan-cerrado-staging-limpio-legacy-2026-10-27.md` §2 (`DEC-043`). **Referencias:** `informe-fase-1-repeticion.md` e `informe-actualizacion-fases-1-2.md` (carga del v3).
> **Partida:** BE `911399c` en `develop`, limpio; docs `0836639` en `main`, limpio. Sin cambios de código.
> **Datos personales:** el informe lleva conteos, números de depósito, ids del legacy y códigos de la v2. Los CSV, las salidas del API y los extractos están fuera de git, en `db_legacy/trabajo/` (`csv/`, `extractos/v4/` y `evidencias/v4/local/`).
> **Secretos:** no se abrió ningún `.env*`. La contraseña del Admin local se generó en `db_legacy/trabajo/.admin-migracion.local` (0600) y no se imprimió; la cadena de conexión se armó en el proceso con las variables del contenedor, sin mostrarlas.

## Veredicto

**Fase 1: OK (L1 a L5).**

- **Conjunto v4:** los 10 CSV del v3 con su hash y `11_depositos.csv` y `12_levantes.csv` regenerados con las consultas actuales del plan (prórroga y año del depósito) y el corte en el 2026-10-26.
- **Carga local:** las 12 entidades en firme con **los mismos conteos y los mismos mensajes de rechazo que el v3**. La conciliación da 133 «Ok».
- **Lo nuevo de la herramienta actual:**
  - los 128 depósitos quedan con su año (`legacy_year`);
  - el depósito con prórroga en el legacy (BA4575, 2022) la conserva, con plazo de 60 días;
  - la facturación de los 128 arranca el 2026-10-27, es decir, en R.
- **Script de carga:** `db_legacy/trabajo/staging-limpio/cargar-legacy.sh`, listo para correrlo contra staging en la fase 4.
- **Defectos de la herramienta:** ninguno.
- **Desviaciones:** 4, anotadas en el §6.

## 1. Preparación

| Paso | Resultado | Tiempo |
| --- | --- | --- |
| `legacy-mariadb` (3308) | Estaba detenido; se arrancó. La base `bodegas` está y sus conteos coinciden con el informe de la fase 1: `deposito` 9.682, `ingreso` 9.895, `producto_en_bodega` 19.109, `producto_levante` 20.523, `cliente` 1.060 y `facturaciigo` 15.777. No hubo que recargar el dump | — |
| `wms-postgres-db` (5433) | Estaba detenido; se arrancó. `wmsdb`, `wms_qa_preprod` y las bases de grabación no se tocaron | — |
| Destino del `drop` | `dotnet ef database drop --dry-run` y la variable `ConnectionStrings__DefaultConnection`: `wms_migracion` en `localhost:5433` | — |
| `dotnet ef database drop --force` | `DROP DATABASE wms_migracion WITH (FORCE)` | 1,9 s |
| `dotnet ef database update` | **19 migraciones**, de `20261001193201_InitialParityLegacy` a `20261026183022_AddLabelPrintEntry`: son todas las del repo en `911399c` (desviación 1) | 3,3 s |
| API local | BE `911399c`, puerto **5290**, con variables de entorno: conexión, `Bootstrap__*` y una llave JWT propia del proceso. Log: «Bootstrap admin 'admin' creado». El API del usuario (5281) no estaba corriendo y no se tocó | < 40 s |

**Base vacía:** sin datos de ejemplo. Solo está el producto «Contenedor Vacío»; los demás conteos de negocio están en 0 (`evidencias/v4/local/conteos-base-vacia.txt`).

## 2. Conjunto v4 (S2 y S3)

- **Los 12 CSV del v3**, verificados contra `csv/sha256-csv-fase-1-v3.txt` antes de tocar nada: 12 de 12 «OK».
- **Consultas:** se extrajeron sin editar del plan P1 a `consultas/v4/`. Frente a `consultas/v3/`:
  - las 9 de maestros son idénticas;
  - `11_depositos.sql` solo agrega `D.prorroga` (columna 22);
  - `12_levantes.sql` solo agrega `YEAR(D.fecha_deposito) AS anio_deposito` (columna 13).
- **Corte:** `aplicar_d2.py` recibe ahora la fecha (desviación 3). Con `2026-10-26`:
  - los 128 depósitos quedan con `ultimo_fin_facturado = 2026-10-26`;
  - originalmente, 104 tenían un último fin facturado entre el 2022-12-10 y el 2024-11-30, y 24 no tenían período facturado. Es lo mismo que en el v3.
- **Frente al v3:**
  - **depósitos:** 133 filas en el mismo orden, iguales celda por celda en las 21 columnas del v3, salvo `ultimo_fin_facturado` (2026-09-30 → 2026-10-26). La columna 22 trae `prorroga = 1` en 1 fila y `0` en 132. Los 128 depósitos son de importación;
  - **levantes:** las mismas 170 filas del v3 en sus 12 columnas, más `anio_deposito`: 148 de 2024, 19 de 2023 y 3 de 2022.
- **Reproducibilidad:** se exportaron dos veces y dieron el mismo hash. El desempate O-1 del `ORDER BY` lo hace total.
- **Archivos:** los dos CSV del v3 se movieron, sin borrarlos, a `csv/v3-reemplazados/`. Los hashes del v4 están en `csv/sha256-csv-v4.txt` y en `registro-csv-fase-1.md`, «Conjunto v4».
- **Tiempo de la exportación:** depósitos 14,3 s y levantes 0,3 s. En el v3, los depósitos tardaron 14,3 s.

## 3. Carga con `cargar-legacy.sh` (L1, L5)

**El script:** `cargar-legacy.sh <url-api> <archivo-credencial> [--ambiente] [--usuario] [--solo] [--etiqueta] [--sin-conciliacion]`.
- Antes de cargar, verifica los hashes del v4. Si uno falla, no carga nada.
- Por entidad, en el orden del §3.4 del plan de migración:
  - renueva la sesión del Admin;
  - corre la simulación y el firme;
  - concilia los dos resultados: deben dar los mismos conteos.
- Al final corre la conciliación de depósitos (`legacy-import/reconciliation`).
- Guarda cada respuesta, su código HTTP y un `resumen.tsv` en `evidencias/v4/<ambiente>/`.
- No imprime la contraseña ni el token: el token vive en un archivo temporal 0600.
- Se detiene si una petición no da 200. Sale con 2 si un firme difiere de su simulación o si la conciliación trae diferencias.

| # | Entidad | Filas | Creados | Asociados | Rechazados | v3 (creados / asociados / rechazados) | Sim. | Firme |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Ciudades | 1.781 | 1.774 | 0 | 7 | 1.774 / 0 / 7 | 0,11 s | 0,33 s |
| 2 | Embalajes | 67 | 61 | 6 | 0 | 61 / 6 / 0 | 0,15 s | 0,09 s |
| 3 | Cuadrillas | 7 | 7 | 0 | 0 | 7 / 0 / 0 | 0,08 s | 0,05 s |
| 4 | Ubicaciones | 9 | 9 | 0 | 0 | 9 / 0 / 0 | 0,08 s | 0,06 s |
| 5 | Clientes | 1.056 | 1.053 | 3 | 0 | 1.053 / 3 / 0 | 0,89 s | 0,66 s |
| 6 | Agencias | 78 | 74 | 4 | 0 | 74 / 4 / 0 | 0,07 s | 0,07 s |
| 7 | Transportadoras | 273 | 262 | 9 | 2 | 262 / 9 / 2 | 0,11 s | 0,11 s |
| 8 | Vehículos | 10.594 | 10.393 | 90 | 111 | 10.393 / 90 / 111 | 1,15 s | 1,08 s |
| 9 | Conductores | 4.416 | 4.361 | 47 | 8 | 4.361 / 47 / 8 | 0,51 s | 0,46 s |
| 10 | Productos | 1.778 | 1.639 | 138 | 1 | 1.639 / 138 / 1 | 0,25 s | 0,23 s |
| 11 | Depósitos (filas de producto) | 133 | 133 (128 depósitos) | 0 | 0 | 133 / 0 / 0 | 0,50 s | 0,30 s |
| 12 | Levantes | 170 | 107 | 0 | 18 | 107 / 0 / 18 | 0,24 s | 0,19 s |

- **Cada simulación dio los mismos conteos que su firme** (12 de 12).
- **Rechazos (L1):**
  - son los mismos del v3, con **los mismos mensajes, uno por uno**, en las 12 entidades;
  - sus causas son las de `informe-fase-1-repeticion.md` §4.2: dato inválido del legacy, exclusión por regla en cascada o duplicado legítimo;
  - Ubicaciones informa en su lista una línea, «Filas leídas…», igual que en el v3;
  - **la herramienta no causa ningún rechazo**;
  - los depósitos no traen advertencias: los 128 son de importación, así que la prórroga no se ignora en ninguno.
- **Tiempos (L5):**
  - carga completa con el script: **12,8 s**, con los hashes, 13 inicios de sesión, las 12 simulaciones y firmes y la conciliación;
  - simulación + firme de las 12 entidades: 7,8 s, frente a 6,3 s del v3, que no renovaba la sesión;
  - conciliación: 0,19 s, frente a 0,12 s del v3.

**Conteos de la v2 tras la carga**, frente al v3 (`evidencias/v4/local/conteos-antes-idem.txt`):

| Tabla | v4 | v3 | Diferencia |
| --- | --- | --- | --- |
| Terceros / roles / configuraciones de facturación | 1.389 / 2.449 / 1.053 | Igual | — |
| Vehículos / conductores | 10.393 / 4.361 | Igual | — |
| Embalajes / cuadrillas / ciudades / ubicaciones | 61 / 7 / 1.774 / 9 | Igual | — |
| Productos | 1.640 | Igual | — |
| Depósitos / productos de depósito / servicios / movimientos / levantes | 128 / 133 / 128 / 202 / 107 | Igual | — |
| `legacy_id_map` | 18.284 | Igual | — |
| Contactos de terceros | 0 | 0 | — |
| `legacy_import_batches` | 24 | 36 | −12. El v3 hizo una primera pasada de simulación sin maestros (12 lotes); el script no la hace |
| `audit_logs` | 21.582 | 21.592 | −10. El v3 creó las 5 cuentas `mig.*` (alta y cambio de contraseña; `ApplicationUser` es auditable). Este plan no crea cuentas de prueba (S8) |

## 4. Idempotencia (L3)

Segunda carga de clientes y depósitos con el mismo script (`--solo Customers,Deposits --etiqueta idem`), en simulación y en firme:
- **clientes:** 1.056 omitidos, 0 creados;
- **depósitos:** 133 filas con «Fila n: el depósito BA… (año) ya fue migrado.», 0 creados. El mensaje ya muestra el año.

**Los 19 conteos quedaron idénticos** antes y después, salvo `legacy_import_batches`, que sube 4 (2 simulaciones y 2 firmes). `audit_logs` no cambia (`conteos-antes-idem.txt` y `conteos-despues-idem.txt`). Tiempo: 1,0 s.

## 5. Verificación en SQL de lectura

**Depósitos vivos y conciliación (L2):**
- 128 depósitos, todos `is_migrated`, con 133 productos.
- Conciliación: **133 Ok, 0 Difference, 0 NotMigrated y 0 errores**. No hay diferencias que explicar.
- `billing_start_date = 2026-10-27` en los 128: es R (S3).

**C7: prórroga (L4).** La verdad del legacy sale de una consulta propia de lectura, `consultas/v4/verificacion/c7_c8_legacy.sql`, con la misma condición de «vivo» que F6-03:
- de los 128 vivos, 1 tiene `prorroga = 1`: el **BA4575 de 2022** (legacy 22153, importación);
- en la v2 es el **`2022BA00002`**, con la prórroga registrada y la nota «Prórroga registrada en el legacy (depósito BA4575 (2022)); migrada.»;
- los otros 127 están sin prórroga, como en el legacy: **128 de 128 coinciden**;
- **plazo**, por el API (`GET foreign-trade/abandonment?all=true`, 67 depósitos con saldo por nacionalizar): el `2022BA00002` tiene `deadlineDays = 60`, y los otros 66, 30.

**C8: números repetidos (L4).**
- **Entre los 128 vivos no hay números repetidos.** Ya lo decía el informe de la fase 1: «entre los 128 vivos sí es único». Por eso C8 no tiene casos de dos vivos con el mismo número.
- Sí tiene el riesgo que la columna del año cubre: **127 de los 128 números vivos existen también en otros años del legacy**, en depósitos cerrados.
- Se verificó:
  - los 128 depósitos de la v2 tienen `legacy_year`, ninguno nulo, y es el año de su fecha de ingreso en hora de Colombia en 128 de 128;
  - el conjunto de claves (número, año) de la v2 es **idéntico** al de los vivos del legacy: 128 claves distintas;
  - **los levantes van al depósito de su año:** los 107 pares levante–aceptación de la v2, por (número, año, levante, aceptación), son los mismos del CSV sin las 18 filas de productos agotados. Coinciden en cantidad, FOB en dólares (una vez por par) y peso bruto en **107 de 107**.

**Log del API:** 0 líneas `crit:`. Hay una línea `fail:`, que es el sondeo de la ruta de login con un cuerpo vacío, hecho antes de la carga para comprobar la ruta. Los 6 `warn` de `NotificationService` («No se han configurado emails de administradores») salen de los trabajos de fondo al arrancar, no de la carga.

## 6. Criterios OK

| # | Criterio | Resultado |
| --- | --- | --- |
| L1 | Las 12 entidades en firme, cada rechazo con su causa y ninguno por la herramienta | **Cumple.** Los mismos conteos y mensajes del v3, 0 por la herramienta |
| L2 | Conciliación sin diferencias sin explicar | **Cumple.** 133 Ok, 0 Difference, 0 NotMigrated |
| L3 | La segunda carga no duplica | **Cumple.** Clientes y depósitos: conteos idénticos |
| L4 | C7 y C8 coinciden con el legacy | **Cumple.** C7: 1 prórroga y plazo de 60 días. C8: 0 repetidos entre vivos; año en los 128 y levantes por año en 107 de 107 |
| L5 | Tiempos de cada carga anotados | **Cumple.** §1 a §4 |

## 7. Estado que queda

- **`wms_migracion`:** con la carga del v4, el Admin local y sin tarifas, convenios ni `open-billing`. Es la base de partida de la fase 3.
- **`legacy-mariadb`:** arriba, para la fase 2.
- **El API del 5290 y `wms-postgres-db`:** detenidos al cerrar la fase.
- **En `db_legacy/trabajo/`, fuera de git:**
  - `consultas/v4/` con su `verificacion/`;
  - `csv/` (v4), `csv/v3-reemplazados/` y `csv/sha256-csv-v4.txt`;
  - `extractos/v4/`;
  - `evidencias/v4/local/`;
  - `staging-limpio/cargar-legacy.sh`;
  - `.admin-migracion.local`;
  - `extractos/aplicar_d2-antes-v4.py`, el script anterior al cambio de la fecha.
