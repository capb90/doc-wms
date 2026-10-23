# Informe de la actualización de las fases 1 y 2 tras DEF-MIG-008: recarga local y redespliegue de staging

> **Fecha:** 2026-10-06 (hora de Colombia). **Ejecutor:** agente (Opus 5.5). **Prompt:** `prompt-actualizacion-fases-1-2.md`.
> **Build:**
> - BE `b31ddb6` (`develop`). Los commits de DEF-MIG-008 son `dd151ed` (corrección), `0149648` (migración `RemoveSampleSeedData`), `b8bb09e` (carpeta de llaves en staging) y `b31ddb6` (consulta de ubicaciones y ficha).
> - FE `508b91b` (`develop`). Sobre el `4799cc4` de la fase 2 solo agrega «ocultar Estadísticas del menú»; no toca la migración.
>
> **Plan:** `plan-migracion-legacy-staging.md` §3 a §5. **Referencias:** `informe-fase-1-repeticion.md` e `informe-fase-2.md`.
> **Datos personales:** el informe lleva conteos, códigos y nombres de bodegas. Las evidencias con datos reales están fuera de git, en `db_legacy/trabajo/evidencias/v3/`.
> **Secretos:** se nombran claves, nunca valores. La contraseña del Admin de staging se leyó de `db_legacy/trabajo/.admin-staging.local` sin imprimirla.

## Veredicto

**Listo para la Fase 3.**

- **A (local):** la recarga en una base limpia sin semillas de ejemplo reproduce la repetición de la fase 1:
  - 133/133 «Ok» en la conciliación;
  - 128 «Opened»;
  - el total del primer período, **exactamente $91.257.475,39**.
  Las únicas diferencias son las esperadas de DEF-MIG-008, todas explicadas (§A.4):
  - 9 ubicaciones en vez de 26;
  - 1.640 productos en vez de 1.643.
- **Conjunto v3** congelado para la fase 3: los 11 CSV del v2 con su hash y el de ubicaciones nuevo (`58e984c2…367d`).
- **B (staging):** redesplegado con el BE `b31ddb6` / FE `508b91b` **sin recrear la base**:
  - 11 migraciones, 0 ubicaciones y solo «Contenedor Vacío»;
  - el Admin y el destino de respaldo conservados;
  - llaves de DataProtection persistentes: un enlace de recuperación emitido antes de reiniciar el API sigue sirviendo después;
  - respaldos, DIAN y correo verificados.
- **DEF-MIG-008: Verificado.** No hay defectos nuevos.

---

## A. Recarga en local

### A.1 Base limpia

| Paso | Resultado | Tiempo |
|---|---|---|
| Detener el API local | Detenido (proceso del BE de la repetición). | — |
| Comprobar el destino del `drop` | Dos comprobaciones: la variable `ConnectionStrings__DefaultConnection` de `.env.migracion.local` y `dotnet ef database drop --dry-run` dicen `wms_migracion` en `localhost:5433`. | — |
| `dotnet ef database drop --force` | `DROP DATABASE wms_migracion WITH (FORCE)`. `wmsdb` sigue en el servidor y **no se le aplicó la migración** (D6). | 4,6 s |
| `dotnet ef database update` | **11 migraciones**, de `20261001193201_InitialParityLegacy` a `20261007030137_RemoveSampleSeedData`. | 4,2 s |
| Arranque del API (5291) | Con el BE `b31ddb6` y `.env.migracion.local`. `Bootstrap admin 'admin' creado`. Login del Admin: 200. | < 30 s |

**La base nueva no trae los datos de ejemplo:**
- `warehouse_locations`: **0** (antes, 20 sembradas).
- `products`: **1**, «Contenedor Vacío» (antes, 5: los 4 de ejemplo y Contenedor Vacío).
- El resto del catálogo está: los 6 roles del sistema, 5 roles de negocio, 4 modalidades, 5 servicios y 10 unidades de medida.
- Las cuentas `mig.*` se recrearon por el API (`POST user`) con las contraseñas de `credenciales-migracion-local.local.md`, y se les quitó el cambio obligatorio con `auth/change-password`, como en la repetición.

### A.2 Conjunto de CSV v3

- **Los 12 CSV del v2** se verificaron contra `sha256-csv-fase-1-v2.txt` antes de tocar nada: **12 de 12 «OK»**.
- **Ubicaciones:** se exportó **solo** este CSV, con la consulta nueva de F6-02, extraída sin editar del plan (`consultas/v3/04_ubicaciones.sql`). El CSV del v2 se movió, sin borrarlo, a `csv/v2-reemplazados/`.
  - **9 filas** con 7 columnas: **6 de sección** (4027 a 4032; la 4027, de Bodega 1 BA, `deshabilitado`) y **3 de bodega sin sección** (Cobertizo, Patio 1 BA y Patio 2 BA, bodegas 18 a 20), con `ocupacion`.
  - Exportación en 0,14 s. Se exportó dos veces y dio el mismo hash.
- **Consultas del plan frente a las del v2:** solo cambian la de ubicaciones y el desempate del `ORDER BY` de depósitos y levantes (observación O-1). Esos dos CSV no se reexportaron: se usa el archivo congelado.
- **Conjunto v3 congelado para la fase 3:** los 11 del v2 sin cambios y el de ubicaciones nuevo. Registro completo en `registro-csv-fase-1.md`, «Conjunto v3»; hashes en `csv/sha256-csv-fase-1-v3.txt`.

| Archivo | Filas | SHA-256 |
|---|---|---|
| `04_ubicaciones.csv` (**nuevo**) | 9 | `58e984c260aaf7aaa0ddbc28c1cf43aa2199799659f2b41f5681e5637206367d` |
| Los otros 11 | Las del v2 | Los del v2, sin cambios |

### A.3 Carga completa

Orden del §3.4: una primera pasada de simulación sin maestros y luego el firme, cada entidad precedida de su simulación.

| # | Entidad | Filas | Creados | Asociados | Rechazados | Repetición (creados / asociados / rechazados) |
|---|---|---|---|---|---|---|
| 1 | Ciudades | 1.781 | 1.774 | 0 | 7 | 1.774 / 0 / 7 |
| 2 | Embalajes | 67 | 61 | 6 | 0 | 61 / 6 / 0 |
| 3 | Cuadrillas | 7 | 7 | 0 | 0 | 7 / 0 / 0 |
| 4 | **Ubicaciones** | **9** | **9** | 0 | **0** | 6 / 0 / 0 |
| 5 | Clientes | 1.056 | 1.053 | 3 | 0 | 1.053 / 3 / 0 |
| 6 | Agencias | 78 | 74 | 4 | 0 | 74 / 4 / 0 |
| 7 | Transportadoras | 273 | 262 | 9 | 2 | 262 / 9 / 2 |
| 8 | Vehículos | 10.594 | 10.393 | 90 | 111 | 10.393 / 90 / 111 |
| 9 | Conductores | 4.416 | 4.361 | 47 | 8 | 4.361 / 47 / 8 |
| 10 | **Productos** | 1.778 | **1.639** | **138** | 1 | 1.638 / 139 / 1 |
| 11 | Depósitos (filas de producto) | 133 | 133 (128 depósitos) | 0 | 0 | 133 / 0 / 0 |
| 12 | Levantes | 170 | 107 | 0 | 18 | 107 / 0 / 18 |

- **Simulaciones:** la primera pasada da los rechazos conocidos de FA-MIG-002 (vehículos 8.863, productos 1.778, depósitos 133 y levantes 170, por maestros no cargados). Cada simulación previa al firme dio los mismos conteos que su firme.
- **Rechazos:** los mismos de la repetición, con las mismas causas (`informe-fase-1-repeticion.md` §4.2). **0 rechazos por defecto de la herramienta.**
- **Tiempos:** simulación inicial 2,5 s; simulación + firme de las 12 entidades **6,3 s**; idempotencia 0,3 s; conciliación 0,12 s; tarifas 0,19 s; `open-billing` **1,41 s**. Con la exportación, la parte mecánica sigue por debajo de 30 s.

**Conteos de la v2 tras la carga**, frente a la repetición:

| Tabla | Ahora | Repetición | Diferencia |
|---|---|---|---|
| Terceros / roles / configuraciones de facturación | 1.389 / 2.449 / 1.053 | Igual | — |
| Vehículos / conductores | 10.393 / 4.361 | Igual | — |
| Embalajes / cuadrillas / ciudades | 61 / 7 / 1.774 | Igual | — |
| **Ubicaciones** | **9** | 26 (20 de ejemplo + 6) | −20 de ejemplo, +3 bodegas sin sección |
| **Productos** | **1.640** | 1.643 | −4 de ejemplo, +1 legacy que ahora se crea (A.4) |
| Depósitos / productos de depósito / servicios / movimientos / levantes | 128 / 133 / 128 / 202 / 107 | Igual | — |
| `legacy_id_map` | **18.284** | 18.281 | +3: las 3 bodegas sin sección (`B18`, `B19` y `B20`) |
| Contactos de terceros | 0 | 0 | — |

### A.4 Verificación

**Ubicaciones:**
- **9 creadas con 0 rechazos.** El lote dice «Filas leídas: 6 de sección y 3 de bodega sin sección.».
- `Bodega 1 BA-[1][1]` (legacy 4027) queda **No disponible**. Las otras 8 quedan **Disponibles**: Bodega 2 a 5 BA, Bodega Baja BA, Cobertizo, Patio 1 BA y Patio 2 BA. Las 3 sin sección tienen id legacy `B18`, `B19` y `B20`, el código y el nombre de la bodega y capacidad 1.
- **Segunda carga:** 9 omitidas, 0 creadas, sin cambios de disponibilidad.
- **En la pantalla** (`http://localhost:3001/admin/locations`, Admin): «Total 9 · Disponibles 8 · No disponibles 1», con solo esas 9 filas. No aparece ninguna de ejemplo (`A01-R01-N01`, `PATIO-01`…).

**Productos: −3 frente a la repetición (1.643 → 1.640).**
- Faltan los **4 de ejemplo** (Manteca (Importaciones), Granos, Enlatados y Plátano Seco).
- **Se crea 1 producto más del legacy:** el legacy 238, «PLATANO SECO», embalaje 23.
  - En la repetición, el importador lo asociaba por nombre normalizado al de ejemplo «Plátano Seco» (Id `e5f6a7b8-…`): por eso eran 1.638 creados y 139 asociados. Ahora se crea (1.639 / 138).
  - Lo usan **7 filas de 7 depósitos** (BA0558, BA0988, BA1140, BA1198, BA1391, BA1999 y BA2318). En la repetición quedaban apuntando al producto de ejemplo; ahora apuntan al producto migrado.
  - Ninguno de los otros 3 de ejemplo tenía equivalente en el legacy.
- Cuenta: 1.643 − 4 + 1 = **1.640**.

**Idempotencia (OK-3):**
- Segunda carga en firme de ciudades, ubicaciones, clientes, vehículos, productos, depósitos y levantes:
  - ciudades: 1.774 «actualizadas» por `LegacyId` y 7 errores;
  - ubicaciones: **9 omitidas**;
  - clientes: 1.056 omitidos;
  - vehículos: 10.483 omitidos y 111 errores;
  - productos: 1.777 omitidos y 1 error;
  - depósitos: 133 «ya fue migrado»;
  - levantes: 107 omitidos y los mismos 18 errores.
- **Los conteos de negocio quedaron idénticos** (`evidencias/v3/carga/conteos-antes-idem.txt` y `conteos-despues-idem.txt`). Solo suben `legacy_import_batches` (+7 lotes) y `audit_logs` (+1.774, la auditoría de las ciudades actualizadas).

**Conciliación:** **133 Ok**, 0 Difference y 0 NotMigrated, en 0,12 s.

**Tarifas T1 a T4:** por el API con el Admin, el mismo mapeo aprobado (`mapeo-tarifas-propuesto.md`): T1 regla `PERCENTAGE_OF_VALUE` 0,295 % con mínimo de $50.000 con IVA, T2 mínimo de $50.000, T3 IVA y $16.806,72 para báscula, T4 $15.000 para la guía. Las 5 peticiones dieron 200.

**`open-billing`:** **128 Opened**, 0 Skipped y 0 Failed.

**Primer período:**

| | Facturas | Total con IVA | Repetición |
|---|---|---|---|
| Ciclo de 15 días (01/10 a 16/10/2026) | 92 | $63.258.314,46 | Igual |
| Ciclo de 180 días (01/10/2026 a 30/03/2027) | 36 | $27.999.160,93 | Igual |
| **Total** | **128** | **$91.257.475,39** ($76.686.954,14 + $14.570.521,25 de IVA) | **Igual** |

- **El total es exactamente $91.257.475,39.**
- Los 128 con `PERCENTAGE_OF_VALUE`, 4 en el piso de $50.000, rango de $50.000 a $3.483.997,59.
- 0 facturas con «TRM PENDIENTE» o «No existe un precio…».
- El cambio de producto de los 7 depósitos con «PLATANO SECO» no altera el importe, porque T1 se calcula sobre el CIF del depósito y no depende del producto.

**Guía sobre un migrado (DEF-MIG-005 y DEF-MIG-007):**
- **Depósito:** BA0042 → `2024BA00002` (recibido 648; en el legacy salen 200; saldo 448).
- **Recorrido por el API**, una cuenta por rol:
  1. OC `2026OC00001` por 50 u: reservado 50, disponible 398.
  2. Ingreso de un vehículo migrado.
  3. Inicio de salida en báscula: total propuesto **$20.000,00**, ya redondeado (O-3). Cobro inmediato y tara.
  4. Cargue: stock 448 → 398 y reserva liberada.
  5. Guía `2026S00001`.
  6. Repesaje: ciclo `Complete` y OC `Dispatched`.
  7. Salida de Vigilancia.
- **Línea congelada de la guía:** recibido **648** / saldo anterior **448** / sale **50** / nuevo saldo **398**. → **DEF-MIG-005 sigue bien.**
- **PDF:** la columna «Manifiesto» imprime el manifiesto DIAN del depósito, igual al del CSV, con su levante y aceptación. → **DEF-MIG-007 sigue bien.**
- **Reimpresión:** mismo contenido. Solo cambia la hora de «impreso el», un segundo después.
- **Cobros:** báscula $20.000 y guía $15.000, las dos `Paid`.
- **Correo:** 0 mensajes en Mailpit; `stakeholder_contacts_info` vacía.
- **Log del API local:** 0 líneas `fail:` o `crit:`.
- Evidencias: `evidencias/v3/e19/BA0042/`.

---

## B. Redespliegue de staging (sin recrear la base)

### B.0 Antes de empezar
- **Tareas del usuario de la fase 2, hechas:**
  - el login del `admin` con la contraseña de `.admin-staging.local` da 200, sin cambio obligatorio;
  - existe el destino `local-staging` (Local, `/opt/wms/backups`, activo), creado el 2026-10-06 a las 21:28.
- **Inventario (solo lectura):**
  - `wms-api` (imagen de la fase 2), `caddy:2` y `postgres:18.0` arriba;
  - volúmenes `pgdata`, `caddy_data` y `caddy_config`;
  - disco 6,8 de 77 GB; RAM 3,8 GB (2,8 disponibles);
  - `/opt/wms/data/keys` no existía.

### B.1 Artefactos

- **`staging.sql`:** regenerado con `dotnet ef migrations script --idempotent`. Trae **11 migraciones**, de `20261001193201_InitialParityLegacy` a `20261007030137_RemoveSampleSeedData`, con los 24 `DELETE` (20 ubicaciones y 4 productos).
- **Prueba en un Postgres 18.0 desechable**, que simula la base de staging:
  1. se aplicó el script de las 10 migraciones anteriores: 10 migraciones, 20 ubicaciones y 5 productos;
  2. se aplicó `staging.sql` **dos veces** sin error: 11 migraciones, 0 ubicaciones, solo «Contenedor Vacío» y 6 roles.
- **Imagen `wms-api:staging`** (linux/amd64), con `scripts/deploy-staging.sh backend` (21 s, incluida la transferencia). Corre como UID 1654 y trae `pg_dump` 18.6.
- **Frontend:** `scripts/deploy-staging.sh frontend` con el FE `508b91b` y `NUXT_PUBLIC_API_BASE=https://api.100-60-89-139.sslip.io/api/v1`. Pesa 80 MB y no tiene referencias a `localhost`.

### B.2 Configuración
- **`bootstrap`:** idempotente. Creó **`/opt/wms/data/keys` con dueño 1654:1654 y modo 700**. `/opt/wms/backups` queda en 1654:1654, modo 750.
- **`config`:** subió el compose (con `DataProtection__KeysPath=/app/keys` y el montaje `/opt/wms/data/keys:/app/keys`), el Caddyfile y el `.env`.

### B.3 Comprobación antes de migrar (SQL de solo lectura)
- En staging estaban las **20 ubicaciones y los 4 productos de ejemplo**, con 10 migraciones, 0 depósitos y 0 lotes de importación.
- Se buscaron referencias a esos 24 Id en **todas las columnas con FK** hacia `warehouse_locations` y `products`:
  - `agreement_services`, `invoice_items`, `packing_list_items`, `service_pricing_rules`, `storage_billing_period_products`, `storage_billing_periods` y `warehouse_storage_products` (producto);
  - `warehouse_storage_product_placements`, `warehouse_storage_products` y `warehouse_storages` (ubicación).
- **Resultado: 0 referencias en las 10 columnas.** Se siguió con el despliegue.

### B.4 Despliegue

| Paso | Hora | Resultado |
|---|---|---|
| `backend` | 22:20 | Imagen cargada en el servidor. |
| `frontend` | 22:21 | `rsync` a `/opt/wms/site/`. |
| `migrate` | 22:21 | «Migraciones aplicadas: **11** (esperado 11)» y «Roles sembrados: 6». |
| `up` | 22:21 | Se recreó solo `wms-api`. `postgres` y `caddy` siguieron arriba. |

- **`pgdata` no se borró** ni se recreó la base: no hubo `down`, `volume rm` ni `dbup`.
- **Arranque del API:**
  - `Hosting environment: Production` y `Application started`;
  - **`Bootstrap admin 'admin' ya existe; se omite.`**: se conservó el Admin con su contraseña nueva;
  - `DatabaseBackupJob iniciado. Hora de ejecución: 02:00 (Colombia).`;
  - sin `fail`, `crit` ni excepciones.
- **Advertencias del log:**
  - la de la fase 2 («DataProtection guarda sus llaves dentro del contenedor») **ya no aparece**;
  - queda «No XML encryptor configured… unencrypted form», esperada: las llaves no se cifran con certificado, pendiente para producción según la ficha;
  - siguen las conocidas de `FormulaType.ParameterSchema` y `URLS`.

### B.5 Verificación

| Comprobación | Resultado |
|---|---|
| **Base** | 11 migraciones (la última, `RemoveSampleSeedData`); `warehouse_locations` **0**; `products` solo **«Contenedor Vacío»**; 6 roles; 1 usuario; el destino de respaldo conservado; 0 depósitos y 0 lotes de importación. |
| **Llaves de DataProtection** | `/opt/wms/data/keys/key-6cc44126-….xml` (1654, modo 600), escrita en el arranque de las 22:21. |
| **Prueba de las llaves** (recuperación → reinicio → enlace) | **Cumple.** El usuario pidió la recuperación del `admin` (correo de las 22:31). A las 22:33 se reinició el API (`docker compose restart wms-api`): arrancó sin errores y la carpeta conserva **la misma llave**, sin generar otra. **El usuario confirmó que el enlace del correo sigue funcionando después del reinicio.** El agente no usó el enlace. |
| **`smoke`** | Frontend 200, SPA 200, login inválido 400 y CORS `https://app.100-60-89-139.sslip.io`. **Verde.** |
| **Login del Admin** | 200 con la contraseña de `.admin-staging.local`; rol Admin; sin cambio obligatorio. |
| **Respaldos: prueba del destino** (FB-BAK-002) | 200, «Se escribió y borró un archivo de prueba en /opt/wms/backups/_prueba/…». |
| **Respaldos: manual** (FB-BAK-003) | `POST administration/backups/run` → 202; corrida `Manual`, `Succeeded` en 0,4 s. En el host quedaron `/opt/wms/backups/2026/10/wms_20261006_2222.dump` (305.807 B) y `uploads_20261006_2222.tar.gz` (342.517 B). |
| **DIAN desde el contenedor del API** (pendiente de la fase 2) | La imagen no trae `curl`: se midió con `openssl s_client` dentro del contenedor contra `www.datos.gov.co:443`, el servicio de la TRM de `DianTrm`. Tres peticiones: **HTTP 200 en 171, 155 y 126 ms**. Además, `GET system/dian-trm/today` por el API de staging: 200 con la TRM del día, **0,70 s** de ida y vuelta desde el Mac (sin caché) y 0,32 s con caché. **Cumple: 3 s o menos.** |
| **Correo de recuperación a `capb.dev@gmail.com`** (pendiente de la fase 2) | **Llegó.** El usuario pidió la recuperación del `admin` desde la pantalla y confirmó el correo: 06/10/2026 22:31, asunto «Recuperación de Contraseña - WMS». **Cerrado.** |

---

## C. Pendientes y estado que queda

**Pendientes cerrados:**
- **De la fase 2:**
  - cambio de la contraseña del `admin` y destino de respaldo Local (los hizo el usuario);
  - correo de recuperación a `capb.dev@gmail.com`;
  - salida hacia la DIAN en 3 s o menos;
  - llaves de DataProtection persistentes (la sugerencia del §6.4 del informe de la fase 2).
- **De DEF-MIG-008:** toda su lista de verificación (ver la ficha).

**Quedan, sin bloquear la fase 3:**
- **Producción:** cifrar las llaves de DataProtection con un certificado (advertencia «No XML encryptor configured»), como dice la ficha.
- **Fase 4:**
  - los casos de QA que nombran ubicaciones de ejemplo (`F1-UBI-003`, `F4-REC-004`, `F4-UBI-001` y `F4-UBI-003`) usan ubicaciones migradas o creadas como dato QA (ficha DEF-MIG-008);
  - FB-BAK-005 (restaurar en una base aparte) sigue para cuando haya datos.
- **Limpieza opcional del servidor:** las imágenes anteriores del API quedaron huérfanas (`docker image prune`).


| Recurso | Estado |
|---|---|
| `legacy-mariadb` (3308) | Arriba, sin cambios. |
| `wms_migracion` (5433) | Recreada con 11 migraciones y la carga v3: tarifas T1 a T4, 128 períodos abiertos y la salida de BA0042 (OC `2026OC00001`, guía `2026S00001`). |
| API local (5291) | Arriba con el BE `b31ddb6` (PID en `evidencias/v3/api.pid`; log en `evidencias/v3/api.log`). |
| Frontend local (3001) | Arriba (Nuxt dev, FE `508b91b`). |
| Mailpit | Arriba, con 0 mensajes. |
| CSV | **Conjunto v3 congelado** en `db_legacy/trabajo/csv/` con `sha256-csv-fase-1-v3.txt`. |
| Staging | BE `b31ddb6` / FE `508b91b`, 11 migraciones, sin datos migrados, respaldos activos y llaves persistentes. |
| `wmsdb`, `mysql57` y producción | Sin tocar. |
| Repositorios | Sin cambios de código ni de configuración. Solo `docs/planes/migracion-staging/` sin commit. |
