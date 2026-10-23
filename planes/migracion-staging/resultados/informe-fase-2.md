# Informe de la fase 2: preparar y desplegar staging

> **Fecha:** 2026-10-06. **Ejecutor:** agente (Opus 5.5).
> **Build desplegado:** BE `bf2dea6` / FE `4799cc4` (`develop` de los dos repos), más los cambios de configuración de esta fase, sin commit.
> **Plan:** `docs/planes/migracion-staging/plan-migracion-legacy-staging.md` §5. **Prompt:** `prompt-fase-2.md`.
> **Servidor:** AWS Lightsail de julio (Ubuntu, x86_64, 4 GB). URLs: `https://app.100-60-89-139.sslip.io` y `https://api.100-60-89-139.sslip.io/api/v1`.
> **Secretos:** este informe nombra claves, nunca valores.

## Veredicto

**Staging desplegado con el build candidato, la base recreada con las 10 migraciones actuales, los respaldos activos y el correo de Gmail configurado. No tiene datos migrados:** la migración es la fase 3.

Quedan dos tareas del usuario (§6): cambiar la contraseña del `admin` en el primer ingreso y crear el destino de respaldo Local.

---

## 1. Inventario previo (solo lectura)

| Elemento | Estado antes del despliegue |
|---|---|
| Contenedores | `wms-api` (imagen del 2026-08-10), `caddy:2` y `postgres:18.0`, arriba desde el 2026-07-17 |
| API | `Wms.Api/1.0.0` del 2026-08-10, sin `pg_dump` |
| Base `wms_staging` | 15 MB, 22 migraciones de la cadena vieja (`20260605155310_InitialDb` … `20260717214122_FixRolesCreatedAt`) |
| Datos de prueba | 8 usuarios, 107 terceros, 14 depósitos, 15 servicios, 24 ingresos, 17 ciclos de báscula, 26 facturas, 15 pagos, 1 orden de cargue, 1 guía, 567 auditorías |
| Volúmenes | `pgdata`, `caddy_data`, `caddy_config` (73 MB en total) |
| `/opt/wms/` | `deploy/` (compose y Caddyfile idénticos a los del repo), `site/` (68 MB), `data/uploads/` (1 archivo); sin `backups/` |
| Recursos | Disco 6,7 de 77 GB; RAM 3,7 GB (2,6 disponibles); swap 2 GB casi sin uso |

## 2. Configuración

**`.env.staging`:**
- Tiene todas las claves de `.env.staging.example`, sin duplicados ni claves sobrantes.
- `SMTP_HOST=smtp.gmail.com`, puerto 587, y `NOTIFICATIONS_ENABLED=true`.
- `NOTIFICATIONS_ADMIN_EMAILS` y `BOOTSTRAP_ADMIN_EMAIL` son `capb.dev@gmail.com` (D4).
- `POSTGRES_PASSWORD`, `JWT_KEY` (≥ 32), `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL` y `BOOTSTRAP_ADMIN_PASSWORD` están definidos. La contraseña del admin cumple la política.
- El usuario no tuvo que cambiar ningún valor.

**Cambios versionados (sin commit):**

| Archivo | Cambio |
|---|---|
| `deploy/staging/compose.staging.yaml` | En `wms-api`: `Backups__Enabled=true`, `Backups__DailyTime=02:00`, `Backups__TempPath=/tmp` y el montaje `/opt/wms/backups:/opt/wms/backups`. |
| `scripts/deploy-staging.sh` | `bootstrap` crea `/opt/wms/backups` (dueño 1654, modo 750). `migrate` contaba mal las migraciones esperadas: el filtro `Designer\|Snapshot` descartaba `AddDispatchGuideLineReleaseSnapshot`, y ahora solo excluye `*.Designer.cs` y `*ModelSnapshot.cs`. |
| `deploy/staging/README.md` | Sección Respaldos: staging ya los trae activos (FB-BAK-006 resuelto), con la carpeta del host y los pasos del destino Local. Sección Correo: Gmail real, solo hacia direcciones del equipo (D4); se quitó la mención a Mailtrap. |

## 3. Artefactos

- **`staging.sql`:**
  - Regenerado con `dotnet ef migrations script --idempotent`. Trae las 10 migraciones, de `20261001193201_InitialParityLegacy` a `20261006034830_AddEntryLogServiceDiscardedAt`, y ninguna de la cadena vieja.
  - Probado antes del despliegue en un Postgres 18.0 desechable: dos aplicaciones seguidas sin error, con 10 migraciones, 6 roles y 89 tablas.
- **Imagen `wms-api:staging`** (linux/amd64): corre como UID 1654 y trae `pg_dump` 18.6 (`postgresql-client-18`, PGDG).
- **Frontend:** `yarn generate` con `NUXT_PUBLIC_API_BASE=https://api.100-60-89-139.sslip.io/api/v1`. Pesa 80 MB y no tiene referencias a `localhost`.

## 4. Despliegue (aprobado por el usuario en el chat)

El usuario dijo que no hacía falta respaldar la base anterior, porque eran datos de prueba.

1. `bootstrap`: idempotente; creó `/opt/wms/backups`.
2. `config`: subió el compose nuevo, el Caddyfile y el `.env`.
3. Transferencias:
   - la imagen, con `docker save | gzip | ssh docker load`;
   - el frontend, con `rsync --delete` a `/opt/wms/site/`.
4. `docker compose down` sin `-v`, y luego `docker volume rm wms-staging_pgdata`. **`caddy_data` y `caddy_config` se conservaron.**
5. `dbup`: Postgres limpio y healthy.
6. `migrate`: **10 migraciones (esperado 10) y 6 roles.**
7. `up`: los tres contenedores arriba. Caddy reutilizó los certificados.

## 5. Verificación

| Comprobación | Resultado |
|---|---|
| Arranque del API | `Application started`, `Hosting environment: Production`, sin `fail`, `crit` ni excepciones |
| Admin inicial | `Bootstrap admin 'admin' creado con rol Admin (debe cambiar contraseña en el primer login)`; 1 usuario en la base |
| Job de respaldos | `DatabaseBackupJob iniciado. Hora de ejecución: 02:00 (Colombia).` |
| Variables `Backups__*` en el contenedor | Presentes; `/opt/wms/backups` escribible por el contenedor; `pg_dump` en `/usr/bin` |
| `smoke`: frontend y SPA fallback | 200 y 200 |
| `smoke`: login inválido | 400, «Credenciales inválidas» (error en español) |
| `smoke`: CORS | `access-control-allow-origin: https://app.100-60-89-139.sslip.io` |
| Swagger | 404 (apagado) |

**Advertencias del log, todas conocidas o benignas:**
- **DataProtection guarda sus llaves dentro del contenedor.** Las llaves se pierden al recrear el contenedor: los enlaces de recuperación de contraseña emitidos antes de un redespliegue dejan de servir. Ya pasaba en julio.
- **`FormulaType.ParameterSchema` no tiene comparador de valores.** También aparece en local.
- **`URLS` sobrescribe `HTTP_PORTS`.** Es la configuración esperada.

## 6. Pendientes

1. **Del usuario:**
   - entrar con `admin` y cambiar la contraseña obligatoria;
   - crear por el API un destino **Local** con carpeta `/opt/wms/backups` y probarlo (`POST /api/v1/administration/backup-destinations` y `…/{id}/test`; el frontend no tiene pantalla de respaldos; comandos en el README, sección Respaldos). Sin un destino activo, el job de las 02:00 no tiene dónde escribir.
2. **Verificaciones del §5.7 del plan que piden el login del Admin:**
   - entrar como Admin;
   - enviar un correo de prueba con la recuperación de contraseña a `capb.dev@gmail.com`.

   Quedan para el usuario o para la fase 4.
3. **Limpieza opcional:**
   - dos imágenes huérfanas en el servidor, entre ellas la del API de agosto: `docker image prune`;
   - la foto de `uploads` de agosto quedó huérfana.
4. **Sugerencia aparte (no es un defecto de la migración):** persistir las llaves de DataProtection en un volumen.
