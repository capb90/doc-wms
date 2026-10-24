# 08-procesos-infra-fuera-alcance — 05 Análisis V2

> AG-08 · 2026-10-23 · Estático (sin compilar, sin ejecutar, sin Git). Código en disco a esa fecha; según `docs/contexto/estado.md`: BE `35a61b2` / FE `c924a8b`.
> **Prefijos:** `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `D/` = `docs/`; `L/` = `bodegas-legacy/`. Rutas de API con prefijo `/api/v1` (`B/Wms.Api/Program.cs:162`).

## 1. Resumen

- **Respaldos (CF-V080)** e **importación legacy (CF-V081)** existen solo como API de administrador, sin pantallas, por decisión DF3. Están implementados con simulación, conciliación, retención y aviso de fallo. Lo que falta está en la configuración del despliegue y en el alcance de datos del corte, no en los endpoints.
- **Notificaciones (CF-V082)**: hub SignalR autenticado, persistencia y página. Se encontró un defecto nuevo: los avisos se ordenan del más antiguo al más reciente (BR-08-014).
- **Centro de ayuda (CF-V083)**: frontend público que lee un bucket. No tiene backend.
- **`SystemController` (CF-V085)** no es un «estado del sistema». Solo expone la TRM de la DIAN del día y no tiene consumidor. No hay endpoint de salud.
- **Jobs (CF-V086)**: 6 `BackgroundService`, todos registrados. Solo el de respaldo tiene interruptor.
- **Parte B**: no quedan restos de Colmotores ni del portal en V2. Ningún módulo depende de VIN, serial o voltaje.

## 2. Respaldos — CF-V080 (P14, GAP-021, F6-05)

| Endpoint | Política | Handler / servicio | Consumidor |
| --- | --- | --- | --- |
| `GET administration/backup-destinations` | `AdminOnly` (clase, `B/Wms.Api/Controllers/v1/BackupsController.cs:19-22`) | `GetBackupDestinationsQuery` | Colección Postman `B/deploy/postman/wms-respaldos.postman_collection.json` (paso 2) |
| `POST administration/backup-destinations` | `AdminOnly` | `CreateBackupDestinationCommand`: 400 sin carpeta o sin bucket; 409 nombre duplicado | Postman (paso 3); runbook `B/deploy/staging/README.md:183-192` |
| `PUT` / `DELETE administration/backup-destinations/{id}` | `AdminOnly` | `Update…` / `DeleteBackupDestinationCommand` (los archivos quedan en el destino) | — |
| `POST administration/backup-destinations/{id}/test` | `AdminOnly` | `BackupService.TestDestinationAsync`: escribe y borra un archivo (`B/Wms.Application/Administration/Backups/Common/BackupService.cs:188-211`) | Postman (paso 4) |
| `POST administration/backups/run` | `AdminOnly`; autor del token (`BackupsController.cs:93-97`) | `StartManualAsync`: 202 y ejecución en segundo plano; 409 «Ya hay un respaldo en curso.» (`BackupService.cs:57-77`) | Postman (paso 5) |
| `GET administration/backups/runs` | `AdminOnly` | `GetBackupRunsQuery`, paginado | Postman (paso 6) |

- **Ejecución** (`BackupService.ExecuteAsync`, `:106-186`): `pg_dump --format=custom` con la clave por `PGPASSWORD` y un límite de 2 h (`B/Wms.Infrastructure/Services/Backups/PgDumpRunner.cs:28-72`). Hace el `tar.gz` de `Storage:Local:BasePath` solo si `Storage:Type = Local` (`:74-88`). Copia a cada destino activo y anota el resultado por destino en `backup_runs`. Borra los temporales.
- **Retención** (`BackupRetentionPolicy.cs:17-35`; `BackupService.cs:214-260`): por destino, 30 diarios y 12 mensuales; los manuales no se borran. **Cumple P14.**
- **Programación** (`B/Wms.Api/BackgroundJobs/DatabaseBackupBackgroundService.cs:20-56`): solo con `Backups:Enabled = true`, a la hora `Backups:DailyTime` de Colombia (`ColombiaTime.Now`). Es idempotente por día y la primera corrida exitosa del mes es mensual.
- **Fallo:** aviso de nivel Error al rol Admin, solo en la aplicación (`sendEmail: false`, `BackupService.cs:262-288`). Con cero destinos activos, la corrida falla y avisa (`:132-133`).
- **Concurrencia:** `pg_advisory_xact_lock` al registrar la corrida; una corrida colgada deja de bloquear a las 6 h (`:46-55,297-316`). Corresponde a DEF-F11-020, Verificado.
- **Credenciales S3:** nunca en la base. Salen de `Backups:S3Credentials:{Name}:*` o de la cadena por defecto de AWS (`S3BackupTarget.cs:12,39-40`). El DTO no las devuelve.
- **Restauración:** no hay endpoint. Es un procedimiento del runbook (`README.md:205-221`), validado en FB-BAK-005 (`D/qa/resultados/F11-informe-S6-2026-10-06.md` §4.9).
- **Pruebas:** `B/Wms.Tests/Administration/BackupRetentionPolicyTests.cs`, `B/Wms.Tests/Domain/Administration/BackupDestinationTests.cs`, `B/Wms.IntegrationTests/Administration/BackupConcurrencyTests.cs`.
- **Capas:** `BackupService` está en `Wms.Application` y depende de `Wms.Infrastructure` (`AppDbContext`, `Services.Backups`). Es una desviación documentada en el propio plan (`plan-backend-paridad-legacy.md` §C.6, desviación 7). No es una brecha funcional.

**Qué es código y qué es configuración del despliegue**

| Aspecto | Dónde | Estado |
| --- | --- | --- |
| Encender el job, hora y carpeta temporal | `B/Wms.Api/appsettings.json:19-23` (apagado por defecto); `B/deploy/staging/compose.staging.yaml:78-82` (activo en staging) | Configuración |
| Destinos | Registros en `backup_destinations` creados por API después del despliegue (runbook `:180-192`) | Dato operativo. En staging hay un solo destino, `local-staging` (`D/planes/migracion-staging/resultados/informe-fase-5.md:57`) |
| Carpeta del destino Local | Volumen `/opt/wms/backups` del mismo servidor (`compose.staging.yaml:91-92`) | Configuración: **sin copia fuera del servidor** (BR-08-001) |
| Destino S3 | Código listo; credenciales por entorno (`README.md:197-203`) | No configurado en staging ni en la plantilla de producción (`B/deploy/postman/produccion.postman_environment.json`: `local-produccion`, `/opt/wms/backups`, dominio `CAMBIAR-DOMINIO-API`) |
| Archivos subidos | `Storage__Type: "Local"` en staging (`compose.staging.yaml:55-57`) y en Azure test (`B/infra/main.tf:112-114`) | Con otro tipo de almacenamiento no se copian (BR-08-002) |
| Azure test | `B/infra/main.tf` sin `Backups__*` (búsqueda `Backups__` en `infra/*.tf`: sin resultados) | Sin respaldo; ambiente pendiente de baja (`D/contexto/estado.md` §4 n.º 9) |
| `pg_dump` en la imagen | `B/deploy/staging/Dockerfile.staging` (`postgresql-client-18`, runbook `:194-195`) | Configuración |

**Inconsistencia del runbook:** `README.md:160` dice que «el frontend no tiene pantalla de respaldos». `:206` habla del Id «que muestra la pantalla de respaldos». La búsqueda `backup`, `respaldo` en `F/` solo encuentra la etiqueta `BackupDestination` de la auditoría (`F/features/audit/utils/entity-labels.ts:9`). Es un detalle de documentación; no se registra como brecha.

## 3. Importación legacy — CF-V081 (P13, GAP-001, F6-01…04)

| Endpoint | Política | Handler | Consumidor |
| --- | --- | --- | --- |
| `POST administration/legacy-import/{entity}` (multipart `file`, `headerRows=1`, `dryRun=true`) | `AdminOnly` (`B/Wms.Api/Controllers/v1/LegacyImportController.cs:24-27`) | `ImportLegacyFileCommandHandler` | Ninguno en `F/` (DF3). Operado por API en la migración (`D/planes/migracion-staging/plan-migracion-legacy-staging.md` §3.3) |
| `GET administration/legacy-import/batches`, `/batches/{id}` | `AdminOnly` | `GetImportBatchesQuery`, `GetImportBatchByIdQuery` | Ídem |
| `POST administration/legacy-import/reconciliation` | `AdminOnly` | `ReconcileDepositsCommandHandler` (no escribe) | Ídem |
| `POST administration/legacy-import/open-billing` (`warehouseStorageIds` opcional) | `AdminOnly` | `OpenMigratedBillingCommandHandler` | Ídem |
| `POST administration/cities/import` | `AdminOnly` (`B/Wms.Api/Controllers/v1/CitiesController.cs:99-100`) | `ImportCitiesHandler` (registra lote `Cities`) | `F/features/administration/services/administration-service.ts:189` (pantalla de ciudades, módulo 01) |

**Lo que se pidió verificar:**

- **Solo Admin:** sí, en los cinco endpoints de importación y en los seis de respaldo (atributo de clase `AdminOnly` → `SystemRolesCode.Admin`, `B/Wms.Domain/Security/WmsPolicyRoles.cs:31`).
- **Simulación:** sí, es el valor por defecto. Recorre el mismo camino, con restricciones, dentro de una transacción que se revierte. El lote queda como bitácora (`ImportLegacyFileCommandHandler.cs:41-86`). **Límite conocido** (FA-MIG-002): la simulación de las entidades dependientes exige los maestros cargados en firme.
- **Transaccional:** una transacción por archivo. Guarda las filas válidas e informa las inválidas. Un error de base revierte todo y deja un lote con el error (`:65-75`). En depósitos, una fila mala deja sin migrar el depósito completo (`B/Wms.Application/Administration/LegacyImport/Importers/DepositsImporter.cs:78-117`). La apertura de facturación va en una transacción por depósito (`OpenMigratedBillingCommand.cs:97-129`).
- **Idempotente:** sí, por `legacy_id_map` (`LegacyImporterBase.cs:46-50`), por depósito ya migrado (`DepositsImporter.cs:83-85`, que se informa como error) y por levante existente (`ReleasesImporter.cs:117`). Validado en FA-MIG-004 (`D/planes/migracion-staging/resultados/informe-fase-1-repeticion.md` §5.4).
- **Conciliación:** `Ok`/`Difference`/`NotMigrated` por fila. Descuenta los movimientos de V2 posteriores a la migración, pero no los levantes nuevos (`DepositReconciler.cs:51-64`; observación O-2 → BR-08-007).
- **Codificación:** UTF-8 o Windows-1252 en el importador común (`Common/LegacyCsvReader.cs:33-46`). Las ciudades solo se leen como UTF-8 (`CitiesController.cs:117`) → BR-08-013.

**Qué importa frente a lo que el legacy tiene vivo**

| Dato vivo del legacy | ¿Lo importa V2? | Evidencia / observación |
| --- | --- | --- |
| Ciudades con `dias` | Sí | `CitiesController.cs:99` (F2-06) |
| Embalajes, cuadrillas, ubicaciones | Sí | `LegacyImportEntity.cs:9-11`; ubicaciones con capacidad 1 (desviación 3 del plan) |
| Clientes, agencias, transportadoras, vehículos, conductores, productos | Sí | `LegacyImportEntity.cs:12-17`. Lo que V2 no guarda (fotos, marca y carrocería, representantes) se descarta por GAP-023 |
| Depósitos vivos con saldo, nacionalizado, CIF y moneda | Sí | `DepositsImporter.cs` (128 depósitos y 133 filas en la prueba, `D/planes/migracion-staging/resultados/informe-fase-3.md:99`) |
| Levantes de los vivos | Sí | `ReleasesImporter.cs` (agrupados, DEF-MIG-003) |
| Último período facturado | Sí, como inicio de facturación | `LegacyDepositRowParser.cs:44-45` |
| **Prórroga del depósito** (`deposito.prorroga`) | **No** | BR-08-003 |
| **Posición de la mercancía** (`productodetalle_x_seccion`) | **No** | BR-03-006 (módulo 03) |
| **Órdenes de cargue y salidas abiertas, cobros de báscula «por facturar», facturas con saldo** | **No** | BR-08-004 |
| Tarifas y convenios | No: se configuran a mano | P13 (`plan-backend-paridad-legacy.md:62`); `DEC-041` |
| Histórico (salidas, guías, facturas cerradas) | No: se consulta en el legacy | P13 |
| Número legacy del depósito | Se guarda, pero no se muestra ni se busca | BR-08-006; `ROADMAP.md:113` pedía conservarlo «como referencia» |
| FOB/CIF | Sí, pero sin validar la equivalencia | Pendiente ya registrado: `D/contexto/estado.md` §4 n.º 8 |

**Riesgo FOB/CIF** (`D/analisis/revision-fob-cif-migracion-v2-2026-10-08.md` §1-§2): `fob_dolares` del legacy, que su formulario rotula «CIF USD», entra como `FobUsd` (`ReleasesImporter.cs:54`), y `ingreso.preciomercancia`, que `vista_poliza` rotula FOB, entra como `CargoValue` (CIF) para facturar. Se cita el pendiente; no se duplica como brecha. Afecta la regla R-19 (`NO_VERIFICADO`).

**Pruebas:** `B/Wms.Tests/Administration/LegacyCsvReaderTests.cs`, `B/Wms.Tests/Administration/LegacyImport/*` (7 archivos), `B/Wms.IntegrationTests/Administration/{LegacyLocationsImportTests,LegacyReleasesImportTests,LegacyMigrationScenario}.cs`.

## 4. Notificaciones — CF-V082 (tiempo real) y CF-V087 (correo)

| Pieza | Evidencia |
| --- | --- |
| Hub | `B/Wms.Api/Hubs/NotificationHub.cs:7-38`: `[Authorize]`, grupos `user:{id}` y `role:{rol}`; mapeado en `/hubs/notifications` (`Program.cs:163`). Token por query `access_token` solo bajo `/hubs` (`B/Wms.Api/Common/Identity/WmsAuthentication.cs:62-64`) |
| Envío | `NotificationOrchestrator.cs:32-115`: persiste una fila por usuario activo del rol y la empuja por `SignalRNotifier` (`ReceiveNotification`). Los errores se registran y no cortan la operación de negocio |
| Endpoints | `GET user/{id}/notifications` (filtro `isRead`, paginado), `POST user/{userId}/notifications/{notificationId}/read`, `POST user/{id}/notifications/read-all`, `GET user/{id}/notifications/unread-count`. Todos con `ActiveUser` y la comprobación de que `{id}` es el usuario del token (`B/Wms.Api/Controllers/v1/UserController.cs:152-208`) |
| Cliente | `F/plugins/signalr.client.ts:13-99`: conecta al iniciar sesión, reconecta a los 0, 2, 5, 10 y 30 s y se detiene al cerrar sesión. `F/features/users/composables/useNotifications.ts:35-118`: panel (página 1 de 15), contador y toast al recibir. Página `F/pages/notifications/index.vue` (filtros Todas, No leídas y Leídas, y paginación). Menú `F/components/layout/AppMenu.vue:9-14` |
| Contrato | `NotificationDto` (`B/Wms.Application/Users/Queries/GetNotifications/NotificationDto.cs`) ↔ `INotification` (`F/features/users/types/notification.ts`): coinciden campo a campo. El TS acepta el nivel `Success`, que el enum del backend no tiene (`B/Wms.Domain/Enums/NotificationLevel.cs:3-9`): es inofensivo |
| **Orden** | `GetNotificationsHandler.cs:35-36`: `OrderBy(CreatedAt).ThenBy(Id)`, ascendente. El panel y la página 1 muestran **los más antiguos** → BR-08-014 |
| Reconexión | Si el primer `start()` falla, la conexión queda nula y no se reintenta hasta un nuevo inicio de sesión (`signalr.client.ts:58-64`). La escucha se intenta adjuntar 5 veces en 5 s (`useNotifications.ts:82-96`). No hay sondeo de respaldo → BR-08-010 |
| Correo (CF-V087) | `B/Wms.Infrastructure/Services/NotificationService.cs`: todo correo va a `Notifications:AdminEmails` (`:30-33,619-635`), con `Notifications:Enabled` (`:36`). Hora en UTC (`:124,201,298,403,490,594`). `NotifyUsersAsync` con correo lo envía como rol «Users» (`NotificationOrchestrator.cs:52-60`) → BR-08-009. Lo usan 7 flujos con `sendEmail: true` (búsqueda en `B/Wms.Application`): recepción sin báscula, cargue, correcciones de peso y de fecha, validación de depósito y vencimiento de facturas. `B/EMAIL_CONFIGURATION.md` solo documenta el SMTP de recuperación de contraseña, no `Notifications:*` |
| Navegación | La página no enlaza la entidad (`D/planes/paridad-legacy/plan-frontend-paridad-legacy.md:2700`, §G.13; F7-NOT-007 OBS) → incluido en BR-08-010 |

## 5. Centro de ayuda — CF-V083

- Páginas `F/pages/ayuda/index.vue` y `F/pages/ayuda/[numero].vue`, públicas: el middleware deja pasar `/ayuda` sin sesión (`F/middleware/auth.global.ts:19-20`), con layout según haya sesión o no (`useHelpLayout`). Entrada en el menú (`AppMenu.vue:21-29`).
- Datos: `catalogo.json` del bucket público, leído con `$fetch` sin token (`F/features/help/services/help-catalog-service.ts:7-12`). La URL sale de `NUXT_PUBLIC_AYUDA_BASE_URL` (`nuxt.config.ts:32-34`); vacía, la página avisa que no hay videos (`useHelpCatalog.ts:8-17`).
- Sin backend: el despliegue del bucket, la lectura pública, el CORS y la publicación están en `B/deploy/ayuda/README.md` y `cors-ayuda.json`, y los hace el usuario. `scripts/deploy-staging.sh` pasa `AYUDA_BASE_URL` al `yarn generate` (comentario `:24-25`).
- Pendiente ya registrado: no consta que los 81 videos estén publicados ni que F7 esté aprobada (`D/contexto/estado.md` §4 n.º 10 y §7). No se duplica como brecha.

## 6. SystemController — CF-V085

- Único endpoint: `GET system/dian-trm/today`, con `[Authorize]` (cualquier usuario con sesión). Devuelve la TRM USD de la DIAN del día de Colombia, con caché, o 503 `DIAN_UNAVAILABLE` (`B/Wms.Api/Controllers/v1/SystemController.cs:11-47`). **No es un estado del sistema.**
- Sin consumidor: la búsqueda `dian-trm` y `system/` en `F/` solo encuentra `administration/system-roles` y los parámetros del sistema. No tiene decisión DF3 ni de otro tipo.
- **No hay endpoint de salud:** la búsqueda `AddHealthChecks`, `MapHealthChecks` y `/health` en `B/` no encuentra nada. `compose.staging.yaml` solo tiene `healthcheck` para Postgres (`:20-24`). La prueba de humo usa el 400 del login (`B/scripts/deploy-staging.sh:209-223`). → BR-08-011.
- La lógica de la TRM y la alerta de «tasa desactualizada» del legacy son del módulo 06.

## 7. Jobs — CF-V086 (solo infraestructura)

Todos se registran en `B/Wms.Api/Program.cs:77-82`. Las pruebas de integración los quitan (`B/Wms.IntegrationTests/Infrastructure/WmsApiFactory.cs:38-45,114-115`). Cada corrida usa su propio scope, registra la excepción y no tumba el proceso.

| Job | Primera corrida | Frecuencia / hora | Zona horaria | Idempotencia | Errores | Interruptor | Lógica |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `OverdueDetectionBackgroundService` | 30 s | cada 24 h desde el arranque | No anclado (intervalo) | Recalcula estados (la evalúa el módulo 06) | log; sigue | No | 06 |
| `InvoicePaymentReconciliationBackgroundService` | 45 s | cada 24 h desde el arranque | No anclado | Recalcula (06) | log; sigue | No | 06 |
| `StoragePeriodAutoCloseBackgroundService` | 30 s | dinámica, de 5 min a 24 h hasta el próximo vencimiento (`:74-108`) | `UtcNow` para la espera | Cierra lo vencido (06) | log; reintento a los 5 min (`:64-71`) | No | 06 |
| `InvoiceDueNotificationBackgroundService` | 1 min | cada 24 h desde el arranque | No anclado | `DueNoticeSentAt` (`B/Wms.Application/Billing/Jobs/BillingJobService.cs:298,329`) | log; sigue | No | 06 |
| `AbandonmentAlertBackgroundService` | 1 min | diario a las 07:00 de Colombia (`B/Wms.Application/ForeignTrade/Jobs/AbandonmentAlertService.cs:22`) | `ColombiaTime.Now` | No repite el aviso del día (`AbandonmentAlertService.cs:53-56`) | log; sigue | No | 04 |
| `DatabaseBackupBackgroundService` | 2 min | diario a `Backups:DailyTime` (02:00) | `ColombiaTime.Now` | Uno exitoso por día; advisory lock | log; aviso a Admin | `Backups:Enabled` | 08 |

Brecha de infraestructura (BR-08-012): cinco jobs sin interruptor. Los tres de facturación con intervalo de 24 h vuelven a correr en cada arranque o redespliegue, a cualquier hora. Además, ninguno se protege si hay más de una instancia, salvo el registro del respaldo. Hoy staging tiene una sola instancia. No contradice lo que audita el módulo 04 (CF-V084, `modulos/04-ce-ingresos-depositos/05-analisis-v2.md:114`). El directorio del módulo 06 no existía al cerrar este informe.

**Modelo de despliegue frente al legacy:** el legacy dependía de un cron del servidor (`L/cron.php`) y de alertas que el navegador evaluaba al abrir el panel (`L/inicial.php:78`). La v2 ejecuta todo dentro del proceso del API y no necesita cron. Por eso un API caído o reiniciado detiene o reprograma los procesos, y nadie lo vigila si no hay endpoint de salud (BR-08-011).

## 8. Parte B — búsqueda de restos de Colmotores y del portal

**Términos buscados** (sin distinguir mayúsculas): `colmotores`, `\bVIN\b`, `vines`, `voltaje`, `voltage`, `\bserial`, `lectura`, `patio`, `portal`, `reportesweb`, `salida externa`, `ExternalYard`, `chasis|chassis`, `averia|avería`, `usuariocliente|ClientUser|CustomerUser|CustomerPortal|customer-portal`, `placacolmotores|vehiculo_x_convenio`. En el backend también `\bVin[A-Z]\w*`, `SerialNumber`, `Voltage`, `sonvehiculos` y el id `70` en `Wms.Application/Administration/LegacyImport`.

**Carpetas:** `B/` completo (`*.cs`, `*.json`, `*.sql`, incluidas `Wms.Infrastructure/Migrations`, excluidos `bin/`, `obj/`, `publish/` y `artifacts/`), `F/`, `Frontend/wms/stores`, `Frontend/wms/server`.

**Resultado:**

| Término | Backend | Frontend | Lectura |
| --- | ---: | ---: | --- |
| `colmotores`, `VIN`, `vines`, `voltaje`, `voltage`, `salida externa`, `ExternalYard`, `chasis`, `avería`, tablas del portal, `placacolmotores` | 0 | 0 | Sin restos |
| `serial` | 22 archivos | 0 | Todos son serialización JSON (filtro `serializ`: 0 restantes) |
| `lectura` | 26 | 32 | «Solo lectura» y similares |
| `patio` | 16 | 5 | Ubicaciones semilla genéricas `PATIO-01`/`PATIO-02` y comentarios «Bodega/Patio» (`F/features/warehouse/README.md:1`) |
| `portal`, `reportesweb` | 0 | 2 | Comentarios que citan el portal como origen del reporte de agencias (`F/pages/reports/customs-agency-entries.vue:4-5`; `F/features/reports/types/customs-agency-entries.ts:4`) |

**Dependencias:** ninguna entidad de depósito, levante, salida, recepción o producto tiene VIN, serial o voltaje (búsqueda en `B/Wms.Domain`, `B/Wms.Application`, `B/Wms.Api`). No hay enums, tablas EF, endpoints, rutas ni textos de menú de Colmotores. El menú lateral no tiene grupo Colmotores (`F/components/layout/AppMenu.vue`, 538 líneas, sin coincidencias). Lo que queda de los conceptos vecinos ya está decidido:

- precarga por placa: `GET weighbridge/lookup` existe sin uso por decisión (`plan-frontend-paridad-legacy.md`, §A.3, último punto; GAP-018). Es la versión no Colmotores de `vehiculo_x_convenio`, que llenaba `CF-L262`;
- seriales por unidad fuera de Colmotores: BR-04-009 (módulo 04);
- módulo 01: colores de vehículo (`CF-L013…016`) y usuarios del portal (`CF-L099`), sin restos.

**Datos de Colmotores en la migración:** el importador no filtra al cliente 70; la exclusión vive en las consultas de exportación (R-12). La consulta de productos no excluye los productos vehiculares de Colmotores (`plan-backend-paridad-legacy.md:2846`). Puede haber metido modelos de vehículo en el catálogo de productos. Sin acceso a `db_legacy/` no se puede comprobar: queda como incertidumbre.

## 9. Endpoints sin consumidor y llamadas sin endpoint

| Endpoint | Consumidor en `F/` | Justificación |
| --- | --- | --- |
| 6 de respaldos (`administration/backup-destinations*`, `administration/backups/*`) | Ninguno | DF3 y P14: por API (`plan-frontend-paridad-legacy.md:43,56`; `B/deploy/staging/README.md:159-160`). Intencional |
| 5 de importación legacy (`administration/legacy-import/*`) | Ninguno | DF3. Intencional |
| `GET system/dian-trm/today` | Ninguno | **Sin decisión** → BR-08-011 |

**Llamadas del frontend sin endpoint** en este módulo: ninguna. Las 4 rutas de notificaciones y el hub existen; el catálogo de ayuda va al bucket, no al API.

## 10. SOLO_V2 confirmadas

| ID | Capacidad | Confirmación |
| --- | --- | --- |
| CF-V080 | Respaldos con destinos configurables | Confirmada. Reemplaza y amplía `CF-L004` |
| CF-V081 | Importación legacy por CSV con simulación, conciliación y apertura de facturación | Confirmada |
| CF-V082 | Notificaciones en tiempo real y persistidas | Confirmada |
| CF-V083 | Centro de ayuda con videos | Confirmada (solo frontend y bucket) |
| CF-V085 | `SystemController` | **Corregida:** es la TRM de la DIAN del día, no el estado del sistema |
| CF-V086 | Infraestructura de jobs en segundo plano (nueva) | Confirmada |
| CF-V087 | Avisos por correo SMTP a la lista de administradores (nueva) | Confirmada |
