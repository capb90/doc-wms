# Informe de la fase 4 del staging limpio: reinicio, carga y configuración en staging

> **Fecha:** 2026-10-27, de 11:56 a 13:50 (hora de Colombia). **Ejecutor:** agente (Opus 5.5), con el «sí» del usuario en cada paso. **R:** 2026-10-27; corte simulado 2026-10-26 (S3).
> **Plan:** `planes/plan-cerrado-staging-limpio-legacy-2026-10-27.md` §5 (`DEC-043`). **Referencias:** `informe-staging-limpio-fase-1.md` y `informe-staging-limpio-fase-3.md`.
> **Partida:** BE `911399c` en `develop`, limpio; docs `7e4c568` en `main`, limpio. En staging, BE `911399c` / FE `33fbeba` (fase 13 del plan P1, cerrada). Sin cambios de código ni despliegue de código.
> **Datos personales:** el informe lleva conteos, números de depósito y códigos de la v2. Las salidas de los scripts y del API están fuera de git, en `db_legacy/trabajo/evidencias/v4/staging/`.
> **Secretos:** no se abrió ningún `.env*`. Los scripts de carga y de cuentas los corrió el usuario; leen la contraseña del Admin de `db_legacy/trabajo/.admin-staging.local` y no la imprimen. Las llamadas del agente al API usaron la sesión del Admin que el usuario abrió en el navegador integrado. Las credenciales S3 se comprobaron solo por su longitud.

## Veredicto

**Fase 4: hecha, sin convenios ni `open-billing`** (S11). Facturación no ha devuelto `propuesta-convenios-v1-validada.xlsx`, así que esa parte queda para la fase 4b.

- **Base recreada** con las 19 migraciones del repo, y el Admin que crea `Bootstrap`.
- **Carga del legacy idéntica a la fase 1:**
  - las 12 entidades tienen los mismos conteos y los mismos mensajes de rechazo, uno por uno;
  - la conciliación da 133 «Ok»;
  - los conteos de la base son iguales tabla por tabla.
- **Tarifas idénticas al ensayo de la fase 3:** T1 (la base, porque Facturación no fijó otra), T2 a T4 y las cinco de montacargas.
- **Respaldos:** `local-staging` y `s3-externo` creados y probados. El fallo provocado quedó `PartiallySucceeded` y el usuario confirmó que llegó el correo.
- **Cuentas:** las 5 `operario.*`, con cambio de contraseña al entrar. No hay ninguna `qa.*`.
- **Verificación de solo lectura:**
  - sin operaciones, facturas ni convenios;
  - nada `PRAC-` ni `QA-`;
  - en pantalla, los 128 depósitos confirmados y el `2022BA00002` con plazo de 60 días.
- **Respaldo «listo para operarios v2»:** corrida `bf7bf952`, `Succeeded` en los dos destinos.
- **Defectos de la herramienta:** ninguno.

## 1. Pasos y tiempos

| # | Paso | Resultado | Hora / tiempo |
| --- | --- | --- | --- |
| 1 | Inventario de solo lectura | 3 contenedores arriba (`wms-api:staging`, `caddy:2`, `postgres:18.0`). Volúmenes `wms-staging_pgdata`, `_caddy_data` y `_caddy_config`. Disco: 70 GB libres de 77. Base de 56 MB con 19 migraciones y 6 roles. Destinos `local-staging` y `s3-externo` activos. 1 archivo subido. `/opt/wms/backups` con 153 MB | 11:56 |
| 2 | Respaldo «antes del reinicio» | Corrida `b88fdf98`, `Succeeded` en los dos destinos: `wms_20261027_115925_b88fdf98.dump` (4,59 MB) y `uploads_20261027_115925_b88fdf98.tar.gz`, en `/opt/wms/backups/2026/10/` y en `s3://s3-externo/staging/2026/10/` | 11:59, 1 s |
| 3 | Lo que se pierde | Los conteos del §2. El «sí» del usuario autorizó el paso 4 | 12:02 |
| 4 | Recrear la base | `docker compose down` sin `-v` y `docker volume rm wms-staging_pgdata`. El archivo subido se movió a `/opt/wms/data/uploads-antes-reinicio-20261027`, y `uploads` se volvió a crear vacía, con dueño 1654 (desviación 2). `caddy_data`, `caddy_config`, `/opt/wms/data/keys` y `/opt/wms/backups` no se tocaron | 12:08, 1,1 s |
| 5 | Base y API | `dbup` (12 s); `migrate` con `staging.sql` (6 s): **19 migraciones** y 6 roles; `up` (3 s). El script idempotente se regeneró antes en local y dio el mismo SHA-256 que el de la fase 13. Log: «Bootstrap admin 'admin' creado…». Verificación en SQL de lectura: un solo usuario, `admin`, con `must_change_password = true`; 0 depósitos, terceros, facturas y destinos; 1 producto («Contenedor Vacío»); `GUIDE_CODE_TYPE` = `QR`. El usuario cambió la contraseña del Admin | 12:15, 21 s |
| 6 | Cargar los datos | `cargar-legacy.sh`, corrido por el usuario: hashes del v4 12/12 OK, 25 respuestas 200, estado 0. Comparación en el §3 | 44,7 s (local: 12,8 s) |
| 7 | Tarifas | `cargar-tarifas-convenios.sh --tarifas`, corrido por el usuario: 20 respuestas 200, estado 0. `tc-tarifas-resumen.json` es **idéntico** a `f3-tarifas-resumen.json` de la fase 3, incluso en los ids sembrados. Sin hoja validada, `--convenios --apertura` quedan para la 4b | 7,3 s (local: 1,2 s) |
| 8 | Respaldos | §4 | 13:30 |
| 9 | Cuentas | `crear-cuentas-operarios-staging.sh`, corrido por el usuario: las 5 cuentas con 201 y el inicio de sesión con la temporal pide el cambio. §5 | 13:46, 6 s |
| 10 | Verificación de solo lectura | §6 | 13:48 |
| 11 | Respaldo «listo para operarios v2» | Corrida `bf7bf952`, `Succeeded`, 3,98 MB: `/opt/wms/backups/2026/10/wms_20261027_134951_bf7bf952.dump` y `s3://s3-externo/staging/2026/10/wms_20261027_134951_bf7bf952.dump`, con su `uploads_…tar.gz` | 13:49, 1 s |

Staging estuvo sin servicio de 12:08 a 12:15.

## 2. Lo que se perdió con el reinicio (paso 3)

Todo está en la corrida `b88fdf98`.

| Qué | Antes del reinicio |
| --- | --- |
| Depósitos | 137: 128 migrados con la herramienta del 6/10 y 9 creados en staging |
| Facturas | 252: 230 en Borrador, 2 aprobadas y 20 pagadas |
| Operación | 28 entradas, 18 ciclos de báscula, 7 órdenes de cargue, 5 guías, 111 levantes, 1 uso de montacargas, 228 períodos y 222 movimientos |
| Convenios | 2 activos |
| Usuarios | 11: `admin`, 5 `operario.*` y 5 `qa.*` |
| Maestros creados en staging | 6 terceros, 21 vehículos, 7 conductores y 3 productos |
| Datos de QA | Con `QA-`: 4 depósitos, 6 terceros, 6 conductores y 6 órdenes. La búsqueda por texto no encontró nada marcado `PRAC-` |
| Archivos subidos | 1 (368 KB) |

## 3. Carga del legacy frente a la fase 1 (paso 6)

- **`carga-resumen.tsv`:** igual al de la fase 1 en entidades, filas, creados, actualizados, omitidos, errores y en la igualdad entre la simulación y el firme. Solo cambian los tiempos.
- **Respuestas en firme:** las 12 tienen **las mismas listas de rechazo** que en local, mensaje por mensaje, y los mismos campos escalares. Los rechazos por entidad son 7, 0, 0, 1, 0, 0, 2, 111, 8, 1, 0 y 18.
- **Conciliación:** 133 Ok, 0 Difference, 0 NotMigrated y 0 errores.
- **Conteos de la base** (SQL de lectura, paso 10), iguales a la tabla del §3 del informe de la fase 1:

| Tabla | Staging | Fase 1 |
| --- | --- | --- |
| Terceros / roles / configuraciones de facturación | 1.389 / 2.449 / 1.053 | Igual |
| Vehículos / conductores | 10.393 / 4.361 | Igual |
| Embalajes / cuadrillas / ciudades / ubicaciones | 61 / 7 / 1.774 / 9 | Igual |
| Productos | 1.640 | Igual |
| Depósitos / productos de depósito / servicios / movimientos / levantes | 128 / 133 / 128 / 202 / 107 | Igual |
| `legacy_id_map` / contactos / `legacy_import_batches` | 18.284 / 0 / 24 | Igual |
| `audit_logs` | 21.604 | 21.582 antes de las tarifas. La diferencia sale de las tarifas, los destinos de respaldo y las 5 cuentas |

- **Depósitos:** los 128 están migrados, tienen `legacy_year` y forman 128 claves (número, año) distintas. Todos tienen `billing_start_date = 2026-10-27`, es decir, R.
- **Prórroga (C7):** el `2022BA00002` (BA4575, 2022) tiene plazo de 60 días. El API de abandono da 67 depósitos con saldo por nacionalizar: 66 con 30 días y 1 con 60, igual que la fase 1. Los 67 están «En abandono» por la fecha de 2024.

## 4. Respaldos (paso 8; §13 del plan P1, pasos 4 a 7)

- Los pasos 1 a 3 (bucket, clave y configuración) siguen como los dejó la fase 13. Las dos credenciales llegan al contenedor: 20 y 40 caracteres, verificadas sin mostrarlas.
- **Destinos:** `local-staging` (Local, `/opt/wms/backups`) y `s3-externo` (S3, bucket `s3-externo`, prefijo `staging`, `us-east-2`). Los dos dieron `success: true` en la prueba: escribieron y borraron un archivo.
- **Corrida `29433cd2`:** `Succeeded`, con los dos destinos en `Succeeded` (`wms_20261027_133038_29433cd2.dump`, 3,97 MB).
- **Fallo provocado:**
  - destino temporal `prueba-fallo-s3-inexistente`, apuntando a un bucket que no existe;
  - la corrida `20dd2306` quedó `PartiallySucceeded`: `local-staging` y `s3-externo` en `Succeeded`, y el temporal en `Failed` («The specified bucket does not exist»);
  - el log registra «Email enviado a 1 destinatarios: [WMS] Falló el respaldo del 27/10/2026» y el aviso en la aplicación al Admin. **El usuario confirmó que llegó el correo**;
  - el temporal se borró (204). Quedan activos solo `local-staging` y `s3-externo`.

## 5. Cuentas (paso 9)

| Usuario | Rol | Activa | Cambio de contraseña al entrar | Correo `capb.dev+<usuario>@gmail.com` |
| --- | --- | --- | --- | --- |
| `operario.vigilancia` | Operario vigilancia | Sí | Sí | Sí |
| `operario.bascula` | Operario báscula | Sí | Sí | Sí |
| `operario.bodega` | Operario bodega | Sí | Sí | Sí |
| `operario.comext` | Comercio exterior | Sí | Sí | Sí |
| `operario.facturacion` | Facturación | Sí | Sí | Sí |

- Además está `admin`, con la contraseña que maneja el usuario. **No hay ninguna cuenta `qa.*`.**
- Las contraseñas temporales están solo en `db_legacy/trabajo/credenciales-operarios-staging.local.md` (0600).
- Las del staging anterior se movieron a `credenciales-operarios-staging-antes-reinicio.local.md`.

## 6. Verificación de solo lectura (paso 10)

- **`deploy-staging.sh smoke`:** frontend 200, fallback de la SPA 200, login inválido 400 y CORS con el origen exacto.
- **SQL de lectura (`BEGIN TRANSACTION READ ONLY … ROLLBACK`):**
  - entradas, ciclos, pesajes, órdenes de cargue, guías, usos de montacargas y recepciones: **0**;
  - facturas, períodos de almacenamiento y convenios: **0**. La apertura y los convenios quedan para la 4b;
  - terceros, conductores, depósitos y productos con `PRAC-` o `QA-`: **0**;
  - 6 usuarios, 2 destinos activos y 3 corridas de respaldo.
- **En pantalla, con la sesión del Admin:**
  - el tablero de depósitos muestra **128 «Confirmado»** y 0 en Borrador. Se revisaron más de diez depósitos migrados (`2022BA00001`, `2022BA00002`, `2023BA00008` a `2023BA00020`), con su importador, producto, cantidad y carta porte;
  - en «Abandono y prórrogas», el **`2022BA00002`** aparece con ingreso el 19/12/2022, plazo de **60 días** y «En abandono».
- **Un convenio en pantalla:** no aplica, porque no hay convenios hasta la 4b.

## 7. Desviaciones

1. **Sin convenios ni `open-billing`** (S11): no hay hoja validada. Los depósitos migrados no tienen factura de almacenamiento hasta la 4b, y la tarifa base es T1 (S4).
2. **Carpeta `uploads` nueva y vacía.** S9 dice mover los archivos subidos. El agente volvió a crear `/opt/wms/data/uploads`, vacía y con dueño 1654, porque el API escribe ahí (montaje `Storage:Local:BasePath`). Se hizo dentro del «sí» del paso 4, que lo nombraba.
3. **Paso 8:** los pasos 1 a 3 del §13 del plan P1 no se repitieron, porque el bucket, la clave y la configuración ya estaban en el servidor desde la fase 13. Solo se comprobó que las credenciales llegan al contenedor.
4. **Paso 9:** la primera verificación encontró 0 cuentas, porque el script todavía no se había corrido. El usuario lo corrió después de mover el archivo de credenciales anterior, y la verificación se repitió.
5. **`__EFMigrationsHistory`** usa la columna `migration_id`, no `MigrationId`. Solo afecta a las consultas manuales.

## 8. Fuera de alcance (anotado, sin actuar)

- **Fecha en las tarjetas del tablero de depósitos:** las tarjetas de los migrados muestran 27/10/2026, mientras «Abandono y prórrogas» muestra el ingreso del legacy (19/12/2022 en el `2022BA00002`). No se investigó qué fecha muestra la tarjeta (alta en la v2 o inicio de facturación). Conviene revisarlo antes de que los operarios lo reporten.
- **El respaldo «listo para operarios» de `DEC-042`** (`wms_20261007_020011_a564692e.dump`) ya no es el punto de vuelta: lo reemplaza `bf7bf952`. Los respaldos viejos siguen en `/opt/wms/backups` (S9).

## 9. Estado que queda

- **Staging:** BE `911399c` / FE `33fbeba`, con 19 migraciones, los datos del legacy (v4, corte en el 2026-10-26), las tarifas T1 a T4 y de montacargas, el Admin, las 5 cuentas `operario.*`, y los respaldos diarios en `local-staging` y `s3-externo`. Sin convenios, sin `open-billing` y sin datos de QA ni de práctica.
- **Punto de vuelta para repetir las pruebas:** la corrida `bf7bf952`.
- **Fase 4b:** cuando Facturación devuelva la hoja validada (§5.1 del plan).
- **En `db_legacy/trabajo/`, fuera de git:**
  - `evidencias/v4/staging/`, con las salidas de los scripts y los archivos `paso1` a `paso11`;
  - `credenciales-operarios-staging.local.md` (nuevo) y `credenciales-operarios-staging-antes-reinicio.local.md`.
- **Navegador integrado:** se cerró la pestaña al terminar.
