# 08-procesos-infra-fuera-alcance — 09 Integraciones

> AG-08 · 2026-10-23 · Trazas estáticas (no se ejecutó nada). **Prefijos:** `B/` = `Backend/wms-api/`; `F/` = `Frontend/wms/app/`; `L/` = `bodegas-legacy/`; `D/` = `docs/`. Rutas con prefijo `/api/v1`.

## 1. Operaciones principales

### T-01 · Respaldo manual (CF-V080.b)

Cliente HTTP con token de Admin (colección `B/deploy/postman/wms-respaldos.postman_collection.json`, pasos 1 y 5)
→ `POST /api/v1/administration/backups/run`. `BackupsController.Run` (`B/Wms.Api/Controllers/v1/BackupsController.cs:88-99`), con `AdminOnly` y el autor tomado del token
→ `RunBackupCommand` → `BackupService.StartManualAsync` (`B/Wms.Application/Administration/Backups/Common/BackupService.cs:57-77`): advisory lock, `BackupRun` en `Running` y `Task.Run` con scope propio
→ **202** `BackupRunStartedDto`, o **409** «Ya hay un respaldo en curso.»
→ en segundo plano, `ExecuteAsync` (`:106-186`): `PgDumpRunner.DumpDatabaseAsync` (`pg_dump`, proceso externo) y `ArchiveUploadsAsync` (`tar.gz`); por destino, `LocalBackupTarget` o `S3BackupTarget.UploadAsync`; luego `run.Finish` → `backup_runs`; retención (`:214-260`); aviso si falla (`:262-288`)
→ consulta: `GET /api/v1/administration/backups/runs` (paginado).

Sin frontend, por DF3. Validado en FB-BAK-003 (`D/qa/resultados/F11-informe-S6-2026-10-06.md:160`).

### T-02 · Respaldo programado (CF-V080.b, CF-V086)

Host → `DatabaseBackupBackgroundService.ExecuteAsync` (`B/Wms.Api/BackgroundJobs/DatabaseBackupBackgroundService.cs:20-56`). Sale si `Backups:Enabled = false`. Espera 2 min y calcula `DelayUntilNextRun(ColombiaTime.Now, 02:00)`
→ `BackupService.RunScheduledAsync` (`BackupService.cs:79-104`): `ShouldRunToday` decide si corre y `ScheduledKind` si es `Daily` o `Monthly`
→ T-01 desde `ExecuteAsync`.

Configuración: `B/deploy/staging/compose.staging.yaml:78-82`. Validado: corrida `96640179` `Daily` `Succeeded` el 07/10 a las 02:00 (`D/planes/migracion-staging/resultados/informe-fase-5.md:44,136-137`).

### T-03 · Restauración (CF-V080.e)

Operador con SSH al servidor → `docker cp` del `.dump` → `pg_restore --clean --if-exists` en el contenedor de Postgres → `tar -xzf uploads_….tar.gz` en `/opt/wms/data/uploads` y `chown 1654` (`B/deploy/staging/README.md:205-217`). Exige aprobación del usuario (`D/procesos/despliegue-staging.md:4,41`). Validado en FB-BAK-005 (`F11-informe-S6-2026-10-06.md` §4.9).

### T-04 · Carga de un CSV legacy (CF-V081.a)

Exportación MySQL fuera de la aplicación, con las consultas de `D/planes/paridad-legacy/plan-backend-paridad-legacy.md` §C.6. CSV con `;` en UTF-8.
→ `POST /api/v1/administration/legacy-import/{entity}` (multipart: `file`, `headerRows`, `dryRun`) → `LegacyImportController.Import` (`B/Wms.Api/Controllers/v1/LegacyImportController.cs:39-54`): `AdminOnly`; archivo vacío → 400
→ `ImportLegacyFileCommandHandler.Handle` (`…/Commands/ImportLegacyFile/ImportLegacyFileCommandHandler.cs:23-97`). Hace en orden:
  1. `ParseEntity`: entidad desconocida → 400.
  2. `LegacyCsvReader.Read`: detecta codificación y separador.
  3. Valida el tamaño: más de 50.000 filas → 400.
  4. Abre una transacción.
  5. Llama a `importer.ImportAsync`, que por fila hace `Parse`, consulta `legacy_id_map`, aplica la fila y anota la correspondencia (`LegacyImporterBase.cs:34-66`); en depósitos, por grupo `nro_deposito` (`DepositsImporter.cs:30-120`).
  6. Agrega `LegacyImportBatch` y hace `SaveChanges`.
  7. Si es simulación, `Rollback`; si es firme, `Commit`.
→ respuesta `LegacyImportResultDto` (`batchId`, cuentas y hasta 500 errores)
→ `GET …/legacy-import/batches/{id}` para ver el lote con hasta 1.000 errores.

Orden obligatorio: ciudades (`POST /administration/cities/import`), embalajes, cuadrillas, ubicaciones, clientes, agencias, transportadoras, vehículos, conductores, productos, depósitos, levantes (`plan-backend-paridad-legacy.md` §C.6.1).

### T-05 · Conciliación (CF-V081.c)

CSV de depósitos reexportado el día del corte → `POST …/legacy-import/reconciliation` (`LegacyImportController.cs:84-93`) → `ReconcileDepositsCommandHandler` (`…/Commands/ReconcileDeposits/ReconcileDepositsCommand.cs:28-104`). Por fila hace:
  1. `ParseForReconciliation`.
  2. `LoadAsync(número legacy)`: depósito migrado, productos, levantes y movimientos que no son `MigrationOpening`.
  3. `DepositReconciler.Reconcile`.

→ `DepositReconciliationDto` (resumen, filas y errores). No escribe nada (verificado en `D/planes/migracion-staging/resultados/informe-fase-1.md:127-133`).

### T-06 · Apertura de la facturación de los migrados (CF-V081.d)

Tarifas configuradas a mano (P13, `DEC-041`) → `POST …/legacy-import/open-billing` (`{ warehouseStorageIds? }`) → `OpenMigratedBillingCommandHandler` (`…/Commands/OpenMigratedBilling/OpenMigratedBillingCommand.cs:43-133`). Por depósito, en su propio scope y transacción:
  1. `StorageBillingService.OpenPeriodWithInvoiceAsync(id, cliente, StoragePeriodOpenOptions(true, BillingStartDate))`.
  2. `Commit`.
  3. `StorageBillingNotifier.NotifyBillingWarningsAsync`, que avisa a Facturación de la TRM pendiente y de las advertencias.

→ `[{ id, número, número legacy, Opened | Skipped | Failed, mensaje }]`. Validado: 128 Opened en staging (`D/planes/migracion-staging/resultados/informe-fase-3.md:27,192`).

### T-07 · Aviso en tiempo real (CF-V082)

Handler de negocio, por ejemplo `StorageBillingNotifier` o `BackupService.NotifyFailureAsync`
→ `INotificationOrchestrator.NotifyRoleAsync(rol, params, sendEmail)` (`B/Wms.Api/Services/NotificationOrchestrator.cs:69-115`). Hace en orden:
  1. `UserManager.GetUsersInRoleAsync`, solo usuarios activos.
  2. Crea un `Notification` por usuario y hace `SaveChanges`.
  3. `SignalRNotifier.SendToUserAsync`, grupo `user:{id}`, método `ReceiveNotification` (`B/Wms.Api/Services/SignalRNotifier.cs:21-28`).
  4. Opcional: correo (T-09).

→ hub `/hubs/notifications` (`B/Wms.Api/Hubs/NotificationHub.cs`, `[Authorize]`; token por `access_token`, `B/Wms.Api/Common/Identity/WmsAuthentication.cs:62-64`)
→ cliente `F/plugins/signalr.client.ts` (conexión abierta al iniciar sesión)
→ `useNotifications.onReceiveNotification` (`F/features/users/composables/useNotifications.ts:68-77`): invalida `["notifications"]` y `["notifications-unread-count"]` y muestra un toast según el nivel.

Validado: F7-NOT-001 y 002 PASA (`D/qa/resultados/F7-informe-2026-10-03.md:72-73`).

### T-08 · Bandeja de avisos (CF-V082)

Campana (`F/features/users/components/NotificationPanel.vue`) o página `F/pages/notifications/index.vue`
→ `UserService.getNotifications(userId, { pageIndex, pageSize, isRead })` → `GET /api/v1/user/{id}/notifications` (`UserController.cs:152-165`, `ActiveUser`, 403 si `{id}` no es el usuario del token)
→ `GetNotificationsHandler` (orden **ascendente**, `:35-36`, BR-08-014)
→ `PaginatedList<NotificationDto>` → la lista se pinta tal cual. Leer: `POST …/notifications/{notificationId}/read` y `…/read-all`. Contador: `GET …/notifications/unread-count`.

Contrato: `NotificationDto` ↔ `INotification`, iguales campo a campo (`level` como texto por `JsonStringEnumConverter`, `B/Wms.Api/Program.cs:63`).

### T-09 · Correo de avisos (CF-V087)

`NotificationOrchestrator` con `sendEmail: true` → `INotificationService.NotifyRoleAsync` (`B/Wms.Infrastructure/Services/NotificationService.cs:517-615`) → `SendToAdminsAsync` → `IEmailService.SendEmailToMultipleAsync(Notifications:AdminEmails)` → SMTP (`Email__*` en `compose.staging.yaml:59-64`; los valores están en el `.env` del servidor, que no se abrió). Staging usa Gmail real, solo hacia direcciones del equipo (`B/deploy/staging/README.md:263-274`).

### T-10 · Centro de ayuda (CF-V083)

`/ayuda`, pública (`F/middleware/auth.global.ts:19-20`) → `useHelpCatalog` (`F/features/help/composables/useHelpCatalog.ts:7-35`) → `$fetch("catalogo.json", { baseURL: NUXT_PUBLIC_AYUDA_BASE_URL })` sin token (`help-catalog-service.ts:7-12`) → bucket público de Lightsail → reproductor de MP4 y VTT con `Range` y CORS (`B/deploy/ayuda/cors-ayuda.json`). Publicación: `npm run catalogo` y `npm run publicar` desde `Frontend/wms/tools/video-tutoriales` (`B/deploy/ayuda/README.md:141-159`). La URL queda compilada en el build (`:175-177`).

### T-11 · TRM del día (CF-V085)

Sin consumidor. `GET /api/v1/system/dian-trm/today` → `SystemController.GetTodayTrm` (`B/Wms.Api/Controllers/v1/SystemController.cs:18-44`) → `IDianTrmService.GetTrmAsync(ColombiaTime.Today, "USD")` (DIAN, `appsettings.json:12-18`) → 200 `{ date, currency, trm, fromCache }` o 503 `DIAN_UNAVAILABLE`.

## 2. Procesos automáticos, legacy frente a V2

| Legacy | Disparo legacy | V2 | Disparo V2 | Módulo que audita la lógica |
| --- | --- | --- | --- | --- |
| `L/menus/backup.php` | Manual, desde el menú o una URL directa | `DatabaseBackupBackgroundService` + `POST administration/backups/run` | Diario 02:00 de Colombia + manual por API | 08 |
| `L/cron.php` | Cron del servidor (supuesto; no está en el checkout) | `StoragePeriodAutoCloseBackgroundService` | Dinámico, de 5 min a 24 h | 06 |
| `L/menus/evaluatasacambio.php` | AJAX al abrir el panel (nivel ≤ 1) | TRM a la DIAN al crear la factura (DEC-023); `GET system/dian-trm/today` sin uso | Al facturar | 06 |
| `L/menus/evaluaabandonos.php` | AJAX al abrir el panel (nivel ≤ 1) y el menú | `AbandonmentAlertBackgroundService` | Diario 07:00 de Colombia | 04 |
| — | — | `OverdueDetectionBackgroundService`, `InvoicePaymentReconciliationBackgroundService`, `InvoiceDueNotificationBackgroundService` | Cada 24 h desde el arranque | 06 |

## 3. Integraciones externas del módulo

| Integración | Dirección | Credenciales | Dónde se configura | Riesgo |
| --- | --- | --- | --- | --- |
| `pg_dump` / `pg_restore` | API → Postgres (proceso) | Cadena de conexión; clave por `PGPASSWORD` (`PgDumpRunner.cs:48-49`) | `ConnectionStrings`, `Backups:PgDumpPath`; imagen con `postgresql-client-18` | Versión del cliente distinta de la del servidor (mitigado en el Dockerfile) |
| S3 o compatible (respaldos) | API → bucket | `Backups:S3Credentials:{Name}:*` o el rol de la instancia (`S3BackupTarget.cs:39-40`) | Entorno del servidor | No configurado (BR-08-001) |
| SMTP | API → servidor de correo | `Email__*` en el `.env` | `compose.staging.yaml:59-64` | Correo real en staging; solo al equipo |
| Bucket del centro de ayuda | Navegador → bucket (lectura pública); equipo de publicación → bucket (clave) | Clave solo en el equipo que publica (`B/deploy/ayuda/README.md:79-97`) | `NUXT_PUBLIC_AYUDA_BASE_URL` / `AYUDA_BASE_URL` | Publicación no confirmada (`estado.md` §7) |
| SignalR (WebSocket) | Navegador ↔ API | JWT por query en `/hubs` | Caddy reenvía `/hubs` (`README.md:9`) | BR-08-010 |
| DIAN (TRM) | API → datos.gov.co | Ninguna | `appsettings.json:12-18` | Módulo 06 |
