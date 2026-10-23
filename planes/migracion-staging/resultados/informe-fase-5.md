# Informe de la Fase 5 — Staging listo para los operarios

> **Fecha:** 2026-10-07, de 01:30 a 02:05, hora de Colombia.
> **Build:** BE `84c712f` / FE `8527144`, el del redespliegue del re-test de S6. Sin cambios de código.
> **Prompt:** `docs/archivo/prompts/migracion-staging/prompt-fase-5.md`. **Ejecutor:** Claude Opus 5.5 (el prompt recomendaba Sonnet 5.5).
> **Resultado:** staging queda listo para los operarios:
> - con los datos de QA-S6 conservados como ejemplo, por decisión del usuario que reemplaza a F5-1;
> - con las tarifas reales de montacargas;
> - con cinco cuentas `operario.*` que exigen cambio de contraseña;
> - con seis escenarios de práctica, una guía por rol y el respaldo «listo para operarios».

## 1. Cómo se trabajó

| Tema | Detalle |
|---|---|
| Sesiones | **El agente no escribió contraseñas ni creó cuentas**, porque staging no es un host local. **El usuario:**<br>• inició cada sesión en el navegador integrado (`admin`, `operario.vigilancia` y `operario.comext`);<br>• ejecutó el script de cuentas.<br>El agente usó esas sesiones con `fetch` desde la página. Los tokens no salieron del navegador. |
| Lectura | SQL de **solo lectura** por SSH (`BEGIN TRANSACTION READ ONLY … ROLLBACK`). Para elegir las parejas vehículo–conductor se consultó la MariaDB local `legacy-mariadb`, sin imprimir documentos ni nombres. |
| Escritura | Solo por el API: un respaldo inicial, 5 tarifas, 4 ingresos, 1 orden de cargue y el respaldo final. Las cuentas las creó el script del usuario, también por el API. **Sin SQL de escritura**, sin borrar volúmenes ni archivos. |
| Secretos | Ninguna contraseña, token ni valor de `.env` en el chat ni en este informe. |

## 2. Decisiones de la fase

| # | Decisión | Estado |
|---|---|---|
| F5-1 | Restaurar el respaldo «staging migrado» (`wms_20261006_2302.dump`) | **Revocada por el usuario a las 01:38**, después del checkpoint del paso 2: «dejar los datos de QA, NO hacer la restauración, esto sirve de ejemplo para los operarios». **No se restauró nada.** |
| F5-2 | Tarifas base de montacargas | Aplicada (§4) |
| F5-3 | Una cuenta por rol, con alias `capb.dev+operario.<rol>@gmail.com` | Aplicada (§5) |

**Consecuencias de no restaurar:**
- **Se conservan:**
  - las operaciones de QA-S6;
  - las 5 cuentas `qa.*`, activas;
  - la factura de O-3;
  - la contraseña actual del Admin.
- **No hizo falta la recuperación del Admin** del paso 4.
- **Los camiones QA-S6 siguen en planta:** `QSP001`, `QSB202`, `QSC301`, `QSD401`, `QSE501` y `QSE502`. La guía los presenta como ejemplo y reserva `QSP001` para PRF-002.

## 3. Respaldos

| Momento | Corrida | Archivo en `/opt/wms/backups/2026/10/` | Tamaño | Resultado |
|---|---|---|---|---|
| Antes de F5 (01:39) | `9bc04891` | `wms_20261007_013925_9bc04891.dump` + `uploads_…_9bc04891.tar.gz` | 4.460.024 B | `Succeeded` |
| Staging restaurado | — | No aplica: no hubo restauración | — | — |
| Programado de las 02:00 | `96640179` (`Daily`) | `wms_20261007_020000_96640179.dump` + `uploads_…_96640179.tar.gz` | 4.465.379 B | `Succeeded` |
| **Listo para operarios** (02:00:11) | `a564692e` | **`wms_20261007_020011_a564692e.dump`** + **`uploads_20261007_020011_a564692e.tar.gz`** | 4.465.445 B | `Succeeded` |

**Estado antes de F5** (SQL de solo lectura, 01:35):

| Dato | Valor |
|---|---|
| Migraciones | 11 |
| Depósitos | 131: 129 `Confirmed`, 1 `Closed` y 1 `Draft` |
| Facturas | 143 por $91.977.198,26:<br>• Draft: 130, por $90.974.014,65<br>• Approved: 2, por $758.683,61<br>• Paid: 11, por $244.500 |
| Usuarios | 6: `admin` y `qa.*` |
| Operación | 13 entradas, 9 ciclos, 3 órdenes de cargue, 3 guías y 1 uso de montacargas |
| Ubicaciones | 9; `[1][1]` No disponible |
| Destino de respaldo | `local-staging` (Local, `/opt/wms/backups`, activo) |

**Archivos del respaldo «staging migrado»:** se verificaron en el host. `wms_20261006_2302.dump` pesa 4.065.098 B y `uploads_20261006_2302.tar.gz` pesa 342.517 B, iguales a la Fase 3. Quedan disponibles por si se quiere volver a los datos migrados limpios.

## 4. Tarifas de montacargas (F5-2)

**El modelo coincide con la decisión:**
- `ForkliftRate.Amount` es la tarifa base que precarga el cobro.
- Al finalizar el uso, `ForkliftVatCalculator` suma el IVA activo del catálogo (19 %) **solo si se marca «Aplicar IVA»** (WMS-28).
- El servicio `MONTACARGAS` no tiene `ServiceTax`.

`PUT forklift-rates/{tipo}` con el Admin, el mismo contrato de la pantalla: 5 respuestas 200 a las 01:39. **Reemplazaron las tarifas de prueba de S6** (de $50.000 a $20.000).

| Tipo | Tarifa base |
|---|---|
| Tractomula | $220.000 |
| Doble Troque | $150.000 |
| Sencillo | $140.000 |
| Turbo | $110.000 |
| Guacal o Estiba | $40.000 |

- **Pantalla** «Administración → Tarifas de montacargas»: muestra los cinco valores, actualizados el 07/10/2026 a las 01:39.
- **Vista previa sin crear datos** (`GET warehouse/forklift-rate?vehicleType=Tractomula`): `ratePerHour` 220.000, `taxRatePercent` 0 y `vatRatePercent` 19. Con «Aplicar IVA» el cobro sería $220.000 + $41.800 = **$261.800**.

## 5. Cuentas de los operarios (F5-3)

- **Script:** `db_legacy/trabajo/crear-cuentas-operarios-staging.sh`, fuera de git. Es copia del de QA con dos cambios:
  - **no hace el primer cambio de contraseña;**
  - lee `.admin-staging.local` en su formato actual.
- **Ejecución:** la hizo el usuario a las 01:42, con 5 respuestas 201. El login con la contraseña temporal da `mustChangePassword=true`.
- **Credenciales:** `db_legacy/trabajo/credenciales-operarios-staging.local.md`, con permisos 600.

| Usuario | Rol | Correo | Estado |
|---|---|---|---|
| `operario.vigilancia` | Operario vigilancia | `capb.dev+operario.vigilancia@gmail.com` | Activa, cambio pendiente |
| `operario.bascula` | Operario báscula | `capb.dev+operario.bascula@gmail.com` | Activa, cambio pendiente |
| `operario.bodega` | Operario bodega | `capb.dev+operario.bodega@gmail.com` | Activa, cambio pendiente |
| `operario.comext` | Comercio exterior | `capb.dev+operario.comext@gmail.com` | Activa, cambio pendiente |
| `operario.facturacion` | Facturación | `capb.dev+operario.facturacion@gmail.com` | Activa, cambio pendiente |

- **Cuentas usadas para crear datos:** `operario.vigilancia` y `operario.comext`. El usuario inició su sesión con la contraseña temporal y **no la cambió**: el API acepta la sesión con `mustChangePassword=true` y la cuenta sigue pendiente de cambio. La verificación SQL a las 01:47 da `must_change_password = true` en las cinco.
- **Ninguna creación de cuenta envió correo.** La recuperación por correo es solo para el Admin (CHG-51).

## 6. Datos de práctica

- **Vehículos y conductores:** son migrados. Cada pareja salió de los últimos pesajes del legacy (8 al 10/06/2024), así que **cada camión entra con el conductor que lo manejó en el legacy**.
- **Marcas:** los ingresos llevan «PRÁCTICA Pn» en las observaciones, y la orden externa tiene prefijo `PRAC-`.
- **Autoría:** verificada por SQL en `entry_logs.entry_authorized_by_id` y en `loading_orders.created_by`.

| # | Escenario | Dato | Autor | Estado inicial |
|---|---|---|---|---|
| P1 | Importación nueva | Ingreso de **GLS926** (ECU), conductor migrado del vehículo GLS926, motivo «Descargue mercancia importacion» | `operario.vigilancia` | `Registered`, sin servicio: cola de báscula sin iniciar |
| P2 | Solo báscula | Ingreso de **SRC396** (COL), conductor migrado del vehículo SRC396, motivo «Solo Bascula» | `operario.vigilancia` | Igual |
| P3 | Salida de un depósito migrado | **Depósito 2024BA00005** (BA0090): `Confirmed`, Nacionalizado, 1 producto, 2.000 unidades, cliente `Active`.<br>**OC 2026OC00004** (externa `PRAC-OC-0001`, emisor: la agencia de aduanas del depósito), 200 unidades, destino Pasto, `Pending`.<br>Ingreso de **SVO318** (COL), conductor migrado del vehículo SVO318, motivo «Cargue mercancia importacion». | OC: `operario.comext`; ingreso: `operario.vigilancia` | Stock 2.000, reservado 200, disponible 1.800; camión en la cola sin iniciar |
| P4 | Levante pendiente | **Depósito 2024BA00006** (BA0118): `Confirmed`, SinNacionalizar, 1.350 unidades, con manifiesto | — (solo elegido) | Sin tocar |
| P5 | Factura de almacenamiento | Facturas en Borrador de **2024BA00001** (BA0008), por **$558.159,96**, y de **2024BA00003** (BA0085), por **$474.566,16**. Período del 01/10 al 16/10/2026 | — (solo elegidas) | Sin tocar |
| P6 | PRF-002 | Ingreso de **CAH514** (ECU), conductor migrado del vehículo CAH514, motivo «Descargue mercancia importacion». `QSP001` (S6) queda de reserva | `operario.vigilancia` | Cola de báscula sin iniciar |

- **Excluidos:** BA0042 y BA0558, que tienen OC, levantes y saldos tocados por S6.
- **Elección de P3 y P4:** depósitos migrados sin reservas, sin OC y sin levantes nuevos.
- **Exportación e inspección:** no se crearon datos. Todos los depósitos migrados son `IMP001` (71 nacionalizados y 57 sin nacionalizar). La guía explica cómo empezar uno desde báscula.

## 7. Guía

`docs/planes/migracion-staging/resultados/guia-pruebas-operarios.md` contiene:
- la URL, los usuarios sin contraseña y los avisos (datos de 2024 con corte al 01/10/2026, 66 depósitos en abandono, «Estadísticas» fuera del menú, recuperación solo para el Admin y cambio en el primer ingreso);
- los ejemplos QA-S6;
- cómo reportar un problema (el destinatario queda `[completar]`);
- una sección por rol con pasos sobre P1 a P6;
- la sección de PRF-002 con F3-REG-024, F3-PES-015 y la hoja de tiempos;
- la tabla de datos de práctica;
- cómo volver al punto de restauración.

## 8. README de staging

En la restauración, `deploy/staging/README.md` extraía los archivos subidos en `/opt/wms/uploads`. Esa carpeta no existe en el host. La real es **`/opt/wms/data/uploads`**, el bind mount de `compose.staging.yaml` hacia `/app/wwwroot/uploads`. Se corrigió la ruta y se agregó el `chown -R 1654:1654`.

## 9. Respaldo «listo para operarios» y respaldo de las 02:00

- **Respaldo programado de las 02:00** (pendiente desde la Fase 4): **la sesión lo alcanzó y corrió solo.**
  - Corrida `96640179`, tipo `Daily`, de 02:00:00 a 02:00:01.
  - Resultado `Succeeded`, con 4.465.379 B, en `wms_20261007_020000_96640179.dump`.
  - Esto cierra el caso «no ejecutado» de S6 (A.5).
- **Respaldo «listo para operarios»:**
  - `POST administration/backups/run` a las 02:00:11, con respuesta 202.
  - Corrida `a564692e`, `Manual`, resultado **`Succeeded`**, con 4.465.445 B.
  - Archivos: **`wms_20261007_020011_a564692e.dump`** (4.122.928 B) y **`uploads_20261007_020011_a564692e.tar.gz`** (342.517 B).
  - **Es el punto de restauración para repetir las pruebas de los operarios desde cero.** La guía (§11) explica cómo volver a él.
  - **Al restaurarlo, las contraseñas vuelven a las temporales de `credenciales-operarios-staging.local.md`**, y el Admin, a la que tenía a las 02:00 del 07/10.
- **Limpieza de imágenes:** se hizo `docker image prune -f` con el «sí» del usuario.
  - Borró 4 imágenes huérfanas de despliegues anteriores y liberó 340,2 MB.
  - Quedan `wms-api:staging` (`70ba08c858a7`), `caddy:2` y `postgres:18.0`.
  - El disco quedó en 6,8 G de 77 G (9 %).

## 10. Estado final de staging

SQL de solo lectura, a las 02:01.

| Dato | Valor | Cambio en la fase |
|---|---|---|
| Build | BE `84c712f` / FE `8527144`; contenedores `caddy`, `wms-api` y `postgres` arriba; `postgres` healthy | — |
| Migraciones | 11 | — |
| Depósitos | 131: 129 `Confirmed`, 1 `Closed` y 1 `Draft`. 128 son migrados (`IMP001`) | — |
| Facturas | 143 por $91.977.198,26: Draft 130, Approved 2 y Paid 11 | — |
| Usuarios | 11: `admin`, 5 `operario.*` con cambio pendiente y 5 `qa.*` | +5 `operario.*` |
| Entradas | 17: las de QA-S6 y 4 de práctica (P1, P2, P3 y P6), en la cola de báscula | +4 |
| Ciclos de báscula | 9 | — |
| Órdenes de cargue | 4: las 3 de S6 y **2026OC00004** de P3 | +1 |
| Guías | 3 | — |
| Montacargas | Tarifas reales F5-2; 1 uso de S6 | 5 tarifas reemplazadas |
| Ubicaciones | 9; `[1][1]` No disponible | — |
| Maestros | 10.404 vehículos, 4.363 conductores y 1.393 terceros | — |
| Tarifas | T1 a T4 (1 regla de almacenamiento y 3 precios base) | — |
| Respaldos | Destino `local-staging` activo; respaldo diario de las 02:00 verificado | — |
| Disco | 6,8 G de 77 G (9 %) | −340 MB |
| URL | <https://app.100-60-89-139.sslip.io> | — |

## 11. Pendientes

1. **PRF-002 con un operario,** con F3-REG-024 y F3-PES-015. El escenario es P6 (CAH514), con `QSP001` de reserva; la hoja de tiempos está en la guía, §10. Con PRF-002 en 30 s o menos, el informe final del QA pasa a **GO**.
2. **Al terminar las pruebas** (§9 del plan): decidir si se vacía o se anonimiza staging, porque tiene datos reales de clientes.
3. **Cuentas `qa.*`:** siguen activas, con contraseñas fijas en `credenciales-qa-staging.local.md`. Conviene que el usuario decida si las desactiva mientras prueban los operarios.
4. **Guía:** completar a quién y por qué canal se reportan los problemas.
