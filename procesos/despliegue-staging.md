# Despliegue a staging

> **Para qué sirve:** resumen de cómo se despliega y opera staging. El procedimiento completo es el runbook `Backend/wms-api/deploy/staging/README.md`, que manda sobre este resumen.
> **Regla:** todo despliegue, migración o restauración en staging necesita la aprobación explícita del usuario. Staging tiene datos migrados del legacy y lo usan operarios.

## 1. El ambiente

- Una instancia de **AWS Lightsail** con Docker Compose: Postgres, API .NET y Caddy. Caddy sirve el frontend estático y el API con HTTPS de sslip.io.
- Frontend `https://app.100-60-89-139.sslip.io` · API `https://api.100-60-89-139.sslip.io/api/v1`.
- Los videos del centro de ayuda se sirven desde un bucket de Lightsail Object Storage (`Backend/wms-api/deploy/ayuda/README.md`).
- Conexión y secretos: `deploy/staging/.env.deploy` y `.env.staging`, fuera de git. No muestres su contenido ni lo copies.

## 2. Comandos (`Backend/wms-api/scripts/deploy-staging.sh`)

| Subcomando | Qué hace |
| --- | --- |
| `backend` | `dotnet publish -r linux-x64` nativo en el Mac + imagen delgada (`Dockerfile.staging`) y carga en el servidor. No uses el Dockerfile multistage bajo QEMU |
| `frontend` | `yarn generate` contra el API de staging y `rsync` a `/opt/wms/site` |
| `config` | Sube `compose.staging.yaml`, `Caddyfile` y `.env` |
| `migrate` | Aplica `deploy/staging/artifacts/staging.sql`, generado con `dotnet ef migrations script --idempotent`, y verifica `__EFMigrationsHistory` |
| `up`, `logs`, `smoke` | Levantar, ver logs, pruebas de humo |
| `bootstrap`, `dbup`, `all` | Primer aprovisionamiento |

Redespliegue típico tras un cambio de código: `backend` y reinicio de `wms-api`, y `frontend`. Si hay migraciones nuevas, primero `migrate`.

## 3. Antes de desplegar

1. Confirma con el usuario los commits a desplegar y la ventana (hay operarios probando).
2. Haz un respaldo manual (`POST administration/backups/run`) y anota su nombre.
3. Revisa si el cambio trae migraciones. Staging se actualiza en sitio; recrear `pgdata` exige un «sí» explícito del usuario.

## 4. Después de desplegar

- `smoke` y una revisión rápida con el rol afectado.
- Registra en el informe o plan correspondiente: fecha, commits BE/FE desplegados, migraciones aplicadas y respaldo previo. Actualiza `contexto/estado.md` §3.

## 5. Respaldos

- La API respalda la base y los archivos subidos a diario a las 02:00 (Colombia) en los destinos activos (`/api/v1/administration/backup-destinations`, solo Admin). Retiene 30 diarios y 12 mensuales; los manuales no se borran.
- En staging el destino es Local, en `/opt/wms/backups`. Nombre del archivo: `wms_{aaaammdd_hhmmss}_{id8}.dump`.
- **Destino externo (BR-08-001, plan de brechas P1 fase 10; se aplica en la fase 13):** además del Local, un destino S3 llamado `s3-externo` en un bucket **privado** de Lightsail Object Storage en otra región. El usuario crea el bucket y la clave de acceso, y guarda `BACKUP_S3_ACCESS_KEY_ID` y `BACKUP_S3_SECRET_ACCESS_KEY` solo en `deploy/staging/.env.staging`; `compose.staging.yaml` las pasa como `Backups__S3Credentials__s3-externo__*`. Con aprobación: `scripts/deploy-staging.sh config`, recrear `wms-api`, crear el destino (Postman «3b. Crear destino S3»), probarlo y correr un respaldo con dos destinos `Succeeded`. Pasos completos en `Backend/wms-api/deploy/staging/README.md`.
- **Correo de fallo:** un respaldo `Failed` o `PartiallySucceeded` envía «[WMS] Falló el respaldo del dd/MM/aaaa» a los Admin activos y a `Notifications:AdminEmails`, sin repetir, aunque la base esté caída o `Notifications:Enabled` esté apagado. Antes de provocar un fallo para probarlo, verifica que esos correos sean de cuentas reales.
- La restauración se describe en el runbook. Restaurar borra lo que los operarios hicieron después: solo con aprobación del usuario.

## 6. Cuidado

- El agente no escribe contraseñas en el navegador: el usuario inicia sesión y el agente usa esa sesión.
- No edites datos migrados del legacy para probar. Usa los datos de práctica (`PRAC-`) o crea datos marcados `QA-…`.
- Los uploads viven en `/opt/wms/data/uploads`, no en `/opt/wms/uploads`.
